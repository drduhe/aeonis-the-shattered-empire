"""Phase machine (Round_Structure.md).

Milestone 2: Event phase, Strategy draft, High Council, initiative Action Phase,
and strategy primaries/secondaries (subset).
"""
from __future__ import annotations

import json
import random
from typing import Optional

from . import combat
from .build import apply_build, enumerate_builds
from .cleanup import run_cleanup
from .council import (
    AGENDA_CARDS,
    apply_motion,
    enumerate_proposal_choices,
    enumerate_vote_choices,
    reveal_agenda,
    run_emergency_council,
    tally_votes,
)
from .events import draw_event, resolve_event
from .arcane import apply_research, enumerate_research
from .artifacts import (
    apply_purge_draw,
    apply_site_claim,
    attach_building_relic,
    discard_lord_equipment,
    enumerate_attach_choices,
    enumerate_discard_lord,
    enumerate_purge_draw,
    enumerate_site_claims,
)
from .exploration import (
    apply_cleanse,
    apply_exploration_choice,
    begin_exploration,
    enumerate_cleanse,
    exploration_choices,
)
from .invariants import check_invariants
from .negotiation import (
    NegotiationSession,
    active_promises_for,
    apply_session_choice,
    check_attack_promises,
    check_vote_promises,
    enumerate_council_negotiation,
    enumerate_trade_negotiation,
    enumerate_trade_starts,
    expire_promises,
    start_session,
    validate_offer,
)
from .move import apply_move, enumerate_moves
from .objectives import (
    apply_secret_discard_at_cap,
    apply_secret_keep,
    deal_secret_draw,
    deal_round3_secrets,
    draw_public_to_row,
    record_public_progress,
    secret_cap_discard_choices,
    secret_cap_keep_choices,
    try_immediate_secrets,
    winds_draw_choices,
)
from .whispers import (
    apply_action_whisper,
    auto_apply_combat_whispers,
    auto_apply_council_whispers,
    auto_apply_sabotage,
    auto_apply_when_whispers,
    discard_whisper,
    draw_whispers,
    enumerate_action_whispers,
    enumerate_whisper_discard,
    hand_over_limit,
)
from .observations import DecisionPoint
from .production import run_production
from .recruit import apply_recruit, enumerate_recruits
from .setup import build_initial_state
from .strategy import (
    apply_draft_pick,
    apply_arcane_ascendancy_primary,
    apply_diplomatic_decree_primary,
    apply_economic_boom_primary,
    apply_expansion_strategy_primary,
    apply_imperial_mandate_primary,
    apply_resource_surge_primary,
    apply_strategy_secondary,
    begin_strategy_selection,
    build_draft_queue,
    claim_neutral_hex,
    enumerate_draft_choices,
    enumerate_expansion_primary_choices,
    enumerate_military_maneuver_attacks,
    enumerate_military_maneuver_moves,
    enumerate_secondary_choices,
    enumerate_strategy_primaries,
    enumerate_tactical_primary_recruits,
    finish_undrafted_bounty,
    initiative_order,
    pay_primary_ap,
    secondary_eligible_players,
    SECONDARY_EFFECTS,
)
from .types import (BASE_AP, BuildingType, DEFAULT_ROUND_CAP, Terrain,
                    UNIT_STATS, UnitType)
from .lords import (
    apply_council_patronage,
    apply_desert_tempest,
    apply_exaltation,
    apply_hit_and_run,
    apply_letters_of_credit,
    apply_lock_the_line,
    apply_entangling_roots,
    apply_sandstride_retreat,
    apply_shadow_sight,
    configured_roster,
    controls_unique,
    enumerate_desert_tempest,
    enumerate_hit_and_run_moves,
    enumerate_lock_the_line,
    enumerate_entangling_roots,
    enumerate_sandstride_retreats,
    is_lord,
    lord_hp,
    mark_round_used,
    round_unused,
    game_unused,
    scry_top_agenda,
    whisper_hand_limit,
)
from .lords.discoveries import (
    apply_diplomatic_tariffs,
    apply_guild_contracts_trade_influence,
    apply_shadow_network,
    apply_spellweave_doctrine,
    apply_void_anchor,
    bump_renown,
    enumerate_shadow_network,
    enumerate_void_anchor,
)

MAX_ACTIONS_PER_PLAYER_ROUND = 100


def _canon(choice: dict) -> str:
    return json.dumps(choice, sort_keys=True)


