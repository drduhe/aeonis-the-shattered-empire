"""Whisper Cards (Whispers.md First Playable 26-card deck)."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from .hexmap import distance, neighbors
from .types import BuildingType, Terrain, Unit, UNIT_STATS, UnitType

if TYPE_CHECKING:
    from .types import GameState

WHISPER_HAND_LIMIT = 7

WHISPER_CARD_IDS: tuple[str, ...] = (
    # Combat (8)
    "shield_wall",
    "flanking_charge",
    "deadly_volley",
    "tactical_withdrawal",
    "rallying_cry",
    "fortify_position",
    "overwhelming_numbers",
    "iron_resolve",
    # Political (5)
    "sabotage",
    "backroom_deal",
    "veto",
    "political_leverage",
    "leaked_intelligence",
    # Economic (6)
    "hidden_cache",
    "war_profiteer",
    "emergency_conscription",
    "prospectors_find",
    "contraband",
    "relic_hunter",
    # Movement / Arcane (4)
    "forced_march",
    "blink",
    "ley_line_surge",
    "waystone_activation",
    # Subterfuge (3)
    "saboteur",
    "mercenary_company",
    "relic_thief",
)


@dataclass(frozen=True)
class WhisperSpec:
    id: str
    timing: str  # action | combat | council | when
    combat_step: Optional[str] = None  # pre_strike | strike | counterstrike | retreat | reinforce
    when_trigger: Optional[str] = None


WHISPER_SPECS: dict[str, WhisperSpec] = {
    "shield_wall": WhisperSpec("shield_wall", "combat", "counterstrike"),
    "flanking_charge": WhisperSpec("flanking_charge", "combat", "strike"),
    "deadly_volley": WhisperSpec("deadly_volley", "combat", "pre_strike"),
    "tactical_withdrawal": WhisperSpec("tactical_withdrawal", "combat", "retreat"),
    "rallying_cry": WhisperSpec("rallying_cry", "when", when_trigger="battle_casualties"),
    "fortify_position": WhisperSpec("fortify_position", "when", when_trigger="defender_win"),
    "overwhelming_numbers": WhisperSpec("overwhelming_numbers", "combat", "reinforce"),
    "iron_resolve": WhisperSpec("iron_resolve", "combat", "pre_roll"),
    "sabotage": WhisperSpec("sabotage", "when", when_trigger="whisper_played"),
    "backroom_deal": WhisperSpec("backroom_deal", "council", when_trigger="pre_tally"),
    "veto": WhisperSpec("veto", "council", when_trigger="post_pass"),
    "political_leverage": WhisperSpec("political_leverage", "council", when_trigger="proposal"),
    "leaked_intelligence": WhisperSpec("leaked_intelligence", "council", when_trigger="agenda_reveal"),
    "hidden_cache": WhisperSpec("hidden_cache", "action"),
    "war_profiteer": WhisperSpec("war_profiteer", "when", when_trigger="enemy_attack"),
    "emergency_conscription": WhisperSpec("emergency_conscription", "when", when_trigger="recruit_done"),
    "prospectors_find": WhisperSpec("prospectors_find", "action"),
    "contraband": WhisperSpec("contraband", "action"),
    "relic_hunter": WhisperSpec("relic_hunter", "action"),
    "forced_march": WhisperSpec("forced_march", "when", when_trigger="before_move"),
    "blink": WhisperSpec("blink", "when", when_trigger="before_move"),
    "ley_line_surge": WhisperSpec("ley_line_surge", "action"),
    "waystone_activation": WhisperSpec("waystone_activation", "when", when_trigger="portal_travel"),
    "saboteur": WhisperSpec("saboteur", "action"),
    "mercenary_company": WhisperSpec("mercenary_company", "action"),
    "relic_thief": WhisperSpec("relic_thief", "when", when_trigger="artifact_claim"),
}


@dataclass
class BattleWhisperMods:
    att_cap_bonus: int = 0
    def_cap_bonus: int = 0
    shield_uid: Optional[int] = None
    flanking_uid: Optional[int] = None
    iron_resolve_uid: Optional[int] = None
    deadly_volley: bool = False
    tactical_withdrawal: bool = False


def init_whisper_deck(rng: random.Random) -> list[str]:
    deck = list(WHISPER_CARD_IDS)
    rng.shuffle(deck)
    return deck


def _reshuffle_whispers(state: GameState, rng: random.Random) -> None:
    if state.whisper_discard:
        state.whisper_deck = list(state.whisper_discard)
        state.whisper_discard = []
        rng.shuffle(state.whisper_deck)


def draw_whispers(state: GameState, pid: int, n: int, rng: random.Random) -> int:
    p = state.player(pid)
    drawn = 0
    for _ in range(n):
        if not state.whisper_deck:
            _reshuffle_whispers(state, rng)
        if not state.whisper_deck:
            break
        p.whisper_hand.append(state.whisper_deck.pop())
        drawn += 1
    return drawn


def discard_whisper(state: GameState, pid: int, card_id: str) -> None:
    p = state.player(pid)
    if card_id in p.whisper_hand:
        p.whisper_hand.remove(card_id)
        state.whisper_discard.append(card_id)


def hand_over_limit(state: GameState, pid: int) -> bool:
    from .lords import whisper_hand_limit
    return len(state.player(pid).whisper_hand) > whisper_hand_limit(
        state, pid, WHISPER_HAND_LIMIT,
    )


def enumerate_whisper_discard(state: GameState, pid: int) -> list[dict]:
    p = state.player(pid)
    return [
        {"type": "whisper_discard", "card": c}
        for c in p.whisper_hand
    ]


def cards_for_timing(hand: list[str], timing: str, **ctx) -> list[str]:
    out = []
    hall_any = bool(ctx.get("hall_any_timing"))
    for cid in hand:
        spec = WHISPER_SPECS.get(cid)
        if spec is None:
            continue
        if not hall_any and spec.timing != timing:
            continue
        if not hall_any:
            if timing == "combat" and spec.combat_step != ctx.get("step"):
                continue
            if timing == "when" and spec.when_trigger != ctx.get("trigger"):
                continue
            if timing == "council" and spec.when_trigger != ctx.get("council_window"):
                continue
        if not _requirements_met(cid, ctx):
            continue
        out.append(cid)
    return out


def _requirements_met(card_id: str, ctx: dict) -> bool:
    state = ctx.get("state")
    pid = ctx.get("pid")
    battle = ctx.get("battle")
    if card_id == "shield_wall":
        return battle is not None and pid == battle.defender
    if card_id == "flanking_charge":
        line = ctx.get("line", [])
        return any(u.type == UnitType.CAVALRY for u in line)
    if card_id == "deadly_volley":
        line = ctx.get("line", [])
        return any(u.type == UnitType.ARCHER for u in line)
    if card_id == "tactical_withdrawal":
        return bool(ctx.get("retreating"))
    if card_id == "relic_thief":
        return bool(ctx.get("adjacent_to_site"))
    return True


def enumerate_action_whispers(state: GameState, pid: int) -> list[dict]:
    p = state.player(pid)
    out = []
    for cid in cards_for_timing(p.whisper_hand, "action"):
        if cid == "hidden_cache":
            out.extend([
                {"type": "whisper_play", "card": cid, "choice": "gold"},
                {"type": "whisper_play", "card": cid, "choice": "mana"},
            ])
        elif cid == "prospectors_find":
            for t in state.controlled(pid):
                out.append({
                    "type": "whisper_play",
                    "card": cid,
                    "hex": list(t.coord),
                })
        elif cid == "saboteur":
            for t in state.tiles.values():
                if t.controller == pid or not t.buildings:
                    continue
                if any(
                    n in state.tiles and state.tiles[n].controller == pid
                    for n in neighbors(t.coord)
                ):
                    out.append({
                        "type": "whisper_play",
                        "card": cid,
                        "hex": list(t.coord),
                        "building": t.buildings[0].value,
                    })
        elif cid == "mercenary_company":
            for coord, tile in state.tiles.items():
                if tile.controller is not None:
                    continue
                if any(
                    state.tiles[n].controller == pid
                    for n in neighbors(coord)
                    if n in state.tiles
                ):
                    out.append({
                        "type": "whisper_play",
                        "card": cid,
                        "hex": list(coord),
                    })
        else:
            out.append({"type": "whisper_play", "card": cid})
    # Hall of Whispers: once/round play any timing as an Action play.
    from .lords.legendaries import hall_any_timing_available
    if hall_any_timing_available(state, pid):
        action_ids = {c["card"] for c in out}
        for cid in cards_for_timing(
            p.whisper_hand, "action", hall_any_timing=True, state=state, pid=pid,
        ):
            if cid in action_ids:
                continue
            out.append({"type": "whisper_play", "card": cid, "hall_any_timing": True})
    return out


def enumerate_combat_whispers(
    state: GameState,
    pid: int,
    battle,
    step: str,
    *,
    line: list | None = None,
    retreating: bool = False,
) -> list[dict]:
    p = state.player(pid)
    ctx = {
        "state": state,
        "pid": pid,
        "battle": battle,
        "step": step,
        "line": line or [],
        "retreating": retreating,
    }
    cards = cards_for_timing(p.whisper_hand, "combat", **ctx)
    choices = [{"type": "whisper_skip"}]
    for cid in cards:
        base = {"type": "whisper_play", "card": cid, "step": step}
        if cid in ("shield_wall", "flanking_charge", "iron_resolve"):
            for u in ctx["line"]:
                choices.append({**base, "uid": u.uid})
        else:
            choices.append(base)
    return choices


def enumerate_council_whispers(
    state: GameState,
    pid: int,
    window: str,
    *,
    motion_id: str = "",
) -> list[dict]:
    p = state.player(pid)
    ctx = {"state": state, "pid": pid, "council_window": window, "motion_id": motion_id}
    cards = cards_for_timing(p.whisper_hand, "council", **ctx)
    choices = [{"type": "whisper_skip"}]
    for cid in cards:
        if cid == "backroom_deal":
            choices.extend([
                {"type": "whisper_play", "card": cid, "side": "for"},
                {"type": "whisper_play", "card": cid, "side": "against"},
            ])
        elif cid == "veto" and motion_id in ("hero_of_the_realm", "magister_of_mana"):
            continue  # titles immune
        else:
            choices.append({"type": "whisper_play", "card": cid})
    return choices


def enumerate_when_whispers(state: GameState, pid: int, trigger: str, **ctx) -> list[dict]:
    p = state.player(pid)
    full_ctx = {"state": state, "pid": pid, "trigger": trigger, **ctx}
    cards = cards_for_timing(p.whisper_hand, "when", **full_ctx)
    choices = [{"type": "whisper_skip"}]
    for cid in cards:
        choices.append({"type": "whisper_play", "card": cid})
    return choices


def apply_action_whisper(state: GameState, pid: int, choice: dict) -> None:
    cid = choice["card"]
    p = state.player(pid)
    discard_whisper(state, pid, cid)
    p.whispers_played += 1
    if choice.get("hall_any_timing"):
        from .lords.legendaries import mark_hall_any_timing_used
        mark_hall_any_timing_used(state, pid)
    if cid == "hidden_cache":
        if choice.get("choice") == "mana":
            p.mana += 3
        else:
            p.gold += 3
    elif cid == "contraband":
        p.gold += 1
        p.mana += 1
        p.influence += 1
    elif cid == "ley_line_surge":
        p.mana += 2
        p.whisper_flags["free_research_ap"] = True
    elif cid == "prospectors_find":
        coord = tuple(choice["hex"])
        p.whisper_flags["double_tile"] = coord
    elif cid == "relic_hunter":
        p.remnants += 1
    elif cid == "saboteur":
        tile = state.tiles[tuple(choice["hex"])]
        btype = BuildingType(choice["building"])
        if btype not in tile.suspended:
            tile.suspended.append(btype)
    elif cid == "mercenary_company":
        coord = tuple(choice["hex"])
        tile = state.tiles[coord]
        tile.controller = pid
        tile.explored = True
        for _ in range(2):
            if p.pop_pool <= 0:
                break
            st = UNIT_STATS[UnitType.INFANTRY]
            tile.units.append(
                Unit(uid=state.new_uid(), owner=pid, type=UnitType.INFANTRY, hp=st.hp)
            )
            p.pop_pool -= st.pop


def apply_combat_whisper(
    state: GameState,
    pid: int,
    choice: dict,
    mods: BattleWhisperMods,
    battle,
) -> None:
    cid = choice["card"]
    discard_whisper(state, pid, cid)
    if cid == "shield_wall":
        mods.shield_uid = int(choice["uid"])
    elif cid == "flanking_charge":
        mods.flanking_uid = int(choice["uid"])
    elif cid == "iron_resolve":
        mods.iron_resolve_uid = int(choice["uid"])
    elif cid == "deadly_volley":
        mods.deadly_volley = True
    elif cid == "overwhelming_numbers":
        if pid == battle.attacker:
            mods.att_cap_bonus += 1
        else:
            mods.def_cap_bonus += 1
    elif cid == "tactical_withdrawal":
        mods.tactical_withdrawal = True


def apply_when_whisper(state: GameState, pid: int, choice: dict, rng=None) -> None:
    cid = choice["card"]
    p = state.player(pid)
    discard_whisper(state, pid, cid)
    p.whispers_played += 1
    if cid == "war_profiteer":
        p.gold += 2
    elif cid == "rallying_cry":
        p.ap += 1
    elif cid == "emergency_conscription":
        coord = choice.get("city")
        if coord and p.pop_pool > 0:
            tile = state.tiles[tuple(coord)]
            st = UNIT_STATS[UnitType.INFANTRY]
            tile.units.append(
                Unit(uid=state.new_uid(), owner=pid, type=UnitType.INFANTRY, hp=st.hp)
            )
            p.pop_pool -= st.pop
    elif cid == "fortify_position":
        coord = choice.get("hex")
        if coord and p.pop_pool > 0:
            tile = state.tiles[tuple(coord)]
            st = UNIT_STATS[UnitType.INFANTRY]
            tile.units.append(
                Unit(uid=state.new_uid(), owner=pid, type=UnitType.INFANTRY, hp=st.hp)
            )
            p.pop_pool -= st.pop
    elif cid == "forced_march":
        p.whisper_flags["forced_march"] = True
    elif cid == "blink":
        p.whisper_flags["blink_uid"] = int(choice["uid"])
    elif cid == "waystone_activation":
        p.whisper_flags["hostile_portal_ok"] = True
    elif cid == "relic_hunter":
        p.remnants += 1
    if rng is not None:
        from .lords.discoveries import apply_stolen_secrets
        apply_stolen_secrets(state, pid, rng)


def apply_council_whisper(state: GameState, pid: int, choice: dict) -> dict:
    """Returns vote modifiers: {for: n, against: n} or {veto: True}."""
    cid = choice["card"]
    discard_whisper(state, pid, cid)
    state.player(pid).whispers_played += 1
    if cid == "backroom_deal":
        side = choice.get("side", "for")
        return {side: 2}
    if cid == "veto":
        return {"veto": True}
    if cid == "political_leverage":
        state.player(pid).influence += 2
        state.player(pid).whisper_flags["extra_proposal"] = True
        return {}
    if cid == "leaked_intelligence":
        if state.agenda_deck:
            state.agenda_revealed = state.agenda_deck.pop()
        return {}
    return {}


def combat_defense_mod(mods: BattleWhisperMods, uid: int) -> int:
    return 2 if mods.shield_uid == uid else 0


def combat_attack_die(mods: BattleWhisperMods, u) -> int:
    if mods.flanking_uid == u.uid and u.type == UnitType.CAVALRY:
        return 12
    return UNIT_STATS[u.type].attack_die


def combat_pre_strike_bonus(mods: BattleWhisperMods) -> int:
    return 1 if mods.deadly_volley else 0


def combat_iron_resolve(mods: BattleWhisperMods, u) -> bool:
    return mods.iron_resolve_uid == u.uid


def auto_apply_combat_whispers(
    state: GameState,
    battle,
    step: str,
    mods: BattleWhisperMods,
    *,
    retreating: bool = False,
) -> None:
    """Sim auto-heuristic (AL-40): play one eligible combat whisper per player per step."""
    if not hasattr(battle, "_whisper_steps_used"):
        battle._whisper_steps_used = set()
    used = battle._whisper_steps_used
    for pid in (battle.attacker, battle.defender):
        key = (pid, step)
        if key in used:
            continue
        line = battle.att_line if pid == battle.attacker else battle.def_line
        ctx = {
            "state": state,
            "pid": pid,
            "battle": battle,
            "step": step,
            "line": line,
            "retreating": retreating and pid == battle.defender,
        }
        cards = cards_for_timing(state.player(pid).whisper_hand, "combat", **ctx)
        if not cards:
            continue
        cid = cards[0]
        choice: dict = {"type": "whisper_play", "card": cid, "step": step}
        if cid in ("shield_wall", "flanking_charge", "iron_resolve"):
            pick = None
            if cid == "flanking_charge":
                pick = next((u for u in line if u.type == UnitType.CAVALRY), None)
            else:
                pick = line[0] if line else None
            if pick is None:
                continue
            choice["uid"] = pick.uid
        apply_combat_whisper(state, pid, choice, mods, battle)
        used.add(key)


def offer_sabotage_players(state: GameState, player: int, played_card: str) -> list[int]:
    if played_card == "sabotage":
        return []
    out = []
    for pid, p in enumerate(state.players):
        if pid == player:
            continue
        if "sabotage" in p.whisper_hand:
            out.append(pid)
    return out


def apply_relic_thief_cancel(state: GameState, thief: int, site_coord: tuple) -> str | None:
    """Cancel rival claim; thief takes the site card."""
    from .artifacts import gain_artifact
    key = f"{site_coord[0]},{site_coord[1]}"
    site = state.artifact_sites.get(key)
    if site is None:
        return None
    card_id = site.get("card_id")
    if not card_id:
        return None
    discard_whisper(state, thief, "relic_thief")
    gain_artifact(state, thief, card_id)
    del state.artifact_sites[key]
    return card_id


def auto_apply_council_whispers(
    state: GameState,
    window: str,
    *,
    motion_id: str = "",
    extra_votes: dict | None = None,
    veto_flag: list | None = None,
) -> None:
    """Sim auto-heuristic (AL-40): play eligible council whispers once per window."""
    for pid, p in enumerate(state.players):
        ctx = {
            "state": state,
            "pid": pid,
            "council_window": window,
            "motion_id": motion_id,
        }
        cards = cards_for_timing(p.whisper_hand, "council", **ctx)
        if not cards:
            continue
        cid = cards[0]
        choice: dict = {"type": "whisper_play", "card": cid}
        if cid == "backroom_deal":
            choice["side"] = "for"
        result = apply_council_whisper(state, pid, choice)
        if extra_votes is not None:
            extra_votes["for"] = extra_votes.get("for", 0) + result.get("for", 0)
            extra_votes["against"] = extra_votes.get("against", 0) + result.get(
                "against", 0
            )
        if veto_flag is not None and result.get("veto"):
            veto_flag[0] = True


def apply_sabotage(
    state: GameState,
    sabotager: int,
    *,
    target_card: str,
) -> None:
    """Cancel a whisper play; both cards discard (AL-40 sim heuristic)."""
    discard_whisper(state, sabotager, "sabotage")


def auto_apply_sabotage(
    state: GameState,
    player: int,
    played_card: str,
) -> bool:
    """First eligible opponent auto-plays Sabotage (sim heuristic)."""
    for pid in offer_sabotage_players(state, player, played_card):
        apply_sabotage(state, pid, target_card=played_card)
        return True
    return False


def auto_apply_when_whispers(state: GameState, trigger: str, **ctx) -> None:
    """Auto-play obvious WHEN whispers (sim heuristic, AL-40)."""
    skip = ctx.get("skip")
    rng = ctx.get("rng")
    for pid, p in enumerate(state.players):
        if skip is not None and pid == skip:
            continue
        if trigger == "enemy_attack" and pid == ctx.get("attacker"):
            continue
        full_ctx = {"state": state, "pid": pid, "trigger": trigger, **ctx}
        cards = cards_for_timing(p.whisper_hand, "when", **full_ctx)
        if not cards:
            continue
        cid = cards[0]
        choice: dict = {"type": "whisper_play", "card": cid}
        if cid == "emergency_conscription" and ctx.get("city"):
            choice["city"] = list(ctx["city"])
        elif cid == "fortify_position" and ctx.get("hex"):
            choice["hex"] = list(ctx["hex"])
        elif cid == "blink":
            uid = ctx.get("uid")
            uids = ctx.get("uids") or []
            pick = uid if uid is not None else (uids[0] if uids else None)
            if pick is None:
                continue
            choice["uid"] = pick
        apply_when_whisper(state, pid, choice, rng=rng)


def expire_whisper_flags(state: GameState) -> None:
    for p in state.players:
        p.whisper_flags = {}
        for t in state.controlled(p.pid):
            t.suspended = []

