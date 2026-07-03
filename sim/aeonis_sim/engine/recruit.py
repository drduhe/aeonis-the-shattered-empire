from __future__ import annotations

from itertools import combinations_with_replacement

from .types import BuildingType, Terrain, Unit, UNIT_STATS, UnitType

RECRUITABLE = [UnitType.INFANTRY, UnitType.CAVALRY, UnitType.ARCHER]


def _unit_gold(ut: UnitType, *, forge: bool) -> int:
    """Forge (Buildings.md): units recruited at this City cost -1 Gold (min 1)."""
    gold = UNIT_STATS[ut].gold
    return max(1, gold - 1) if forge else gold


def _affordable(p, unit_types, *, forge: bool) -> bool:
    gold = sum(_unit_gold(u, forge=forge) for u in unit_types)
    mana = sum(UNIT_STATS[u].mana for u in unit_types)
    pop = sum(UNIT_STATS[u].pop for u in unit_types)
    return p.gold >= gold and p.mana >= mana and p.pop_pool >= pop


def enumerate_recruits(state, pid) -> list:
    p = state.player(pid)
    if p.ap < 1:
        return []
    out = []
    for tile in state.controlled(pid):
        if tile.terrain != Terrain.CITY:
            continue
        if tile.coord in p.recruited_cities:
            continue  # Actions.md: each City at most once per round
        # Forge (active): +1 unit beyond the 2-unit limit at this City.
        forge = tile.active(BuildingType.FORGE)
        sizes = (1, 2, 3) if forge else (1, 2)
        combos = [list(c) for n in sizes
                  for c in combinations_with_replacement(RECRUITABLE, n)]
        for combo in combos:
            if _affordable(p, combo, forge=forge):
                out.append({
                    "type": "recruit",
                    "city": list(tile.coord),
                    "units": sorted(u.value for u in combo),
                })
    return out


def apply_recruit(state, pid, choice) -> None:
    p = state.player(pid)
    tile = state.tiles[tuple(choice["city"])]
    forge = tile.active(BuildingType.FORGE)
    p.ap -= 1
    p.recruited_cities.append(tile.coord)
    for name in choice["units"]:
        ut = UnitType(name)
        st = UNIT_STATS[ut]
        p.gold -= _unit_gold(ut, forge=forge)
        p.mana -= st.mana
        p.pop_pool -= st.pop
        tile.units.append(Unit(uid=state.new_uid(), owner=pid, type=ut, hp=st.hp))
