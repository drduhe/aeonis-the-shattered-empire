"""Feature extraction for persona-bot scoring (1-ply where deterministic)."""
from __future__ import annotations

from ..engine.build import apply_build
from ..engine.hexmap import distance, neighbors
from ..engine.move import apply_move
from ..engine.objectives import PUBLIC_OBJECTIVES, SECRET_OBJECTIVES
from ..engine.recruit import apply_recruit
from ..engine.types import (
    BUILDING_SPECS,
    BuildingType,
    GameState,
    Terrain,
    UNIT_STATS,
    UnitType,
    VP_THRESHOLD,
)


def _clone(state: GameState) -> GameState:
    return state.copy()


def _seat_coord(state) -> tuple | None:
    for t in state.tiles.values():
        if t.imperial_seat:
            return t.coord
    return None


def _unscored_hard_objectives(state, pid: int) -> list[str]:
    """Public row objectives that often stall sub-threshold games."""
    p = state.player(pid)
    out = []
    for oid in ("warlord", "portal_mastery"):
        if oid in state.shared_public_revealed and oid not in p.shared_scored:
            out.append(oid)
    return out


def _closing_multiplier(vp: int) -> float:
    if vp >= VP_THRESHOLD - 2:
        return 1.6
    if vp >= VP_THRESHOLD - 4:
        return 1.25
    return 1.0


def evaluate_state(state, pid: int) -> dict[str, float]:
    """Normalized state features for the acting player."""
    p = state.player(pid)
    n_players = len(state.players)
    max_opp_vp = max(
        (q.vp for q in state.players if q.pid != pid),
        default=0,
    )
    controlled = state.controlled(pid)
    map_size = max(len(state.tiles), 1)

    economy = 0.0
    military = 0.0
    for t in controlled:
        for b in t.buildings:
            spec = BUILDING_SPECS[b]
            economy += spec.gold * 0.15 + spec.mana * 0.12 + spec.influence * 0.1
    for _, u in state.units_of(pid):
        st = UNIT_STATS[u.type]
        military += st.attack_die * 0.08 + st.defense_die * 0.05 + u.hp * 0.05

    has_seat = any(t.imperial_seat for t in controlled)
    lord_on_seat = 0.0
    if has_seat:
        seat_tile = next(t for t in controlled if t.imperial_seat)
        if any(u.owner == pid and u.type == UnitType.LORD for u in seat_tile.units):
            lord_on_seat = 1.0

    obj = _best_shared_objective_progress(state, pid)
    if p.secret_objective and not p.secret_scored:
        sec = _objective_progress(state, pid, p.secret_objective, secret=True)
        obj = max(obj, sec)

    n_ctrl = len(controlled)
    territory_sat = max(0.0, min((n_ctrl - 3) / 5.0, 1.0))
    building_count = sum(len(t.buildings) for t in controlled)
    builder_track = min(building_count, 3) / 3.0
    gold_track = min(p.gold, 10) / 10.0
    catch_up = max(0, max_opp_vp - p.vp) / VP_THRESHOLD
    built = sum(len(t.buildings) for t in controlled)
    builder_push = 0.0
    if "builder" in state.shared_public_revealed and "builder" not in p.shared_scored:
        builder_push = max(0.0, (3 - min(built, 3)) / 3.0)

    return {
        "vp": p.vp / VP_THRESHOLD,
        "vp_lead": (p.vp - max_opp_vp) / VP_THRESHOLD,
        "territory": len(controlled) / map_size,
        "territory_sat": territory_sat,
        "builder_track": builder_track,
        "builder_push": builder_push,
        "gold_track": gold_track,
        "catch_up": catch_up,
        "seat": 1.0 if has_seat else 0.0,
        "seat_streak": min(p.rite_count, 3) / 3.0,
        "rite_ready": lord_on_seat,
        "objective": obj,
        "economy": min(economy, 3.0) / 3.0,
        "military": min(military, 3.0) / 3.0,
        "renown": min(p.renown, 5) / 5.0,
        "ap": p.ap / 5.0,
    }


