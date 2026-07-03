"""Heuristic persona bots for balance tournaments."""
from __future__ import annotations

import random

from ..engine.types import GameState
from .features import score_action

# Directional priors — sim-tuned 2026-07-03 (H7 persona parity); not canon.
PERSONA_WEIGHTS: dict[str, dict[str, float]] = {
    "warmonger": {
        "vp": 1.5, "vp_lead": 1.2, "combat": 2.5, "military": 1.8, "military_delta": 2.0,
        "next_military": 1.2, "expansion": 1.0, "seat": 0.5, "seat_pull": 0.4,
        "economy": 0.3, "economy_delta": 0.2, "objective": 1.4, "next_objective": 1.2,
        "pass_penalty": 1.5,
    },
    "economist": {
        "vp": 1.5, "vp_lead": 1.25, "next_vp": 2.0, "catch_up": 2.5,
        "economy": 2.0, "economy_delta": 4.0, "next_economy": 2.6,
        "builder_delta": 8.0, "builder_track": 3.0, "next_builder_track": 2.8,
        "builder_push": 3.5, "next_builder_push": 3.0,
        "production_bonus": 3.0,
        "gold_track": 2.5, "next_gold_track": 2.2,
        "builder_need": 4.0,
        "objective": 3.2, "next_objective": 3.0,
        "territory": 0.3, "expansion": 0.15, "combat": 0.1, "military": 0.2,
        "military_delta": -0.8, "pass_penalty": 1.6,
    },
    "expander": {
        "vp": 1.25, "vp_lead": -2.5, "next_vp_lead": -2.0,
        "territory": 0.7, "next_territory": 0.55, "expansion": 0.65,
        "territory_sat": -5.5, "next_territory_sat": -4.0,
        "seat": 0.55, "seat_pull": 0.55, "rite_ready": 0.55, "seat_streak": 0.45,
        "next_seat": 0.45,
        "objective": 2.1, "next_objective": 1.9, "combat": 0.45, "pass_penalty": 0.85,
    },
    "diplomat": {
        "vp": 1.25, "vp_lead": 1.0, "objective": 3.0, "next_objective": 2.5,
        "economy": 1.45, "territory": 0.7, "combat": 0.25, "military": 0.45,
        "pass_penalty": 0.85, "renown": 1.15, "catch_up": 1.1,
    },
    "balanced": {
        "vp": 1.25, "vp_lead": 1.05, "territory": 0.8, "seat": 0.95, "seat_pull": 0.9,
        "objective": 2.0, "next_objective": 1.85, "economy": 1.05, "economy_delta": 1.05,
        "military": 0.95, "military_delta": 0.95, "combat": 0.7, "expansion": 0.75,
        "pass_penalty": 0.95, "next_vp": 1.5, "next_territory": 0.5,
    },
}

PERSONA_NAMES = tuple(PERSONA_WEIGHTS.keys())


def _dot(weights: dict[str, float], feats: dict[str, float]) -> float:
    return sum(weights.get(k, 0.0) * v for k, v in feats.items())


# Post-multiply selected features per persona (sim-only).
PERSONA_FEATURE_BOOSTS: dict[str, dict[str, float]] = {
    "economist": {
        "builder_delta": 2.0,
        "next_builder_track": 1.5,
        "next_objective": 1.4,
        "production_bonus": 1.5,
    },
}


from ..engine.council import motion_vote_utility, persona_motion_adjustment
from ..engine.negotiation import offer_value_for_recipient, validate_offer
from ..engine.strategy import STRATEGY_CARDS


def _score_draft_choice(state: GameState, choice: dict, persona: str = "") -> float:
    card = STRATEGY_CARDS[choice["card"]]
    bounty = state.strategy_bounty.get(choice["card"], 0)
    tempo = 9 - card.initiative
    economy = 0.0
    card_id = choice["card"]
    if card_id == "resource_surge":
        economy = 2.5
    elif card_id == "economic_boom":
        economy = 2.0
    elif card_id == "military_maneuvers":
        economy = 0.5
    if persona == "economist" and card_id in ("economic_boom", "resource_surge"):
        economy += 2.5
    if persona == "expander" and card_id in ("expansion_strategy", "imperial_mandate"):
        tempo += 2.0
    if persona == "expander" and card_id == "military_maneuvers":
        tempo += 0.5
    return bounty * 10.0 + tempo + economy


def _score_strategy_choice(state: GameState, pid: int, choice: dict, persona: str = "") -> float:
    if choice["type"] == "strategy_primary":
        card_id = choice["card"]
        if persona == "economist":
            if card_id == "economic_boom":
                return 4.5
            if card_id == "resource_surge":
                return 4.0
        if persona == "expander":
            if card_id == "military_maneuvers":
                return 3.5
            if card_id == "resource_surge":
                return 2.5
        if card_id == "resource_surge":
            return 3.0
        if card_id == "economic_boom":
            return 2.5
        if card_id == "military_maneuvers":
            return 2.0
        return 1.0
    if choice["type"] == "strategy_secondary":
        return 1.5 if choice.get("use") else 0.0
    if choice["type"] in ("mm_skip_move", "mm_skip_attack"):
        return 0.0
    return 1.0


def _score_council_vote(
    state: GameState,
    pid: int,
    choice: dict,
    context: dict,
    persona: str,
) -> float:
    motion = context.get("motion", "")
    proposer = int(context.get("proposer", pid))
    util = motion_vote_utility(
        state,
        pid,
        motion,
        proposer,
        support=bool(choice.get("support")),
        lobby=int(choice.get("lobby", 0)),
    )
    util += persona_motion_adjustment(
        persona, motion, support=bool(choice.get("support")),
    )
    return util


