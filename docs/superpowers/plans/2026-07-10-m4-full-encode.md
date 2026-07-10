# M4 Full Lord-Asymmetry Encode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Encode the remaining eight launch-Lord sheet contents (unique tiles, remaining abilities, faction discoveries, Legendary Buildings) behind opt-in `lord_asymmetry`, then close the architecture 100-game M4 gate.

**Architecture:** Hybrid package `sim/aeonis_sim/engine/lords/` — per-Lord modules own sheet data/hooks; owning engine modules stay authoritative and call a thin registry. M1–M3 defaults and goldens stay unchanged; M4 remains opt-in until Batch 5.

**Tech Stack:** Python 3.11, pytest, existing `aeonis_sim` engine, `scripts/regression_check.py` brackets.

**Spec:** `docs/superpowers/specs/2026-07-10-m4-full-encode-design.md`

**Working directory for all commands:** `sim/` unless noted.

---

## File structure (locked)

| Path | Responsibility |
| --- | --- |
| `aeonis_sim/engine/lords/__init__.py` | Public API: predicates, registry helpers, re-exports |
| `aeonis_sim/engine/lords/specs.py` | `LordSpec`, `LAUNCH_LORDS`, `LORD_SPECS`, `configured_roster` |
| `aeonis_sim/engine/lords/tiles.py` | `UniqueTileSpec`, `UNIQUE_TILES`, `place_unique_tiles`, production/build helpers |
| `aeonis_sim/engine/lords/cassian.py` … `thalrik.py` | Per-Lord ability/discovery/legendary hooks + constants |
| `aeonis_sim/engine/lords.py` | **Deleted** after package lands (imports keep working via package) |
| `aeonis_sim/engine/types.py` | `Tile.unique_tile_id`, Legendary `BuildingType`s, player counters |
| `aeonis_sim/engine/setup.py` | Call `place_unique_tiles` after home control |
| `aeonis_sim/engine/{build,recruit,move,combat,arcane,production,cleanup,game,whispers}.py` | Call registry helpers |
| `tests/test_lords_m4_*.py` | Split coverage by batch |
| `configs/bracket-m4.json`, `bracket-m4-ci.json` | Gate + CI smoke |
| `playtest/Ambiguity_Ledger.md` | AL-49 close; AL-50/51/52 |
| `docs/reports/YYYY-MM-DD-m4-gate.md`, `docs/plans/INDEX.md`, `sim/README.md` | Gate close docs |

---

### Task 0: Lords package split (no behavior change)

**Files:**
- Create: `sim/aeonis_sim/engine/lords/specs.py`
- Create: `sim/aeonis_sim/engine/lords/__init__.py`
- Create: `sim/aeonis_sim/engine/lords/cassian.py`, `seraphel.py`, `vharok.py`, `elyndra.py`, `rakhis.py`, `nyxara.py`, `auriel.py`, `thalrik.py` (empty modules with module docstring only)
- Delete: `sim/aeonis_sim/engine/lords.py`
- Test: `sim/tests/test_lords_m4.py` (existing; must stay green)

- [ ] **Step 1: Move `LordSpec` / roster into `specs.py`**

Copy the current contents of `lords.py` (`LordSpec`, `LAUNCH_LORDS`, `LORD_SPECS`, and all helper functions) into `aeonis_sim/engine/lords/specs.py` unchanged.

- [ ] **Step 2: Re-export from package `__init__.py`**

```python
"""Launch-Lord signatures for the M4 asymmetry layer."""
from .specs import (
    LAUNCH_LORDS,
    LORD_SPECS,
    LordSpec,
    configured_roster,
    is_lord,
    lord_attack_die,
    lord_defense_die,
    lord_hp,
    lord_id,
    lord_move,
    mark_round_used,
    round_unused,
    spec_for,
    whisper_hand_limit,
)

__all__ = [
    "LAUNCH_LORDS", "LORD_SPECS", "LordSpec", "configured_roster",
    "is_lord", "lord_attack_die", "lord_defense_die", "lord_hp",
    "lord_id", "lord_move", "mark_round_used", "round_unused",
    "spec_for", "whisper_hand_limit",
]
```

Create eight stub files like:

```python
"""Cassian sheet hooks (M4)."""
```

- [ ] **Step 3: Remove old `lords.py` module file**

Delete `sim/aeonis_sim/engine/lords.py` so the package takes precedence.

- [ ] **Step 4: Run foundation tests**

Run: `python -m pytest tests/test_lords_m4.py -q`

Expected: PASS (all existing tests)

- [ ] **Step 5: Commit**

```bash
git add sim/aeonis_sim/engine/lords/ sim/aeonis_sim/engine/lords.py
git commit -m "refactor(sim): split M4 lords into package with stable imports"
```

---

### Task 1: Unique-tile field + placement helper

**Files:**
- Modify: `sim/aeonis_sim/engine/types.py` (`Tile`)
- Create: `sim/aeonis_sim/engine/lords/tiles.py`
- Modify: `sim/aeonis_sim/engine/lords/__init__.py`
- Modify: `sim/aeonis_sim/engine/setup.py`
- Test: `sim/tests/test_lords_m4_tiles.py`

- [ ] **Step 1: Write failing placement test**

