from __future__ import annotations

from .types import UnitType


class InvariantViolation(AssertionError):
    pass


def check_invariants(state) -> None:
    seen_uids = set()
    lords = {}
    for coord, t in state.tiles.items():
        for u in t.units:
            if u.uid in seen_uids:
                raise InvariantViolation(f"duplicate uid {u.uid}")
            seen_uids.add(u.uid)
            if u.hp < 1:
                raise InvariantViolation(f"dead unit on board at {coord}")
            if u.type == UnitType.LORD:
                lords[u.owner] = lords.get(u.owner, 0) + 1
    for pid, n in lords.items():
        if n > 1:
            raise InvariantViolation(f"player {pid} has {n} lords")
    for p in state.players:
        for attr in ("gold", "mana", "influence", "ap", "pop_pool", "vp", "renown"):
            if getattr(p, attr) < 0:
                raise InvariantViolation(f"player {p.pid} negative {attr}")
        if p.lord_captured and state.find_lord(p.pid) is not None:
            raise InvariantViolation(f"player {p.pid} captured lord on board")
        # Note: pop_used may legally exceed GLOBAL_POP_CAP via involuntary
        # acquisition (conquest, adjacency claims, occupation flips) — AL-15.
        # The cap only gates voluntary recruit/build through the pop_pool.
        if sum(p.vp_sources.values()) != p.vp:
            raise InvariantViolation(f"player {p.pid} vp/source mismatch")
