import random

from aeonis_sim.engine.recruit import enumerate_recruits, apply_recruit
from aeonis_sim.engine.setup import build_initial_state


def make_state():
    return build_initial_state(
        {"players": 3, "lord_asymmetry": {"enabled": False}},
        random.Random(5),
    )


def test_enumerates_affordable_combos_at_home_city():
    s = make_state()
    p = s.players[0]  # 2 gold, 2 mana, pool 6
    recs = enumerate_recruits(s, 0)
    assert all(tuple(r["city"]) == p.home for r in recs)
    combos = {tuple(sorted(r["units"])) for r in recs}
    # 2 gold buys: 1 inf, 2 inf, 1 cav, 1 archer(1g1m), 2 archers, inf+archer
    assert ("infantry", "infantry") in combos
    assert ("cavalry",) in combos
    assert ("archer", "infantry") in combos
    # cavalry+anything needs 3+ gold -> absent
    assert not any("cavalry" in c and len(c) == 2 for c in combos)


def test_apply_recruit_pays_and_places():
    s = make_state()
    p = s.players[0]
    rec = next(r for r in enumerate_recruits(s, 0)
               if sorted(r["units"]) == ["archer", "infantry"])
    apply_recruit(s, 0, rec)
    assert p.ap == 4 and p.gold == 0 and p.mana == 1
    assert p.pop_pool == 4  # 6 - 2
    home = s.tiles[p.home]
    assert len(home.units) == 7  # 5 starting + 2
    assert p.recruited_cities == [p.home]


def test_city_reuse_blocked_within_round():
    s = make_state()
    rec = next(r for r in enumerate_recruits(s, 0) if r["units"] == ["infantry"])
    apply_recruit(s, 0, rec)
    assert enumerate_recruits(s, 0) == []  # only city already used


def test_pop_pool_blocks_recruiting():
    s = make_state()
    s.players[0].pop_pool = 0
    assert enumerate_recruits(s, 0) == []
