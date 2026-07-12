"""M4 Legendary Buildings — types, prereqs, build path, VP, upkeep."""
from __future__ import annotations

import random

import pytest

from aeonis_sim.engine.build import apply_build, build_ap_cost, enumerate_builds
from aeonis_sim.engine.cleanup import run_cleanup
from aeonis_sim.engine.lords import (
    LEGENDARY_BUILDINGS,
    can_build_legendary,
    legendary_for_lord,
)
from aeonis_sim.engine.production import run_production
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BuildingType, Terrain


ROSTER = [
    "cassian", "seraphel", "vharok", "elyndra",
    "rakhis", "nyxara", "auriel", "thalrik",
]


def m4_state(lords: list[str] | None = None, seed: int = 9):
    lords = lords or ROSTER[:3]
    return build_initial_state(
        {
            "players": len(lords),
            "lord_asymmetry": {"enabled": True, "lords": lords},
        },
        random.Random(seed),
    )


def _stock_for_build(p, *, ap=10, gold=20, mana=20, influence=20, pop=10):
    p.ap, p.gold, p.mana, p.influence, p.pop_pool = ap, gold, mana, influence, pop


def _clear_city_for_legendary(state, pid: int):
    home = state.tiles[state.player(pid).home]
    home.buildings = []
    home.controller = pid
    return home


def _place_markets(state, pid: int, n: int = 2):
    """Place n Markets on controlled non-home tiles (free home City slots)."""
    home = state.player(pid).home
    placed = 0
    for t in state.controlled(pid):
        if t.coord == home:
            continue
        t.terrain = Terrain.CITY
        t.buildings = [BuildingType.MARKET]
        placed += 1
        if placed >= n:
            break
    assert placed >= n


def test_legendary_building_types_and_specs():
    assert len(LEGENDARY_BUILDINGS) == 8
    assert legendary_for_lord("cassian") == BuildingType.GRAND_EXCHANGE
    assert legendary_for_lord("thalrik") == BuildingType.DIMENSIONAL_NEXUS
    assert legendary_for_lord("") is None
    ge = BuildingType.GRAND_EXCHANGE
    from aeonis_sim.engine.types import BUILDING_SPECS
    assert BUILDING_SPECS[ge].terrain == Terrain.CITY
    assert BUILDING_SPECS[ge].pop == 3
    assert BUILDING_SPECS[ge].gold == 6
    assert BUILDING_SPECS[ge].influence == 3
    assert BUILDING_SPECS[BuildingType.IRON_CITADEL].upkeep_gold == 2
    assert build_ap_cost(m4_state(), BuildingType.GRAND_EXCHANGE) == 4


def test_grand_exchange_prereqs_and_cost():
    state = m4_state(["cassian", "seraphel", "vharok"])
    p = state.player(0)
    _clear_city_for_legendary(state, 0)
    _place_markets(state, 0, 2)
    _stock_for_build(p, gold=20, influence=10, pop=10)

    choices = enumerate_builds(state, 0)
    ge = [c for c in choices if c["building"] == "grand_exchange"]
    assert ge, "expected Grand Exchange when 2 Markets and 8+ gold"
    assert can_build_legendary(state, 0, BuildingType.GRAND_EXCHANGE)

    before_renown = p.renown
    apply_build(state, 0, ge[0], rng=random.Random(1))
    assert p.renown == before_renown + 2
    assert BuildingType.GRAND_EXCHANGE in state.tiles[tuple(ge[0]["hex"])].buildings
    assert p.gold == 20 - 6
    assert p.influence == 10 - 3
    assert p.pop_pool == 10 - 3
    assert p.ap == 10 - 4


def test_wrong_lord_cannot_build_anothers_legendary():
    state = m4_state(["cassian", "seraphel", "vharok"])
    # Seraphel (pid 1) meets Cassian resources but must not see Grand Exchange.
    p = state.player(1)
    _clear_city_for_legendary(state, 1)
    _place_markets(state, 1, 2)
    _stock_for_build(p)
    assert not can_build_legendary(state, 1, BuildingType.GRAND_EXCHANGE)
    choices = enumerate_builds(state, 1)
    assert not any(c["building"] == "grand_exchange" for c in choices)


