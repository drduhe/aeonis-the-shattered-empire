"""Tournament batch runner for persona balance campaigns."""
from __future__ import annotations

import argparse
import json
import os
import random
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from ..agents.factory import agents_from_config
from ..reports.hypotheses import evaluate_hypotheses, hypotheses_markdown
from ..reports.html import generate_html
from ..reports.summary import append_session_log, balance_summary
from .play import play_game


def _assign_personas(config: dict, game_index: int) -> list[str]:
    """Per-game seat persona assignment (deterministic from config + index)."""
    players = config["players"]
    roster = config.get("personas", ["balanced"] * players)
    mode = config.get("matchmaking", "rotate")

    if mode == "solo":
        # One persona per game — all seats same (first in roster cycles).
        name = roster[game_index % len(roster)]
        return [name] * players

    if mode == "rotate":
        # Shift roster each game so each persona gets varied seats.
        shift = game_index % players
        return [roster[(i + shift) % len(roster)] for i in range(players)]

    if mode == "random":
        # Advance the RNG stream to match sequential tournament order.
        rng = random.Random(config.get("seed_base", 1))
        for _ in range(game_index * players):
            rng.choice(roster)
        return [rng.choice(roster) for _ in range(players)]

    if isinstance(roster, list) and len(roster) == players:
        return roster

    raise ValueError(f"unknown matchmaking mode: {mode}")


def _play_tournament_game(config: dict, game_index: int) -> dict:
    """Run one tournament game (picklable worker entry point)."""
    seed_base = config.get("seed_base", 1)
    game_config = {"players": config["players"]}
    game_config["personas"] = _assign_personas(config, game_index)
    seed = seed_base + game_index
    agents = agents_from_config(game_config, seed)
    return play_game(game_config, seed, agents=agents)


def run_tournament(
    config: dict,
    out_path: str | None = None,
    workers: int = 1,
) -> list[dict]:
    games = config.get("games", 1)
    if workers <= 1:
        records = [_play_tournament_game(config, i) for i in range(games)]
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            records = list(pool.map(_play_tournament_game, [config] * games, range(games)))
        records.sort(key=lambda r: r["seed"])

    if out_path:
        from ..engine.record import save_record

        Path(out_path).write_text("")
        for rec in records:
            save_record(rec, out_path)
    return records


def main() -> None:
    ap = argparse.ArgumentParser(description="Run persona-bot tournament")
    ap.add_argument("--config", required=True, help="Tournament JSON config")
    ap.add_argument("--out", default=None, help="JSONL output path")
    ap.add_argument("--report", default=None, help="Markdown report path")
    ap.add_argument("--html", default=None, help="HTML report path")
    ap.add_argument("--session-log", default=None, help="Append to session_log.csv")
    ap.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Parallel game workers (default: CPU count)",
    )
    args = ap.parse_args()

    workers = args.workers if args.workers is not None else (os.cpu_count() or 1)
    config = json.loads(Path(args.config).read_text())
    records = run_tournament(config, args.out, workers=workers)
    verdicts = {}
    for r in records:
        verdicts[r["verdict"]] = verdicts.get(r["verdict"], 0) + 1
    print(
        f"tournament={config.get('name', 'unnamed')} games={len(records)} "
        f"workers={workers} verdicts={verdicts}"
    )

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
