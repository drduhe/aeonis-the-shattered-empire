from __future__ import annotations

from .hexmap import neighbors
from .objectives import record_fortress_built, record_influence_hex_gain
from .arcane import (
    build_gold_cost,
    mark_build_discount_used,
    mark_waystones_used,
    waystones_move_discount,
)
from .types import BUILDING_SPECS, BuildingType, Terrain

BUILD_AP = 3


def _slots(tile) -> int:
    return 2 if tile.terrain == Terrain.CITY else 1


def _can_afford(p, spec, state, pid, btype) -> bool:
    gold = build_gold_cost(state, pid, btype, spec.gold)
    return (p.gold >= gold and p.mana >= spec.mana
            and p.influence >= spec.influence and p.pop_pool >= spec.pop)


def enumerate_builds(state, pid) -> list:
    p = state.player(pid)
    if p.ap < BUILD_AP:
        return []
    out = []
    for btype, spec in BUILDING_SPECS.items():
        if not _can_afford(p, spec, state, pid, btype):
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
            if spec.terrain is not None and tile.terrain != spec.terrain:
                continue
            if spec.terrain is None and tile.terrain == Terrain.LAKE:
                continue
            out.append({"type": "build", "hex": list(tile.coord),
                        "building": btype.value})
    return out


def apply_build(state, pid, choice) -> None:
    p = state.player(pid)
    tile = state.tiles[tuple(choice["hex"])]
    btype = BuildingType(choice["building"])
    spec = BUILDING_SPECS[btype]
    p.ap -= BUILD_AP
    gold = build_gold_cost(state, pid, btype, spec.gold)
    p.gold -= gold
    p.mana -= spec.mana
    p.influence -= spec.influence
    p.pop_pool -= spec.pop
    mark_build_discount_used(state, pid, btype, spec.gold)
    tile.buildings.append(btype)
    if btype == BuildingType.FORTRESS:
        record_fortress_built(state, pid, tile.coord)
    if btype == BuildingType.BRIDGE and tile.controller is None:
        tile.controller = pid  # AL-6
