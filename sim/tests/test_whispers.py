import random

from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.whispers import (
    WHISPER_CARD_IDS,
    WHISPER_HAND_LIMIT,
    apply_action_whisper,
    discard_whisper,
    draw_whispers,
    hand_over_limit,
    init_whisper_deck,
)


def make_state(seed=1, players=4):
    return build_initial_state({"players": players}, random.Random(seed))


def test_whisper_deck_has_26_cards():
    deck = init_whisper_deck(random.Random(0))
    assert len(deck) == 26
    assert set(deck) == set(WHISPER_CARD_IDS)


def test_setup_draws_two_whispers():
    s = make_state()
    for p in s.players:
        assert len(p.whisper_hand) == 2


def test_draw_on_vp_pending():
    s = make_state()
    p = s.players[0]
    before = len(p.whisper_hand)
    p.add_vp(1, "test")
    assert p.pending_whisper_draws == 1
    draw_whispers(s, 0, p.pending_whisper_draws, random.Random(1))
    p.pending_whisper_draws = 0
    assert len(p.whisper_hand) == before + 1


def test_hidden_cache_gold():
    s = make_state()
    p = s.players[0]
    p.whisper_hand = ["hidden_cache"]
    apply_action_whisper(s, 0, {"card": "hidden_cache", "choice": "gold"})
    assert p.gold >= 5
    assert "hidden_cache" not in p.whisper_hand


def test_contraband_resources():
    s = make_state()
    p = s.players[0]
    g, m, i = p.gold, p.mana, p.influence
    p.whisper_hand = ["contraband"]
    apply_action_whisper(s, 0, {"card": "contraband"})
    assert p.gold == g + 1 and p.mana == m + 1 and p.influence == i + 1


def test_hand_limit_detection():
    s = make_state()
    p = s.players[0]
    p.whisper_hand = list(WHISPER_CARD_IDS[: WHISPER_HAND_LIMIT + 1])
    assert hand_over_limit(s, 0)


def test_discard_removes_from_hand():
    s = make_state()
    p = s.players[0]
    p.whisper_hand = ["sabotage", "hidden_cache"]
    discard_whisper(s, 0, "sabotage")
    assert "sabotage" not in p.whisper_hand
    assert "sabotage" in s.whisper_discard


def test_whisper_specs_cover_all_cards():
    from aeonis_sim.engine.whispers import WHISPER_SPECS
    assert set(WHISPER_SPECS) == set(WHISPER_CARD_IDS)


def test_council_whisper_backroom_deal_votes():
    from aeonis_sim.engine.whispers import apply_council_whisper
    s = make_state()
    s.players[0].whisper_hand = ["backroom_deal"]
    result = apply_council_whisper(s, 0, {
        "type": "whisper_play",
        "card": "backroom_deal",
        "side": "for",
    })
    assert result == {"for": 2}


def test_sabotage_offered_to_opponents():
    from aeonis_sim.engine.whispers import offer_sabotage_players
    s = make_state(players=3)
    s.players[1].whisper_hand = ["sabotage"]
    assert offer_sabotage_players(s, 0, "hidden_cache") == [1]
    assert offer_sabotage_players(s, 0, "sabotage") == []

