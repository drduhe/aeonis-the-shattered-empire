"""M4 faction discoveries: catalog + Research merge + effect hooks."""
from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from aeonis_sim.engine.arcane import (
    apply_research,
    build_gold_cost,
    enumerate_research,
    mark_build_discount_used,
)
from aeonis_sim.engine import combat
from aeonis_sim.engine.combat import finish_battle, start_battle
from aeonis_sim.engine.cleanup import run_cleanup
from aeonis_sim.engine.lords import FACTION_DISCOVERIES, FACTION_DISCOVERY_IDS, tile_is_portal
from aeonis_sim.engine.lords.discoveries import (
    apply_guild_contracts_trade_influence,
    apply_planar_echo,
    apply_sandsworn_pact,
    apply_stolen_secrets,
    apply_void_anchor,
    bump_renown,
    enumerate_void_anchor,
    luminous_bulwark_bonus,
    mana_nexus_bonus,
    mirage_riders_attack_bonus,
    reinforced_fortifications_bonus,
    thornwatch_bonus,
)
from aeonis_sim.engine.move import apply_move
from aeonis_sim.engine.production import run_production
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BUILDING_SPECS, BuildingType, Terrain, Unit, UnitType, UNIT_STATS
from aeonis_sim.engine.whispers import apply_when_whisper


def _m4(lords: list[str], *, seed: int = 2):
    """Pad to a legal 3-player map while keeping the requested lord order."""
    pad = ["vharok", "elyndra", "rakhis"]
    roster = list(lords)
    for lord in pad:
        if len(roster) >= 3:
            break
        if lord not in roster:
            roster.append(lord)
    while len(roster) < 3:
        roster.append("nyxara")
    return build_initial_state(
        {"players": len(roster), "lord_asymmetry": {"enabled": True, "lords": roster}},
        random.Random(seed),
    )


def _strip(state):
    for tile in state.tiles.values():
        tile.units = []
        tile.controller = None
        tile.buildings = []
        tile.unique_tile_id = ""
        tile.void_anchor_until_round = 0
    return state


def _put(state, coord, owner, unit_type):
    unit = Unit(
        uid=state.new_uid(), owner=owner, type=unit_type,
        hp=UNIT_STATS[unit_type].hp,
    )
    state.tiles[coord].units.append(unit)
    return unit


def test_sixteen_faction_discoveries_registered():
    assert len(FACTION_DISCOVERY_IDS) == 16
    assert len(FACTION_DISCOVERIES) == 16
    assert set(FACTION_DISCOVERY_IDS) == set(FACTION_DISCOVERIES)


def test_cassian_can_research_guild_contracts():
    state = build_initial_state(
        {"players": 3, "lord_asymmetry": {"enabled": True, "lords": ["cassian", "vharok", "elyndra"]}},
        random.Random(2),
    )
    p = state.player(0)
    p.ap, p.gold, p.influence = 5, 10, 10
    choices = enumerate_research(state, 0)
    assert any(c["discovery"] == "guild_contracts" for c in choices)
    apply_research(state, 0, "guild_contracts")
    assert "guild_contracts" in p.discoveries
    assert p.remnants >= 1


def test_non_cassian_does_not_see_guild_contracts():
    state = _m4(["seraphel", "cassian"], seed=3)
    p = state.player(0)
    p.ap, p.gold, p.mana, p.influence = 5, 10, 10, 10
    choices = enumerate_research(state, 0)
    assert not any(c["discovery"] == "guild_contracts" for c in choices)
    assert any(c["discovery"] == "mana_nexus" for c in choices)


def test_wrong_lord_cannot_research_guild_contracts():
    state = _m4(["vharok"], seed=4)
    p = state.player(0)
    p.ap, p.gold, p.mana, p.influence = 5, 10, 10, 10
    with pytest.raises(ValueError, match="wrong lord"):
        apply_research(state, 0, "guild_contracts")
    assert "guild_contracts" not in p.discoveries


def test_owned_faction_discovery_excluded_from_enumerate():
    state = _m4(["cassian"], seed=5)
    p = state.player(0)
    p.ap, p.gold, p.influence = 5, 10, 10
    p.discoveries.append("guild_contracts")
    choices = enumerate_research(state, 0)
    assert not any(c["discovery"] == "guild_contracts" for c in choices)
    assert any(c["discovery"] == "diplomatic_tariffs" for c in choices)


