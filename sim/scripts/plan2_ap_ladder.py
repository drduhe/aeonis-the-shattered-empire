"""Matched M4 Plan 2 ladder: baseline -> AP cap -> cap plus Rally."""
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
    bookkeeping_metrics,
    combat_metrics,
    played_rounds,
    win_rate_by_persona,
)
from aeonis_sim.runner.tournament import run_tournament  # noqa: E402

COUNTS = (4, 6, 8)
VARIANTS = {
    "baseline": {},
    "cap": {"ap_economy": {"ap_bonus_cap": 2, "rally": False}},
    "cap_rally": {"ap_economy": {"ap_bonus_cap": 2, "rally": True}},
}


def _winner(record: dict) -> int:
    players = record["final_state"]["players"]
    return max(
        players,
        key=lambda p: (p["vp"], p["renown"], p["influence"], -p["pid"]),
    )["pid"]


def summarize(records: list[dict]) -> dict:
    done = _completed(records)
    apm = ap_economy_metrics(records)
    bkm = bookkeeping_metrics(records)
    cm = combat_metrics(records)
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
        "ap": {key: round(value, 4) for key, value in apm.items()},
        "bookkeeping": {key: round(value, 4) for key, value in bkm.items()},
        "combat": {
            "contested_attacker_win_rate": round(
                cm.get("contested_attacker_win_rate", 0.0), 4
            ),
            "battles_per_player_round": round(
                cm.get("battles_per_player_round", 0.0), 4
            ),
        },
        "persona_win_rates": {
            name: round(row["win_rate"], 4)
            for name, row in win_rate_by_persona(records).items()
        },
    }


def main() -> None:
    workers = min(8, os.cpu_count() or 1)
    output: dict[str, dict] = {}
    for players in COUNTS:
        base = json.loads(
            (ROOT / "configs" / f"bracket-plan2-bookkeeping-{players}p.json").read_text(
                encoding="utf-8"
            )
        )
        output[str(players)] = {}
        for name, overlay in VARIANTS.items():
            config = copy.deepcopy(base)
            config["name"] = f"{base['name']}-{name}"
            config.update(copy.deepcopy(overlay))
            print(f"RUN {players}p {name}", flush=True)
            summary = summarize(run_tournament(config, workers=workers))
            output[str(players)][name] = summary
            print(json.dumps(summary, sort_keys=True), flush=True)
    dest = ROOT / "tmp-plan2-ap-ladder.json"
    dest.write_text(json.dumps(output, indent=2, sort_keys=True), encoding="utf-8")
    print(f"WROTE {dest}", flush=True)


if __name__ == "__main__":
    main()
