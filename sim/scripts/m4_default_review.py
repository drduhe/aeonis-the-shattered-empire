"""Matched canonical-stack review for making full M4 Lord asymmetry default-on."""
from __future__ import annotations

import copy
import json
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aeonis_sim.reports.summary import (  # noqa: E402
    _completed,
    ap_economy_metrics,
    combat_metrics,
    played_rounds,
    win_rate_by_lord,
    win_rate_by_persona,
)
from aeonis_sim.runner.tournament import run_tournament  # noqa: E402

COUNTS = (4, 6, 8)
ROSTER = [
    "cassian",
    "seraphel",
    "vharok",
    "elyndra",
    "rakhis",
    "nyxara",
    "auriel",
    "thalrik",
]
VARIANTS = {
    "m4_off": {"lord_asymmetry": {"enabled": False}},
    "m4_on": {"lord_asymmetry": {"enabled": True, "roster": ROSTER}},
}


def _winner(record: dict) -> int:
    players = record["final_state"]["players"]
    return max(
        players,
        key=lambda p: (p["vp"], p["renown"], p["influence"], -p["pid"]),
    )["pid"]


def summarize(records: list[dict]) -> dict:
    done = _completed(records)
    combat = combat_metrics(records)
    ap = ap_economy_metrics(records)
    objective_shares = []
    for record in done:
        winner = _winner(record)
        vp = int(record["final_vp"].get(str(winner), record["final_vp"].get(winner, 0)))
        sources = record["vp_sources"].get(
            str(winner), record["vp_sources"].get(winner, {})
        )
        objective_shares.append(int(sources.get("objective", 0)) / max(vp, 1))
    return {
        "games": len(records),
        "verdicts": dict(Counter(r["verdict"] for r in records)),
        "mean_rounds": round(
            sum(played_rounds(r) for r in done) / len(done), 4
        ) if done else 0.0,
        "winner_objective_share": round(
            sum(objective_shares) / len(objective_shares), 4
        ) if objective_shares else 0.0,
        "actions_per_player_round": round(
            ap.get("actions_per_player_round", 0.0), 4
        ),
        "avg_action_gap": round(ap.get("avg_action_gap", 0.0), 4),
        "contested_attacker_win_rate": round(
            combat.get("contested_attacker_win_rate", 0.0), 4
        ),
        "battles_per_player_round": round(
            combat.get("battles_per_player_round", 0.0), 4
        ),
        "persona_win_rates": {
            name: round(row["win_rate"], 4)
            for name, row in win_rate_by_persona(records).items()
        },
        "lord_win_rates": {
            name: {
                "games": row["games"],
                "win_rate": round(row["win_rate"], 4),
            }
            for name, row in win_rate_by_lord(records).items()
        },
    }


def main() -> None:
    workers = min(8, os.cpu_count() or 1)
    output: dict[str, dict] = {}
    for players in COUNTS:
        base = json.loads(
            (ROOT / "configs" / f"bracket-m4-default-review-{players}p.json").read_text(
                encoding="utf-8"
            )
        )
        output[str(players)] = {}
        for name, overlay in VARIANTS.items():
            config = copy.deepcopy(base)
            config["name"] = f"{base['name']}-{name}"
            config.update(copy.deepcopy(overlay))
            print(f"RUN {players}p {name}", flush=True)
            result = summarize(run_tournament(config, workers=workers))
            output[str(players)][name] = result
            print(json.dumps(result, sort_keys=True), flush=True)
    dest = ROOT / "tmp-m4-default-review.json"
    dest.write_text(json.dumps(output, indent=2, sort_keys=True), encoding="utf-8")
    print(f"WROTE {dest}", flush=True)


if __name__ == "__main__":
    main()
