"""Matched M4 ladder: reduced First Playable row vs audited public deck."""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aeonis_sim.runner.tournament import run_tournament  # noqa: E402


COUNTS = (4, 6, 8)


def _winner(record: dict) -> int:
    players = record["final_state"]["players"]
    return max(
        players,
        key=lambda p: (p["vp"], p["renown"], p["influence"], -p["pid"]),
    )["pid"]


def _summarize(records: list[dict]) -> dict:
    verdicts = Counter(r["verdict"] for r in records)
    scored = Counter()
    revealed = Counter()
    persona_games = Counter()
    persona_wins = Counter()
    winner_objective_shares = []
    for rec in records:
        for oid in rec["final_state"]["shared_public_revealed"]:
            revealed[oid] += 1
        for p in rec["final_state"]["players"]:
            scored.update(p.get("shared_scored", []))
        winner = _winner(rec)
        personas = rec["config"].get("personas", [])
        for persona in personas:
            persona_games[persona] += 1
        if winner < len(personas):
            persona_wins[personas[winner]] += 1
        vp = int(rec["final_vp"][str(winner)] if str(winner) in rec["final_vp"] else rec["final_vp"][winner])
        objective_vp = int(
            rec["vp_sources"].get(str(winner), rec["vp_sources"].get(winner, {})).get("objective", 0)
        )
        winner_objective_shares.append(objective_vp / max(vp, 1))
    objective_rows = {}
    for oid in sorted(revealed):
        objective_rows[oid] = {
            "revealed_games": revealed[oid],
            "scores": scored[oid],
        }
    return {
        "games": len(records),
        "verdicts": dict(verdicts),
        "mean_rounds": round(sum(r["rounds"] - 1 for r in records) / len(records), 3),
        "winner_objective_share": round(
            sum(winner_objective_shares) / len(winner_objective_shares), 4
        ),
        "objective_rows": objective_rows,
        "persona_win_rates": {
            name: round(persona_wins[name] / games, 4)
            for name, games in sorted(persona_games.items())
        },
    }


def main() -> None:
    workers = min(8, os.cpu_count() or 1)
    out: dict[str, dict] = defaultdict(dict)
    for players in COUNTS:
        path = ROOT / "configs" / f"bracket-plan3-objectives-{players}p.json"
        audited = json.loads(path.read_text(encoding="utf-8"))
        baseline = dict(audited)
        baseline["name"] = audited["name"].replace("audited-objectives", "reduced-row-baseline")
        baseline.pop("objectives", None)
        print(f"RUN {players}p baseline", flush=True)
        out[str(players)]["baseline"] = _summarize(
            run_tournament(baseline, workers=workers)
        )
        print(f"RUN {players}p audited", flush=True)
        out[str(players)]["audited"] = _summarize(
            run_tournament(audited, workers=workers)
        )
    dest = ROOT / "tmp-plan3-objective-audit.json"
    dest.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(f"WROTE {dest}", flush=True)


if __name__ == "__main__":
    main()