def _best_shared_objective_progress(state, pid: int) -> float:
    best = 0.0
    p = state.player(pid)
    for obj_id in state.shared_public_revealed:
        if obj_id in p.shared_scored:
            continue
        if PUBLIC_OBJECTIVES[obj_id](state, pid):
            return 1.0
        best = max(best, _objective_progress(state, pid, obj_id))
    return best


def _objective_progress(state, pid: int, name: str, *, secret: bool = False) -> float:
    if secret:
        if name == "golden_hoard":
            return min(state.player(pid).gold, 10) / 10.0
        if name == "mana_flood":
            return min(state.player(pid).mana, 10) / 10.0
        if name == "architect_of_control":
            special = sum(
                1 for t in state.controlled(pid)
                if t.imperial_seat or t.terrain in (Terrain.CITY, Terrain.RUINS, Terrain.PORTAL)
            )
            return min(special, 2) / 2.0
        return 0.0
    if name == "frontier_lord":
        return min(len(state.controlled(pid)), 7) / 7.0
    if name == "builder":
        b = sum(len(t.buildings) for t in state.controlled(pid))
        return min(b, 3) / 3.0
    if name == "merchant_lord":
        return min(state.player(pid).gold, 8) / 8.0
    if name == "portal_mastery":
        portal = any(t.terrain == Terrain.PORTAL for t in state.controlled(pid))
        travel = state.player(pid).used_portal_travel
        return (0.5 if portal else 0.0) + (0.5 if travel else 0.0)
    if name == "warlord":
        return min(state.player(pid).battle_wins, 2) / 2.0
    if name == "seat_of_empire":
        return 1.0 if any(t.imperial_seat for t in state.controlled(pid)) else 0.0
    return 0.0


def _combat_features(state, pid: int, choice: dict) -> dict[str, float]:
    t = choice["type"]
    if t == "attack":
        target = tuple(choice["target"])
        return {"combat": _attack_value(state, pid, target)}
    if t == "press":
        return {"combat": 0.8}
    if t == "hold":
        return {"combat": -0.3}
    if t == "retreat":
        return {"combat": -0.5}
    return {"combat": 0.0}


def _attack_value(state, pid: int, target: tuple) -> float:
    my_hexes = {c for c, t in state.tiles.items() if any(u.owner == pid for u in t.units)}
    if not any(n in my_hexes for n in neighbors(target)):
        return 0.0
    att = sum(
        UNIT_STATS[u.type].attack_die
        for c in my_hexes
        if target in neighbors(c)
        for u in state.tiles[c].units
        if u.owner == pid
    )
    tile = state.tiles[target]
    deff = sum(UNIT_STATS[u.type].defense_die for u in tile.units if u.owner != pid)
    if deff == 0:
        deff = 4
    odds = att / max(deff, 1)
    lord_bonus = 0.5 if any(u.type == UnitType.LORD and u.owner != pid for u in tile.units) else 0.0
    siege_penalty = -0.4 if tile.terrain == Terrain.CITY or tile.has(BuildingType.FORTRESS) else 0.0
    return min(2.0, odds * 0.4 + lord_bonus + siege_penalty)


def _builder_need(state, pid: int) -> float:
    p = state.player(pid)
    if "builder" in state.shared_public_revealed and "builder" not in p.shared_scored:
        built = sum(len(t.buildings) for t in state.controlled(pid))
        if built < 3:
            return (3 - built) / 3.0
    return 0.0


def _move_features(state, pid: int, choice: dict) -> dict[str, float]:
    dest = tuple(choice["dest"])
    seat = _seat_coord(state)
    expansion = 0.0
    tile = state.tiles.get(dest)
    if tile and tile.controller not in (pid, None):
        expansion = 0.45
    elif tile and tile.controller is None:
        expansion = 0.3
    seat_pull = 0.0
    if seat is not None:
        # Compare min distance from moved units' origins vs dest to seat.
        origins = {tuple(choice["from"])}
        before = min(distance(o, seat) for o in origins)
        after = distance(dest, seat)
        seat_pull = max(0.0, (before - after) * 0.25)
    builder_need = _builder_need(state, pid)
    return {
        "expansion": expansion,
        "seat_pull": seat_pull,
        "rite_ready": 1.0 if (seat is not None and dest == seat) else 0.0,
        "builder_need": builder_need,
    }


