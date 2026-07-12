"""M4 faction discoveries: catalog and effect hooks."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ..types import BuildingType, Terrain, UnitType
from .specs import is_lord, mark_round_used, round_unused

if TYPE_CHECKING:
    from ..types import GameState

TIER_I_AP = 1
TIER_I_REMNANTS = 1


@dataclass(frozen=True)
class FactionDiscoverySpec:
    id: str
    lord_id: str
    gold: int = 0
    mana: int = 0
    influence: int = 0


FACTION_DISCOVERIES: dict[str, FactionDiscoverySpec] = {
    "guild_contracts": FactionDiscoverySpec("guild_contracts", "cassian", gold=2, influence=2),
    "diplomatic_tariffs": FactionDiscoverySpec("diplomatic_tariffs", "cassian", influence=3),
    "mana_nexus": FactionDiscoverySpec("mana_nexus", "seraphel", mana=4, gold=1),
    "spellweave_doctrine": FactionDiscoverySpec("spellweave_doctrine", "seraphel", mana=2, influence=2),
    "reinforced_fortifications": FactionDiscoverySpec(
        "reinforced_fortifications", "vharok", gold=3, mana=1,
    ),
    "siege_logistics": FactionDiscoverySpec("siege_logistics", "vharok", gold=2, influence=2),
    "thornwatch": FactionDiscoverySpec("thornwatch", "elyndra", mana=3, influence=1),
    "seedbound_resilience": FactionDiscoverySpec("seedbound_resilience", "elyndra", mana=2, gold=2),
    "mirage_riders": FactionDiscoverySpec("mirage_riders", "rakhis", gold=3, mana=1),
    "sandsworn_pact": FactionDiscoverySpec("sandsworn_pact", "rakhis", influence=2, gold=2),
    "stolen_secrets": FactionDiscoverySpec("stolen_secrets", "nyxara", mana=2, influence=2),
    "shadow_network": FactionDiscoverySpec("shadow_network", "nyxara", mana=3, gold=1),
    "luminous_bulwark": FactionDiscoverySpec("luminous_bulwark", "auriel", mana=2, influence=2),
    "sacred_rite": FactionDiscoverySpec("sacred_rite", "auriel", influence=3, mana=1),
    "planar_echo": FactionDiscoverySpec("planar_echo", "thalrik", mana=3, gold=1),
    "void_anchor": FactionDiscoverySpec("void_anchor", "thalrik", mana=2, influence=2),
}

FACTION_DISCOVERY_IDS: tuple[str, ...] = tuple(FACTION_DISCOVERIES.keys())


def faction_research_cost(
    state: GameState,
    pid: int,
    discovery_id: str,
    *,
    free: bool,
) -> tuple[int, int, int]:
    if free:
        return 0, 0, 0
    spec = FACTION_DISCOVERIES[discovery_id]
    return spec.mana, spec.gold, spec.influence


def can_afford_faction_research(
    state: GameState,
    pid: int,
    discovery_id: str,
    *,
    free: bool,
    ap_waived: bool = False,
) -> bool:
    if discovery_id not in FACTION_DISCOVERIES:
        return False
    p = state.player(pid)
    if discovery_id in p.discoveries:
        return False
    spec = FACTION_DISCOVERIES[discovery_id]
    if not is_lord(state, pid, spec.lord_id):
        return False
    if not free and not ap_waived and p.ap < TIER_I_AP:
        return False
    mana, gold, inf = faction_research_cost(state, pid, discovery_id, free=free)
    return p.mana >= mana and p.gold >= gold and p.influence >= inf


def apply_faction_research(
    state: GameState,
    pid: int,
    discovery_id: str,
    *,
    free: bool = False,
    ap_waived: bool = False,
) -> None:
    if discovery_id not in FACTION_DISCOVERIES:
        raise ValueError(f"unknown faction discovery: {discovery_id}")
    p = state.player(pid)
    if discovery_id in p.discoveries:
        raise ValueError("already owned")
    spec = FACTION_DISCOVERIES[discovery_id]
    if not is_lord(state, pid, spec.lord_id):
        raise ValueError("wrong lord for faction discovery")
    mana, gold, inf = faction_research_cost(state, pid, discovery_id, free=free)
    if not free and not ap_waived:
        if p.whisper_flags.pop("free_research_ap", False):
            pass
        else:
            if p.ap < TIER_I_AP:
                raise ValueError("insufficient AP")
            p.ap -= TIER_I_AP
    if p.mana < mana or p.gold < gold or p.influence < inf:
        raise ValueError("cannot afford research")
    p.mana -= mana
    p.gold -= gold
    p.influence -= inf
    p.discoveries.append(discovery_id)
    p.remnants += TIER_I_REMNANTS


# --- Effect hooks ---


def guild_contracts_market_discount(state: GameState, pid: int, btype: BuildingType, gold: int) -> int:
    p = state.player(pid)
    if (
        "guild_contracts" in p.discoveries
        and btype == BuildingType.MARKET
        and not p.arcane_round.get("guild_contracts_market")
    ):
        return max(0, gold - 1)
    return gold


def mark_guild_contracts_market_used(state: GameState, pid: int, btype: BuildingType) -> None:
    p = state.player(pid)
    if "guild_contracts" in p.discoveries and btype == BuildingType.MARKET:
        p.arcane_round["guild_contracts_market"] = True


def apply_guild_contracts_trade_influence(state: GameState, pid: int, *, zero_ap_market: bool) -> bool:
    p = state.player(pid)
    if not zero_ap_market or "guild_contracts" not in p.discoveries:
        return False
    if not round_unused(state, pid, "guild_contracts_trade"):
        return False
    p.influence += 1
    mark_round_used(state, pid, "guild_contracts_trade")
    return True


def apply_diplomatic_tariffs(state: GameState, trader_pid: int) -> None:
    for p in state.players:
        pid = p.pid
        if pid == trader_pid:
            continue
        if "diplomatic_tariffs" not in p.discoveries:
            continue
        if not round_unused(state, pid, "diplomatic_tariffs"):
            continue
        if not any(t.active(BuildingType.EMBASSY) for t in state.controlled(pid)):
            continue
        p.gold += 1
        mark_round_used(state, pid, "diplomatic_tariffs")


def mana_nexus_bonus(state: GameState, pid: int) -> int:
    p = state.player(pid)
    if "mana_nexus" not in p.discoveries:
        return 0
    bonus = 0
    for t in state.controlled(pid):
        if t.terrain == Terrain.FOREST or t.has(BuildingType.GROVE):
            bonus += 1
    return bonus


def apply_spellweave_doctrine(state: GameState, pid: int, lobby_spent: int) -> bool:
    if lobby_spent <= 0:
        return False
    p = state.player(pid)
    if "spellweave_doctrine" not in p.discoveries:
        return False
    if not round_unused(state, pid, "spellweave_doctrine"):
        return False
    p.mana += 1
    mark_round_used(state, pid, "spellweave_doctrine")
    return True


def reinforced_fortifications_bonus(state: GameState, pid: int, tile) -> int:
    if "reinforced_fortifications" not in state.player(pid).discoveries:
        return 0
    return 1 if tile.has(BuildingType.TOWER) else 0


def apply_siege_logistics(state: GameState, pid: int, target_coord) -> bool:
    p = state.player(pid)
    if "siege_logistics" not in p.discoveries:
        return False
    if not round_unused(state, pid, "siege_logistics"):
        return False
    tile = state.tiles[target_coord]
    if tile.terrain != Terrain.CITY and not tile.has(BuildingType.FORTRESS):
        return False
    p.ap += 1
    mark_round_used(state, pid, "siege_logistics")
    return True


def thornwatch_bonus(state: GameState, battle, defender_unit) -> int:
    if battle.defender is None:
        return 0
    p = state.player(battle.defender)
    if "thornwatch" not in p.discoveries:
        return 0
    tile = state.tiles[battle.target]
    if tile.terrain != Terrain.FOREST:
        return 0
    if defender_unit.type != UnitType.ARCHER:
        return 0
    if defender_unit not in battle.def_line:
        return 0
    return 1


def apply_seedbound_resilience(state: GameState, pid: int, battle) -> bool:
    p = state.player(pid)
    if "seedbound_resilience" not in p.discoveries:
        return False
    if battle.defender != pid:
        return False
    if not round_unused(state, pid, "seedbound_resilience"):
        return False
    room = state.pop_cap(pid) - state.pop_used(pid) - p.pop_pool
    if room <= 0:
        return False
    p.pop_pool += 1
    mark_round_used(state, pid, "seedbound_resilience")
    return True


def mirage_riders_attack_bonus(state: GameState, pid: int, striker, origin_coord) -> int:
    if "mirage_riders" not in state.player(pid).discoveries:
        return 0
    if striker.type != UnitType.CAVALRY:
        return 0
    tile = state.tiles.get(origin_coord)
    if tile is None or tile.terrain != Terrain.DESERT:
        return 0
    return 1


def apply_sandsworn_pact(state: GameState, pid: int, *, claimed_neutral: bool) -> bool:
    if not claimed_neutral:
        return False
    p = state.player(pid)
    if "sandsworn_pact" not in p.discoveries:
        return False
    if not round_unused(state, pid, "sandsworn_pact"):
        return False
    p.gold += 1
    mark_round_used(state, pid, "sandsworn_pact")
    return True


def apply_stolen_secrets(state: GameState, pid: int, rng: random.Random) -> int:
    from ..whispers import draw_whispers

    p = state.player(pid)
    if "stolen_secrets" not in p.discoveries:
        return 0
    if not round_unused(state, pid, "stolen_secrets"):
        return 0
    drawn = draw_whispers(state, pid, 1, rng)
    mark_round_used(state, pid, "stolen_secrets")
    return drawn


def enumerate_shadow_network(state: GameState, pid: int) -> list[dict]:
    p = state.player(pid)
    if "shadow_network" not in p.discoveries:
        return []
    if not round_unused(state, pid, "shadow_network"):
        return []
    if not p.whisper_hand:
        return []
    out = []
    for card in p.whisper_hand:
        out.append({
            "type": "shadow_network",
            "card": card,
            "reward": "gold",
        })
        out.append({
            "type": "shadow_network",
            "card": card,
            "reward": "influence",
        })
    return out


def apply_shadow_network(state: GameState, pid: int, choice: dict) -> None:
    from ..whispers import discard_whisper

    p = state.player(pid)
    if "shadow_network" not in p.discoveries:
        raise ValueError("shadow_network not owned")
    if not round_unused(state, pid, "shadow_network"):
        raise ValueError("shadow_network already used")
    card = choice["card"]
    if card not in p.whisper_hand:
        raise ValueError("card not in hand")
    discard_whisper(state, pid, card)
    reward = choice.get("reward", "gold")
    if reward == "influence":
        p.influence += 2
    else:
        p.gold += 2
    mark_round_used(state, pid, "shadow_network")


def luminous_bulwark_bonus(state: GameState, pid: int, tile) -> int:
    if "luminous_bulwark" not in state.player(pid).discoveries:
        return 0
    if tile.controller != pid:
        return 0
    return 1 if tile.buildings else 0


def bump_renown(state: GameState, pid: int, amount: int, rng: Optional[random.Random] = None) -> int:
    """Adjust renown and fire Sacred Rite milestones when applicable."""
    p = state.player(pid)
    old = p.renown
    p.renown += amount
    if rng is not None:
        apply_sacred_rite_milestones(state, pid, old, rng)
    return p.renown


def apply_sacred_rite_milestones(
    state: GameState,
    pid: int,
    old_renown: int,
    rng: random.Random,
) -> None:
    from ..whispers import draw_whispers

    p = state.player(pid)
    if "sacred_rite" not in p.discoveries:
        return
    new = p.renown
    if not p.sacred_rite_5 and old_renown < 5 <= new:
        p.sacred_rite_5 = True
        draw_whispers(state, pid, 2, rng)
        p.add_vp(1, "sacred_rite")
    if not p.sacred_rite_10 and old_renown < 10 <= new:
        p.sacred_rite_10 = True
        draw_whispers(state, pid, 2, rng)
        p.add_vp(1, "sacred_rite")


def apply_planar_echo(state: GameState, pid: int, *, used_portal: bool) -> bool:
    if not used_portal:
        return False
    p = state.player(pid)
    if "planar_echo" not in p.discoveries:
        return False
    if not round_unused(state, pid, "planar_echo"):
        return False
    p.ap += 1
    mark_round_used(state, pid, "planar_echo")
    return True


def enumerate_void_anchor(state: GameState, pid: int) -> list[dict]:
    p = state.player(pid)
    if "void_anchor" not in p.discoveries:
        return []
    if not round_unused(state, pid, "void_anchor"):
        return []
    if p.mana < 1:
        return []
    return [
        {"type": "void_anchor", "hex": list(t.coord)}
        for t in state.controlled(pid)
    ]


def apply_void_anchor(state: GameState, pid: int, coord) -> None:
    p = state.player(pid)
    if "void_anchor" not in p.discoveries:
        raise ValueError("void_anchor not owned")
    if not round_unused(state, pid, "void_anchor"):
        raise ValueError("void_anchor already used")
    tile = state.tiles[coord]
    if tile.controller != pid:
        raise ValueError("must control hex")
    if p.mana < 1:
        raise ValueError("insufficient mana")
    p.mana -= 1
    tile.void_anchor_until_round = state.round
    mark_round_used(state, pid, "void_anchor")


def void_anchor_is_portal(state: GameState, coord, pid: int) -> bool:
    tile = state.tiles[coord]
    return (
        tile.void_anchor_until_round == state.round
        and tile.controller == pid
    )


def clear_void_anchors(state: GameState) -> None:
    for tile in state.tiles.values():
        tile.void_anchor_until_round = 0
