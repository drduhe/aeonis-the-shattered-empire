"""High Council phase tests."""
from __future__ import annotations

import random

from aeonis_sim.engine.council import (
    AGENDA_CARD_IDS,
    apply_motion,
    council_votes,
    init_agenda_deck,
    reveal_agenda,
    tally_votes,
)
from aeonis_sim.engine.game import Game
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import GameState, PlayerState

from .conftest import advance_to_action_phase, complete_strategy_draft


def test_council_follows_strategy_draft():
    g = Game({"players": 4}, seed=99)
    complete_strategy_draft(g)
    dp = g.next_decision()
    assert dp.kind == "council_propose"


def test_speaker_rotates_at_cleanup():
    g = Game({"players": 3}, seed=5)
    start = g.state.speaker
    advance_to_action_phase(g)
    for _ in range(3):
        dp = g.next_decision()
        g.submit({"type": "pass"})
    g.next_decision()
    assert g.state.speaker == (start + 1) % 3


def test_council_votes_include_renown_tiers():
    state = GameState(
        players=[
            PlayerState(pid=0, home=(0, 0), renown=10),
            PlayerState(pid=1, home=(1, 0), renown=2),
        ],
        tiles={},
    )
    assert council_votes(state, 0) == 3
    assert council_votes(state, 1) == 1


def test_motion_passes_with_majority():
    state = build_initial_state({"players": 3}, random.Random(3))
    ballots = [
        {"pid": 0, "support": True, "lobby": 0},
        {"pid": 1, "support": True, "lobby": 0},
        {"pid": 2, "support": False, "lobby": 0},
    ]
    assert tally_votes(state, "hero_of_the_realm", ballots)


def test_apply_motion_hero_grants_renown():
    state = build_initial_state({"players": 3}, random.Random(4))
    before = state.player(1).renown
    apply_motion(state, "hero_of_the_realm", 1)
    assert state.player(1).renown == before + 1


def test_agenda_deck_reveals_card():
    state = GameState(players=[], tiles={}, agenda_deck=list(AGENDA_CARD_IDS))
    rng = random.Random(0)
    card = reveal_agenda(state, rng)
    assert card in AGENDA_CARD_IDS
    assert state.agenda_revealed == card
