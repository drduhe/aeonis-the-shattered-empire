"""Attribute the canonical 8p economist floor to row, Lord, and VP paths."""
from __future__ import annotations

import copy
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aeonis_sim.reports.summary import (  # noqa: E402
    _completed,
    _winner,
    played_rounds,
    win_rate_by_lord,
    win_rate_by_persona,
)
from aeonis_sim.runner.tournament import run_tournament  # noqa: E402

VARIANTS = {
    "full_deck": {
        "objectives": {
            "full_public_deck": True,
            "exclude_public_ids": ["archmage"],
        },
    },
    "first_playable_row": {},
}


def _mean(total: float, count: int) -> float:
    return round(total / count, 4) if count else 0.0


def summarize(records: list[dict]) -> dict:
    done = _completed(records)
    persona_rows: dict[str, dict] = defaultdict(
        lambda: {
            "seats": 0,
            "wins": 0,
            "vp": 0,
            "objective_vp": 0,
            "gold": 0,
            "mana": 0,
            "influence": 0,
            "buildings": 0,
            "controlled": 0,
            "public_scores": Counter(),
            "secret_scores": Counter(),
        }
    )
    economist_lords: dict[str, dict] = defaultdict(
        lambda: {"seats": 0, "wins": 0, "vp": 0, "objective_vp": 0}
    )
    revealed = Counter()
    for record in done:
        winner = _winner(record)
        final = record["final_state"]
        revealed.update(final.get("shared_public_revealed", []))
        tiles = list(final["tiles"].values())
        personas = record["config"]["personas"]
        lords = record["config"].get("lord_asymmetry", {}).get("lords", [])
        for player in final["players"]:
            pid = int(player["pid"])
            persona = personas[pid]
            row = persona_rows[persona]
            row["seats"] += 1
            row["wins"] += int(winner == pid)
            row["vp"] += int(player["vp"])
            row["objective_vp"] += int(player.get("vp_sources", {}).get("objective", 0))
            row["gold"] += int(player["gold"])
            row["mana"] += int(player["mana"])
            row["influence"] += int(player["influence"])
            controlled = [tile for tile in tiles if tile.get("controller") == pid]
            row["controlled"] += len(controlled)
            row["buildings"] += sum(len(tile.get("buildings", [])) for tile in controlled)
            row["public_scores"].update(player.get("shared_scored", []))
            row["secret_scores"].update(player.get("secrets_scored", []))
            if persona == "economist":
                lord = lords[pid] if pid < len(lords) else "unknown"
                lord_row = economist_lords[lord]
                lord_row["seats"] += 1
                lord_row["wins"] += int(winner == pid)
                lord_row["vp"] += int(player["vp"])
                lord_row["objective_vp"] += int(
                    player.get("vp_sources", {}).get("objective", 0)
                )
    personas_out = {}
    for persona, row in sorted(persona_rows.items()):
        seats = row["seats"]
        personas_out[persona] = {
            "seats": seats,
            "wins": row["wins"],
            "win_rate": _mean(row["wins"], seats),
            "avg_vp": _mean(row["vp"], seats),
            "avg_objective_vp": _mean(row["objective_vp"], seats),
            "avg_gold": _mean(row["gold"], seats),
            "avg_mana": _mean(row["mana"], seats),
            "avg_influence": _mean(row["influence"], seats),
            "avg_buildings": _mean(row["buildings"], seats),
            "avg_controlled": _mean(row["controlled"], seats),
            "public_scores": dict(row["public_scores"].most_common()),
            "secret_scores": dict(row["secret_scores"].most_common()),
        }
    lord_out = {}
    for lord, row in sorted(economist_lords.items()):
        seats = row["seats"]
        lord_out[lord] = {
            "seats": seats,
            "wins": row["wins"],
            "win_rate": _mean(row["wins"], seats),
            "avg_vp": _mean(row["vp"], seats),
            "avg_objective_vp": _mean(row["objective_vp"], seats),
        }
    return {
        "games": len(records),
        "completed": len(done),
        "mean_rounds": _mean(sum(played_rounds(r) for r in done), len(done)),
        "revealed_games": dict(revealed.most_common()),
        "personas": personas_out,
        "economist_by_lord": lord_out,
    }


def summarize_guard(records: list[dict]) -> dict:
    done = _completed(records)
    return {
        "games": len(records),
        "completed": len(done),
        "mean_rounds": _mean(sum(played_rounds(r) for r in done), len(done)),
        "persona_win_rates": {
            persona: round(row["win_rate"], 4)
            for persona, row in win_rate_by_persona(records).items()
        },
        "lord_win_rates": {
            lord: round(row["win_rate"], 4)
            for lord, row in win_rate_by_lord(records).items()
        },
    }


def main() -> None:
    base = json.loads(
        (ROOT / "configs" / "bracket-economist-diagnosis-8p.json").read_text(
            encoding="utf-8"
        )
    )
    workers = min(8, os.cpu_count() or 1)
    output = {}
    for name, overlay in VARIANTS.items():
        config = copy.deepcopy(base)
        config["name"] = f"{base['name']}-{name}"
        config.update(copy.deepcopy(overlay))
        print(f"RUN 8p {name}", flush=True)
        result = summarize(run_tournament(config, workers=workers))
        output[name] = result
        print(json.dumps(result, sort_keys=True), flush=True)
    guard = json.loads(
        (ROOT / "configs" / "bracket-m4-default-review-4p.json").read_text(
            encoding="utf-8"
        )
    )
    print("RUN 4p Auriel/warmonger regression guard", flush=True)
    output["guard_4p"] = summarize_guard(
        run_tournament(guard, workers=workers)
    )
    print(json.dumps(output["guard_4p"], sort_keys=True), flush=True)
    dest = ROOT / "tmp-economist-8p-diagnosis.json"
    dest.write_text(json.dumps(output, indent=2, sort_keys=True), encoding="utf-8")
    print(f"WROTE {dest}", flush=True)


if __name__ == "__main__":
    main()
