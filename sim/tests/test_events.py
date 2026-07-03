"""Global Event phase tests."""
from __future__ import annotations

import random

from aeonis_sim.engine.events import (
    EVENT_CARD_IDS,
    draw_event,
    init_event_deck,
    resolve_event,
)
from aeonis_sim.engine.game import Game
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import GameState, PlayerState


def test_event_fires_before_strategy_draft():
    g = Game({"players": 3}, seed=42)
    assert g.event_stats["resolved"] >= 1
    assert g.state.last_event_id in EVENT_CARD_IDS
    dp = g.next_decision()
    assert dp.kind == "strategy_draft"


def test_event_deck_cycles():
    rng = random.Random(7)
    state = GameState(
        players=[PlayerState(pid=0, home=(0, 0))],
        tiles={},
        event_deck=[],
    )
    first_pass = [draw_event(state, rng) for _ in range(12)]
    assert len(set(first_pass)) == 12
    second = draw_event(state, rng)
    assert second in EVENT_CARD_IDS
    assert len(state.event_deck) == 11


def test_mana_surge_grants_mana():
    state = build_initial_state({"players": 3}, random.Random(1))
    before = [state.player(i).mana for i in range(3)]
    resolve_event(state, "mana_surge")
    for i in range(3):
        assert state.player(i).mana == before[i] + 2


def test_festival_grants_pending_ap():
    state = build_initial_state({"players": 3}, random.Random(2))
    resolve_event(state, "festival")
    assert all(state.player(i).pending_ap == 1 for i in range(3))
