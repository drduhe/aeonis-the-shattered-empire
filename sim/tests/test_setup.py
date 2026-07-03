import random

from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.objectives import OBJECTIVES
from aeonis_sim.engine.types import UnitType


def make_state(players=4, seed=1):
    return build_initial_state({"players": players}, random.Random(seed))


def test_starting_resources_and_tracks():
    s = make_state()
    for p in s.players:
        assert p.ap == 5 and p.gold == 2 and p.mana == 2 and p.influence == 1
        assert p.renown == 0 and p.vp == 0
        # AL-4: pool 6 = cap 10 minus 4 pop occupied by starting units
        assert p.pop_pool == 6
        assert s.pop_cap(p.pid) == 10
        assert s.pop_used(p.pid) == 4


def test_starting_units_and_control():
    s = make_state()
    for p in s.players:
        home = s.tiles[p.home]
        types = sorted(u.type.value for u in home.units)
        assert types == ["archer", "infantry", "infantry", "infantry", "lord"]
        assert home.controller == p.pid
        # Home cluster of 4 controlled tiles
        assert len(s.controlled(p.pid)) == 4


def test_objectives_dealt_uniquely():
    s = make_state()
    objs = [p.objective for p in s.players]
    assert len(set(objs)) == len(objs)
    assert all(o in OBJECTIVES for o in objs)