def test_guild_contracts_charges_costs_ap_gold_influence():
    state = _m4(["cassian"], seed=6)
    p = state.player(0)
    p.ap, p.gold, p.mana, p.influence = 5, 10, 7, 10
    before_remnants = p.remnants
    apply_research(state, 0, "guild_contracts")
    assert p.ap == 4
    assert p.gold == 8
    assert p.influence == 8
    assert p.mana == 7  # faction research does not spend mana for guild_contracts
    assert p.remnants == before_remnants + 1
    assert p.discoveries.count("guild_contracts") == 1


def test_m4_off_excludes_faction_discoveries():
    state = build_initial_state({"players": 3}, random.Random(7))
    p = state.player(0)
    p.ap, p.gold, p.mana, p.influence = 5, 10, 10, 10
    choices = enumerate_research(state, 0)
    assert not any(c["discovery"] in FACTION_DISCOVERIES for c in choices)


# --- Effect hooks (one deterministic test per discovery) ---


def test_guild_contracts_market_discount_and_trade_influence():
    state = _m4(["cassian"], seed=10)
    p = state.player(0)
    p.discoveries.append("guild_contracts")
    base = BUILDING_SPECS[BuildingType.MARKET].gold
    discounted = max(0, base - 1)
    assert build_gold_cost(state, 0, BuildingType.MARKET, base) == discounted
    # Always-on while owned — not once/round.
    mark_build_discount_used(state, 0, BuildingType.MARKET, base)
    assert build_gold_cost(state, 0, BuildingType.MARKET, base) == discounted
    assert build_gold_cost(state, 0, BuildingType.FARM, BUILDING_SPECS[BuildingType.FARM].gold) == (
        BUILDING_SPECS[BuildingType.FARM].gold
    )

    before = p.influence
    assert apply_guild_contracts_trade_influence(state, 0, zero_ap_market=True)
    assert p.influence == before + 1
    assert not apply_guild_contracts_trade_influence(state, 0, zero_ap_market=True)


def test_diplomatic_tariffs_on_other_player_trade():
    from aeonis_sim.engine.game import Game
    from tests.conftest import advance_to_action_phase

    g = Game(
        {
            "players": 3,
            "lord_asymmetry": {
                "enabled": True,
                "lords": ["cassian", "vharok", "elyndra"],
            },
        },
        seed=11,
    )
    advance_to_action_phase(g)
    g._initiative_queue = [1, 0, 2]
    g._pending = None
    cassian = g.state.player(0)
    cassian.discoveries.append("diplomatic_tariffs")
    home = next(t for t in g.state.controlled(0))
    home.buildings.append(BuildingType.EMBASSY)
    # Give trader a Market so trade is 0-AP and always enumerable.
    trader_home = next(t for t in g.state.controlled(1))
    trader_home.buildings.append(BuildingType.MARKET)
    g.state.player(1).gold = 5
    g.state.player(0).mana = 5
    from aeonis_sim.engine.lords import round_unused
    assert round_unused(g.state, 0, "diplomatic_tariffs")
    before = cassian.gold
    dp = g.next_decision()
    assert dp.pid == 1
    trade = next(c for c in dp.choices if c["type"] == "trade")
    g.submit(trade)
    assert not round_unused(g.state, 0, "diplomatic_tariffs")
    assert cassian.gold >= before + 1


def test_mana_nexus_bonus_on_mana_producing_hexes():
    state = _strip(_m4(["seraphel"], seed=12))
    p = state.player(0)
    p.discoveries.append("mana_nexus")
    forest = (0, 0)
    plains_grove = (1, 0)
    mountain = (2, 0)
    state.tiles[forest].terrain = Terrain.FOREST
    state.tiles[forest].controller = 0
    state.tiles[plains_grove].terrain = Terrain.PLAINS
    state.tiles[plains_grove].controller = 0
    state.tiles[plains_grove].buildings = [BuildingType.GROVE]
    state.tiles[mountain].terrain = Terrain.MOUNTAIN
    state.tiles[mountain].controller = 0
    assert mana_nexus_bonus(state, 0) == 2
    before = p.mana
    run_production(state)
    assert p.mana >= before + 2


