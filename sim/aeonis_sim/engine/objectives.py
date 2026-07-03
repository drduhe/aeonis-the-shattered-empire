"""Objective predicates and secret draw economy (First Playable §4.4, Objectives.md §3)."""
from __future__ import annotations

import random
from itertools import combinations
from typing import TYPE_CHECKING, Optional

from .hexmap import distance
from .types import BuildingType, Terrain

if TYPE_CHECKING:
    from .types import GameState

# --- Public shared row ---
# Council Power stays deferred (full-deck audit). merchant_lord is the
# PROPOSED economy experiment filling the sixth slot (2026-07-03, economist
# memo Lever B; Objectives.md §4.4).

PUBLIC_OBJECTIVE_IDS = (
    "frontier_lord",
    "builder",
    "merchant_lord",
    "portal_mastery",
    "warlord",
    "seat_of_empire",
)

SECRET_OBJECTIVE_IDS = (
    "hidden_arsenal",
    "golden_hoard",
    "mana_flood",
    "quiet_knife",
    "borderbreaker",
    "architect_of_control",
)

SECRET_CAP = 3
IMMEDIATE_SECRETS = frozenset({"golden_hoard", "mana_flood"})


def _frontier_lord(state, pid) -> bool:
    return len(state.controlled(pid)) >= 7


def _builder(state, pid) -> bool:
    return sum(len(t.buildings) for t in state.controlled(pid)) >= 3


def _merchant_lord(state, pid) -> bool:
    return state.player(pid).gold >= 8


def _portal_mastery(state, pid) -> bool:
    controls_portal = any(t.terrain == Terrain.PORTAL for t in state.controlled(pid))
    return controls_portal and state.player(pid).used_portal_travel


def _warlord(state, pid) -> bool:
    return state.player(pid).battle_wins >= 2


def _seat_of_empire(state, pid) -> bool:
    return any(t.imperial_seat for t in state.controlled(pid))


PUBLIC_OBJECTIVES = {
    "frontier_lord": _frontier_lord,
    "builder": _builder,
    "merchant_lord": _merchant_lord,
    "portal_mastery": _portal_mastery,
    "warlord": _warlord,
    "seat_of_empire": _seat_of_empire,
}


def _hidden_arsenal(state, pid) -> bool:
    p = state.player(pid)
    for coord in p.fortress_built:
        if coord in p.battle_wins_at:
            return True
    return False


def _golden_hoard(state, pid) -> bool:
    return state.player(pid).gold >= 10


def _mana_flood(state, pid) -> bool:
    return state.player(pid).mana >= 10


def _quiet_knife(state, pid) -> bool:
    return bool(state.player(pid).influence_hex_gains)


def _borderbreaker(state, pid) -> bool:
    unit_hexes = {coord for coord, _ in state.units_of(pid)}
    if len(unit_hexes) < 3:
        return False
    for trio in combinations(unit_hexes, 3):
        if all(distance(a, b) >= 3 for a, b in combinations(trio, 2)):
            return True
    return False


def _architect_of_control(state, pid) -> bool:
    special = {Terrain.CITY, Terrain.RUINS, Terrain.PORTAL}
    count = sum(
        1 for t in state.controlled(pid)
        if t.imperial_seat or t.terrain in special
    )
    return count >= 2


SECRET_OBJECTIVES = {
    "hidden_arsenal": _hidden_arsenal,
    "golden_hoard": _golden_hoard,
    "mana_flood": _mana_flood,
    "quiet_knife": _quiet_knife,
    "borderbreaker": _borderbreaker,
    "architect_of_control": _architect_of_control,
}

OBJECTIVES = PUBLIC_OBJECTIVES


def _reshuffle_secret_deck(state: GameState, rng: random.Random) -> None:
    if state.secret_objective_discard:
        state.secret_objective_deck = list(state.secret_objective_discard)
        state.secret_objective_discard = []
        rng.shuffle(state.secret_objective_deck)


def draw_secret_card(state: GameState, rng: random.Random) -> Optional[str]:
    if not state.secret_objective_deck:
        _reshuffle_secret_deck(state, rng)
    if not state.secret_objective_deck:
        return None
    return state.secret_objective_deck.pop()


def discard_secret_card(state: GameState, card_id: str) -> None:
    state.secret_objective_discard.append(card_id)


