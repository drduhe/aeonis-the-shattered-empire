"""Objective predicates and secret draw economy (First Playable §4.4, Objectives.md §3)."""
from __future__ import annotations

import random
from itertools import combinations
from typing import TYPE_CHECKING, Optional

from .hexmap import distance
from .types import BuildingType, Terrain, UnitType, PUBLIC_OBJECTIVE_VP

if TYPE_CHECKING:
    from .types import GameState

# --- Public shared row ---

FIRST_PLAYABLE_PUBLIC_OBJECTIVE_IDS = (
    "frontier_lord",
    "builder",
    "merchant_lord",
    "portal_mastery",
    "warlord",
    "seat_of_empire",
)

STAGE_I_PUBLIC_OBJECTIVE_IDS = (
    "frontier_lord",
    "builder",
    "council_power",
    "portal_mastery",
    "warlord",
    "seat_of_empire",
    "twin_cities",
    "adept_of_the_schools",
    "voice_of_the_realm",
    "relic_seeker",
    "merchant_lord",
    "standing_army",
)

STAGE_II_PUBLIC_OBJECTIVE_IDS = (
    "dominion",
    "prosperous_realm",
    "living_legend",
    "crossroads_of_empire",
    "archmage",
    "breaker_of_walls",
    "conqueror",
    "hold_the_line",
    "lawgiver",
    "beacon_of_renown",
    "imperial_treasury",
    "reliquary",
)

PUBLIC_OBJECTIVE_IDS = STAGE_I_PUBLIC_OBJECTIVE_IDS + STAGE_II_PUBLIC_OBJECTIVE_IDS

# E3 staged row: economy cards fixed in opening 2 (First Playable PROPOSED experiment).
STAGED_ECONOMY_OPENING = ("builder", "merchant_lord")

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


def setup_shared_public_row(
    rng: random.Random,
    objectives_config: dict | None = None,
) -> tuple[list[str], list[str], list[str]]:
    """Deal opening shared row, Stage I remainder, and staged Stage II deck.

    Default is the six-card First Playable row. ``full_public_deck`` enables
    the audited 24-card deck; ``exclude_public_ids`` removes modules that are
    outside a sim scope (notably Archmage while Tier II is disabled).
    """
    objectives_config = objectives_config or {}
    opening = objectives_config.get("opening_public_ids")
    if opening is None and objectives_config.get("staged_economy_opening"):
        opening = list(STAGED_ECONOMY_OPENING)
    if objectives_config.get("full_public_deck"):
        excluded = {str(x) for x in objectives_config.get("exclude_public_ids", [])}
        stage_one = [x for x in STAGE_I_PUBLIC_OBJECTIVE_IDS if x not in excluded]
        stage_two = [x for x in STAGE_II_PUBLIC_OBJECTIVE_IDS if x not in excluded]
    else:
        stage_one = list(FIRST_PLAYABLE_PUBLIC_OBJECTIVE_IDS)
        stage_two = []
    public_deck = list(stage_one)
    if opening is not None:
        opening = [str(x) for x in opening]
        for oid in opening:
            if oid not in public_deck:
                raise ValueError(f"unknown opening public objective: {oid}")
        if len(opening) > 2:
            raise ValueError("opening_public_ids exceeds First Playable opening size (2)")
        for oid in opening:
            public_deck.remove(oid)
        rng.shuffle(public_deck)
        revealed = list(opening)
        while len(revealed) < 2:
            revealed.append(public_deck.pop())
        rng.shuffle(stage_two)
        return revealed, public_deck, stage_two
    rng.shuffle(public_deck)
    rng.shuffle(stage_two)
    return [public_deck.pop(), public_deck.pop()], public_deck, stage_two


def _frontier_lord(state, pid) -> bool:
    return len(state.controlled(pid)) >= state.frontier_lord_min_hexes


def _builder(state, pid) -> bool:
    return sum(len(t.buildings) for t in state.controlled(pid)) >= state.builder_min_buildings


def _merchant_lord(state, pid) -> bool:
    return state.player(pid).gold >= state.merchant_lord_min_gold


def _progress(state, pid: int, obj_id: str) -> int:
    return int(state.player(pid).public_objective_progress.get(obj_id, 0))


def record_public_progress(state, pid: int, obj_id: str, amount: int = 1) -> None:
    """Track a cumulative public objective only after it is revealed."""
    p = state.player(pid)
    if obj_id not in state.shared_public_revealed or obj_id in p.shared_scored:
        return
    p.public_objective_progress[obj_id] = _progress(state, pid, obj_id) + amount


def _portal_mastery(state, pid) -> bool:
    controls_portal = any(t.terrain == Terrain.PORTAL for t in state.controlled(pid))
    return controls_portal and _progress(state, pid, "portal_mastery") >= 1


def _warlord(state, pid) -> bool:
    return _progress(state, pid, "warlord") >= 2


def _seat_of_empire(state, pid) -> bool:
    return any(t.imperial_seat for t in state.controlled(pid))


def _council_power(state, pid) -> bool:
    return _progress(state, pid, "council_power") >= 4


def _city_count(state, pid: int) -> int:
    return sum(1 for t in state.controlled(pid) if t.imperial_seat or t.terrain == Terrain.CITY)


