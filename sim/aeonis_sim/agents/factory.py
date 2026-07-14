"""Construct agent tables from tournament / game config."""
from __future__ import annotations

from .chaos import ChaosBot
from .llm import LLMPlaytestAgent
from .persona import PERSONA_NAMES, PersonaBot
from .providers import provider_from_config


def make_agents(seat_personas: dict[int, str], seed: int) -> dict[int, object]:
    return {
        pid: PersonaBot(persona, seed * 1000 + pid)
        for pid, persona in seat_personas.items()
    }


def parse_persona_list(spec: str, players: int) -> dict[int, str]:
    """Comma-separated personas per seat, or one name for all seats."""
    parts = [p.strip().lower() for p in spec.split(",") if p.strip()]
    if len(parts) == 1:
        name = parts[0]
        if name == "chaos":
            return {i: "chaos" for i in range(players)}
        if name not in PERSONA_NAMES:
            raise ValueError(f"unknown persona: {name}")
        return {i: name for i in range(players)}
    if len(parts) != players:
        raise ValueError(f"expected {players} personas, got {len(parts)}")
    for p in parts:
        if p not in PERSONA_NAMES and p != "chaos":
            raise ValueError(f"unknown persona: {p}")
    return dict(enumerate(parts))


def agents_from_config(config: dict, seed: int) -> dict[int, object]:
    players = config["players"]
    personas = config.get("personas")
    if personas is None:
        seat = {p: "chaos" for p in range(players)}
    elif isinstance(personas, dict):
        seat = {int(k): v for k, v in personas.items()}
    elif isinstance(personas, list):
        seat = dict(enumerate(personas))
    else:
        raise ValueError("personas must be dict or list")
    out = {}
    qualitative = dict(config.get("llm_playtest", {}))
    qualitative_enabled = bool(qualitative.get("enabled", False))
    qualitative_seats = {int(x) for x in qualitative.get("seats", range(players))}
    seat_overrides = {
        int(k): dict(v)
        for k, v in dict(qualitative.get("seat_overrides", {})).items()
    }
    for pid in range(players):
        name = seat.get(pid, "balanced")
        if name == "chaos":
            fallback = ChaosBot(seed * 1000 + pid)
        else:
            fallback = PersonaBot(name, seed * 1000 + pid)
        if qualitative_enabled and pid in qualitative_seats:
            seat_config = {**qualitative, **seat_overrides.get(pid, {})}
            provider = provider_from_config(
                dict(qualitative.get("provider", {"type": "deterministic"})),
                seed=seed * 1000 + pid,
            )
            out[pid] = LLMPlaytestAgent(
                provider=provider,
                fallback=fallback,
                persona=name,
                seat=pid,
                decision_kinds=list(seat_config.get("decision_kinds", [])) or None,
                max_decision_calls=int(seat_config.get("max_decision_calls_per_seat", 8)),
                max_round_reflections=int(seat_config.get("max_round_reflections_per_seat", 2)),
                retries=int(seat_config.get("retries", 1)),
                decision_round_min=int(seat_config.get("decision_round_min", 1)),
                max_presented_choices=int(seat_config.get("max_presented_choices", 80)),
            )
        else:
            out[pid] = fallback
    return out
