from __future__ import annotations

from .types import BuildingType, Terrain

# Tiles.md: base production, upgraded by the matching production building.
_PLAIN = {Terrain.MOUNTAIN: ("gold", 1), Terrain.FOREST: ("mana", 1),
          Terrain.DESERT: ("influence", 1)}
_UPGRADED = {BuildingType.MINE: ("gold", 3), BuildingType.GROVE: ("mana", 3),
             BuildingType.EMBASSY: ("influence", 3)}


def tile_printed_production(tile) -> dict[str, int]:
    """One-time printed production (Plan 1 Pillage). Cities: 2 Gold."""
    if tile.terrain == Terrain.CITY:
        return {"gold": 2}
    out: dict[str, int] = {}
    for b in tile.buildings:
        if b in _UPGRADED:
            res, amt = _UPGRADED[b]
            out[res] = out.get(res, 0) + amt
    if not out:
        plain = _PLAIN.get(tile.terrain)
        if plain:
            res, amt = plain
            out[res] = amt
    return out


def apply_tile_production(player, tile) -> None:
    for res, amt in tile_printed_production(tile).items():
        setattr(player, res, getattr(player, res) + amt)


def run_production(state) -> None:
    # Round_Structure.md §6: production, then growth, then upkeep.
    for p in state.players:
        # 1. Resource production (AL-13: Cities produce no resources in M1)
        for t in state.controlled(p.pid):
            produced = None
            for b in t.buildings:
                if b in _UPGRADED:
                    produced = _UPGRADED[b]
            if produced is None:
                produced = _PLAIN.get(t.terrain)
            if produced:
                setattr(p, produced[0], getattr(p, produced[0]) + produced[1])
        # 2. Population growth
        growth = 1  # Population.md base growth
        for t in state.controlled(p.pid):
            if t.terrain == Terrain.PLAINS:
                growth += 2 if t.has(BuildingType.FARM) else 1
            elif t.terrain == Terrain.CITY:
                growth += 2
        room = state.pop_cap(p.pid) - state.pop_used(p.pid) - p.pop_pool
        p.pop_pool += max(0, min(growth, room))
        # 3. Castle upkeep (AL-8: suspend when unpaid)
        for t in state.controlled(p.pid):
            if t.has(BuildingType.CASTLE):
                if p.gold >= 2:
                    p.gold -= 2
                    t.castle_suspended = False
                else:
                    t.castle_suspended = True
