"""Aggregate JSONL game records into balance summaries."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import mean, median

VP_SOURCES = (
    "imperial_seat",
    "seat_streak_bonus",
    "objective",
    "lord_capture",
)


def played_rounds(record: dict) -> int:
    """Rounds actually played (record counter increments at round start)."""
    return max(0, record.get("rounds", 0) - 1)


def load_records(path: str | Path) -> list[dict]:
    out = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def verdict_breakdown(records: list[dict]) -> dict[str, int]:
    return dict(Counter(r["verdict"] for r in records))


def _winner(record: dict) -> int | None:
    vp = record.get("final_vp", {})
    if not vp:
        return None
    best = max(vp.values())
    leaders = [int(pid) for pid, v in vp.items() if v == best]
    return leaders[0] if len(leaders) == 1 else None


def _persona_of(record: dict, pid: int) -> str:
    personas = record.get("config", {}).get("personas", {})
    if isinstance(personas, list):
        return personas[pid] if pid < len(personas) else "unknown"
    return personas.get(str(pid), personas.get(pid, "unknown"))


def _completed(records: list[dict]) -> list[dict]:
    return [r for r in records if r["verdict"] == "completed"]


def win_rate_by_persona(records: list[dict]) -> dict[str, dict]:
    stats: dict[str, dict] = defaultdict(lambda: {"games": 0, "wins": 0})
    for r in _completed(records):
        w = _winner(r)
        if w is None:
            continue
        for pid in r["final_vp"]:
            pid = int(pid)
            persona = _persona_of(r, pid)
            stats[persona]["games"] += 1
            if pid == w:
                stats[persona]["wins"] += 1
    out = {}
    for persona, s in sorted(stats.items()):
        g = s["games"]
        out[persona] = {
            "games": g,
            "wins": s["wins"],
            "win_rate": s["wins"] / g if g else 0.0,
        }
    return out


def vp_source_totals(records: list[dict]) -> dict[str, int]:
    totals: dict[str, int] = Counter()
    for r in _completed(records):
        for sources in r.get("vp_sources", {}).values():
            for src, n in sources.items():
                totals[src] += n
    return dict(totals)


def winner_vp_source_mix(records: list[dict]) -> dict[str, float]:
    """Average share of winner VP by source."""
    shares: dict[str, list[float]] = defaultdict(list)
    for r in _completed(records):
        w = _winner(r)
        if w is None:
            continue
        sources = r.get("vp_sources", {}).get(str(w), r.get("vp_sources", {}).get(w, {}))
        total = sum(sources.values()) or 1
        for src in VP_SOURCES:
            shares[src].append(sources.get(src, 0) / total)
    return {src: mean(vals) if vals else 0.0 for src, vals in shares.items()}


def runaway_rate(records: list[dict], margin: int = 7) -> float:
    done = _completed(records)
    if not done:
        return 0.0
    blowouts = 0
    for r in done:
        vp = [int(v) for v in r["final_vp"].values()]
        if max(vp) - sorted(vp)[-2] >= margin:
            blowouts += 1
    return blowouts / len(done)


def balance_summary(records: list[dict], title: str = "Balance Summary") -> str:
    n = len(records)
    verdicts = verdict_breakdown(records)
    completed = _completed(records)
    lines = [
        f"# {title}",
        "",
        f"Games: {n} · Completed: {len(completed)} ({100 * len(completed) / n:.1f}%)" if n else f"# {title}",
        "",
        "## Verdict breakdown",
        "",
        "| Verdict | Count | % |",
        "| --- | ---: | ---: |",
    ]
    for v, c in sorted(verdicts.items(), key=lambda x: -x[1]):
        lines.append(f"| {v} | {c} | {100 * c / n:.1f}% |")

    if not completed:
        lines.append("\nNo completed games — balance sections omitted.")
        return "\n".join(lines) + "\n"

    rounds = [played_rounds(r) for r in completed]
    margins = []
    for r in completed:
        vp = sorted((int(v) for v in r["final_vp"].values()), reverse=True)
        if len(vp) >= 2:
            margins.append(vp[0] - vp[1])

    lines.extend([
        "",
        "## Round length (completed)",
        "",
        f"- Mean: {mean(rounds):.1f}",
        f"- Median: {median(rounds):.0f}",
        "",
        "## Winning margin (completed)",
        "",
        f"- Mean: {mean(margins):.1f} VP" if margins else "- Mean: n/a",
        f"- Runaway rate (margin ≥7): {100 * runaway_rate(completed):.1f}%",
        "",
        "## Win rate by persona (seat games, completed only)",
        "",
        "| Persona | Games | Wins | Win % |",
        "| --- | ---: | ---: | ---: |",
    ])
    for persona, s in win_rate_by_persona(records).items():
        lines.append(
            f"| {persona} | {s['games']} | {s['wins']} | {100 * s['win_rate']:.1f}% |"
        )

    totals = vp_source_totals(records)
    all_vp = sum(totals.values()) or 1
    winner_mix = winner_vp_source_mix(records)
    lines.extend([
        "",
        "## VP sources (all VP in completed games)",
        "",
        "| Source | VP | % of total | % of winner VP (avg) |",
        "| --- | ---: | ---: | ---: |",
    ])
    for src in VP_SOURCES:
        v = totals.get(src, 0)
        lines.append(
            f"| {src} | {v} | {100 * v / all_vp:.1f}% | {100 * winner_mix.get(src, 0):.1f}% |"
        )
    seat_streak = totals.get("imperial_seat", 0) + totals.get("seat_streak_bonus", 0)
    lines.append(
        f"\n**Seat + streak combined:** {100 * seat_streak / all_vp:.1f}% of all VP"
    )
    return "\n".join(lines) + "\n"


def append_session_log(records: list[dict], path: str | Path) -> int:
    """Append simulated session rows; returns rows written."""
    p = Path(path)
    if not p.exists():
        p.write_text(
            "date,players,vp_variant,rounds,total_minutes,minutes_per_round,"
            "winner_lord,winner_vp,lords_in_play,vp_by_player,winner_vp_sources,"
            "first_artifact_round,first_legendary_round,seat_rounds_held_by,"
            "lord_captures,motions_proposed,motions_passed,catchup_worked,"
            "worst_downtime_min,play_again_yes,play_again_no,notes\n"
        )
    today = date.today().isoformat()
    rows = []
    for r in records:
        if r["verdict"] != "completed":
            continue
        w = _winner(r)
        if w is None:
            continue
        vp = r["final_vp"]
        sources = r.get("vp_sources", {}).get(str(w), r.get("vp_sources", {}).get(w, {}))
        src_str = ";".join(f"{k}:{v}" for k, v in sorted(sources.items()))
        vp_str = ";".join(f"p{pid}:{v}" for pid, v in sorted(vp.items(), key=lambda x: int(x[0])))
        personas = r.get("config", {}).get("personas", {})
        note = f"sim;personas={personas}"
        rows.append(
            f"{today},{r['config']['players']},10,{played_rounds(r)},0,0,"
            f"generic,{vp[str(w)]},generic,{vp_str},{src_str},"
            f",,,,,,,,simulated,0,0,{note}\n"
        )
    with p.open("a") as f:
        for row in rows:
            f.write(row)
    return len(rows)
