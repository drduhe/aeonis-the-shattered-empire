"""Strategy card model and draft (Strategy.md).

M2 simplification: primaries for Arcane Ascendancy (resources-only stub),
Diplomatic Decree (council), and full secondary menu deferred to M2.1 / Task 5.
Task 3 subset: Resource Surge, Military Maneuvers, Economic Boom (+ secondaries
for Surge and Boom). Plan "Consolidation of Power" maps to Economic Boom.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from . import combat
from .move import apply_move, enumerate_moves
from .hexmap import neighbors

if TYPE_CHECKING:
    from .types import GameState, Terrain

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


# All eight primaries encoded (M3 Task 7).
PRIMARY_IMPLEMENTED: frozenset[str] = frozenset(STRATEGY_CARD_IDS)

SECONDARY_EFFECTS: dict[str, dict] = {
    "resource_surge": {"ap": 1, "gold": 1, "mana": 1},
    "economic_boom": {"ap": 1, "gold": 2},
    "diplomatic_decree": {"ap": 1, "influence": 2},
    "expansion_strategy": {"claim_hex": True},
    "tactical_reinforcements": {"ap": 1, "extra_recruit": True},
    "imperial_mandate": {"draw_whisper": True},
    "arcane_ascendancy": {"arcane_secondary": True},
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


def _can_use_primary(state: GameState, pid: int, card_id: str) -> bool:
    player = state.player(pid)
    if card_id not in player.held_cards or card_id in player.primary_used:
        return False
    if card_id not in PRIMARY_IMPLEMENTED:
        return False
    card = STRATEGY_CARDS[card_id]
    if player.ap < card.primary_ap:
        return False
    if card_id == "diplomatic_decree" and player.influence < 2:
        return False
    if card_id == "expansion_strategy":
        return bool(_eligible_claim_hexes(state, pid))
    if card_id == "tactical_reinforcements":
        from .recruit import enumerate_recruits
        return bool(enumerate_recruits(state, pid, ignore_city_limit=True))
    return True


def enumerate_strategy_primaries(state: GameState, pid: int) -> list[dict]:
    """Legal Strategy Card primaries on the acting player's turn (Strategy.md §2.1)."""
    out = []
    for card_id in state.player(pid).held_cards:
        if not _can_use_primary(state, pid, card_id):
            continue
        card = STRATEGY_CARDS[card_id]
        out.append({
            "type": "strategy_primary",
            "card": card_id,
            "cost": card.primary_ap,
        })
    return out


def apply_resource_surge_primary(state: GameState, pid: int) -> None:
    player = state.player(pid)
    player.gold += 2
    player.mana += 2
    player.influence += 1


def apply_economic_boom_primary(state: GameState, pid: int) -> None:
    state.player(pid).gold += 5


def apply_arcane_ascendancy_primary(state: GameState, pid: int) -> None:
    state.player(pid).mana += 2


def _eligible_claim_hexes(state: GameState, pid: int) -> list[tuple]:
    from .types import Terrain
    out = []
    for t in state.controlled(pid):
        for nb in neighbors(t.coord):
            nt = state.tiles.get(nb)
            if nt is None or nt.controller is not None:
                continue
            if any(u.owner != pid for u in nt.units):
                continue
            out.append(nb)
    return sorted(set(out))


def claim_neutral_hex(state: GameState, pid: int, coord: tuple) -> None:
    tile = state.tiles[coord]
    if tile.controller is not None:
        raise ValueError("hex not neutral")
    tile.controller = pid
    tile.explored = True


def apply_expansion_strategy_primary(state: GameState, pid: int, coord: tuple) -> None:
    claim_neutral_hex(state, pid, coord)
    p = state.player(pid)
    cap = state.pop_cap(pid)
    p.pop_pool = min(cap, p.pop_pool + 1)


def apply_diplomatic_decree_primary(state: GameState, pid: int) -> None:
    p = state.player(pid)
    p.influence -= 2
    state.speaker = pid


def apply_imperial_mandate_primary(state: GameState, pid: int, rng) -> None:
    from .objectives import deal_secret_draw
    p = state.player(pid)
    if any(t.imperial_seat for t in state.controlled(pid)):
        p.add_vp(1, "imperial_mandate")
    else:
        deal_secret_draw(state, pid, rng)
    p.influence += 1


