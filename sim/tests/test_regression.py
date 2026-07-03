"""Regression gate evaluator tests."""
from __future__ import annotations

from aeonis_sim.reports.regression import evaluate_regression, regression_markdown


def _record(
    verdict: str = "completed",
    *,
    battles: int = 10,
    attacker_wins: int = 8,
    lord_capture: float = 0.15,
    avg_spread: float = 1.0,
    max_spread: int = 2,
) -> dict:
    winner_vp = 10
    lord_vp = int(round(winner_vp * lord_capture))
    other_vp = winner_vp - lord_vp
    return {
        "verdict": verdict,
        "config": {"players": 4},
        "final_vp": {0: winner_vp, 1: 3},
        "vp_sources": {
            0: {"lord_capture": lord_vp, "objective": other_vp},
            1: {"objective": 3},
        },
        "combat_stats": {
            "battles": battles,
            "attacker_wins": attacker_wins,
            "defender_wins": battles - attacker_wins,
        },
        "ap_economy_stats": {"avg_spread": avg_spread, "max_spread": max_spread},
        "rounds": 5,
        "players": 4,
    }


def test_evaluate_regression_passes_in_band():
    records = [_record() for _ in range(10)]
    gates = [
        {"metric": "crash_rate", "max": 0.0},
        {"metric": "attacker_win_rate", "min": 0.70, "max": 0.90},
    ]
    assert evaluate_regression(records, gates) == []


def test_evaluate_regression_flags_high_attacker_win():
    records = [_record(attacker_wins=10, battles=10) for _ in range(5)]
    gates = [{"metric": "attacker_win_rate", "max": 0.85}]
    failures = evaluate_regression(records, gates)
    assert len(failures) == 1
    assert failures[0]["metric"] == "attacker_win_rate"


def test_evaluate_regression_ap_spread():
    records = [_record(max_spread=6) for _ in range(3)]
    gates = [{"metric": "max_ap_spread", "max": 4.0}]
    failures = evaluate_regression(records, gates)
    assert failures[0]["metric"] == "max_ap_spread"


def test_regression_markdown_includes_status():
    records = [_record()]
    gates = [{"metric": "completed_rate", "label": "Done", "min": 0.5}]
    body = regression_markdown(records, gates, [])
    assert "pass" in body
    assert "Done" in body
