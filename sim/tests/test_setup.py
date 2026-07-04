import random

from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.objectives import PUBLIC_OBJECTIVES, SECRET_OBJECTIVES
from aeonis_sim.engine.types import UnitType


def make_state(players=4, seed=1):
    return build_initial_state({"players": players}, random.Random(seed))


def test_starting_resources_and_tracks():
    s = make_state()
    for p in s.players:
        assert p.ap == 5 and p.gold == 2 and p.mana == 2 and p.influence == 1
        assert p.renown == 0 and p.vp == 0
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
        assert len(s.controlled(p.pid)) == 4


def test_staged_economy_opening_from_objectives_config():
    s = build_initial_state(
        {"players": 4, "objectives": {"staged_economy_opening": True}},
        random.Random(99),
    )
    assert set(s.shared_public_revealed) == {"builder", "merchant_lord"}
    assert len(s.shared_public_deck) == 4
    assert not {"builder", "merchant_lord"} & set(s.shared_public_deck)


def test_shared_public_row_and_secrets():
    s = make_state()
    assert len(s.shared_public_revealed) == 2
    assert all(o in PUBLIC_OBJECTIVES for o in s.shared_public_revealed)
    secrets = [p.secret_objectives[0] for p in s.players if p.secret_objectives]
    assert all(o in SECRET_OBJECTIVES for o in secrets)