def _twin_cities(state, pid) -> bool:
    return _city_count(state, pid) >= 2


def _adept_of_the_schools(state, pid) -> bool:
    return len(state.player(pid).discoveries) >= 2


def _voice_of_the_realm(state, pid) -> bool:
    return state.player(pid).renown >= 5


def _artifact_count(state, pid: int) -> int:
    p = state.player(pid)
    attached = sum(1 for t in state.controlled(pid) if t.building_relic)
    return len(p.lord_equipment) + len(p.utilities) + attached + (1 if p.pending_building_relic else 0)


def _relic_seeker(state, pid) -> bool:
    return _artifact_count(state, pid) >= 1


def _realm_of_plenty(state, pid) -> bool:
    standard = {Terrain.PLAINS, Terrain.FOREST, Terrain.MOUNTAIN, Terrain.DESERT}
    return len({t.terrain for t in state.controlled(pid) if t.terrain in standard}) >= 3


def _standing_army(state, pid) -> bool:
    return sum(1 for _, u in state.units_of(pid) if u.type != UnitType.LORD) >= 8


def _dominion(state, pid) -> bool:
    return len(state.controlled(pid)) >= 12


def _master_of_cities(state, pid) -> bool:
    return _city_count(state, pid) >= 3


def _prosperous_realm(state, pid) -> bool:
    buildings = sum(len(t.buildings) for t in state.controlled(pid))
    return buildings >= 5 and state.pop_cap(pid) >= 12


def _living_legend(state, pid) -> bool:
    from .lords.legendaries import LEGENDARY_BUILDINGS, legendary_for_lord
    expected = legendary_for_lord(state.player(pid).lord_id)
    return expected in LEGENDARY_BUILDINGS and any(
        expected in t.buildings for t in state.controlled(pid)
    )


def _crossroads_of_empire(state, pid) -> bool:
    special = {Terrain.CITY, Terrain.RUINS, Terrain.PORTAL}
    return sum(
        1 for t in state.controlled(pid)
        if t.imperial_seat or t.terrain in special
    ) >= 4


def _archmage(state, pid) -> bool:
    # Tier II is outside the First Playable simulator; audit configs exclude
    # this card. Keep the predicate false instead of encoding a false proxy.
    return False


def _breaker_of_walls(state, pid) -> bool:
    return _progress(state, pid, "breaker_of_walls") >= 1


def _conqueror(state, pid) -> bool:
    return _progress(state, pid, "conqueror") >= 5


def _hold_the_line(state, pid) -> bool:
    return _progress(state, pid, "hold_the_line") >= 2


def _lawgiver(state, pid) -> bool:
    return _progress(state, pid, "lawgiver") >= 2


def _beacon_of_renown(state, pid) -> bool:
    return state.player(pid).renown >= 10


def _imperial_treasury(state, pid) -> bool:
    p = state.player(pid)
    return p.gold + p.mana + p.influence >= 20


def _reliquary(state, pid) -> bool:
    return _artifact_count(state, pid) >= 3


PUBLIC_OBJECTIVES = {
    "frontier_lord": _frontier_lord,
    "builder": _builder,
    "merchant_lord": _merchant_lord,
    "council_power": _council_power,
    "portal_mastery": _portal_mastery,
    "warlord": _warlord,
    "seat_of_empire": _seat_of_empire,
    "twin_cities": _twin_cities,
    "adept_of_the_schools": _adept_of_the_schools,
    "voice_of_the_realm": _voice_of_the_realm,
    "relic_seeker": _relic_seeker,
    "realm_of_plenty": _realm_of_plenty,
    "standing_army": _standing_army,
    "dominion": _dominion,
    "master_of_cities": _master_of_cities,
    "prosperous_realm": _prosperous_realm,
    "living_legend": _living_legend,
    "crossroads_of_empire": _crossroads_of_empire,
    "archmage": _archmage,
    "breaker_of_walls": _breaker_of_walls,
    "conqueror": _conqueror,
    "hold_the_line": _hold_the_line,
    "lawgiver": _lawgiver,
    "beacon_of_renown": _beacon_of_renown,
    "imperial_treasury": _imperial_treasury,
    "reliquary": _reliquary,
}


def public_objective_vp(state, obj_id: str) -> int:
    """VP awarded for scoring a public row card (seat sweep S1 varies seat_of_empire)."""
    if obj_id == "seat_of_empire":
        return state.seat_of_empire_vp
    return PUBLIC_OBJECTIVE_VP


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


def _merge_stage_two(state: GameState, rng: random.Random) -> None:
    if not state.shared_public_stage_two:
        return
    state.shared_public_deck.extend(state.shared_public_stage_two)
    state.shared_public_stage_two = []
    rng.shuffle(state.shared_public_deck)


def draw_public_to_row(
    state: GameState,
    rng: random.Random,
    *,
    round_start: bool = False,
) -> bool:
    """Reveal one shared objective, respecting Stage II timing."""
    if state.shared_public_stage_two and (
        (round_start and state.round >= 4) or not state.shared_public_deck
    ):
        _merge_stage_two(state, rng)
    if not state.shared_public_deck:
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
    if state.shared_public_deck or state.shared_public_stage_two:
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
