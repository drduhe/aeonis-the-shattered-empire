"""Evaluate structural hypotheses H1–H6 from readiness brief."""
from __future__ import annotations

from .summary import (
    _completed,
    _winner,
    artifact_metrics,
    played_rounds,
    persona_parity_metrics,
    runaway_rate,
    seat_vp_from_totals,
    verdict_breakdown,
    vp_source_totals,
    whisper_metrics,
    win_rate_by_persona,
    winner_vp_source_mix,
    is_mixed_tournament,
)

HYPOTHESES = {
    "H1": {
        "name": "Seat+streak >50% of all VP under contest",
        "kill": "Seat+streak <40% with strategic contest",
    },
    "H2": {
        "name": "Winning margin >5 VP under strategic play",
        "kill": "Margin <4 VP → runaway acceptable",
    },
    "H3": {
        "name": "Objectives can reach ≥60% of winner VP",
        "kill": "Winner objective share ≥60% at either count",
    },
    "H4": {
        "name": "8p timeouts are pacing not map bug",
        "kill": "Timeout rate <3% with VP-seeking bots at 8p",
    },
    "H5": {
        "name": "Combat VP marginal even for Warmonger",
        "kill": "Lord capture >10% of winner VP",
    },
    "H6": {
        "name": "no_vp_progress is chaos artifact",
        "kill": "Degenerate rate <2% with strategic bots",
    },
    "H7": {
        "name": "No persona dominates mixed-seat win rate",
        "kill": "Expander ≤30% and max persona ≤28% in mixed brackets",
    },
    "H8": {
        "name": "Economist viable in mixed seats (builder/gold path)",
        "kill": "Economist win rate ≥5% in mixed 6–8p brackets",
    },
    "H9": {
        "name": "Diplomat win rate ≥3% in mixed 4p M2 bracket",
        "kill": "Diplomat win rate ≥3% in mixed 4p",
    },
    "H10": {
        "name": "Whisper draw rate keeps hands manageable (≤7 without flooding)",
        "kill": "Forced discard rate <25% of whisper draws",
    },
    "H11": {
        "name": "First artifact by round 3–4 (packet goal 10)",
        "kill": "Median first-artifact round 3–4 in completed games",
    },
    "H12": {
        "name": "Merchant Lord lifts economist mixed 4p win rate ≥5%",
        "kill": "Economist win rate ≥5% in mixed 4p at M3 fidelity",
    },
}


def _avg_margin(records: list[dict]) -> float:
    margins = []
    for r in _completed(records):
        vp = sorted((int(v) for v in r["final_vp"].values()), reverse=True)
        if len(vp) >= 2:
            margins.append(vp[0] - vp[1])
    return sum(margins) / len(margins) if margins else 0.0


def _status_h1(records: list[dict]) -> str:
    totals = vp_source_totals(records)
    all_vp = sum(totals.values()) or 1
    seat = seat_vp_from_totals(totals)
    pct = 100 * seat / all_vp
    if pct < 40:
        return "killed"
    if pct > 50:
        return "confirmed"
    return "inconclusive"


def _status_h2(records: list[dict]) -> str:
    m = _avg_margin(records)
    if m < 4:
        return "killed"
    if m > 5:
        return "confirmed"
    return "inconclusive"


def _status_h3(records: list[dict]) -> str:
    mix = winner_vp_source_mix(records)
    if mix.get("objective", 0) >= 0.6:
        return "killed"  # kill criterion met = hypothesis goal achieved
    if mix.get("objective", 0) < 0.3:
        return "confirmed"  # objectives still marginal
    return "inconclusive"


def _status_h4(records: list[dict], players: int = 8) -> str:
    subset = [r for r in records if r["config"].get("players") == players]
    if not subset:
        return "inconclusive"
    timeouts = sum(1 for r in subset if r["verdict"] == "timeout")
    rate = timeouts / len(subset)
    if rate < 0.03:
        return "killed"
    if rate > 0.08:
        return "confirmed"
    return "inconclusive"


def _status_h5(records: list[dict]) -> str:
    mix = winner_vp_source_mix(records)
    if mix.get("lord_capture", 0) > 0.10:
        return "killed"  # combat path viable — Plan 1 urgent
    if mix.get("lord_capture", 0) < 0.03:
        return "confirmed"
    return "inconclusive"


def _status_h6(records: list[dict]) -> str:
    n = len(records)
    deg = sum(1 for r in records if r["verdict"] == "degenerate")
    rate = deg / n if n else 0
    if rate < 0.02:
        return "killed"
    if rate > 0.05:
        return "confirmed"
    return "inconclusive"


def _status_h7(records: list[dict]) -> str:
    pm = persona_parity_metrics(records)
    if not pm:
        return "inconclusive"
    exp = pm.get("expander_win_rate", 1.0)
    mx = pm.get("max_win_rate", 1.0)
    if exp <= 0.30 and mx <= 0.28:
        return "killed"
    if exp > 0.35 or mx > 0.35:
        return "confirmed"
    return "inconclusive"


def _status_h8(records: list[dict]) -> str:
    pm = persona_parity_metrics(records)
    if not pm:
        return "inconclusive"
    players = records[0]["config"].get("players", 0) if records else 0
    if players < 6:
        return "inconclusive"
    eco = pm.get("by_persona", {}).get("economist", {}).get("win_rate", 0.0)
    if eco >= 0.05:
        return "killed"
    if eco < 0.02:
        return "confirmed"
    return "inconclusive"


