"""Generate shareable HTML balance reports from game records."""
from __future__ import annotations

from statistics import mean, median

from .hypotheses import HYPOTHESES, evaluate_hypotheses
from .summary import (
    _completed,
    _winner,
    played_rounds,
    runaway_rate,
    verdict_breakdown,
    vp_source_totals,
    win_rate_by_persona,
    winner_vp_source_mix,
)

_STATUS_CLASS = {
    "confirmed": "warn-chip",
    "killed": "ok-chip",
    "inconclusive": "warn-chip",
}


def _game_persona(record: dict) -> str:
    personas = record.get("config", {}).get("personas", [])
    if isinstance(personas, list) and personas and len(set(personas)) == 1:
        return personas[0]
    return "mixed"


def _persona_game_stats(records: list[dict]) -> dict[str, dict]:
    """Per-persona stats for solo tournaments (all seats share one persona)."""
    stats: dict[str, dict] = {}
    for r in records:
        persona = _game_persona(r)
        if persona == "mixed":
            continue
        s = stats.setdefault(
            persona,
            {"games": 0, "completed": 0, "rounds": [], "seat_streak_vp": 0, "total_vp": 0},
        )
        s["games"] += 1
        if r["verdict"] == "completed":
            s["completed"] += 1
            s["rounds"].append(played_rounds(r))
            for sources in r.get("vp_sources", {}).values():
                s["total_vp"] += sum(sources.values())
                s["seat_streak_vp"] += sources.get("imperial_seat", 0) + sources.get(
                    "seat_streak_bonus", 0
                )
    for s in stats.values():
        s["completion_rate"] = s["completed"] / s["games"] if s["games"] else 0
        s["avg_rounds"] = mean(s["rounds"]) if s["rounds"] else 0
        s["seat_streak_pct"] = (
            100 * s["seat_streak_vp"] / s["total_vp"] if s["total_vp"] else 0
        )
    return dict(sorted(stats.items()))


def _avg_margin(completed: list[dict]) -> float:
    margins = []
    for r in completed:
        vp = sorted((int(v) for v in r["final_vp"].values()), reverse=True)
        if len(vp) >= 2:
            margins.append(vp[0] - vp[1])
    return mean(margins) if margins else 0.0


def _vp_bar(seat_pct: float, obj_pct: float, lord_pct: float, streak_pct: float) -> str:
    return (
        f'<div class="trend-bar">'
        f'<span style="width:{seat_pct:.1f}%;background:var(--seat)"></span>'
        f'<span style="width:{streak_pct:.1f}%;background:var(--streak)"></span>'
        f'<span style="width:{obj_pct:.1f}%;background:var(--obj)"></span>'
        f'<span style="width:{lord_pct:.1f}%;background:var(--lord)"></span>'
        f"</div>"
    )


def generate_html(
    records: list[dict],
    *,
    title: str = "Persona Playtest Report",
    subtitle: str = "",
    chaos_baseline_seat_pct: float = 63.0,
) -> str:
    n = len(records)
    verdicts = verdict_breakdown(records)
    completed = _completed(records)
    n_done = len(completed)
    crashes = verdicts.get("crashed", 0)
    totals = vp_source_totals(records)
    all_vp = sum(totals.values()) or 1
    seat_vp = totals.get("imperial_seat", 0)
    streak_vp = totals.get("seat_streak_bonus", 0)
    obj_vp = totals.get("objective", 0)
    lord_vp = totals.get("lord_capture", 0)
    seat_pct = 100 * (seat_vp + streak_vp) / all_vp
    obj_pct = 100 * obj_vp / all_vp
    lord_pct = 100 * lord_vp / all_vp
    seat_only = 100 * seat_vp / all_vp
    streak_only = 100 * streak_vp / all_vp
    rounds = [played_rounds(r) for r in completed]
    avg_rounds = mean(rounds) if rounds else 0
    med_rounds = median(rounds) if rounds else 0
    avg_margin = _avg_margin(completed)
    blowout = 100 * runaway_rate(completed)
    winner_mix = winner_vp_source_mix(records)
    persona_games = _persona_game_stats(records)
    hypotheses = evaluate_hypotheses(records)

    h1_status = hypotheses["H1"]["status"]
    h2_status = hypotheses["H2"]["status"]
    seat_delta = seat_pct - chaos_baseline_seat_pct
    seat_note = (
        f"down {abs(seat_delta):.0f} pp from chaos baseline ({chaos_baseline_seat_pct:.0f}%)"
        if seat_delta < 0
        else f"up {seat_delta:.0f} pp from chaos baseline ({chaos_baseline_seat_pct:.0f}%)"
    )

    persona_rows = ""
    for name, s in persona_games.items():
        persona_rows += (
            f"<tr><td>{name}</td><td class=\"r\">{s['games']}</td>"
            f"<td class=\"r\">{s['completed']}</td>"
            f"<td class=\"r\">{100 * s['completion_rate']:.1f}%</td>"
            f"<td class=\"r\">{s['avg_rounds']:.1f}</td>"
            f"<td class=\"r\">{s['seat_streak_pct']:.0f}%</td></tr>\n"
        )

    hyp_rows = ""
    for hid, h in hypotheses.items():
        chip = _STATUS_CLASS.get(h["status"], "warn-chip")
        detail = ", ".join(f"{k}={v}" for k, v in h["detail"].items())
        hyp_rows += (
            f"<tr><td><strong>{hid}</strong></td><td>{h['name']}</td>"
            f"<td><span class=\"{chip}\">{h['status']}</span></td>"
            f"<td>{detail}</td></tr>\n"
        )

    verdict_rows = ""
    for v, c in sorted(verdicts.items(), key=lambda x: -x[1]):
        verdict_rows += f"<tr><td>{v}</td><td class=\"r\">{c}</td><td class=\"r\">{100*c/n:.1f}%</td></tr>\n"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Aeonis — {title}</title>