def test_spellweave_doctrine_after_lobby():
    from aeonis_sim.engine.game import Game
    from aeonis_sim.engine.observations import DecisionPoint
    from tests.conftest import advance_to_action_phase

    g = Game(
        {
            "players": 3,
            "lord_asymmetry": {
                "enabled": True,
                "lords": ["seraphel", "cassian", "vharok"],
            },
        },
        seed=13,
    )
    advance_to_action_phase(g)
    p = g.state.player(0)
    p.discoveries.append("spellweave_doctrine")
    p.influence = 5
    before = p.mana
    vote = {
        "type": "council_vote",
        "motion": "magister_of_mana",
        "support": True,
        "lobby": 2,
    }
    g._pending = DecisionPoint(
        kind="council_vote",
        phase="council",
        pid=0,
        choices=[vote],
    )
    g._council_motions = [{"motion": "magister_of_mana", "proposer": 0}]
    g._council_vote_motion_idx = 0
    g._council_vote_queue = [0, 1]  # leave a voter so tally does not run yet
    g._council_ballots = []
    g._council_extra_votes = {"for": 0, "against": 0}
    g.submit(vote)
    assert p.mana == before + 1
    assert p.influence == 3
    # Once/round: second lobby same round does not grant again.
    after = p.mana
    vote2 = {
        "type": "council_vote",
        "motion": "magister_of_mana",
        "support": True,
        "lobby": 2,
    }
    p.influence = 5
    g._pending = DecisionPoint(
        kind="council_vote",
        phase="council",
        pid=0,
        choices=[vote2],
    )
    g._council_vote_queue = [0, 1]
    g.submit(vote2)
    assert p.mana == after
    assert p.influence == 3


def test_reinforced_fortifications_tower_defense():
    state = _strip(_m4(["vharok"], seed=14))
    p = state.player(0)
    p.discoveries.append("reinforced_fortifications")
    hex_ = (1, 0)
    state.tiles[hex_].terrain = Terrain.PLAINS
    state.tiles[hex_].controller = 0
    state.tiles[hex_].buildings = [BuildingType.TOWER]
    assert reinforced_fortifications_bonus(state, 0, state.tiles[hex_]) == 1
    battle = SimpleNamespace(defender=0, target=hex_)
    assert combat._defense_bonus(state, battle, "def") >= 2  # tower + discovery
    # Attacker-side defense rolls must not receive discovery defense bonuses.
    assert combat._defense_bonus(state, battle, "att") == 0


def test_discovery_defense_bonuses_defender_side_only():
    """reinforced_fortifications / luminous_bulwark apply only when side == def."""
    state = _strip(_m4(["vharok", "auriel"], seed=27))
    state.player(0).discoveries.append("reinforced_fortifications")
    state.player(0).discoveries.append("luminous_bulwark")
    hex_ = (1, 0)
    state.tiles[hex_].terrain = Terrain.PLAINS
    state.tiles[hex_].controller = 0
    state.tiles[hex_].buildings = [BuildingType.TOWER]
    battle = SimpleNamespace(defender=0, attacker=1, target=hex_)
    def_bonus = combat._defense_bonus(state, battle, "def")
    # Tower (+1) + reinforced (+1) + luminous (+1) + Vharok forged (+1) = 4
    assert def_bonus == 4
    assert combat._defense_bonus(state, battle, "att") == 0


def test_siege_logistics_after_city_attack():
    state = _strip(_m4(["vharok", "cassian"], seed=15))
    att = state.player(0)
    att.discoveries.append("siege_logistics")
    att.ap = 5
    city = (1, 0)
    origin = (2, 0)
    state.tiles[city].terrain = Terrain.CITY
    state.tiles[city].controller = 1
    state.tiles[origin].terrain = Terrain.PLAINS
    state.tiles[origin].controller = 0
    _put(state, city, 1, UnitType.INFANTRY)
    _put(state, origin, 0, UnitType.INFANTRY)
    before = att.ap
    start_battle(state, 0, {"type": "attack", "target": list(city), "cost": 2})
    # spent 2 AP for attack, gained 1 from siege logistics
    assert att.ap == before - 2 + 1


def test_thornwatch_archer_defense_on_grove():
    state = _strip(_m4(["elyndra"], seed=16))
    state.player(0).discoveries.append("thornwatch")
    hex_ = (1, 0)
    state.tiles[hex_].terrain = Terrain.PLAINS
    state.tiles[hex_].controller = 0
    state.tiles[hex_].buildings = [BuildingType.GROVE]
    archer = _put(state, hex_, 0, UnitType.ARCHER)
    battle = SimpleNamespace(defender=0, target=hex_, def_line=[archer])
    assert thornwatch_bonus(state, battle, archer) == 1


