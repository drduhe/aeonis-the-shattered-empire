from __future__ import annotations

from typing import Protocol


class Agent(Protocol):
    """One seat at the table. Milestone 1: choose() only; reflect() and
    exit_interview() join in plan C (LLM agents)."""

    def choose(self, observation: dict, decision_point) -> dict:
        """Return exactly one of decision_point.choices."""
        ...