def _build_features(state, pid: int, choice: dict) -> dict[str, float]:
    b = BuildingType(choice["building"])
    spec = BUILDING_SPECS[b]
    econ = spec.gold * 0.2 + spec.mana * 0.15 + spec.influence * 0.1
    mil = 0.3 if b in (BuildingType.FORTRESS, BuildingType.TOWER, BuildingType.CASTLE) else 0.0
    before = sum(len(t.buildings) for t in state.controlled(pid))
    after = before + 1
    builder_delta = max(0.0, min(after, 3) / 3.0 - min(before, 3) / 3.0)
    production_bonus = 0.4 if b in (
        BuildingType.MINE, BuildingType.GROVE, BuildingType.FARM, BuildingType.EMBASSY,
    ) else 0.0
    return {
        "economy_delta": min(econ, 1.5),
        "military_delta": mil,
        "builder_delta": builder_delta,
        "production_bonus": production_bonus,
    }


def _recruit_features(state, pid: int, choice: dict) -> dict[str, float]:
    power = sum(UNIT_STATS[UnitType(n)].attack_die for n in choice["units"])
    return {
        "military_delta": min(power * 0.1, 1.0),
        "builder_need": _builder_need(state, pid),
    }


def simulate_action(state, pid: int, choice: dict, dp_kind: str):
    """Apply a deterministic action to a clone; None if not simulatable."""
    if dp_kind != "action":
        return None
    t = choice["type"]
    if t == "attack":
        return None
    s = _clone(state)
    p = s.player(pid)
    if t == "pass":
        p.passed = True
        p.banked = min(2, p.ap)
    elif t == "move":
        apply_move(s, pid, choice)
    elif t == "recruit":
        apply_recruit(s, pid, choice)
    elif t == "build":
        apply_build(s, pid, choice)
    else:
        return None
    return s


def score_action(state, pid: int, choice: dict, dp) -> dict[str, float]:
    """Merged feature vector for weighted persona scoring."""
    feats = dict(evaluate_state(state, pid))
    t = choice["type"]
    if t == "pass":
        feats["pass_penalty"] = -0.15 if state.player(pid).ap > 0 else 0.0
    elif t == "move":
        feats.update(_move_features(state, pid, choice))
    elif t == "build":
        feats.update(_build_features(state, pid, choice))
    elif t == "recruit":
        feats.update(_recruit_features(state, pid, choice))
    elif t == "strategy_primary":
        card = choice.get("card", "")
        if card == "resource_surge":
            feats["economy_delta"] = 1.2
            feats["economy"] = feats.get("economy", 0) + 0.2
        elif card == "economic_boom":
            feats["economy_delta"] = 1.5
        elif card == "military_maneuvers":
            feats["military_delta"] = 1.0
            feats["combat"] = feats.get("combat", 0) + 0.5
    elif t == "strategy_secondary" and choice.get("use"):
        feats["economy_delta"] = 0.5
    feats.update(_combat_features(state, pid, choice))

    p = state.player(pid)
    close = _closing_multiplier(p.vp)
    hard = _unscored_hard_objectives(state, pid)
    if hard and p.vp >= VP_THRESHOLD - 4:
        feats["objective"] = max(feats.get("objective", 0), 0.45) * close
        if "warlord" in hard and t == "attack":
            feats["combat"] = feats.get("combat", 0) * close + 0.35
        if "portal_mastery" in hard and t == "move" and choice.get("portal"):
            feats["expansion"] = feats.get("expansion", 0) + 0.9 * close
    if p.vp >= VP_THRESHOLD - 2:
        if t == "move":
            feats["seat_pull"] = feats.get("seat_pull", 0) * close
            feats["rite_ready"] = feats.get("rite_ready", 0) * close

    nxt = simulate_action(state, pid, choice, dp.kind)
    if nxt is not None:
        for k, v in evaluate_state(nxt, pid).items():
            feats[f"next_{k}"] = v
    return feats
