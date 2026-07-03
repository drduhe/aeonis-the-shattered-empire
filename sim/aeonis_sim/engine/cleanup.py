from __future__ import annotations

from .hexmap import distance, neighbors
from .arcane import apply_boundary_stones
from .artifacts import score_artifact_vp
from .objectives import PUBLIC_OBJECTIVES, score_cleanup_secrets
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


def _fortress_blocks_claim(state, coord, pid: int) -> bool:
    """Tiles.md: enemy Fortresses block Adjacency Claims on adjacent neutrals."""
    for n in neighbors(coord):
        nt = state.tiles.get(n)
        if nt is None or nt.controller is None or nt.controller == pid:
            continue
        if nt.has(BuildingType.FORTRESS):
            return True
    return False


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
                    and not any(u.owner != pid for u in t.units)
                    and not _fortress_blocks_claim(state, coord, pid)]  # AL-16
        if len(eligible) != 1:
            t.adj_claim = None  # AL-14: contested claims stay neutral (First Playable sim)
            continue
        pid = eligible[0]
        if t.adj_claim and t.adj_claim[0] == pid:
            t.controller = pid
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
        else:
            cands = [t for t in state.controlled(p.pid)
                     if not any(u.owner != p.pid for u in t.units)]
            if cands:
                dest = min(cands, key=lambda t: (distance(t.coord, p.home), t.coord))
        if dest is None:
            continue
        st = UNIT_STATS[UnitType.LORD]
        dest.units.append(Unit(uid=state.new_uid(), owner=p.pid,
                               type=UnitType.LORD, hp=st.hp))
        p.lord_captured = False


def _lord_on_seat(state, pid: int) -> bool:
    """Coronation Rite: control Seat and Lord unit present on Seat hex."""
    for t in state.controlled(pid):
        if not t.imperial_seat:
            continue
        for u in t.units:
            if u.owner == pid and u.type == UnitType.LORD:
                return True
    return False


def _score_coronation(state, pid: int) -> None:
    p = state.player(pid)
    if not _lord_on_seat(state, pid):
        return
    p.add_vp(1, "coronation_rite")
    p.rite_count += 1
    if p.rite_count >= 3 and not p.rite_bonus_scored:
        p.add_vp(2, "coronation_milestone")
        p.rite_bonus_scored = True


def _score_objectives(state, pid: int) -> None:
    """AL-5: score at Cleanup & Checks; VP permanent once awarded."""
    p = state.player(pid)

    if not p.public_scored_this_round:
        for obj_id in state.shared_public_revealed:
            if obj_id in p.shared_scored:
                continue
            if PUBLIC_OBJECTIVES[obj_id](state, pid):
                p.add_vp(2, "objective")
                p.shared_scored.append(obj_id)
                p.public_scored_this_round = True
                break

    score_cleanup_secrets(state, pid)


def run_cleanup(state) -> None:
    for p in state.players:
        apply_boundary_stones(state, p.pid)
    _adjacency_claims(state)
    _release_lords(state)

    for p in state.players:
        _score_coronation(state, p.pid)
        _score_objectives(state, p.pid)
        score_artifact_vp(state, p.pid)

    if any(p.vp >= VP_THRESHOLD for p in state.players):
        state.final_round = True

    for p in state.players:
        p.recruited_cities = []
        p.passed = False
        p.public_scored_this_round = False
        p.arcane_round = {}
    n = len(state.players)
    state.speaker = (state.speaker + 1) % n
    state.agenda_revealed = None
    state.round += 1
