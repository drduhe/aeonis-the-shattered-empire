# M4 full Lord-asymmetry encode — design

**Date:** 2026-07-10  
**Status:** IMPLEMENTED 2026-07-12 — gate closed (`docs/reports/2026-07-12-m4-gate.md`)  
**Prior art:** Plan 5 promoted; M4 foundation live (`docs/reports/2026-07-09-plan5-m4-foundation.md`); AL-49 open  
**Canon:** eight launch sheets in `lords/`; architecture milestone 4 in `docs/plans/2026-07-02-agent-playtest-simulation-design.md` §5

---

## 1. Goal

Close sim Milestone 4: encode the remaining launch-Lord sheet content behind the existing opt-in `lord_asymmetry` flag, then pass the architecture gate of **100 consecutive crash/invariant-free bot games**. M1–M3 default path and golden replays stay unchanged until that gate closes.

**In scope (architecture §5):** remaining passives/actives, unique starting tiles, faction discoveries, Legendary Buildings, 100-game gate, AL triage.

**Out of scope:** faction objectives, special/elite/mythic units, expansion Lords, Tier II+ shared Arcane content, balance tuning from partial win-rate tables.

---

## 2. Architecture (hybrid)

### 2.1 Package layout

```
sim/aeonis_sim/engine/lords/
  __init__.py          # public registry API + predicates (is_lord, round_unused, …)
  specs.py             # LordSpec, LAUNCH_LORDS, LORD_SPECS, configured_roster
  cassian.py … thalrik.py   # one module per launch Lord
```

Existing `lords.py` becomes the package above (move/rename; keep import paths stable via `__init__.py` re-exports so `from .lords import is_lord` continues to work).

### 2.2 Ownership split

| Layer | Owns |
| --- | --- |
| Per-Lord module | Sheet data: unique tile, ability hooks, faction discovery specs, Legendary Building spec; AL abstractions for that sheet |
| `lords/__init__.py` registry | Aggregates hooks; exposes thin helpers (`unique_tile_for`, `defense_bonus`, `faction_discoveries`, `legendary_for`, …) |
| Owning engine modules (`setup`, `move`, `combat`, `arcane`, `buildings`/`build`, `production`, `whispers`, `council`, `game`) | Legality, decision points, resolution; call registry helpers instead of raw `if is_lord` forests |

### 2.3 Opt-in

- `config["lord_asymmetry"]["enabled"]` remains required for all M4 behavior.
- Tournament rotation (`roster` + per-game `lords`) stays as in the foundation.
- Foundation signature hooks already encoded remain; this work fills the rest of each sheet.

### 2.4 Batch order

| Batch | Deliverable | Exit |
| --- | --- | --- |
| 0 | Package split + registry scaffolding; no behavior change | existing `test_lords_m4.py` green |
| 1 | Unique starting tiles | per-tile unit tests |
| 2 | Remaining abilities (+ AL abstractions) | per-ability unit tests; AL entries filed |
| 3 | Faction discoveries | research + effect tests |
| 4 | Legendary Buildings | build/prereq/VP/effect tests |
| 5 | 100-game gate + docs/INDEX/report; close or split AL-49 | `bracket-m4.json` 100/100 |

Each batch is shippable and testable alone. Prefer not to regenerate M1–M3 goldens unless a batch accidentally changes the default (non-M4) decision sequence — that is a bug.

---

## 3. Unique starting tiles (Batch 1)

### 3.1 Placement rule

At setup, after map generation and home assignment, for each player with a `lord_id`:

1. Find a controlled hex in the home cluster whose terrain matches the sheet’s “replaces your X” terrain (City home itself is never replaced except where a sheet says so — none of the launch 8 replace the City).
2. Prefer an adjacent non-City hex of that terrain under the player’s starting control; if none, search the home cluster; if still none, convert one adjacent non-City hex to the counted-as terrain and apply the unique overlay (log as AL if conversion is required often).
3. Mark the tile with `unique_tile_id` (string) and any flags the sheet needs (e.g. Thal’rik Rift Anchor also counts as Portal).