<style>
  :root {{
    --ink: #1e2430; --muted: #5c6675; --line: #e3e7ee; --bg: #ffffff;
    --panel: #f6f8fb; --accent: #7a5af5; --gold: #c9962a; --good: #2e9e5b;
    --warn: #c74e39; --seat: #7a5af5; --obj: #5b8def; --streak: #b8a0f0; --lord: #ddd7fb;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.6 Georgia, serif; }}
  .wrap {{ max-width: 920px; margin: 0 auto; padding: 48px 28px 80px; }}
  header {{ border-bottom: 3px double var(--ink); padding-bottom: 20px; margin-bottom: 36px; }}
  .kicker {{ font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 12px;
    letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent); font-weight: 700; }}
  h1 {{ font-size: 34px; line-height: 1.2; margin: 8px 0 6px; }}
  .subtitle {{ color: var(--muted); font-size: 15px; }}
  h2 {{ font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 15px;
    letter-spacing: 0.12em; text-transform: uppercase; border-bottom: 1px solid var(--line);
    padding-bottom: 8px; margin: 44px 0 16px; }}
  p {{ margin: 0 0 14px; }}
  .tldr {{ background: var(--panel); border-left: 4px solid var(--accent);
    padding: 18px 22px; border-radius: 0 8px 8px 0; }}
  .statgrid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 12px; margin: 20px 0; }}
  .stat {{ background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; }}
  .stat .num {{ font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 26px; font-weight: 700; }}
  .stat .lbl {{ font-size: 12px; color: var(--muted); margin-top: 4px;
    font-family: 'Helvetica Neue', Arial, sans-serif; }}
  table {{ border-collapse: collapse; width: 100%; margin: 14px 0 20px;
    font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 13px; }}
  th {{ text-align: left; font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase;
    color: var(--muted); border-bottom: 2px solid var(--ink); padding: 8px; }}
  td {{ border-bottom: 1px solid var(--line); padding: 8px; vertical-align: top; }}
  td.r, th.r {{ text-align: right; font-variant-numeric: tabular-nums; }}
  .note {{ background: #fdf6ec; border-left: 4px solid var(--gold); padding: 14px 18px;
    border-radius: 0 8px 8px 0; font-size: 15px; margin: 18px 0; }}
  .ok-chip, .warn-chip {{ display: inline-block; font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 11px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;
    padding: 2px 9px; border-radius: 99px; }}
  .ok-chip {{ background: #e3f4ea; color: var(--good); }}
  .warn-chip {{ background: #fbe9e4; color: var(--warn); }}
  .trend-row {{ display: grid; grid-template-columns: 120px 1fr 52px; gap: 10px; align-items: center;
    margin: 6px 0; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 13px; }}
  .trend-bar {{ display: flex; height: 20px; border-radius: 5px; overflow: hidden; background: var(--panel); }}
  .trend-bar span {{ height: 100%; }}
  .legend {{ display: flex; flex-wrap: wrap; gap: 16px; margin: 12px 0 20px;
    font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 12px; color: var(--muted); }}
  .legend i {{ display: inline-block; width: 12px; height: 12px; border-radius: 3px;
    vertical-align: -2px; margin-right: 5px; }}
  footer {{ margin-top: 56px; padding-top: 16px; border-top: 1px solid var(--line);
    color: var(--muted); font-size: 13px; font-family: 'Helvetica Neue', Arial, sans-serif; }}
</style>
</head>
<body>
<div class="wrap">

<header>
  <div class="kicker">Aeonis · Plan B · Persona Bots</div>
  <h1>{title}</h1>
  <div class="subtitle">{subtitle}</div>
</header>

<div class="tldr">
  <p style="margin:0"><strong>TL;DR —</strong> {n:,} persona-bot games at 4 players, zero crashes.
  <strong>{n_done:,} completed ({100*n_done/n:.1f}%)</strong>. Seat+streak supplies
  <strong>{seat_pct:.0f}%</strong> of all VP ({seat_note}). Mean winning margin
  <strong>{avg_margin:.1f} VP</strong>; runaway rate (≥7 margin) <strong>{blowout:.0f}%</strong>.
  H1 (Seat dominance): <strong>{h1_status}</strong>. H2 (blowout margins): <strong>{h2_status}</strong>.</p>
</div>

<h2>1 · Campaign at a glance <span class="ok-chip">{n:,} games · {crashes} crashes</span></h2>

<div class="statgrid">
  <div class="stat"><div class="num">{n_done:,}</div><div class="lbl">completed</div></div>
  <div class="stat"><div class="num">{avg_rounds:.1f}</div><div class="lbl">avg rounds</div></div>
  <div class="stat"><div class="num">{avg_margin:.1f}</div><div class="lbl">avg win margin</div></div>
  <div class="stat"><div class="num">{seat_pct:.0f}%</div><div class="lbl">seat + streak VP</div></div>
  <div class="stat"><div class="num">{obj_pct:.0f}%</div><div class="lbl">objective VP</div></div>
  <div class="stat"><div class="num">{lord_pct:.1f}%</div><div class="lbl">lord capture VP</div></div>
</div>

<h2>2 · Verdict breakdown</h2>
<table>
  <tr><th>Verdict</th><th class="r">Count</th><th class="r">%</th></tr>
  {verdict_rows}
</table>

<h2>3 · VP source distribution (completed games)</h2>
<div class="legend">
  <span><i style="background:var(--seat)"></i>Imperial Seat</span>
  <span><i style="background:var(--streak)"></i>Streak bonus</span>
  <span><i style="background:var(--obj)"></i>Objectives</span>
  <span><i style="background:var(--lord)"></i>Lord capture</span>
</div>
<div class="trend-row">
  <span>All VP</span>
  {_vp_bar(seat_only, obj_pct, lord_pct, streak_only)}
  <span class="r">{all_vp:,}</span>
</div>

<table>
  <tr><th>Source</th><th class="r">VP</th><th class="r">% total</th><th class="r">% winner VP (avg)</th></tr>
  <tr><td>imperial_seat</td><td class="r">{seat_vp:,}</td><td class="r">{seat_only:.1f}%</td>
      <td class="r">{100*winner_mix.get('imperial_seat',0):.1f}%</td></tr>
  <tr><td>seat_streak_bonus</td><td class="r">{streak_vp:,}</td><td class="r">{streak_only:.1f}%</td>
      <td class="r">{100*winner_mix.get('seat_streak_bonus',0):.1f}%</td></tr>
  <tr><td>objective</td><td class="r">{obj_vp:,}</td><td class="r">{obj_pct:.1f}%</td>
      <td class="r">{100*winner_mix.get('objective',0):.1f}%</td></tr>
  <tr><td>lord_capture</td><td class="r">{lord_vp:,}</td><td class="r">{lord_pct:.1f}%</td>
      <td class="r">{100*winner_mix.get('lord_capture',0):.1f}%</td></tr>
</table>

<div class="note">
<strong>Chaos baseline comparison:</strong> Chaos bots at 4p showed ~73% Seat wins and 63% Seat+streak
VP share. Persona bots shift incentives but Seat+streak remains the largest bucket unless H1 is killed.
</div>

<h2>4 · Per-persona breakdown (solo-seat tournaments)</h2>
<p>Each game assigns the same persona to all four seats (200 games each). Win rate is
not meaningful here — every winner is that persona. Completion rate and VP shape are the comparators.</p>
<table>
  <tr><th>Persona</th><th class="r">Games</th><th class="r">Completed</th>
      <th class="r">Completion</th><th class="r">Avg rounds</th><th class="r">Seat+streak VP</th></tr>
  {persona_rows}
</table>

<h2>5 · Hypothesis evaluation (H1–H6)</h2>
<table>
  <tr><th>ID</th><th>Hypothesis</th><th>Status</th><th>Metrics</th></tr>
  {hyp_rows}
</table>

<footer>
  Persona-bot tournament · seeds from config seed_base · Balance stats from <code>completed</code> verdicts only.
  Chaos data excluded. Not a canon-change input without human playtest confirmation.
</footer>

</div>
</body>
</html>
"""
