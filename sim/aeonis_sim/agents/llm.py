"""Engine-bounded qualitative playtest agent (M5)."""
from __future__ import annotations

import json
import time
from collections import Counter

from ..engine.strategy import STRATEGY_RULE_SUMMARIES
from .providers import CompletionProvider, ProviderError


DECISION_SCHEMA = {
    "title": "AeonisDecision",
    "type": "object",
    "properties": {
        "action_index": {"type": "integer"},
        "reason": {"type": "string"},
        "highlight": {"type": "string"},
        "frustration": {"type": "string"},
        "rules_question": {"type": "string"},
    },
    "required": ["action_index", "reason", "highlight", "frustration", "rules_question"],
    "additionalProperties": False,
}

NEGOTIATION_DECISION_SCHEMA = {
    "title": "AeonisNegotiationDecision",
    "type": "object",
    "properties": {
        "action_index": {"type": "integer"},
        "message": {"type": "string"},
        "intent": {"type": "string"},
        "reason": {"type": "string"},
        "highlight": {"type": "string"},
        "frustration": {"type": "string"},
        "rules_question": {"type": "string"},
    },
    "required": [
        "action_index", "message", "intent", "reason", "highlight",
        "frustration", "rules_question",
    ],
    "additionalProperties": False,
}

ROUND_REFLECTION_SCHEMA = {
    "title": "AeonisRoundReflection",
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "highlight": {"type": "string"},
        "frustration": {"type": "string"},
        "rules_question": {"type": "string"},
    },
    "required": ["summary", "highlight", "frustration", "rules_question"],
    "additionalProperties": False,
}

EXIT_INTERVIEW_SCHEMA = {
    "title": "AeonisExitInterview",
    "type": "object",
    "properties": {
        "pacing": {"type": "string"},
        "map_flow": {"type": "string"},
        "politics": {"type": "string"},
        "combat": {"type": "string"},
        "economy_pressure": {"type": "string"},
        "best_moment": {"type": "string"},
        "biggest_friction": {"type": "string"},
        "rules_questions": {"type": "array", "items": {"type": "string"}},
        "play_again": {"type": "boolean"},
        "hypotheses": {"type": "array", "items": {"type": "string"}, "maxItems": 5},
    },
    "required": [
        "pacing", "map_flow", "politics", "combat", "economy_pressure",
        "best_moment", "biggest_friction", "rules_questions", "play_again", "hypotheses",
    ],
    "additionalProperties": False,
}

PHASE_DIGESTS = {
    "strategy": (
        "Strategy Selection: lowest VP drafts first; ties use lowest Renown then Speaker order. "
        "At 3-4 players each player drafts two cards. Initiative is the lowest card number held. "
        "Source: rules_and_systems/Strategy.md and Round_Structure.md."
    ),
    "council": (
        "High Council: proposals, the revealed agenda, bounded negotiation, lobbying, voting, then enactment. "
        "Lobbying costs 2 Influence per vote; strict majority passes and ties fail. "
        "Source: rules_and_systems/High_Council.md and Diplomacy.md."
    ),
    "action": (
        "Action Phase: take one enumerated action on your turn or Pass. AP and all resource costs are enforced "
        "by the engine. Source: rules_and_systems/Actions.md."
    ),
    "combat": (
        "Combat: the engine enforces Battle Lines, Pre-Strike, strikes, retreat, victory, and the single Press "
        "the Attack option. Source: rules_and_systems/Combat.md."
    ),
    "cleanup": (
        "Cleanup & Checks: score eligible objectives, resolve Coronation Rites, enforce limits, and check the "
        "10 VP final-round trigger. Source: rules_and_systems/Round_Structure.md and Victory.md."
    ),
    "round_start": (
        "Round Start refreshes abilities/AP, draws Whispers, reveals scheduled public objectives, and precedes "
        "the Event Phase. Source: rules_and_systems/Round_Structure.md."
    ),
}


def _clean_string(value) -> str:
    return str(value or "").strip()[:600]


