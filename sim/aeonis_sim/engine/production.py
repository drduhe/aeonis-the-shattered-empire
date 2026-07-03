from __future__ import annotations

from .types import BUILDING_SPECS, BuildingType, Terrain
from .artifacts import (
    production_adjacent_gold,
    production_ley_line_mana,
    production_verdant_bonus,
    production_wellspring,
)
from .arcane import production_golden_alchemy

# Tiles.md: base production, upgraded by the matching production building.
_PLAIN = {Terrain.MOUNTAIN: ("gold", 1), Terrain.FOREST: ("mana", 1),
          Terrain.DESERT: ("influence", 1)}
_UPGRADED = {BuildingType.MINE: ("gold", 3), BuildingType.GROVE: ("mana", 3),
             BuildingType.EMBASSY: ("influence", 3)}


def tile_printed_production(tile) -> dict[str, int]:
    """One-time printed production (Plan 1 Pillage). Cities: 2 Gold."""
    if tile.terrain == Terrain.CITY:
        return {"gold": 2}
    out: dict[str, int] = {}
    for b in tile.buildings:
        if b in _UPGRADED:
            res, amt = _UPGRADED[b]
            out[res] = out.get(res, 0) + amt
    if not out:
        plain = _PLAIN.get(tile.terrain)
        if plain:
            res, amt = plain
            out[res] = amt
    return out


def apply_tile_production(player, tile) -> None:
    for res, amt in tile_printed_production(tile).items():
        setattr(player, res, getattr(player, res) + amt)


def _pay_upkeep(state, p) -> None:
    """Building upkeep with AL-8 suspension (Castle gold; Forge/Academy mana)."""
    for t in state.controlled(p.pid):
        t.suspended = []
        for b in t.buildings:
            spec = BUILDING_SPECS[b]
            if b == BuildingType.CASTLE:
                if p.gold >= spec.upkeep_gold:
                    p.gold -= spec.upkeep_gold
                    t.castle_suspended = False
                else:
                    t.castle_suspended = True
            elif spec.upkeep_mana:
                if p.mana >= spec.upkeep_mana:
                    p.mana -= spec.upkeep_mana
                else:
                    t.suspended.append(b.value)


def _bank_conversion(state, p) -> str | None:
    """Bank (Buildings.md): once per Production & Upkeep, convert at 2:3.

    Sim auto-heuristic (AL-26): runs at end of Production & Upkeep; converts
    surplus mana to gold, or gold to mana when mana-starved. One Bank use per
    player per round regardless of Bank count.
    """
    if not any(t.active(BuildingType.BANK) for t in state.controlled(p.pid)):
        return None
    if p.mana >= 4:
        p.mana -= 2
        p.gold += 3
        return "mana_to_gold"
    if p.gold >= 6 and p.mana == 0:
        p.gold -= 2
        p.mana += 3
        return "gold_to_mana"
    return None


def run_production(state) -> dict:
    """Round_Structure.md §6: production, growth, upkeep. Returns stats."""
    stats: dict = {"bank_conversions": {}}
    for p in state.players:
        # 1. Resource production (AL-13: Cities print growth only, not trade resources)
        for t in state.controlled(p.pid):
            if t.cursed:
                continue
            double = p.whisper_flags.pop("double_tile", None)
            mult = 2 if double and tuple(t.coord) == tuple(double) else 1
            produced = None
            for b in t.buildings:
                if b in _UPGRADED:
                    produced = _UPGRADED[b]
            if produced is None:
                produced = _PLAIN.get(t.terrain)
            if produced:
                res, amt = produced
                extra = production_ley_line_mana(t)
                if res == "gold":
                    amt += production_adjacent_gold(state, p.pid, t)
                setattr(p, res, getattr(p, res) + (amt + (extra if res == "mana" else 0)) * mult)
                if extra and res != "mana":
                    p.mana += extra * mult
        # 2. Population growth
        growth = 1  # Population.md base growth
        for t in state.controlled(p.pid):
            if t.terrain == Terrain.PLAINS:
                growth += 2 if t.has(BuildingType.FARM) else 1
            elif t.terrain == Terrain.CITY:
                growth += 2
            growth += production_verdant_bonus(t)
        room = state.pop_cap(p.pid) - state.pop_used(p.pid) - p.pop_pool
        p.pop_pool += max(0, min(growth, room))
        # 3. Upkeep (suspend when unpaid)
        _pay_upkeep(state, p)
        # 4. Bank conversion (after upkeep so it never starves upkeep mana)
        conv = _bank_conversion(state, p)
        if conv:
            stats["bank_conversions"][p.pid] = conv
        production_wellspring(state, p.pid)
        production_golden_alchemy(state, p.pid)
        # 5. Remnants from controlled Ruins
        for t in state.controlled(p.pid):
            if t.terrain == Terrain.RUINS:
                p.remnants += 1
    return stats