def enumerate_expansion_primary_choices(state: GameState, pid: int) -> list[dict]:
    return [
        {"type": "expansion_claim", "hex": list(c)}
        for c in _eligible_claim_hexes(state, pid)
    ]


def enumerate_tactical_primary_recruits(state: GameState, pid: int) -> list[dict]:
    from .recruit import enumerate_recruits
    out = []
    for choice in enumerate_recruits(state, pid, ignore_city_limit=True):
        if len(choice.get("units", [])) <= 2:
            out.append({**choice, "type": "tactical_recruit", "free": True})
    return out


def pay_primary_ap(state: GameState, pid: int, card_id: str) -> None:
    card = STRATEGY_CARDS[card_id]
    state.player(pid).ap -= card.primary_ap
    state.player(pid).primary_used.append(card_id)


def enumerate_military_maneuver_moves(state: GameState, pid: int) -> list[dict]:
    """Move at 0 terrain AP; ZOC surcharges still apply (Strategy.md §3 card 3)."""
    return enumerate_moves(state, pid, waive_terrain=True)


def enumerate_military_maneuver_attacks(state: GameState, pid: int) -> list[dict]:
    return combat.enumerate_attacks(state, pid, attack_ap=1)


def secondary_eligible_players(
    state: GameState, owner_pid: int, card_id: str,
) -> list[int]:
    """Followers who may opt into a secondary, in initiative order."""
    if card_id not in SECONDARY_EFFECTS:
        return []
    spec = SECONDARY_EFFECTS[card_id]
    need_ap = spec.get("ap", 0)
    card = STRATEGY_CARDS[card_id]
    need_inf = card.secondary_influence or 0
    out = []
    for pid in initiative_order(state):
        if pid == owner_pid:
            continue
        player = state.player(pid)
        if card_id in player.secondary_used:
            continue
        if player.ap < need_ap:
            continue
        if need_inf and player.influence < need_inf:
            continue
        out.append(pid)
    return out


def enumerate_secondary_choices(
    state: GameState, pid: int, card_id: str, owner_pid: int,
) -> list[dict]:
    if pid == owner_pid or card_id not in SECONDARY_EFFECTS:
        return []
    if card_id in state.player(pid).secondary_used:
        return []
    spec = SECONDARY_EFFECTS[card_id]
    card = STRATEGY_CARDS[card_id]
    choices = [{"type": "strategy_secondary", "card": card_id, "use": False}]
    player = state.player(pid)
    if player.ap >= spec.get("ap", 0):
        if not card.secondary_influence or player.influence >= card.secondary_influence:
            choices.append({
                "type": "strategy_secondary",
                "card": card_id,
                "use": True,
                "cost": spec.get("ap", 0),
            })
    return choices


def apply_strategy_secondary(
    state: GameState,
    pid: int,
    card_id: str,
    *,
    use: bool,
    rng=None,
) -> dict | None:
    """Apply secondary; return optional follow-up payload for game loop."""
    player = state.player(pid)
    if card_id in player.secondary_used:
        raise ValueError(f"secondary already used: {card_id}")
    if not use:
        player.secondary_used.append(card_id)
        return None
    spec = SECONDARY_EFFECTS[card_id]
    card = STRATEGY_CARDS[card_id]
    player.ap -= spec.get("ap", 0)
    if card.secondary_influence:
        player.influence -= card.secondary_influence
    player.gold += spec.get("gold", 0)
    player.mana += spec.get("mana", 0)
    player.influence += spec.get("influence", 0)
    player.secondary_used.append(card_id)
    if spec.get("claim_hex"):
        hexes = _eligible_claim_hexes(state, pid)
        if hexes:
            claim_neutral_hex(state, pid, hexes[0])
    if spec.get("draw_whisper") and rng is not None:
        from .whispers import draw_whispers
        draw_whispers(state, pid, 1, rng)
    if spec.get("arcane_secondary"):
        player.mana = max(0, player.mana - 1)
        return {"kind": "arcane_secondary_research", "pid": pid, "card": card_id}
    return None
