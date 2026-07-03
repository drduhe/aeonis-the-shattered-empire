"""Shared test helpers for the sim test suite."""
from __future__ import annotations


def advance_past_strategy_draft(game):
    """Consume Strategy Selection picks; return the first non-draft decision."""
    while True:
        dp = game.next_decision()
        if dp is None:
            return None
        if dp.kind != "strategy_draft":
            return dp
        game.submit(dp.choices[0])


def complete_strategy_draft(game) -> None:
    """Draft until the Action Phase begins."""
    while True:
        dp = game.next_decision()
        if dp is None:
            return
        if dp.kind != "strategy_draft":
            game._pending = dp
            return
        game.submit(dp.choices[0])
