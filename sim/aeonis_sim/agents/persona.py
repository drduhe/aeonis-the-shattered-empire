"""Heuristic persona bots for balance tournaments."""
from __future__ import annotations

import random

from ..engine.types import GameState
from .features import score_action

# Directional priors — revisit after Bracket A data, not canon.
PERSONA_WEIGHTS: dict[str, dict[str, float]] = {
    "warmonger": {
        "vp": 1.5, "vp_lead": 1.2, "combat": 3.0, "military": 2.0, "military_delta": 2.5,
        "next_military": 1.5, "expansion": 1.2, "seat": 0.5, "seat_pull": 0.4,
        "economy": 0.3, "economy_delta": 0.2, "objective": 0.6, "pass_penalty": 1.5,
    },
    "economist": {
        "vp": 1.2, "economy": 3.0, "economy_delta": 3.0, "next_economy": 2.0,
        "objective": 1.5, "next_objective": 1.2, "territory": 0.8, "combat": 0.2,
        "military": 0.5, "pass_penalty": 1.0,
    },
    "expander": {
        "vp": 1.3, "territory": 3.0, "next_territory": 2.5, "expansion": 3.0,
        "seat": 2.5, "seat_pull": 2.5, "rite_ready": 2.0, "seat_streak": 2.0, "next_seat": 2.0,
        "objective": 1.2, "combat": 1.0, "pass_penalty": 1.2,
    },
    "diplomat": {
        "vp": 1.0, "vp_lead": 0.8, "objective": 1.5, "economy": 1.2, "territory": 1.0,
        "combat": 0.4, "military": 0.6, "pass_penalty": 0.8, "renown": 1.0,
    },
    "balanced": {
        "vp": 1.2, "vp_lead": 1.0, "territory": 1.2, "seat": 1.0, "seat_pull": 1.0,
        "objective": 1.3, "economy": 1.0, "economy_delta": 1.0, "military": 1.0,
        "military_delta": 1.0, "combat": 1.0, "expansion": 1.2, "pass_penalty": 1.0,
        "next_vp": 1.5, "next_territory": 1.0, "next_objective": 1.2,
    },
}

PERSONA_NAMES = tuple(PERSONA_WEIGHTS.keys())


def _dot(weights: dict[str, float], feats: dict[str, float]) -> float:
    return sum(weights.get(k, 0.0) * v for k, v in feats.items())


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
        scored: list[tuple[float, dict]] = []
        for choice in decision_point.choices:
            feats = score_action(state, pid, choice, decision_point)
            scored.append((_dot(self.weights, feats), choice))
        best = max(s for s, _ in scored)
        top = [c for s, c in scored if abs(s - best) < 1e-9]
        return self.rng.choice(top)
