from __future__ import annotations

from .hexmap import neighbors
from .objectives import record_fortress_built, record_influence_hex_gain
from .arcane import (
    build_gold_cost,
    mark_build_discount_used,
    mark_waystones_used,
    waystones_move_discount,
)
from .types import BUILDING_SPECS, BuildingType, DEFAULT_BUILD_AP, Terrain
from .lords import controls_unique, mark_round_used, round_unused, unique_spec_by_id

TIER1_PRODUCTION = frozenset({
    BuildingType.FARM,
    BuildingType.MINE,
    BuildingType.GROVE,
    BuildingType.EMBASSY,
})

BUILD_AP = DEFAULT_BUILD_AP  # legacy alias for tests/docs


def build_ap_cost(state, btype: BuildingType) -> int:
    if btype in TIER1_PRODUCTION:
        return state.tier1_production_build_ap
    return DEFAULT_BUILD_AP


def _slots(tile) -> int:
    return 2 if tile.terrain == Terrain.CITY else 1


def _can_afford(p, spec, state, pid, btype, tile) -> bool:
    gold = build_gold_cost(state, pid, btype, spec.gold, tile=tile)
    return (p.gold >= gold and p.mana >= spec.mana
            and p.influence >= spec.influence and p.pop_pool >= spec.pop)


def _terrain_allows(spec, tile, us, btype) -> bool:
    if us and btype.value in us.allow_buildings:
        return True
    if spec.terrain is not None and tile.terrain != spec.terrain:
        return False
    if spec.terrain is None and tile.terrain == Terrain.LAKE:
        return False
    return True


def _unique_allows(btype, us) -> bool:
    if us is None:
        return True
    if btype.value in us.deny_buildings:
        return False
    return True


def enumerate_builds(state, pid) -> list:
    p = state.player(pid)
    out = []
    for btype, spec in BUILDING_SPECS.items():
        if p.ap < build_ap_cost(state, btype):
            continue
        if not _can_afford(p, spec, state, pid, btype, None):
            continue
        if btype == BuildingType.BRIDGE:
            for coord, tile in state.tiles.items():
                if tile.terrain != Terrain.LAKE or tile.has(BuildingType.BRIDGE):
                    continue
                if any(state.tiles[n].controller == pid
                       for n in neighbors(coord) if n in state.tiles
                       and state.tiles[n].terrain != Terrain.LAKE):
                    out.append({"type": "build", "hex": list(coord),
                                "building": btype.value})
            continue
        for tile in state.controlled(pid):
            if len(tile.buildings) >= _slots(tile):
                continue
            if btype in tile.buildings:
                continue
            us = unique_spec_by_id(tile.unique_tile_id)
            if not _unique_allows(btype, us):
                continue
            if not _terrain_allows(spec, tile, us, btype):
                continue
            if not _can_afford(p, spec, state, pid, btype, tile):
                continue
            out.append({"type": "build", "hex": list(tile.coord),
                        "building": btype.value})
    return out


def apply_build(state, pid, choice) -> None:
    p = state.player(pid)
    tile = state.tiles[tuple(choice["hex"])]
    btype = BuildingType(choice["building"])
    spec = BUILDING_SPECS[btype]
    p.ap -= build_ap_cost(state, btype)
    gold = build_gold_cost(state, pid, btype, spec.gold, tile=tile)
    p.gold -= gold
    p.mana -= spec.mana
    p.influence -= spec.influence
    p.pop_pool -= spec.pop
    mark_build_discount_used(state, pid, btype, spec.gold)
    if (
        btype == BuildingType.FORTRESS
        and tile.unique_tile_id == "ironworks_ridge"
        and controls_unique(state, pid, "ironworks_ridge")
        and round_unused(state, pid, "ironworks_fortress")
    ):
        mark_round_used(state, pid, "ironworks_fortress")
    tile.buildings.append(btype)
    if btype == BuildingType.FORTRESS:
        record_fortress_built(state, pid, tile.coord)
    if btype == BuildingType.BRIDGE and tile.controller is None:
        tile.controller = pid  # AL-6
