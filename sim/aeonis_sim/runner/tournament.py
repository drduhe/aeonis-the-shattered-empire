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
from ..engine.lords import LAUNCH_LORDS


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

    if mode == "mixed":
        # Shuffle seats; each roster persona appears at least once when possible.
        rng = random.Random(config.get("seed_base", 1) + game_index)
        base = list(roster)
        rng.shuffle(base)
        seats = base[: min(players, len(base))]
        while len(seats) < players:
            seats.append(rng.choice(roster))
        rng.shuffle(seats)
        return seats

    if isinstance(roster, list) and len(roster) == players:
        return roster

    raise ValueError(f"unknown matchmaking mode: {mode}")


def _assign_lords(config: dict, game_index: int) -> list[str] | None:
    """Rotate the launch roster so every Lord sees every seat across a bracket."""
    block = config.get("lord_asymmetry", {})
    if not block.get("enabled", False):
        return None
    players = int(config["players"])
    roster = list(block.get("roster") or LAUNCH_LORDS)
    if len(roster) < players:
        raise ValueError("lord_asymmetry.roster is smaller than player count")
    shift = game_index % len(roster)
    return [roster[(shift + seat) % len(roster)] for seat in range(players)]


def _play_tournament_game(config: dict, game_index: int) -> dict:
    """Run one tournament game (picklable worker entry point)."""
    seed_base = config.get("seed_base", 1)
    game_config = {"players": config["players"]}
    if "combat" in config:
        game_config["combat"] = dict(config["combat"])
    if "ap_economy" in config:
        game_config["ap_economy"] = dict(config["ap_economy"])
    if "pacing" in config:
        game_config["pacing"] = dict(config["pacing"])
    if "objectives" in config:
        game_config["objectives"] = dict(config["objectives"])
    if "seat_rewards" in config:
        game_config["seat_rewards"] = dict(config["seat_rewards"])
    if "economy" in config:
        game_config["economy"] = dict(config["economy"])
    assigned_lords = _assign_lords(config, game_index)
    if assigned_lords is not None:
        game_config["lord_asymmetry"] = {
            "enabled": True,
            "lords": assigned_lords,
        }
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
        Path(args.report).write_text(body, encoding="utf-8")
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
        Path(args.html).write_text(html, encoding="utf-8")
        print(f"html -> {args.html}")

    if args.session_log:
        n = append_session_log(records, args.session_log)
        print(f"session_log rows appended: {n}")


if __name__ == "__main__":
    main()
