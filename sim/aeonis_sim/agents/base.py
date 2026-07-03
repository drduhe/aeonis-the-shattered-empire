from __future__ import annotations

from typing import Protocol


class Agent(Protocol):
    name: str

    def choose(self, observation: dict, decision_point) -> dict:
        """Return one of decision_point.choices."""
        ...
