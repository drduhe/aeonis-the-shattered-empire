"""Structured negotiation — binding trades and tracked promises."""
from __future__ import annotations

import random

from aeonis_sim.engine.game import Game
from aeonis_sim.engine.negotiation import (
    apply_session_choice,
    check_attack_promises,
    check_payment_promises,
    enumerate_trade_starts,
    execute_transfer,
    expire_promises,
    start_session,
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


def test_population_is_not_tradeable_and_remnants_are():
    state = build_initial_state({"players": 3}, random.Random(13))
    state.player(0).pop_pool = 4
    state.player(0).remnants = 2
    state.player(1).remnants = 0

    execute_transfer(state, 0, 1, {"population": 2, "remnants": 1}, {})

    assert state.player(0).pop_pool == 4
    assert state.player(0).remnants == 1
    assert state.player(1).remnants == 1


def test_paid_non_aggression_is_logged_then_breaks_on_attack():
    state = build_initial_state({"players": 3}, random.Random(14))
    state.player(0).gold = 3
    stats = {}
    promises = []
    session = start_session(
        window="trade",
        proposer=0,
        target=1,
        gives={"gold": 1},
        gets={},
        promises=[{
            "kind": "non_aggression", "from": 1, "to": 0,
            "through_round": state.round + 1,
        }],
        motion=None,
        state=state,
        deal_kind="protection_payment",
    )

    closed, outcome = apply_session_choice(
        state, session, {"type": "negotiation_accept"},
        promises_log=promises, stats=stats,
    )
    assert closed is None and outcome == "accepted"
    assert state.player(0).gold == 2
    assert promises[0]["kept"] is None

    check_attack_promises(promises, attacker=1, defender=0, round_num=state.round, stats=stats)
    assert promises[0]["kept"] is False
    assert stats["non_aggression_promises_broken"] == 1


def test_non_aggression_kept_when_term_expires_without_attack():
    promises = [{
        "kind": "non_aggression", "from": 1, "to": 0,
        "round": 1, "through_round": 2, "kept": None,
    }]
    stats = {}

    expire_promises(promises, completed_round=2, stats=stats)

    assert promises[0]["kept"] is True
    assert stats["non_aggression_promises_kept"] == 1


def test_trade_enumerates_protection_mutual_pact_and_attack_contract():
    state = build_initial_state({"players": 3}, random.Random(15))
    state.player(0).gold = 10

    deal_kinds = {choice["deal_kind"] for choice in enumerate_trade_starts(state, 0)}

    assert {
        "resource_trade", "protection_payment", "mutual_non_aggression", "attack_contract",
    } <= deal_kinds


def test_attack_contract_and_future_payment_resolve_from_later_actions():
    promises = [
        {
            "kind": "attack_target", "from": 1, "to": 0, "target": 2,
            "round": 1, "through_round": 2, "kept": None,
        },
        {
            "kind": "future_payment", "from": 0, "to": 1, "resource": "gold",
            "amount": 2, "round": 1, "due_round": 2, "kept": None,
        },
    ]
    stats = {}

    check_attack_promises(promises, attacker=1, defender=2, round_num=2, stats=stats)
    check_payment_promises(
        promises, payer=0, recipient=1, paid={"gold": 2}, round_num=2, stats=stats,
    )

    assert all(promise["kept"] is True for promise in promises)
    assert stats["attack_target_promises_kept"] == 1
    assert stats["future_payment_promises_kept"] == 1


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
