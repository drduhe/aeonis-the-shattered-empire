from __future__ import annotations

import argparse
import json

from ..agents.chaos import ChaosBot
from ..engine.game import Game
from ..engine.invariants import InvariantViolation
from ..engine.record import build_record, save_record

AGENTS = {"chaos": ChaosBot}


def make_agent(name: str, seed: int):
    return AGENTS[name](seed)


def play_game(config: dict, seed: int, agent_names: list) -> dict:
    game = Game(config, seed)
    agents = {pid: make_agent(name, seed * 1000 + pid)
              for pid, name in enumerate(agent_names)}
    try:
        while not game.over:
            dp = game.next_decision()
            if dp is None:
                continue
            from ..engine.observations import observe
            obs = observe(game.state, dp.pid)
            choice = agents[dp.pid].choose(obs, dp)
            game.submit(choice)
    except InvariantViolation as e:
        game.over = True
        game.verdict = "crashed"
        rec = build_record(game)
        rec["crash"] = {"type": "InvariantViolation", "message": str(e)}
        return rec
    rec = build_record(game)
    if game.degenerate_flags and rec["verdict"] == "completed":
        rec["verdict"] = "degenerate"
    return rec


def main() -> None:
    ap = argparse.ArgumentParser(description="Run chaos playtest games")
    ap.add_argument("--players", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--games", type=int, default=1)
    ap.add_argument("--out", type=str, default="records/chaos.jsonl")
    args = ap.parse_args()

    tally = {}
    for i in range(args.games):
        seed = args.seed + i
        rec = play_game({"players": args.players}, seed,
                        ["chaos"] * args.players)
        save_record(rec, args.out)
        tally[rec["verdict"]] = tally.get(rec["verdict"], 0) + 1
        print(f"seed={seed} verdict={rec['verdict']} rounds={rec['rounds']} "
              f"vp={rec['final_vp']}")
    print(json.dumps(tally, sort_keys=True))


if __name__ == "__main__":
    main()
