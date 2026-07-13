"""Plan 1/2 regression gates for tournament configs (sim-only, not canon)."""
from __future__ import annotations

from .summary import (
    _completed,
    ap_economy_metrics,
    bookkeeping_metrics,
    combat_metrics,
    played_rounds,
    verdict_breakdown,
    winner_vp_source_mix,
)


def _crash_rate(records: list[dict]) -> float:
    n = len(records) or 1
    return verdict_breakdown(records).get("crashed", 0) / n


def _timeout_rate(records: list[dict]) -> float:
    n = len(records) or 1
    return verdict_breakdown(records).get("timeout", 0) / n


def _completed_rate(records: list[dict]) -> float:
    n = len(records) or 1
    return len(_completed(records)) / n


def _degenerate_rate(records: list[dict]) -> float:
    n = len(records) or 1
    return verdict_breakdown(records).get("degenerate", 0) / n


def _avg_ap_spread(records: list[dict]) -> float:
    vals = [
        r.get("ap_economy_stats", {}).get("avg_spread", 0.0)
        for r in _completed(records)
    ]
    return sum(vals) / len(vals) if vals else 0.0


def _max_ap_spread(records: list[dict]) -> float:
    vals = [
        r.get("ap_economy_stats", {}).get("max_spread", 0.0)
        for r in _completed(records)
    ]
    return max(vals) if vals else 0.0


def _mean_rounds(records: list[dict]) -> float:
    vals = [played_rounds(r) for r in _completed(records)]
    return sum(vals) / len(vals) if vals else 0.0


_METRICS = {
    "crash_rate": _crash_rate,
    "timeout_rate": _timeout_rate,
    "completed_rate": _completed_rate,
    "degenerate_rate": _degenerate_rate,
    "attacker_win_rate": lambda rs: combat_metrics(rs).get("attacker_win_rate", 0.0),
    "battles_per_player_round": lambda rs: combat_metrics(rs).get(
        "battles_per_player_round", 0.0
    ),
    "winner_lord_capture_share": lambda rs: winner_vp_source_mix(_completed(rs)).get(
        "lord_capture", 0.0
    ),
    "avg_ap_spread": _avg_ap_spread,
    "max_ap_spread": _max_ap_spread,
    "avg_action_gap": lambda rs: ap_economy_metrics(rs).get("avg_action_gap", 0.0),
    "max_action_gap": lambda rs: ap_economy_metrics(rs).get("max_action_gap", 0.0),
    "actions_per_player_round": lambda rs: ap_economy_metrics(rs).get(
        "actions_per_player_round", 0.0
    ),
    "stranded_ap_per_player_round": lambda rs: ap_economy_metrics(rs).get(
        "stranded_ap_per_player_round", 0.0
    ),
    "builds_per_player_game": lambda rs: ap_economy_metrics(rs).get(
        "builds_per_player_game", 0.0
    ),
    "upkeep_checks_per_player_round": lambda rs: bookkeeping_metrics(rs).get(
        "upkeep_checks_per_player_round", 0.0
    ),
    "mean_rounds": _mean_rounds,
    "contested_attacker_win_rate": lambda rs: combat_metrics(rs).get(
        "contested_attacker_win_rate", 0.0
    ),
}


def evaluate_regression(records: list[dict], gates: list[dict]) -> list[dict]:
    """Return list of failures: {metric, value, gate, message}."""
    failures = []
    for gate in gates:
        metric = gate["metric"]
        fn = _METRICS.get(metric)
        if fn is None:
            failures.append({
                "metric": metric,
                "value": None,
                "gate": gate,
                "message": f"unknown regression metric: {metric}",
            })
            continue
        value = fn(records)
        label = gate.get("label", metric)
        if "min" in gate and value < gate["min"]:
            failures.append({
                "metric": metric,
                "value": value,
                "gate": gate,
                "message": f"{label}: {value:.4f} < min {gate['min']}",
            })
        if "max" in gate and value > gate["max"]:
            failures.append({
                "metric": metric,
                "value": value,
                "gate": gate,
                "message": f"{label}: {value:.4f} > max {gate['max']}",
            })
    return failures


def regression_markdown(
    records: list[dict], gates: list[dict], failures: list[dict]
) -> str:
    lines = ["## Regression gates", ""]
    lines.append("| Metric | Value | Min | Max | Status |")
    lines.append("| --- | ---: | ---: | ---: | --- |")
    fail_metrics = {f["metric"] for f in failures}
    for gate in gates:
        metric = gate["metric"]
        value = _METRICS[metric](records)
        lo = gate.get("min", "")
        hi = gate.get("max", "")
        status = "**FAIL**" if metric in fail_metrics else "pass"
        lines.append(
            f"| {gate.get('label', metric)} | {value:.4f} | {lo} | {hi} | {status} |"
        )
    if failures:
        lines.append("")
        lines.append("### Failures")
        for f in failures:
            lines.append(f"- {f['message']}")
    return "\n".join(lines) + "\n"
