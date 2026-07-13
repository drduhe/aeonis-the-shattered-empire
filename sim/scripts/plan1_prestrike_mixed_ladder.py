"""Run Plan 1 Pre-Strike Edge mixed ladder (baseline vs pre_strike at 4/6/8p)."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aeonis_sim.reports.summary import combat_metrics  # noqa: E402
from aeonis_sim.runner.tournament import run_tournament  # noqa: E402

CONFIGS = [
    "configs/bracket-plan1-baseline-mixed-4p.json",
    "configs/bracket-plan1-prestrike-mixed-4p.json",
    "configs/bracket-plan1-baseline-mixed-6p.json",
    "configs/bracket-plan1-prestrike-mixed-6p.json",
    "configs/bracket-plan1-baseline-mixed-8p.json",
    "configs/bracket-plan1-prestrike-mixed-8p.json",
]


def _mean_rounds(recs: list) -> float:
    rounds = [r.get("rounds", 0) for r in recs if r.get("verdict") == "completed"]
    return sum(rounds) / len(rounds) if rounds else 0.0


def main() -> None:
    workers = min(4, os.cpu_count() or 1)
    out = []
    for rel in CONFIGS:
        cfg = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        recs = run_tournament(cfg, workers=workers)
        cm = combat_metrics(recs)
        row = {
            "name": cfg["name"],
            "players": cfg["players"],
            "games": len(recs),
            "edge": cfg.get("combat", {}).get("aggressors_edge_mode", "off"),
            "attacker_win_rate": round(cm.get("attacker_win_rate", 0.0), 4),
            "contested_attacker_win_rate": round(
                cm.get("contested_attacker_win_rate", 0.0), 4
            ),
            "battles_per_player_round": round(
                cm.get("battles_per_player_round", 0.0), 4
            ),
            "mean_rounds": round(_mean_rounds(recs), 3),
        }
        out.append(row)
        print(json.dumps(row), flush=True)
    dest = ROOT / "tmp-plan1-prestrike-ladder.json"
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {dest}", flush=True)


if __name__ == "__main__":
    main()