```python
"""M4 unique starting tiles."""
from __future__ import annotations
import random
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import Terrain

ROSTER = [
    "cassian", "seraphel", "vharok", "elyndra",
    "rakhis", "nyxara", "auriel", "thalrik",
]

EXPECTED = {
    "cassian": ("caravan_bazaar", Terrain.DESERT),
    "seraphel": ("arcane_nexus", Terrain.FOREST),
    "vharok": ("ironworks_ridge", Terrain.MOUNTAIN),
    "elyndra": ("sacred_grove", Terrain.FOREST),
    "rakhis": ("oasis_wellspring", Terrain.PLAINS),
    "nyxara": ("obsidian_spire", Terrain.MOUNTAIN),
    "auriel": ("hallowed_grove", Terrain.FOREST),
    "thalrik": ("rift_anchor", Terrain.FOREST),
}

def test_each_lord_gets_unique_tile_in_home_cluster():
    state = build_initial_state(
        {"players": 8, "lord_asymmetry": {"enabled": True, "lords": ROSTER}},
        random.Random(19),
    )
    for p in state.players:
        uid, terrain = EXPECTED[p.lord_id]
        matches = [
            t for t in state.tiles.values()
            if t.unique_tile_id == uid and t.controller == p.pid
        ]
        assert len(matches) == 1, p.lord_id
        tile = matches[0]
        assert tile.terrain == terrain
        assert tile.coord != p.home  # never replaces City
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_lords_m4_tiles.py::test_each_lord_gets_unique_tile_in_home_cluster -v`

Expected: FAIL (`unique_tile_id` missing or placement missing)

- [ ] **Step 3: Add `Tile.unique_tile_id`**

In `types.py` on `Tile`, add `unique_tile_id: str = ""`. Include it in `to_dict`, `from_dict`, and `GameState.copy()` tile reconstruction (mirror `building_relic` handling).

- [ ] **Step 4: Implement `lords/tiles.py`**

```python
"""Unique starting tiles for launch Lords."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from ..hexmap import neighbors
from ..types import Terrain

@dataclass(frozen=True)
class UniqueTileSpec:
    id: str
    lord_id: str
    replaces: Terrain          # preferred existing terrain to overlay
    counts_as: Terrain         # terrain after placement
    gold: int = 0
    mana: int = 0
    influence: int = 0
    population: int = 0        # added to pop_pool at Production
    allow_buildings: frozenset = frozenset()
    deny_buildings: frozenset = frozenset()
    portal: bool = False       # also functions as Portal (Rift Anchor)

UNIQUE_TILES: dict[str, UniqueTileSpec] = {
    "cassian": UniqueTileSpec(
        "caravan_bazaar", "cassian", Terrain.DESERT, Terrain.DESERT,
        influence=2, allow_buildings=frozenset({"embassy"}),
        deny_buildings=frozenset({"tower"}),
    ),
    "seraphel": UniqueTileSpec(
        "arcane_nexus", "seraphel", Terrain.FOREST, Terrain.FOREST,
        mana=2, allow_buildings=frozenset({"tower"}),
        deny_buildings=frozenset({"grove"}),
    ),
    "vharok": UniqueTileSpec(
        "ironworks_ridge", "vharok", Terrain.MOUNTAIN, Terrain.MOUNTAIN,
        gold=2, allow_buildings=frozenset({"fortress", "mine"}),
        deny_buildings=frozenset(),
    ),
    "elyndra": UniqueTileSpec(
        "sacred_grove", "elyndra", Terrain.FOREST, Terrain.FOREST,
        mana=1, population=1, allow_buildings=frozenset({"tower"}),
        deny_buildings=frozenset({"grove"}),
    ),
    "rakhis": UniqueTileSpec(
        "oasis_wellspring", "rakhis", Terrain.PLAINS, Terrain.PLAINS,
        gold=1, population=1, allow_buildings=frozenset({"farm"}),
        deny_buildings=frozenset({"tower"}),
    ),
    "nyxara": UniqueTileSpec(
        "obsidian_spire", "nyxara", Terrain.MOUNTAIN, Terrain.MOUNTAIN,
        gold=1, mana=1, allow_buildings=frozenset({"mine"}),
        deny_buildings=frozenset({"tower"}),
    ),
    "auriel": UniqueTileSpec(
        "hallowed_grove", "auriel", Terrain.FOREST, Terrain.FOREST,
        mana=1, influence=1, allow_buildings=frozenset({"grove"}),
        deny_buildings=frozenset({"tower"}),
    ),
    "thalrik": UniqueTileSpec(
        "rift_anchor", "thalrik", Terrain.FOREST, Terrain.FOREST,
        mana=1, allow_buildings=frozenset({"tower"}),
        deny_buildings=frozenset({"grove"}), portal=True,
    ),
}

def unique_spec_for_lord(lord_id: str) -> Optional[UniqueTileSpec]:
    return UNIQUE_TILES.get(lord_id)

def place_unique_tiles(state) -> None:
    """AL-52: prefer matching terrain in home cluster; else convert one adjacent hex."""
    from .specs import LORD_SPECS
    for p in state.players:
        if p.lord_id not in LORD_SPECS:
            continue
        spec = UNIQUE_TILES[p.lord_id]
        home = p.home
        candidates = []
        for nb in neighbors(home):
            t = state.tiles.get(nb)
            if t is None or t.imperial_seat or t.terrain == Terrain.CITY:
                continue
            if t.controller == p.pid and t.terrain == spec.replaces:
                candidates.append(t)
        if not candidates:
            for nb in neighbors(home):
                t = state.tiles.get(nb)
                if t is None or t.imperial_seat or t.terrain == Terrain.CITY:
                    continue
                if t.controller == p.pid:
                    candidates.append(t)
                    break
        if not candidates:
            # Convert first adjacent non-city hex (AL-52)
            for nb in neighbors(home):
                t = state.tiles.get(nb)
                if t is not None and not t.imperial_seat and t.terrain != Terrain.CITY:
                    t.controller = p.pid
                    candidates.append(t)
                    break
        tile = candidates[0]
        tile.terrain = spec.counts_as
        tile.unique_tile_id = spec.id
        # Cassian needs Desert in cluster — deserts are not auto-controlled at setup;
        # ensure controller after conversion.
        tile.controller = p.pid

def tile_is_portal(state, coord) -> bool:
    t = state.tiles[coord]
    if t.terrain == Terrain.PORTAL:
        return True
    if t.unique_tile_id == "rift_anchor":
        return True
    return False
```

