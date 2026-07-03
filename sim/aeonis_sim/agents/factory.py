"""Construct agent tables from tournament / game config."""
from __future__ import annotations

from .chaos import ChaosBot
from .persona import PERSONA_NAMES, PersonaBot


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
        return {p: ChaosBot(seed * 1000 + p) for p in range(players)}
    if isinstance(personas, dict):
        seat = {int(k): v for k, v in personas.items()}
    elif isinstance(personas, list):
        seat = dict(enumerate(personas))
    else:
        raise ValueError("personas must be dict or list")
    out = {}
    for pid in range(players):
        name = seat.get(pid, "balanced")
        if name == "chaos":
            out[pid] = ChaosBot(seed * 1000 + pid)
        else:
            out[pid] = PersonaBot(name, seed * 1000 + pid)
    return out
