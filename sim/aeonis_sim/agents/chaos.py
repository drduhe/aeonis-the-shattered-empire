from __future__ import annotations

import random


class ChaosBot:
    """Uniform-random agent. Purpose: rules fuzzing, not balance signal."""

    name = "chaos"

    def __init__(self, seed: int):
        self.rng = random.Random(seed)

    def choose(self, observation: dict, decision_point) -> dict:
        return self.rng.choice(decision_point.choices)