Export `place_unique_tiles`, `unique_spec_for_lord`, `UNIQUE_TILES`, `tile_is_portal` from `lords/__init__.py`.

- [ ] **Step 5: Call placement from setup**

In `setup.py`, after the home-neighbor control loop (after line ~112) and before `pop_pool` seeding:

```python
from .lords import place_unique_tiles
# ...
place_unique_tiles(state)
```

Only runs meaningfully when lords are assigned (`configured_roster` non-empty ids); `place_unique_tiles` no-ops players without `lord_id` in `LORD_SPECS`.

- [ ] **Step 6: Run tile test**

Run: `python -m pytest tests/test_lords_m4_tiles.py tests/test_lords_m4.py -q`

Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add sim/aeonis_sim/engine/types.py sim/aeonis_sim/engine/lords/ sim/aeonis_sim/engine/setup.py sim/tests/test_lords_m4_tiles.py
git commit -m "feat(sim): place M4 unique starting tiles at setup"
```

---

### Task 2: Unique-tile production, build permissions, owner benefits

**Files:**
- Modify: `sim/aeonis_sim/engine/production.py`
- Modify: `sim/aeonis_sim/engine/build.py`
- Modify: `sim/aeonis_sim/engine/recruit.py`
- Modify: `sim/aeonis_sim/engine/arcane.py`
- Modify: `sim/aeonis_sim/engine/game.py` (round-start whisper; trade bazaar)
- Modify: `sim/aeonis_sim/engine/cleanup.py`
- Modify: `sim/aeonis_sim/engine/move.py` (Rift Anchor free portal)
- Modify: `sim/aeonis_sim/engine/lords/tiles.py` (helper predicates)
- Test: `sim/tests/test_lords_m4_tiles.py`

- [ ] **Step 1: Write failing production/permission tests**

```python
def test_arcane_nexus_produces_two_mana():
    state = build_initial_state(
        {"players": 1, "lord_asymmetry": {"enabled": True, "lords": ["seraphel"]}},
        random.Random(3),
    )
    from aeonis_sim.engine.production import run_production
    before = state.player(0).mana
    run_production(state)
    # Nexus +2 mana beyond any other forest production on that hex
    nexus = next(t for t in state.tiles.values() if t.unique_tile_id == "arcane_nexus")
    assert nexus.controller == 0
    assert state.player(0).mana >= before + 2

def test_sacred_grove_denies_grove_allows_tower():
    from aeonis_sim.engine.build import enumerate_builds
    from aeonis_sim.engine.types import BuildingType
    state = build_initial_state(
        {"players": 1, "lord_asymmetry": {"enabled": True, "lords": ["elyndra"]}},
        random.Random(5),
    )
    p = state.player(0)
    p.ap, p.gold, p.mana, p.influence, p.pop_pool = 10, 20, 20, 20, 20
    grove = next(t for t in state.tiles.values() if t.unique_tile_id == "sacred_grove")
    builds = enumerate_builds(state, 0)
    assert any(b["building"] == "tower" and b["hex"] == list(grove.coord) for b in builds)
    assert not any(b["building"] == "grove" and b["hex"] == list(grove.coord) for b in builds)
```

- [ ] **Step 2: Run tests — expect FAIL**

Run: `python -m pytest tests/test_lords_m4_tiles.py -q`

Expected: FAIL on production/permissions

- [ ] **Step 3: Wire production for unique tiles**

In `production.py` `run_production`, after normal tile production for each controlled tile:

```python
from .lords import unique_spec_for_lord
# when processing tile with unique_tile_id:
spec = None
for lid, us in UNIQUE_TILES.items():  # or lookup by id
    if us.id == tile.unique_tile_id:
        spec = us
        break
if spec and tile.controller is not None:
    p = state.player(tile.controller)
    p.gold += spec.gold
    p.mana += spec.mana
    p.influence += spec.influence
    if spec.population:
        room = state.pop_cap(p.pid) - state.pop_used(p.pid) - p.pop_pool
        # prefer: add to pop_pool up to remaining cap headroom
        p.pop_pool += min(spec.population, max(0, state.pop_cap(p.pid) - state.pop_used(p.pid) - p.pop_pool + spec.population))
```

Prefer a clean helper `apply_unique_tile_production(state, tile)` in `lords/tiles.py` that adds gold/mana/influence/population correctly using `pop_cap`/`pop_used`.

Also at end of each player's production pass: if Elyndra owns `sacred_grove` under her control, `pop_pool += 1` up to cap (owner-only benefit — separate from tile printed production).

- [ ] **Step 4: Wire build permissions**

In `enumerate_builds`, when considering `tile` with `unique_tile_id`:

```python
from .lords.tiles import unique_spec_by_id
us = unique_spec_by_id(tile.unique_tile_id)
if us:
    if btype.value in us.deny_buildings:
        continue
    # allow listed buildings even if terrain would normally block (e.g. Fortress on Ironworks)
    if us.allow_buildings and btype.value in us.allow_buildings:
        # skip terrain mismatch continue
        pass
    elif spec.terrain is not None and tile.terrain != spec.terrain:
        continue
