"""Phase machine (Round_Structure.md).

Milestone 1: Event, Strategy Selection, and High Council phases are no-op
stubs; Action Phase turn order is seating order (Strategy-card initiative
arrives in Milestone 2 / plan B).
"""
from __future__ import annotations

import json
import random
from typing import Optional

from . import combat
from .build import apply_build, enumerate_builds
from .cleanup import run_cleanup
from .invariants import check_invariants
from .move import apply_move, enumerate_moves
from .observations import DecisionPoint
from .production import run_production
from .recruit import apply_recruit, enumerate_recruits
from .setup import build_initial_state
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
        self._turn_idx = 0
        self._actions_taken: dict = {}
        self._battle: Optional[combat.Battle] = None
        self._battle_stage: Optional[str] = None  # "defender_retreat" | "press"
        self._round_hashes: list = []
        self._pending: Optional[DecisionPoint] = None
        self._round_start()

    # ---- phases ----
    def _round_start(self) -> None:
        s = self.state
        if s.round > DEFAULT_ROUND_CAP:
            self._end("timeout")
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
            cities = sum(1 for t in s.controlled(p.pid)
                         if t.terrain == Terrain.CITY)
            guild = sum(1 for t in s.controlled(p.pid)
                        if t.has(BuildingType.GUILD_HALL))
            p.ap = (BASE_AP + p.banked + min(2, cities) + guild
                    + (1 if p.renown >= 5 else 0))
            p.banked = 0
        self._turn_idx = 0
        self._actions_taken = {p.pid: 0 for p in s.players}
        # Plan 3 MVP: reveal shared public objective from Round 2 onward.
        if s.round >= 2 and s.shared_public_deck:
            s.shared_public_revealed.append(s.shared_public_deck.pop())
        # Event / Strategy / Council: no-ops in Milestone 1.

    def _end(self, verdict: str) -> None:
        self.over = True
        self.verdict = verdict
        self._pending = None

    def _advance_phases(self) -> None:
        """All players have passed: Production, Cleanup, next round or end."""
        run_production(self.state)
        run_cleanup(self.state)
        check_invariants(self.state)
        if self.state.final_round:
            self._end("completed")
            return
        self._round_start()

    # ---- decision loop ----
    def _active_pid(self) -> Optional[int]:
        s = self.state
        n = len(s.players)
        for i in range(n):
            pid = (self._turn_idx + i) % n
            if not s.players[pid].passed:
                self._turn_idx = pid
                return pid
        return None

    def _action_choices(self, pid: int) -> list:
        s = self.state
        if self._actions_taken[pid] >= MAX_ACTIONS_PER_PLAYER_ROUND:
            if "action_cap" not in self.degenerate_flags:
                self.degenerate_flags.append("action_cap")
            return [{"type": "pass"}]
        out = [{"type": "pass"}]
        out.extend(enumerate_moves(s, pid))
        out.extend(enumerate_recruits(s, pid))
        out.extend(enumerate_builds(s, pid))
        out.extend(combat.enumerate_attacks(s, pid))
        return out

    def next_decision(self) -> Optional[DecisionPoint]:
        if self.over:
            return None
        if self._pending is not None:
            return self._pending
        if self._battle is not None:
            self._pending = self._battle_decision()
            if self._pending is not None:
                return self._pending
        pid = self._active_pid()
        if pid is None:
            self._advance_phases()
            return None if self.over else self.next_decision()
        self._pending = DecisionPoint(kind="action", pid=pid,
                                      choices=self._action_choices(pid))
        return self._pending

    def _battle_decision(self) -> Optional[DecisionPoint]:
        b = self._battle
        if b.winner is not None or self._battle_stage == "done":
            combat.finish_battle(self.state, b)
            check_invariants(self.state)
            self._battle = None
            self._battle_stage = None
            return None
        if self._battle_stage == "defender_retreat":
            retreats = combat.enumerate_defender_retreats(self.state, b)
            if retreats:
                return DecisionPoint(kind="defender_retreat", pid=b.defender,
                                     choices=retreats + [{"type": "hold"}],
                                     context={"target": list(b.target)})
            self._battle_stage = "press"
        if self._battle_stage == "press":
            if b.rounds < 2 and self.state.player(b.attacker).ap >= combat.PRESS_AP:
                return DecisionPoint(kind="press", pid=b.attacker,
                                     choices=[{"type": "press"}, {"type": "end"}],
                                     context={"target": list(b.target)})
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
        if dp.kind == "action":
            self._actions_taken[dp.pid] += 1
            t = choice["type"]
            if t == "pass":
                p = s.player(dp.pid)
                p.passed = True
                p.banked = min(2, p.ap)  # Actions.md banking
                self._turn_idx = (dp.pid + 1) % len(s.players)
            elif t == "move":
                apply_move(s, dp.pid, choice)
                self._turn_idx = (dp.pid + 1) % len(s.players)
            elif t == "recruit":
                apply_recruit(s, dp.pid, choice)
                self._turn_idx = (dp.pid + 1) % len(s.players)
            elif t == "build":
                apply_build(s, dp.pid, choice)
                self._turn_idx = (dp.pid + 1) % len(s.players)
            elif t == "attack":
                self._battle = combat.start_battle(s, dp.pid, choice)
                combat.resolve_round(s, self._battle, self.rng)
                self._battle_stage = "defender_retreat"
                self._turn_idx = (dp.pid + 1) % len(s.players)
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