@pytest.mark.parametrize(
    "lord,btype,setup",
    [
        (
            "cassian",
            BuildingType.GRAND_EXCHANGE,
            lambda s, pid: (_clear_city_for_legendary(s, pid), _stock_for_build(s.player(pid))),
        ),
        (
            "seraphel",
            BuildingType.ARCANE_SANCTUM,
            lambda s, pid: (
                _clear_city_for_legendary(s, pid),
                _stock_for_build(s.player(pid)),
                setattr(s.player(pid), "discoveries", ["a", "b"]),  # need 3
            ),
        ),
        (
            "vharok",
            BuildingType.IRON_CITADEL,
            lambda s, pid: (
                _clear_city_for_legendary(s, pid),
                _stock_for_build(s.player(pid)),
            ),
        ),
        (
            "elyndra",
            BuildingType.HEARTWOOD_SANCTUM,
            lambda s, pid: (
                _clear_city_for_legendary(s, pid),
                _stock_for_build(s.player(pid)),
            ),
        ),
        (
            "rakhis",
            BuildingType.WINDSWORN_WARCAMP,
            lambda s, pid: (
                _clear_city_for_legendary(s, pid),
                _stock_for_build(s.player(pid)),
                setattr(s.player(pid), "attacker_battle_wins", 1),
            ),
        ),
        (
            "nyxara",
            BuildingType.HALL_OF_WHISPERS,
            lambda s, pid: (
                _clear_city_for_legendary(s, pid),
                _stock_for_build(s.player(pid)),
                setattr(s.player(pid), "whispers_played", 3),
            ),
        ),
        (
            "auriel",
            BuildingType.CATHEDRAL_OF_RADIANCE,
            lambda s, pid: (
                _clear_city_for_legendary(s, pid),
                _stock_for_build(s.player(pid)),
                setattr(s.player(pid), "renown", 4),
            ),
        ),
        (
            "thalrik",
            BuildingType.DIMENSIONAL_NEXUS,
            lambda s, pid: (
                _clear_city_for_legendary(s, pid),
                _stock_for_build(s.player(pid)),
            ),
        ),
    ],
)
def test_legendary_prereq_fails(lord, btype, setup):
    # Three-player board; put the tested Lord in seat 0.
    others = [x for x in ROSTER if x != lord][:2]
    state = m4_state([lord] + others, seed=11)
    setup(state, 0)
    assert not can_build_legendary(state, 0, btype)
    assert not any(
        c["building"] == btype.value for c in enumerate_builds(state, 0)
    )


def test_cleanup_awards_two_vp_while_controlled():
    state = m4_state(["cassian", "seraphel", "vharok"])
    p = state.player(0)
    home = _clear_city_for_legendary(state, 0)
    home.buildings = [BuildingType.GRAND_EXCHANGE]
    before = p.vp
    run_cleanup(state, rng=random.Random(2))
    assert p.vp == before + 2
    assert p.vp_sources.get("legendary") == 2
    # Second cleanup awards again while still controlled (artifact-style).
    before2 = p.vp
    run_cleanup(state, rng=random.Random(3))
    assert p.vp == before2 + 2


def test_iron_citadel_upkeep_charged():
    state = m4_state(["vharok", "cassian", "seraphel"])
    p = state.player(0)
    home = _clear_city_for_legendary(state, 0)
    home.buildings = [BuildingType.IRON_CITADEL]
    # Zero out production noise: leave only the city tile controlled.
    for t in list(state.controlled(0)):
        if t.coord != home.coord:
            t.controller = None
    p.gold = 5
    run_production(state)
    assert p.gold == 5 - 2  # city prints 0 gold resources in AL-13; only upkeep


def test_attacker_battle_wins_and_whispers_played_serialize():
    state = m4_state(["rakhis", "nyxara", "cassian"])
    p = state.player(0)
    p.attacker_battle_wins = 2
    p.whispers_played = 4
    d = state.to_dict()
    restored = type(state).from_dict(d)
    assert restored.player(0).attacker_battle_wins == 2
    assert restored.player(0).whispers_played == 4
    cloned = state.copy()
    assert cloned.player(0).attacker_battle_wins == 2
    assert cloned.player(0).whispers_played == 4


def test_finish_battle_increments_attacker_wins():
    from aeonis_sim.engine import combat
    from aeonis_sim.engine.types import Unit, UnitType, UNIT_STATS

    state = m4_state(["rakhis", "cassian", "vharok"])
    # Minimal contested hex: defender owns target with a unit; attacker adjacent.
    origin = state.player(0).home
    target = next(
        c for c in state.tiles
        if c != origin and state.tiles[c].terrain != Terrain.LAKE
    )
    state.tiles[target].controller = 1
    state.tiles[target].units = [
        Unit(uid=state.new_uid(), owner=1, type=UnitType.INFANTRY,
             hp=UNIT_STATS[UnitType.INFANTRY].hp),
    ]
    state.tiles[origin].units = [
        Unit(uid=state.new_uid(), owner=0, type=UnitType.INFANTRY,
             hp=UNIT_STATS[UnitType.INFANTRY].hp),
    ]
    battle = combat.Battle(
        attacker=0, defender=1, target=target,
        att_committed=[(origin, state.tiles[origin].units[0])],
        def_committed=[(target, state.tiles[target].units[0])],
    )
    battle.winner = "attacker"
    assert state.player(0).attacker_battle_wins == 0
    combat.finish_battle(state, battle)
    assert state.player(0).attacker_battle_wins == 1


def test_whisper_play_increments_counter():
    from aeonis_sim.engine.whispers import apply_action_whisper

    state = m4_state(["nyxara", "cassian", "seraphel"])
    p = state.player(0)
    p.whisper_hand = ["hidden_cache"]
    apply_action_whisper(
        state, 0, {"type": "whisper_play", "card": "hidden_cache", "choice": "gold"},
    )
    assert p.whispers_played == 1

