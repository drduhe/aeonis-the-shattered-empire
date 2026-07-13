"""M4 unique starting tiles."""
from __future__ import annotations
import random
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import Terrain

ROSTER = [
    "cassian", "seraphel", "vharok", "elyndra",
    "rakhis", "nyxara", "auriel", "thalrik",
]

EXPECTED = {
    "cassian": ("caravan_bazaar", Terrain.DESERT),
    "seraphel": ("arcane_nexus", Terrain.FOREST),
    "vharok": ("ironworks_ridge", Terrain.MOUNTAIN),
    "elyndra": ("sacred_grove", Terrain.FOREST),
    "rakhis": ("oasis_wellspring", Terrain.PLAINS),
    "nyxara": ("obsidian_spire", Terrain.MOUNTAIN),
    "auriel": ("hallowed_grove", Terrain.FOREST),
    "thalrik": ("rift_anchor", Terrain.FOREST),
}


def test_each_lord_gets_unique_tile_in_home_cluster():
    state = build_initial_state(
        {"players": 8, "lord_asymmetry": {"enabled": True, "lords": ROSTER}},
        random.Random(19),
    )
    for p in state.players:
        uid, terrain = EXPECTED[p.lord_id]
        matches = [
            t for t in state.tiles.values()
            if t.unique_tile_id == uid and t.controller == p.pid
        ]
        assert len(matches) == 1, p.lord_id
        tile = matches[0]
        assert tile.terrain == terrain
        assert tile.coord != p.home  # never replaces City


def test_arcane_nexus_produces_two_mana():
    state = build_initial_state(
        {
            "players": 3,
            "lord_asymmetry": {"enabled": True, "lords": ["seraphel", "cassian", "vharok"]},
        },
        random.Random(3),
    )
    from aeonis_sim.engine.production import run_production
    before = state.player(0).mana
    run_production(state)
    nexus = next(t for t in state.tiles.values() if t.unique_tile_id == "arcane_nexus")
    assert nexus.controller == 0
    assert state.player(0).mana >= before + 2


def test_sacred_grove_denies_grove_allows_tower():
    from aeonis_sim.engine.build import enumerate_builds
    state = build_initial_state(
        {
            "players": 3,
            "lord_asymmetry": {"enabled": True, "lords": ["elyndra", "cassian", "vharok"]},
        },
        random.Random(5),
    )
    p = state.player(0)
    p.ap, p.gold, p.mana, p.influence, p.pop_pool = 10, 20, 20, 20, 20
    grove = next(t for t in state.tiles.values() if t.unique_tile_id == "sacred_grove")
    builds = enumerate_builds(state, 0)
    assert any(b["building"] == "tower" and b["hex"] == list(grove.coord) for b in builds)
    assert not any(b["building"] == "grove" and b["hex"] == list(grove.coord) for b in builds)


def test_rift_anchor_counts_as_portal():
    from aeonis_sim.engine.lords import tile_is_portal
    state = build_initial_state(
        {
            "players": 3,
            "lord_asymmetry": {"enabled": True, "lords": ["thalrik", "cassian", "vharok"]},
        },
        random.Random(7),
    )
    anchor = next(t for t in state.tiles.values() if t.unique_tile_id == "rift_anchor")
    assert tile_is_portal(state, anchor.coord)


def test_hallowed_grove_grants_renown_on_cleanup():
    from aeonis_sim.engine.cleanup import run_cleanup
    state = build_initial_state(
        {
            "players": 3,
            "lord_asymmetry": {"enabled": True, "lords": ["auriel", "cassian", "vharok"]},
        },
        random.Random(11),
    )
    grove = next(t for t in state.tiles.values() if t.unique_tile_id == "hallowed_grove")
    assert grove.controller == 0
    before = state.player(0).renown
    run_cleanup(state)
    assert state.player(0).renown == before + 1