```

Vharok Mine on Ironworks: `-1` gold via `build_gold_cost` hook or local override in `apply_build`/`build_gold_cost`. Fortress once/round `-1` gold when owner controls Ironworks: use `lord_round["ironworks_fortress"]`.

Seraphel Nexus: once/round `-1` mana on Research — in `arcane.research_resource_cost`, if owner controls nexus and `round_unused(..., "nexus_discount")`, reduce mana by 1 and mark used on apply.

- [ ] **Step 5: Wire remaining owner benefits**

| Benefit | Hook |
| --- | --- |
| Nyxara Obsidian Spire +1 Whisper at Round Start | `game._round_start`: if controls spire, `draw_whispers(..., 1)` extra (stacks with Nyxara 3 → 4) |
| Auriel Hallowed Grove +1 Renown at Cleanup | `cleanup.run_cleanup`: if controls grove, `renown += 1` |
| Cassian Bazaar +1 Gold on 0-AP Trade | `game.submit` trade branch when AP cost is 0: find controller of `caravan_bazaar`, once/round via `lord_round` or tile flag on controller |
| Rakhis Oasis Cavalry −1 Gold | `recruit.py` when recruiting exactly one Cavalry and controls oasis, once/round |
| Thal’rik Rift Anchor free portal from tile | `move.py` portal cost 0 once/round when origin is rift_anchor and owner |

- [ ] **Step 6: Add tests for Spire draw, Auriel renown, Rift portal flag**

```python
def test_rift_anchor_counts_as_portal():
    from aeonis_sim.engine.lords import tile_is_portal
    state = build_initial_state(
        {"players": 1, "lord_asymmetry": {"enabled": True, "lords": ["thalrik"]}},
        random.Random(7),
    )
    anchor = next(t for t in state.tiles.values() if t.unique_tile_id == "rift_anchor")
    assert tile_is_portal(state, anchor.coord)
```

- [ ] **Step 7: Run all tile tests + foundation**

Run: `python -m pytest tests/test_lords_m4_tiles.py tests/test_lords_m4.py -q`

Expected: PASS

- [ ] **Step 8: Commit**

```bash
git add sim/aeonis_sim/engine/production.py sim/aeonis_sim/engine/build.py sim/aeonis_sim/engine/recruit.py sim/aeonis_sim/engine/arcane.py sim/aeonis_sim/engine/game.py sim/aeonis_sim/engine/cleanup.py sim/aeonis_sim/engine/move.py sim/aeonis_sim/engine/lords/ sim/tests/test_lords_m4_tiles.py
git commit -m "feat(sim): wire unique-tile production, permissions, and owner benefits"
```

---

### Task 3: Remaining combat passives + AL ledger stubs

**Files:**
- Modify: `sim/aeonis_sim/engine/combat.py`
- Modify: `sim/aeonis_sim/engine/lords/{vharok,elyndra,auriel,thalrik,rakhis}.py`
- Modify: `sim/aeonis_sim/engine/lords/__init__.py` — add `defense_bonus(state, battle, side) -> int` aggregating Lord hooks
- Modify: `playtest/Ambiguity_Ledger.md`
- Test: `sim/tests/test_lords_m4_abilities.py`

- [ ] **Step 1: Write failing defense-passive tests**

```python
"""Remaining M4 abilities."""
from __future__ import annotations
import random
from aeonis_sim.engine import combat
from aeonis_sim.engine.setup import build_initial_state
from aeonis_sim.engine.types import BuildingType, Terrain, UnitType, Unit, UNIT_STATS
from tests.test_lords_m4 import strip_map, put

def _m4(lords, n=None):
    n = n or len(lords)
    return build_initial_state(
        {"players": n, "lord_asymmetry": {"enabled": True, "lords": lords}},
        random.Random(11),
    )

def test_auriel_radiant_presence_adds_defense_when_committed():
    state = strip_map(_m4(["auriel", "vharok"]))
    hex_ = (1, 0)
    state.tiles[hex_].terrain = Terrain.PLAINS
    state.tiles[hex_].controller = 0
    put(state, hex_, 0, UnitType.INFANTRY)
    put(state, hex_, 0, UnitType.LORD)
    put(state, (2, 0), 1, UnitType.INFANTRY)
    state.tiles[(2, 0)].controller = 1
    # Attack into auriel's hex from vharok
    state.player(1).ap = 5
    b = combat.start_battle(state, 1, {"target": list(hex_), "cost": 2, "units": None})
    assert combat._defense_bonus(state, b, "def") >= 1
```

Add similar tests for: Thal’rik Portal ward (+1 on portal hex), Elyndra forest reroll flag path (unit test the helper that grants one reroll), Vharok Forged (already +1 from bastion path — assert building hex still +1 even if you temporarily disable bastion cap logic; Forged is the +1 Defense already present — document that Bastion Doctrine + Forged share the +1 Defense line already encoded; only Lock the Line is new for Vharok combat active).

**Clarification for implementers:** Foundation already applies Vharok +1 Defense on built hexes in `_defense_bonus`. Treat Forged in Battle as that line. Do not double it. Task 3 focuses on Auriel Radiant Presence, Thal’rik Threshold Ward, Elyndra Rooted Defenses (reroll), and ledger entries.

- [ ] **Step 2: Run — expect FAIL for Auriel/Thal’rik/Elyndra**

Run: `python -m pytest tests/test_lords_m4_abilities.py -q`

- [ ] **Step 3: Implement registry `extra_defense_bonus`**

```python
# lords/__init__.py
def extra_defense_bonus(state, battle, side: str) -> int:
    if side != "def" or battle.defender is None:
        return 0
    bonus = 0
    t = state.tiles[battle.target]
    # Auriel Radiant Presence
    if is_lord(state, battle.defender, "auriel"):
        if any(u.type.value == "lord" and u.owner == battle.defender
               for u in list(battle.def_line) + [u for _, u in battle.def_committed]):
            bonus += 1
    # Thal'rik Threshold Ward
    if is_lord(state, battle.defender, "thalrik") and tile_is_portal(state, battle.target):
        bonus += 1
    return bonus