def draw_public_to_row(state: GameState) -> bool:
    """Reveal one public objective to the shared row if possible."""
    if not state.shared_public_deck:
        return False
    if len(state.shared_public_revealed) >= len(PUBLIC_OBJECTIVE_IDS):
        return False
    state.shared_public_revealed.append(state.shared_public_deck.pop())
    return True


def record_influence_hex_gain(state: GameState, pid: int, coord: tuple) -> None:
    p = state.player(pid)
    if coord not in p.influence_hex_gains:
        p.influence_hex_gains.append(coord)


def record_fortress_built(state: GameState, pid: int, coord: tuple) -> None:
    p = state.player(pid)
    if coord not in p.fortress_built:
        p.fortress_built.append(coord)


def record_battle_win_at(state: GameState, pid: int, coord: tuple) -> None:
    p = state.player(pid)
    if coord not in p.battle_wins_at:
        p.battle_wins_at.append(coord)


def try_immediate_secrets(state: GameState, pid: int) -> list[str]:
    """Score golden_hoard / mana_flood the moment thresholds are met."""
    p = state.player(pid)
    scored: list[str] = []
    for sid in list(p.secret_objectives):
        if sid not in IMMEDIATE_SECRETS:
            continue
        if SECRET_OBJECTIVES[sid](state, pid):
            p.add_vp(2, "objective")
            p.secrets_scored.append(sid)
            p.secret_objectives.remove(sid)
            scored.append(sid)
    return scored


def score_cleanup_secrets(state: GameState, pid: int) -> None:
    p = state.player(pid)
    for sid in list(p.secret_objectives):
        if SECRET_OBJECTIVES[sid](state, pid):
            p.add_vp(2, "objective")
            p.secrets_scored.append(sid)
            p.secret_objectives.remove(sid)


def deal_secret_draw(
    state: GameState,
    pid: int,
    rng: random.Random,
) -> Optional[dict]:
    """Draw one secret for pid. Returns cap-resolution payload if at cap."""
    p = state.player(pid)
    if len(p.secret_objectives) < SECRET_CAP:
        card = draw_secret_card(state, rng)
        if card:
            p.secret_objectives.append(card)
            try_immediate_secrets(state, pid)
        return None
    drawn = [draw_secret_card(state, rng) for _ in range(2)]
    drawn = [c for c in drawn if c]
    if not drawn:
        return None
    return {"kind": "secret_cap", "pid": pid, "drawn": drawn, "step": "keep"}


def deal_round3_secrets(state: GameState, rng: random.Random) -> list[dict]:
    pending: list[dict] = []
    for p in state.players:
        payload = deal_secret_draw(state, p.pid, rng)
        if payload:
            pending.append(payload)
    return pending


def winds_draw_choices(state: GameState, pid: int) -> list[dict]:
    choices = [{"type": "obj_draw_secret"}]
    if state.shared_public_deck and len(state.shared_public_revealed) < len(PUBLIC_OBJECTIVE_IDS):
        choices.append({"type": "obj_draw_public"})
    return choices


def secret_cap_keep_choices(drawn: list[str]) -> list[dict]:
    choices = [{"type": "obj_keep", "card": c} for c in drawn]
    choices.append({"type": "obj_keep_none"})
    return choices


def secret_cap_discard_choices(secrets: list[str]) -> list[dict]:
    return [{"type": "obj_discard", "card": c} for c in secrets]


def apply_secret_keep(
    state: GameState,
    pid: int,
    kept: Optional[str],
    drawn: list[str],
    rng: random.Random,
) -> Optional[dict]:
    """Apply keep/discard for draw-2-keep-1. Returns discard step if needed."""
    for card in drawn:
        if card != kept:
            discard_secret_card(state, card)
    if kept is None:
        return None
    p = state.player(pid)
    if len(p.secret_objectives) >= SECRET_CAP:
        return {"kind": "secret_cap", "pid": pid, "kept": kept, "step": "discard"}
    p.secret_objectives.append(kept)
    try_immediate_secrets(state, pid)
    return None


def apply_secret_discard_at_cap(state: GameState, pid: int, kept: str, discard_id: str) -> None:
    p = state.player(pid)
    if discard_id in p.secret_objectives:
        p.secret_objectives.remove(discard_id)
        discard_secret_card(state, discard_id)
    if kept not in p.secret_objectives:
        p.secret_objectives.append(kept)
    try_immediate_secrets(state, pid)
