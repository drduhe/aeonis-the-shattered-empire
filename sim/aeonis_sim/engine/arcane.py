"""Arcane Tier I research (Arcane.md / First Playable §4.6).

First Playable: Tier I only; sigil prerequisites deferred (AL-35).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .types import BuildingType

if TYPE_CHECKING:
    from .types import GameState

from .lords import controls_unique, mark_round_used, round_unused
from .lords.discoveries import (
    FACTION_DISCOVERIES,
    FACTION_DISCOVERY_IDS,
    apply_faction_research,
    can_afford_faction_research,
    guild_contracts_market_discount,
    mark_guild_contracts_market_used,
)

TIER_I_AP = 1
TIER_I_REMNANTS = 1

BASIC_PRODUCTION = frozenset({
    BuildingType.FARM,
    BuildingType.MINE,
    BuildingType.GROVE,
    BuildingType.EMBASSY,
})

STONEBUILD = frozenset({
    BuildingType.TOWER,
    BuildingType.FORTRESS,
    BuildingType.BRIDGE,
})


@dataclass(frozen=True)
class DiscoverySpec:
    id: str
    mana: int = 0
    gold: int = 0
    influence: int = 0
    kind: str = "passive"  # passive | ritual


TIER_I_DISCOVERY_IDS: tuple[str, ...] = (
    "battle_runes",
    "searing_salvo",
    "sigiled_masonry",
    "warding_charm",
    "scrying_pool",
    "battle_augury",
    "golden_alchemy",
    "waystones",
    "boundary_stones",
    "stonewright",
)

DISCOVERIES: dict[str, DiscoverySpec] = {
    "battle_runes": DiscoverySpec("battle_runes", mana=2, kind="ritual"),
    "searing_salvo": DiscoverySpec("searing_salvo", mana=2, kind="ritual"),
    "sigiled_masonry": DiscoverySpec("sigiled_masonry", mana=1, gold=1),
    "warding_charm": DiscoverySpec("warding_charm", mana=2, kind="ritual"),
    "scrying_pool": DiscoverySpec("scrying_pool", influence=2),
    "battle_augury": DiscoverySpec("battle_augury", mana=1, influence=1, kind="ritual"),
    "golden_alchemy": DiscoverySpec("golden_alchemy", mana=2),
    "waystones": DiscoverySpec("waystones", mana=1, gold=1),
    "boundary_stones": DiscoverySpec("boundary_stones", mana=1, influence=1),
    "stonewright": DiscoverySpec("stonewright", mana=1, gold=1),
}


def has_academy_discount(state: GameState, pid: int) -> bool:
    from .types import BuildingType as BT
    p = state.player(pid)
    if p.arcane_round.get("academy_discount"):
        return False
    return any(t.active(BT.ACADEMY) for t in state.controlled(pid))


def _mana_after_academy(
    state: GameState,
    pid: int,
    spec: DiscoverySpec,
    *,
    free: bool,
) -> int:
    if free:
        return 0
    mana = spec.mana
    if has_academy_discount(state, pid):
        mana = max(0, mana - 1)
    return mana


def research_resource_cost(
    state: GameState,
    pid: int,
    spec: DiscoverySpec,
    *,
    free: bool,
) -> tuple[int, int, int]:
    if free:
        return 0, 0, 0
    mana = _mana_after_academy(state, pid, spec, free=free)
    gold, inf = spec.gold, spec.influence
    if (
        controls_unique(state, pid, "arcane_nexus")
        and round_unused(state, pid, "nexus_discount")
        and mana > 0
    ):
        mana = max(0, mana - 1)
    return mana, gold, inf


def can_afford_research(
    state: GameState,
    pid: int,
    discovery_id: str,
    *,
    free: bool,
    ap_waived: bool = False,
) -> bool:
    p = state.player(pid)
    if discovery_id in p.discoveries:
        return False
    if discovery_id not in DISCOVERIES:
        return False
    if not free and not ap_waived and p.ap < TIER_I_AP:
        return False
    mana, gold, inf = research_resource_cost(state, pid, DISCOVERIES[discovery_id], free=free)
    return p.mana >= mana and p.gold >= gold and p.influence >= inf


def enumerate_research(
    state: GameState,
    pid: int,
    *,
    free: bool = False,
    ap_waived: bool = False,
) -> list[dict]:
    out = []
    for did in TIER_I_DISCOVERY_IDS:
        if not can_afford_research(state, pid, did, free=free, ap_waived=ap_waived):
            continue
        ap = 0 if (free or ap_waived) else TIER_I_AP
        out.append({
            "type": "research",
            "discovery": did,
            "free": free,
            "cost": ap,
        })
    for did in FACTION_DISCOVERY_IDS:
        if not can_afford_faction_research(
            state, pid, did, free=free, ap_waived=ap_waived,
        ):
            continue
        ap = 0 if (free or ap_waived) else TIER_I_AP
        out.append({
            "type": "research",
            "discovery": did,
            "free": free,
            "cost": ap,
        })
    return out


def apply_research(
    state: GameState,
    pid: int,
    discovery_id: str,
    *,
    free: bool = False,
    ap_waived: bool = False,
) -> None:
    if discovery_id in FACTION_DISCOVERIES:
        apply_faction_research(
            state, pid, discovery_id, free=free, ap_waived=ap_waived,
        )
        return
    if discovery_id not in DISCOVERIES:
        raise ValueError(f"unknown discovery: {discovery_id}")
    p = state.player(pid)
    if discovery_id in p.discoveries:
        raise ValueError("already owned")
    spec = DISCOVERIES[discovery_id]
    mana_after_academy_val = _mana_after_academy(state, pid, spec, free=free)
    mana, gold, inf = research_resource_cost(state, pid, spec, free=free)
    if not free and not ap_waived:
        if p.whisper_flags.pop("free_research_ap", False):
            pass
        else:
            if p.ap < TIER_I_AP:
                raise ValueError("insufficient AP")
            p.ap -= TIER_I_AP
    if p.mana < mana or p.gold < gold or p.influence < inf:
        raise ValueError("cannot afford research")
    if not free and has_academy_discount(state, pid):
        p.arcane_round["academy_discount"] = True
    if (
        not free
        and controls_unique(state, pid, "arcane_nexus")
        and round_unused(state, pid, "nexus_discount")
        and mana_after_academy_val > 0
    ):
        mark_round_used(state, pid, "nexus_discount")
    p.mana -= mana
    p.gold -= gold
    p.influence -= inf
    p.discoveries.append(discovery_id)
    p.remnants += TIER_I_REMNANTS


def build_gold_cost(
    state: GameState,
    pid: int,
    btype: BuildingType,
    base: int,
    *,
    tile=None,
) -> int:
    p = state.player(pid)
    gold = base
    if (
        "sigiled_masonry" in p.discoveries
        and not p.arcane_round.get("sigiled_masonry")
        and btype in BASIC_PRODUCTION
    ):
        gold = max(0, gold - 1)
    if (
        "stonewright" in p.discoveries
        and not p.arcane_round.get("stonewright")
        and btype in STONEBUILD
    ):
        gold = max(0, gold - 1)
    gold = guild_contracts_market_discount(state, pid, btype, gold)
    if tile is not None:
        if (
            btype == BuildingType.MINE
            and tile.unique_tile_id == "ironworks_ridge"
            and controls_unique(state, pid, "ironworks_ridge")
        ):
            gold = max(0, gold - 1)
        if (
            btype == BuildingType.FORTRESS
            and tile.unique_tile_id == "ironworks_ridge"
            and controls_unique(state, pid, "ironworks_ridge")
            and round_unused(state, pid, "ironworks_fortress")
        ):
            gold = max(0, gold - 1)
    return gold


def mark_build_discount_used(state: GameState, pid: int, btype: BuildingType, base: int) -> None:
    p = state.player(pid)
    if (
        "sigiled_masonry" in p.discoveries
        and btype in BASIC_PRODUCTION
        and build_gold_cost(state, pid, btype, base) < base
    ):
        p.arcane_round["sigiled_masonry"] = True
    if (
        "stonewright" in p.discoveries
        and btype in STONEBUILD
        and build_gold_cost(state, pid, btype, base) < base
    ):
        p.arcane_round["stonewright"] = True
    mark_guild_contracts_market_used(state, pid, btype)


def waystones_move_discount(state: GameState, pid: int, cost: int) -> int:
    p = state.player(pid)
    if cost <= 0:
        return cost
    if "waystones" not in p.discoveries or p.arcane_round.get("waystones"):
        return cost
    return max(1, cost - 1)


def mark_waystones_used(state: GameState, pid: int) -> None:
    if "waystones" in state.player(pid).discoveries:
        state.player(pid).arcane_round["waystones"] = True


def production_golden_alchemy(state: GameState, pid: int) -> None:
    p = state.player(pid)
    if "golden_alchemy" not in p.discoveries:
        return
    if p.arcane_round.get("golden_alchemy"):
        return
    if p.mana >= 2:
        p.mana -= 2
        p.gold += 3
        p.arcane_round["golden_alchemy"] = True


def apply_boundary_stones(state: GameState, pid: int) -> bool:
    """Auto-heuristic: claim first eligible neutral (AL-36). Returns True if claimed."""
    from .hexmap import neighbors
    from .types import Terrain

    p = state.player(pid)
    if "boundary_stones" not in p.discoveries:
        return False
    if p.arcane_round.get("boundary_stones"):
        return False
    anchors = [
        t for t in state.controlled(pid)
        if t.terrain == Terrain.CITY or t.has(BuildingType.TOWER)
    ]
    cands = []
    for anchor in anchors:
        for nb in neighbors(anchor.coord):
            tile = state.tiles.get(nb)
            if tile is None or tile.controller is not None:
                continue
            if tile.imperial_seat:
                continue
            if any(u.owner != pid for u in tile.units):
                continue
            cands.append(tile.coord)
    if not cands:
        return False
    coord = min(cands)
    state.tiles[coord].controller = pid
    p.arcane_round["boundary_stones"] = True
    return True


# --- Combat ritual heuristics (AL-36: auto-resolve in sim) ---

def searing_salvo_damage(state: GameState, attacker: int, battle) -> None:
    p = state.player(attacker)
    if "searing_salvo" not in p.discoveries or p.arcane_round.get("searing_salvo"):
        return
    if p.mana < 2:
        return
    line = battle.def_line if battle.def_line else [
        u for _, u in battle.def_committed
    ]
    if not line:
        return
    target = min(line, key=lambda u: (u.hp, u.uid))
    p.mana -= 2
    p.arcane_round["searing_salvo"] = True
    target.hp -= 1
    if target.hp <= 0:
        from . import combat
        combat._kill(state, battle, target)


def battle_runes_attack_bonus(state: GameState, pid: int, battle) -> int:
    p = state.player(pid)
    key = f"battle_runes_r{battle.rounds}"
    if "battle_runes" not in p.discoveries or p.arcane_round.get(key):
        return 0
    if p.mana < 1:
        return 0
    p.mana -= 1
    p.arcane_round[key] = True
    return 1


def warding_charm_defense_bonus(state: GameState, pid: int, battle) -> int:
    p = state.player(pid)
    key = f"warding_charm_r{battle.rounds}"
    if "warding_charm" not in p.discoveries or p.arcane_round.get(key):
        return 0
    if p.mana < 1:
        return 0
    p.mana -= 1
    p.arcane_round[key] = True
    return 1


def battle_augury_attack_penalty(state: GameState, pid: int, battle) -> int:
    p = state.player(pid)
    key = f"battle_augury_r{battle.rounds}"
    if "battle_augury" not in p.discoveries or p.arcane_round.get(key):
        return 0
    if p.influence < 1:
        return 0
    p.influence -= 1
    p.arcane_round[key] = True
    return 1