def test_seedbound_resilience_on_controlled_hex_after_battle():
    state = _strip(_m4(["elyndra", "vharok"], seed=17))
    p = state.player(0)
    p.discoveries.append("seedbound_resilience")
    p.pop_pool = 0
    hex_ = (1, 0)
    origin = (2, 0)
    state.tiles[hex_].terrain = Terrain.PLAINS
    state.tiles[hex_].controller = 0
    state.tiles[origin].terrain = Terrain.PLAINS
    state.tiles[origin].controller = 1
    _put(state, hex_, 0, UnitType.INFANTRY)
    _put(state, origin, 1, UnitType.INFANTRY)
    state.player(1).ap = 5
    battle = start_battle(state, 1, {"type": "attack", "target": list(hex_), "cost": 2})
    battle.winner = "defender"
    before = p.pop_pool
    finish_battle(state, battle)
    assert p.pop_pool == before + 1


def test_mirage_riders_cavalry_from_desert():
    state = _strip(_m4(["rakhis"], seed=18))
    state.player(0).discoveries.append("mirage_riders")
    desert = (1, 0)
    state.tiles[desert].terrain = Terrain.DESERT
    state.tiles[desert].controller = 0
    cav = _put(state, desert, 0, UnitType.CAVALRY)
    assert mirage_riders_attack_bonus(state, 0, cav, desert) == 1
    plains = (2, 0)
    state.tiles[plains].terrain = Terrain.PLAINS
    assert mirage_riders_attack_bonus(state, 0, cav, plains) == 0


def test_sandsworn_pact_on_neutral_claim():
    state = _strip(_m4(["rakhis"], seed=19))
    p = state.player(0)
    p.discoveries.append("sandsworn_pact")
    p.ap = 5
    src = (0, 0)
    dst = (1, 0)
    state.tiles[src].terrain = Terrain.PLAINS
    state.tiles[src].controller = 0
    state.tiles[dst].terrain = Terrain.PLAINS
    state.tiles[dst].controller = None
    unit = _put(state, src, 0, UnitType.INFANTRY)
    before = p.gold
    apply_move(state, 0, {
        "type": "move", "from": list(src), "dest": list(dst),
        "uids": [unit.uid], "cost": 1, "portal": False,
    })
    assert state.tiles[dst].controller == 0
    assert p.gold == before + 1
    assert not apply_sandsworn_pact(state, 0, claimed_neutral=True)


def test_stolen_secrets_on_when_whisper():
    state = _m4(["nyxara"], seed=20)
    p = state.player(0)
    p.discoveries.append("stolen_secrets")
    p.whisper_hand = ["war_profiteer"]
    state.whisper_deck = ["hidden_cache", "contraband"]
    before = len(p.whisper_hand)
    apply_when_whisper(
        state, 0, {"type": "whisper_play", "card": "war_profiteer"},
        rng=random.Random(1),
    )
    # war_profiteer discarded, stolen_secrets draws 1
    assert "war_profiteer" not in p.whisper_hand
    assert len(p.whisper_hand) == before  # discarded 1, drew 1
    assert apply_stolen_secrets(state, 0, random.Random(2)) == 0  # once/round


def test_shadow_network_free_action():
    from aeonis_sim.engine.game import Game
    from tests.conftest import advance_to_action_phase

    g = Game(
        {
            "players": 3,
            "lord_asymmetry": {
                "enabled": True,
                "lords": ["nyxara", "cassian", "vharok"],
            },
        },
        seed=21,
    )
    advance_to_action_phase(g)
    g._initiative_queue = [0, 1, 2]
    g._pending = None
    p = g.state.player(0)
    p.discoveries.append("shadow_network")
    p.whisper_hand = ["hidden_cache"]
    before = p.gold
    dp = g.next_decision()
    choice = next(
        c for c in dp.choices
        if c["type"] == "shadow_network" and c.get("reward") == "gold"
    )
    g.submit(choice)
    assert p.gold == before + 2
    assert "hidden_cache" not in p.whisper_hand
    # Once/round: not enumerable again; apply fails.
    from aeonis_sim.engine.lords.discoveries import (
        apply_shadow_network,
        enumerate_shadow_network,
    )
    p.whisper_hand = ["contraband"]
    assert enumerate_shadow_network(g.state, 0) == []
    with pytest.raises(ValueError, match="already used"):
        apply_shadow_network(
            g.state, 0,
            {"type": "shadow_network", "card": "contraband", "reward": "gold"},
        )


