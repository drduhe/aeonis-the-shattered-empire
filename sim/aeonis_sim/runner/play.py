from __future__ import annotations

import argparse
import json

from ..agents.factory import agents_from_config, parse_persona_list
from ..engine.game import Game
from ..engine.observations import observe
from ..engine.record import build_record, save_record
from ..engine.types import VP_THRESHOLD  # re-export for tests; play uses state.vp_threshold
from ..reports.qualitative import save_qualitative_report

# Degeneracy monitor: no player gains VP for this many consecutive rounds.
NO_VP_ROUNDS_FLAG = 8


def _round_summary(game: Game, completed_round: int) -> dict:
    return {
        "completed_round": completed_round,
        "scoreboard": {
            p.pid: {
                "lord": p.lord_id,
                "vp": p.vp,
                "renown": p.renown,
                "gold": p.gold,
                "mana": p.mana,
                "influence": p.influence,
                "controlled_hexes": len(game.state.controlled(p.pid)),
            }
            for p in game.state.players
        },
        "battles_so_far": game.combat_stats.get("battles", 0),
        "motions_proposed_so_far": game.council_stats.get("motions_proposed", 0),
        "motions_passed_so_far": game.council_stats.get("motions_passed", 0),
    }


def _run_round_reflections(agents: dict, summary: dict) -> None:
    for agent in agents.values():
        reflect = getattr(agent, "reflect", None)
        if callable(reflect):
            reflect(summary)


def _attach_qualitative_record(record: dict, agents: dict) -> None:
    qualitative_agents = {
        pid: agent
        for pid, agent in agents.items()
        if callable(getattr(agent, "qualitative_payload", None))
    }
    if not qualitative_agents:
        return
    final_state = record.get("final_state", {})
    final_tiles = list(final_state.get("tiles", {}).values())
    final_players = []
    for player in final_state.get("players", []):
        pid = int(player["pid"])
        final_players.append({
            key: player.get(key)
            for key in ("pid", "lord_id", "gold", "mana", "influence", "renown", "vp", "pop_pool")
        } | {
            "controlled_hexes": sum(1 for tile in final_tiles if tile.get("controller") == pid),
            "buildings": sum(
                len(tile.get("buildings", []))
                for tile in final_tiles
                if tile.get("controller") == pid
            ),
        })
    game_summary = {
        "seed": record["seed"],
        "verdict": record["verdict"],
        "rounds": record["rounds"],
        "final_vp": record["final_vp"],
        "vp_sources": record["vp_sources"],
        "combat_stats": record["combat_stats"],
        "council_stats": record["council_stats"],
        "negotiation_stats": record["negotiation_stats"],
        "ap_economy_stats": record["ap_economy_stats"],
        "building_stats": record["building_stats"],
        "whisper_stats": record["whisper_stats"],
        "final_players": final_players,
        "evidence_limits": {
            "games_observed": 1,
            "battles_observed": record["combat_stats"].get("battles", 0),
            "instruction": "Treat low-count outcomes as observations, not established balance trends.",
        },
    }
    for pid, agent in qualitative_agents.items():
        interview = getattr(agent, "exit_interview", None)
        if callable(interview):
            interview({**game_summary, "viewer": pid})
    record["agent_playtest"] = {
        "sim_only": True,
        "seats": {pid: agent.qualitative_payload() for pid, agent in qualitative_agents.items()},
    }


