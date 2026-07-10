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
    from aeonis_sim.engine.lords import controls_unique
    from aeonis_sim.engine.whispers import draw_whispers
    state = build_initial_state(
        {
            "players": 3,
            "lord_asymmetry": {"enabled": True, "lords": ["nyxara", "cassian", "vharok"]},
        },
        random.Random(13),
    )
    spire = next(
        t for t in state.tiles.values() if t.unique_tile_id == "obsidian_spire"
    )
    assert spire.controller == 0
    assert controls_unique(state, 0, "obsidian_spire")
    p = state.player(0)
    p.whisper_hand = []
    rng = random.Random(99)
    base = draw_whispers(state, 0, 3, rng)
    bonus = draw_whispers(state, 0, 1, rng)
    assert base == 3
    assert bonus == 1
    assert len(p.whisper_hand) == 4


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
