from __future__ import annotations

import json
from pathlib import Path


def build_record(game) -> dict:
    s = game.state
    return {
        "seed": game.seed,
        "config": game.config,
        "choices": game.choices_log,
        "verdict": game.verdict,
        "degenerate_flags": game.degenerate_flags,
        "round_cap_finish": game.round_cap_finish,
        "rounds": s.round,
        "final_vp": {p.pid: p.vp for p in s.players},
        "vp_sources": {p.pid: p.vp_sources for p in s.players},
        "combat_stats": dict(game.combat_stats),
        "ap_economy_stats": {
            "max_spread": max(game.ap_spread_log) if game.ap_spread_log else 0,
            "avg_spread": (
                sum(game.ap_spread_log) / len(game.ap_spread_log)
                if game.ap_spread_log else 0.0
            ),
        },
        "event_stats": dict(game.event_stats),
        "council_stats": dict(game.council_stats),
        "negotiation_stats": dict(game.negotiation_stats),
        "building_stats": dict(game.building_stats),
        "final_state": s.to_dict(),
    }


def save_record(record: dict, path: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")


def replay(record: dict):
    """Re-run a recorded game; returns the reconstructed Game. Raises if any
    recorded choice is no longer legal (i.e., engine behavior changed)."""
    from .game import Game
    g = Game(record["config"], record["seed"])
    for choice in record["choices"]:
        dp = g.next_decision()
        while dp is None and not g.over:
            dp = g.next_decision()
        if g.over:
            break
        g.submit(choice)
    while not g.over and g.next_decision() is None:
        pass
    return g
