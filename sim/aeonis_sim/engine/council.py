"""High Council phase (High_Council.md / First_Playable_Packet.md §5).

M2: bots propose/vote on revealed agenda cards; structured negotiation in Task 6.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .hexmap import neighbors
from .objectives import record_influence_hex_gain, record_public_progress

if TYPE_CHECKING:
    from .types import GameState

AGENDA_CARD_IDS: tuple[str, ...] = (
    "road_networks",
    "demilitarized_zone",
    "open_borders_treaty",
    "imperial_annexation",
    "border_arbitration",
    "realm_tax",
    "hero_of_the_realm",
    "magister_of_mana",
)


@dataclass(frozen=True)
class AgendaCard:
    id: str
    name: str
    kind: str  # law | decree | title


AGENDA_CARDS: dict[str, AgendaCard] = {
    "road_networks": AgendaCard("road_networks", "Road Networks", "law"),
    "demilitarized_zone": AgendaCard("demilitarized_zone", "Demilitarized Zone", "decree"),
    "open_borders_treaty": AgendaCard("open_borders_treaty", "Open Borders Treaty", "decree"),
    "imperial_annexation": AgendaCard("imperial_annexation", "Imperial Annexation", "decree"),
    "border_arbitration": AgendaCard("border_arbitration", "Border Arbitration", "decree"),
    "realm_tax": AgendaCard("realm_tax", "Realm Tax", "law"),
    "hero_of_the_realm": AgendaCard("hero_of_the_realm", "Hero of the Realm", "title"),
    "magister_of_mana": AgendaCard("magister_of_mana", "Magister of Mana", "title"),
}


def init_agenda_deck(rng: random.Random) -> list[str]:
    deck = list(AGENDA_CARD_IDS)
    rng.shuffle(deck)
    return deck


def reveal_agenda(state: GameState, rng: random.Random) -> str | None:
    if not state.agenda_deck:
        state.agenda_deck = init_agenda_deck(rng)
    if not state.agenda_deck:
        return None
    card = state.agenda_deck.pop()
    state.agenda_revealed = card
    return card


def council_votes(state: GameState, pid: int) -> int:
    from .artifacts import council_influence_bonus
    p = state.player(pid)
    votes = 1 + council_influence_bonus(state, pid)
    if p.renown >= 5:
        votes += 1
    if p.renown >= 10:
        votes += 1
    return votes


def enumerate_proposal_choices(state: GameState, pid: int) -> list[dict]:
    if not state.agenda_revealed:
        return [{"type": "council_pass"}]
    if state.council_crisis and pid == state.speaker:
        return [{
            "type": "council_propose",
            "motion": state.agenda_revealed,
        }]
    return [
        {"type": "council_pass"},
        {
            "type": "council_propose",
            "motion": state.agenda_revealed,
        },
    ]


def enumerate_vote_choices(state: GameState, pid: int, motion_id: str) -> list[dict]:
    p = state.player(pid)
    choices = [
        {"type": "council_vote", "motion": motion_id, "support": False, "lobby": 0},
        {"type": "council_vote", "motion": motion_id, "support": True, "lobby": 0},
    ]
    if p.influence >= 2:
        choices.append({
            "type": "council_vote",
            "motion": motion_id,
            "support": True,
            "lobby": 2,
        })
    if p.influence >= 4:
        choices.append({
            "type": "council_vote",
            "motion": motion_id,
            "support": True,
            "lobby": 4,
        })
    return choices


def tally_votes(
    state: GameState,
    motion_id: str,
    ballots: list[dict],
    *,
    extra_yes: int = 0,
    extra_no: int = 0,
    proposer: int | None = None,
) -> bool:
    """Majority of votes cast passes; Speaker breaks ties."""
    from .lords.legendaries import controls_legendary
    from .types import BuildingType

    yes = extra_yes
    no = extra_no
    for b in ballots:
        multiplier = 2 if b.get("sanctify") else 1
        if not b.get("support"):
            no += multiplier * council_votes(state, b["pid"])
            continue
        lobby = int(b.get("lobby", 0))
        lobby_votes = lobby // 2
        if (
            proposer is not None
            and b["pid"] == proposer
            and controls_legendary(state, proposer, BuildingType.CATHEDRAL_OF_RADIANCE)
        ):
            lobby_votes = lobby  # double influence on motions you initiated
        yes += multiplier * (council_votes(state, b["pid"]) + lobby_votes)
    if yes > no:
        return True
    if no > yes:
        return False
    # Tie: motion fails (no Speaker auto-pass in M2 sim).
    return False


def _fortress_blocks_annex(state: "GameState", coord, pid: int) -> bool:
    for n in neighbors(coord):
        nt = state.tiles.get(n)
        if nt is None or nt.controller is None or nt.controller == pid:
            continue
        from .types import BuildingType
        if nt.has(BuildingType.FORTRESS):
            return True
    return False


def _claim_influence_hex(state: "GameState", proposer: int) -> None:
    """Annexation / arbitration: claim one eligible neutral adjacent to proposer territory."""
    cands = []
    for t in state.controlled(proposer):
        for nb in neighbors(t.coord):
            nt = state.tiles.get(nb)
            if nt is None or nt.controller is not None:
                continue
            if any(u.owner != proposer for u in nt.units):
                continue
            if _fortress_blocks_annex(state, nb, proposer):
                continue
            cands.append(nb)
    if not cands:
        return
    coord = min(cands)
    state.tiles[coord].controller = proposer
    state.tiles[coord].explored = True
    record_influence_hex_gain(state, proposer, coord)


def apply_motion(state: GameState, motion_id: str, proposer: int, rng=None) -> None:
    p = state.player(proposer)
    if motion_id == "road_networks":
        if motion_id not in state.active_laws:
            state.active_laws.append(motion_id)
    elif motion_id == "realm_tax":
        if motion_id not in state.active_laws:
            state.active_laws.append(motion_id)
        for pl in state.players:
            pl.gold += 1
            if pl.influence > 0:
                pl.influence -= 1
    elif motion_id == "imperial_annexation":
        p.influence += 2
        _claim_influence_hex(state, proposer)
    elif motion_id == "hero_of_the_realm":
        from .lords.discoveries import bump_renown
        bump_renown(state, proposer, 1, rng)
        p.influence += 1
    elif motion_id == "magister_of_mana":
        p.mana += 2
    elif motion_id == "border_arbitration":
        p.influence += 1
        _claim_influence_hex(state, proposer)
    # demilitarized_zone / open_borders_treaty: no-op in M2 sim


def run_emergency_council(state: GameState, proposer: int, rng: random.Random) -> bool:
    """Diplomatic Decree: propose revealed agenda and resolve vote immediately."""
    if not state.agenda_revealed:
        reveal_agenda(state, rng)
    motion = state.agenda_revealed
    if not motion:
        return False
    ballots = []
    for pid in range(len(state.players)):
        support = pid == proposer or rng.random() < 0.35
        ballots.append({"pid": pid, "support": support, "lobby": 0})
    if tally_votes(state, motion, ballots, proposer=proposer):
        apply_motion(state, motion, proposer, rng)
        card = AGENDA_CARDS.get(motion)
        for ballot in ballots:
            if ballot.get("support") and int(ballot.get("lobby", 0)):
                record_public_progress(
                    state, ballot["pid"], "council_power", int(ballot.get("lobby", 0)),
                )
            if ballot.get("support") and card and card.kind == "law":
                record_public_progress(state, ballot["pid"], "lawgiver")
        return True
    return False


def motion_vote_utility(
    state: GameState,
    pid: int,
    motion_id: str,
    proposer: int,
    *,
    support: bool,
    lobby: int = 0,
) -> float:
    """Heuristic utility for a council ballot (sim-only, not canon)."""
    if pid == proposer:
        return 2.5 if support else 0.1

    card = AGENDA_CARDS.get(motion_id)
    kind = card.kind if card else "decree"
    p = state.player(pid)

    if not support:
        score = 0.65
    else:
        score = 0.35

    if motion_id == "realm_tax":
        if support:
            score = 1.3 if p.gold < 7 else 0.55
        else:
            score = 0.85 if p.influence >= 2 else 0.45
    elif motion_id == "road_networks":
        score = 0.95 if support else 0.55
    elif motion_id in ("demilitarized_zone", "open_borders_treaty"):
        score = 0.45 if support else 0.85
    elif kind == "title" or motion_id in (
        "imperial_annexation",
        "border_arbitration",
        "magister_of_mana",
    ):
        score = 0.2 if support else 1.05
    elif motion_id == "hero_of_the_realm":
        score = 0.15 if support else 1.1

    if lobby > 0:
        if support and p.influence >= lobby + 1:
            score += 0.35
        else:
            score -= 2.0
    return score


def persona_motion_adjustment(
    persona: str,
    motion_id: str,
    *,
    support: bool,
) -> float:
    """Persona-specific council lean (sim-only)."""
    adj = 0.0
    if persona == "diplomat":
        adj += 0.35 if support else -0.1
        if motion_id in ("open_borders_treaty", "border_arbitration", "demilitarized_zone"):
            adj += 0.25 if support else -0.15
    elif persona == "warmonger":
        if motion_id in ("demilitarized_zone", "open_borders_treaty"):
            adj -= 0.45 if support else 0.2
        if motion_id == "hero_of_the_realm":
            adj += 0.2 if support else -0.1
    elif persona == "economist":
        if motion_id == "realm_tax":
            adj += 0.4 if support else -0.2
        if motion_id == "road_networks":
            adj += 0.2 if support else 0.0
    elif persona == "expander":
        if motion_id == "imperial_annexation":
            adj += 0.3 if support else -0.15
    return adj
