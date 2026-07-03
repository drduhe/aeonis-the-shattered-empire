"""Run a tournament config and enforce regression gates (CI + local).

Usage (from sim/):
    python scripts/regression_check.py --config configs/regression-plan1-baseline.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aeonis_sim.reports.regression import (  # noqa: E402
    evaluate_regression,
    regression_markdown,
)
from aeonis_sim.runner.tournament import run_tournament  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Tournament regression gate checker")
    ap.add_argument("--config", required=True, help="Tournament JSON with regression.gates")
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--report", default=None, help="Optional markdown report path")
    args = ap.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    config = json.loads(config_path.read_text())
    gates = config.get("regression", {}).get("gates", [])
    if not gates:
        print(f"no regression.gates in {config_path}", file=sys.stderr)
        return 2

    workers = args.workers if args.workers is not None else min(4, os.cpu_count() or 1)
    records = run_tournament(config, workers=workers)
    failures = evaluate_regression(records, gates)

    verdicts = {}
    for r in records:
        verdicts[r["verdict"]] = verdicts.get(r["verdict"], 0) + 1
    print(
        f"regression={config.get('name', 'unnamed')} games={len(records)} "
        f"workers={workers} verdicts={verdicts} failures={len(failures)}"
    )

    body = regression_markdown(records, gates, failures)
    print(body)

    if args.report:
        Path(args.report).write_text(body, encoding="utf-8")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