def test_obsidian_spire_grants_extra_whisper_draw():
    from aeonis_sim.engine.game import Game
    from aeonis_sim.engine.lords import controls_unique
    from tests.conftest import advance_to_action_phase

    g = Game(
        {
            "players": 3,
            "lord_asymmetry": {
                "enabled": True,
                "lords": ["nyxara", "cassian", "vharok"],
            },
        },
        seed=13,
    )
    spire = next(
        t for t in g.state.tiles.values() if t.unique_tile_id == "obsidian_spire"
    )
    assert spire.controller == 0
    assert controls_unique(g.state, 0, "obsidian_spire")
    p = g.state.player(0)

    advance_to_action_phase(g)
    p.whisper_hand = []

    for _ in range(3):
        dp = g.next_decision()
        g.submit({"type": "pass"})

    g.next_decision()  # triggers cleanup + round 2 _round_start

    assert g.state.round == 2
    assert len(p.whisper_hand) == 4  # Nyxara whisper network (3) + Obsidian Spire (1)


def test_ironworks_allows_fortress_build():
    from aeonis_sim.engine.build import enumerate_builds
    state = build_initial_state(
        {
            "players": 3,
            "lord_asymmetry": {"enabled": True, "lords": ["vharok", "cassian", "seraphel"]},
        },
        random.Random(17),
    )
    p = state.player(0)
    p.ap, p.gold, p.mana, p.influence, p.pop_pool = 10, 20, 20, 20, 20
    ridge = next(t for t in state.tiles.values() if t.unique_tile_id == "ironworks_ridge")
    builds = enumerate_builds(state, 0)
    assert any(
        b["building"] == "fortress" and b["hex"] == list(ridge.coord) for b in builds
    )


def test_arcane_nexus_research_mana_discount():
    from aeonis_sim.engine.arcane import (
        apply_research,
        enumerate_research,
        research_resource_cost,
        DISCOVERIES,
    )
    from aeonis_sim.engine.lords import round_unused
    from aeonis_sim.engine.types import BuildingType
    state = build_initial_state(
        {
            "players": 3,
            "lord_asymmetry": {"enabled": True, "lords": ["seraphel", "cassian", "vharok"]},
        },
        random.Random(3),
    )
    p = state.player(0)
    p.ap, p.mana = 1, 1
    spec = DISCOVERIES["battle_runes"]
    assert research_resource_cost(state, 0, spec, free=False) == (1, 0, 0)
    assert any(c["discovery"] == "battle_runes" for c in enumerate_research(state, 0))
    apply_research(state, 0, "battle_runes")
    assert p.mana == 0
    assert "battle_runes" in p.discoveries
    assert not round_unused(state, 0, "nexus_discount")
    assert not any(c["discovery"] == "sigiled_masonry" for c in enumerate_research(state, 0))


def test_nexus_discount_not_marked_when_academy_zeroes_mana():
    from aeonis_sim.engine.arcane import apply_research
    from aeonis_sim.engine.lords import round_unused
    from aeonis_sim.engine.types import BuildingType
    state = build_initial_state(
        {
            "players": 3,
            "lord_asymmetry": {"enabled": True, "lords": ["seraphel", "cassian", "vharok"]},
        },
        random.Random(3),
    )
    p = state.player(0)
    nexus = next(t for t in state.tiles.values() if t.unique_tile_id == "arcane_nexus")
    nexus.buildings.append(BuildingType.ACADEMY)
    p.ap, p.mana = 1, 0
    apply_research(state, 0, "sigiled_masonry")
    assert "sigiled_masonry" in p.discoveries
    assert round_unused(state, 0, "nexus_discount")


