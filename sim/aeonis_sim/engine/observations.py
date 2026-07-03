from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DecisionPoint:
    """A point where an agent must choose. kind is one of:
    - "action":           your Action Phase turn; choices are actions
    - "press":            attacker after a battle round: press or end
    - "defender_retreat": defender after a battle round: retreat or hold
    """
    kind: str
    pid: int
    choices: list                      # list[dict], JSON-safe
    context: dict = field(default_factory=dict)


def observe(state, viewer_pid: int) -> dict:
    """The viewer's view of the game. Milestone 1: full information."""
    return {"viewer": viewer_pid, "state": state.to_dict()}