def _status_h9(records: list[dict]) -> str:
    if not is_mixed_tournament(records):
        return "inconclusive"
    players = records[0]["config"].get("players", 0) if records else 0
    if players != 4:
        return "inconclusive"
    pm = persona_parity_metrics(records)
    if not pm:
        return "inconclusive"
    dip = pm.get("by_persona", {}).get("diplomat", {}).get("win_rate", 0.0)
    if dip >= 0.03:
        return "killed"
    if dip < 0.01:
        return "confirmed"
    return "inconclusive"


def _status_h12(records: list[dict]) -> str:
    if not is_mixed_tournament(records):
        return "inconclusive"
    players = records[0]["config"].get("players", 0) if records else 0
    if players != 4:
        return "inconclusive"
    pm = persona_parity_metrics(records)
    if not pm:
        return "inconclusive"
    eco = pm.get("by_persona", {}).get("economist", {}).get("win_rate", 0.0)
    if eco >= 0.05:
        return "killed"
    if eco < 0.02:
        return "confirmed"
    return "inconclusive"


def _status_h10(records: list[dict]) -> str:
    wm = whisper_metrics(records)
    if not wm or wm.get("drawn", 0) == 0:
        return "inconclusive"
    rate = wm.get("discard_rate", 0.0)
    if rate < 0.25:
        return "killed"
    if rate > 0.40:
        return "confirmed"
    return "inconclusive"


def _status_h11(records: list[dict]) -> str:
    am = artifact_metrics(records)
    med = am.get("median_first_artifact_round")
    if med is None:
        return "inconclusive"
    if 3 <= med <= 4:
        return "killed"
    if med < 2 or med > 5:
        return "confirmed"
    return "inconclusive"


_EVALUATORS = {
    "H1": _status_h1,
    "H2": _status_h2,
    "H3": _status_h3,
    "H4": lambda r: _status_h4(r, 8),
    "H5": _status_h5,
    "H6": _status_h6,
    "H7": _status_h7,
    "H8": _status_h8,
    "H9": _status_h9,
    "H10": _status_h10,
    "H11": _status_h11,
    "H12": _status_h12,
}


def evaluate_hypotheses(records: list[dict]) -> dict[str, dict]:
    completed = _completed(records)
    out = {}
    for hid, meta in HYPOTHESES.items():
        status = _EVALUATORS[hid](records)
        detail = {}
        if hid == "H1":
            t = vp_source_totals(completed)
            all_vp = sum(t.values()) or 1
            detail["seat_streak_pct"] = round(
                100 * seat_vp_from_totals(t) / all_vp, 1
            )
        elif hid == "H2":
            detail["avg_margin"] = round(_avg_margin(completed), 2)
            detail["runaway_rate"] = round(runaway_rate(completed), 3)
        elif hid == "H3":
            detail["winner_objective_share"] = round(
                winner_vp_source_mix(completed).get("objective", 0), 3
            )
        elif hid == "H4":
            p8 = [r for r in records if r["config"].get("players") == 8]
            detail["timeout_rate_8p"] = round(
                sum(1 for r in p8 if r["verdict"] == "timeout") / max(len(p8), 1), 3
            )
        elif hid == "H5":
            detail["winner_lord_capture_share"] = round(
                winner_vp_source_mix(completed).get("lord_capture", 0), 3
            )
        elif hid == "H6":
            detail["degenerate_rate"] = round(
                verdict_breakdown(records).get("degenerate", 0) / max(len(records), 1), 3
            )
        elif hid == "H7":
            pm = persona_parity_metrics(records)
            detail["expander_win_rate"] = round(pm.get("expander_win_rate", 0), 3)
            detail["max_persona_win_rate"] = round(pm.get("max_win_rate", 0), 3)
        elif hid == "H8":
            pm = persona_parity_metrics(records)
            detail["economist_win_rate"] = round(
                pm.get("by_persona", {}).get("economist", {}).get("win_rate", 0.0), 3
            )
        elif hid == "H9":
            pm = persona_parity_metrics(records)
            detail["diplomat_win_rate"] = round(
                pm.get("by_persona", {}).get("diplomat", {}).get("win_rate", 0.0), 3
            )
            detail["mixed_4p"] = is_mixed_tournament(records) and (
                records[0]["config"].get("players") == 4 if records else False
            )
        elif hid == "H10":
            wm = whisper_metrics(records)
            detail["whisper_discard_rate"] = round(wm.get("discard_rate", 0.0), 3)
            detail["plays_per_round"] = round(wm.get("plays_per_round", 0.0), 2)
        elif hid == "H11":
            am = artifact_metrics(records)
            med = am.get("median_first_artifact_round")
            detail["median_first_artifact_round"] = med
            detail["artifact_vp_share"] = round(am.get("artifact_vp_share", 0.0), 3)
        elif hid == "H12":
            pm = persona_parity_metrics(records)
            detail["economist_win_rate_4p"] = round(
                pm.get("by_persona", {}).get("economist", {}).get("win_rate", 0.0), 3
            )
            detail["mixed_4p"] = is_mixed_tournament(records) and (
                records[0]["config"].get("players") == 4 if records else False
            )
        out[hid] = {
            "name": meta["name"],
            "kill_criterion": meta["kill"],
            "status": status,
            "detail": detail,
        }
    return out


def hypotheses_markdown(results: dict[str, dict]) -> str:
    lines = ["## Hypothesis evaluation (H1–H12)", ""]
    lines.append("| ID | Hypothesis | Status | Detail |")
    lines.append("| --- | --- | --- | --- |")
    for hid, r in results.items():
        detail = ", ".join(f"{k}={v}" for k, v in r["detail"].items())
        lines.append(f"| {hid} | {r['name']} | **{r['status']}** | {detail} |")
    return "\n".join(lines) + "\n"