```

In `combat._defense_bonus`, add `bonus += extra_defense_bonus(state, battle, side)`.

Elyndra Rooted Defenses: in `resolve_round` / `_strike` defense path, once per battle round when defending Forest, allow one defense die reroll via `battle.whisper_mods` or `lord_round["rooted_reroll_r{N}"]` — prefer auto-reroll if new roll is higher (bot-safe, no DP).

- [ ] **Step 4: Add AL-50, AL-51, AL-52 to Ambiguity Ledger**

Append rows (Open → Resolved for AL-52 when Task 1 placement is done; AL-50/51 Resolved with the abstractions in the design):

| AL-50 | Seraphel virtual sigils above Tier I | No-op while Tier I only (AL-35). |
| AL-51 | Nyxara hand peek | Information token counter `shadow_sight_tokens` on PlayerState; no card reveal. |
| AL-52 | Unique tile terrain missing | Convert adjacent hex (implemented in `place_unique_tiles`). |

- [ ] **Step 5: Run tests**

Run: `python -m pytest tests/test_lords_m4_abilities.py tests/test_lords_m4.py -q`

Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add sim/aeonis_sim/engine/combat.py sim/aeonis_sim/engine/lords/ sim/tests/test_lords_m4_abilities.py playtest/Ambiguity_Ledger.md
git commit -m "feat(sim): encode M4 combat passives and AL-50/51/52"
```

---

### Task 4: Remaining actives and decision-point abilities

**Files:**
- Modify: `sim/aeonis_sim/engine/game.py`, `move.py`, `combat.py`, `recruit.py`, `council` paths
- Modify: per-Lord modules under `lords/`
- Test: `sim/tests/test_lords_m4_abilities.py`

Implement and test each ability below. For each: write a focused failing test first, then minimal wiring, then re-run.

#### 4a — Cassian Council Patronage + Letters of Credit

- Patronage: after lobby resolves with Influence spent, if Cassian and `round_unused(..., "patronage")`, `gold += 1`, mark used.
- Letters: during High Council, free action choice `{"type":"letters_of_credit"}` costing 1 Influence → +2 Gold once/round. Enumerate from council decision window in `game.py` (same phase as lobby).

#### 4b — Seraphel Scry the Council + Blink Step

- Scry: at High Council phase start, if Seraphel, expose `agenda_deck[0]` via a skippable DP `{"type":"scry_ack"}` (bot always acks). No deck mutation.
- Blink: Move choice flag `blink_step: true` with `mana >= 2` once/round; Mountains/Deserts cost 1 for that path enumeration.

#### 4c — Vharok Lock the Line

- After targets declared / before dice in `resolve_round`, if Vharok defender committed and mana ≥ 1 and unused this battle round, optional DP to reassign up to 2 attacker targets. Bot heuristic: skip (safe default) unless a trivial self-damage case exists; still enumerate for legality tests.

#### 4d — Elyndra Entangling Roots

- Once per battle round while defending Forest, after an enemy Attack roll, optional spend 1 Mana to apply −2 (min 1). Bot: use when it would prevent a hit.

#### 4e — Rakhis Sandstride pre-Pre-Strike retreat + Hit and Run + Desert Tempest

- Pre-Pre-Strike: before archer pre-strike in `resolve_round`, once per battle, Rakhis may retreat committed group (reuse defender/attacker retreat destination rules; block City/Fortress/Hold-the-Walls per sheet).
- Hit and Run: in `finish_battle`, if Rakhis won as attacker and `round_unused(..., "hit_and_run")`, enumerate free 1-hex move for survivors to controlled/neutral adjacent; apply and mark.
- Desert Tempest: Action choice spend 2 Mana, choose controlled Desert; store `state.desert_tempest = {coord, round}`; `move.py` adds +2 AP for other players entering that hex until cleanup clears it.

#### 4f — Nyxara Shadow Sight + Veil of Shadows

- Shadow Sight (AL-51): when another player plays a Whisper, if Nyxara and unused, `nyxara.shadow_sight_tokens += 1` (add field on `PlayerState`, default 0, serialize in to_dict/from_dict/copy).
- Veil: Move flag `veil: true`, cost 2 Mana once/round; ignore ZOC; allow path through enemy-controlled hexes; cannot end on enemy-occupied hex.

#### 4g — Auriel Exaltation

- Action choice `{"type":"exaltation"}`: requires 3 Influence, 0 AP, consumes turn (`_finish_action_turn`), +2 Renown once/round.

#### 4h — Thal’rik Rift Summon

- In `enumerate_recruits`, if Thal’rik, also allow recruit placement on controlled Portal hexes (including Rift Anchor), still max 2 units and pop/gold rules; track `recruited_cities` by coord equivalently.

- [ ] **Step final for Task 4: full ability suite green**

Run: `python -m pytest tests/test_lords_m4_abilities.py tests/test_lords_m4.py -q`

Expected: PASS

- [ ] **Commit**

```bash
git add sim/aeonis_sim/engine/ sim/tests/test_lords_m4_abilities.py
git commit -m "feat(sim): encode remaining M4 Lord actives and decision hooks"
```

---

### Task 5: Faction discoveries — catalog + research merge

