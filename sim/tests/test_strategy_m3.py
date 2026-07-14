"""Strategy primaries/secondaries completion (M3 Task 7)."""
from __future__ import annotations

from aeonis_sim.engine.game import Game
from aeonis_sim.engine.strategy import (
    apply_diplomatic_decree_primary,
    apply_imperial_mandate_primary,
    pay_primary_ap,
)

from .conftest import complete_strategy_draft


def _force_cards(g: Game, pid: int, *cards: str) -> None:
    complete_strategy_draft(g)
    g._pending = None
    g._begin_council_phase()
    g._council_proposal_queue = []
    g.state.player(pid).held_cards = list(cards)
    g.state.player(pid).primary_used = []
    g.state.player(pid).secondary_used = []
    g._begin_action_phase()
    g._initiative_queue = [pid] + [p for p in g._initiative_queue if p != pid]


def test_diplomatic_decree_grants_influence_and_speaker():
    g = Game({"players": 3}, seed=42)
    _force_cards(g, 0, "diplomatic_decree")
    p = g.state.player(0)
    p.influence = 5
    old_speaker = g.state.speaker
    pay_primary_ap(g.state, 0, "diplomatic_decree")
    apply_diplomatic_decree_primary(g.state, 0)
    assert p.influence == 7
    assert g.state.speaker == 0
    assert old_speaker != 0 or g.state.speaker == 0


def test_imperial_mandate_vp_when_holding_seat():
    g = Game({"players": 3}, seed=99)
    _force_cards(g, 0, "imperial_mandate")
    p = g.state.player(0)
    for t in g.state.controlled(0):
        if t.imperial_seat:
            break
    else:
        for t in g.state.tiles.values():
            if t.imperial_seat:
                t.controller = 0
                break
    before_vp = p.vp
    pay_primary_ap(g.state, 0, "imperial_mandate")
    apply_imperial_mandate_primary(g.state, 0, g.rng)
    assert p.vp == before_vp + 1
    assert p.influence >= 1


def test_imperial_mandate_secondary_draws_whisper():
    from aeonis_sim.engine.strategy import apply_strategy_secondary
    g = Game({"players": 3}, seed=77)
    _force_cards(g, 0, "imperial_mandate")
    p = g.state.player(1)
    p.ap = 2
    p.influence = 3
    before = len(p.whisper_hand)
    apply_strategy_secondary(g.state, 1, "imperial_mandate", use=True, rng=g.rng)
    assert len(p.whisper_hand) > before