### 3.2 Per-Lord tiles

| Lord | Tile | Counts as | Production | Build permissions | Owner/controller benefit |
| --- | --- | --- | --- | --- | --- |
| Cassian | Caravan Bazaar | Desert | +2 Influence | Embassy yes; Tower no | Controller: +1 Gold once/round when any player initiates a 0-AP Trade |
| Seraphel | Arcane Nexus | Forest | +2 Mana | Tower yes; Grove no | Owner: once/round −1 Mana on one Research (min 0) |
| Vharok | Ironworks Ridge | Mountain | +2 Gold | Fortress allowed; Mine −1 Gold cost | Owner: once/round Fortress build −1 Gold (min 0) |
| Elyndra | Sacred Grove | Forest | +1 Mana, +1 Population | Tower yes; Grove no | Owner: end of Production & Upkeep +1 Population Pool (up to cap) |
| Rakhis | Oasis Wellspring | Plains | +1 Population, +1 Gold | Farm yes; Tower no | Owner: once/round Recruit 1 Cavalry at −1 Gold (min 0) |
| Nyxara | Obsidian Spire | Mountain | +1 Gold, +1 Mana | Mine yes; Tower no | Owner: Round Start +1 Whisper draw |
| Auriel | Hallowed Grove | Forest | +1 Mana, +1 Influence | Grove yes; Tower no | Owner: Cleanup & Checks +1 Renown while controlled |
| Thal’rik | Rift Anchor | Forest + Portal | +1 Mana | Tower yes; Grove no | Owner: once/round Portal travel from this tile enter+exit AP = 0 |

Population production on tiles means: increase that player’s population pool at Production (same channel as other pop producers), not a map token.

### 3.3 Engine touchpoints

- `setup.py` — place overlay.
- `production.py` — tile production + Elyndra owner benefit.
- `build` / recruit paths — permission and cost modifiers.
- `whispers` / Round Start — Nyxara Spire draw.
- `cleanup.py` — Auriel Renown.
- Trade initiation — Cassian Bazaar controller gold.
- `move.py` / portal — Rift Anchor free transit + Portal adjacency.

---

## 4. Remaining abilities (Batch 2)

Foundation already encodes the Plan 5 signatures listed in the foundation report. Batch 2 encodes everything else on the eight sheets.

### 4.1 Ability checklist (remaining)

| Lord | Remaining | Notes |
| --- | --- | --- |
| Cassian | Council Patronage; Letters of Credit | Lobby→+1 Gold; High Council 1 Inf→+2 Gold once/round |
| Seraphel | Scry the Council; Blink Step; Polymath virtual sigils | Peek top agenda; Move Mountains/Deserts as 1 AP for 2 Mana; virtual sigils → AL-50 |
| Vharok | Forged in Battle; Lock the Line | +1 Def on building hex (may overlap Bastion); retarget up to 2 attacker targets for 1 Mana |
| Elyndra | Rooted Defenses; Entangling Roots | Forest defense reroll; −2 to one Attack roll for 1 Mana |
| Rakhis | Sandstride pre-Pre-Strike retreat; Hit and Run; Desert Tempest | Completes AL-49 combat pieces; Desert +2 AP for others |
| Nyxara | Shadow Sight; Veil of Shadows | Private-hand peek → AL-51; Move ignore ZOC + pass through enemy hexes |
| Auriel | Radiant Presence; Exaltation | +1 Def while Auriel committed; 0-AP turn for 3 Inf→+2 Renown |
| Thal’rik | Threshold Ward; Rift Summon | +1 Def on Portal hex; Recruit into controlled Portals |

### 4.2 Ambiguity Ledger abstractions (policy A)

