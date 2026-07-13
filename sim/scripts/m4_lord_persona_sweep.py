"""M4 Lord × persona sweep: solo 4p + mixed 4p/6p.

Usage (from sim/):
    python scripts/m4_lord_persona_sweep.py
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aeonis_sim.reports.summary import (  # noqa: E402
    _completed,
    _lord_of,
    _persona_of,
    _winner,
    combat_metrics,
    win_rate_by_lord,
    win_rate_by_persona,
    winner_vp_source_mix,
)
from aeonis_sim.runner.tournament import run_tournament  # noqa: E402

PERSONAS = ["warmonger", "economist", "expander", "diplomat", "balanced"]
WATCH = ["rakhis", "thalrik", "vharok", "cassian"]
CONFIGS = [
    "bracket-m4-lord-persona-solo-4p",
    "bracket-m4-lord-persona-mixed-4p",
    "bracket-m4-lord-persona-mixed-6p",
]


def solo_persona(r: dict) -> str:
    personas = r.get("config", {}).get("personas", [])
    if isinstance(personas, list) and personas:
        return personas[0]
    return "unknown"


def lord_rates_for(recs: list[dict]) -> dict:
    return {
        lord: {
            "games": s["games"],
            "wins": s["wins"],
            "win_rate": round(s["win_rate"], 4),
        }
        for lord, s in win_rate_by_lord(recs).items()
    }


def winner_crosstab(recs: list[dict]) -> dict:
    wins: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    seats: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in _completed(recs):
        for raw_pid in r["final_vp"]:
            pid = int(raw_pid)
            lord = _lord_of(r, pid)
            persona = _persona_of(r, pid)
            if lord:
                seats[persona][lord] += 1
        w = _winner(r)
        if w is None:
            continue
        wins[_persona_of(r, w)][_lord_of(r, w)] += 1
    rates: dict = {}
    for persona in sorted(set(list(wins) + list(seats))):
        rates[persona] = {}
        for lord in sorted(set(list(wins[persona]) + list(seats[persona]))):
            g = seats[persona].get(lord, 0)
            wi = wins[persona].get(lord, 0)
            rates[persona][lord] = {
                "wins": wi,
                "seat_games": g,
                "win_rate": round(wi / g, 4) if g else None,
            }
    return rates


def main() -> None:
    out: dict = {}
    for name in CONFIGS:
        cfg = json.loads(Path(f"configs/{name}.json").read_text(encoding="utf-8"))
        print(f"RUN {name} games={cfg['games']} ...", flush=True)
        recs = run_tournament(cfg, workers=4)
        completed = _completed(recs)
        rounds = [r["rounds"] for r in completed]
        block: dict = {
            "n": len(recs),
            "completed": len(completed),
            "mean_rounds": round(mean(rounds), 2) if rounds else None,
            "lords": lord_rates_for(recs),
            "personas": {
                k: {
                    "games": v["games"],
                    "wins": v["wins"],
                    "win_rate": round(v["win_rate"], 4),
                }
                for k, v in win_rate_by_persona(recs).items()
            },
            "winner_crosstab": winner_crosstab(recs),
            "combat": {
                k: (round(v, 4) if isinstance(v, float) else v)
                for k, v in combat_metrics(recs).items()
            },
            "winner_vp_mix": {
                k: round(v, 4) for k, v in winner_vp_source_mix(recs).items()
            },
        }
        if cfg.get("matchmaking") == "solo":
            by_persona = {}
            for p in PERSONAS:
                subset = [r for r in completed if solo_persona(r) == p]
                by_persona[p] = {"games": len(subset), "lords": lord_rates_for(subset)}
            block["solo_lords_by_persona"] = by_persona
        out[name] = block
        print(
            f"  done completed={len(completed)} mean_rounds={block['mean_rounds']}",
            flush=True,
        )

    Path("tmp-m4-lord-persona.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("WROTE tmp-m4-lord-persona.json", flush=True)
    print("\n=== WATCH SUMMARY ===", flush=True)
    for name, block in out.items():
        print(f"\n{name}", flush=True)
        for lord in WATCH:
            s = block["lords"].get(lord, {})
            rate = 100 * s.get("win_rate", 0)
            print(
                f"  {lord}: {rate:.1f}% ({s.get('wins', 0)}/{s.get('games', 0)})",
                flush=True,
            )


if __name__ == "__main__":
    main()
