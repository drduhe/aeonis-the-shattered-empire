from __future__ import annotations

from .types import BuildingType, Terrain

# Tiles.md: base production, upgraded by the matching production building.
_PLAIN = {Terrain.MOUNTAIN: ("gold", 1), Terrain.FOREST: ("mana", 1),
          Terrain.DESERT: ("influence", 1)}
_UPGRADED = {BuildingType.MINE: ("gold", 3), BuildingType.GROVE: ("mana", 3),
             BuildingType.EMBASSY: ("influence", 3)}


def run_production(state) -> None:
    for p in state.players:
        growth = 1  # Population.md base growth
        for t in state.controlled(p.pid):
            # Resource production (AL-13: Cities produce no resources in M1)
            produced = None
            for b in t.buildings:
                if b in _UPGRADED:
                    produced = _UPGRADED[b]
            if produced is None:
                produced = _PLAIN.get(t.terrain)
            if produced:
                setattr(p, produced[0], getattr(p, produced[0]) + produced[1])
            # Population growth contributions
            if t.terrain == Terrain.PLAINS:
                growth += 2 if t.has(BuildingType.FARM) else 1
            elif t.terrain == Terrain.CITY:
                growth += 2
            # Castle upkeep (AL-8: suspend when unpaid)
            if t.has(BuildingType.CASTLE):
                if p.gold >= 2:
                    p.gold -= 2
                    t.castle_suspended = False
                else:
                    t.castle_suspended = True
        room = state.pop_cap(p.pid) - state.pop_used(p.pid) - p.pop_pool
        p.pop_pool += max(0, min(growth, room))