| ID | Topic | Interpretation for M4 gate |
| --- | --- | --- |
| AL-50 | Seraphel Polymath virtual sigils above Tier I | While shared Arcane remains Tier I only (AL-35), virtual sigils are a no-op for prerequisite checks. Second Research + Nexus discount still encode. Revisit when Tier II+ lands. |
| AL-51 | Nyxara Shadow Sight / Hall of Whispers hand peek | No private Whisper hands in bot games. Shadow Sight: once/round when another player plays a Whisper, Nyxara gains +1 information token recorded in state (no card reveal). Hall of Whispers “look at hand”: same no-op reveal; timing-window override and extra draw still encode. |
| AL-52 | Setup unique-tile placement when home cluster lacks the replaced terrain | Convert one adjacent non-City hex to the counted-as terrain, then apply overlay. |

Close AL-49 when Batches 2–4 land, pointing residuals at AL-50/51/52 as needed.

### 4.3 Combat / decision-point patterns

- **Rerolls / die modifiers** (Elyndra, Auriel, Vharok Forged, Thal’rik Ward): apply in existing combat modifier hooks.
- **Lock the Line / Entangling Roots / Desert Tempest / Exaltation / Letters of Credit / Veil / Blink / Hit and Run / pre-Pre-Strike retreat:** enumerate as optional decision points or post-battle follow-ups, same style as M3 rituals and M2 negotiation.
- Bots: prefer simple heuristics (use when mana/influence available and effect is strictly positive; skip otherwise). Correctness > clever play.

---

## 5. Faction discoveries (Batch 3)

Sixteen Lord-specific discoveries (2 per launch Lord). They are researched with the existing Research action, pay sheet costs, grant **1 Remnant** like Tier I, and do **not** use school sigil prerequisites.

### 5.1 Catalog

| Lord | Discovery | Cost | Effect summary |
| --- | --- | --- | --- |
| Cassian | Guild Contracts | 2G 2I | Market −1 Gold; once/round 0-AP Market Trade → +1 Influence |
| Cassian | Diplomatic Tariffs | 3I | Once/round when another player Trades, +1 Gold if you control an Embassy |
| Seraphel | Mana Nexus | 4M 1G | Controlled mana-producing hexes +1 Mana |
| Seraphel | Spellweave Doctrine | 2M 2I | Once/round after Lobby → +1 Mana |
| Vharok | Reinforced Fortifications | 3G 1M | Defending Tower hex +1 Defense (stacks with Tower) |
| Vharok | Siege Logistics | 2G 2I | Once/round after Attack vs City/Fortress → +1 AP |
| Elyndra | Thornwatch | 3M 1I | Archers on Battle Line defending Forest/Grove +1 Defense |
| Elyndra | Seedbound Resilience | 2M 2G | Once/round after battle in controlled hex → +1 Population Pool |
| Rakhis | Mirage Riders | 3G 1M | Cavalry +1 Attack when attacking from Desert |
| Rakhis | Sandsworn Pact | 2I 2G | Once/round claim neutral hex by move → +1 Gold |
| Nyxara | Stolen Secrets | 2M 2I | Once/round play WHEN Whisper → draw 1 Whisper |
| Nyxara | Shadow Network | 3M 1G | Once/round discard 1 Whisper → +2 Gold or +2 Influence |
| Auriel | Luminous Bulwark | 2M 2I | Defending hex with your building +1 Defense |
| Auriel | Sacred Rite | 3I 1M | First time at 5 and at 10 Renown: draw 2 Whispers + 1 VP each |
| Thal’rik | Planar Echo | 3M 1G | Once/round after Move with Portal travel → +1 AP |
| Thal’rik | Void Anchor | 2M 2I | Once/round spend 1 Mana: controlled hex counts as Portal for you until Cleanup |

Wire effects into the owning modules via registry callbacks. Research enumeration merges faction discoveries when `lord_asymmetry` is on and the player’s Lord owns that id.

---

## 6. Legendary Buildings (Batch 4)

### 6.1 Shared rules

- Only the matching Lord may build their Legendary.
- Cost: **4 AP** + listed resources; occupies **3 Population**; counts toward City building slots.
- On construct: **+2 Renown**; **2 VP** while the building’s City is controlled (Cleanup & Checks); captors gain the VP with the City.
- One copy per Lord.

