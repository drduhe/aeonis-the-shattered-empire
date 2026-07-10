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
