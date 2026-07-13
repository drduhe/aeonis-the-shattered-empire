import random

import pytest

from aeonis_sim.engine.build import apply_build
from aeonis_sim.engine.cleanup import run_cleanup
from aeonis_sim.engine.combat import finish_battle, start_battle
from aeonis_sim.engine.council import apply_motion
from aeonis_sim.engine.objectives import (
    SECRET_OBJECTIVE_IDS,
    SECRET_OBJECTIVES,
    apply_secret_discard_at_cap,
    apply_secret_keep,
    deal_round3_secrets,
    deal_secret_draw,
    draw_public_to_row,
    try_immediate_secrets,
)
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BuildingType, Unit, UnitType, UNIT_STATS


def make_state(seed=1, players=4):
    return build_initial_state({"players": players}, random.Random(seed))


def test_all_fp_secrets_registered():
    for sid in (
        "hidden_arsenal",
        "golden_hoard",
        "mana_flood",
        "quiet_knife",
        "borderbreaker",
        "architect_of_control",
    ):
        assert sid in SECRET_OBJECTIVES


def test_setup_one_secret_each():
    s = make_state()
    for p in s.players:
        assert len(p.secret_objectives) == 1


def test_round3_second_secret_draw():
    s = make_state(seed=42)
    s.round = 3
    s.secret_objective_deck = list(SECRET_OBJECTIVE_IDS)
    before = [len(p.secret_objectives) for p in s.players]
    deal_round3_secrets(s, random.Random(99))
    after = [len(p.secret_objectives) for p in s.players]
    assert all(a == b + 1 for a, b in zip(after, before))


def test_secret_cap_draw_two_keep_one():
    s = make_state(seed=7)
    p = s.players[0]
    p.secret_objectives = ["golden_hoard", "mana_flood", "architect_of_control"]
    s.secret_objective_deck = ["quiet_knife", "borderbreaker", "hidden_arsenal"]
    payload = deal_secret_draw(s, 0, random.Random(1))
    assert payload is not None
    assert payload["step"] == "keep"
    assert len(payload["drawn"]) == 2
    nxt = apply_secret_keep(s, 0, payload["drawn"][0], payload["drawn"], random.Random(1))
    assert nxt is not None and nxt["step"] == "discard"
    apply_secret_discard_at_cap(s, 0, payload["drawn"][0], "golden_hoard")
    assert len(p.secret_objectives) == 3
    assert payload["drawn"][0] in p.secret_objectives
    assert "golden_hoard" not in p.secret_objectives


def test_hidden_arsenal_predicate():
    s = make_state()
    p = s.players[0]
    coord = p.home
    p.fortress_built.append(coord)
    assert not SECRET_OBJECTIVES["hidden_arsenal"](s, 0)
    p.battle_wins_at.append(coord)
    assert SECRET_OBJECTIVES["hidden_arsenal"](s, 0)


def test_quiet_knife_via_annexation():
    s = make_state(seed=3)
    proposer = 0
    apply_motion(s, "imperial_annexation", proposer)
    if s.players[proposer].influence_hex_gains:
        assert SECRET_OBJECTIVES["quiet_knife"](s, proposer)


def test_borderbreaker_three_hexes_apart():
    s = make_state()
    p = s.players[0]
    hexes = [(0, 0), (3, 0), (0, 3)]
    for i, coord in enumerate(hexes):
        if coord not in s.tiles:
            pytest.skip("map lacks test hexes")
        s.tiles[coord].controller = 0
        s.tiles[coord].units.append(
            Unit(uid=900 + i, owner=0, type=UnitType.INFANTRY, hp=2)
        )
    assert SECRET_OBJECTIVES["borderbreaker"](s, 0)


def test_immediate_golden_hoard():
    s = make_state()
    p = s.players[0]
    p.secret_objectives = ["golden_hoard"]
    p.gold = 10
    scored = try_immediate_secrets(s, 0)
    assert scored == ["golden_hoard"]
    assert p.vp == 2
    assert "golden_hoard" not in p.secret_objectives


def test_cleanup_scores_secret():
    s = make_state()
    p = s.players[0]
    p.secret_objectives = ["golden_hoard"]
    p.gold = 10
    run_cleanup(s)
    assert p.vp >= 2 or "golden_hoard" in p.secrets_scored


def test_winds_public_draw():
    s = make_state()
    n_before = len(s.shared_public_revealed)
    assert draw_public_to_row(s, random.Random(12))
    assert len(s.shared_public_revealed) == n_before + 1


def test_fortress_build_tracked():
    s = make_state(seed=5)
    p = s.players[0]
    home = s.tiles[p.home]
    home.gold = 20
    home.mana = 10
    home.influence = 5
    p.gold = 20
    p.mana = 10
    p.influence = 5
    p.ap = 5
    p.pop_pool = 5
    apply_build(s, 0, {"hex": list(p.home), "building": BuildingType.FORTRESS.value})
    assert p.home in p.fortress_built