**Files:**
- Create: `sim/aeonis_sim/engine/lords/discoveries.py` (or per-Lord `DISCOVERIES` dicts merged in `__init__.py`)
- Modify: `sim/aeonis_sim/engine/arcane.py` — `enumerate_research` / `apply_research` include faction ids
- Test: `sim/tests/test_lords_m4_discoveries.py`

- [ ] **Step 1: Failing test — Cassian can research Guild Contracts**

```python
def test_cassian_can_research_guild_contracts():
    from aeonis_sim.engine.arcane import enumerate_research, apply_research
    state = build_initial_state(
        {"players": 1, "lord_asymmetry": {"enabled": True, "lords": ["cassian"]}},
        random.Random(2),
    )
    p = state.player(0)
    p.ap, p.gold, p.influence = 5, 10, 10
    choices = enumerate_research(state, 0)
    assert any(c["discovery"] == "guild_contracts" for c in choices)
    apply_research(state, 0, "guild_contracts")
    assert "guild_contracts" in p.discoveries
    assert p.remnants >= 1
```

- [ ] **Step 2: Run — expect FAIL**

- [ ] **Step 3: Register all 16 discoveries**

```python
# lords/discoveries.py
from dataclasses import dataclass

@dataclass(frozen=True)
class FactionDiscoverySpec:
    id: str
    lord_id: str
    gold: int = 0
    mana: int = 0
    influence: int = 0

FACTION_DISCOVERIES: dict[str, FactionDiscoverySpec] = {
    "guild_contracts": FactionDiscoverySpec("guild_contracts", "cassian", gold=2, influence=2),
    "diplomatic_tariffs": FactionDiscoverySpec("diplomatic_tariffs", "cassian", influence=3),
    "mana_nexus": FactionDiscoverySpec("mana_nexus", "seraphel", mana=4, gold=1),
    "spellweave_doctrine": FactionDiscoverySpec("spellweave_doctrine", "seraphel", mana=2, influence=2),
    "reinforced_fortifications": FactionDiscoverySpec("reinforced_fortifications", "vharok", gold=3, mana=1),
    "siege_logistics": FactionDiscoverySpec("siege_logistics", "vharok", gold=2, influence=2),
    "thornwatch": FactionDiscoverySpec("thornwatch", "elyndra", mana=3, influence=1),
    "seedbound_resilience": FactionDiscoverySpec("seedbound_resilience", "elyndra", mana=2, gold=2),
    "mirage_riders": FactionDiscoverySpec("mirage_riders", "rakhis", gold=3, mana=1),
    "sandsworn_pact": FactionDiscoverySpec("sandsworn_pact", "rakhis", influence=2, gold=2),
    "stolen_secrets": FactionDiscoverySpec("stolen_secrets", "nyxara", mana=2, influence=2),
    "shadow_network": FactionDiscoverySpec("shadow_network", "nyxara", mana=3, gold=1),
    "luminous_bulwark": FactionDiscoverySpec("luminous_bulwark", "auriel", mana=2, influence=2),
    "sacred_rite": FactionDiscoverySpec("sacred_rite", "auriel", influence=3, mana=1),
    "planar_echo": FactionDiscoverySpec("planar_echo", "thalrik", mana=3, gold=1),
    "void_anchor": FactionDiscoverySpec("void_anchor", "thalrik", mana=2, influence=2),
}
```

In `enumerate_research`, after Tier I loop, if `is_lord` matches and id not owned and resources afford, append research choice. `apply_research` accepts faction ids: charge costs from `FactionDiscoverySpec`, append to `discoveries`, +1 Remnant, no school sigils (AL-50).

- [ ] **Step 4: Run discovery enum test — PASS**

- [ ] **Step 5: Commit**

```bash
git add sim/aeonis_sim/engine/lords/discoveries.py sim/aeonis_sim/engine/arcane.py sim/aeonis_sim/engine/lords/__init__.py sim/tests/test_lords_m4_discoveries.py
git commit -m "feat(sim): register sixteen M4 faction discoveries for Research"
```

---

### Task 6: Faction discovery effects

**Files:** owning modules per effect; tests in `test_lords_m4_discoveries.py`

Wire each effect (test-first per discovery or small groups):

| Discovery | Wire into |
| --- | --- |
| `guild_contracts` | `build_gold_cost` for Market −1; on 0-AP Market trade +1 Influence once/round |
| `diplomatic_tariffs` | on other player trade start, +1 Gold if Embassy controlled, once/round |
| `mana_nexus` | production: +1 mana per mana-producing controlled hex |
| `spellweave_doctrine` | after lobby, +1 Mana once/round |
| `reinforced_fortifications` | `_defense_bonus` +1 on Tower hex |
| `siege_logistics` | after Attack vs City/Fortress, +1 AP once/round |
| `thornwatch` | defense +1 for Archers on line in Forest |
| `seedbound_resilience` | after battle in controlled hex, +1 pop_pool once/round |
| `mirage_riders` | attack die +1 for Cavalry attacking from Desert |
| `sandsworn_pact` | on claim neutral by move, +1 Gold once/round |
| `stolen_secrets` | on WHEN whisper play, draw 1 once/round |
| `shadow_network` | free action discard whisper → +2 gold or +2 influence once/round |
| `luminous_bulwark` | defense +1 on hex with your building |
| `sacred_rite` | on renown crossing 5 and 10 first time: draw 2 whispers + 1 VP (`add_vp(..., "sacred_rite")`); track `sacred_rite_5` / `sacred_rite_10` flags on player |
| `planar_echo` | after move with portal travel, +1 AP once/round |
| `void_anchor` | action: spend 1 Mana, mark controlled hex `void_anchor_until_round`; `tile_is_portal` true for owner only; clear in cleanup |

