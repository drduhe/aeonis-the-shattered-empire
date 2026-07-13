import random

from aeonis_sim.engine.invariants import check_invariants
from aeonis_sim.engine.recruit import enumerate_recruits
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BuildingType, Terrain, Unit, UNIT_STATS, UnitType


def test_pop_used_may_exceed_cap_without_invariant_failure():
    """AL-15: involuntary overflow is legal; pool gates voluntary recruit."""
    s = build_initial_state(
        {"players": 3, "lord_asymmetry": {"enabled": False}},
        random.Random(2),
    )
    p = s.players[0]
    # Simulate post-conquest board: many units/buildings without paying the pool.
    for tile in s.controlled(0):
        if tile.terrain == Terrain.PLAINS and not tile.buildings:
            tile.buildings.append(BuildingType.FARM)
    extra = next(t for t in s.tiles.values() if t.controller is None and t.terrain == Terrain.PLAINS)
    extra.controller = 0
    extra.buildings.append(BuildingType.CASTLE)
    for _ in range(9):
        extra.units.append(
            Unit(uid=s.new_uid(), owner=0, type=UnitType.INFANTRY, hp=UNIT_STATS[UnitType.INFANTRY].hp)
        )
    p.pop_pool = 0
    assert s.pop_used(0) > s.pop_cap(0)
    check_invariants(s)
    assert enumerate_recruits(s, 0) == []
