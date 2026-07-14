from __future__ import annotations

from typing import Protocol


class Agent(Protocol):
    """One seat at the table. Qualitative hooks are optional at runtime."""

    def choose(self, observation: dict, decision_point) -> dict:
        """Return exactly one of decision_point.choices."""
        ...

    def reflect(self, round_summary: dict) -> None:
        ...

    def exit_interview(self, game_summary: dict) -> dict:
        ...