class Game:
    def __init__(self, config: dict, seed: int):
        self.config = dict(config)
        self.seed = seed
        self.rng = random.Random(seed)
        roster = configured_roster(self.config, int(self.config["players"]))
        if any(roster):
            lord_config = dict(self.config.get("lord_asymmetry", {}))
            lord_config["enabled"] = True
            lord_config["lords"] = roster
            self.config["lord_asymmetry"] = lord_config
        self.state = build_initial_state(self.config, self.rng)
        self.over = False
        self.verdict: Optional[str] = None
        self.choices_log: list = []
        self.degenerate_flags: list = []
        self.round_cap_finish = False
        self._actions_taken: dict = {}
        self._initiative_queue: list[int] = []
        self._battle: Optional[combat.Battle] = None
        self._battle_stage: Optional[str] = None  # lord_combat | defender_retreat | press | hit_and_run | done
        self._battle_lord_substage: Optional[str] = None
        self._scry_queue: list[int] = []
        self._round_hashes: list = []
        self._pending: Optional[DecisionPoint] = None
        self.combat_stats = {
            "battles": 0,
            "attacker_wins": 0,
            "defender_wins": 0,
            "stratified": combat.empty_stratified_stats(),
        }
        self.ap_spread_log: list[int] = []
        self.action_count_log: list[dict[int, int]] = []
        self.pass_log: list[dict] = []
        self.build_counts: dict[int, int] = {p.pid: 0 for p in self.state.players}
        self.bookkeeping_stats = {
            "upkeep_checks": 0,
            "upkeep_payments": 0,
            "upkeep_failures": 0,
            "upkeep_gold_paid": 0,
            "upkeep_mana_paid": 0,
        }
        self._draft_queue: list[int] = []
        self._followup: Optional[dict] = None
        self._deferred_followup: Optional[dict] = None
        self._council_proposal_queue: list[int] = []
        self._council_motions: list[dict] = []
        self._council_vote_motion_idx: int = 0
        self._council_vote_queue: list[int] = []
        self._council_ballots: list[dict] = []
        self.event_stats = {"resolved": 0, "by_card": {}}
        self.council_stats = {
            "motions_proposed": 0,
            "motions_passed": 0,
            "motions_failed": 0,
            "votes_yes": 0,
            "votes_no": 0,
            "influence_spent": 0,
        }
        self.negotiation_stats = {
            "offers_proposed": 0,
            "offers_accepted": 0,
            "offers_rejected": 0,
            "counters": 0,
            "promises_made": 0,
            "promises_kept": 0,
            "promises_broken": 0,
            "vote_promises_made": 0,
            "vote_promises_kept": 0,
            "vote_promises_broken": 0,
            "non_aggression_promises_made": 0,
            "non_aggression_promises_kept": 0,
            "non_aggression_promises_broken": 0,
            "attack_target_promises_made": 0,
            "attack_target_promises_kept": 0,
            "attack_target_promises_broken": 0,
            "future_payment_promises_made": 0,
            "future_payment_promises_kept": 0,
            "future_payment_promises_broken": 0,
        }
        self.promises_log: list[dict] = []
        self.negotiation_dialogue_log: list[dict] = []
        self.building_stats = {
            "bank_conversions": 0,
            "forge_recruits": 0,
            "market_trades": 0,
        }
        self.whisper_stats = {"drawn": 0, "played": 0, "discarded": 0, "sabotage": 0}
        self._council_extra_votes = {"for": 0, "against": 0}
        self._council_veto = False
        self.first_artifact_round: int | None = None
        self._negotiation_session: Optional[NegotiationSession] = None
        self._council_negotiation_queue: list[int] = []
        self._trade_used: dict[int, bool] = {}
        self._trade_initiator: Optional[int] = None
        self._trade_consumes_turn = True
        self._exploration_pending: Optional[dict] = None
        self._artifact_followup: Optional[dict] = None
        self._research_followup: Optional[dict] = None
        self._objective_cap_queue: list[dict] = []
        self._objective_draw_queue: list[int] = []
        self._objective_followup: Optional[dict] = None
        self._whisper_discard_queue: list[int] = []
        self._round_start()

    # ---- phases ----
    def _ap_bonus(self, pid: int) -> int:
        s = self.state
        cities = sum(1 for t in s.controlled(pid) if t.terrain == Terrain.CITY)
        guild = sum(1 for t in s.controlled(pid)
                    if t.has(BuildingType.GUILD_HALL))
        renown_bonus = 0 if s.slim_renown else (1 if s.player(pid).renown >= 5 else 0)
        bonus = min(2, cities) + guild + renown_bonus
        if s.ap_bonus_cap is not None:
            bonus = min(bonus, s.ap_bonus_cap)
        return bonus

    def _apply_rally(self) -> None:
        s = self.state
        if not s.rally:
            return
        players = s.players
        pid = min(
            players,
            key=lambda p: (p.vp, p.renown, -p.influence, p.pid),
        ).pid
        s.player(pid).ap += 1

    def _round_start(self) -> None:
        s = self.state
        if s.round > DEFAULT_ROUND_CAP:
            # Sim-only: end at printed round cap with current VP (tiebreak) instead of
            # hanging until timeout. See sim/README.md § pacing.
            self.round_cap_finish = True
            self._end("completed")
            return
        d = s.to_dict()
        d.pop("round")  # only the counter differs in a true stall
        h = json.dumps(d, sort_keys=True)
        if self._round_hashes and self._round_hashes[-1] == h:
            self._end("stalled")
            return
        self._round_hashes.append(h)
        s.open_roads = False
        s.council_crisis = False
        self._exploration_pending = None
        # Tiles.md control method 1: sole-occupier hexes flip at Round Start
        for t in s.tiles.values():
            owners = {u.owner for u in t.units}
            if len(owners) == 1:
                t.controller = owners.pop()
        # Combat.md §2.1.3: Lords heal to full HP at Round Start
        for t in s.tiles.values():
            for u in t.units:
                if u.type == UnitType.LORD:
                    u.hp = lord_hp(s, u.owner, UNIT_STATS[UnitType.LORD].hp)
        from .lords.legendaries import apply_heartwood_round_start_hp, hall_of_whispers_extra_draw
        apply_heartwood_round_start_hp(s)
        s.trades_this_round = 0
        for p in s.players:
            p.lord_round = {}
            pending = p.pending_ap
            p.pending_ap = 0
            p.ap = BASE_AP + p.banked + self._ap_bonus(p.pid) + pending
            p.banked = 0
            whisper_draw = 3 if is_lord(s, p.pid, "nyxara") else 2
            draw_whispers(s, p.pid, whisper_draw, self.rng)
            self.whisper_stats["drawn"] += whisper_draw
            if controls_unique(s, p.pid, "obsidian_spire"):
                draw_whispers(s, p.pid, 1, self.rng)
                self.whisper_stats["drawn"] += 1
            if hall_of_whispers_extra_draw(s, p.pid):
                draw_whispers(s, p.pid, 1, self.rng)
                self.whisper_stats["drawn"] += 1
            while p.pending_whisper_draws > 0:
                draw_whispers(s, p.pid, 1, self.rng)
                self.whisper_stats["drawn"] += 1
                p.pending_whisper_draws -= 1
        self._apply_rally()
        self.ap_spread_log.append(
            max(p.ap for p in s.players) - min(p.ap for p in s.players)
        )
        self._actions_taken = {p.pid: 0 for p in s.players}
        self._meaningful_actions_taken = {p.pid: 0 for p in s.players}
        self._pass_order: list[int] = []
        self._initiative_queue = []
        self._followup = None
        self._deferred_followup = None
        self._council_proposal_queue = []
        self._council_motions = []
        self._council_vote_motion_idx = 0
        self._council_vote_queue = []
        self._council_ballots = []
        self._council_negotiation_queue = []
        self._negotiation_session = None
        self._trade_used = {p.pid: False for p in s.players}
        self._objective_cap_queue = []
        self._objective_draw_queue = []
        self._objective_followup = None
        if s.round == 3:
            self._objective_cap_queue = deal_round3_secrets(s, self.rng)
        self._run_event_phase()
        self._objective_draw_queue.extend(s.pending_winds_draws)
        s.pending_winds_draws.clear()
        if s.round >= 2:
            from .objectives import draw_public_to_row
            draw_public_to_row(s, self.rng, round_start=True)
        begin_strategy_selection(s)
        self._draft_queue = build_draft_queue(s, s.speaker)

    def _run_event_phase(self) -> None:
        card = draw_event(self.state, self.rng)
        if not card:
            return
        resolve_event(self.state, card, self.rng)
        self.event_stats["resolved"] += 1
        by = self.event_stats["by_card"]
        by[card] = by.get(card, 0) + 1

    def _begin_council_phase(self) -> None:
        self._scry_queue = [
            p.pid for p in self.state.players if is_lord(self.state, p.pid, "seraphel")
        ]
        if not self._scry_queue:
            self._reveal_council_agenda()
        self._council_proposal_queue = initiative_order(self.state)
        self._council_motions = []
        self._council_vote_motion_idx = 0
        self._council_vote_queue = []
        self._council_ballots = []
        self._council_extra_votes = {"for": 0, "against": 0}
        self._council_veto = False

    def _reveal_council_agenda(self) -> None:
        reveal_agenda(self.state, self.rng)
        auto_apply_council_whispers(
            self.state,
            "agenda_reveal",
            motion_id=self.state.agenda_revealed or "",
        )

    def _council_extra_choices(self, pid: int) -> list[dict]:
        out = []
        if is_lord(self.state, pid, "cassian") and round_unused(
            self.state, pid, "letters_of_credit",
        ) and self.state.player(pid).influence >= 1:
            out.append({"type": "letters_of_credit"})
        return out

    def _start_council_voting(self) -> None:
        if not self._council_motions:
            self._begin_action_phase()
            return
        self._council_vote_motion_idx = 0
        self._council_ballots = []
        self._council_vote_queue = []
        self._council_negotiation_queue = initiative_order(self.state)

    def _council_motion_id(self) -> str:
        if not self._council_motions:
            return ""
        return self._council_motions[self._council_vote_motion_idx]["motion"]

    def _negotiation_decision(self) -> Optional[DecisionPoint]:
        session = self._negotiation_session
        if session is not None:
            if session.phase == "respond":
                pid = session.target
            elif session.phase == "counter_review":
                pid = session.proposer
            else:
                pid = session.proposer
            if session.window == "council":
                choices = enumerate_council_negotiation(
                    self.state,
                    pid,
                    motion=session.motion or "",
                    session=session,
                )
                choices = self._council_extra_choices(pid) + choices
            else:
                choices = enumerate_trade_negotiation(
                    self.state, pid, session=session,
                )
            return DecisionPoint(
                kind="negotiation",
                phase="council" if session.window == "council" else "action",
                pid=pid,
                choices=choices,
                context={
                    "window": session.window,
                    "motion": session.motion,
                    "proposer": session.proposer,
                    "target": session.target,
                    "gives": dict(session.gives),
                    "gets": dict(session.gets),
                    "promises": list(session.promises),
                    "deal_kind": session.deal_kind,
                    "phase": session.phase,
                    "countered": session.countered,
                    "dialogue": list(session.dialogue),
                    "active_promises": active_promises_for(self.promises_log, pid),
                },
            )
        if self._council_negotiation_queue:
            pid = self._council_negotiation_queue[0]
            motion = self._council_motion_id()
            return DecisionPoint(
                kind="negotiation",
                phase="council",
                pid=pid,
                choices=self._council_extra_choices(pid) + enumerate_council_negotiation(
                    self.state, pid, motion=motion, session=None,
                ),
                context={
                    "window": "council",
                    "motion": motion,
                    "dialogue": [],
                    "active_promises": active_promises_for(self.promises_log, pid),
                },
            )
        return None

    def _advance_council_vote_motion(self) -> None:
        self._council_vote_motion_idx += 1
        self._council_ballots = []
        if self._council_vote_motion_idx >= len(self._council_motions):
            self._begin_action_phase()
            return
        self._council_vote_queue = []
        self._council_negotiation_queue = initiative_order(self.state)

    def _council_decision(self) -> Optional[DecisionPoint]:
        if self._council_proposal_queue:
            pid = self._council_proposal_queue[0]
            return DecisionPoint(
                kind="council_propose",
                phase="council",
                pid=pid,
                choices=self._council_extra_choices(pid) + enumerate_proposal_choices(self.state, pid),
                context={"agenda": self.state.agenda_revealed},
            )
        if (
            self._council_motions
            and self._council_vote_motion_idx < len(self._council_motions)
        ):
            neg = self._negotiation_decision()
            if neg is not None:
                return neg
            if not self._council_vote_queue:
                self._council_vote_queue = initiative_order(self.state)
            motion = self._council_motions[self._council_vote_motion_idx]
            pid = self._council_vote_queue[0]
            choices = enumerate_vote_choices(self.state, pid, motion["motion"])
            choices = self._council_extra_choices(pid) + choices
            binding = next((
                pr for pr in self.promises_log
                if pr.get("binding") and pr.get("kept") is None
                and pr.get("from") == pid and pr.get("motion") == motion["motion"]
            ), None)
            if binding is not None:
                expected = bool(binding.get("support", True))
                choices = [c for c in choices if bool(c.get("support")) == expected]
            if is_lord(self.state, pid, "auriel") and round_unused(
                self.state, pid, "sanctify",
            ):
                choices += [{**c, "sanctify": True} for c in choices]
            return DecisionPoint(
                kind="council_vote",
                phase="council",
                pid=pid,
                choices=choices,
                context={
                    "motion": motion["motion"],
                    "proposer": motion["proposer"],
                },
            )
        return None

    def _begin_action_phase(self) -> None:
        """Action Phase turn order from lowest Strategy card (Strategy.md §1.4)."""
        self._initiative_queue = initiative_order(self.state)
        self._council_proposal_queue = []
        self._council_motions = []
        self._council_vote_queue = []

    def _research_decision(self) -> Optional[DecisionPoint]:
        fu = self._research_followup
        if fu is None:
            return None
        pid = fu["pid"]
        free = bool(fu.get("free"))
        choices = enumerate_research(self.state, pid, free=free, ap_waived=free)
        if not choices:
            self._research_followup = None
            return None
        if fu.get("seraphel_second"):
            choices = choices + [{"type": "research_skip"}]
        return DecisionPoint(
            kind="research",
            phase="action",
            pid=pid,
            choices=choices,
            context={"free": free, "seraphel_second": bool(fu.get("seraphel_second"))},
        )

    def _track_whisper_play(self, pid: int, card: str) -> None:
        self.whisper_stats["played"] += 1
        apply_shadow_sight(self.state, pid)
        if auto_apply_sabotage(self.state, pid, card):
            self.whisper_stats["sabotage"] += 1

    def _after_gain_artifact(self, pid: int, pending: str | None) -> None:
        if self.first_artifact_round is None:
            self.first_artifact_round = self.state.round
        auto_apply_when_whispers(
            self.state,
            "artifact_claim",
            claimer=pid,
            skip=pid,
            rng=self.rng,
        )
        if pending == "discard_lord":
            self._artifact_followup = {"kind": "discard_lord", "pid": pid}
        elif pending == "attach_building":
            if enumerate_attach_choices(self.state, pid):
                self._artifact_followup = {"kind": "attach", "pid": pid}

    def _artifact_decision(self) -> Optional[DecisionPoint]:
        fu = self._artifact_followup
        if fu is None:
            return None
        pid = fu["pid"]
        if fu["kind"] == "discard_lord":
            choices = enumerate_discard_lord(self.state, pid)
        else:
            choices = enumerate_attach_choices(self.state, pid)
        if not choices:
            self._artifact_followup = None
            return None
        return DecisionPoint(
            kind="artifact",
            phase="action",
            pid=pid,
            choices=choices,
            context={"step": fu["kind"]},
        )

    def _after_unit_entry(self, pid: int, coord: tuple) -> bool:
        """First entry to unexplored hex draws exploration event. Returns True if choice needed."""
        card, needs = begin_exploration(self.state, pid, coord, self.rng)
        if card is None:
            return False
        if needs:
            after = "combat" if self._battle is not None else "action"
            self._exploration_pending = {
                "pid": pid,
                "coord": coord,
                "card": card,
                "after": after,
            }
            return True
        return False

    def _exploration_decision(self) -> DecisionPoint:
        ep = self._exploration_pending
        assert ep is not None
        return DecisionPoint(
            kind="exploration",
            phase="action" if ep["after"] == "action" else "combat",
            pid=ep["pid"],
            choices=exploration_choices(ep["card"], self.state, ep["pid"], ep["coord"]),
            context={"coord": list(ep["coord"]), "card": ep["card"]},
        )

    def _finish_exploration(self) -> None:
        ep = self._exploration_pending
        if ep is None:
            return
        defer = ep.get("defer")
        after = ep["after"]
        pid = ep["pid"]
        self._exploration_pending = None
        if after == "combat":
            self._battle_stage = "done"
            return
        if self._artifact_followup:
            return
        if defer and defer[0] == "mm":
            _, dpid, card = defer
            attacks = enumerate_military_maneuver_attacks(self.state, dpid)
            if attacks:
                self._followup = {"kind": "mm_attack", "pid": dpid, "card": card}
            else:
                self._start_secondary_window(dpid, card)
        else:
            self._finish_action_turn(pid)

    def _rotate_initiative(self, pid: int) -> None:
        if self._initiative_queue and self._initiative_queue[0] == pid:
            self._initiative_queue.append(self._initiative_queue.pop(0))

    def _remove_from_initiative(self, pid: int) -> None:
        if pid in self._initiative_queue:
            self._initiative_queue.remove(pid)

    def _start_secondary_window(self, owner_pid: int, card_id: str) -> None:
        queue = secondary_eligible_players(self.state, owner_pid, card_id)
        payload = {
            "kind": "strategy_secondary",
            "owner": owner_pid,
            "card": card_id,
            "queue": queue,
        }
        if self._battle is not None:
            self._deferred_followup = payload
        else:
            self._followup = payload

    def _finish_action_turn(self, pid: int) -> None:
        self._rotate_initiative(pid)

    def _followup_decision(self) -> Optional[DecisionPoint]:
        fu = self._followup
        if fu is None:
            return None
        kind = fu["kind"]
        if kind == "mm_move":
            pid = fu["pid"]
            moves = enumerate_military_maneuver_moves(self.state, pid)
            choices = moves + [{"type": "mm_skip_move", "card": fu["card"]}]
            return DecisionPoint(
                kind="strategy_primary",
                phase="action",
                pid=pid,
                choices=choices,
                context={"step": "mm_move", "card": fu["card"]},
            )
        if kind == "mm_attack":
            pid = fu["pid"]
            attacks = enumerate_military_maneuver_attacks(self.state, pid)
            choices = attacks + [{"type": "mm_skip_attack", "card": fu["card"]}]
            return DecisionPoint(
                kind="strategy_primary",
                phase="action",
                pid=pid,
                choices=choices,
                context={"step": "mm_attack", "card": fu["card"]},
            )
        if kind == "strategy_secondary":
            if not fu["queue"]:
                owner = fu["owner"]
                self._followup = None
                self._finish_action_turn(owner)
                return None
            pid = fu["queue"][0]
            choices = enumerate_secondary_choices(
                self.state, pid, fu["card"], fu["owner"],
            )
            if not choices:
                fu["queue"].pop(0)
                return self._followup_decision()
            return DecisionPoint(
                kind="strategy_secondary",
                phase="action",
                pid=pid,
                choices=choices,
                context={"card": fu["card"], "owner": fu["owner"]},
            )
        if kind == "expansion_primary":
            pid = fu["pid"]
            card = fu["card"]
            choices = enumerate_expansion_primary_choices(self.state, pid)
            if not choices:
                self._followup = None
                self._start_secondary_window(pid, card)
                return self._followup_decision()
            return DecisionPoint(
                kind="strategy_primary",
                phase="action",
                pid=pid,
                choices=choices + [{"type": "expansion_skip", "card": card}],
                context={"step": "expansion_claim", "card": card},
            )
        if kind == "tactical_primary":
            pid = fu["pid"]
            card = fu["card"]
            recs = enumerate_tactical_primary_recruits(self.state, pid)
            if not recs:
                self._followup = None
                self._start_secondary_window(pid, card)
                return self._followup_decision()
            return DecisionPoint(
                kind="strategy_primary",
                phase="action",
                pid=pid,
                choices=recs + [{"type": "tactical_skip", "card": card}],
                context={"step": "tactical_recruit", "card": card},
            )
        if kind == "expansion_secondary":
            pid = fu["pid"]
            card = fu["card"]
            choices = enumerate_expansion_primary_choices(self.state, pid)
            if not choices:
                self._followup = None
                return None
            return DecisionPoint(
                kind="strategy_primary",
                phase="action",
                pid=pid,
                choices=choices,
                context={"step": "expansion_secondary_claim", "card": card},
            )
        if kind == "tactical_secondary_recruit":
            pid = fu["pid"]
            card = fu["card"]
            from .recruit import enumerate_recruits
            recs = [
                {**c, "type": "recruit"}
                for c in enumerate_recruits(self.state, pid)
            ]
            if not recs:
                self._followup = None
                return None
            return DecisionPoint(
                kind="action",
                phase="action",
                pid=pid,
                choices=recs,
                context={"secondary_recruit": card},
            )
        if kind == "arcane_secondary_research":
            pid = fu["pid"]
            card = fu["card"]
            choices = enumerate_research(self.state, pid, ap_waived=True)
            if not choices:
                self._followup = None
                return None
            return DecisionPoint(
                kind="research",
                phase="action",
                pid=pid,
                choices=choices,
                context={"ap_waived": True, "card": card},
            )
        return None

    def _after_resource_or_boom_primary(self, pid: int, card_id: str) -> None:
        self._start_secondary_window(pid, card_id)

    def _after_military_primary_paid(self, pid: int, card_id: str) -> None:
        moves = enumerate_military_maneuver_moves(self.state, pid)
        if moves:
            self._followup = {"kind": "mm_move", "pid": pid, "card": card_id}
        else:
            attacks = enumerate_military_maneuver_attacks(self.state, pid)
            if attacks:
                self._followup = {"kind": "mm_attack", "pid": pid, "card": card_id}
            else:
                self._start_secondary_window(pid, card_id)

    def _end(self, verdict: str) -> None:
        self.over = True
        self.verdict = verdict
        self._pending = None

    def _advance_phases(self) -> None:
        """All players have passed: Production, Cleanup, next round or end."""
        self.action_count_log.append(dict(self._meaningful_actions_taken))
        prod_stats = run_production(self.state, rng=self.rng)
        self.building_stats["bank_conversions"] += len(
            prod_stats.get("bank_conversions", {})
        )
        upkeep = prod_stats.get("upkeep", {})
        for source, target in (
            ("checks", "upkeep_checks"),
            ("payments", "upkeep_payments"),
            ("failures", "upkeep_failures"),
            ("gold_paid", "upkeep_gold_paid"),
            ("mana_paid", "upkeep_mana_paid"),
        ):
            self.bookkeeping_stats[target] += int(upkeep.get(source, 0))
        for p in self.state.players:
            try_immediate_secrets(self.state, p.pid)
        run_cleanup(self.state, self.rng)
        expire_promises(self.promises_log, self.state.round, self.negotiation_stats)
        check_invariants(self.state)
        self._whisper_discard_queue = [
            p.pid for p in self.state.players if hand_over_limit(self.state, p.pid)
        ]
        if self.state.final_round:
            self._end("completed")
            return
        self._round_start()

    # ---- decision loop ----
    def _active_pid(self) -> Optional[int]:
        if not self._initiative_queue:
            return None
        return self._initiative_queue[0]

    def _action_choices(self, pid: int) -> list:
        s = self.state
        if self._actions_taken[pid] >= MAX_ACTIONS_PER_PLAYER_ROUND:
            if "action_cap" not in self.degenerate_flags:
                self.degenerate_flags.append("action_cap")
            return [{"type": "pass"}]
        out = [{"type": "pass"}]
        out.extend(enumerate_strategy_primaries(s, pid))
        out.extend(enumerate_moves(s, pid))
        out.extend(enumerate_recruits(s, pid))
        out.extend(enumerate_builds(s, pid))
        out.extend(combat.enumerate_attacks(s, pid))
        # Market (Buildings.md): the once-per-round trade initiation costs
        # 0 AP with an active Market; limit stays one trade per round (AL-27).
        # Grand Exchange: one extra 0-AP trade once/round.
        from .lords.legendaries import (
            controls_legendary,
            enumerate_nexus_teleport,
            enumerate_warcamp_cavalry_move,
        )
        ge_extra = (
            controls_legendary(s, pid, BuildingType.GRAND_EXCHANGE)
            and round_unused(s, pid, "ge_extra_trade")
        )
        if not self._trade_used.get(pid, False) or ge_extra:
            free = self._has_active_market(pid) or (
                is_lord(s, pid, "cassian") and round_unused(s, pid, "ledger_trade")
            ) or ge_extra
            if free or s.player(pid).ap >= 1:
                out.extend(self._enumerate_trade_starts(pid))
        out.extend(enumerate_cleanse(s, pid))
        out.extend(enumerate_purge_draw(s, pid))
        out.extend(enumerate_site_claims(s, pid))
        out.extend(enumerate_attach_choices(s, pid))
        out.extend(enumerate_discard_lord(s, pid))
        # Arcane Sanctum: free Tier I research once/round
        if (
            controls_legendary(s, pid, BuildingType.ARCANE_SANCTUM)
            and round_unused(s, pid, "sanctum_free_research")
        ):
            out.extend(enumerate_research(s, pid, free=True, ap_waived=True))
        else:
            out.extend(enumerate_research(s, pid))
        out.extend(enumerate_action_whispers(s, pid))
        out.extend(enumerate_desert_tempest(s, pid))
        out.extend(enumerate_shadow_network(s, pid))
        out.extend(enumerate_void_anchor(s, pid))
        out.extend(enumerate_nexus_teleport(s, pid))
        out.extend(enumerate_warcamp_cavalry_move(s, pid))
        if is_lord(s, pid, "auriel") and round_unused(s, pid, "exaltation"):
            if s.player(pid).influence >= 3:
                out.append({"type": "exaltation"})
        return out

    def _has_active_market(self, pid: int) -> bool:
        return any(t.active(BuildingType.MARKET)
                   for t in self.state.controlled(pid))

    def _grant_bazaar_trade_gold(self, state) -> None:
        for t in state.tiles.values():
            if t.unique_tile_id != "caravan_bazaar" or t.controller is None:
                continue
            pid = t.controller
            if round_unused(state, pid, "bazaar_trade_gold"):
                state.player(pid).gold += 1
                mark_round_used(state, pid, "bazaar_trade_gold")
            break

    def _enumerate_trade_starts(self, pid: int) -> list[dict]:
        return enumerate_trade_starts(self.state, pid)

    def _close_negotiation_session(self, window: str) -> None:
        if window == "trade" and self._trade_initiator is not None:
            if self._trade_consumes_turn:
                self._finish_action_turn(self._trade_initiator)
            self._trade_initiator = None
            self._trade_consumes_turn = True

    def _submit_negotiation(self, dp: DecisionPoint, choice: dict) -> None:
        s = self.state
        t = choice["type"]
        if self._negotiation_session is None:
            if t == "negotiation_skip":
                if (
                    self._council_negotiation_queue
                    and self._council_negotiation_queue[0] == dp.pid
                ):
                    self._council_negotiation_queue.pop(0)
                return
            if t == "negotiation_propose":
                target = int(choice["target"])
                err = validate_offer(
                    s, dp.pid, target,
                    choice.get("gives", {}), choice.get("gets", {}),
                    choice.get("promises"),
                )
                if err:
                    raise ValueError(err)
                motion = dp.context.get("motion")
                self._negotiation_session = start_session(
                    window="council",
                    proposer=dp.pid,
                    target=target,
                    gives=choice.get("gives", {}),
                    gets=choice.get("gets", {}),
                    promises=choice.get("promises"),
                    motion=motion,
                    state=s,
                    deal_kind=str(choice.get("deal_kind", "resource_trade")),
                )
                self.negotiation_stats["offers_proposed"] += 1
                if (
                    self._council_negotiation_queue
                    and self._council_negotiation_queue[0] == dp.pid
                ):
                    self._council_negotiation_queue.pop(0)
            return
        active_session = self._negotiation_session
        window = active_session.window
        before_promises = len(self.promises_log)
        session, outcome = apply_session_choice(
            s,
            self._negotiation_session,
            choice,
            promises_log=self.promises_log,
            stats=self.negotiation_stats,
        )
        self._negotiation_session = session
        added = len(self.promises_log) - before_promises
        if outcome == "accepted" and added:
            actual_proposer = (
                active_session.counter_proposer
                if active_session.phase == "counter_review"
                and active_session.counter_proposer is not None
                else active_session.proposer
            )
            cassian = actual_proposer if (
                is_lord(s, actual_proposer, "cassian")
                and round_unused(s, actual_proposer, "binding_deal")
            ) else None
            if cassian is not None:
                for pr in self.promises_log[before_promises:]:
                    if pr.get("kind") == "vote" and pr.get("motion") == active_session.motion:
                        pr["binding"] = True
                        mark_round_used(s, cassian, "binding_deal")
                        break
        if added:
            self.negotiation_stats["promises_made"] += added
        if session is None:
            self._close_negotiation_session(window)

    def record_negotiation_dialogue(
        self, dp: DecisionPoint, choice: dict, message: str, intent: str = "",
    ) -> None:
        """Record bounded, public table talk attached to a structured choice."""
        cleaned = " ".join(str(message or "").split())[:500]
        if dp.kind != "negotiation" or not cleaned:
            return
        entry = {
            "round": self.state.round,
            "phase": dp.phase,
            "speaker": dp.pid,
            "choice_type": choice.get("type"),
            "deal_kind": choice.get("deal_kind", dp.context.get("deal_kind", "")),
            "intent": str(intent or "")[:80],
            "message": cleaned,
            "authoritative_terms": {
                "gives": dict(
                    choice.get("gives", dp.context.get("gives", {})) or {},
                ),
                "gets": dict(
                    choice.get("gets", dp.context.get("gets", {})) or {},
                ),
                "promises": list(
                    choice.get("promises", dp.context.get("promises", [])) or [],
                ),
            },
        }
        self.negotiation_dialogue_log.append(entry)
        if self._negotiation_session is not None:
            self._negotiation_session.dialogue.append(entry)

    def _whisper_discard_decision(self) -> Optional[DecisionPoint]:
        if not self._whisper_discard_queue:
            return None
        pid = self._whisper_discard_queue[0]
        return DecisionPoint(
            kind="whisper_discard",
            phase="cleanup",
            pid=pid,
            choices=enumerate_whisper_discard(self.state, pid),
            context={
                "over_limit": len(self.state.player(pid).whisper_hand)
                - whisper_hand_limit(self.state, pid, 7),
            },
        )

    def _ensure_objective_cap_followup(self) -> None:
        if self._objective_followup is None and self._objective_cap_queue:
            self._objective_followup = self._objective_cap_queue.pop(0)

    def _objective_draw_decision(self) -> Optional[DecisionPoint]:
        self._ensure_objective_cap_followup()
        fu = self._objective_followup
        if fu is not None:
            pid = fu["pid"]
            if fu["step"] == "keep":
                return DecisionPoint(
                    kind="objective_draw",
                    phase="round_start",
                    pid=pid,
                    choices=secret_cap_keep_choices(fu["drawn"]),
                    context={"step": "keep", "drawn": fu["drawn"]},
                )
            kept = fu["kept"]
            p = self.state.player(pid)
            return DecisionPoint(
                kind="objective_draw",
                phase="round_start",
                pid=pid,
                choices=secret_cap_discard_choices(list(p.secret_objectives)),
                context={"step": "discard", "kept": kept},
            )
        if self._objective_draw_queue:
            pid = self._objective_draw_queue[0]
            return DecisionPoint(
                kind="objective_draw",
                phase="round_start",
                pid=pid,
                choices=winds_draw_choices(self.state, pid),
                context={"source": "winds"},
            )
        return None

    def _finish_objective_cap_step(self) -> None:
        self._objective_followup = None
        self._ensure_objective_cap_followup()

    def _strategy_draft_decision(self) -> Optional[DecisionPoint]:
        if not self._draft_queue:
            return None
        pid = self._draft_queue[0]
        return DecisionPoint(
            kind="strategy_draft",
            phase="strategy",
            pid=pid,
            choices=enumerate_draft_choices(self.state),
        )

    def next_decision(self) -> Optional[DecisionPoint]:
        if self.over:
            return None
        if self._pending is not None:
            return self._pending
        obj_dp = self._objective_draw_decision()
        if obj_dp is not None:
            self._pending = obj_dp
            return self._pending
        wh_dp = self._whisper_discard_decision()
        if wh_dp is not None:
            self._pending = wh_dp
            return self._pending
        if self._research_followup is not None:
            res_dp = self._research_decision()
            if res_dp is not None:
                self._pending = res_dp
                return self._pending
            fu = self._research_followup
            pid = fu.get("pid")
            free = fu.get("free")
            self._research_followup = None
            if (
                free
                and pid is not None
                and "arcane_ascendancy" in self.state.player(pid).primary_used
            ):
                self._start_secondary_window(pid, "arcane_ascendancy")
            elif pid is not None:
                self._finish_action_turn(pid)
        if self._artifact_followup is not None:
            art_dp = self._artifact_decision()
            if art_dp is not None:
                self._pending = art_dp
                return self._pending
        if self._exploration_pending is not None:
            self._pending = self._exploration_decision()
            return self._pending
        if self._battle is not None:
            self._pending = self._battle_decision()
            if self._pending is not None:
                return self._pending
        followup_dp = self._followup_decision()
        if followup_dp is not None:
            self._pending = followup_dp
            return self._pending
        draft_dp = self._strategy_draft_decision()
        if draft_dp is not None:
            self._pending = draft_dp
            return self._pending
        if self._scry_queue:
            pid = self._scry_queue[0]
            self._pending = DecisionPoint(
                kind="scry_ack",
                phase="council",
                pid=pid,
                choices=[{"type": "scry_ack"}],
                context={"top_agenda": scry_top_agenda(self.state)},
            )
            return self._pending
        council_dp = self._council_decision()
        if council_dp is not None:
            self._pending = council_dp
            return self._pending
        if self._negotiation_session and self._negotiation_session.window == "trade":
            trade_neg = self._negotiation_decision()
            if trade_neg is not None:
                self._pending = trade_neg
                return self._pending
        pid = self._active_pid()
        if pid is None:
            self._advance_phases()
            return None if self.over else self.next_decision()
        self._pending = DecisionPoint(
            kind="action",
            phase="action",
            pid=pid,
            choices=self._action_choices(pid),
        )
        return self._pending

    def _lord_combat_decision(self) -> Optional[DecisionPoint]:
        b = self._battle
        assert b is not None
        sub = self._battle_lord_substage
        if sub == "sandstride":
            choices = enumerate_sandstride_retreats(self.state, b)
            actionable = [c for c in choices if c["type"] != "sandstride_skip"]
            if actionable:
                pid = (
                    b.defender
                    if is_lord(self.state, b.defender, "rakhis")
                    else b.attacker
                )
                return DecisionPoint(
                    kind="sandstride_retreat",
                    phase="combat",
                    pid=pid,
                    choices=choices,
                    context={"target": list(b.target)},
                )
            self._battle_lord_substage = "lock_line"
            return self._lord_combat_decision()
        if sub == "lock_line":
            combat.declare_attacker_targets(b)
            choices = enumerate_lock_the_line(self.state, b)
            if choices:
                return DecisionPoint(
                    kind="lock_the_line",
                    phase="combat",
                    pid=b.defender,
                    choices=choices,
                    context={"target": list(b.target)},
                )
            self._battle_lord_substage = "entangling_roots"
            return self._lord_combat_decision()
        if sub == "entangling_roots":
            choices = enumerate_entangling_roots(self.state, b)
            if choices:
                return DecisionPoint(
                    kind="entangling_roots",
                    phase="combat",
                    pid=b.defender,
                    choices=choices,
                    context={"target": list(b.target)},
                )
            self._battle_lord_substage = "execute"
            return self._lord_combat_decision()
        if sub == "execute":
            combat.execute_battle_round(self.state, b, self.rng)
            self._battle_stage = "defender_retreat"
            self._battle_lord_substage = None
            return self._battle_decision()
        return None

    def _lord_asymmetry_enabled(self) -> bool:
        return bool(self.config.get("lord_asymmetry", {}).get("enabled", True))

    def _start_lord_combat_round(self) -> None:
        combat.prepare_battle_round(self.state, self._battle)
        if not self._lord_asymmetry_enabled():
            combat.execute_battle_round(self.state, self._battle, self.rng)
            self._battle_stage = "defender_retreat"
            return
        self._battle_stage = "lord_combat"
        self._battle_lord_substage = "sandstride"

    def _battle_decision(self) -> Optional[DecisionPoint]:
        b = self._battle
        if b.winner is not None or self._battle_stage == "done":
            if (
                self._lord_asymmetry_enabled()
                and b.winner == "attacker"
                and is_lord(self.state, b.attacker, "rakhis")
                and game_unused(self.state, b.attacker, "hit_and_run")
            ):
                moves = enumerate_hit_and_run_moves(self.state, b)
                if moves:
                    self._battle_stage = "hit_and_run"
                    return DecisionPoint(
                        kind="hit_and_run",
                        phase="combat",
                        pid=b.attacker,
                        choices=moves + [{"type": "hit_and_run_skip"}],
                        context={"target": list(b.target)},
                    )
            combat.finish_battle(self.state, b)
            combat.record_battle_outcome(self.combat_stats, b)
            check_invariants(self.state)
            self._battle = None
            self._battle_stage = None
            self._battle_lord_substage = None
            if self._deferred_followup is not None:
                self._followup = self._deferred_followup
                self._deferred_followup = None
            return None
        if self._battle_stage == "lord_combat":
            return self._lord_combat_decision()
        if self._battle_stage == "hit_and_run":
            moves = enumerate_hit_and_run_moves(self.state, b)
            return DecisionPoint(
                kind="hit_and_run",
                phase="combat",
                pid=b.attacker,
                choices=moves + [{"type": "hit_and_run_skip"}],
                context={"target": list(b.target)},
            )
        if self._battle_stage == "defender_retreat":
            retreats = combat.enumerate_defender_retreats(self.state, b)
            if retreats:
                return DecisionPoint(
                    kind="defender_retreat",
                    phase="combat",
                    pid=b.defender,
                    choices=retreats + [{"type": "hold"}],
                    context={"target": list(b.target)},
                )
            self._battle_stage = "press"
        if self._battle_stage == "press":
            if b.rounds < 2 and self.state.player(b.attacker).ap >= combat.PRESS_AP:
                return DecisionPoint(
                    kind="press",
                    phase="combat",
                    pid=b.attacker,
                    choices=[{"type": "press"}, {"type": "end"}],
                    context={"target": list(b.target)},
                )
            self._battle_stage = "done"
            return self._battle_decision()
        return None

    def submit(self, choice: dict) -> None:
        dp = self._pending
        if dp is None:
            raise ValueError("no pending decision")
        if _canon(choice) not in {_canon(c) for c in dp.choices}:
            raise ValueError(f"illegal choice: {choice}")
        self.choices_log.append(choice)
        self._pending = None
        s = self.state
        if dp.kind == "whisper_discard":
            discard_whisper(s, dp.pid, choice["card"])
            self.whisper_stats["discarded"] += 1
            if not hand_over_limit(s, dp.pid):
                self._whisper_discard_queue.pop(0)
        elif dp.kind == "objective_draw":
            step = dp.context.get("step")
            if step == "keep":
                fu = self._objective_followup
                assert fu is not None
                drawn = fu["drawn"]
                if choice["type"] == "obj_keep_none":
                    apply_secret_keep(s, dp.pid, None, drawn, self.rng)
                    self._finish_objective_cap_step()
                else:
                    kept = choice["card"]
                    nxt = apply_secret_keep(s, dp.pid, kept, drawn, self.rng)
                    if nxt:
                        self._objective_followup = nxt
                    else:
                        self._finish_objective_cap_step()
            elif step == "discard":
                apply_secret_discard_at_cap(
                    s, dp.pid, dp.context["kept"], choice["card"],
                )
                self._finish_objective_cap_step()
            elif dp.context.get("source") == "winds":
                self._objective_draw_queue.pop(0)
                if choice["type"] == "obj_draw_public":
                    draw_public_to_row(s, self.rng)
                else:
                    cap = deal_secret_draw(s, dp.pid, self.rng)
                    if cap:
                        self._objective_cap_queue.insert(0, cap)
                        self._ensure_objective_cap_followup()
        elif dp.kind == "strategy_draft":
            apply_draft_pick(s, dp.pid, choice["card"])
            self._draft_queue.pop(0)
            if not self._draft_queue:
                finish_undrafted_bounty(s)
                self._begin_council_phase()
        elif dp.kind == "scry_ack":
            self._scry_queue.pop(0)
            if not self._scry_queue:
                self._reveal_council_agenda()
        elif dp.kind == "council_propose":
            if choice["type"] == "letters_of_credit":
                apply_letters_of_credit(s, dp.pid)
                return
            self._council_proposal_queue.pop(0)
            if choice["type"] == "council_propose":
                auto_apply_council_whispers(
                    s,
                    "proposal",
                    motion_id=choice["motion"],
                )
                self._council_motions.append({
                    "motion": choice["motion"],
                    "proposer": dp.pid,
                })
                self.council_stats["motions_proposed"] += 1
            if not self._council_proposal_queue:
                self._start_council_voting()
        elif dp.kind == "council_vote":
            if choice["type"] == "letters_of_credit":
                apply_letters_of_credit(s, dp.pid)
                return
            lobby = int(choice.get("lobby", 0))
            motion = self._council_motions[self._council_vote_motion_idx]["motion"]
            check_vote_promises(
                self.promises_log,
                dp.pid,
                motion,
                bool(choice.get("support")),
                self.negotiation_stats,
            )
            if lobby:
                s.player(dp.pid).influence -= lobby
                self.council_stats["influence_spent"] += lobby
                apply_spellweave_doctrine(s, dp.pid, lobby)
            self._council_ballots.append({
                "pid": dp.pid,
                "support": bool(choice.get("support")),
                "lobby": lobby,
                "sanctify": bool(choice.get("sanctify", False)),
            })
            if choice.get("sanctify"):
                mark_round_used(s, dp.pid, "sanctify")
            if choice.get("support"):
                self.council_stats["votes_yes"] += 1
            else:
                self.council_stats["votes_no"] += 1
            self._council_vote_queue.pop(0)
            if not self._council_vote_queue:
                motion = self._council_motions[self._council_vote_motion_idx]
                auto_apply_council_whispers(
                    s,
                    "pre_tally",
                    motion_id=motion["motion"],
                    extra_votes=self._council_extra_votes,
                )
                passed = tally_votes(
                    s,
                    motion["motion"],
                    self._council_ballots,
                    extra_yes=self._council_extra_votes.get("for", 0),
                    extra_no=self._council_extra_votes.get("against", 0),
                    proposer=motion["proposer"],
                )
                if passed:
                    veto = [False]
                    auto_apply_council_whispers(
                        s,
                        "post_pass",
                        motion_id=motion["motion"],
                        veto_flag=veto,
                    )
                    if not veto[0]:
                        apply_motion(s, motion["motion"], motion["proposer"], self.rng)
                        for ballot in self._council_ballots:
                            if ballot.get("support") and int(ballot.get("lobby", 0)):
                                record_public_progress(
                                    s,
                                    ballot["pid"],
                                    "council_power",
                                    int(ballot.get("lobby", 0)),
                                )
                            card = AGENDA_CARDS.get(motion["motion"])
                            if ballot.get("support") and card and card.kind == "law":
                                record_public_progress(s, ballot["pid"], "lawgiver")
                            if (
                                ballot.get("support")
                                and is_lord(s, ballot["pid"], "auriel")
                            ):
                                bump_renown(
                                    s,
                                    ballot["pid"],
                                    2 if ballot.get("sanctify") else 1,
                                    self.rng,
                                )
                        self.council_stats["motions_passed"] += 1
                    else:
                        self.council_stats["motions_failed"] += 1
                else:
                    self.council_stats["motions_failed"] += 1
                    if (
                        s.council_crisis
                        and motion["proposer"] == s.speaker
                    ):
                        s.player(s.speaker).renown = max(
                            0, s.player(s.speaker).renown - 1,
                        )
                for ballot in self._council_ballots:
                    apply_council_patronage(s, ballot["pid"], int(ballot.get("lobby", 0)))
                self._council_extra_votes = {"for": 0, "against": 0}
                self._advance_council_vote_motion()
        elif dp.kind == "negotiation":
            if choice["type"] == "letters_of_credit":
                apply_letters_of_credit(s, dp.pid)
                return
            self._submit_negotiation(dp, choice)
        elif dp.kind == "action":
            self._actions_taken[dp.pid] += 1
            t = choice["type"]
            if t != "pass":
                self._meaningful_actions_taken[dp.pid] += 1
            if t == "pass":
                p = s.player(dp.pid)
                remaining = p.ap
                p.passed = True
                p.banked = min(2, p.ap)  # Actions.md banking
                self.pass_log.append({
                    "round": s.round,
                    "pid": dp.pid,
                    "order": len(self._pass_order) + 1,
                    "remaining_ap": remaining,
                    "banked_ap": p.banked,
                    "stranded_ap": max(0, remaining - p.banked),
                    "actions_before_pass": sum(self._meaningful_actions_taken.values()),
                })
                self._pass_order.append(dp.pid)
                self._remove_from_initiative(dp.pid)
            elif t == "strategy_primary":
                card = choice["card"]
                pay_primary_ap(s, dp.pid, card)
                if card == "resource_surge":
                    apply_resource_surge_primary(s, dp.pid)
                    self._after_resource_or_boom_primary(dp.pid, card)
                elif card == "economic_boom":
                    apply_economic_boom_primary(s, dp.pid)
                    self._after_resource_or_boom_primary(dp.pid, card)
                elif card == "arcane_ascendancy":
                    apply_arcane_ascendancy_primary(s, dp.pid)
                    if enumerate_research(s, dp.pid, free=True, ap_waived=True):
                        self._research_followup = {"pid": dp.pid, "free": True}
                    else:
                        self._start_secondary_window(dp.pid, card)
                elif card == "military_maneuvers":
                    self._after_military_primary_paid(dp.pid, card)
                elif card == "diplomatic_decree":
                    apply_diplomatic_decree_primary(s, dp.pid)
                    run_emergency_council(s, dp.pid, self.rng)
                    self._start_secondary_window(dp.pid, card)
                elif card == "expansion_strategy":
                    hexes = enumerate_expansion_primary_choices(s, dp.pid)
                    if hexes:
                        self._followup = {
                            "kind": "expansion_primary",
                            "pid": dp.pid,
                            "card": card,
                        }
                    else:
                        self._start_secondary_window(dp.pid, card)
                elif card == "tactical_reinforcements":
                    recs = enumerate_tactical_primary_recruits(s, dp.pid)
                    if recs:
                        self._followup = {
                            "kind": "tactical_primary",
                            "pid": dp.pid,
                            "card": card,
                        }
                    else:
                        self._start_secondary_window(dp.pid, card)
                elif card == "imperial_mandate":
                    apply_imperial_mandate_primary(s, dp.pid, self.rng)
                    self._start_secondary_window(dp.pid, card)
                else:
                    self._finish_action_turn(dp.pid)
            elif t == "move":
                auto_apply_when_whispers(
                    s,
                    "before_move",
                    uid=choice.get("uid"),
                    skip=dp.pid,
                    rng=self.rng,
                )
                apply_move(s, dp.pid, choice)
                if not self._after_unit_entry(dp.pid, tuple(choice["dest"])):
                    self._finish_action_turn(dp.pid)
            elif t == "recruit":
                if len(choice["units"]) > 2:
                    self.building_stats["forge_recruits"] += 1
                apply_recruit(s, dp.pid, choice)
                city = choice.get("city")
                auto_apply_when_whispers(
                    s, "recruit_done", city=city, recruiter=dp.pid, rng=self.rng,
                )
                self._finish_action_turn(dp.pid)
            elif t == "build":
                apply_build(s, dp.pid, choice, rng=self.rng)
                self.build_counts[dp.pid] += 1
                self._finish_action_turn(dp.pid)
            elif t == "trade":
                target = int(choice["target"])
                err = validate_offer(
                    s, dp.pid, target,
                    choice.get("gives", {}), choice.get("gets", {}),
                    choice.get("promises"),
                )
                if err:
                    raise ValueError(err)
                from .lords.legendaries import controls_legendary
                ge_extra = (
                    self._trade_used.get(dp.pid, False)
                    and controls_legendary(s, dp.pid, BuildingType.GRAND_EXCHANGE)
                    and round_unused(s, dp.pid, "ge_extra_trade")
                )
                cassian_free = (
                    is_lord(s, dp.pid, "cassian")
                    and round_unused(s, dp.pid, "ledger_trade")
                )
                zero_ap_trade = (
                    self._has_active_market(dp.pid) or cassian_free or ge_extra
                )
                if zero_ap_trade:
                    if ge_extra:
                        mark_round_used(s, dp.pid, "ge_extra_trade")
                    elif self._has_active_market(dp.pid):
                        self.building_stats["market_trades"] += 1  # 0 AP (AL-27)
                        apply_guild_contracts_trade_influence(
                            s, dp.pid, zero_ap_market=True,
                        )
                    elif cassian_free:
                        mark_round_used(s, dp.pid, "ledger_trade")
                    self._grant_bazaar_trade_gold(s)
                else:
                    s.player(dp.pid).ap -= 1
                if self._trade_used.get(dp.pid, False):
                    pass  # second (GE) trade
                else:
                    self._trade_used[dp.pid] = True
                s.trades_this_round += 1
                apply_diplomatic_tariffs(s, dp.pid)
                self._trade_initiator = dp.pid
                self._trade_consumes_turn = not cassian_free and not ge_extra
                self._negotiation_session = start_session(
                    window="trade",
                    proposer=dp.pid,
                    target=target,
                    gives=choice.get("gives", {}),
                    gets=choice.get("gets", {}),
                    promises=choice.get("promises"),
                    motion=None,
                    state=s,
                    deal_kind=str(choice.get("deal_kind", "resource_trade")),
                )
                self.negotiation_stats["offers_proposed"] += 1
            elif t == "attack":
                auto_apply_when_whispers(
                    s,
                    "enemy_attack",
                    attacker=dp.pid,
                    target=tuple(choice["target"]),
                    rng=self.rng,
                )
                self._battle = combat.start_battle(s, dp.pid, choice, rng=self.rng)
                check_attack_promises(
                    self.promises_log, dp.pid, self._battle.defender,
                    s.round, self.negotiation_stats,
                )
                self._start_lord_combat_round()
                self._finish_action_turn(dp.pid)
            elif t == "desert_tempest":
                apply_desert_tempest(s, dp.pid, tuple(choice["coord"]))
                self._finish_action_turn(dp.pid)
            elif t == "exaltation":
                apply_exaltation(s, dp.pid, self.rng)
                self._finish_action_turn(dp.pid)
            elif t == "shadow_network":
                apply_shadow_network(s, dp.pid, choice)
                self._finish_action_turn(dp.pid)
            elif t == "void_anchor":
                apply_void_anchor(s, dp.pid, tuple(choice["hex"]))
                self._finish_action_turn(dp.pid)
            elif t == "nexus_teleport":
                from .lords.legendaries import apply_nexus_teleport
                apply_nexus_teleport(s, dp.pid, choice)
                self._finish_action_turn(dp.pid)
            elif t == "warcamp_cavalry_move":
                from .lords.legendaries import apply_warcamp_cavalry_move
                apply_warcamp_cavalry_move(s, dp.pid, choice)
                self._finish_action_turn(dp.pid)
            elif t == "cleanse":
                apply_cleanse(s, dp.pid, tuple(choice["hex"]))
                self._finish_action_turn(dp.pid)
            elif t == "artifact_purge_draw":
                pending = apply_purge_draw(s, dp.pid)
                self._after_gain_artifact(dp.pid, pending)
                if self._artifact_followup is None:
                    self._finish_action_turn(dp.pid)
            elif t == "artifact_claim":
                pending = apply_site_claim(s, dp.pid, tuple(choice["hex"]))
                self._after_gain_artifact(dp.pid, pending)
                if self._artifact_followup is None:
                    self._finish_action_turn(dp.pid)
            elif t == "artifact_attach":
                attach_building_relic(s, dp.pid, choice["card"], tuple(choice["hex"]))
                if self._artifact_followup and self._artifact_followup.get("kind") == "attach":
                    self._artifact_followup = None
                self._finish_action_turn(dp.pid)
            elif t == "artifact_discard_lord":
                discard_lord_equipment(s, dp.pid, choice["card"])
                if len(s.player(dp.pid).lord_equipment) <= 2:
                    self._artifact_followup = None
                self._finish_action_turn(dp.pid)
            elif t == "whisper_play":
                apply_action_whisper(s, dp.pid, choice)
                self._track_whisper_play(dp.pid, choice["card"])
                self._finish_action_turn(dp.pid)
            elif t == "research":
                apply_research(
                    s, dp.pid, choice["discovery"],
                    free=choice.get("free", False),
                    ap_waived=choice.get("free", False),
                )
                if choice.get("free"):
                    from .lords.legendaries import controls_legendary
                    if controls_legendary(s, dp.pid, BuildingType.ARCANE_SANCTUM):
                        mark_round_used(s, dp.pid, "sanctum_free_research")
                if (
                    is_lord(s, dp.pid, "seraphel")
                    and round_unused(s, dp.pid, "polymath_second")
                    and enumerate_research(s, dp.pid)
                ):
                    self._research_followup = {
                        "pid": dp.pid,
                        "free": False,
                        "seraphel_second": True,
                    }
                else:
                    self._finish_action_turn(dp.pid)
        elif dp.kind == "research":
            if choice["type"] == "research_skip":
                self._research_followup = None
                self._finish_action_turn(dp.pid)
                check_invariants(s)
                return
            apply_research(
                s, dp.pid, choice["discovery"],
                free=dp.context.get("free", False),
                ap_waived=dp.context.get("ap_waived", False),
            )
            if dp.context.get("seraphel_second"):
                mark_round_used(s, dp.pid, "polymath_second")
                self._research_followup = None
                self._finish_action_turn(dp.pid)
                check_invariants(s)
                return
            sec_card = dp.context.get("card")
            if sec_card == "arcane_ascendancy":
                self._research_followup = None
                self._followup = None
                self._finish_action_turn(dp.pid)
            elif self._research_followup is not None:
                self._research_followup = None
                if (
                    dp.context.get("free")
                    and "arcane_ascendancy" in s.player(dp.pid).primary_used
                ):
                    self._start_secondary_window(dp.pid, "arcane_ascendancy")
                else:
                    self._finish_action_turn(dp.pid)
            elif sec_card:
                self._followup = None
                self._finish_action_turn(dp.pid)
            else:
                self._research_followup = None
                if (
                    dp.context.get("free")
                    and "arcane_ascendancy" in s.player(dp.pid).primary_used
                ):
                    self._start_secondary_window(dp.pid, "arcane_ascendancy")
                else:
                    self._finish_action_turn(dp.pid)
        elif dp.kind == "artifact":
            step = dp.context.get("step")
            if step == "discard_lord":
                discard_lord_equipment(s, dp.pid, choice["card"])
                if len(s.player(dp.pid).lord_equipment) <= 2:
                    self._artifact_followup = None
                    self._finish_action_turn(dp.pid)
            elif step == "attach":
                attach_building_relic(s, dp.pid, choice["card"], tuple(choice["hex"]))
                self._artifact_followup = None
                self._finish_action_turn(dp.pid)
        elif dp.kind == "exploration":
            ep = self._exploration_pending
            assert ep is not None
            pending = apply_exploration_choice(
                s, dp.pid, ep["coord"], ep["card"],
                choice["choice"], self.rng,
            )
            if pending:
                self._after_gain_artifact(dp.pid, pending)
            self._finish_exploration()
        elif dp.kind == "strategy_primary":
            t = choice["type"]
            pid = dp.pid
            card = dp.context.get("card", choice.get("card"))
            if t == "move":
                apply_move(s, pid, choice)
                dest = tuple(choice["dest"])
                if self._after_unit_entry(pid, dest):
                    assert self._exploration_pending is not None
                    self._exploration_pending["defer"] = ("mm", pid, card)
                else:
                    attacks = enumerate_military_maneuver_attacks(s, pid)
                    if attacks:
                        self._followup = {"kind": "mm_attack", "pid": pid, "card": card}
                    else:
                        self._start_secondary_window(pid, card)
            elif t == "attack":
                self._battle = combat.start_battle(s, dp.pid, choice, rng=self.rng)
                check_attack_promises(
                    self.promises_log, dp.pid, self._battle.defender,
                    s.round, self.negotiation_stats,
                )
                self._start_lord_combat_round()
                self._deferred_followup = {
                    "kind": "strategy_secondary",
                    "owner": pid,
                    "card": card,
                    "queue": secondary_eligible_players(s, pid, card),
                }
            elif t in ("mm_skip_move", "mm_skip_attack"):
                if t == "mm_skip_move":
                    attacks = enumerate_military_maneuver_attacks(s, pid)
                    if attacks:
                        self._followup = {"kind": "mm_attack", "pid": pid, "card": card}
                    else:
                        self._start_secondary_window(pid, card)
                else:
                    self._start_secondary_window(pid, card)
            elif t == "expansion_claim":
                apply_expansion_strategy_primary(s, pid, tuple(choice["hex"]))
                self._followup = None
                self._start_secondary_window(pid, card)
            elif t == "expansion_skip":
                self._followup = None
                self._start_secondary_window(pid, card)
            elif t == "tactical_recruit":
                apply_recruit(
                    s, pid, choice, free=True, ignore_city_limit=True,
                )
                self._followup = None
                self._start_secondary_window(pid, card)
            elif t == "tactical_skip":
                self._followup = None
                self._start_secondary_window(pid, card)
        elif dp.kind == "strategy_secondary":
            followup = apply_strategy_secondary(
                s, dp.pid, choice["card"], use=choice["use"], rng=self.rng,
            )
            if followup:
                self._followup = followup
            elif self._followup and self._followup.get("kind") == "strategy_secondary":
                if self._followup["queue"]:
                    self._followup["queue"].pop(0)
                if not self._followup["queue"]:
                    owner = self._followup["owner"]
                    self._followup = None
                    self._finish_action_turn(owner)
        elif dp.kind == "defender_retreat":
            if choice["type"] == "retreat":
                combat.apply_defender_retreat(s, self._battle, choice)
                if not self._after_unit_entry(dp.pid, tuple(choice["dest"])):
                    self._battle_stage = "done"
            else:
                self._battle_stage = "press"
        elif dp.kind == "sandstride_retreat":
            apply_sandstride_retreat(s, self._battle, choice)
            if self._battle.def_retreated or self._battle.att_retreated:
                self._battle_stage = "done"
            else:
                self._battle_lord_substage = "lock_line"
        elif dp.kind == "lock_the_line":
            apply_lock_the_line(s, self._battle, choice)
            self._battle_lord_substage = "entangling_roots"
        elif dp.kind == "entangling_roots":
            apply_entangling_roots(s, self._battle, choice)
            self._battle_lord_substage = "execute"
        elif dp.kind == "hit_and_run":
            if choice["type"] != "hit_and_run_skip":
                apply_hit_and_run(s, self._battle, choice)
            self._battle_stage = "done"
        elif dp.kind == "press":
            if choice["type"] == "press":
                s.player(self._battle.attacker).ap -= combat.PRESS_AP
                self._start_lord_combat_round()
            else:
                self._battle_stage = "done"
        check_invariants(s)
