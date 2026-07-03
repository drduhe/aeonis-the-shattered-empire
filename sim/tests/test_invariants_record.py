import random

import pytest

from aeonis_sim.engine.game import Game
from aeonis_sim.engine.invariants import InvariantViolation, check_invariants
from aeonis_sim.engine.record import build_record, replay
from aeonis_sim.engine.setup import build_initial_state


def test_invariants_pass_on_fresh_state():
    s = build_initial_state({"players": 4}, random.Random(2))
    check_invariants(s)


def test_invariants_catch_negative_gold():
    s = build_initial_state({"players": 3}, random.Random(2))
    s.players[0].gold = -1
    with pytest.raises(InvariantViolation):
        check_invariants(s)


def _play_short_game(seed):
    g = Game({"players": 3}, seed=seed)
    while not g.over:
        dp = g.next_decision()
        if dp is None:
            continue
        # Deterministic policy: first choice in canonical order
        choice = sorted(dp.choices, key=lambda c: str(sorted(c.items())))[0]
        g.submit(choice)
    return g


def test_record_replay_reproduces_final_state():
    g = _play_short_game(21)
    rec = build_record(g)
    g2 = replay(rec)
    assert g2.verdict == g.verdict
    assert g2.state.to_dict() == g.state.to_dict()