def test_ironworks_mine_and_fortress_gold_discount():
    from aeonis_sim.engine.build import apply_build, enumerate_builds
    state = build_initial_state(
        {
            "players": 3,
            "lord_asymmetry": {"enabled": True, "lords": ["vharok", "cassian", "seraphel"]},
        },
        random.Random(17),
    )
    p = state.player(0)
    ridge = next(t for t in state.tiles.values() if t.unique_tile_id == "ironworks_ridge")
    p.ap, p.mana, p.influence, p.pop_pool = 10, 10, 10, 10
    p.gold = 2
    builds = enumerate_builds(state, 0)
    assert any(
        b["building"] == "mine" and b["hex"] == list(ridge.coord) for b in builds
    )
    p.gold = 4
    builds = enumerate_builds(state, 0)
    assert any(
        b["building"] == "fortress" and b["hex"] == list(ridge.coord) for b in builds
    )
    p.gold = 4
    apply_build(state, 0, {"hex": list(ridge.coord), "building": "fortress"})
    assert p.gold == 0


def test_cassian_bazaar_trade_grants_gold_once():
    from aeonis_sim.engine.game import Game
    from aeonis_sim.engine.lords import round_unused
    from tests.conftest import advance_to_action_phase
    g = Game(
        {
            "players": 3,
            "lord_asymmetry": {
                "enabled": True,
                "lords": ["cassian", "seraphel", "vharok"],
            },
        },
        seed=37,
    )
    advance_to_action_phase(g)
    g._initiative_queue = [0, 1, 2]
    g._pending = None
    g.state.player(0).gold = 5
    g.state.player(1).mana = 5
    dp = g.next_decision()
    trade = next(c for c in dp.choices if c["type"] == "trade")
    before = g.state.player(0).gold
    g.submit(trade)
    assert g.state.player(0).gold == before + 1
    assert not round_unused(g.state, 0, "bazaar_trade_gold")
    g._grant_bazaar_trade_gold(g.state)
    assert g.state.player(0).gold == before + 1


def test_oasis_wellspring_has_no_cavalry_recruit_discount():
    """Rakhis ladder Dial 1 (2026-07-12): Oasis keeps production; no -1 Cavalry Gold."""
    from aeonis_sim.engine.recruit import apply_recruit, enumerate_recruits
    state = build_initial_state(
        {
            "players": 3,
            "lord_asymmetry": {"enabled": True, "lords": ["rakhis", "cassian", "vharok"]},
        },
        random.Random(21),
    )
    p = state.player(0)
    city = next(t for t in state.controlled(0) if t.terrain == Terrain.CITY)
    assert any(t.unique_tile_id == "oasis_wellspring" for t in state.tiles.values())
    p.ap, p.gold, p.mana, p.pop_pool = 5, 1, 5, 5
    assert not any(r["units"] == ["cavalry"] for r in enumerate_recruits(state, 0))
    p.gold = 2
    cav = next(r for r in enumerate_recruits(state, 0) if r["units"] == ["cavalry"])
    assert cav["city"] == list(city.coord)
    apply_recruit(state, 0, cav)
    assert p.gold == 0


def test_rift_anchor_free_portal_move_once_per_round():
    from aeonis_sim.engine.move import apply_move, enumerate_moves
    from aeonis_sim.engine.types import Unit, UnitType, UNIT_STATS
    state = build_initial_state(
        {
            "players": 3,
            "lord_asymmetry": {"enabled": True, "lords": ["thalrik", "cassian", "vharok"]},
        },
        random.Random(7),
    )
    anchor = next(t for t in state.tiles.values() if t.unique_tile_id == "rift_anchor")
    portal_dest = next(
        c for c, t in state.tiles.items()
        if t.terrain == Terrain.PORTAL and c != anchor.coord
    )
    unit = Unit(
        uid=state.new_uid(), owner=0, type=UnitType.INFANTRY,
        hp=UNIT_STATS[UnitType.INFANTRY].hp,
    )
    anchor.units.append(unit)
    state.player(0).ap = 5
    moves = enumerate_moves(state, 0)
    free = next(
        m for m in moves
        if tuple(m["dest"]) == portal_dest and m.get("rift_anchor_free")
    )
    assert free["cost"] == 0
    apply_move(state, 0, free)
    moves2 = enumerate_moves(state, 0)
    assert not any(m.get("rift_anchor_free") for m in moves2)
