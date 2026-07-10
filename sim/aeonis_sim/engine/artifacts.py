"""Artifact system (Artifacts.md / First Playable §4.8).

24-card deck, Remnant purge-draw, event-driven sites, three ownership
categories, and VP relic scoring at Cleanup & Checks.
"""
from __future__ import annotations

import random
from typing import TYPE_CHECKING, Optional

from .hexmap import distance
from .types import BuildingType, Terrain, UNIT_STATS, UnitType

if TYPE_CHECKING:
    from .types import GameState

ARTIFACT_CARD_IDS: tuple[str, ...] = (
    "blade_of_the_last_emperor",
    "crown_of_aeonis",
    "voidwalkers_cloak",
    "emberstone_gauntlet",
    "wardens_aegis",
    "whisperers_mask",
    "scepter_of_command",
    "ley_line_conduit",
    "titans_cornerstone",
    "eternal_forge",
    "verdant_hearthstone",
    "astral_beacon",
    "archive_of_the_fallen",
    "shard_of_the_throne",
    "cartographers_glass",
    "scroll_of_dominion",
    "tome_of_forbidden_rites",
    "mask_of_many_faces",
    "wellspring_chalice",
    "imperial_seal",
    "echo_of_the_world_tree",
    "mercenary_contract",
    "windcallers_horn",
    "shroud_of_nightfall",
)

VP_ARTIFACTS = frozenset({
    "crown_of_aeonis",
    "eternal_forge",
    "shard_of_the_throne",
    "imperial_seal",
})

LORD_EQUIPMENT = frozenset({
    "blade_of_the_last_emperor",
    "crown_of_aeonis",
    "voidwalkers_cloak",
    "emberstone_gauntlet",
    "wardens_aegis",
    "whisperers_mask",
    "scepter_of_command",
})

BUILDING_RELICS = frozenset({
    "ley_line_conduit",
    "titans_cornerstone",
    "eternal_forge",
    "verdant_hearthstone",
    "astral_beacon",
    "archive_of_the_fallen",
})

BUILDING_RELIC_TARGETS: dict[str, frozenset[BuildingType] | None] = {
    "ley_line_conduit": frozenset({BuildingType.ACADEMY, BuildingType.GROVE}),
    "titans_cornerstone": frozenset({BuildingType.FORTRESS, BuildingType.TOWER}),
    "eternal_forge": frozenset({BuildingType.FORGE}),
    "verdant_hearthstone": frozenset({BuildingType.FARM}),
    "astral_beacon": None,  # any building on a Portal hex
    "archive_of_the_fallen": frozenset({BuildingType.ACADEMY}),
}

_DIE_UP = {4: 6, 6: 8, 8: 10, 10: 12}


def init_artifact_deck(rng: random.Random) -> list[str]:
    deck = list(ARTIFACT_CARD_IDS)
    rng.shuffle(deck)
    return deck


def draw_artifact(state: GameState) -> str | None:
    if not state.artifact_deck:
        return None
    return state.artifact_deck.pop()


def return_to_deck_bottom(state: GameState, card_id: str) -> None:
    state.artifact_deck.insert(0, card_id)


def _key(coord) -> str:
    return f"{coord[0]},{coord[1]}"


def has_site(state: GameState, coord) -> bool:
    return _key(coord) in state.artifact_sites


def place_site(state: GameState, coord) -> bool:
    """Place site marker + face-up artifact card. Returns False if deck empty."""
    card = draw_artifact(state)
    if card is None:
        return False
    state.artifact_sites[_key(coord)] = {"card_id": card, "owner": None}
    return True


def pick_neutral_ruins_hex(state: GameState) -> Optional[tuple]:
    for t in state.tiles.values():
        if t.terrain == Terrain.RUINS and t.controller is None:
            return t.coord
    for t in state.tiles.values():
        if t.controller is None and not t.imperial_seat:
            return t.coord
    return None


def pick_seat_adjacent_site_hex(
    state: GameState,
    speaker_home: tuple | None = None,
) -> Optional[tuple]:
    seat = next((t.coord for t in state.tiles.values() if t.imperial_seat), None)
    if seat is None:
        return None
    cands = [
        t.coord for t in state.tiles.values()
        if not has_site(state, t.coord)
    ]
    if not cands:
        return None
    if speaker_home is None:
        return min(cands, key=lambda c: distance(c, seat))
    return min(
        cands,
        key=lambda c: (distance(c, seat), c[0] - speaker_home[0], c[1] - speaker_home[1]),
    )


