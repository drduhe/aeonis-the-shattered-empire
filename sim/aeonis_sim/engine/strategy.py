"""Strategy card model and draft (Strategy.md).

M2 simplification: card effect data is recorded for Task 3; primaries that need
Arcane Tier II+ or emergency council resolve as stubs until Tasks 3–5 land.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import GameState

STRATEGY_CARD_IDS: tuple[str, ...] = (
    "arcane_ascendancy",
    "resource_surge",
    "military_maneuvers",
    "diplomatic_decree",
    "expansion_strategy",
    "tactical_reinforcements",
    "economic_boom",
    "imperial_mandate",
)


@dataclass(frozen=True)
class StrategyCard:
    id: str
    name: str
    initiative: int
    primary_ap: int
    secondary_ap: int | None = None
    secondary_influence: int | None = None


STRATEGY_CARDS: dict[str, StrategyCard] = {
    "arcane_ascendancy": StrategyCard(
        "arcane_ascendancy", "Arcane Ascendancy", 1, 1
    ),
    "resource_surge": StrategyCard(
        "resource_surge", "Resource Surge", 2, 0
    ),
    "military_maneuvers": StrategyCard(
        "military_maneuvers", "Military Maneuvers", 3, 1
    ),
    "diplomatic_decree": StrategyCard(
        "diplomatic_decree", "Diplomatic Decree", 4, 1
    ),
    "expansion_strategy": StrategyCard(
        "expansion_strategy", "Expansion Strategy", 5, 1,
        secondary_influence=2,
    ),
    "tactical_reinforcements": StrategyCard(
        "tactical_reinforcements", "Tactical Reinforcements", 6, 1,
        secondary_ap=1,
    ),
    "economic_boom": StrategyCard(
        "economic_boom", "Economic Boom", 7, 0, secondary_ap=1
    ),
    "imperial_mandate": StrategyCard(
        "imperial_mandate", "Imperial Mandate", 8, 1,
        secondary_influence=2,
    ),
}


def cards_per_player(player_count: int) -> int:
    """Strategy.md §1.2: 2 cards at 3–4p, 1 card at 5–8p."""
    return 2 if player_count <= 4 else 1


def _clockwise_distance(pid: int, speaker: int, player_count: int) -> int:
    return (pid - speaker - 1) % player_count


def draft_order(state: GameState, speaker: int) -> list[int]:
    """Ascending VP, then Renown, then clockwise from Speaker."""
    n = len(state.players)
    return sorted(
        range(n),
        key=lambda pid: (
            state.player(pid).vp,
            state.player(pid).renown,
            _clockwise_distance(pid, speaker, n),
            pid,
        ),
    )


def build_draft_queue(state: GameState, speaker: int) -> list[int]:
    order = draft_order(state, speaker)
    picks = cards_per_player(len(state.players))
    queue: list[int] = []
    for _ in range(picks):
        queue.extend(order)
    return queue


def begin_strategy_selection(state: GameState) -> None:
    """Reveal all eight cards and reset per-round player strategy state."""
    state.strategy_pool = list(STRATEGY_CARD_IDS)
    for p in state.players:
        p.held_cards = []
        p.primary_used = []
        p.secondary_used = []


def enumerate_draft_choices(state: GameState) -> list[dict]:
    return [{"type": "draft", "card": card_id} for card_id in state.strategy_pool]


def apply_draft_pick(state: GameState, pid: int, card_id: str) -> None:
    if card_id not in state.strategy_pool:
        raise ValueError(f"card not in pool: {card_id}")
    state.strategy_pool.remove(card_id)
    player = state.player(pid)
    player.held_cards.append(card_id)
    player.gold += state.strategy_bounty.get(card_id, 0)
    state.strategy_bounty[card_id] = 0


def finish_undrafted_bounty(state: GameState) -> None:
    """Strategy.md §1.3: +1 Gold on each undrafted card (accumulates)."""
    for card_id in state.strategy_pool:
        state.strategy_bounty[card_id] = state.strategy_bounty.get(card_id, 0) + 1
    state.strategy_pool = []


def initiative_for_player(state: GameState, pid: int) -> int:
    cards = state.player(pid).held_cards
    if not cards:
        return 99
    return min(STRATEGY_CARDS[c].initiative for c in cards)


def initiative_order(state: GameState) -> list[int]:
    """Lowest held card number acts first; ties by pid."""
    return sorted(
        range(len(state.players)),
        key=lambda pid: (initiative_for_player(state, pid), pid),
    )
