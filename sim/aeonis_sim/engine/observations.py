from __future__ import annotations

from dataclasses import dataclass, field

_DEFAULT_PHASE = {
    "strategy_draft": "strategy",
    "action": "action",
    "strategy_primary": "action",
    "strategy_secondary": "action",
    "council_propose": "council",
    "council_vote": "council",
    "negotiation": "council",
    "exploration": "action",
    "objective_draw": "round_start",
    "artifact": "action",
    "research": "action",
    "objective_draw": "round_start",
    "press": "combat",
    "defender_retreat": "combat",
}


@dataclass
class DecisionPoint:
    """A point where an agent must choose.

    kind: fine-grained decision type (action, strategy_draft, press, …)
    phase: round-structure window (strategy, action, combat, council, …)
    """
    kind: str
    pid: int
    choices: list                      # list[dict], JSON-safe
    phase: str | None = None
    context: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.phase is None:
            self.phase = _DEFAULT_PHASE.get(self.kind, self.kind)


def observe(state, viewer_pid: int) -> dict:
    """The viewer's view of the game. Milestone 1: full information."""
    return {"viewer": viewer_pid, "state": state.to_dict()}
