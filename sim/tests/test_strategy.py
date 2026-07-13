"""Strategy draft phase (Strategy.md)."""
from __future__ import annotations

from aeonis_sim.engine.game import Game
from aeonis_sim.engine.strategy import (
    STRATEGY_CARD_IDS,
    apply_draft_pick,
    begin_strategy_selection,
    build_draft_queue,
    cards_per_player,
    draft_order,
    finish_undrafted_bounty,
    initiative_order,
)
from aeonis_sim.engine.types import GameState, PlayerState

from .conftest import advance_to_action_phase, complete_strategy_draft


def _state(players: int, *, speaker: int = 0) -> GameState:
    s = GameState(
        players=[
            PlayerState(pid=i, home=(i, 0), vp=i, renown=0)
            for i in range(players)
        ],
        tiles={},
        speaker=speaker,
    )
    begin_strategy_selection(s)
    return s


def test_cards_per_player_by_count():
    assert cards_per_player(3) == 2
    assert cards_per_player(4) == 2
    assert cards_per_player(5) == 1
    assert cards_per_player(8) == 1


def test_draft_order_follows_vp_then_renown():
    s = GameState(
        players=[
            PlayerState(pid=0, home=(0, 0), vp=5, renown=2),
            PlayerState(pid=1, home=(1, 0), vp=2, renown=9),
            PlayerState(pid=2, home=(2, 0), vp=2, renown=1),
            PlayerState(pid=3, home=(3, 0), vp=8, renown=0),
        ],
        tiles={},
        speaker=1,
    )
    assert draft_order(s, speaker=1) == [2, 1, 0, 3]


def test_build_draft_queue_two_passes_at_4p():
    s = _state(4)
    queue = build_draft_queue(s, speaker=0)
    assert len(queue) == 8
    assert queue[:4] == queue[4:]


def test_bounty_accumulates_on_undrafted_cards():
    s = _state(3)
    s.strategy_bounty["economic_boom"] = 2
    apply_draft_pick(s, 0, "resource_surge")
    assert s.player(0).gold == 0
    assert "resource_surge" not in s.strategy_pool
    finish_undrafted_bounty(s)
    assert s.strategy_bounty["economic_boom"] == 3
    for card in STRATEGY_CARD_IDS:
        if card in ("resource_surge", "economic_boom"):
            continue
        assert s.strategy_bounty[card] == 1


def test_draft_pick_pays_accumulated_bounty():
    s = _state(3)
    s.strategy_bounty["military_maneuvers"] = 4
    apply_draft_pick(s, 1, "military_maneuvers")
    assert s.player(1).gold == 4
    assert s.strategy_bounty["military_maneuvers"] == 0


def test_initiative_order_uses_lowest_held_card():
    s = _state(4)
    s.player(0).held_cards = ["imperial_mandate", "resource_surge"]
    s.player(1).held_cards = ["arcane_ascendancy"]
    s.player(2).held_cards = ["military_maneuvers"]
    s.player(3).held_cards = ["economic_boom"]
    assert initiative_order(s) == [1, 0, 2, 3]


def test_4p_players_receive_two_cards_each():
    g = Game({"players": 4, "lord_asymmetry": {"enabled": False}}, seed=77)
    picks: dict[int, list[str]] = {i: [] for i in range(4)}
    for _ in range(8):
        dp = g.next_decision()
        assert dp.kind == "strategy_draft"
        picks[dp.pid].append(dp.choices[0]["card"])
        g.submit(dp.choices[0])
    for pid, cards in picks.items():
        assert len(cards) == 2
    dp = g.next_decision()
    assert dp.kind == "council_propose"


def test_3p_players_receive_two_cards_each():
    g = Game({"players": 3}, seed=88)
    counts = {0: 0, 1: 0, 2: 0}
    for _ in range(6):
        dp = g.next_decision()
        assert dp.kind == "strategy_draft"
        counts[dp.pid] += 1
        g.submit(dp.choices[0])
    assert all(n == 2 for n in counts.values())


def test_lowest_vp_drafts_first_in_game():
    g = Game({"players": 4}, seed=99)
    g.state.player(2).vp = 0
    g.state.player(0).vp = 10
    g.state.player(1).vp = 5
    g.state.player(3).vp = 3
    g._draft_queue = build_draft_queue(g.state, g.state.speaker)
    dp = g.next_decision()
    assert dp.pid == 2


def test_initiative_card_1_acts_before_card_8():
    g = Game({"players": 3}, seed=1)
    advance_to_action_phase(g)
    g.state.player(0).held_cards = ["imperial_mandate"]
    g.state.player(1).held_cards = ["arcane_ascendancy"]
    g.state.player(2).held_cards = ["economic_boom"]
    g._initiative_queue = initiative_order(g.state)
    g._pending = None
    dp = g.next_decision()
    assert dp.kind == "action" and dp.pid == 1


def test_pass_removes_player_from_initiative_queue():
    g = Game({"players": 3}, seed=5)
    advance_to_action_phase(g)
    dp = g.next_decision()
    passed = dp.pid
    g.submit({"type": "pass"})
    assert passed not in g._initiative_queue


def test_non_pass_action_rotates_initiative():
    g = Game({"players": 3}, seed=5)
    advance_to_action_phase(g)
    first = g._initiative_queue[0]
    dp = g.next_decision()
    assert dp.pid == first
    g.submit({"type": "pass"})
    # second player is now at head after first passed
    dp = g.next_decision()
    second = dp.pid
    g.submit({"type": "pass"})
    dp = g.next_decision()
    third = dp.pid
    # third takes a non-pass if available, else pass
    if any(c["type"] != "pass" for c in dp.choices):
        choice = next(c for c in dp.choices if c["type"] != "pass")
        g.submit(choice)
        assert g._initiative_queue[0] == third
        assert g._initiative_queue[-1] == third
