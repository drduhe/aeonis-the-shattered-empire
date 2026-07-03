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
        "vp": 1.3, "economy": 2.5, "economy_delta": 2.5, "next_economy": 1.6,
        "objective": 2.6, "next_objective": 2.2, "territory": 0.6, "combat": 0.2,
        "military": 0.5, "pass_penalty": 1.0,
    },
    "expander": {
        "vp": 1.25, "territory": 0.7, "next_territory": 0.55, "expansion": 0.65,
        "territory_sat": -3.8, "next_territory_sat": -2.8,
        "seat": 0.85, "seat_pull": 0.85, "rite_ready": 0.9, "seat_streak": 0.7, "next_seat": 0.7,
        "objective": 2.1, "next_objective": 1.9, "combat": 0.45, "pass_penalty": 0.85,
    },
    "diplomat": {
        "vp": 1.15, "vp_lead": 0.95, "objective": 2.9, "next_objective": 2.3,
        "economy": 1.35, "territory": 0.65, "combat": 0.3, "military": 0.5,
        "pass_penalty": 0.8, "renown": 1.0,
    },
    "balanced": {
        "vp": 1.35, "vp_lead": 1.15, "territory": 0.85, "seat": 1.05, "seat_pull": 0.95,
        "objective": 2.5, "next_objective": 2.3, "economy": 1.1, "economy_delta": 1.1,
        "military": 1.0, "military_delta": 1.0, "combat": 0.75, "expansion": 0.8,
        "pass_penalty": 1.0, "next_vp": 1.65, "next_territory": 0.55,
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
