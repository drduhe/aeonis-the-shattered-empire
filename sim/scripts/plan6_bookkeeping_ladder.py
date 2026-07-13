"""Matched M4 Plan 6 ladder: slim Renown and no-building-upkeep packages."""
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
    council_metrics,
    played_rounds,
    win_rate_by_persona,
)
from aeonis_sim.runner.tournament import run_tournament  # noqa: E402

COUNTS = (4, 6, 8)
VARIANTS = {
    "baseline": {},
    "slim_renown": {
        "bookkeeping": {"slim_renown": True, "building_upkeep": True},
    },
    "no_upkeep": {
        "bookkeeping": {"slim_renown": False, "building_upkeep": False},
    },
    "combined": {
        "bookkeeping": {"slim_renown": True, "building_upkeep": False},
    },
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
    council = council_metrics(records)
    objective_shares = []
    final_players = []
    building_mix: Counter = Counter()
    for record in done:
        final_players.extend(record["final_state"]["players"])
        building_mix.update(
            choice["building"]
            for choice in record.get("choices", [])
            if choice.get("type") == "build" and choice.get("building")
        )
        winner = _winner(record)
        vp = int(record["final_vp"].get(str(winner), record["final_vp"].get(winner, 0)))
        sources = record["vp_sources"].get(
            str(winner), record["vp_sources"].get(winner, {})
        )
        objective_shares.append(int(sources.get("objective", 0)) / max(vp, 1))
    seats = len(final_players) or 1
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
        "council": {
            "pass_rate": round(council.get("pass_rate", 0.0), 4),
            "influence_spent": council.get("influence_spent", 0),
        },
        "renown": {
            "mean_final": round(sum(p["renown"] for p in final_players) / seats, 4),
            "reached_5_share": round(sum(p["renown"] >= 5 for p in final_players) / seats, 4),
            "reached_10_share": round(sum(p["renown"] >= 10 for p in final_players) / seats, 4),
            "reward_5_share": round(sum(p.get("renown_reward_5", False) for p in final_players) / seats, 4),
            "reward_10_share": round(sum(p.get("renown_reward_10", False) for p in final_players) / seats, 4),
        },
        "final_resources": {
            "gold_per_seat": round(sum(p["gold"] for p in final_players) / seats, 4),
            "mana_per_seat": round(sum(p["mana"] for p in final_players) / seats, 4),
            "influence_per_seat": round(sum(p["influence"] for p in final_players) / seats, 4),
        },
        "building_mix_per_game": {
            name: round(count / len(done), 4)
            for name, count in sorted(building_mix.items())
        } if done else {},
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
    dest = ROOT / "tmp-plan6-bookkeeping-ladder.json"
    dest.write_text(json.dumps(output, indent=2, sort_keys=True), encoding="utf-8")
    print(f"WROTE {dest}", flush=True)


if __name__ == "__main__":
    main()