def test_grand_exchange_production_from_trades():
    from aeonis_sim.engine.lords.legendaries import apply_grand_exchange_production
    state = m4_state(['cassian', 'seraphel', 'vharok'])
    home = _clear_city_for_legendary(state, 0)
    home.buildings = [BuildingType.GRAND_EXCHANGE]
    state.trades_this_round = 3
    before = state.player(0).gold
    apply_grand_exchange_production(state, 0)
    assert state.player(0).gold == before + 3


def test_arcane_sanctum_production_and_lord_die():
    from aeonis_sim.engine.artifacts import attack_die
    from aeonis_sim.engine.lords.legendaries import apply_arcane_sanctum_production
    from aeonis_sim.engine.types import Unit, UnitType, UNIT_STATS
    state = m4_state(['seraphel', 'cassian', 'vharok'])
    home = _clear_city_for_legendary(state, 0)
    home.buildings = [BuildingType.ARCANE_SANCTUM]
    before = state.player(0).mana
    apply_arcane_sanctum_production(state, 0)
    assert state.player(0).mana == before + 2
    lord = Unit(uid=state.new_uid(), owner=0, type=UnitType.LORD, hp=UNIT_STATS[UnitType.LORD].hp)
    home.units.append(lord)
    die = attack_die(state, 0, lord)
    assert die >= 6  # base lord die bumped at least one step


def test_iron_citadel_siege_and_defense():
    from aeonis_sim.engine import combat
    from aeonis_sim.engine.lords.legendaries import legendary_defense_bonus
    state = m4_state(['vharok', 'cassian', 'seraphel'])
    home = _clear_city_for_legendary(state, 0)
    home.buildings = [BuildingType.IRON_CITADEL]
    home.controller = 0
    b = combat.Battle(attacker=1, defender=0, target=home.coord)
    assert legendary_defense_bonus(state, b, 'def') == 3
    assert legendary_defense_bonus(state, b, 'att') == 0
    choice = {'target': list(home.coord), 'cost': 0}
    state.player(1).ap = 5
    battle = combat.start_battle(state, 1, choice)
    assert battle.siege is True
    assert battle.cap == 5


def test_heartwood_production_and_hp():
    from aeonis_sim.engine.lords.legendaries import (
        apply_heartwood_production, apply_heartwood_round_start_hp,
    )
    from aeonis_sim.engine.types import Unit, UnitType, UNIT_STATS
    state = m4_state(['elyndra', 'cassian', 'vharok'])
    home = _clear_city_for_legendary(state, 0)
    home.buildings = [BuildingType.HEARTWOOD_SANCTUM]
    p = state.player(0)
    p.pop_pool = 0
    apply_heartwood_production(state, 0)
    assert p.pop_pool >= 3
    u = Unit(uid=state.new_uid(), owner=0, type=UnitType.INFANTRY, hp=1)
    home.units.append(u)
    apply_heartwood_round_start_hp(state)
    assert u.hp == 2


def test_cathedral_defense_bonus():
    from aeonis_sim.engine.lords.legendaries import legendary_defense_bonus
    from aeonis_sim.engine import combat
    state = m4_state(['auriel', 'cassian', 'vharok'])
    home = _clear_city_for_legendary(state, 0)
    home.buildings = [BuildingType.CATHEDRAL_OF_RADIANCE]
    b = combat.Battle(attacker=1, defender=0, target=home.coord)
    assert legendary_defense_bonus(state, b, 'def') == 2


def test_dimensional_nexus_counts_as_portal():
    from aeonis_sim.engine.lords import tile_is_portal
    state = m4_state(['thalrik', 'cassian', 'seraphel'])
    home = _clear_city_for_legendary(state, 0)
    home.buildings = [BuildingType.DIMENSIONAL_NEXUS]
    assert tile_is_portal(state, home.coord, 0)


def test_warcamp_cavalry_enumerate():
    from aeonis_sim.engine.lords.legendaries import enumerate_warcamp_cavalry_move
    from aeonis_sim.engine.types import Unit, UnitType, UNIT_STATS
    state = m4_state(['rakhis', 'cassian', 'vharok'])
    home = _clear_city_for_legendary(state, 0)
    home.buildings = [BuildingType.WINDSWORN_WARCAMP]
    home.units.append(Unit(uid=state.new_uid(), owner=0, type=UnitType.CAVALRY,
                           hp=UNIT_STATS[UnitType.CAVALRY].hp))
    choices = enumerate_warcamp_cavalry_move(state, 0)
    assert choices


def test_hall_any_timing_flag():
    from aeonis_sim.engine.lords.legendaries import hall_any_timing_available
    state = m4_state(['nyxara', 'cassian', 'seraphel'])
    home = _clear_city_for_legendary(state, 0)
    home.buildings = [BuildingType.HALL_OF_WHISPERS]
    assert hall_any_timing_available(state, 0) is True
