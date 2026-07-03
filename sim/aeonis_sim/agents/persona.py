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
        "production_bonus": 3.0,
        "gold_track": 2.5, "next_gold_track": 2.2,
        "builder_need": -4.0,
        "objective": 3.2, "next_objective": 3.0,
        "territory": 0.3, "expansion": 0.15, "combat": 0.1, "military": 0.2,
        "military_delta": -0.8, "pass_penalty": 1.6,
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
            for key, mul in PERSONA_FEATURE_BOOSTS.get(self.persona, {}).items():
                if key in feats:
                    feats[key] *= mul
            scored.append((_dot(self.weights, feats), choice))
        best = max(s for s, _ in scored)
        top = [c for s, c in scored if abs(s - best) < 1e-9]
        return self.rng.choice(top)
