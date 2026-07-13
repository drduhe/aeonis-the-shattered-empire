from __future__ import annotations

from itertools import combinations_with_replacement

from .types import BuildingType, Terrain, Unit, UNIT_STATS, UnitType
from .artifacts import recruit_gold_discount
from .lords import is_lord, tile_is_portal

RECRUITABLE = [UnitType.INFANTRY, UnitType.CAVALRY, UnitType.ARCHER]


def _unit_gold(ut: UnitType, *, forge: bool, eternal: bool, discount: int = 0) -> int:
    """Forge (Buildings.md): units recruited at this City cost -1 Gold (min 1)."""
    gold = UNIT_STATS[ut].gold
    if forge:
        gold = max(1, gold - 1)
    if eternal:
        gold = max(1, gold - 1)
    if discount:
        gold = max(0, gold - discount)
    return gold


def _affordable(p, unit_types, *, forge: bool, eternal: bool, discount: int = 0) -> bool:
    gold = sum(_unit_gold(u, forge=forge, eternal=eternal, discount=discount) for u in unit_types)
    mana = sum(UNIT_STATS[u].mana for u in unit_types)
    pop = sum(UNIT_STATS[u].pop for u in unit_types)
    return p.gold >= gold and p.mana >= mana and p.pop_pool >= pop


def _recruit_sites(state, pid):
    sites = []
    for tile in state.controlled(pid):
        if tile.terrain == Terrain.CITY:
            sites.append(tile)
        elif is_lord(state, pid, "thalrik") and tile_is_portal(state, tile.coord, pid):
            sites.append(tile)
    return sites


def enumerate_recruits(state, pid, *, ignore_city_limit: bool = False) -> list:
    p = state.player(pid)
    if p.ap < 1 and not ignore_city_limit:
        return []
    out = []
    for tile in _recruit_sites(state, pid):
        if not ignore_city_limit and tile.coord in p.recruited_cities:
            continue  # Actions.md: each City at most once per round
        # Forge (active): +1 unit beyond the 2-unit limit at this City.
        forge = tile.active(BuildingType.FORGE)
        eternal = recruit_gold_discount(state, pid, tile.coord) > 0
        sizes = (1, 2, 3) if forge else (1, 2)
        combos = [list(c) for n in sizes
                  for c in combinations_with_replacement(RECRUITABLE, n)]
        for combo in combos:
            if _affordable(p, combo, forge=forge, eternal=eternal):
                choice = {
                    "type": "recruit",
                    "city": list(tile.coord),
                    "units": sorted(u.value for u in combo),
                }
                if tile_is_portal(state, tile.coord, pid):
                    choice["portal"] = True
                out.append(choice)
    return out


def apply_recruit(state, pid, choice, *, free: bool = False, ignore_city_limit: bool = False) -> None:
    p = state.player(pid)
    tile = state.tiles[tuple(choice["city"])]
    forge = tile.active(BuildingType.FORGE)
    eternal = recruit_gold_discount(state, pid, tile.coord) > 0
    units = [UnitType(name) for name in choice["units"]]
    if not free:
        p.ap -= 1
    if not ignore_city_limit:
        p.recruited_cities.append(tile.coord)
    for ut in units:
        st = UNIT_STATS[ut]
        if not free:
            p.gold -= _unit_gold(ut, forge=forge, eternal=eternal)
            p.mana -= st.mana
        p.pop_pool -= st.pop
        tile.units.append(Unit(uid=state.new_uid(), owner=pid, type=ut, hp=st.hp))
