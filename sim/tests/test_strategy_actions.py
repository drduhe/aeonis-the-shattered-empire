"""Strategy primary and secondary actions (Task 3)."""
from __future__ import annotations

from aeonis_sim.engine.game import Game
from aeonis_sim.engine.strategy import (
    apply_resource_surge_primary,
    apply_strategy_secondary,
    enumerate_secondary_choices,
    enumerate_strategy_primaries,
    pay_primary_ap,
    secondary_eligible_players,
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


def test_resource_surge_primary_grants_resources():
    g = Game({"players": 3}, seed=42)
    _force_cards(g, 0, "resource_surge")
    p = g.state.player(0)
    before = (p.gold, p.mana, p.influence, p.ap)
    pay_primary_ap(g.state, 0, "resource_surge")
    apply_resource_surge_primary(g.state, 0)
    assert (p.gold, p.mana, p.influence) == (
        before[0] + 2, before[1] + 2, before[2] + 1,
    )


def test_enumerate_strategy_primaries_requires_ap_and_once_per_round():
    g = Game({"players": 3}, seed=42)
    _force_cards(g, 0, "military_maneuvers", "resource_surge")
    p = g.state.player(0)
    p.ap = 0
    primaries = enumerate_strategy_primaries(g.state, 0)
    assert {c["card"] for c in primaries} == {"resource_surge"}
    assert "military_maneuvers" not in {c["card"] for c in primaries}
    p.ap = 5
    primaries = enumerate_strategy_primaries(g.state, 0)
    assert {c["card"] for c in primaries} == {"military_maneuvers", "resource_surge"}
    pay_primary_ap(g.state, 0, "military_maneuvers")
    primaries = enumerate_strategy_primaries(g.state, 0)
    assert {c["card"] for c in primaries} == {"resource_surge"}


def test_resource_surge_secondary_once_per_player_per_round():
    g = Game({"players": 3}, seed=55)
    _force_cards(g, 0, "resource_surge")
    g.state.player(1).ap = 3
    g.state.player(2).ap = 3
    eligible = secondary_eligible_players(g.state, 0, "resource_surge")
    assert eligible == [1, 2]
    choices = enumerate_secondary_choices(g.state, 1, "resource_surge", 0)
    assert any(c.get("use") for c in choices)
    apply_strategy_secondary(g.state, 1, "resource_surge", use=True)
    assert "resource_surge" in g.state.player(1).secondary_used
    assert enumerate_secondary_choices(g.state, 1, "resource_surge", 0) == []


def test_resource_surge_primary_in_action_choices():
    g = Game({"players": 3}, seed=77)
    _force_cards(g, 0, "resource_surge")
    dp = g.next_decision()
    assert dp.kind == "action"
    surge = next(c for c in dp.choices if c.get("card") == "resource_surge")
    g.submit(surge)
    p = g.state.player(0)
    assert p.gold >= 2 and p.mana >= 2 and p.influence >= 1
    assert "resource_surge" in p.primary_used


def test_secondary_window_after_resource_surge_primary():
    g = Game({"players": 3}, seed=88)
    _force_cards(g, 0, "resource_surge")
    g.state.player(1).ap = 2
    dp = g.next_decision()
    g.submit(next(c for c in dp.choices if c.get("card") == "resource_surge"))
    dp2 = g.next_decision()
    assert dp2.kind == "strategy_secondary" and dp2.pid == 1
    g.submit({"type": "strategy_secondary", "card": "resource_surge", "use": False})
    dp3 = g.next_decision()
    assert dp3.kind == "strategy_secondary" and dp3.pid == 2
