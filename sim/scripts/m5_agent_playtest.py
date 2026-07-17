"""Run a reproducible M5 qualitative-agent playtest campaign."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aeonis_sim.engine.record import save_record  # noqa: E402
from aeonis_sim.reports.qualitative import save_qualitative_report  # noqa: E402
from aeonis_sim.runner.play import play_game  # noqa: E402


def _rotate(values: list, shift: int) -> list:
    if not values:
        return []
    shift %= len(values)
    return values[shift:] + values[:shift]


def game_config_for_offset(campaign: dict, offset: int, rotation: dict) -> dict:
    """Return an isolated game config with optional seat assignment rotation."""
    game_config = copy.deepcopy(campaign)
    step = int(rotation.get("step", 1))
    shift = offset * step
    if rotation.get("lords", False):
        lord_block = dict(game_config.get("lord_asymmetry", {}))
        lords = list(lord_block.get("lords", []))
        if lords:
            lord_block["lords"] = _rotate(lords, shift)
            game_config["lord_asymmetry"] = lord_block
    if rotation.get("personas", False):
        personas = list(game_config.get("personas", []))
        if personas:
            game_config["personas"] = _rotate(personas, shift)
    return game_config


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--out", required=True, help="JSONL records (replaced atomically per campaign)")
    parser.add_argument("--report", required=True, help="Markdown qualitative report")
    args = parser.parse_args()

    source = Path(args.config)
    if not source.is_absolute():
        source = ROOT / source
    campaign = json.loads(source.read_text(encoding="utf-8"))
    games = int(campaign.pop("games", 1))
    seed_base = int(campaign.pop("seed_base", 1))
    title = str(campaign.pop("report_title", "Aeonis M5 Agent Playtest Report"))
    rotation = dict(campaign.pop("assignment_rotation", {}))

    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.unlink(missing_ok=True)

    records = []
    verdicts: dict[str, int] = {}
    for offset in range(games):
        seed = seed_base + offset
        game_config = game_config_for_offset(campaign, offset, rotation)
        record = play_game(game_config, seed=seed)
        records.append(record)
        verdicts[record["verdict"]] = verdicts.get(record["verdict"], 0) + 1
        save_record(record, temporary)
        print(
            f"seed={seed} verdict={record['verdict']} rounds={record['rounds']} "
            f"vp={record['final_vp']}"
        )

    temporary.replace(output)
    save_qualitative_report(records, args.report, title=title)
    print(f"verdicts={verdicts}")
    print(f"records={output}")
    print(f"report={args.report}")


if __name__ == "__main__":
    main()
