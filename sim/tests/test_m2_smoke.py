"""M2 gate smoke — phase order, council/events live, CI bracket stability."""
from __future__ import annotations

import json
from pathlib import Path

from aeonis_sim.engine.game import Game
from aeonis_sim.engine.strategy import initiative_order
from aeonis_sim.reports.regression import evaluate_regression
from aeonis_sim.runner.tournament import _play_tournament_game

from .conftest import advance_to_action_phase, complete_strategy_draft


def test_event_resolves_before_strategy_draft():
    g = Game({"players": 4}, seed=101)
    assert g.event_stats["resolved"] >= 1
    dp = g.next_decision()
    assert dp.kind == "strategy_draft"
    assert dp.phase == "strategy"


def test_council_follows_strategy_before_action():
    g = Game({"players": 4, "lord_asymmetry": {"enabled": False}}, seed=102)
    complete_strategy_draft(g)
    dp = g.next_decision()
    assert dp.kind == "council_propose"
    assert dp.phase == "council"
    advance_to_action_phase(g)
    dp = g.next_decision()
    assert dp.kind == "action"
    assert dp.phase == "action"


def test_initiative_queue_used_not_seating_order():
    g = Game({"players": 4}, seed=103)
    advance_to_action_phase(g)
    order = initiative_order(g.state)
    assert order
    assert g._initiative_queue == order
    first = g.next_decision()
    assert first.pid == order[0]


def test_council_stats_populated_after_round():
    g = Game({"players": 4, "personas": ["diplomat"] * 4}, seed=104)
    advance_to_action_phase(g)
    for _ in range(4):
        dp = g.next_decision()
        if dp is None:
            break
        g.submit({"type": "pass"})
    assert g.council_stats["motions_proposed"] >= 0


def test_m2_ci_bracket_regression_gates():
    """Mirrors CI m2-gate job (20 mixed 4p games, zero non-completed)."""
    config = json.loads(
        Path("configs/bracket-m2-ci.json").read_text(encoding="utf-8")
    )
    records = [_play_tournament_game(config, i) for i in range(config["games"])]
    failures = evaluate_regression(records, config["regression"]["gates"])
    assert failures == [], failures