def play_game(config: dict, seed: int, agents=None) -> dict:
    game = Game(config, seed)
    if agents is None:
        agents = agents_from_config(config, seed)
    last_vp_round, last_vp_total = 1, 0
    observed_round = game.state.round
    latest_round_summary = _round_summary(game, observed_round)
    while not game.over:
        dp = game.next_decision()
        if dp is None:
            continue
        if game.state.round > observed_round:
            # ``next_decision`` advances automatic Cleanup and Round Start work.
            # Reflect against the last snapshot from the completed round so the
            # qualitative record does not accidentally describe refreshed state.
            _run_round_reflections(agents, latest_round_summary)
            observed_round = game.state.round
            latest_round_summary = _round_summary(game, observed_round)
        vp_total = sum(p.vp for p in game.state.players)
        if vp_total > last_vp_total:
            last_vp_total, last_vp_round = vp_total, game.state.round
            if "no_vp_progress" in game.degenerate_flags:
                game.degenerate_flags.remove("no_vp_progress")
        elif (game.state.round - last_vp_round >= NO_VP_ROUNDS_FLAG
              and "no_vp_progress" not in game.degenerate_flags):
            game.degenerate_flags.append("no_vp_progress")
        obs = observe(game.state, dp.pid)
        game.submit(agents[dp.pid].choose(obs, dp))
        latest_round_summary = _round_summary(game, observed_round)
    record = build_record(game)
    if record["verdict"] == "completed" and record["degenerate_flags"]:
        max_vp = max(int(v) for v in record["final_vp"].values())
        if max_vp >= game.state.vp_threshold:
            record["degenerate_flags"] = [
                f
                for f in record["degenerate_flags"]
                if f not in ("no_vp_progress", "action_cap")
            ]
        if record.get("round_cap_finish"):
            record["degenerate_flags"] = [
                f for f in record["degenerate_flags"] if f != "no_vp_progress"
            ]
        if record["degenerate_flags"]:
            record["verdict"] = "degenerate"
    _attach_qualitative_record(record, agents)
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
    ap.add_argument(
        "--aggressors-edge",
        action="store_true",
        help="Plan 1: attacker Attack rolls win ties",
    )
    ap.add_argument(
        "--pillage",
        action="store_true",
        help="Plan 1: one-time printed production on hex capture",
    )
    ap.add_argument(
        "--llm-provider",
        choices=("deterministic", "ollama"),
        default=None,
        help="Enable M5 qualitative seats with this provider",
    )
    ap.add_argument("--llm-model", default=None, help="Provider model name (required for Ollama)")
    ap.add_argument("--llm-seats", default=None, help="Comma-separated qualitative seat numbers; default all")
    ap.add_argument("--llm-max-decisions", type=int, default=8, help="Model decisions per qualitative seat")
    ap.add_argument("--llm-max-reflections", type=int, default=2, help="Round reflections per qualitative seat")
    ap.add_argument("--qualitative-report", default=None, help="Write the M5 Markdown report here")
    args = ap.parse_args()
    counts = {}
    records = []
    for i in range(args.games):
        config: dict = {"players": args.players}
        if args.aggressors_edge or args.pillage:
            config["combat"] = {
                "aggressors_edge": args.aggressors_edge,
                "pillage": args.pillage,
            }
        if args.personas:
            config["personas"] = list(parse_persona_list(args.personas, args.players).values())
        elif args.persona:
            config["personas"] = [args.persona] * args.players
        if args.llm_provider:
            if args.llm_provider == "ollama" and not args.llm_model:
                ap.error("--llm-model is required with --llm-provider ollama")
            seats = (
                [int(x.strip()) for x in args.llm_seats.split(",") if x.strip()]
                if args.llm_seats else list(range(args.players))
            )
            config["llm_playtest"] = {
                "enabled": True,
                "seats": seats,
                "provider": {
                    "type": args.llm_provider,
                    **({"model": args.llm_model} if args.llm_model else {}),
                },
                "max_decision_calls_per_seat": args.llm_max_decisions,
                "max_round_reflections_per_seat": args.llm_max_reflections,
            }
        rec = play_game(config, seed=args.seed + i)
        records.append(rec)
        counts[rec["verdict"]] = counts.get(rec["verdict"], 0) + 1
        if args.out:
            save_record(rec, args.out)
        print(f"seed={args.seed + i} verdict={rec['verdict']} "
              f"rounds={rec['rounds']} vp={rec['final_vp']}")
    print("verdicts:", counts)
    if args.qualitative_report:
        save_qualitative_report(records, args.qualitative_report)
        print(f"qualitative_report={args.qualitative_report}")


if __name__ == "__main__":
    main()