### 6.2 Per-Lord Legendaries

| Lord | Building | Prerequisite | Resources | Effect summary |
| --- | --- | --- | --- | --- |
| Cassian | Grand Exchange | 2 Markets + 8+ Gold | 6G 3I | Production: +1 Gold per Trade this round; once/round extra 0-AP Trade |
| Seraphel | Arcane Sanctum | 3 Discoveries | 4G 6M | Production +2 Mana; once/round free Tier I Research; Lord +1 Attack die size in hex |
| Vharok | Iron Citadel | ≥1 Fortress | 8G 2M (upkeep 2G) | City treated as Fortress; defenders +3 Defense |
| Elyndra | Heartwood Sanctum | Pop cap 15+ | 3G 4M 2I | Production +3 pop growth here; adjacent controlled hexes +1 primary resource; units here +1 HP at Round Start |
| Rakhis | Windsworn Warcamp | 2 attacker battle wins | 5G 3I | Recruits here +1 Move first move/round; once/round free 1-hex Cavalry Move |
| Nyxara | Hall of Whispers | Played 4 Whispers | 4G 4M 2I | +1 Round Start Whisper; hand peek → AL-51; once/round play Whisper as any timing |
| Auriel | Cathedral of Radiance | 5 Renown | 4G 3M 3I | Influence double on motions you initiated; +1 Renown if Speaker at Production; defenders +2 Defense |
| Thal’rik | Dimensional Nexus | 2 Portals | 5G 5M | City counts as Portal; once/round 0-AP teleport group to a Portal you control or occupy |

Track cumulative counters on `PlayerState` as needed (Whispers played, attacker wins, etc.).

### 6.3 BuildingType

Add eight Legendary `BuildingType` values (or a single `LEGENDARY` plus `legendary_id` on the tile). Prefer explicit enum members for invariant clarity and capture/VP scoring.

---

## 7. Testing & gate (Batch 5)

### 7.1 Unit tests

- Extend `sim/tests/test_lords_m4.py` or split `test_lords_m4_tiles.py`, `_abilities.py`, `_discoveries.py`, `_legendaries.py`.
- At least one deterministic test per unique tile, remaining ability, faction discovery, and Legendary (prereq fail + success + effect).
- Foundation signature tests remain green.

### 7.2 Gate bracket

New `sim/configs/bracket-m4.json`:

- 4p mixed personas, `lord_asymmetry.enabled`, rotating roster
- **100 games**, seed base distinct from foundation (e.g. 95000)
- Hard gates: crash_rate=0, timeout_rate=0, degenerate_rate=0, completed_rate=1.0
- Record (not hard-gate): mean rounds, win rate by Lord (watch items only)

CI: add job or extend workflow like M3 (`bracket-m4-ci.json` may be a shorter smoke if full 100 is too slow for PR CI; the milestone gate itself is 100 games run locally/report).

### 7.3 Docs on gate close

- Report: `docs/reports/2026-07-10-m4-gate.md` (or dated run day)
- Update `docs/plans/INDEX.md` M4 line to DONE
- Update `sim/README.md`
- Close AL-49; open/resolve AL-50–52 as specified
- `content-manifest.json` only if new docs are browsable

---

## 8. Non-goals / guardrails

- Do not tune Lord balance from foundation or mid-batch win rates.
- Do not enable `lord_asymmetry` by default until Batch 5 passes.
- Do not encode faction objectives or special units under this design.
- Do not expand shared Arcane past Tier I solely to make Polymath sigils matter (AL-50).
- Mechanics doc changes are not required; canon sheets are already locked. Sim-only encode + ledger + reports/plans index.

---

## 9. Success criteria

1. All Batch 0–4 pytest coverage green.
2. `bracket-m4.json` completes 100/100 with zero crash/timeout/degenerate.
3. Default (M4-off) goldens and M1–M3 CI brackets still green.
4. AL-49 closed; AL-50–52 recorded.
5. Plans INDEX marks M4 Lord asymmetry DONE (opt-in full encode).
)