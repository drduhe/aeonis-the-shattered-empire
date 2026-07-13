from __future__ import annotations

import json
from pathlib import Path


def build_record(game) -> dict:
    s = game.state
    action_spreads = [
        max(row.values()) - min(row.values())
        for row in game.action_count_log
        if row
    ]
    player_rounds = sum(len(row) for row in game.action_count_log)
    total_actions = sum(sum(row.values()) for row in game.action_count_log)
    total_stranded = sum(entry["stranded_ap"] for entry in game.pass_log)
    first_passes = [entry for entry in game.pass_log if entry["order"] == 1]
    total_builds = sum(game.build_counts.values())
    players = len(s.players) or 1
    bookkeeping = dict(game.bookkeeping_stats)
    bookkeeping["upkeep_checks_per_player_round"] = (
        bookkeeping["upkeep_checks"] / player_rounds if player_rounds else 0.0
    )
    bookkeeping["upkeep_payments_per_player_round"] = (
        bookkeeping["upkeep_payments"] / player_rounds if player_rounds else 0.0
    )
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
            "max_action_gap": max(action_spreads) if action_spreads else 0,
            "avg_action_gap": (
                sum(action_spreads) / len(action_spreads) if action_spreads else 0.0
            ),
            "actions_per_player_round": (
                total_actions / player_rounds if player_rounds else 0.0
            ),
            "stranded_ap": total_stranded,
            "stranded_ap_per_player_round": (
                total_stranded / player_rounds if player_rounds else 0.0
            ),
            "avg_first_pass_after_actions": (
                sum(entry["actions_before_pass"] for entry in first_passes) / len(first_passes)
                if first_passes else 0.0
            ),
            "builds": total_builds,
            "builds_per_player_game": total_builds / players,
            "builds_by_player": dict(game.build_counts),
            "round_action_counts": list(game.action_count_log),
        },
        "event_stats": dict(game.event_stats),
        "council_stats": dict(game.council_stats),
        "negotiation_stats": dict(game.negotiation_stats),
        "building_stats": dict(game.building_stats),
        "bookkeeping_stats": bookkeeping,
        "whisper_stats": dict(game.whisper_stats),
        "first_artifact_round": game.first_artifact_round,
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
    config = dict(record["config"])
    if "lord_asymmetry" not in config:
        final_players = record.get("final_state", {}).get("players", [])
        if final_players and not any(p.get("lord_id") for p in final_players):
            # Records created before the M4 default omitted the flag because
            # neutral Lords were implicit. Preserve their historical ruleset.
            config["lord_asymmetry"] = {"enabled": False}
    g = Game(config, record["seed"])
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
