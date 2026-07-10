"""Unique starting tiles for launch Lords."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ..hexmap import neighbors
from ..types import Terrain


@dataclass(frozen=True)
class UniqueTileSpec:
    id: str
    lord_id: str
    replaces: Terrain
    counts_as: Terrain
    gold: int = 0
    mana: int = 0
    influence: int = 0
    population: int = 0
    allow_buildings: frozenset = field(default_factory=frozenset)
    deny_buildings: frozenset = field(default_factory=frozenset)
    portal: bool = False


UNIQUE_TILES: dict[str, UniqueTileSpec] = {
    "cassian": UniqueTileSpec(
        "caravan_bazaar", "cassian", Terrain.DESERT, Terrain.DESERT,
        influence=2, allow_buildings=frozenset({"embassy"}),
        deny_buildings=frozenset({"tower"}),
    ),
    "seraphel": UniqueTileSpec(
        "arcane_nexus", "seraphel", Terrain.FOREST, Terrain.FOREST,
        mana=2, allow_buildings=frozenset({"tower"}),
        deny_buildings=frozenset({"grove"}),
    ),
    "vharok": UniqueTileSpec(
        "ironworks_ridge", "vharok", Terrain.MOUNTAIN, Terrain.MOUNTAIN,
        gold=2, allow_buildings=frozenset({"fortress", "mine"}),
    ),
    "elyndra": UniqueTileSpec(
        "sacred_grove", "elyndra", Terrain.FOREST, Terrain.FOREST,
        mana=1, population=1, allow_buildings=frozenset({"tower"}),
        deny_buildings=frozenset({"grove"}),
    ),
    "rakhis": UniqueTileSpec(
        "oasis_wellspring", "rakhis", Terrain.PLAINS, Terrain.PLAINS,
        gold=1, population=1, allow_buildings=frozenset({"farm"}),
        deny_buildings=frozenset({"tower"}),
    ),
    "nyxara": UniqueTileSpec(
        "obsidian_spire", "nyxara", Terrain.MOUNTAIN, Terrain.MOUNTAIN,
        gold=1, mana=1, allow_buildings=frozenset({"mine"}),
        deny_buildings=frozenset({"tower"}),
    ),
    "auriel": UniqueTileSpec(
        "hallowed_grove", "auriel", Terrain.FOREST, Terrain.FOREST,
        mana=1, influence=1, allow_buildings=frozenset({"grove"}),
        deny_buildings=frozenset({"tower"}),
    ),
    "thalrik": UniqueTileSpec(
        "rift_anchor", "thalrik", Terrain.FOREST, Terrain.FOREST,
        mana=1, allow_buildings=frozenset({"tower"}),
        deny_buildings=frozenset({"grove"}), portal=True,
    ),
}


def unique_spec_for_lord(lord_id: str) -> Optional[UniqueTileSpec]:
    return UNIQUE_TILES.get(lord_id)


def place_unique_tiles(state) -> None:
    """AL-52: prefer matching terrain in home cluster; else convert one adjacent hex."""
    from .specs import LORD_SPECS

    for p in state.players:
        if p.lord_id not in LORD_SPECS:
            continue
        spec = UNIQUE_TILES[p.lord_id]
        home = p.home
        candidates = []
        for nb in neighbors(home):
            t = state.tiles.get(nb)
            if t is None or t.imperial_seat or t.terrain == Terrain.CITY:
                continue
            if t.controller == p.pid and t.terrain == spec.replaces:
                candidates.append(t)
        if not candidates:
            for nb in neighbors(home):
                t = state.tiles.get(nb)
                if t is None or t.imperial_seat or t.terrain == Terrain.CITY:
                    continue
                if t.controller == p.pid:
                    candidates.append(t)
                    break
        if not candidates:
            for nb in neighbors(home):
                t = state.tiles.get(nb)
                if t is not None and not t.imperial_seat and t.terrain != Terrain.CITY:
                    t.controller = p.pid
                    candidates.append(t)
                    break
        tile = candidates[0]
        tile.terrain = spec.counts_as
        tile.unique_tile_id = spec.id
        tile.controller = p.pid


def tile_is_portal(state, coord) -> bool:
    t = state.tiles[coord]
    return t.terrain == Terrain.PORTAL or t.unique_tile_id == "rift_anchor"
