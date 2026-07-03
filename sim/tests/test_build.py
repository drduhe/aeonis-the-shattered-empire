import random

from aeonis_sim.engine.build import enumerate_builds, apply_build
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BuildingType, Terrain


def make_state():
    s = build_initial_state({"players": 3}, random.Random(5))
    s.players[0].gold = 20
    s.players[0].mana = 20
    s.players[0].influence = 20
    return s


def options(state, pid):
    return {(tuple(b["hex"]), b["building"]) for b in enumerate_builds(state, pid)}


def test_terrain_matching():
    s = make_state()
    p = s.players[0]
    opts = options(s, 0)
    plains = next(t.coord for t in s.controlled(0) if t.terrain == Terrain.PLAINS)
    mountain = next(t.coord for t in s.controlled(0) if t.terrain == Terrain.MOUNTAIN)
    assert (plains, "farm") in opts
    assert (mountain, "mine") in opts
    assert (plains, "mine") not in opts
    assert (p.home, "guild_hall") in opts
    assert (plains, "tower") in opts  # any-terrain building


def test_apply_build_farm():
    s = make_state()
    p = s.players[0]
    plains = next(t.coord for t in s.controlled(0) if t.terrain == Terrain.PLAINS)
    cap_before = s.pop_cap(0)
    pool_before = p.pop_pool
    choice = next(b for b in enumerate_builds(s, 0)
                  if tuple(b["hex"]) == plains and b["building"] == "farm")
    apply_build(s, 0, choice)
    assert p.ap == 2 and p.gold == 18
    assert s.tiles[plains].has(BuildingType.FARM)
    assert s.pop_cap(0) == cap_before + 2      # Farm: +2 cap
    assert p.pop_pool == pool_before - 1        # occupies 1 pop


def test_slot_limits():
    s = make_state()
    plains = next(t.coord for t in s.controlled(0) if t.terrain == Terrain.PLAINS)
    farm = next(b for b in enumerate_builds(s, 0)
                if tuple(b["hex"]) == plains and b["building"] == "farm")
    apply_build(s, 0, farm)
    s.players[0].ap = 5
    # Basic terrain: 1 building max -> no more options on that hex
    assert not any(tuple(b["hex"]) == plains for b in enumerate_builds(s, 0))


def test_bridge_requires_adjacent_control_and_claims_lake():
    s = make_state()
    from aeonis_sim.engine.hexmap import neighbors
    lake = next(c for c, t in s.tiles.items() if t.terrain == Terrain.LAKE)
    # Give player 0 control of a neighbor of the lake (clear units to be safe)
    nb = next(c for c in neighbors(lake) if c in s.tiles
              and s.tiles[c].terrain != Terrain.LAKE)
    s.tiles[nb].controller = 0
    choice = next(b for b in enumerate_builds(s, 0)
                  if tuple(b["hex"]) == lake and b["building"] == "bridge")
    apply_build(s, 0, choice)
    assert s.tiles[lake].has(BuildingType.BRIDGE)
    assert s.tiles[lake].controller == 0  # AL-6
