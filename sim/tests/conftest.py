"""Shared test helpers for the sim test suite."""
from __future__ import annotations

_PHASE_SKIP = frozenset({
    "strategy_draft",
    "council_propose",
    "council_vote",
    "negotiation",
    "exploration",
})


def advance_past_strategy_draft(game):
    """Consume Strategy Selection picks; return the first non-draft decision."""
    while True:
        dp = game.next_decision()
        if dp is None:
            return None
        if dp.kind not in _PHASE_SKIP:
            return dp
        game.submit(dp.choices[0])


def advance_to_action_phase(game):
    """Skip draft and council; return the first Action Phase decision."""
    while True:
        dp = game.next_decision()
        if dp is None:
            return None
        if dp.kind == "action":
            return dp
        game.submit(dp.choices[0])


def complete_strategy_draft(game) -> None:
    """Draft until council or action phase begins."""
    while True:
        dp = game.next_decision()
        if dp is None:
            return
        if dp.kind not in ("strategy_draft",):
            game._pending = dp
            return
        game.submit(dp.choices[0])
