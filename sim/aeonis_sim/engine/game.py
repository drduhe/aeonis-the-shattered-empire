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
    apply_motion,
    enumerate_proposal_choices,
    enumerate_vote_choices,
    reveal_agenda,
    tally_votes,
)
from .events import draw_event, resolve_event
from .invariants import check_invariants
from .negotiation import (
    NegotiationSession,
    apply_session_choice,
    check_vote_promises,
    enumerate_council_negotiation,
    enumerate_trade_negotiation,
    enumerate_trade_starts,
    start_session,
    validate_offer,
)
from .move import apply_move, enumerate_moves
from .observations import DecisionPoint
from .production import run_production
from .recruit import apply_recruit, enumerate_recruits
from .setup import build_initial_state
from .strategy import (
    apply_draft_pick,
    apply_economic_boom_primary,
    apply_resource_surge_primary,
    apply_strategy_secondary,
    begin_strategy_selection,
    build_draft_queue,
    enumerate_draft_choices,
    enumerate_military_maneuver_attacks,
    enumerate_military_maneuver_moves,
    enumerate_secondary_choices,
    enumerate_strategy_primaries,
    finish_undrafted_bounty,
    initiative_order,
    pay_primary_ap,
    secondary_eligible_players,
)
from .types import (BASE_AP, BuildingType, DEFAULT_ROUND_CAP, Terrain,
                    UNIT_STATS, UnitType)

MAX_ACTIONS_PER_PLAYER_ROUND = 100


def _canon(choice: dict) -> str:
    return json.dumps(choice, sort_keys=True)


