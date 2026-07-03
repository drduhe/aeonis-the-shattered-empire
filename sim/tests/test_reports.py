"""Reports module tests."""
from __future__ import annotations

from aeonis_sim.reports.hypotheses import evaluate_hypotheses, hypotheses_markdown
from aeonis_sim.reports.summary import (
    balance_summary,
    council_metrics,
    persona_parity_metrics,
    played_rounds,
    strategy_metrics,
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
    assert "H7" in results
    assert "H9" in results
    assert results["H1"]["status"] in ("confirmed", "killed", "inconclusive")
    md = hypotheses_markdown(results)
    assert "H1" in md
    assert "H7" in md


def test_persona_parity_metrics_mixed():
    rec = {
        "verdict": "completed",
        "rounds": 8,
        "config": {"players": 4, "personas": ["expander", "balanced", "warmonger", "diplomat"]},
        "final_vp": {"0": 10, "1": 4, "2": 3, "3": 2},
        "vp_sources": {"0": {"objective": 10}, "1": {}, "2": {}, "3": {}},
    }
    pm = persona_parity_metrics([rec])
    assert pm["expander_win_rate"] == 1.0
    assert pm["max_win_rate"] == 1.0


def test_strategy_metrics_from_choices():
    rec = {
        "verdict": "completed",
        "rounds": 5,
        "config": {"players": 4, "personas": ["balanced"] * 4},
        "final_vp": {"0": 10, "1": 3, "2": 2, "3": 1},
        "vp_sources": {},
        "choices": [
            {"type": "draft", "card": "resource_surge"},
            {"type": "draft", "card": "economic_boom"},
            {"type": "strategy_primary", "card": "resource_surge"},
            {"type": "strategy_secondary", "card": "resource_surge", "use": True},
            {"type": "strategy_secondary", "card": "economic_boom", "use": False},
        ],
    }
    sm = strategy_metrics([rec])
    assert sm["draft_picks"]["resource_surge"] == 1
    assert sm["primary_uses"]["resource_surge"] == 1
    assert sm["secondary_opt_in_rate"] == 0.5


def test_council_metrics_tracks_failures():
    rec = {
        "verdict": "completed",
        "rounds": 5,
        "config": {"players": 4, "personas": ["diplomat"] * 4},
        "final_vp": {"0": 10, "1": 3, "2": 2, "3": 1},
        "vp_sources": {},
        "council_stats": {
            "motions_proposed": 10,
            "motions_passed": 6,
            "motions_failed": 4,
            "votes_yes": 20,
            "votes_no": 12,
            "influence_spent": 8,
        },
    }
    cm = council_metrics([rec])
    assert cm["pass_rate"] == 0.6
    assert cm["yes_vote_rate"] == 20 / 32


def test_h9_diplomat_mixed_4p():
    records = []
    for i in range(40):
        winner = i % 4
        personas = ["expander", "balanced", "warmonger", "diplomat"]
        records.append({
            "verdict": "completed",
            "rounds": 8,
            "config": {"players": 4, "personas": personas},
            "final_vp": {str(p): (10 if p == winner else 4) for p in range(4)},
            "vp_sources": {str(winner): {"objective": 10}},
        })
    results = evaluate_hypotheses(records)
    assert results["H9"]["status"] == "killed"
    assert results["H9"]["detail"]["diplomat_win_rate"] >= 0.03