- [ ] **Step: Run discovery tests**

Run: `python -m pytest tests/test_lords_m4_discoveries.py -q`

Expected: PASS (at least one test per discovery)

- [ ] **Commit**

```bash
git add sim/aeonis_sim/engine/ sim/tests/test_lords_m4_discoveries.py
git commit -m "feat(sim): wire M4 faction discovery effects"
```

---

### Task 7: Legendary Buildings — types, shared rules, build path

**Files:**
- Modify: `sim/aeonis_sim/engine/types.py` — eight `BuildingType` members + `BUILDING_SPECS`
- Create: `sim/aeonis_sim/engine/lords/legendaries.py`
- Modify: `sim/aeonis_sim/engine/build.py`
- Modify: `sim/aeonis_sim/engine/cleanup.py` — score 2 VP for controlled Legendaries
- Modify: `sim/aeonis_sim/engine/production.py` — upkeep for Iron Citadel
- Test: `sim/tests/test_lords_m4_legendaries.py`

- [ ] **Step 1: Failing test — only Cassian can build Grand Exchange when prereqs met**

```python
def test_grand_exchange_prereqs_and_cost():
    from aeonis_sim.engine.build import enumerate_builds, apply_build
    from aeonis_sim.engine.types import BuildingType, Terrain
    state = build_initial_state(
        {"players": 1, "lord_asymmetry": {"enabled": True, "lords": ["cassian"]}},
        random.Random(9),
    )
    p = state.player(0)
    home = state.tiles[p.home]
    home.buildings = [BuildingType.MARKET, BuildingType.MARKET]
    # City slot: Markets already 2 — need room; use pop/resources
    p.ap, p.gold, p.influence, p.pop_pool = 10, 20, 10, 10
    # If slots full, clear one market into a second city tile if needed for the test map
    choices = enumerate_builds(state, 0)
    ge = [c for c in choices if c["building"] == "grand_exchange"]
    assert ge, "expected Grand Exchange when 2 Markets and 8+ gold"
    apply_build(state, 0, ge[0])
    assert p.renown >= 2
    assert BuildingType.GRAND_EXCHANGE in state.tiles[tuple(ge[0]["hex"])].buildings
```

- [ ] **Step 2: Add BuildingTypes**

```python
class BuildingType(str, Enum):
    # ... existing ...
    GRAND_EXCHANGE = "grand_exchange"
    ARCANE_SANCTUM = "arcane_sanctum"
    IRON_CITADEL = "iron_citadel"
    HEARTWOOD_SANCTUM = "heartwood_sanctum"
    WINDSWORN_WARCAMP = "windsworn_warcamp"
    HALL_OF_WHISPERS = "hall_of_whispers"
    CATHEDRAL_OF_RADIANCE = "cathedral_of_radiance"
    DIMENSIONAL_NEXUS = "dimensional_nexus"

LEGENDARY_BUILDINGS = frozenset({
    BuildingType.GRAND_EXCHANGE, BuildingType.ARCANE_SANCTUM,
    BuildingType.IRON_CITADEL, BuildingType.HEARTWOOD_SANCTUM,
    BuildingType.WINDSWORN_WARCAMP, BuildingType.HALL_OF_WHISPERS,
    BuildingType.CATHEDRAL_OF_RADIANCE, BuildingType.DIMENSIONAL_NEXUS,
})
```

`BUILDING_SPECS` entries: `terrain=Terrain.CITY`, `pop=3`, resource costs per design §6.2; Iron Citadel `upkeep_gold=2`.

- [ ] **Step 3: `legendaries.py` prereq helpers**

```python
def legendary_for_lord(lord_id: str) -> BuildingType | None: ...

def can_build_legendary(state, pid, btype: BuildingType) -> bool:
    # matching lord, not already built anywhere, prereqs, city slot, resources, ap>=4
    ...
```

Prereqs:
- Grand Exchange: ≥2 Markets controlled + gold ≥ 8
- Arcane Sanctum: `len(discoveries) >= 3`
- Iron Citadel: any Fortress controlled
- Heartwood: `state.pop_cap(pid) >= 15` (Elyndra starts 11 — need growth; test can set cap via controlling pop buildings / temporary test hook `p._test_pop_cap` only if pop_cap is derived — prefer set `pop` buildings or temporarily monkeypatch in test)
- Warcamp: track `attacker_battle_wins` on PlayerState (increment in `finish_battle` when attacker wins); need ≥ 2
- Hall of Whispers: `whispers_played` counter ≥ 4 (increment on whisper play)
- Cathedral: `renown >= 5`
- Nexus: count portal hexes controlled ≥ 2 (include rift_anchor)

- [ ] **Step 4: `build_ap_cost` returns 4 for Legendaries; `enumerate_builds` filters via `can_build_legendary`; `apply_build` grants +2 Renown**

- [ ] **Step 5: Cleanup VP**

In `run_cleanup` scoring section:

```python
for t in state.tiles.values():
    for b in t.buildings:
        if b in LEGENDARY_BUILDINGS and t.controller is not None:
            state.player(t.controller).add_vp(2, f"legendary:{b.value}")
```

Ensure `add_vp` is idempotent per cleanup pass (score each cleanup from sources reset, or use the same pattern as artifact VP — check `score_artifact_vp` and mirror).

- [ ] **Step 6: Tests green + commit**

```bash
git commit -m "feat(sim): Legendary Building types, prereqs, build, and VP"
```

---

### Task 8: Legendary Building effects

**Files:** production, combat, move, recruit, game, whispers, council; tests in `test_lords_m4_legendaries.py`

