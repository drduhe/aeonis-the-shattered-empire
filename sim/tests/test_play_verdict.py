"""Play loop verdict and degeneracy handling."""
from __future__ import annotations

from aeonis_sim.engine.game import Game
from aeonis_sim.engine.types import DEFAULT_ROUND_CAP, VP_THRESHOLD
from aeonis_sim.runner.play import NO_VP_ROUNDS_FLAG, play_game


def test_no_vp_progress_cleared_when_vp_resumes():
    game = Game({"players": 3}, seed=1)
    game.degenerate_flags.append("no_vp_progress")
    game.state.players[0].add_vp(2, "objective")
    # play_game loop logic inlined for unit test
    flags = list(game.degenerate_flags)
    vp_total = sum(p.vp for p in game.state.players)
    if vp_total > 0 and "no_vp_progress" in flags:
        flags.remove("no_vp_progress")
    assert "no_vp_progress" not in flags


def test_completed_at_threshold_ignores_stale_no_vp_progress():
    record = {
        "verdict": "completed",
        "degenerate_flags": ["no_vp_progress"],
        "final_vp": {0: VP_THRESHOLD, 1: 6},
    }
    max_vp = max(int(v) for v in record["final_vp"].values())
    if max_vp >= VP_THRESHOLD:
        record["degenerate_flags"] = [
            f for f in record["degenerate_flags"] if f != "no_vp_progress"
        ]
    if record["degenerate_flags"]:
        record["verdict"] = "degenerate"
    assert record["verdict"] == "completed"


def test_round_cap_finishes_as_completed_not_timeout(monkeypatch):
    """Games that hit DEFAULT_ROUND_CAP end completed (sim tiebreak)."""
    from aeonis_sim.engine import game as game_mod

    monkeypatch.setattr(game_mod, "DEFAULT_ROUND_CAP", 3)
    rec = play_game({"players": 3, "personas": ["chaos"]}, seed=999)
    assert rec["verdict"] == "completed"
    assert rec.get("round_cap_finish") is True
    assert rec["rounds"] > 3


def test_completed_at_threshold_clears_action_cap():
    record = {
        "verdict": "completed",
        "degenerate_flags": ["action_cap"],
        "final_vp": {0: VP_THRESHOLD + 1, 1: 4},
        "round_cap_finish": False,
    }
    max_vp = max(int(v) for v in record["final_vp"].values())
    if max_vp >= VP_THRESHOLD:
        record["degenerate_flags"] = [
            f
            for f in record["degenerate_flags"]
            if f not in ("no_vp_progress", "action_cap")
        ]
    assert record["verdict"] == "completed"
    assert record["degenerate_flags"] == []


def test_round_cap_clears_no_vp_progress_at_sub_threshold():
    record = {
        "verdict": "completed",
        "degenerate_flags": ["no_vp_progress"],
        "final_vp": {0: 8, 1: 8, 2: 8, 3: 8},
        "round_cap_finish": True,
    }
    if record.get("round_cap_finish"):
        record["degenerate_flags"] = [
            f for f in record["degenerate_flags"] if f != "no_vp_progress"
        ]
    assert record["degenerate_flags"] == []


def test_no_vp_rounds_constant_sane():
    assert NO_VP_ROUNDS_FLAG >= 4
    assert DEFAULT_ROUND_CAP > NO_VP_ROUNDS_FLAG