def test_luminous_bulwark_on_built_hex():
    state = _strip(_m4(["auriel"], seed=22))
    state.player(0).discoveries.append("luminous_bulwark")
    hex_ = (1, 0)
    state.tiles[hex_].terrain = Terrain.PLAINS
    state.tiles[hex_].controller = 0
    state.tiles[hex_].buildings = [BuildingType.FARM]
    assert luminous_bulwark_bonus(state, 0, state.tiles[hex_]) == 1
    state.tiles[hex_].buildings = []
    assert luminous_bulwark_bonus(state, 0, state.tiles[hex_]) == 0


def test_sacred_rite_milestones_at_5_and_10():
    state = _m4(["auriel"], seed=23)
    p = state.player(0)
    p.discoveries.append("sacred_rite")
    p.renown = 4
    state.whisper_deck = ["hidden_cache"] * 10
    before_vp = p.vp
    before_hand = len(p.whisper_hand)
    bump_renown(state, 0, 1, random.Random(3))
    assert p.renown == 5
    assert p.sacred_rite_5 is True
    assert p.vp == before_vp + 1
    assert p.vp_sources.get("sacred_rite") == 1
    assert len(p.whisper_hand) == before_hand + 2

    p.renown = 9
    before_vp = p.vp
    bump_renown(state, 0, 1, random.Random(4))
    assert p.sacred_rite_10 is True
    assert p.vp == before_vp + 1
    assert p.vp_sources.get("sacred_rite") == 2


def test_sacred_rite_fires_on_lord_capture_renown():
    """Non-exaltation path: combat lord-capture renown crosses 5."""
    from aeonis_sim.engine.combat import resolve_round

    class ScriptRng:
        def __init__(self, rolls):
            self.rolls = list(rolls)

        def randint(self, a, b):
            return self.rolls.pop(0) if self.rolls else b

        def random(self):
            return 0.5

        def shuffle(self, xs):
            pass

    state = _strip(_m4(["auriel", "vharok"], seed=26))
    p = state.player(0)
    p.discoveries.append("sacred_rite")
    p.renown = 4
    p.whisper_hand = []
    state.whisper_deck = ["hidden_cache"] * 10
    state.whisper_discard = []
    origin, target = (0, 0), (1, 0)
    state.tiles[origin].terrain = Terrain.PLAINS
    state.tiles[origin].controller = 0
    state.tiles[target].terrain = Terrain.PLAINS
    state.tiles[target].controller = 1
    for _ in range(3):
        _put(state, origin, 0, UnitType.CAVALRY)
    _put(state, target, 1, UnitType.LORD)
    p.ap = 5
    before_vp = p.vp
    battle = start_battle(
        state, 0, {"type": "attack", "target": list(target), "cost": 2},
        rng=ScriptRng([8, 1, 8, 1, 8, 1]),
    )
    resolve_round(state, battle, ScriptRng([8, 1, 8, 1, 8, 1]))
    assert p.renown == 6
    assert p.sacred_rite_5 is True
    assert p.vp == before_vp + 1 + 1  # lord_capture + sacred_rite
    assert p.vp_sources.get("sacred_rite") == 1
    assert len(p.whisper_hand) == 2


def test_planar_echo_after_portal_move():
    state = _m4(["thalrik"], seed=24)
    p = state.player(0)
    p.discoveries.append("planar_echo")
    p.ap = 3
    assert apply_planar_echo(state, 0, used_portal=True)
    assert p.ap == 4
    assert not apply_planar_echo(state, 0, used_portal=True)


def test_void_anchor_owner_only_portal_clears_in_cleanup():
    state = _strip(_m4(["thalrik", "cassian"], seed=25))
    p = state.player(0)
    p.discoveries.append("void_anchor")
    p.mana = 3
    hex_ = (1, 0)
    state.tiles[hex_].terrain = Terrain.PLAINS
    state.tiles[hex_].controller = 0
    state.round = 2
    choices = enumerate_void_anchor(state, 0)
    assert any(tuple(c["hex"]) == hex_ for c in choices)
    apply_void_anchor(state, 0, hex_)
    assert state.tiles[hex_].void_anchor_until_round == 2
    assert tile_is_portal(state, hex_, pid=0) is True
    assert tile_is_portal(state, hex_, pid=1) is False
    assert tile_is_portal(state, hex_) is False
    run_cleanup(state, random.Random(5))
    assert state.tiles[hex_].void_anchor_until_round == 0
    assert tile_is_portal(state, hex_, pid=0) is False
