"""Move action (Movement.md, Tiles.md ZOC).

Branching bound: groups enumerated are the WHOLE STACK and each SINGLE UNIT,
not every subset. This is an agent-capability bound, not a rules ruling.
"""
from __future__ import annotations

import heapq

from .hexmap import neighbors
from .types import BuildingType, Terrain, TERRAIN_COST, UNIT_STATS, UnitType


def _enemy_zoc(state, pid) -> set:
    """Hexes adjacent to at least one enemy military unit."""
    zoc = set()
    for t in state.tiles.values():
        if any(u.owner != pid for u in t.units):
            for n in neighbors(t.coord):
                if n in state.tiles:
                    zoc.add(n)
    return zoc


def _passable(state, pid, coord) -> bool:
    t = state.tiles.get(coord)
    if t is None:
        return False
    if t.terrain == Terrain.LAKE and not t.has(BuildingType.BRIDGE):
        return False
    if any(u.owner != pid for u in t.units):
        return False  # attacks are declared; never move into enemy units
    return True


def _portal_exits(state, pid, coord):
    """Portal-to-portal edges at 0 AP (AL-19: no ZOC surcharge on portal hops)."""
    t = state.tiles.get(coord)
    if t is None or t.terrain != Terrain.PORTAL:
        return []
    out = []
    for c2, t2 in state.tiles.items():
        if c2 == coord or t2.terrain != Terrain.PORTAL:
            continue
        if t2.controller in (None, pid):
            out.append(c2)
    return out


def _paths_from(state, pid, start, max_range, max_cost, has_cavalry,
                *, waive_terrain: bool = False):
    """Dijkstra over (hex, flank_spent). Returns dest -> (cost, hexes_entered, used_portal)."""
    best = {}
    # (cost, hexes_entered, coord, flank_spent, used_portal)
    heap = [(0, 0, start, not has_cavalry, False)]
    seen = {}
    while heap:
        cost, steps, coord, flanked, portaled = heapq.heappop(heap)
        key = (coord, flanked)
        if key in seen and seen[key] <= (cost, steps):
            continue
        seen[key] = (cost, steps)
        if coord != start:
            prev = best.get(coord)
            if prev is None or (cost, steps) < (prev[0], prev[1]):
                best[coord] = (cost, steps, portaled)
        if steps >= max_range:
            continue
        zoc = _enemy_zoc(state, pid)
        for nxt in neighbors(coord):
            if not _passable(state, pid, nxt):
                continue
            step = 0 if waive_terrain else TERRAIN_COST[state.tiles[nxt].terrain]
            f2 = flanked
            if nxt in zoc:
                if not flanked:
                    f2 = True  # cavalry flanking: first ZOC hex free
                else:
                    step += 1
            if cost + step <= max_cost:
                heapq.heappush(heap, (cost + step, steps + 1, nxt, f2, portaled))
        for nxt in _portal_exits(state, pid, coord):
            if _passable(state, pid, nxt) and cost <= max_cost:
                heapq.heappush(heap, (cost, steps + 1, nxt, flanked, True))
    return best


def _groups(tile, pid):
    mine = [u for u in tile.units if u.owner == pid]
    if not mine:
        return []
    groups = [mine]  # whole stack
    if len(mine) > 1:
        groups.extend([[u] for u in mine])
    return groups


def enumerate_moves(state, pid, *, waive_terrain: bool = False) -> list:
    p = state.player(pid)
    out = []
    for tile in state.tiles.values():
        for group in _groups(tile, pid):
            uids = sorted(u.uid for u in group)
            max_range = min(UNIT_STATS[u.type].move for u in group)
            has_cav = any(u.type == UnitType.CAVALRY for u in group)
            for dest, (cost, _steps, portaled) in _paths_from(
                    state, pid, tile.coord, max_range, p.ap, has_cav,
                    waive_terrain=waive_terrain).items():
                out.append({
                    "type": "move",
                    "from": list(tile.coord),
                    "dest": list(dest),
                    "uids": uids,
                    "cost": cost,
                    "portal": portaled,
                })
    return out


def apply_move(state, pid, choice) -> None:
    p = state.player(pid)
    src = state.tiles[tuple(choice["from"])]
    dst = state.tiles[tuple(choice["dest"])]
    moving = [u for u in src.units if u.uid in set(choice["uids"])]
    src.units = [u for u in src.units if u.uid not in set(choice["uids"])]
    dst.units.extend(moving)
    p.ap -= choice["cost"]
    if choice["portal"]:
        p.used_portal_travel = True
    # Tiles.md control method 3: neutral hex claimed immediately.
    if dst.controller is None:
        dst.controller = pid
