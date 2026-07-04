import random

from aeonis_sim.engine.cleanup import run_cleanup
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BuildingType, Unit, UnitType, UNIT_STATS


def make_state():
    return build_initial_state({"players": 3}, random.Random(5))


def put(s, coord, owner, utype):
    u = Unit(uid=s.new_uid(), owner=owner, type=utype, hp=UNIT_STATS[utype].hp)
    s.tiles[coord].units.append(u)
    return u


def test_seat_of_empire_vp_from_seat_rewards_config():
    s = build_initial_state(
        {"players": 3, "seat_rewards": {"seat_of_empire_vp": 1}},
        random.Random(77),
    )
    assert s.seat_of_empire_vp == 1
    seat = next(t for t in s.tiles.values() if t.imperial_seat)
    seat.controller = 0
    s.shared_public_revealed = ["seat_of_empire"]
    from aeonis_sim.engine.cleanup import _score_objectives

    _score_objectives(s, 0)
    assert s.players[0].vp == 1
    assert s.players[0].vp_sources["objective"] == 1


def test_objectives_frontier_lord_min_hexes_from_config():
    s = build_initial_state(
        {"players": 4, "objectives": {"frontier_lord_min_hexes": 8}},
        random.Random(88),
    )
    assert s.frontier_lord_min_hexes == 8


def test_pacing_vp_threshold_from_config():
    s = build_initial_state(
        {"players": 4, "pacing": {"vp_threshold": 12}},
        random.Random(99),
    )
    assert s.vp_threshold == 12


def test_shared_public_row_setup():
    s = make_state()
    assert len(s.shared_public_revealed) == 2
    assert len(s.shared_public_deck) == 4  # 6 public cards (merchant_lord experiment)


def test_coronation_rite_requires_lord_on_seat():
    s = make_state()
    s.shared_public_revealed = []
    s.players[0].secret_objectives = []
    seat = next(t for t in s.tiles.values() if t.imperial_seat)
    seat.controller = 0
    # Control without Lord on seat — no VP
    run_cleanup(s)
    assert s.players[0].vp == 0
    # Move Lord onto seat
    lord_coord, lord = s.find_lord(0)
    seat.units.append(lord)
    s.tiles[lord_coord].units.remove(lord)
    for expected_vp, expected_rites in ((1, 1), (2, 2), (5, 3)):
        run_cleanup(s)
        assert s.players[0].vp == expected_vp
        assert s.players[0].rite_count == expected_rites
    assert s.players[0].vp_sources["coronation_rite"] == 3
    assert s.players[0].vp_sources["coronation_milestone"] == 2


def test_shared_objective_scored_once_per_player():
    s = make_state()
    p = s.players[0]
    s.shared_public_revealed = ["warlord"]
    p.battle_wins = 2
    run_cleanup(s)
    assert p.vp == 2 and "warlord" in p.shared_scored
    run_cleanup(s)
    assert p.vp == 2


def test_one_public_objective_per_round():
    s = make_state()
    p = s.players[0]
    p.secret_objectives = []
    s.shared_public_revealed = ["warlord", "frontier_lord"]
    p.battle_wins = 2
    while len(s.controlled(0)) < 7:
        for t in s.tiles.values():
            if t.controller is None and not t.imperial_seat:
                t.controller = 0
                break
    run_cleanup(s)
    assert p.vp == 2  # only one public scored this round
    run_cleanup(s)
    assert p.vp == 4


def test_merchant_lord_scores_at_8_gold():
    s = make_state()
    p = s.players[0]
    s.shared_public_revealed = ["merchant_lord"]
    p.gold = 7
    run_cleanup(s)
    assert p.vp == 0 and "merchant_lord" not in p.shared_scored
    p.gold = 8
    run_cleanup(s)
    assert p.vp == 2 and "merchant_lord" in p.shared_scored
    run_cleanup(s)
    assert p.vp == 2  # scores once


def test_secret_objective_scored_once():
    s = make_state()
    p = s.players[0]
    s.shared_public_revealed = []  # isolate from merchant_lord public (also gold-based)
    p.secret_objectives = ["golden_hoard"]
    p.gold = 10
    run_cleanup(s)
    assert p.vp == 2 and "golden_hoard" in p.secrets_scored
    run_cleanup(s)
    assert p.vp == 2


def test_adjacency_claim_two_checks():
    s = make_state()
    p = s.players[0]
    from aeonis_sim.engine.hexmap import neighbors
    neutral = next(c for c in neighbors(p.home)
                   if c in s.tiles and s.tiles[c].controller == p.pid)
    s.tiles[neutral].controller = None
    run_cleanup(s)
    assert s.tiles[neutral].controller is None
    assert s.tiles[neutral].adj_claim == (0, 1)
    run_cleanup(s)
    assert s.tiles[neutral].controller == 0


def test_lord_release():
    s = make_state()
    p1 = s.players[1]
    coord, lord = s.find_lord(1)
    s.tiles[coord].units.remove(lord)
    p1.lord_captured = True
    run_cleanup(s)
    assert p1.lord_captured is False
    home_units = s.tiles[p1.home].units
    released = [u for u in home_units if u.type == UnitType.LORD]
    assert len(released) == 1 and released[0].hp == UNIT_STATS[UnitType.LORD].hp


def test_lord_release_to_nearest_safe_hex_when_home_held():
    s = make_state()
    p1 = s.players[1]
    coord, lord = s.find_lord(1)
    s.tiles[coord].units.remove(lord)
    p1.lord_captured = True
    s.tiles[p1.home].controller = 0
    s.tiles[p1.home].units = []
    put(s, p1.home, 0, UnitType.INFANTRY)
    for t in s.controlled(1):
        if t.coord != p1.home:
            t.units = []
    run_cleanup(s)
    assert p1.lord_captured is False
    lord_coord, _ = s.find_lord(1)
    assert lord_coord is not None and lord_coord != p1.home


def test_enemy_fortress_blocks_adjacency_claim():
    s = make_state()
    p = s.players[0]
    from aeonis_sim.engine.hexmap import neighbors
    neutral = next(c for c in neighbors(p.home)
                   if c in s.tiles and s.tiles[c].controller == p.pid)
    s.tiles[neutral].controller = None
    for n in neighbors(neutral):
        nt = s.tiles.get(n)
        if nt is None:
            continue
        if nt.controller != 1:
            nt.controller = 1
        nt.buildings.append(BuildingType.FORTRESS)
        break
    run_cleanup(s)
    assert s.tiles[neutral].adj_claim is None
    run_cleanup(s)
    assert s.tiles[neutral].controller is None


def test_coronation_milestone_once_per_game_after_broken_streak():
    s = make_state()
    seat = next(t for t in s.tiles.values() if t.imperial_seat)
    seat.controller = 0
    lord_coord, lord = s.find_lord(0)
    seat.units.append(lord)
    s.tiles[lord_coord].units.remove(lord)
    run_cleanup(s)
    run_cleanup(s)
    seat.controller = None
    run_cleanup(s)
    seat.controller = 0
    run_cleanup(s)
    assert s.players[0].vp_sources.get("coronation_milestone", 0) == 2
    assert s.players[0].rite_bonus_scored is True
    vp_before = s.players[0].vp
    for _ in range(3):
        run_cleanup(s)
    assert s.players[0].vp_sources.get("coronation_milestone", 0) == 2
    assert s.players[0].vp > vp_before


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
    p.public_scored_this_round = True
    run_cleanup(s)
    assert p.recruited_cities == [] and p.passed is False
    assert p.public_scored_this_round is False
    assert s.round == 2
