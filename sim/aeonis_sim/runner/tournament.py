"""Tournament batch runner for persona balance campaigns."""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from ..agents.factory import agents_from_config
from ..reports.hypotheses import evaluate_hypotheses, hypotheses_markdown
from ..reports.html import generate_html
from ..reports.summary import append_session_log, balance_summary, load_records
from .play import play_game


def _assign_personas(config: dict, game_index: int, rng: random.Random) -> dict:
    """Per-game seat persona assignment."""
    players = config["players"]
    roster = config.get("personas", ["balanced"] * players)
    mode = config.get("matchmaking", "rotate")

    if mode == "solo":
        # One persona per game — all seats same (first in roster cycles).
        name = roster[game_index % len(roster)]
        return list([name] * players)

    if mode == "rotate":
        # Shift roster each game so each persona gets varied seats.
        shift = game_index % players
        ordered = [roster[(i + shift) % len(roster)] for i in range(players)]
        return ordered

    if mode == "random":
        return [rng.choice(roster) for _ in range(players)]

    if isinstance(roster, list) and len(roster) == players:
        return roster

    raise ValueError(f"unknown matchmaking mode: {mode}")


def run_tournament(config: dict, out_path: str | None = None) -> list[dict]:
    games = config.get("games", 1)
    seed_base = config.get("seed_base", 1)
    rng = random.Random(seed_base)
    records = []
    for i in range(games):
        game_config = {"players": config["players"]}
        game_config["personas"] = _assign_personas(config, i, rng)
        seed = seed_base + i
        agents = agents_from_config(game_config, seed)
        rec = play_game(game_config, seed, agents=agents)
        records.append(rec)
        if out_path:
            from ..engine.record import save_record
            save_record(rec, out_path)
    return records


def main() -> None:
    ap = argparse.ArgumentParser(description="Run persona-bot tournament")
    ap.add_argument("--config", required=True, help="Tournament JSON config")
    ap.add_argument("--out", default=None, help="JSONL output path")
    ap.add_argument("--report", default=None, help="Markdown report path")
    ap.add_argument("--html", default=None, help="HTML report path")
    ap.add_argument("--session-log", default=None, help="Append to session_log.csv")
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text())
    if args.out:
        Path(args.out).write_text("")
    records = run_tournament(config, args.out)
    verdicts = {}
    for r in records:
        verdicts[r["verdict"]] = verdicts.get(r["verdict"], 0) + 1
    print(f"tournament={config.get('name', 'unnamed')} games={len(records)} verdicts={verdicts}")

    if args.report:
        title = config.get("name", "Tournament")
        body = balance_summary(records, title=title)
        body += "\n" + hypotheses_markdown(evaluate_hypotheses(records))
        Path(args.report).write_text(body)
        print(f"report -> {args.report}")

    if args.html:
        subtitle = (
            f"{config.get('players', '?')} players · "
            f"{len(records):,} games · seeds {config.get('seed_base', '?')}+ · "
            f"July 2, 2026"
        )
        html = generate_html(
            records,
            title=config.get("name", "Persona Tournament"),
            subtitle=subtitle,
        )
        Path(args.html).write_text(html)
        print(f"html -> {args.html}")

    if args.session_log:
        n = append_session_log(records, args.session_log)
        print(f"session_log rows appended: {n}")


if __name__ == "__main__":
    main()