def _clean_optional(value) -> str:
    cleaned = _clean_string(value)
    if cleaned.lower().rstrip(".") in {"none", "no", "n/a", "not applicable"}:
        return ""
    return cleaned


def _validate_response(value, schema: dict) -> dict:
    """Validate the small JSON-schema subset used by M5 without a dependency."""
    if not isinstance(value, dict):
        raise ProviderError("provider response root must be an object")
    missing = [key for key in schema.get("required", []) if key not in value]
    if missing:
        raise ProviderError(f"provider response missing required fields: {', '.join(missing)}")
    properties = schema.get("properties", {})
    if schema.get("additionalProperties") is False:
        extra = sorted(set(value) - set(properties))
        if extra:
            raise ProviderError(f"provider response has unknown fields: {', '.join(extra)}")
    for key, spec in properties.items():
        if key not in value:
            continue
        item = value[key]
        expected = spec.get("type")
        valid = (
            (expected == "string" and isinstance(item, str))
            or (expected == "integer" and isinstance(item, int) and not isinstance(item, bool))
            or (expected == "boolean" and isinstance(item, bool))
            or (expected == "array" and isinstance(item, list))
        )
        if not valid:
            raise ProviderError(f"provider field {key!r} must be {expected}")
        if expected == "array":
            item_type = spec.get("items", {}).get("type")
            if item_type == "string" and not all(isinstance(entry, str) for entry in item):
                raise ProviderError(f"provider field {key!r} must contain strings")
            if "maxItems" in spec and len(item) > int(spec["maxItems"]):
                raise ProviderError(
                    f"provider field {key!r} exceeds {int(spec['maxItems'])} items"
                )
    return value


def _public_player(player: dict, *, own: bool) -> dict:
    visible = {
        key: player.get(key)
        for key in (
            "pid", "lord_id", "ap", "banked", "gold", "mana", "influence",
            "renown", "vp", "pop_pool", "passed", "battle_wins", "lord_captured",
            "rite_count", "held_cards", "discoveries", "lord_equipment", "utilities",
        )
        if key in player
    }
    visible["public_objectives_scored"] = list(player.get("shared_scored", []))
    visible["secret_objectives_scored"] = list(player.get("secrets_scored", []))
    visible["whisper_count"] = len(player.get("whisper_hand", []))
    if own:
        visible["secret_objectives"] = list(player.get("secret_objectives", []))
        visible["whisper_hand"] = list(player.get("whisper_hand", []))
    return visible


def compact_observation(observation: dict, decision_point) -> dict:
    """Redact opponent hidden cards and compress the state for a model prompt."""
    state = observation["state"]
    viewer = int(observation["viewer"])
    tiles = list(state.get("tiles", {}).values())
    controlled = Counter(tile.get("controller") for tile in tiles if tile.get("controller") is not None)
    units = Counter()
    buildings = Counter()
    for tile in tiles:
        for unit in tile.get("units", []):
            units[int(unit["owner"])] += 1
        if tile.get("controller") is not None:
            buildings[int(tile["controller"])] += len(tile.get("buildings", []))
    return {
        "viewer": viewer,
        "round": state.get("round"),
        "phase": decision_point.phase,
        "decision_kind": decision_point.kind,
        "decision_context": decision_point.context,
        "speaker": state.get("speaker"),
        "last_event": state.get("last_event_id"),
        "agenda_revealed": state.get("agenda_revealed"),
        "active_laws": list(state.get("active_laws", [])),
        "shared_public_objectives": list(state.get("shared_public_revealed", [])),
        "players": [
            {
                **_public_player(player, own=int(player["pid"]) == viewer),
                "controlled_hexes": controlled[int(player["pid"])],
                "unit_count": units[int(player["pid"])],
                "building_count": buildings[int(player["pid"])],
            }
            for player in state.get("players", [])
        ],
    }


def _prompt_choice(choice: dict) -> dict:
    shown = {"action": choice}
    card = choice.get("card")
    if card in STRATEGY_RULE_SUMMARIES:
        shown["rules_gloss"] = STRATEGY_RULE_SUMMARIES[card]
    return shown