def _score_council_propose(
    state: GameState,
    pid: int,
    choice: dict,
    context: dict,
    persona: str,
) -> float:
    if choice["type"] == "council_pass":
        return 0.55
    motion = choice.get("motion", context.get("agenda", ""))
    score = motion_vote_utility(
        state, pid, motion, pid, support=True, lobby=0,
    )
    score += persona_motion_adjustment(persona, motion, support=True)
    if persona == "diplomat":
        score += 0.6
    return score


def _score_negotiation_choice(
    state: GameState,
    pid: int,
    choice: dict,
    context: dict,
    persona: str,
) -> float:
    t = choice["type"]
    weights = PERSONA_WEIGHTS[persona]
    if t == "negotiation_skip":
        return 0.55 if persona != "diplomat" else 0.25
    if t == "negotiation_reject":
        return 0.65
    if t == "negotiation_accept":
        proposer = int(context.get("proposer", pid))
        gives = context.get("gives", {})
        gets = context.get("gets", {})
        if context.get("phase") == "counter_review":
            cp = int(context.get("target", proposer))
            val = offer_value_for_recipient(state, pid, cp, gives, gets, weights)
        else:
            val = offer_value_for_recipient(state, pid, proposer, gives, gets, weights)
        return val + (0.2 if persona == "diplomat" else 0.0)
    if t == "negotiation_propose":
        target = int(choice["target"])
        err = validate_offer(
            state, pid, target,
            choice.get("gives", {}), choice.get("gets", {}),
        )
        if err:
            return -10.0
        val = -offer_value_for_recipient(
            state, target, pid,
            choice.get("gives", {}), choice.get("gets", {}),
            weights,
        )
        if persona == "diplomat":
            val += 0.35
        if choice.get("promises"):
            val += 0.25 if persona == "diplomat" else 0.05
        return val
    if t == "negotiation_counter":
        proposer = int(context.get("proposer", pid))
        err = validate_offer(
            state, pid, proposer,
            choice.get("gives", {}), choice.get("gets", {}),
        )
        if err:
            return -10.0
        val = offer_value_for_recipient(
            state, pid, proposer,
            choice.get("gives", {}), choice.get("gets", {}),
            weights,
        )
        return val
    return 0.0


class PersonaBot:
    """Scores legal actions with persona-weighted features; deterministic tie-break."""

    def __init__(self, persona: str, seed: int):
        if persona not in PERSONA_WEIGHTS:
            raise ValueError(f"unknown persona: {persona}")
        self.persona = persona
        self.weights = PERSONA_WEIGHTS[persona]
        self.rng = random.Random(seed)

    def choose(self, observation: dict, decision_point) -> dict:
        state = GameState.from_dict(observation["state"])
        pid = observation["viewer"]
        if decision_point.kind == "strategy_draft":
            scored = [
                (_score_draft_choice(state, c, self.persona), c)
                for c in decision_point.choices
            ]
            best = max(s for s, _ in scored)
            top = [c for s, c in scored if abs(s - best) < 1e-9]
            return self.rng.choice(top)
        if decision_point.kind in ("strategy_primary", "strategy_secondary"):
            scored = [
                (_score_strategy_choice(state, pid, c, self.persona), c)
                for c in decision_point.choices
            ]
            best = max(s for s, _ in scored)
            top = [c for s, c in scored if abs(s - best) < 1e-9]
            return self.rng.choice(top)
        if decision_point.kind == "council_propose":
            scored = [
                (
                    _score_council_propose(
                        state, pid, c, decision_point.context, self.persona,
                    ),
                    c,
                )
                for c in decision_point.choices
            ]
            best = max(s for s, _ in scored)
            top = [c for s, c in scored if abs(s - best) < 1e-9]
            return self.rng.choice(top)
        if decision_point.kind == "council_vote":
            scored = [
                (
                    _score_council_vote(
                        state, pid, c, decision_point.context, self.persona,
                    ),
                    c,
                )
                for c in decision_point.choices
            ]
            best = max(s for s, _ in scored)
            top = [c for s, c in scored if abs(s - best) < 1e-9]
            return self.rng.choice(top)
        if decision_point.kind == "negotiation":
            scored = [
                (
                    _score_negotiation_choice(
                        state, pid, c, decision_point.context, self.persona,
                    ),
                    c,
                )
                for c in decision_point.choices
            ]
            best = max(s for s, _ in scored)
            top = [c for s, c in scored if abs(s - best) < 1e-9]
            return self.rng.choice(top)
        if decision_point.kind == "objective_draw":
            for c in decision_point.choices:
                if c["type"] == "obj_draw_secret":
                    return c
            for c in decision_point.choices:
                if c["type"] == "obj_keep":
                    return c
            for c in decision_point.choices:
                if c["type"] == "obj_discard":
                    return c
            return decision_point.choices[0]
        if decision_point.kind == "whisper_discard":
            return decision_point.choices[0]
        scored: list[tuple[float, dict]] = []
        for choice in decision_point.choices:
            feats = score_action(state, pid, choice, decision_point)
            for key, mul in PERSONA_FEATURE_BOOSTS.get(self.persona, {}).items():
                if key in feats:
                    feats[key] *= mul
            scored.append((_dot(self.weights, feats), choice))
        best = max(s for s, _ in scored)
        top = [c for s, c in scored if abs(s - best) < 1e-9]
        return self.rng.choice(top)
