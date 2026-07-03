"""Structured negotiation — binding resource trades and tracked promises.

Per simulation design §6 and Diplomacy.md §1: immediate resource exchanges are
binding; future vote / non-aggression promises are tracked for metrics only.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .types import GameState

RESOURCE_KEYS = ("gold", "mana", "influence", "population")


def empty_bundle() -> dict[str, int]:
    return {k: 0 for k in RESOURCE_KEYS}


def normalize_bundle(raw: dict | None) -> dict[str, int]:
    raw = raw or {}
    return {k: max(0, int(raw.get(k, 0))) for k in RESOURCE_KEYS}


def bundle_nonempty(bundle: dict) -> bool:
    return any(bundle.get(k, 0) > 0 for k in RESOURCE_KEYS)


def _player_bundle(state: GameState, pid: int) -> dict[str, int]:
    p = state.player(pid)
    return {
        "gold": p.gold,
        "mana": p.mana,
        "influence": p.influence,
        "population": p.pop_pool,
    }


def can_afford(state: GameState, pid: int, bundle: dict) -> bool:
    have = _player_bundle(state, pid)
    return all(have[k] >= bundle.get(k, 0) for k in RESOURCE_KEYS)


def validate_offer(
    state: GameState,
    proposer: int,
    target: int,
    gives: dict,
    gets: dict,
) -> Optional[str]:
    """Return error string if illegal, else None."""
    if proposer == target:
        return "cannot negotiate with self"
    if proposer < 0 or target < 0 or proposer >= len(state.players):
        return "invalid seat"
    if target >= len(state.players):
        return "invalid seat"
    g = normalize_bundle(gives)
    r = normalize_bundle(gets)
    if not bundle_nonempty(g) and not bundle_nonempty(r):
        return "empty offer"
    if not can_afford(state, proposer, g):
        return "proposer cannot afford gives"
    if not can_afford(state, target, r):
        return "target cannot afford gets"
    return None


def execute_transfer(
    state: GameState,
    proposer: int,
    target: int,
    gives: dict,
    gets: dict,
) -> None:
    """Binding exchange: proposer pays gives, receives gets from target."""
    err = validate_offer(state, proposer, target, gives, gets)
    if err:
        raise ValueError(err)
    g = normalize_bundle(gives)
    r = normalize_bundle(gets)
    pp = state.player(proposer)
    tp = state.player(target)
    for k in RESOURCE_KEYS:
        attr = "pop_pool" if k == "population" else k
        gv, rv = g[k], r[k]
        setattr(pp, attr, getattr(pp, attr) - gv + rv)
        setattr(tp, attr, getattr(tp, attr) + gv - rv)


@dataclass
class NegotiationSession:
    window: str  # council | trade
    proposer: int
    target: int
    gives: dict = field(default_factory=empty_bundle)
    gets: dict = field(default_factory=empty_bundle)
    promises: list = field(default_factory=list)
    phase: str = "respond"  # respond | counter_review
    countered: bool = False
    counter_proposer: Optional[int] = None
    motion: Optional[str] = None


def normalize_promises(raw: list | None, proposer: int, motion: Optional[str]) -> list[dict]:
    out: list[dict] = []
    for item in raw or []:
        if item.get("kind") != "vote":
            continue
        out.append({
            "kind": "vote",
            "from": proposer,
            "motion": item.get("motion", motion),
            "support": bool(item.get("support", True)),
        })
    return out


def record_promises(
    promises: list[dict],
    *,
    proposer: int,
    target: int,
    motion: Optional[str],
    round_num: int,
    log: list[dict],
) -> None:
    for pr in promises:
        log.append({
            **pr,
            "from": proposer,
            "to": target,
            "motion": pr.get("motion", motion),
            "round": round_num,
            "kept": None,
        })


def check_vote_promises(
    promises_log: list[dict],
    pid: int,
    motion: str,
    support: bool,
    stats: dict,
) -> None:
    for pr in promises_log:
        if pr.get("kept") is not None:
            continue
        if pr.get("from") != pid or pr.get("motion") != motion:
            continue
        expected = bool(pr.get("support", True))
        pr["kept"] = support == expected
        if pr["kept"]:
            stats["promises_kept"] = stats.get("promises_kept", 0) + 1
        else:
            stats["promises_broken"] = stats.get("promises_broken", 0) + 1


def _template_offers(state: GameState, proposer: int, target: int) -> list[tuple[dict, dict]]:
    """Small affordable offer templates for bot enumeration."""
    templates: list[tuple[dict, dict]] = []
    p = state.player(proposer)
    t = state.player(target)
    if p.gold >= 1 and t.mana >= 1:
        templates.append(({"gold": 1}, {"mana": 1}))
    if p.mana >= 1 and t.gold >= 1:
        templates.append(({"mana": 1}, {"gold": 1}))
    if p.gold >= 2:
        templates.append(({"gold": 2}, {}))
    if p.influence >= 2 and t.influence >= 1:
        templates.append(({"influence": 2}, {"influence": 1}))
    if p.gold >= 1:
        templates.append(({"gold": 1}, {}))
    return templates


def enumerate_council_negotiation(
    state: GameState,
    pid: int,
    *,
    motion: str,
    session: Optional[NegotiationSession],
) -> list[dict]:
    if session is not None:
        return _enumerate_session_choices(state, session, pid)
    choices: list[dict] = [{"type": "negotiation_skip"}]
    for other in range(len(state.players)):
        if other == pid:
            continue
        for gives, gets in _template_offers(state, pid, other):
            prom = []
            if motion:
                prom = [{"kind": "vote", "motion": motion, "support": True}]
            offer = {
                "type": "negotiation_propose",
                "target": other,
                "gives": gives,
                "gets": gets,
                "promises": prom,
            }
            if validate_offer(state, pid, other, gives, gets) is None:
                choices.append(offer)
    return choices


def enumerate_trade_starts(state: GameState, pid: int) -> list[dict]:
    """Legal trade-action offers (1 AP) from pid to each opponent."""
    choices: list[dict] = []
    for other in range(len(state.players)):
        if other == pid:
            continue
        for gives, gets in _template_offers(state, pid, other):
            if validate_offer(state, pid, other, gives, gets) is None:
                choices.append({
                    "type": "trade",
                    "target": other,
                    "gives": gives,
                    "gets": gets,
                    "promises": [],
                })
    return choices


def enumerate_trade_negotiation(
    state: GameState,
    pid: int,
    *,
    session: Optional[NegotiationSession],
) -> list[dict]:
    if session is not None:
        return _enumerate_session_choices(state, session, pid)
    choices: list[dict] = [{"type": "negotiation_skip"}]
    for other in range(len(state.players)):
        if other == pid:
            continue
        for gives, gets in _template_offers(state, pid, other):
            offer = {
                "type": "negotiation_propose",
                "target": other,
                "gives": gives,
                "gets": gets,
                "promises": [],
            }
            if validate_offer(state, pid, other, gives, gets) is None:
                choices.append(offer)
    return choices


def _enumerate_session_choices(
    state: GameState,
    session: NegotiationSession,
    pid: int,
) -> list[dict]:
    if session.phase == "respond" and pid == session.target:
        choices: list[dict] = [
            {"type": "negotiation_reject"},
            {"type": "negotiation_accept"},
        ]
        if not session.countered:
            for gives, gets in _template_offers(state, session.target, session.proposer):
                if validate_offer(
                    state, session.target, session.proposer, gives, gets,
                ) is None:
                    choices.append({
                        "type": "negotiation_counter",
                        "gives": gives,
                        "gets": gets,
                    })
        return choices
    if session.phase == "counter_review" and pid == session.proposer:
        return [
            {"type": "negotiation_reject"},
            {"type": "negotiation_accept"},
        ]
    return [{"type": "negotiation_skip"}]


def start_session(
    *,
    window: str,
    proposer: int,
    target: int,
    gives: dict,
    gets: dict,
    promises: list | None,
    motion: Optional[str],
) -> NegotiationSession:
    return NegotiationSession(
        window=window,
        proposer=proposer,
        target=target,
        gives=normalize_bundle(gives),
        gets=normalize_bundle(gets),
        promises=normalize_promises(promises, proposer, motion),
        phase="respond",
        motion=motion,
    )


def apply_session_choice(
    state: GameState,
    session: NegotiationSession,
    choice: dict,
    *,
    promises_log: list[dict],
    stats: dict,
) -> tuple[Optional[NegotiationSession], str]:
    """Return (session or None if closed, outcome label)."""
    t = choice["type"]
    if t == "negotiation_reject":
        stats["offers_rejected"] = stats.get("offers_rejected", 0) + 1
        return None, "rejected"
    if t == "negotiation_accept":
        if session.phase == "counter_review":
            cp = session.counter_proposer if session.counter_proposer is not None else session.target
            execute_transfer(state, cp, session.proposer, session.gives, session.gets)
            record_promises(
                session.promises,
                proposer=cp,
                target=session.proposer,
                motion=session.motion,
                round_num=state.round,
                log=promises_log,
            )
        else:
            execute_transfer(state, session.proposer, session.target, session.gives, session.gets)
            record_promises(
                session.promises,
                proposer=session.proposer,
                target=session.target,
                motion=session.motion,
                round_num=state.round,
                log=promises_log,
            )
        stats["offers_accepted"] = stats.get("offers_accepted", 0) + 1
        return None, "accepted"
    if t == "negotiation_counter" and session.phase == "respond" and not session.countered:
        session.gives = normalize_bundle(choice.get("gives"))
        session.gets = normalize_bundle(choice.get("gets"))
        session.countered = True
        session.phase = "counter_review"
        session.counter_proposer = session.target
        stats["counters"] = stats.get("counters", 0) + 1
        return session, "countered"
    raise ValueError(f"illegal negotiation choice in phase {session.phase}: {choice}")


def offer_value_for_recipient(
    state: GameState,
    recipient: int,
    proposer: int,
    gives: dict,
    gets: dict,
    persona_weights: dict[str, float],
) -> float:
    """Net utility of accepting from recipient's view (sim-only)."""
    g = normalize_bundle(gives)
    r = normalize_bundle(gets)
    # Recipient receives proposer's gives and pays gets.
    recv = {
        "gold": g["gold"] - r["gold"],
        "mana": g["mana"] - r["mana"],
        "influence": g["influence"] - r["influence"],
    }
    score = 0.0
    score += persona_weights.get("economy", 1.0) * recv["gold"] * 0.15
    score += persona_weights.get("economy", 1.0) * recv["mana"] * 0.12
    score += persona_weights.get("economy", 1.0) * recv["influence"] * 0.1
    if recv["gold"] + recv["mana"] + recv["influence"] < 0:
        score -= 2.0
    # Slight bonus if behind on VP
    p = state.player(recipient)
    max_opp = max(state.player(i).vp for i in range(len(state.players)) if i != recipient)
    if p.vp < max_opp and recv["gold"] + recv["mana"] > 0:
        score += persona_weights.get("catch_up", 0.5) * 0.3
    if recipient == proposer:
        score = -99.0
    return score
