"""Reports module tests."""
from __future__ import annotations

from aeonis_sim.reports.hypotheses import evaluate_hypotheses, hypotheses_markdown
from aeonis_sim.reports.summary import (
    balance_summary,
    played_rounds,
    verdict_breakdown,
    win_rate_by_persona,
)


def _record(verdict="completed", winner_vp=10, loser_vp=3, persona="balanced", players=2):
    return {
        "verdict": verdict,
        "rounds": 12,
        "config": {"players": players, "personas": [persona] * players},
        "final_vp": {"0": winner_vp, "1": loser_vp},
        "vp_sources": {
            "0": {"coronation_rite": 3, "objective": 4, "coronation_milestone": 2},
            "1": {"coronation_rite": 2, "objective": 1},
        },
    }


def test_played_rounds_offset():
    assert played_rounds({"rounds": 14}) == 13


def test_verdict_breakdown():
    recs = [_record(), _record(verdict="timeout")]
    assert verdict_breakdown(recs) == {"completed": 1, "timeout": 1}


def test_win_rate_by_persona():
    warmonger_win = _record(persona="warmonger")
    economist_loss = {
        "verdict": "completed",
        "rounds": 12,
        "config": {"players": 2, "personas": ["economist", "warmonger"]},
        "final_vp": {"0": 3, "1": 10},
        "vp_sources": {"0": {}, "1": {"objective": 10}},
    }
    rates = win_rate_by_persona([warmonger_win, economist_loss])
    assert rates["warmonger"]["wins"] == 2  # both games have a warmonger winner seat
    assert rates["economist"]["wins"] == 0


def test_balance_summary_sections():
    md = balance_summary([_record()])
    assert "Verdict breakdown" in md
    assert "Win rate by persona" in md
    assert "Seat + streak combined" in md


def test_hypotheses_evaluation():
    results = evaluate_hypotheses([_record(), _record()])
    assert "H1" in results
    assert results["H1"]["status"] in ("confirmed", "killed", "inconclusive")
    md = hypotheses_markdown(results)
    assert "H1" in md
