import random

from aeonis_sim.engine.move import enumerate_moves, apply_move
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import Terrain, Tile, Unit, UnitType, UNIT_STATS


def make_state():
    return build_initial_state({"players": 3}, random.Random(5))


def strip_map(state):
    """Clear all units off the board for hand-built scenarios."""
    for t in state.tiles.values():
        t.units = []
        t.controller = None
    return state


def put(state, coord, owner, utype, terrain=None):
    if terrain is not None:
        state.tiles[coord].terrain = terrain
    u = Unit(uid=state.new_uid(), owner=owner, type=utype, hp=UNIT_STATS[utype].hp)
    state.tiles[coord].units.append(u)
    return u


def test_infantry_range_and_cost():
    s = strip_map(make_state())
    put(s, (0, 0), 0, UnitType.INFANTRY, terrain=Terrain.PLAINS)
    s.players[0].ap = 5
    moves = enumerate_moves(s, 0)
    dests = {tuple(m["dest"]) for m in moves}
    # Infantry range 1: only the 6 neighbors (minus impassable), never distance 2
    assert all(
        max(abs(d[0]), abs(d[1]), abs(d[0] + d[1])) <= 1 or s.tiles[d].terrain == Terrain.PORTAL
        for d in dests
    )


def test_mountain_costs_2():
    s = strip_map(make_state())
    put(s, (0, 0), 0, UnitType.INFANTRY, terrain=Terrain.PLAINS)
    s.tiles[(1, 0)].terrain = Terrain.MOUNTAIN
    s.players[0].ap = 5
    moves = enumerate_moves(s, 0)
    m = next(m for m in moves if tuple(m["dest"]) == (1, 0))
    assert m["cost"] == 2


def test_zoc_surcharge_and_cavalry_flanking():
    s = strip_map(make_state())
    put(s, (0, 0), 0, UnitType.INFANTRY, terrain=Terrain.PLAINS)
    put(s, (2, -1), 1, UnitType.INFANTRY, terrain=Terrain.PLAINS)  # enemy adj to (1,0) and (1,-1)
    s.tiles[(1, 0)].terrain = Terrain.PLAINS
    s.players[0].ap = 5
    moves = enumerate_moves(s, 0)
    m = next(m for m in moves if tuple(m["dest"]) == (1, 0))
    assert m["cost"] == 2  # 1 terrain + 1 ZOC
    # Same spot with cavalry: first ZOC hex is exempt
    s2 = strip_map(make_state())
    put(s2, (0, 0), 0, UnitType.CAVALRY, terrain=Terrain.PLAINS)
    put(s2, (2, -1), 1, UnitType.INFANTRY, terrain=Terrain.PLAINS)
    s2.tiles[(1, 0)].terrain = Terrain.PLAINS
    s2.players[0].ap = 5
    m2 = next(m for m in enumerate_moves(s2, 0) if tuple(m["dest"]) == (1, 0))
    assert m2["cost"] == 1


def test_cannot_enter_occupied_or_unbridged_lake():
    s = strip_map(make_state())
    put(s, (0, 0), 0, UnitType.INFANTRY, terrain=Terrain.PLAINS)
    put(s, (1, 0), 1, UnitType.INFANTRY)
    s.tiles[(0, 1)].terrain = Terrain.LAKE
    s.players[0].ap = 5
    dests = {tuple(m["dest"]) for m in enumerate_moves(s, 0)}
    assert (1, 0) not in dests
    assert (0, 1) not in dests


def test_apply_move_claims_neutral_and_pays_ap():
    s = strip_map(make_state())
    u = put(s, (0, 0), 0, UnitType.INFANTRY, terrain=Terrain.PLAINS)
    s.tiles[(1, 0)].terrain = Terrain.PLAINS
    s.players[0].ap = 5
    m = next(m for m in enumerate_moves(s, 0) if tuple(m["dest"]) == (1, 0))
    apply_move(s, 0, m)
    assert s.players[0].ap == 5 - m["cost"]
    assert any(x.uid == u.uid for x in s.tiles[(1, 0)].units)
    assert s.tiles[(1, 0)].controller == 0  # neutral hex claimed immediately


def test_portal_travel_zero_ap_and_flag():
    s = strip_map(make_state())
    portals = [c for c, t in s.tiles.items() if t.terrain == Terrain.PORTAL]
    a, b = portals[0], portals[1]
    put(s, a, 0, UnitType.INFANTRY)
    s.tiles[a].controller = 0
    s.players[0].ap = 5
    m = next(m for m in enumerate_moves(s, 0) if tuple(m["dest"]) == b)
    assert m["cost"] == 0
    apply_move(s, 0, m)
    assert s.players[0].used_portal_travel is True
