"""Structured negotiation — binding trades and tracked promises."""
from __future__ import annotations

import random

from aeonis_sim.engine.game import Game
from aeonis_sim.engine.negotiation import (
    execute_transfer,
    validate_offer,
)
from aeonis_sim.engine.setup import build_initial_state

from .conftest import advance_to_action_phase, complete_strategy_draft


def test_resource_trade_executes():
    state = build_initial_state({"players": 3}, random.Random(11))
    state.player(0).gold = 5
    state.player(0).mana = 0
    state.player(1).gold = 0
    state.player(1).mana = 3
    execute_transfer(state, 0, 1, {"gold": 2}, {"mana": 1})
    assert state.player(0).gold == 3
    assert state.player(0).mana == 1
    assert state.player(1).gold == 2
    assert state.player(1).mana == 2


def test_illegal_offer_rejected():
    state = build_initial_state({"players": 3}, random.Random(12))
    state.player(0).gold = 1
    err = validate_offer(state, 0, 1, {"gold": 5}, {})
    assert err == "proposer cannot afford gives"


def test_council_negotiation_before_vote():
    g = Game({"players": 3}, seed=201)
    complete_strategy_draft(g)
    while True:
        dp = g.next_decision()
        if dp is None:
            break
        if dp.kind == "council_propose":
            g.submit({"type": "council_propose", "motion": dp.choices[-1]["motion"]})
            continue
        if dp.kind == "negotiation":
            assert dp.phase == "council"
            return
        g.submit(dp.choices[0])
    raise AssertionError("negotiation phase not reached")


def test_trade_action_opens_negotiation():
    g = Game({"players": 3}, seed=202)
    advance_to_action_phase(g)
    dp = g.next_decision()
    assert dp.kind == "action"
    trade_choices = [c for c in dp.choices if c["type"] == "trade"]
    assert trade_choices
    g.submit(trade_choices[0])
    dp2 = g.next_decision()
    assert dp2 is not None
    assert dp2.kind == "negotiation"
    assert dp2.pid == trade_choices[0]["target"]


def test_accepted_trade_transfers_resources():
    g = Game({"players": 3}, seed=203)
    advance_to_action_phase(g)
    dp = g.next_decision()
    initiator = dp.pid
    before_ap = g.state.player(initiator).ap
    trade = next(c for c in dp.choices if c["type"] == "trade")
    g.submit(trade)
    dp2 = g.next_decision()
    g.submit({"type": "negotiation_accept"})
    assert g._negotiation_session is None
    assert g.state.player(initiator).ap == before_ap - 1
    assert g.negotiation_stats["offers_accepted"] >= 1