class Game:
    def __init__(self, config: dict, seed: int):
        self.config = dict(config)
        self.seed = seed
        self.rng = random.Random(seed)
        self.state = build_initial_state(config, self.rng)
        self.over = False
        self.verdict: Optional[str] = None
        self.choices_log: list = []
        self.degenerate_flags: list = []
        self.round_cap_finish = False
        self._actions_taken: dict = {}
        self._initiative_queue: list[int] = []
        self._battle: Optional[combat.Battle] = None
        self._battle_stage: Optional[str] = None  # "defender_retreat" | "press"
        self._round_hashes: list = []
        self._pending: Optional[DecisionPoint] = None
        self.combat_stats = {
            "battles": 0,
            "attacker_wins": 0,
            "defender_wins": 0,
            "stratified": combat.empty_stratified_stats(),
        }
        self.ap_spread_log: list[int] = []
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
        }
        self.promises_log: list[dict] = []
        self.building_stats = {
            "bank_conversions": 0,
            "forge_recruits": 0,
            "market_trades": 0,
        }
        self._negotiation_session: Optional[NegotiationSession] = None
        self._council_negotiation_queue: list[int] = []
        self._trade_used: dict[int, bool] = {}
        self._trade_initiator: Optional[int] = None
        self._round_start()

    # ---- phases ----
    def _ap_bonus(self, pid: int) -> int:
        s = self.state
        cities = sum(1 for t in s.controlled(pid) if t.terrain == Terrain.CITY)
        guild = sum(1 for t in s.controlled(pid)
                    if t.has(BuildingType.GUILD_HALL))
        bonus = min(2, cities) + guild + (1 if s.player(pid).renown >= 5 else 0)
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
        # Tiles.md control method 1: sole-occupier hexes flip at Round Start
        for t in s.tiles.values():
            owners = {u.owner for u in t.units}
            if len(owners) == 1:
                t.controller = owners.pop()
        # Combat.md §2.1.3: Lords heal to full HP at Round Start
        for t in s.tiles.values():
            for u in t.units:
                if u.type == UnitType.LORD:
                    u.hp = UNIT_STATS[UnitType.LORD].hp
        for p in s.players:
            pending = p.pending_ap
            p.pending_ap = 0
            p.ap = BASE_AP + p.banked + self._ap_bonus(p.pid) + pending
            p.banked = 0
        self._apply_rally()
        self.ap_spread_log.append(
            max(p.ap for p in s.players) - min(p.ap for p in s.players)
        )
        self._actions_taken = {p.pid: 0 for p in s.players}
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
        self._run_event_phase()
        if s.round >= 2 and s.shared_public_deck:
            s.shared_public_revealed.append(s.shared_public_deck.pop())
        begin_strategy_selection(s)
        self._draft_queue = build_draft_queue(s, s.speaker)

    def _run_event_phase(self) -> None:
        card = draw_event(self.state, self.rng)
        if not card:
            return
        resolve_event(self.state, card)
        self.event_stats["resolved"] += 1
        by = self.event_stats["by_card"]
        by[card] = by.get(card, 0) + 1

    def _begin_council_phase(self) -> None:
        reveal_agenda(self.state, self.rng)
        self._council_proposal_queue = initiative_order(self.state)
        self._council_motions = []
        self._council_vote_motion_idx = 0
        self._council_vote_queue = []
        self._council_ballots = []

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
                    "phase": session.phase,
                    "countered": session.countered,
                },
            )
        if self._council_negotiation_queue:
            pid = self._council_negotiation_queue[0]
            motion = self._council_motion_id()
            return DecisionPoint(
                kind="negotiation",
                phase="council",
                pid=pid,
                choices=enumerate_council_negotiation(
                    self.state, pid, motion=motion, session=None,
                ),
                context={"window": "council", "motion": motion},
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
                choices=enumerate_proposal_choices(self.state, pid),
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
            return DecisionPoint(
                kind="council_vote",
                phase="council",
                pid=pid,
                choices=enumerate_vote_choices(
                    self.state, pid, motion["motion"],
                ),
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
        prod_stats = run_production(self.state)
        self.building_stats["bank_conversions"] += len(
            prod_stats.get("bank_conversions", {})
        )
        run_cleanup(self.state)
        check_invariants(self.state)
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
        if not self._trade_used.get(pid, False):
            free = self._has_active_market(pid)
            if free or s.player(pid).ap >= 1:
                out.extend(self._enumerate_trade_starts(pid))
        return out

    def _has_active_market(self, pid: int) -> bool:
        return any(t.active(BuildingType.MARKET)
                   for t in self.state.controlled(pid))

    def _enumerate_trade_starts(self, pid: int) -> list[dict]:
        return enumerate_trade_starts(self.state, pid)

    def _close_negotiation_session(self, window: str) -> None:
        if window == "trade" and self._trade_initiator is not None:
            self._finish_action_turn(self._trade_initiator)
            self._trade_initiator = None

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
                )
                self.negotiation_stats["offers_proposed"] += 1
                if (
                    self._council_negotiation_queue
                    and self._council_negotiation_queue[0] == dp.pid
                ):
                    self._council_negotiation_queue.pop(0)
            return
        window = self._negotiation_session.window
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
        if added:
            self.negotiation_stats["promises_made"] += added
        if session is None:
            self._close_negotiation_session(window)

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

    def _battle_decision(self) -> Optional[DecisionPoint]:
        b = self._battle
        if b.winner is not None or self._battle_stage == "done":
            combat.finish_battle(self.state, b)
            combat.record_battle_outcome(self.combat_stats, b)
            check_invariants(self.state)
            self._battle = None
            self._battle_stage = None
            if self._deferred_followup is not None:
                self._followup = self._deferred_followup
                self._deferred_followup = None
            return None
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
        if dp.kind == "strategy_draft":
            apply_draft_pick(s, dp.pid, choice["card"])
            self._draft_queue.pop(0)
            if not self._draft_queue:
                finish_undrafted_bounty(s)
                self._begin_council_phase()
        elif dp.kind == "council_propose":
            self._council_proposal_queue.pop(0)
            if choice["type"] == "council_propose":
                self._council_motions.append({
                    "motion": choice["motion"],
                    "proposer": dp.pid,
                })
                self.council_stats["motions_proposed"] += 1
            if not self._council_proposal_queue:
                self._start_council_voting()
        elif dp.kind == "council_vote":
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
            self._council_ballots.append({
                "pid": dp.pid,
                "support": bool(choice.get("support")),
                "lobby": lobby,
            })
            if choice.get("support"):
                self.council_stats["votes_yes"] += 1
            else:
                self.council_stats["votes_no"] += 1
            self._council_vote_queue.pop(0)
            if not self._council_vote_queue:
                motion = self._council_motions[self._council_vote_motion_idx]
                passed = tally_votes(s, motion["motion"], self._council_ballots)
                if passed:
                    apply_motion(s, motion["motion"], motion["proposer"])
                    self.council_stats["motions_passed"] += 1
                else:
                    self.council_stats["motions_failed"] += 1
                self._advance_council_vote_motion()
        elif dp.kind == "negotiation":
            self._submit_negotiation(dp, choice)
        elif dp.kind == "action":
            self._actions_taken[dp.pid] += 1
            t = choice["type"]
            if t == "pass":
                p = s.player(dp.pid)
                p.passed = True
                p.banked = min(2, p.ap)  # Actions.md banking
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
                elif card == "military_maneuvers":
                    self._after_military_primary_paid(dp.pid, card)
                else:
                    self._finish_action_turn(dp.pid)
            elif t == "move":
                apply_move(s, dp.pid, choice)
                self._finish_action_turn(dp.pid)
            elif t == "recruit":
                if len(choice["units"]) > 2:
                    self.building_stats["forge_recruits"] += 1
                apply_recruit(s, dp.pid, choice)
                self._finish_action_turn(dp.pid)
            elif t == "build":
                apply_build(s, dp.pid, choice)
                self._finish_action_turn(dp.pid)
            elif t == "trade":
                target = int(choice["target"])
                err = validate_offer(
                    s, dp.pid, target,
                    choice.get("gives", {}), choice.get("gets", {}),
                )
                if err:
                    raise ValueError(err)
                if self._has_active_market(dp.pid):
                    self.building_stats["market_trades"] += 1  # 0 AP (AL-27)
                else:
                    s.player(dp.pid).ap -= 1
                self._trade_used[dp.pid] = True
                self._trade_initiator = dp.pid
                self._negotiation_session = start_session(
                    window="trade",
                    proposer=dp.pid,
                    target=target,
                    gives=choice.get("gives", {}),
                    gets=choice.get("gets", {}),
                    promises=choice.get("promises"),
                    motion=None,
                )
                self.negotiation_stats["offers_proposed"] += 1
            elif t == "attack":
                self._battle = combat.start_battle(s, dp.pid, choice)
                combat.resolve_round(s, self._battle, self.rng)
                self._battle_stage = "defender_retreat"
                self._finish_action_turn(dp.pid)
        elif dp.kind == "strategy_primary":
            t = choice["type"]
            pid = dp.pid
            card = dp.context.get("card", choice.get("card"))
            if t == "move":
                apply_move(s, pid, choice)
                attacks = enumerate_military_maneuver_attacks(s, pid)
                if attacks:
                    self._followup = {"kind": "mm_attack", "pid": pid, "card": card}
                else:
                    self._start_secondary_window(pid, card)
            elif t == "attack":
                self._battle = combat.start_battle(s, dp.pid, choice)
                combat.resolve_round(s, self._battle, self.rng)
                self._battle_stage = "defender_retreat"
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
        elif dp.kind == "strategy_secondary":
            apply_strategy_secondary(
                s, dp.pid, choice["card"], use=choice["use"],
            )
            if self._followup and self._followup.get("queue"):
                self._followup["queue"].pop(0)
            if self._followup and not self._followup.get("queue"):
                owner = self._followup["owner"]
                self._followup = None
                self._finish_action_turn(owner)
        elif dp.kind == "defender_retreat":
            if choice["type"] == "retreat":
                combat.apply_defender_retreat(s, self._battle, choice)
                self._battle_stage = "done"
            else:
                self._battle_stage = "press"
        elif dp.kind == "press":
            if choice["type"] == "press":
                s.player(self._battle.attacker).ap -= combat.PRESS_AP
                combat.resolve_round(s, self._battle, self.rng)
                self._battle_stage = "defender_retreat"
            else:
                self._battle_stage = "done"
        check_invariants(s)
