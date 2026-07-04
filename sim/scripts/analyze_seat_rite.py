"""Analyze Imperial Seat / Coronation Rite VP by persona from tournament JSONL."""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path


def seat_holder(final_state: dict) -> int | None:
    for td in final_state["tiles"].values():
        if td.get("imperial_seat"):
            c = td.get("controller")
            return int(c) if c is not None else None
    return None


def pid_persona(rec: dict) -> dict[int, str]:
    personas = rec["config"]["personas"]
    return {i: personas[i] for i in range(len(personas))}


def analyze(path: Path) -> None:
    records = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    completed = [r for r in records if r["verdict"] == "completed"]

    stats = defaultdict(
        lambda: {
            "seat_games": 0,
            "wins": 0,
            "rite_vp": 0.0,
            "milestone_vp": 0.0,
            "seat_obj_scored": 0,
            "held_seat_end": 0,
            "rite_count_sum": 0,
            "total_vp": 0.0,
            "won_with_seat_end": 0,
            "milestone_games": 0,
        }
    )
    end_seat = defaultdict(int)

    for rec in completed:
        pmap = pid_persona(rec)
        fs = rec["final_state"]
        winner = max(rec["final_vp"], key=lambda k: rec["final_vp"][k])
        seat_pid = seat_holder(fs)

        if seat_pid is not None:
            end_seat[pmap[seat_pid]] += 1

        for p in fs["players"]:
            pid = p["pid"]
            persona = pmap[pid]
            s = stats[persona]
            s["seat_games"] += 1
            vp_src = rec["vp_sources"][str(pid)]
            rite = vp_src.get("coronation_rite", 0)
            mile = vp_src.get("coronation_milestone", 0)
            s["rite_vp"] += rite
            s["milestone_vp"] += mile
            s["total_vp"] += rec["final_vp"][str(pid)]
            s["rite_count_sum"] += p.get("rite_count", 0)
            if mile > 0:
                s["milestone_games"] += 1
            if "seat_of_empire" in p.get("shared_scored", []):
                s["seat_obj_scored"] += 1
            if seat_pid is not None and seat_pid == pid:
                s["held_seat_end"] += 1
            if str(pid) == winner:
                s["wins"] += 1
                if seat_pid is not None and seat_pid == pid:
                    s["won_with_seat_end"] += 1

    personas = ["expander", "balanced", "warmonger", "diplomat", "economist"]
    print(f"=== Seat / rite analysis ({len(completed)} completed games) ===")
    print(f"{'persona':12} {'games':>6} {'win%':>6} {'rite/g':>7} {'mile/g':>7} "
          f"{'seatObj%':>9} {'endSeat%':>9} {'avgRites':>9} {'seatVP%':>8}")
    for persona in personas:
        s = stats[persona]
        g = s["seat_games"] or 1
        seat_vp = s["rite_vp"] + s["milestone_vp"] + s["seat_obj_scored"] * 2
        total = s["total_vp"] or 1
        print(
            f"{persona:12} {g:6d} {100 * s['wins'] / g:5.1f}% "
            f"{s['rite_vp'] / g:7.2f} {s['milestone_vp'] / g:7.2f} "
            f"{100 * s['seat_obj_scored'] / g:8.1f}% "
            f"{100 * s['held_seat_end'] / g:8.1f}% "
            f"{s['rite_count_sum'] / g:9.2f} "
            f"{100 * seat_vp / total:7.1f}%"
        )

    print("\n=== End-game seat holder ===")
    for p, c in sorted(end_seat.items(), key=lambda x: -x[1]):
        print(f"  {p}: {c} games ({100 * c / len(completed):.1f}%)")

    print("\n=== Winners: seat-related VP (rite + milestone + seat_of_empire obj) ===")
    wstats = defaultdict(lambda: {"n": 0, "seat_vp": 0, "total_wvp": 0})
    for rec in completed:
        pmap = pid_persona(rec)
        winner = max(rec["final_vp"], key=lambda k: rec["final_vp"][k])
        pid = int(winner)
        p = rec["final_state"]["players"][pid]
        vp_src = rec["vp_sources"][winner]
        seat_vp = (
            vp_src.get("coronation_rite", 0)
            + vp_src.get("coronation_milestone", 0)
            + (2 if "seat_of_empire" in p.get("shared_scored", []) else 0)
        )
        w = wstats[pmap[pid]]
        w["n"] += 1
        w["seat_vp"] += seat_vp
        w["total_wvp"] += rec["final_vp"][winner]

    for persona in personas:
        w = wstats[persona]
        if not w["n"]:
            continue
        print(
            f"  {persona:12} n={w['n']:2d}  "
            f"avg seat VP={w['seat_vp'] / w['n']:.2f}  "
            f"({100 * w['seat_vp'] / w['total_wvp']:.1f}% of winner VP)"
        )

    print("\n=== Expander in game: win rate vs end-seat control ===")
    exp = {"games": 0, "wins": 0, "held": 0, "win_held": 0, "not_held": 0, "win_not": 0}
    for rec in completed:
        pmap = pid_persona(rec)
        if "expander" not in pmap.values():
            continue
        exp_pid = next(k for k, v in pmap.items() if v == "expander")
        exp["games"] += 1
        winner = int(max(rec["final_vp"], key=lambda k: rec["final_vp"][k]))
        seat_pid = seat_holder(rec["final_state"])
        held = seat_pid == exp_pid
        if winner == exp_pid:
            exp["wins"] += 1
        if held:
            exp["held"] += 1
            if winner == exp_pid:
                exp["win_held"] += 1
        else:
            exp["not_held"] += 1
            if winner == exp_pid:
                exp["win_not"] += 1
    g = exp["games"] or 1
    print(f"  Expander seated in {g} games, won {exp['wins']} ({100 * exp['wins'] / g:.1f}%)")
    print(
        f"  Held seat at end: {exp['held']} — won {exp['win_held']}/{exp['held'] or 1} "
        f"({100 * exp['win_held'] / (exp['held'] or 1):.0f}% conditional)"
    )
    print(
        f"  Did not hold seat: {exp['not_held']} — won {exp['win_not']}/{exp['not_held'] or 1} "
        f"({100 * exp['win_not'] / (exp['not_held'] or 1):.0f}% conditional)"
    )

    print("\n=== Milestone (+2 at 3rd rite) rate ===")
    for persona in personas:
        s = stats[persona]
        g = s["seat_games"] or 1
        print(f"  {persona:12} {100 * s['milestone_games'] / g:5.1f}% of seat-games")

    # Global seat VP budget
    total_vp = sum(sum(rec["final_vp"].values()) for rec in completed)
    seat_all = 0
    for rec in completed:
        for pid_str, src in rec["vp_sources"].items():
            p = rec["final_state"]["players"][int(pid_str)]
            seat_all += src.get("coronation_rite", 0)
            seat_all += src.get("coronation_milestone", 0)
            if "seat_of_empire" in p.get("shared_scored", []):
                seat_all += 2
    print(f"\n=== Global ===")
    print(f"  All seat-related VP: {seat_all} / {total_vp} ({100 * seat_all / total_vp:.1f}% of all VP)")
    print(f"  Per-game avg seat VP: {seat_all / len(completed):.2f}")

    print("\n=== Conditional win rate by end-seat control ===")
    for target in personas:
        d = {"games": 0, "wins": 0, "held": 0, "win_held": 0, "not_held": 0, "win_not": 0}
        for rec in completed:
            pmap = pid_persona(rec)
            if target not in pmap.values():
                continue
            pid = next(k for k, v in pmap.items() if v == target)
            d["games"] += 1
            winner = int(max(rec["final_vp"], key=lambda k: rec["final_vp"][k]))
            seat_pid = seat_holder(rec["final_state"])
            held = seat_pid == pid
            if winner == pid:
                d["wins"] += 1
            if held:
                d["held"] += 1
                if winner == pid:
                    d["win_held"] += 1
            else:
                d["not_held"] += 1
                if winner == pid:
                    d["win_not"] += 1
        g = d["games"] or 1
        print(
            f"  {target:12} win {100 * d['wins'] / g:4.1f}%  |  "
            f"held seat end: {d['held']:2d} -> {d['win_held']:2d} wins "
            f"({100 * d['win_held'] / (d['held'] or 1):.0f}%)  |  "
            f"no seat: {d['not_held']:2d} -> {d['win_not']:2d} wins "
            f"({100 * d['win_not'] / (d['not_held'] or 1):.0f}%)"
        )

    print("\n=== Winners holding seat at game end ===")
    wh = defaultdict(lambda: {"w": 0, "held": 0})
    for rec in completed:
        pmap = pid_persona(rec)
        winner = int(max(rec["final_vp"], key=lambda k: rec["final_vp"][k]))
        seat_pid = seat_holder(rec["final_state"])
        p = pmap[winner]
        wh[p]["w"] += 1
        if seat_pid == winner:
            wh[p]["held"] += 1
    for p in personas:
        w, h = wh[p]["w"], wh[p]["held"]
        if w:
            print(f"  {p:12} {h}/{w} winners held seat ({100 * h / w:.0f}%)")


if __name__ == "__main__":
    p = Path(sys.argv[1] if len(sys.argv) > 1 else "../docs/reports/_seat-analysis-m3.jsonl")
    analyze(p)
