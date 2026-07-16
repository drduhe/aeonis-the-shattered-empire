"""Structured negotiation with binding exchanges and non-binding promises.

Diplomacy.md section 1 makes an immediate legal exchange binding while future
conduct remains a promise.  The simulator therefore treats prose as table talk
and these typed terms as the authoritative offer.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .types import GameState


RESOURCE_KEYS = ("gold", "mana", "influence", "remnants")
PROMISE_KINDS = ("vote", "non_aggression", "attack_target", "future_payment")


def empty_bundle() -> dict[str, int]:
    return {key: 0 for key in RESOURCE_KEYS}


def normalize_bundle(raw: dict | None) -> dict[str, int]:
    raw = raw or {}
    return {key: max(0, int(raw.get(key, 0))) for key in RESOURCE_KEYS}


def bundle_nonempty(bundle: dict) -> bool:
    return any(bundle.get(key, 0) > 0 for key in RESOURCE_KEYS)


def _player_bundle(state: GameState, pid: int) -> dict[str, int]:
    player = state.player(pid)
    return {key: int(getattr(player, key)) for key in RESOURCE_KEYS}


def can_afford(state: GameState, pid: int, bundle: dict) -> bool:
    have = _player_bundle(state, pid)
    return all(have[key] >= bundle.get(key, 0) for key in RESOURCE_KEYS)


def normalize_promises(
    raw: list | None,
    *,
    proposer: int,
    target: int,
    motion: Optional[str],
    round_num: int,
    player_count: int,
) -> list[dict]:
    """Normalize supported future promises without changing their parties."""
    out: list[dict] = []
    parties = {proposer, target}
    for item in raw or []:
        kind = str(item.get("kind", ""))
        if kind not in PROMISE_KINDS:
            continue
        from_pid = int(item.get("from", target))
        to_pid = int(item.get("to", proposer))
        if from_pid not in parties or to_pid not in parties or from_pid == to_pid:
            continue
        promise = {"kind": kind, "from": from_pid, "to": to_pid}
        if kind == "vote":
            promise.update({
                "motion": item.get("motion", motion),
                "support": bool(item.get("support", True)),
            })
            if not promise["motion"]:
                continue
        elif kind == "non_aggression":
            promise["through_round"] = max(
                round_num, int(item.get("through_round", round_num + 1)),
            )
        elif kind == "attack_target":
            attack_target = int(item.get("target", -1))
            if attack_target < 0 or attack_target >= player_count or attack_target in parties:
                continue
            promise.update({
                "target": attack_target,
                "through_round": max(
                    round_num, int(item.get("through_round", round_num + 1)),
                ),
            })
        elif kind == "future_payment":
            resource = str(item.get("resource", "gold"))
            amount = int(item.get("amount", 0))
            if resource not in RESOURCE_KEYS or amount <= 0:
                continue
            promise.update({
                "resource": resource,
                "amount": amount,
                "due_round": max(round_num, int(item.get("due_round", round_num + 1))),
            })
        out.append(promise)
    return out


def validate_offer(
    state: GameState,
    proposer: int,
    target: int,
    gives: dict,
    gets: dict,
    promises: list | None = None,
) -> Optional[str]:
    """Return an error string when an offer is illegal, otherwise ``None``."""
    if proposer == target:
        return "cannot negotiate with self"
    if proposer < 0 or target < 0 or proposer >= len(state.players) or target >= len(state.players):
        return "invalid seat"
    giving = normalize_bundle(gives)
    receiving = normalize_bundle(gets)
    normalized_promises = normalize_promises(
        promises,
        proposer=proposer,
        target=target,
        motion=None,
        round_num=state.round,
        player_count=len(state.players),
    )
    if not bundle_nonempty(giving) and not bundle_nonempty(receiving) and not normalized_promises:
        return "empty offer"
    if not can_afford(state, proposer, giving):
        return "proposer cannot afford gives"
    if not can_afford(state, target, receiving):
        return "target cannot afford gets"
    return None


def execute_transfer(
    state: GameState,
    proposer: int,
    target: int,
    gives: dict,
    gets: dict,
) -> None:
    """Execute the binding component portion of an accepted offer."""
    giving = normalize_bundle(gives)
    receiving = normalize_bundle(gets)
    if not bundle_nonempty(giving) and not bundle_nonempty(receiving):
        return
    if not can_afford(state, proposer, giving):
        raise ValueError("proposer cannot afford gives")
    if not can_afford(state, target, receiving):
        raise ValueError("target cannot afford gets")
    pp = state.player(proposer)
    tp = state.player(target)
    for key in RESOURCE_KEYS:
        setattr(pp, key, getattr(pp, key) - giving[key] + receiving[key])
        setattr(tp, key, getattr(tp, key) + giving[key] - receiving[key])


@dataclass
class NegotiationSession:
    window: str  # council | trade
    proposer: int
    target: int
    gives: dict = field(default_factory=empty_bundle)
    gets: dict = field(default_factory=empty_bundle)
    promises: list[dict] = field(default_factory=list)
    deal_kind: str = "resource_trade"
    phase: str = "respond"  # respond | counter_review
    countered: bool = False
    counter_proposer: Optional[int] = None
    motion: Optional[str] = None
    dialogue: list[dict] = field(default_factory=list)


def _mark_promise(pr: dict, kept: bool, stats: dict, reason: str) -> None:
    if pr.get("kept") is not None:
        return
    pr["kept"] = kept
    pr["resolution"] = reason
    result = "kept" if kept else "broken"
    stats[f"promises_{result}"] = stats.get(f"promises_{result}", 0) + 1
    kind = pr.get("kind", "unknown")
    stats[f"{kind}_promises_{result}"] = stats.get(
        f"{kind}_promises_{result}", 0,
    ) + 1


def record_promises(
    promises: list[dict],
    *,
    round_num: int,
    log: list[dict],
    stats: dict,
) -> None:
    for promise in promises:
        logged = {**promise, "round": round_num, "kept": None}
        log.append(logged)
        kind = promise["kind"]
        stats[f"{kind}_promises_made"] = stats.get(
            f"{kind}_promises_made", 0,
        ) + 1


def check_vote_promises(
    promises_log: list[dict], pid: int, motion: str, support: bool, stats: dict,
) -> None:
    for promise in promises_log:
        if (
            promise.get("kept") is None
            and promise.get("kind") == "vote"
            and promise.get("from") == pid
            and promise.get("motion") == motion
        ):
            expected = bool(promise.get("support", True))
            _mark_promise(promise, support == expected, stats, "vote_cast")


def check_attack_promises(
    promises_log: list[dict], attacker: int, defender: int, round_num: int, stats: dict,
) -> None:
    """Resolve promises implicated by a declared attack."""
    for promise in promises_log:
        if promise.get("kept") is not None or promise.get("from") != attacker:
            continue
        if promise.get("kind") == "non_aggression":
            if promise.get("to") == defender and round_num <= promise.get("through_round", 0):
                _mark_promise(promise, False, stats, "attacked_protected_player")
        elif promise.get("kind") == "attack_target":
            if promise.get("target") == defender and round_num <= promise.get("through_round", 0):
                _mark_promise(promise, True, stats, "declared_promised_attack")


def check_payment_promises(
    promises_log: list[dict],
    payer: int,
    recipient: int,
    paid: dict,
    round_num: int,
    stats: dict,
) -> None:
    for promise in promises_log:
        if (
            promise.get("kept") is None
            and promise.get("kind") == "future_payment"
            and promise.get("from") == payer
            and promise.get("to") == recipient
            and round_num <= promise.get("due_round", 0)
            and paid.get(promise.get("resource"), 0) >= promise.get("amount", 0)
        ):
            _mark_promise(promise, True, stats, "payment_transferred")


def expire_promises(promises_log: list[dict], completed_round: int, stats: dict) -> None:
    """Resolve promises whose final opportunity has passed at Cleanup & Checks."""
    for promise in promises_log:
        if promise.get("kept") is not None:
            continue
        kind = promise.get("kind")
        if kind == "non_aggression" and promise.get("through_round", 0) <= completed_round:
            _mark_promise(promise, True, stats, "term_expired_without_attack")
        elif kind == "attack_target" and promise.get("through_round", 0) <= completed_round:
            _mark_promise(promise, False, stats, "attack_not_declared")
        elif kind == "future_payment" and promise.get("due_round", 0) <= completed_round:
            _mark_promise(promise, False, stats, "payment_not_transferred")
        elif kind == "vote" and promise.get("round", 0) <= completed_round:
            _mark_promise(promise, False, stats, "promised_vote_not_cast")


def active_promises_for(promises_log: list[dict], pid: int) -> list[dict]:
    return [
        dict(promise) for promise in promises_log
        if promise.get("kept") is None
        and (promise.get("from") == pid or promise.get("to") == pid)
    ]


def _template_offers(state: GameState, proposer: int, target: int) -> list[tuple[dict, dict]]:
    templates: list[tuple[dict, dict]] = []
    p = state.player(proposer)
    t = state.player(target)
    if p.gold >= 1 and t.mana >= 1:
        templates.append(({"gold": 1}, {"mana": 1}))
    if p.mana >= 1 and t.gold >= 1:
        templates.append(({"mana": 1}, {"gold": 1}))
    if p.influence >= 1 and t.gold >= 1:
        templates.append(({"influence": 1}, {"gold": 1}))
    if p.remnants >= 1 and t.gold >= 1:
        templates.append(({"remnants": 1}, {"gold": 1}))
    if p.gold >= 2:
        templates.append(({"gold": 2}, {}))
    if p.gold >= 1:
        templates.append(({"gold": 1}, {}))
    return templates


def _promise(
    kind: str, from_pid: int, to_pid: int, state: GameState, **extra,
) -> dict:
    return {"kind": kind, "from": from_pid, "to": to_pid, **extra}


def enumerate_council_negotiation(
    state: GameState, pid: int, *, motion: str, session: Optional[NegotiationSession],
) -> list[dict]:
    if session is not None:
        return _enumerate_session_choices(state, session, pid)
    choices: list[dict] = [{"type": "negotiation_skip"}]
    for other in range(len(state.players)):
        if other == pid:
            continue
        vote = _promise("vote", other, pid, state, motion=motion, support=True)
        future_pay = _promise(
            "future_payment", pid, other, state,
            resource="gold", amount=1, due_round=state.round + 1,
        )
        for promises, kind in (([vote], "vote_agreement"), ([vote, future_pay], "vote_bargain")):
            choices.append({
                "type": "negotiation_propose",
                "deal_kind": kind,
                "target": other,
                "gives": {},
                "gets": {},
                "promises": promises,
            })
    return choices


def enumerate_trade_starts(state: GameState, pid: int) -> list[dict]:
    choices: list[dict] = []
    for other in range(len(state.players)):
        if other == pid:
            continue
        for gives, gets in _template_offers(state, pid, other):
            choices.append({
                "type": "trade", "deal_kind": "resource_trade", "target": other,
                "gives": gives, "gets": gets, "promises": [],
            })
        if state.player(pid).gold >= 1:
            choices.append({
                "type": "trade", "deal_kind": "protection_payment", "target": other,
                "gives": {"gold": 1}, "gets": {},
                "promises": [_promise(
                    "non_aggression", other, pid, state,
                    through_round=state.round + 1,
                )],
            })
        choices.append({
            "type": "trade", "deal_kind": "mutual_non_aggression", "target": other,
            "gives": {}, "gets": {},
            "promises": [
                _promise("non_aggression", pid, other, state, through_round=state.round + 1),
                _promise("non_aggression", other, pid, state, through_round=state.round + 1),
            ],
        })
        third = next((x for x in range(len(state.players)) if x not in (pid, other)), None)
        if third is not None and state.player(pid).gold >= 1:
            choices.append({
                "type": "trade", "deal_kind": "attack_contract", "target": other,
                "gives": {"gold": 1}, "gets": {},
                "promises": [_promise(
                    "attack_target", other, pid, state,
                    target=third, through_round=state.round + 1,
                )],
            })
    return [
        choice for choice in choices
        if validate_offer(
            state, pid, int(choice["target"]), choice["gives"], choice["gets"],
            choice["promises"],
        ) is None
    ]


def enumerate_trade_negotiation(
    state: GameState, pid: int, *, session: Optional[NegotiationSession],
) -> list[dict]:
    if session is not None:
        return _enumerate_session_choices(state, session, pid)
    return [{"type": "negotiation_skip"}]


def _enumerate_session_choices(
    state: GameState, session: NegotiationSession, pid: int,
) -> list[dict]:
    if session.phase == "respond" and pid == session.target:
        choices = [
            {"type": "negotiation_reject"},
            {"type": "negotiation_accept"},
        ]
        if not session.countered:
            for gives, gets in _template_offers(state, session.target, session.proposer)[:2]:
                if validate_offer(state, session.target, session.proposer, gives, gets) is None:
                    choices.append({
                        "type": "negotiation_counter",
                        "deal_kind": "resource_trade",
                        "gives": gives,
                        "gets": gets,
                        "promises": [],
                    })
        return choices
    if session.phase == "counter_review" and pid == session.proposer:
        return [
            {"type": "negotiation_reject"},
            {"type": "negotiation_accept"},
        ]
    return [{"type": "negotiation_skip"}]


def start_session(
    *, window: str, proposer: int, target: int, gives: dict, gets: dict,
    promises: list | None, motion: Optional[str], state: GameState,
    deal_kind: str = "resource_trade",
) -> NegotiationSession:
    return NegotiationSession(
        window=window,
        proposer=proposer,
        target=target,
        gives=normalize_bundle(gives),
        gets=normalize_bundle(gets),
        promises=normalize_promises(
            promises,
            proposer=proposer,
            target=target,
            motion=motion,
            round_num=state.round,
            player_count=len(state.players),
        ),
        deal_kind=deal_kind,
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
    """Apply accept/reject/counter and return the still-open session, if any."""
    choice_type = choice["type"]
    if choice_type == "negotiation_reject":
        stats["offers_rejected"] = stats.get("offers_rejected", 0) + 1
        return None, "rejected"
    if choice_type == "negotiation_accept":
        if session.phase == "counter_review":
            payer = session.counter_proposer if session.counter_proposer is not None else session.target
            recipient = session.proposer
        else:
            payer = session.proposer
            recipient = session.target
        execute_transfer(state, payer, recipient, session.gives, session.gets)
        check_payment_promises(
            promises_log, payer, recipient, normalize_bundle(session.gives), state.round, stats,
        )
        check_payment_promises(
            promises_log, recipient, payer, normalize_bundle(session.gets), state.round, stats,
        )
        record_promises(
            session.promises, round_num=state.round, log=promises_log, stats=stats,
        )
        stats["offers_accepted"] = stats.get("offers_accepted", 0) + 1
        return None, "accepted"
    if choice_type == "negotiation_counter" and session.phase == "respond" and not session.countered:
        session.gives = normalize_bundle(choice.get("gives"))
        session.gets = normalize_bundle(choice.get("gets"))
        session.promises = normalize_promises(
            choice.get("promises"),
            proposer=session.target,
            target=session.proposer,
            motion=session.motion,
            round_num=state.round,
            player_count=len(state.players),
        )
        session.deal_kind = str(choice.get("deal_kind", "resource_trade"))
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
    """Net utility of the binding resource exchange from the recipient's view."""
    giving = normalize_bundle(gives)
    receiving = normalize_bundle(gets)
    values = {"gold": 0.15, "mana": 0.12, "influence": 0.1, "remnants": 0.18}
    net = {key: giving[key] - receiving[key] for key in RESOURCE_KEYS}
    score = persona_weights.get("economy", 1.0) * sum(
        net[key] * values[key] for key in RESOURCE_KEYS
    )
    if sum(net.values()) < 0:
        score -= 2.0
    player = state.player(recipient)
    max_opp = max(
        state.player(i).vp for i in range(len(state.players)) if i != recipient
    )
    if player.vp < max_opp and net["gold"] + net["mana"] > 0:
        score += persona_weights.get("catch_up", 0.5) * 0.3
    return -99.0 if recipient == proposer else score
