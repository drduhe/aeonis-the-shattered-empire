"""Aggregate JSONL game records into balance summaries."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import mean, median

VP_SOURCES = (
    "coronation_rite",
    "coronation_milestone",
    "imperial_seat",       # legacy records
    "seat_streak_bonus",   # legacy records
    "objective",
    "lord_capture",
)


def seat_vp_from_totals(totals: dict) -> int:
    """Coronation Rite + milestone (includes legacy Seat drip keys)."""
    return (
        totals.get("coronation_rite", 0)
        + totals.get("coronation_milestone", 0)
        + totals.get("imperial_seat", 0)
        + totals.get("seat_streak_bonus", 0)
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


def persona_parity_metrics(records: list[dict]) -> dict:
    """Win-rate spread for mixed-seat tournaments (H7)."""
    rates = win_rate_by_persona(records)
    if not rates:
        return {}
    win_rates = [s["win_rate"] for s in rates.values() if s["games"] > 0]
    if not win_rates:
        return {}
    return {
        "expander_win_rate": rates.get("expander", {}).get("win_rate", 0.0),
        "max_win_rate": max(win_rates),
        "min_win_rate": min(win_rates),
        "by_persona": rates,
    }


def event_metrics(records: list[dict]) -> dict:
    done = _completed(records)
    if not done:
        return {}
    total = sum(r.get("event_stats", {}).get("resolved", 0) for r in done)
    by_card: dict[str, int] = Counter()
    for r in done:
        for card, n in r.get("event_stats", {}).get("by_card", {}).items():
            by_card[card] += n
    rounds = sum(played_rounds(r) for r in done) or 1
    return {
        "events_resolved": total,
        "events_per_round": total / rounds,
        "by_card": dict(by_card),
    }


def council_metrics(records: list[dict]) -> dict:
    done = _completed(records)
    if not done:
        return {}
    proposed = sum(r.get("council_stats", {}).get("motions_proposed", 0) for r in done)
    passed = sum(r.get("council_stats", {}).get("motions_passed", 0) for r in done)
    failed = sum(r.get("council_stats", {}).get("motions_failed", 0) for r in done)
    votes_yes = sum(r.get("council_stats", {}).get("votes_yes", 0) for r in done)
    votes_no = sum(r.get("council_stats", {}).get("votes_no", 0) for r in done)
    influence = sum(r.get("council_stats", {}).get("influence_spent", 0) for r in done)
    rounds = sum(played_rounds(r) for r in done) or 1
    votes = votes_yes + votes_no
    return {
        "motions_proposed": proposed,
        "motions_passed": passed,
        "motions_failed": failed,
        "pass_rate": passed / proposed if proposed else 0.0,
        "motions_per_round": proposed / rounds,
        "votes_yes": votes_yes,
        "votes_no": votes_no,
        "yes_vote_rate": votes_yes / votes if votes else 0.0,
        "influence_spent": influence,
        "avg_influence_per_round": influence / rounds,
    }


def is_mixed_tournament(records: list[dict]) -> bool:
    for r in records:
        personas = r.get("config", {}).get("personas", [])
        if isinstance(personas, list) and len(set(personas)) > 1:
            return True
    return False


def strategy_metrics(records: list[dict]) -> dict:
    """Draft picks and primary uses from choice logs."""
    done = _completed(records)
    if not done:
        return {}
    draft: Counter = Counter()
    primary: Counter = Counter()
    secondary_yes = 0
    secondary_no = 0
    for r in done:
        for c in r.get("choices", []):
            t = c.get("type")
            if t == "draft":
                draft[c["card"]] += 1
            elif t == "strategy_primary":
                primary[c["card"]] += 1
            elif t == "strategy_secondary":
                if c.get("use"):
                    secondary_yes += 1
                else:
                    secondary_no += 1
    draft_total = sum(draft.values()) or 1
    primary_total = sum(primary.values()) or 1
    return {
        "draft_picks": dict(draft),
        "draft_rates": {k: v / draft_total for k, v in draft.items()},
        "primary_uses": dict(primary),
        "primary_rates": {k: v / primary_total for k, v in primary.items()},
        "secondary_opt_in_rate": (
            secondary_yes / (secondary_yes + secondary_no)
            if (secondary_yes + secondary_no)
            else 0.0
        ),
    }


def format_strategy_section(records: list[dict]) -> list[str]:
    sm = strategy_metrics(records)
    if not sm or not sm.get("draft_picks"):
        return []
    lines = [
        "",
        "## Strategy cards (M2)",
        "",
        "### Draft pick rate",
        "",
        "| Card | Picks | % |",
        "| --- | ---: | ---: |",
    ]
    draft_total = sum(sm["draft_picks"].values())
    for card, n in sorted(sm["draft_picks"].items(), key=lambda x: -x[1]):
        lines.append(f"| {card} | {n} | {100 * n / draft_total:.1f}% |")
    if sm.get("primary_uses"):
        lines.extend([
            "",
            "### Primary use rate (among primaries played)",
            "",
            "| Card | Uses | % |",
            "| --- | ---: | ---: |",
        ])
        primary_total = sum(sm["primary_uses"].values())
        for card, n in sorted(sm["primary_uses"].items(), key=lambda x: -x[1]):
            lines.append(f"| {card} | {n} | {100 * n / primary_total:.1f}% |")
    lines.append(
        f"\n**Secondary opt-in rate:** {100 * sm['secondary_opt_in_rate']:.1f}%"
    )
    return lines


def combat_metrics(records: list[dict]) -> dict:
    """Aggregate Plan 1 combat stats from completed games."""
    done = _completed(records)
    if not done:
        return {}
    battles = sum(r.get("combat_stats", {}).get("battles", 0) for r in done)
    att_wins = sum(r.get("combat_stats", {}).get("attacker_wins", 0) for r in done)
    def_wins = sum(r.get("combat_stats", {}).get("defender_wins", 0) for r in done)
    rounds = sum(played_rounds(r) for r in done)
    players = done[0]["config"]["players"]
    player_rounds = rounds * players
    out = {
        "battles": battles,
        "attacker_wins": att_wins,
        "defender_wins": def_wins,
        "attacker_win_rate": att_wins / battles if battles else 0.0,
        "battles_per_player_round": battles / player_rounds if player_rounds else 0.0,
    }
    scm = stratified_combat_metrics(records)
    if scm:
        out["contested_attacker_win_rate"] = scm["contested_attacker_win_rate"]
    return out


_STRATIFIED_KEYS = (
    "retreats",
    "uncontested_captures",
    "contested_gte1_battles",
    "contested_gte1_att_wins",
    "contested_gte1_def_wins",
    "contested_lt1_battles",
    "contested_lt1_att_wins",
    "contested_lt1_def_wins",
)


def _merge_stratified(records: list[dict]) -> dict:
    totals = {k: 0 for k in _STRATIFIED_KEYS}
    for r in _completed(records):
        strat = r.get("combat_stats", {}).get("stratified", {})
        for k in _STRATIFIED_KEYS:
            totals[k] += strat.get(k, 0)
    return totals


def _att_win_rate(att_wins: int, battles: int) -> float | None:
    return att_wins / battles if battles else None


def stratified_combat_metrics(records: list[dict]) -> dict:
    """Contested-only attacker win rates by initiation quality (att dice vs def dice)."""
    done = _completed(records)
    if not done:
        return {}
    s = _merge_stratified(records)
    if not any(s[k] for k in _STRATIFIED_KEYS):
        return {}
    gte1_b = s["contested_gte1_battles"]
    lt1_b = s["contested_lt1_battles"]
    contested_b = gte1_b + lt1_b
    contested_att = s["contested_gte1_att_wins"] + s["contested_lt1_att_wins"]
    return {
        **s,
        "contested_battles": contested_b,
        "contested_att_wins": contested_att,
        "contested_attacker_win_rate": (
            contested_att / contested_b if contested_b else 0.0
        ),
        "gte1_attacker_win_rate": (
            s["contested_gte1_att_wins"] / gte1_b if gte1_b else None
        ),
        "lt1_attacker_win_rate": (
            s["contested_lt1_att_wins"] / lt1_b if lt1_b else None
        ),
    }


def format_stratified_combat_section(records: list[dict]) -> list[str]:
    """Markdown lines for stratified combat block."""
    scm = stratified_combat_metrics(records)
    if not scm:
        return []
    cm = combat_metrics(records)
    lines = [
        "",
        "## Combat stratification (contested initiations)",
        "",
        "Initiation quality uses committed **attack dice** vs **defense dice** at "
        "battle start. Uncontested captures (no defender units) and retreats are "
        "tracked separately and excluded from contested win rates.",
        "",
        f"- All battles (legacy): {cm['battles']} · attacker wins "
        f"{100 * cm['attacker_win_rate']:.1f}%",
        f"- Uncontested captures: {scm['uncontested_captures']}",
        f"- Defender retreats: {scm['retreats']}",
        "",
        "| Bucket | Battles | Att wins | Att win % |",
        "| --- | ---: | ---: | ---: |",
    ]

    def row(label: str, battles: int, att: int) -> str:
        rate = _att_win_rate(att, battles)
        pct = f"{100 * rate:.1f}%" if rate is not None else "—"
        return f"| {label} | {battles} | {att} | {pct} |"

    lines.append(
        row(
            "Contested (all)",
            scm["contested_battles"],
            scm["contested_att_wins"],
        )
    )
    lines.append(
        row(
            "Ratio ≥ 1.0 (att dice ≥ def dice)",
            scm["contested_gte1_battles"],
            scm["contested_gte1_att_wins"],
        )
    )
    lines.append(
        row(
            "Ratio < 1.0 (att dice < def dice)",
            scm["contested_lt1_battles"],
            scm["contested_lt1_att_wins"],
        )
    )
    lines.append(
        f"\n**Contested attacker win rate:** "
        f"{100 * scm['contested_attacker_win_rate']:.1f}% "
        f"(Plan 1 human target: 55–65%)"
    )
    return lines


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
    for src in ("coronation_rite", "coronation_milestone", "objective", "lord_capture"):
        v = totals.get(src, 0)
        lines.append(
            f"| {src} | {v} | {100 * v / all_vp:.1f}% | {100 * winner_mix.get(src, 0):.1f}% |"
        )
    seat_streak = seat_vp_from_totals(totals)
    lines.append(
        f"\n**Seat + streak combined:** {100 * seat_streak / all_vp:.1f}% of all VP"
    )
    cm = combat_metrics(records)
    if cm:
        lines.extend([
            "",
            "## Combat metrics (completed)",
            "",
            f"- Battles resolved: {cm['battles']}",
            f"- Attacker win rate (all): {100 * cm['attacker_win_rate']:.1f}%",
            f"- Battles per player-round: {cm['battles_per_player_round']:.3f}",
        ])
        if "contested_attacker_win_rate" in cm:
            lines.append(
                f"- Contested attacker win rate: "
                f"{100 * cm['contested_attacker_win_rate']:.1f}%"
            )
    lines.extend(format_stratified_combat_section(records))
    em = event_metrics(records)
    if em:
        lines.extend([
            "",
            "## Event phase (M2)",
            "",
            f"- Events resolved: {em['events_resolved']}",
            f"- Events per round: {em['events_per_round']:.2f}",
        ])
        top = sorted(em["by_card"].items(), key=lambda x: -x[1])[:5]
        if top:
            lines.append("- Top events: " + ", ".join(f"{k} ({v})" for k, v in top))
    cr = council_metrics(records)
    if cr:
        lines.extend([
            "",
            "## High Council (M2)",
            "",
            f"- Motions proposed: {cr['motions_proposed']}",
            f"- Motions passed: {cr['motions_passed']}",
            f"- Motions failed: {cr['motions_failed']}",
            f"- Pass rate: {100 * cr['pass_rate']:.1f}%",
            f"- Yes votes: {cr['votes_yes']} · No votes: {cr['votes_no']} "
            f"({100 * cr['yes_vote_rate']:.1f}% yes)",
            f"- Motions per round: {cr['motions_per_round']:.2f}",
            f"- Influence spent (lobby): {cr['influence_spent']}",
            f"- Avg influence spent / round: {cr['avg_influence_per_round']:.2f}",
        ])
    lines.extend(format_strategy_section(records))
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
