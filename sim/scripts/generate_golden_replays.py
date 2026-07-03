"""Regenerate golden replay fixtures after engine changes.

Usage (from sim/):
    python scripts/generate_golden_replays.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aeonis_sim.engine.record import replay  # noqa: E402
from aeonis_sim.runner.play import play_game  # noqa: E402

OUT = ROOT / "tests" / "fixtures" / "golden_replays.jsonl"

# (players, seed, persona for all seats)
CASES = [
    (3, 1001, "balanced"),
    (4, 2001, "balanced"),
    (4, 2002, "warmonger"),
    (4, 2003, "economist"),
    (5, 3001, "balanced"),
    (6, 4001, "balanced"),
    (7, 5001, "balanced"),
    (8, 6001, "balanced"),
]


def main() -> None:
    records = []
    for players, seed, persona in CASES:
        config = {"players": players, "personas": [persona] * players}
        rec = play_game(config, seed)
        if rec["verdict"] != "completed":
            raise SystemExit(
                f"seed={seed} players={players} persona={persona} "
                f"verdict={rec['verdict']} — pick another seed"
            )
        g = replay(rec)
        if g.state.to_dict() != rec["final_state"]:
            raise SystemExit(f"replay mismatch seed={seed}")
        records.append(rec)
        print(f"ok players={players} seed={seed} persona={persona} rounds={rec['rounds']}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, sort_keys=True) + "\n")
    print(f"wrote {len(records)} records -> {OUT}")


if __name__ == "__main__":
    main()