def eligible_attach_hexes(state: GameState, pid: int, card_id: str) -> list[tuple]:
    targets = BUILDING_RELIC_TARGETS.get(card_id)
    out = []
    for t in state.controlled(pid):
        if t.building_relic is not None:
            continue
        if not t.buildings:
            continue
        if card_id == "astral_beacon":
            if t.terrain == Terrain.PORTAL:
                out.append(t.coord)
            continue
        if card_id == "verdant_hearthstone":
            if BuildingType.FARM in t.buildings or t.terrain == Terrain.CITY:
                out.append(t.coord)
            continue
        if targets is None:
            continue
        if any(b in targets for b in t.buildings):
            out.append(t.coord)
    return out


def attach_building_relic(state: GameState, pid: int, card_id: str, coord) -> None:
    tile = state.tiles[coord]
    if tile.controller != pid:
        raise ValueError("cannot attach on uncontrolled hex")
    if tile.building_relic is not None:
        raise ValueError("building already has relic")
    tile.building_relic = card_id
    p = state.player(pid)
    if p.pending_building_relic == card_id:
        p.pending_building_relic = None


def _bump_lord_hp(state: GameState, pid: int, delta: int) -> None:
    for _, u in state.units_of(pid):
        if u.type == UnitType.LORD:
            u.hp = max(1, u.hp + delta)


def gain_artifact(state: GameState, pid: int, card_id: str) -> str | None:
    """Assign artifact to player. Returns pending kind or None.

    pending kinds: 'discard_lord' | 'attach_building'
    """
    p = state.player(pid)
    if card_id in LORD_EQUIPMENT:
        p.lord_equipment.append(card_id)
        if card_id == "wardens_aegis":
            _bump_lord_hp(state, pid, 1)
        if len(p.lord_equipment) > 2:
            return "discard_lord"
    elif card_id in BUILDING_RELICS:
        hexes = eligible_attach_hexes(state, pid, card_id)
        if not hexes:
            p.pending_building_relic = card_id
            return "attach_building"
        if len(hexes) == 1:
            attach_building_relic(state, pid, card_id, hexes[0])
        else:
            p.pending_building_relic = card_id
            return "attach_building"
    else:
        p.utilities.append(card_id)
    return None


def discard_lord_equipment(state: GameState, pid: int, card_id: str) -> None:
    p = state.player(pid)
    if card_id not in p.lord_equipment:
        raise ValueError("lord equipment not held")
    p.lord_equipment.remove(card_id)
    if card_id == "wardens_aegis":
        _bump_lord_hp(state, pid, -1)
    return_to_deck_bottom(state, card_id)


def transfer_lord_equipment(state: GameState, from_pid: int, to_pid: int) -> str | None:
    """Captor takes all Lord Equipment. Returns pending discard kind if needed."""
    src = state.player(from_pid)
    dst = state.player(to_pid)
    cards = list(src.lord_equipment)
    src.lord_equipment.clear()
    pending = None
    for card_id in cards:
        dst.lord_equipment.append(card_id)
        if len(dst.lord_equipment) > 2:
            pending = "discard_lord"
    return pending


def transfer_building_relics_on_capture(state: GameState, coord, new_pid: int) -> None:
    """Building relic stays on hex; new controller benefits (Artifacts.md)."""
    tile = state.tiles[coord]
    if tile.building_relic is None:
        return
    # No player-area field — relic remains attached to the building.
    _ = new_pid


def maybe_transfer_shard(state: GameState, loser_pid: int, winner_pid: int, lord_present: bool) -> None:
    if not lord_present:
        return
    p = state.player(loser_pid)
    if "shard_of_the_throne" not in p.utilities:
        return
    p.utilities.remove("shard_of_the_throne")
    state.player(winner_pid).utilities.append("shard_of_the_throne")


def enumerate_purge_draw(state: GameState, pid: int) -> list[dict]:
    p = state.player(pid)
    if p.remnants < 3 or not state.artifact_deck:
        return []
    return [{"type": "artifact_purge_draw"}]


def apply_purge_draw(state: GameState, pid: int) -> str | None:
    p = state.player(pid)
    if p.remnants < 3:
        raise ValueError("insufficient remnants")
    card = draw_artifact(state)
    if card is None:
        raise ValueError("artifact deck empty")
    p.remnants -= 3
    return gain_artifact(state, pid, card)


def enumerate_site_claims(state: GameState, pid: int) -> list[dict]:
    if state.player(pid).ap < 1:
        return []
    out = []
    for key, site in state.artifact_sites.items():
        if site.get("owner") is not None or not site.get("card_id"):
            continue
        q, r = key.split(",")
        coord = (int(q), int(r))
        tile = state.tiles[coord]
        if not any(u.owner == pid for u in tile.units):
            continue
        out.append({
            "type": "artifact_claim",
            "hex": list(coord),
            "card": site["card_id"],
        })
    return out


