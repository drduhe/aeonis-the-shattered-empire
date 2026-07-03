from __future__ import annotations

from .hexmap import distance, neighbors
from .objectives import OBJECTIVES
from .types import BuildingType, Terrain, Unit, UNIT_STATS, UnitType, VP_THRESHOLD


def _influence_range(state, pid):
    """Hexes within Adjacency-Claim influence: adjacent to a controlled City,
    or within 2 of a controlled Tower (Tiles.md, Borders section)."""
    out = set()
    for t in state.controlled(pid):
        if t.terrain == Terrain.CITY:
            out.update(n for n in neighbors(t.coord) if n in state.tiles)
        if t.has(BuildingType.TOWER):
            out.update(c for c in state.tiles if 0 < distance(c, t.coord) <= 2)
    return out


def _adjacency_claims(state) -> None:
    ranges = {p.pid: _influence_range(state, p.pid) for p in state.players}
    for coord, t in state.tiles.items():
        if t.controller is not None:
            t.adj_claim = None
            continue
        if t.terrain == Terrain.LAKE and not t.has(BuildingType.BRIDGE):
            continue
        eligible = [pid for pid, rng_ in ranges.items()
                    if coord in rng_
                    and not any(u.owner != pid for u in t.units)]
        if len(eligible) != 1:
            t.adj_claim = None  # AL-14: contested claims stay neutral in M1
            continue
        pid = eligible[0]
        if t.adj_claim and t.adj_claim[0] == pid:
            t.controller = pid  # second consecutive check
            t.adj_claim = None
        else:
            t.adj_claim = (pid, 1)


def _release_lords(state) -> None:
    for p in state.players:
        if not p.lord_captured:
            continue
        home = state.tiles[p.home]
        dest = None
        if home.controller == p.pid and not any(u.owner != p.pid for u in home.units):
            dest = home
        else:  # AL-9: nearest controlled hex without enemy units
            cands = [t for t in state.controlled(p.pid)
                     if not any(u.owner != p.pid for u in t.units)]
            if cands:
                dest = min(cands, key=lambda t: (distance(t.coord, p.home), t.coord))
        if dest is None:
            continue  # stays captured; retry next round
        st = UNIT_STATS[UnitType.LORD]
        dest.units.append(Unit(uid=state.new_uid(), owner=p.pid,
                               type=UnitType.LORD, hp=st.hp))
        p.lord_captured = False


def run_cleanup(state) -> None:
    _adjacency_claims(state)
    _release_lords(state)

    for p in state.players:
        # Imperial Seat: +1 VP per round held; +2 bonus at 3 consecutive
        if any(t.imperial_seat for t in state.controlled(p.pid)):
            p.add_vp(1, "imperial_seat")
            p.seat_streak += 1
            if p.seat_streak >= 3 and not p.seat_bonus_scored:
                p.add_vp(2, "seat_streak_bonus")
                p.seat_bonus_scored = True
        else:
            p.seat_streak = 0
        # Objectives (AL-5: auto-score at Cleanup, once per card)
        if p.objective and not p.objective_scored:
            if OBJECTIVES[p.objective](state, p.pid):
                p.add_vp(2, "objective")
                p.objective_scored = True

    if any(p.vp >= VP_THRESHOLD for p in state.players):
        state.final_round = True

    for p in state.players:
        p.recruited_cities = []
        p.passed = False
    state.round += 1