class LLMPlaytestAgent:
    """Uses a model sparingly for qualitative decisions and a persona bot otherwise."""

    def __init__(
        self,
        *,
        provider: CompletionProvider,
        fallback,
        persona: str,
        seat: int,
        decision_kinds: list[str] | None = None,
        max_decision_calls: int = 8,
        max_round_reflections: int = 2,
        retries: int = 1,
        decision_round_min: int = 1,
        max_presented_choices: int = 80,
        full_control: bool = False,
    ):
        self.provider = provider
        self.fallback = fallback
        self.persona = persona
        self.seat = int(seat)
        self.decision_kinds = set(decision_kinds or [
            "strategy_draft", "council_propose", "council_vote", "negotiation", "action", "press",
        ])
        self.max_decision_calls = max(0, int(max_decision_calls))
        self.max_round_reflections = max(0, int(max_round_reflections))
        self.retries = max(0, int(retries))
        self.decision_round_min = max(1, int(decision_round_min))
        self.max_presented_choices = max(2, int(max_presented_choices))
        self.full_control = bool(full_control)
        self.annotations: list[dict] = []
        self.reflections: list[dict] = []
        self.interview: dict | None = None
        self.errors: list[dict] = []
        self._pending_negotiation_utterance: dict | None = None
        self._portal_guard_round = 0
        self._used_zero_cost_portal_routes: set[tuple] = set()
        self.stats = {
            "provider": provider.name,
            "model_decision_attempts": 0,
            "model_decisions": 0,
            "persona_delegations": 0,
            "forced_choices": 0,
            "provider_calls": 0,
            "retries": 0,
            "fallbacks": 0,
            "invalid_responses": 0,
            "provider_seconds": 0.0,
            "shortlisted_decisions": 0,
            "loop_guard_activations": 0,
            "loop_choices_suppressed": 0,
            "reflection_failures": 0,
            "interview_failures": 0,
        }

    def _record_error(self, stage: str, error: Exception | str) -> None:
        if len(self.errors) < 20:
            self.errors.append({"stage": stage, "error": str(error)[:1000]})

    def _shortlist(self, choices: list[dict]) -> list[dict]:
        """Keep a type-balanced, stable subset when action enumeration is huge."""
        if len(choices) <= self.max_presented_choices:
            return choices
        buckets: dict[str, list[dict]] = {}
        for choice in choices:
            kind = str(choice.get("type", "unknown"))
            if choice.get("deal_kind"):
                kind += ":" + str(choice["deal_kind"])
            buckets.setdefault(kind, []).append(choice)
        selected: list[dict] = []
        depth = 0
        while len(selected) < self.max_presented_choices:
            added = False
            for kind in sorted(buckets):
                bucket = buckets[kind]
                if depth < len(bucket):
                    selected.append(bucket[depth])
                    added = True
                    if len(selected) >= self.max_presented_choices:
                        break
            if not added:
                break
            depth += 1
        self.stats["shortlisted_decisions"] += 1
        return selected

    def _guard_repeated_zero_cost_portals(
        self, choices: list[dict], round_num: int,
    ) -> list[dict]:
        """Suppress repeated no-cost Portal routes for full-control model seats."""
        if not self.full_control:
            return choices
        if round_num != self._portal_guard_round:
            self._portal_guard_round = round_num
            self._used_zero_cost_portal_routes.clear()
        guarded: list[dict] = []
        suppressed = 0
        for choice in choices:
            route = (
                tuple(choice.get("from", [])),
                tuple(choice.get("dest", [])),
            )
            repeated_portal = (
                choice.get("type") == "move"
                and int(choice.get("cost", -1)) == 0
                and bool(choice.get("portal"))
                and route in self._used_zero_cost_portal_routes
            )
            if repeated_portal:
                suppressed += 1
            else:
                guarded.append(choice)
        if suppressed and guarded:
            self.stats["loop_guard_activations"] += 1
            self.stats["loop_choices_suppressed"] += suppressed
            return guarded
        return choices

    def _track_zero_cost_portal(self, choice: dict) -> None:
        if (
            self.full_control
            and choice.get("type") == "move"
            and int(choice.get("cost", -1)) == 0
            and bool(choice.get("portal"))
        ):
            self._used_zero_cost_portal_routes.add((
                tuple(choice.get("from", [])),
                tuple(choice.get("dest", [])),
            ))

    def _messages(self, task: str, payload: dict, phase: str) -> list[dict]:
        system = (
            "You are an Aeonis playtest agent, not the rules engine. Select only from the numbered legal "
            "choices. Give concise strategic reasoning, never hidden chain-of-thought. Flag genuine ambiguity "
            "in rules_question; do not invent rules. Your playstyle persona is " + self.persona + ".\n\n" +
            PHASE_DIGESTS.get(phase, "The engine enforces all legal timing and costs.")
        )
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": task + "\n" + json.dumps(payload, sort_keys=True)},
        ]

    def _provider_complete(self, messages: list[dict], schema: dict) -> dict:
        self.stats["provider_calls"] += 1
        started = time.monotonic()
        try:
            return _validate_response(self.provider.complete(messages, schema), schema)
        finally:
            self.stats["provider_seconds"] = round(
                self.stats["provider_seconds"] + time.monotonic() - started,
                3,
            )

    def choose(self, observation: dict, decision_point) -> dict:
        choices = decision_point.choices
        if len(choices) <= 1:
            self.stats["forced_choices"] += 1
            return choices[0]
        if not self.full_control and (
            decision_point.kind not in self.decision_kinds
            or int(observation["state"].get("round", 1)) < self.decision_round_min
            or self.stats["model_decision_attempts"] >= self.max_decision_calls
        ):
            self.stats["persona_delegations"] += 1
            return self.fallback.choose(observation, decision_point)

        compact = compact_observation(observation, decision_point)
        eligible_choices = self._guard_repeated_zero_cost_portals(
            choices, int(compact["round"]),
        )
        if len(eligible_choices) == 1:
            self.stats["forced_choices"] += 1
            return eligible_choices[0]
        presented_choices = (
            eligible_choices if self.full_control else self._shortlist(eligible_choices)
        )
        payload = {
            "observation": compact,
            "legal_choice_count": len(choices),
            "presented_choice_count": len(presented_choices),
            "legal_choices": [
                {"index": i, **_prompt_choice(choice)}
                for i, choice in enumerate(presented_choices)
            ],
        }
        negotiation = decision_point.kind == "negotiation"
        task = "Choose one legal action by action_index and annotate the playtest experience."
        if negotiation:
            task = (
                "Choose one legal negotiation action by action_index. Write a concise public table-facing "
                "message that accurately advocates, accepts, counters, rejects, or declines that indexed "
                "structured offer. The indexed terms control; prose cannot add or change terms. Set intent "
                "to one of trade, vote, non_aggression, attack_target, future_payment, mixed, or decline."
            )
        messages = self._messages(
            task,
            payload,
            str(decision_point.phase),
        )
        self.stats["model_decision_attempts"] += 1
        error = ""
        for attempt in range(self.retries + 1):
            try:
                if error:
                    messages = messages + [{
                        "role": "user",
                        "content": f"Validation error: {error}. Return a corrected JSON object only.",
                    }]
                schema = NEGOTIATION_DECISION_SCHEMA if negotiation else DECISION_SCHEMA
                result = self._provider_complete(messages, schema)
                index = int(result.get("action_index"))
                if not 0 <= index < len(presented_choices):
                    raise ProviderError(
                        f"action_index {index} outside 0..{len(presented_choices) - 1}"
                    )
                self.stats["model_decisions"] += 1
                message = _clean_string(result.get("message")) if negotiation else ""
                intent = _clean_string(result.get("intent")) if negotiation else ""
                if negotiation and message:
                    self._pending_negotiation_utterance = {
                        "message": message,
                        "intent": intent,
                    }
                self.annotations.append({
                    "round": compact["round"],
                    "phase": decision_point.phase,
                    "decision_kind": decision_point.kind,
                    "action_index": index,
                    "action": presented_choices[index],
                    "legal_choice_count": len(choices),
                    "presented_choice_count": len(presented_choices),
                    "reason": _clean_string(result.get("reason")),
                    "highlight": _clean_string(result.get("highlight")),
                    "frustration": _clean_optional(result.get("frustration")),
                    "rules_question": _clean_optional(result.get("rules_question")),
                    **({"message": message, "intent": intent} if negotiation else {}),
                })
                selected = presented_choices[index]
                self._track_zero_cost_portal(selected)
                return selected
            except (ProviderError, TypeError, ValueError, KeyError) as exc:
                error = str(exc)
                self._record_error("decision", exc)
                self.stats["invalid_responses"] += 1
                if attempt < self.retries:
                    self.stats["retries"] += 1

        self.stats["fallbacks"] += 1
        self.annotations.append({
            "round": compact["round"],
            "phase": decision_point.phase,
            "decision_kind": decision_point.kind,
            "fallback": True,
            "error": error[:600],
        })
        selected = self.fallback.choose(observation, decision_point)
        self._track_zero_cost_portal(selected)
        return selected

    def pop_negotiation_utterance(self) -> dict | None:
        utterance = self._pending_negotiation_utterance
        self._pending_negotiation_utterance = None
        return utterance

    def reflect(self, round_summary: dict) -> None:
        if len(self.reflections) >= self.max_round_reflections:
            return
        try:
            result = self._provider_complete(
                self._messages(
                    "Reflect on the completed round as a playtester. Base claims only on the supplied counts. "
                    "Use concrete sentences for highlight and frustration, and an empty string when there is "
                    "nothing to report. Focus on one useful signal; do not prescribe a rules change from one round.",
                    round_summary,
                    "cleanup",
                ),
                ROUND_REFLECTION_SCHEMA,
            )
            self.reflections.append({
                "round": round_summary.get("completed_round"),
                "summary": _clean_string(result.get("summary")),
                "highlight": _clean_string(result.get("highlight")),
                "frustration": _clean_optional(result.get("frustration")),
                "rules_question": _clean_optional(result.get("rules_question")),
            })
        except (ProviderError, TypeError, ValueError, KeyError) as exc:
            self._record_error("round_reflection", exc)
            self.stats["reflection_failures"] += 1
            self.reflections.append({
                "round": round_summary.get("completed_round"),
                "fallback": True,
                "error": str(exc)[:600],
            })

    def exit_interview(self, game_summary: dict) -> dict:
        try:
            result = self._provider_complete(
                self._messages(
                    "Complete the post-game playtest interview. Base every claim on the supplied metrics, note "
                    "small samples explicitly, and separate observation from hypotheses. Use an empty questions "
                    "list when no genuine rules question exists. Do not prescribe a canon change from one game.",
                    game_summary,
                    "cleanup",
                ),
                EXIT_INTERVIEW_SCHEMA,
            )
            self.interview = {
                "pacing": _clean_string(result.get("pacing")),
                "map_flow": _clean_string(result.get("map_flow")),
                "politics": _clean_string(result.get("politics")),
                "combat": _clean_string(result.get("combat")),
                "economy_pressure": _clean_string(result.get("economy_pressure")),
                "best_moment": _clean_string(result.get("best_moment")),
                "biggest_friction": _clean_string(result.get("biggest_friction")),
                "rules_questions": [_clean_string(x) for x in result.get("rules_questions", [])[:8]],
                "play_again": bool(result.get("play_again")),
                "hypotheses": [_clean_string(x) for x in result.get("hypotheses", [])[:5]],
            }
        except (ProviderError, TypeError, ValueError, KeyError) as exc:
            self._record_error("exit_interview", exc)
            self.stats["interview_failures"] += 1
            self.interview = {"fallback": True, "error": str(exc)[:600]}
        return self.interview

    def qualitative_payload(self) -> dict:
        return {
            "seat": self.seat,
            "persona": self.persona,
            "provider": self.provider.name,
            "full_control": self.full_control,
            "annotations": list(self.annotations),
            "round_reflections": list(self.reflections),
            "exit_interview": dict(self.interview or {}),
            "errors": list(self.errors),
            "stats": dict(self.stats),
        }