def apply_site_claim(state: GameState, pid: int, coord) -> str | None:
    site = state.artifact_sites.get(_key(coord))
    if site is None or site.get("owner") is not None:
        raise ValueError("no claimable site")
    card_id = site["card_id"]
    if not card_id:
        raise ValueError("site has no card")
    tile = state.tiles[coord]
    if not any(u.owner == pid for u in tile.units):
        raise ValueError("no unit on site")
    p = state.player(pid)
    if p.ap < 1:
        raise ValueError("insufficient AP")
    p.ap -= 1
    del state.artifact_sites[_key(coord)]
    return gain_artifact(state, pid, card_id)


def enumerate_attach_choices(state: GameState, pid: int) -> list[dict]:
    p = state.player(pid)
    if not p.pending_building_relic:
        return []
    card_id = p.pending_building_relic
    return [
        {"type": "artifact_attach", "hex": list(h), "card": card_id}
        for h in eligible_attach_hexes(state, pid, card_id)
    ]


def enumerate_discard_lord(state: GameState, pid: int) -> list[dict]:
    p = state.player(pid)
    if len(p.lord_equipment) <= 2:
        return []
    return [
        {"type": "artifact_discard_lord", "card": c}
        for c in p.lord_equipment
    ]


def score_artifact_vp(state: GameState, pid: int) -> None:
    """+1 VP per VP-bearing artifact held (Cleanup & Checks)."""
    p = state.player(pid)
    for card_id in p.lord_equipment:
        if card_id in VP_ARTIFACTS:
            p.add_vp(1, "artifact")
    for card_id in p.utilities:
        if card_id in VP_ARTIFACTS:
            p.add_vp(1, "artifact")
    for t in state.controlled(pid):
        if t.building_relic in VP_ARTIFACTS:
            p.add_vp(1, "artifact")


def attack_die(state: GameState, pid: int, unit) -> int:
    die = UNIT_STATS[unit.type].attack_die
    if unit.type == UnitType.LORD:
        from .lords import lord_attack_die
        die = lord_attack_die(state, pid, die)
    if unit.type == UnitType.LORD and "blade_of_the_last_emperor" in state.player(pid).lord_equipment:
        die = _DIE_UP.get(die, die)
    return die


def defense_die(state: GameState, pid: int, unit, battle_target_coord) -> int:
    die = UNIT_STATS[unit.type].defense_die
    if unit.type == UnitType.LORD:
        from .lords import lord_defense_die
        die = lord_defense_die(state, pid, die)
    tile = state.tiles[battle_target_coord]
    if (
        unit.owner == pid
        and unit.type != UnitType.LORD
        and "wardens_aegis" in state.player(pid).lord_equipment
    ):
        lord_here = any(
            u.owner == pid and u.type == UnitType.LORD for u in tile.units
        )
        if lord_here:
            die = _DIE_UP.get(die, die)
    if tile.building_relic == "titans_cornerstone":
        die = _DIE_UP.get(die, die)
    return die


def lord_move_bonus(state: GameState, pid: int) -> int:
    if "voidwalkers_cloak" in state.player(pid).lord_equipment:
        return 1
    return 0


def council_influence_bonus(state: GameState, pid: int) -> int:
    if "crown_of_aeonis" in state.player(pid).lord_equipment:
        return 2
    return 0


def production_wellspring(state: GameState, pid: int) -> None:
    """AL-32: auto-pick Gold when holding Wellspring Chalice."""
    if "wellspring_chalice" not in state.player(pid).utilities:
        return
    state.player(pid).gold += 2


def production_verdant_bonus(tile) -> int:
    if tile.building_relic != "verdant_hearthstone":
        return 0
    return 2


def production_adjacent_gold(state: GameState, pid: int, tile) -> int:
    from .hexmap import neighbors
    bonus = 0
    for t in state.controlled(pid):
        if t.building_relic != "verdant_hearthstone":
            continue
        for nb in neighbors(t.coord):
            if nb == tile.coord:
                bonus += 1
                break
    return bonus


def production_ley_line_mana(tile) -> int:
    if tile.building_relic == "ley_line_conduit":
        return 2
    return 0


def recruit_gold_discount(state: GameState, pid: int, coord) -> int:
    tile = state.tiles[coord]
    if tile.building_relic == "eternal_forge":
        return 1
    return 0


def owned_artifacts(state: GameState, pid: int) -> list[str]:
    p = state.player(pid)
    out = list(p.lord_equipment) + list(p.utilities)
    if p.pending_building_relic:
        out.append(p.pending_building_relic)
    for t in state.controlled(pid):
        if t.building_relic:
            out.append(t.building_relic)
    return out
