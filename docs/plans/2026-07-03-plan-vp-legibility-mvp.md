# Plan 3 MVP — VP Legibility (First Playable slice)

- **Status:** PROPOSED — scoped for playtest + sim; not canon until locked in `INDEX.md`
- **Date:** 2026-07-03
- **Parent:** [Plan 3: VP Legibility](2026-07-02-plan-vp-legibility.md)
- **Design intent (locked):** Objectives are the spine (~60% of winner VP). Conquest is viable (~20% of winner VP) but does not drown objectives. Lord capture stays **+1 VP** per capture.

---

## 1. What this MVP changes (and what it doesn't)

### In scope (MVP)

| Change | Plan 3 ref | Why MVP |
|--------|------------|---------|
| **Shared public objective row** (6 First Playable cards) | D1 | Legibility + races everyone toward the same visible goals |
| **Coronation Rite** replaces Seat +1/round drip | D3 | Same total Seat VP budget; requires Lord on throne; stops silent accounting wins |
| **Objective scoring at Cleanup & Checks** (lock AL-5) | — | Spine needs explicit timing |
| **VP permanence** (one canon line + objective/rite behavior) | D2 (partial) | Objectives and Rite score once, never lost |
| **Population cap/pool clarity** (lock AL-1, AL-4) | — | Prerequisite for sim; no VP impact |

### Explicitly unchanged in MVP

| Item | Rationale |
|------|-----------|
| **Lord capture +1 VP** | Fits ~20% military budget; conquest viability |
| **Secret objectives** (1 per player at start) | Personal spice; still ~2 VP each |
| **10 VP threshold / final round** | Defer until data says otherwise |
| **Plan 1 combat** (Edge, Pillage) | Parallel track; encode after or with MVP sim |

### Deferred to full Plan 3 sweep

- D4 purchased VP removal (not in M1 sim)
- D5 event VP audit
- Artifact / Legendary Building score-once (Milestone 3)
- Council Title score-once (Milestone 2)
- Full 24-card `Objectives.md` audit + Charters variant write-up
- `rulebook/` full rewrite (add First Playable callouts only if time)

---

## 2. VP budget (success target)

Winner's typical 10 VP after MVP + Plan 1:

| Source | Target VP | Share |
|--------|-----------|-------|
| Shared public + secret objectives | **6+** | **≥60%** |
| Coronation Rite (+ streak bonus) | 1–3 | ~15–25% |
| Lord capture (+ artifacts when they land) | 1–2 | ~10–20% |
| Other (events, titles in later milestones) | 0–1 | ≤10% |

**Sim regression gate (Bracket A, 1,000 games):**

| Metric | Current (baseline) | MVP target |
|--------|-------------------|------------|
| Winner objective VP share | ~15% | **≥50%** (stretch ≥60%) |
| Winner Seat+streak share | ~73% | **≤35%** |
| Winner lord capture share | ~12% | **10–25%** (viable, not dominant) |
| Table lord capture (all VP) | ~22% | no hard cap; watch for spike |

---

## 3. Rules text (MVP canon direction)

### 3.1 Shared public row (First Playable)

**Setup:** Shuffle the 6 public objective cards. Reveal **2** face-up in the shared row. Each player still draws **1 secret** at start.

**Each Round Start (from Round 2):** Reveal **1** additional public card until all 6 are face-up (by Round 5 at latest).

**Scoring (Cleanup & Checks):** Each revealed public objective may be scored by **each player once per game** when that player meets the condition. Limit: **1 public objective per player per round.** Mark scored objectives with that player's token on the card.

**First Playable card list** (shared race):

- Frontier Lord · Builder · **Merchant Lord** · Portal Mastery · Warlord · Seat of Empire

> **Sixth-slot note (updated 2026-07-03):** Council Power stays out until the full-deck audit. The sixth slot is filled by **Merchant Lord** (8+ Gold), a PROPOSED economy experiment from the Economist viability memo (Lever B) — defined in `rules_and_systems/Objectives.md` §4.4.

### 3.2 Coronation Rite (replaces §3.2 Seat drip)

