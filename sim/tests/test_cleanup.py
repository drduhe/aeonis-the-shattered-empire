import random

from aeonis_sim.engine.cleanup import run_cleanup
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BuildingType, Terrain, Unit, UnitType, UNIT_STATS


def make_state():
    return build_initial_state({"players": 3}, random.Random(5))


def test_imperial_seat_vp_and_streak():
    s = make_state()
    for p in s.players:
        p.objective = None  # isolate seat VP from objective auto-scoring
    seat = next(t for t in s.tiles.values() if t.imperial_seat)
    seat.controller = 0
    for expected_vp, expected_streak in ((1, 1), (2, 2), (5, 3)):  # +2 bonus at 3
        run_cleanup(s)
        assert s.players[0].vp == expected_vp
        assert s.players[0].seat_streak == expected_streak
    assert s.players[0].vp_sources["imperial_seat"] == 3
    assert s.players[0].vp_sources["seat_streak_bonus"] == 2


def test_objective_scored_once():
    s = make_state()
    p = s.players[0]
    p.objective = "warlord"
    p.battle_wins = 2
    run_cleanup(s)
    assert p.vp == 2 and p.objective_scored
    run_cleanup(s)
    assert p.vp == 2  # not scored twice


def test_adjacency_claim_two_checks():
    s = make_state()
    p = s.players[0]
    for pl in s.players:
        pl.objective = None
    from aeonis_sim.engine.hexmap import neighbors
    # All in-disk neighbors of a corner home City are cluster tiles (controlled),
    # so manufacture a neutral one by un-claiming a cluster tile.
    neutral = next(c for c in neighbors(p.home)
                   if c in s.tiles and s.tiles[c].controller == p.pid)
    s.tiles[neutral].controller = None
    run_cleanup(s)
    assert s.tiles[neutral].controller is None
    assert s.tiles[neutral].adj_claim == (0, 1)
    run_cleanup(s)
    assert s.tiles[neutral].controller == 0  # second consecutive check


def test_lord_release():
    s = make_state()
    p1 = s.players[1]
    # Capture player 1's lord: remove from map, set flag
    coord, lord = s.find_lord(1)
    s.tiles[coord].units.remove(lord)
    p1.lord_captured = True
    run_cleanup(s)
    assert p1.lord_captured is False
    home_units = s.tiles[p1.home].units
    released = [u for u in home_units if u.type == UnitType.LORD]
    assert len(released) == 1 and released[0].hp == UNIT_STATS[UnitType.LORD].hp


def test_victory_check_sets_final():
    s = make_state()
    s.players[2].add_vp(10, "test")
    run_cleanup(s)
    assert s.final_round is True


def test_round_trackers_reset():
    s = make_state()
    p = s.players[0]
    p.recruited_cities = [p.home]
    p.passed = True
    run_cleanup(s)
    assert p.recruited_cities == [] and p.passed is False
    assert s.round == 2