Implement effects from design §6.2 (test-first per building):

| Building | Effect hooks |
| --- | --- |
| Grand Exchange | Production +1 gold per trade this round (track `trades_this_round` on GameState); extra 0-AP trade once/round |
| Arcane Sanctum | Production +2 mana; free Tier I research once/round; Lord attack die +1 while on hex |
| Iron Citadel | Treat city as Fortress for siege; defenders +3 Defense |
| Heartwood Sanctum | +3 pop growth at hex; adjacent controlled +1 primary resource; units on hex +1 HP Round Start |
| Windsworn Warcamp | Recruits from this city +1 move first move/round; free 1-hex cavalry move once/round |
| Hall of Whispers | +1 Round Start whisper; AL-51 peek no-op; once/round play whisper as any timing (`hall_any_timing` flag) |
| Cathedral of Radiance | Double influence on motions you initiated; +1 Renown at Production if Speaker; defenders +2 |
| Dimensional Nexus | City counts as Portal; once/round 0-AP teleport group to portal you control/occupy |

- [ ] **Run:** `python -m pytest tests/test_lords_m4_legendaries.py -q` → PASS

- [ ] **Commit:** `feat(sim): wire Legendary Building effects for all eight Lords`

---

### Task 9: Full M4 pytest sweep + default regression

- [ ] **Step 1: Run full sim pytest**

Run: `python -m pytest -q`

Expected: PASS

- [ ] **Step 2: Confirm M4-off goldens still match**

Run: `python -m pytest tests/test_golden_replays.py -q` (or the repo’s golden test module name)

Expected: PASS without regenerating. If fail, **stop** — find accidental default-path change; do not regenerate unless intentional.

- [ ] **Step 3: Commit any test fixes only if needed**

---

### Task 10: 100-game gate + CI smoke + docs

**Files:**
- Create: `sim/configs/bracket-m4.json`
- Create: `sim/configs/bracket-m4-ci.json`
- Modify: `.github/workflows/sim.yml`
- Create: `docs/reports/2026-07-10-m4-gate.md` (date = run day)
- Modify: `docs/plans/INDEX.md`, `sim/README.md`, `playtest/Ambiguity_Ledger.md` (close AL-49)
- Modify: `docs/superpowers/specs/2026-07-10-m4-full-encode-design.md` status → IMPLEMENTED
- Modify: `content-manifest.json` if reports are browsable

- [ ] **Step 1: Write `bracket-m4.json`**

```json
{
  "name": "m4-gate-4p-mixed",
  "players": 4,
  "games": 100,
  "seed_base": 95000,
  "personas": ["warmonger", "economist", "expander", "diplomat", "balanced"],
  "matchmaking": "mixed",
  "seat_rewards": {"seat_of_empire_vp": 1},
  "lord_asymmetry": {
    "enabled": true,
    "roster": [
      "cassian", "seraphel", "vharok", "elyndra",
      "rakhis", "nyxara", "auriel", "thalrik"
    ]
  },
  "regression": {
    "plan": "m4",
    "step": "gate",
    "gates": [
      {"metric": "crash_rate", "label": "Crash rate", "max": 0.0},
      {"metric": "timeout_rate", "label": "Timeout rate", "max": 0.0},
      {"metric": "degenerate_rate", "label": "Degenerate rate", "max": 0.0},
      {"metric": "completed_rate", "label": "Completed rate", "min": 1.0}
    ]
  }
}
```

- [ ] **Step 2: Write `bracket-m4-ci.json`** — same but `"games": 20`, `"seed_base": 95100`, step `gate_ci`.

- [ ] **Step 3: Add CI job**

Copy `m3-gate` job in `.github/workflows/sim.yml` to `m4-gate` running `configs/bracket-m4-ci.json`.

- [ ] **Step 4: Run local 100-game gate**

Run: `python scripts/regression_check.py --config configs/bracket-m4.json --workers 4`

Expected: all gates pass (100/100 completed, 0 crash/timeout/degenerate)

If failures: fix engine bugs; do not loosen gates.

- [ ] **Step 5: Write gate report**

Include completed count, mean rounds, win-rate-by-Lord table (watch only), note AL-49 closed / AL-50–52 resolved.

- [ ] **Step 6: Update INDEX.md M4 line to DONE; sim README; close AL-49**

- [ ] **Step 7: Commit**

```bash
git add sim/configs/bracket-m4.json sim/configs/bracket-m4-ci.json .github/workflows/sim.yml docs/reports/ docs/plans/INDEX.md sim/README.md playtest/Ambiguity_Ledger.md docs/superpowers/ content-manifest.json
git commit -m "feat(sim): close M4 Lord-asymmetry gate (100-game)"
```

---

## Spec coverage checklist

| Spec section | Task(s) |
| --- | --- |
| §2 Hybrid package | Task 0 |
| §3 Unique tiles | Tasks 1–2 |
| §4 Remaining abilities | Tasks 3–4 |
| §4.2 AL-50/51/52 | Task 3 |
| §5 Faction discoveries | Tasks 5–6 |
| §6 Legendary Buildings | Tasks 7–8 |
| §7 Testing & 100-game gate | Tasks 9–10 |
| §8 Non-goals | Enforced throughout (no faction objectives/special units/default-on) |

## Self-review notes

- No Tier II Arcane expansion; Polymath sigils stay AL-50 no-op.
- Vharok Forged Defense is not double-counted with existing bastion +1.
- `attacker_battle_wins` / `whispers_played` / `shadow_sight_tokens` are new PlayerState fields introduced in Tasks 4/7 with full serialization.
- Goldens must not regenerate on M4-off path.