**Remove:** "If you control the Imperial Seat at Cleanup & Checks, gain +1 VP."

**Add (First Playable rule):**

> **Coronation Rite:** At Cleanup & Checks, if you control the Imperial Seat **and** your Lord unit is in the Seat hex, score **1 VP** (max once per round). Track total Rites scored. The **third** Rite you score awards an additional **+2 VP** (once per game). VP from Rites are permanent.

Expected total: up to 3×1 + 2 = **5 VP** from Seat play (vs up to unbounded drip today if hold is uninterrupted).

### 3.3 AL-5 — Objective timing (`Victory.md`)

> Public and secret objectives score at **Cleanup & Checks** when the condition is met. Each card scores **once per player per game**. No claim action.

### 3.4 AL-1 / AL-4 — Population (`Population.md` + packet §3.3)

> **Population Cap** = 7 base + City/building bonuses (10 with one home City). **Population Pool** = available capacity; starting units occupy Population (default: **6** available, **4** in units).

---

## 4. Propagation checklist (MVP minimum)

| Doc | Change |
|-----|--------|
| `rules_and_systems/Victory.md` | AL-5 timing; Coronation Rite §5; VP permanence line; shared public pointer |
| `playtest/First_Playable_Packet.md` | §3.2 Rite; §3.3 population; §4.4 shared row setup |
| `playtest/Ambiguity_Ledger.md` | AL-1, AL-4, AL-5 → **Resolved** with pointers |
| `rules_and_systems/Population.md` | Base cap 7 formula |
| `playtest/Balance_Dashboard.md` | Add MVP budget target row |
| `sim/` engine | Shared row, Rite scoring, updated cleanup |
| `sim/tests/` | Golden replays regenerated after engine change |

**Defer in this pass:** `Objectives.md` full deck, `Artifacts.md`, `Buildings.md` VP, `High_Council.md`, `rulebook/*` (unless doing atomic sweep in same PR).

---

## 5. Sim implementation notes

**`engine/setup.py`:** Build shared public row (2 revealed + deck); per-player secret only.

**`engine/objectives.py`:** Track `shared_row: list[str]`, `shared_scored: dict[player, set[objective]]`.

**`engine/cleanup.py`:** Replace Seat drip with Rite check (control + lord on hex); increment `rite_count`; award +2 on third rite once.

**`engine/observations.py`:** Expose shared row to all players.

**Persona `features.py`:** Score toward visible shared objectives, not only personal card.

**Regression:** MVP encode validated by sim brackets (winner objective share ~68–72%); current post-M2 baselines live in `docs/reports/INDEX.md`.

---

## 6. Execution sequence (agreed)

### Week 1

1. **Canon pass** — AL-5, AL-1, AL-4 + Coronation Rite + shared row in `Victory.md` / First Playable packet (~1 session)
2. **Plan 1 human step 0** — baseline solo session; log combat metrics to `session_log.csv`
3. **Sim MVP encode** — shared row + Rite + ledger-aligned population
4. **Bracket A re-run** — 1,000 games; check MVP metrics table §2

### Week 2

5. **Plan 1 step 1** — Aggressor's Edge in docs + sim variant flag
6. **100-game Warmonger bracket** — lord capture still 10–25% of winner VP?
7. **First 4p human session** — threat-legibility probe ("who's closest to winning?")

---

## 7. Kill criteria

| Signal | Response |
|--------|----------|
| Winner objective share still &lt;40% after MVP | Reveal 3 publics at setup; bump public VP to 3 per card (playtest only) |
| Nobody contests Seat after Rite | Drop Lord-presence requirement; keep announced 1 VP |
| Lord capture &gt;30% of winner VP consistently | Plan 1 only — do not cut capture VP; buff shared objective scoring rate |
| Shared row homogenizes all strategies | Add 2 more cards to row or restore one personal public (Charters lite) |

---

## 8. Out of scope for this MVP doc

- Plan 2 (AP economy)
- Milestone 2 Council / Strategy cards
- Full Plan 3 atomic 10-file sweep
- LLM playtest agents
