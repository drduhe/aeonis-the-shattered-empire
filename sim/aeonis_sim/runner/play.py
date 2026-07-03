from __future__ import annotations

import argparse
import json

from ..agents.factory import agents_from_config, parse_persona_list
from ..engine.game import Game
from ..engine.observations import observe
from ..engine.record import build_record, save_record

# Degeneracy monitor: no player gains VP for this many consecutive rounds.
NO_VP_ROUNDS_FLAG = 8


def play_game(config: dict, seed: int, agents=None) -> dict:
    game = Game(config, seed)
    if agents is None:
        agents = agents_from_config(config, seed)
    last_vp_round, last_vp_total = 1, 0
    while not game.over:
        dp = game.next_decision()
        if dp is None:
            continue
        vp_total = sum(p.vp for p in game.state.players)
        if vp_total > last_vp_total:
            last_vp_total, last_vp_round = vp_total, game.state.round
        elif (game.state.round - last_vp_round >= NO_VP_ROUNDS_FLAG
              and "no_vp_progress" not in game.degenerate_flags):
            game.degenerate_flags.append("no_vp_progress")
        obs = observe(game.state, dp.pid)
        game.submit(agents[dp.pid].choose(obs, dp))
    record = build_record(game)
    if record["verdict"] == "completed" and record["degenerate_flags"]:
        record["verdict"] = "degenerate"
    return record


def main() -> None:
    ap = argparse.ArgumentParser(description="Run Aeonis bot games")
    ap.add_argument("--players", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--games", type=int, default=1)
    ap.add_argument("--out", default=None, help="JSONL path to append records")
    ap.add_argument(
        "--persona",
        default=None,
        help="Persona for all seats (warmonger|economist|expander|diplomat|balanced|chaos)",
    )
    ap.add_argument(
        "--personas",
        default=None,
        help="Comma-separated persona per seat (overrides --persona)",
    )
    args = ap.parse_args()
    counts = {}
    for i in range(args.games):
        config: dict = {"players": args.players}
        if args.personas:
            config["personas"] = list(parse_persona_list(args.personas, args.players).values())
        elif args.persona:
            config["personas"] = [args.persona] * args.players
        rec = play_game(config, seed=args.seed + i)
        counts[rec["verdict"]] = counts.get(rec["verdict"], 0) + 1
        if args.out:
            save_record(rec, args.out)
        print(f"seed={args.seed + i} verdict={rec['verdict']} "
              f"rounds={rec['rounds']} vp={rec['final_vp']}")
    print("verdicts:", counts)


if __name__ == "__main__":
    main()
