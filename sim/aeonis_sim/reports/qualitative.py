"""Qualitative M5 playtest report generation."""
from __future__ import annotations

import json
from pathlib import Path


def _text(value) -> str:
    return str(value or "").strip() or "None reported."


def _sentence(value) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    return text if text.endswith((".", "!", "?")) else text + "."


def qualitative_report(records: list[dict], title: str = "Aeonis Agent Playtest Report") -> str:
    entries = []
    for record in records:
        for seat, payload in sorted(
            record.get("agent_playtest", {}).get("seats", {}).items(),
            key=lambda item: int(item[0]),
        ):
            entries.append((record, str(seat), payload))

    providers = sorted({payload.get("provider", "unknown") for _, _, payload in entries})
    deterministic_only = bool(entries) and providers == ["deterministic"]
    lines = [
        f"# {title}",
        "",
        f"Games: **{len(records)}** · Qualitative seats: **{len(entries)}** · Providers: "
        + (", ".join(providers) if providers else "none"),
        "",
    ]
    if deterministic_only:
        lines.extend([
            "> **Pipeline dry run only.** The deterministic provider validates orchestration and artifacts; "
            "its comments are not playtest evidence.",
            "",
        ])
    lines.extend([
        "## Game facts",
        "",
        "| Seed | Rounds | Final VP | Battles (attacker wins) | Council passed/proposed | Deals accepted/proposed |",
        "| ---: | ---: | --- | ---: | ---: | ---: |",
    ])
    for record in records:
        combat = record.get("combat_stats", {})
        council = record.get("council_stats", {})
        negotiation = record.get("negotiation_stats", {})
        lines.append(
            f"| {record.get('seed')} | {record.get('rounds')} | {record.get('final_vp')} "
            f"| {combat.get('battles', 0)} ({combat.get('attacker_wins', 0)}) "
            f"| {council.get('motions_passed', 0)}/{council.get('motions_proposed', 0)} "
            f"| {negotiation.get('offers_accepted', 0)}/{negotiation.get('offers_proposed', 0)} |"
        )
    lines.extend([
        "",
        "> Treat one-game and low-battle observations as prompts for replication, not balance conclusions.",
        "",
    ])
    lines.extend([
        "## Reliability",
        "",
        "| Seat-game | Provider calls | Decision attempts | Valid decisions | Persona delegations | Retries | Decision fallbacks | Qualitative failures | Model seconds |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for record, seat, payload in entries:
        stats = payload.get("stats", {})
        lines.append(
            f"| seed {record.get('seed')} / seat {seat} ({payload.get('persona', 'unknown')}) "
            f"| {stats.get('provider_calls', 0)} | {stats.get('model_decision_attempts', 0)} "
            f"| {stats.get('model_decisions', 0)} "
            f"| {stats.get('persona_delegations', 0)} | {stats.get('retries', 0)} "
            f"| {stats.get('fallbacks', 0)} "
            f"| {stats.get('reflection_failures', 0) + stats.get('interview_failures', 0)} "
            f"| {stats.get('provider_seconds', 0)} |"
        )

    diagnostics = [
        (record, seat, error)
        for record, seat, payload in entries
        for error in payload.get("errors", [])
    ]
    lines.extend(["", "### Provider diagnostics", ""])
    if diagnostics:
        for record, seat, error in diagnostics:
            lines.append(
                f"- Seed {record.get('seed')}, seat {seat}, {error.get('stage', 'unknown')}: "
                f"`{_text(error.get('error'))}`"
            )
    else:
        lines.append("- No provider errors recorded.")

    lines.extend(["", "## Round reflections", ""])
    reflection_count = 0
    for record, seat, payload in entries:
        for reflection in payload.get("round_reflections", []):
            reflection_count += 1
            if reflection.get("fallback"):
                lines.append(
                    f"- Seed {record.get('seed')}, seat {seat}, round {reflection.get('round')}: "
                    f"failed safely (`{_text(reflection.get('error'))}`)."
                )
                continue
            lines.append(
                f"- Seed {record.get('seed')}, seat {seat}, round {reflection.get('round')}: "
                f"{_text(reflection.get('summary'))} Highlight: {_text(reflection.get('highlight'))} "
                f"Friction: {_text(reflection.get('frustration'))}"
            )
    if not reflection_count:
        lines.append("- No round reflections requested.")

    lines.extend(["", "## Negotiation transcript", ""])
    dialogue_count = 0
    for record in records:
        for entry in record.get("negotiation_dialogue", []):
            dialogue_count += 1
            terms = entry.get("authoritative_terms")
            terms_suffix = (
                " Terms: `" + json.dumps(terms, sort_keys=True) + "`."
                if terms and any(terms.values()) else ""
            )
            lines.append(
                f"- Seed {record.get('seed')}, round {entry.get('round')}, seat "
                f"{entry.get('speaker')} ({entry.get('choice_type')}, "
                f"{entry.get('deal_kind') or 'unspecified'}): {_text(entry.get('message'))}"
                f"{terms_suffix}"
            )
    if not dialogue_count:
        lines.append("- No model-authored negotiation dialogue recorded.")

    lines.extend(["", "### Promise outcomes", ""])
    promise_count = 0
    for record in records:
        for promise in record.get("promises_log", []):
            promise_count += 1
            status = "unresolved" if promise.get("kept") is None else (
                "kept" if promise.get("kept") else "broken"
            )
            lines.append(
                f"- Seed {record.get('seed')}: {promise.get('kind')} from seat "
                f"{promise.get('from')} to seat {promise.get('to')} — {status} "
                f"({promise.get('resolution', 'game still in progress')})."
            )
    if not promise_count:
        lines.append("- No accepted future promises recorded.")

    lines.extend(["", "## Exit interviews", ""])
    interview_fields = (
        ("Pacing", "pacing"), ("Map flow", "map_flow"), ("Politics", "politics"),
        ("Combat", "combat"), ("Economy pressure", "economy_pressure"),
        ("Best moment", "best_moment"), ("Biggest friction", "biggest_friction"),
    )
    for record, seat, payload in entries:
        interview = payload.get("exit_interview", {})
        lines.extend([
            f"### Seed {record.get('seed')} · Seat {seat} · {payload.get('persona', 'unknown')}",
            "",
        ])
        if interview.get("fallback"):
            lines.extend([f"- Interview failed safely: `{_text(interview.get('error'))}`", ""])
            continue
        for label, key in interview_fields:
            lines.append(f"- **{label}:** {_text(interview.get(key))}")
        lines.append(f"- **Would play again:** {'Yes' if interview.get('play_again') else 'No'}")
        hypotheses = interview.get("hypotheses", [])
        if hypotheses:
            lines.append("- **Hypotheses:** " + " | ".join(_text(x) for x in hypotheses))
        lines.append("")

    questions = []
    for record, seat, payload in entries:
        for annotation in payload.get("annotations", []):
            question = str(annotation.get("rules_question") or "").strip()
            if question and question.lower().rstrip(".") not in {"none", "no", "n/a"}:
                questions.append((record.get("seed"), seat, annotation.get("round"), question))
        for reflection in payload.get("round_reflections", []):
            question = str(reflection.get("rules_question") or "").strip()
            if question and question.lower().rstrip(".") not in {"none", "no", "n/a"}:
                questions.append((record.get("seed"), seat, reflection.get("round"), question))
        for question in payload.get("exit_interview", {}).get("rules_questions", []):
            cleaned = str(question).strip()
            if cleaned and cleaned.lower().rstrip(".") not in {"none", "no", "n/a"}:
                questions.append((record.get("seed"), seat, "post-game", cleaned))
    lines.extend([
        "## Candidate rules questions",
        "",
        "These are triage inputs, not automatic canon or Ambiguity Ledger entries.",
        "",
    ])
    if questions:
        for seed, seat, round_no, question in questions:
            lines.append(f"- Seed {seed}, seat {seat}, round {round_no}: {question}")
    else:
        lines.append("- None reported.")

    lines.extend(["", "## Decision moments", ""])
    moment_count = 0
    for record, seat, payload in entries:
        for annotation in payload.get("annotations", []):
            if annotation.get("fallback"):
                continue
            highlight = str(annotation.get("highlight") or "").strip()
            frustration = str(annotation.get("frustration") or "").strip()
            if not highlight and not frustration:
                continue
            moment_count += 1
            details = []
            if highlight:
                details.append(f"highlight={_sentence(highlight)}")
            if frustration:
                details.append(f"friction={_sentence(frustration)}")
            lines.append(
                f"- Seed {record.get('seed')}, seat {seat}, round {annotation.get('round')} "
                f"({annotation.get('decision_kind')}): " + " ".join(details)
            )
    if not moment_count:
        lines.append("- None reported.")
    lines.extend([
        "",
        "---",
        "",
        "Model feedback is directional sim-only evidence. It does not replace human table play or promote rules to canon.",
        "",
    ])
    return "\n".join(lines)


def save_qualitative_report(records: list[dict], path: str | Path, title: str = "Aeonis Agent Playtest Report") -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(qualitative_report(records, title), encoding="utf-8")
