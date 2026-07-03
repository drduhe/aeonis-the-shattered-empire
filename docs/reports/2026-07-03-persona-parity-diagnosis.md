# Persona Parity Diagnosis — Mixed 4p M2 Smoke

**Date:** 2026-07-03 · **Sim-only** (not canon)

## Symptom (pre-fix)

| Persona | Mixed win % | Solo win % |
| --- | ---: | ---: |
| Expander | **68%** | 25% |
| Economist | **0%** | 25% |
| Balanced | 24% | 25% |
| Warmonger | 25% | 25% |
| Diplomat | 9% | 25% |

Solo brackets are flat (~25% each). Skew is a **mixed-seat interaction**, not a broken persona in isolation.

## Root causes (design vs bot)

### 1. Game tempo favors map race (design signal)

- Mean game length **~6 rounds** after M2 pacing fixes.
- **~83% of all VP** from objectives; expander winners average **6.4 rounds** vs balanced **8.1**.
- Expander winner VP mix: **63% objective + 23% coronation_rite** — seat + territory path closes before economy scales.
- Public row includes **frontier_lord** (7 hexes) and **seat_of_empire** — both reward expansion tempo.

**Verdict:** Some expander dominance is **real design pressure** in a short, objective-heavy sim — not fixed by inflating random weights. Longer human games or more economy objectives may be needed for canon parity.

### 2. Economist bot bug (bot artifact)

- `builder_need` weight was **-4.0** — penalized actions when the Builder objective was unmet.
- Economist seats scored **4+ objective VP in 68% of games** but **won 0%** — they build score but lose the race to 10 VP.

**Fix:** Flip `builder_need` to **+4.0**; add `builder_push` feature when Builder is on the public row.

### 3. Expander runaway when ahead (bot + design)

- High `seat` / `rite_ready` weights + weak lead brake → keeps pressing after taking lead.
- `territory_sat` penalty existed but was insufficient at 5–7 hexes.

**Fix:** Negative `vp_lead` weight, stronger `territory_sat`, lower seat/rite weights — **brake when ahead**, not nerfed baseline expansion.

### 4. Persona-blind strategy layer (bot gap)

- Draft and primary scoring favored **bounty + low initiative** for all personas equally.
- Economist never prioritized **Economic Boom** primaries; expander never prioritized **Expansion Strategy** draft.

**Fix:** Persona-aware draft/primary scoring tied to card identity.

## What we did NOT do

- No global VP threshold changes.
- No objective point rewrites.
- No arbitrary +50% weight inflation across all economist features.

## Regression targets (mixed 4p smoke)

- Expander win % **≤ 35%** (H7 direction; not claiming full kill yet)
- Economist win % **≥ 5%** (H8 direction)
- Solo 4p ladder stays **~20–30%** per persona (no collateral damage)

Re-run `bracket-m2-smoke.json` after fixes and compare this doc.

---

## Post-fix results (100-game `bracket-m2-smoke.json`, seed_base 70000)

| Persona | Mixed win % (pre) | Mixed win % (post) | Solo win % |
| --- | ---: | ---: | ---: |
| Expander | **68%** | **31.5%** | 25% |
| Economist | **0%** | **1.3%** | 25% |
| Balanced | 24% | 51.4% | 25% |
| Warmonger | 25% | 34.5% | 25% |
| Diplomat | 9% | 6.8% | 25% |

*Mixed win % = wins / games **when that persona is seated** (mixed matchmaking seats 4 of 5 roster personas per game).*

### Gate check

| Target | Result |
| --- | --- |
| Expander ≤ 35% | **Pass** (31.5%) |
| Economist ≥ 5% | **Fail** (1.3%) — design signal, not more bot tuning |
| Solo ~20–30% each | **Pass** (25% flat) |
| H7 (exp ≤30%, max ≤28%) | **Inconclusive** — expander in band; balanced seated rate elevated |
| H8 (7–8p, eco ≥5%) | **Unchanged** — still inconclusive at 4p; prior sprint doc applies |

### Interpretation: bot artifact vs design pressure

**Fixed by bot changes (not canon):**

- Expander runaway → lead brake + territory saturation + persona-aware strategy picks.
- Economist actively sabotaged its own Builder path (`builder_need` sign bug).
- Persona-blind strategy draft/primary layer.

**Still looks like design (do not keep inflating weights):**

- Economist seats still lose the **race to 10 VP** in ~6-round games even after the bug fix. Builder (3 buildings) + `golden_hoard` (10 gold) do not close before expander/warmonger objective paths.
- ~83% VP from objectives; public row rewards **map tempo** (`frontier_lord`, `seat_of_empire`).
- Solo ladder flat at 25% — personas work in isolation; mixed skew is **interaction + tempo**, not broken persona definitions.

**Calibration stop rule:** If a persona is flat solo but weak mixed after obvious bot bugs are fixed, treat as **canon/playtest input** (pacing, objective mix, economy VP hooks) — not another +20% weight pass. Next levers are Plan 4 pacing or economist-tagged public objectives, not `PERSONA_WEIGHTS` inflation.

### Shipped code

- `persona.py` — economist `builder_need` +4, expander lead brake, persona-aware draft/primary scoring.
- `features.py` — `builder_push` when Builder is on the public row and unscored.
- `tests/test_persona_parity.py` — regression on weights and draft preferences.

**158 pytest passing** · golden replays unchanged (deterministic engine path).
