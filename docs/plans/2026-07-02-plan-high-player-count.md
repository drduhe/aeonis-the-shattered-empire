# Plan 4: High Player Count Scaling (6–8)

- **Status:** **PARTIAL 2026-07-13** — map geometry and the 91-tile 8p inventory are sim-validated/promoted for First Playable; Docket, Whisper scaling, and slice drafting remain PROPOSED pending humans.
- **Date:** 2026-07-02
- **Owning docs:** `rules_and_systems/High_Council.md` (council throughput), `rules_and_systems/Whispers.md` (deck scaling), **new** `rules_and_systems/Map_Construction.md` (to be created)
- **Related decisions:** 3–8 player support is **LOCKED** (`marketing/Positioning.md`). This plan is about *delivering* it, not relitigating it.

---

## 1. Problem

Everything is currently tuned at 3–4 players. Three systems break structurally at 6–8:

1. **Council throughput is O(players).** `High_Council.md` §3.2 allows one motion per player per round, plus the agenda-deck reveal. At 8 players: up to **9 votable items per round, every round**, each with negotiation and lobbying. TI4 caps agendas at 2 per agenda phase — and only after Mecatol falls. Aeonis's council could add 30–60 minutes per round at high counts.
2. **The Whisper economy cycles too fast.** Every player draws 2 at Round Start (`Whispers.md` §2), plus 1 per VP scored. At 8 players that's **16+ cards/round** from a 44-card full-game deck — full deck cycling every ~2.5 rounds, making "one-of" cards like Sabotage ubiquitous and draws samey.
3. **There is no map-construction system at all.** No tile counts per player count, no layout diagrams, no slice-balance rules, no guaranteed distances. TI4 dedicates an entire subsystem (slice building/drafting) to this; it's a prerequisite for the game existing at any count, and doubly so at 7–8.

Secondary: real-time pacing (downtime between turns is fine — single-action rotation is short — but council and 2-player battles stall the other 6).

## 2. Goals / Non-goals

**Goals**

1. High Council Phase ≤ **15 minutes** at 8 players.
2. Whisper deck cycles no faster than once per **4 rounds** at any player count.
3. A written, reproducible map setup for each count 3→8 with slice-balance guarantees.
4. A tested 6-player game and a tested 8-player game before any component counts are locked for manufacturing (`components/Production_Manifest.md`).

**Non-goals**

- Not changing the council's voting math (votes, lobbying) — only throughput.
- Not redesigning Whisper card content.
- Not deciding retail SKU packaging (base box vs. 7–8 expansion) — that's a business call for `marketing/Campaign_Math.md` once component counts exist; the 3–8 commitment stands either way.

## 3. Recommended design (spec)

### 3.1 Council throughput: the Docket

Replace "everyone may propose" with a fixed-size docket:

> **The Docket:** Each High Council Phase votes on at most **2 items**:
> 1. The **agenda-deck reveal** (Speaker flips the top card; it is always voted on — no longer optional to propose).
> 2. **One player motion.** During the proposal window, each player may **bid Influence** to place their motion on the docket (secret simultaneous bid, or open ascending — playtest both). Highest bid pays and proposes; ties broken by the Speaker. All other bids are returned.
>
> At 3–5 players, the docket may instead hold **two player motions** (bid winner and runner-up, each paying their own bid).

- Influence gets a meaningful sink (Plan 6 cares about this), motion slots become scarce and political, and phase length is constant in player count.
- The 1-Influence flat proposal cost is deleted; the bid replaces it.
- Existing "propose for free" effects (Whispers, Lord abilities, Ozren's kit) become **docket-jump effects**: "your motion is added to the docket without bidding" — audit each.

### 3.2 Whisper scaling: draw rate by player count

Keep one shared deck (it's a physical product constraint) and scale the *draw*, not the deck:

| Players | Round Start draw | Expected cards/round (incl. ~1 VP draw/player/2 rounds) |
|---|---|---|
| 3–5 | 2 each | 8–13 |
| 6–8 | **1 each** | 9–14 |

Plus: hand limit stays 7; the "draw 1 when you score VP" rule is untouched (it rewards the thing we want rewarded). If 6–8p draws feel starved in testing, the fallback is a second printed copy of the 44-card deck shuffled in at 7–8p (component cost noted in `Production_Manifest.md`) — draw-rate reduction is the zero-cost first attempt.

### 3.3 Map construction: new chapter `Map_Construction.md`

Create the owning chapter with:

1. **Slice system:** each player receives a **home slice** — home City tile + 5 surrounding tiles drawn from a curated pool (fixed composition: 1 resource-strong, 1 Ruins-or-Portal, 2 standard terrain, 1 open). Slices are laid around a **shared core**: the Imperial Seat hex plus a ring of contested high-value tiles.
2. **Per-count geometry table:** map radius, total tile count, slices, and core-ring size for each count 3–8. Constraints: every home City is ≥ 4 hexes from any other home City and ≤ 4 hexes from the Imperial Seat's ring at every count.
3. **Balance guardrails:** each slice's total printed production within ±1 resource of every other slice; every slice touches at least one Ruins or Portal within 2 hexes of home.
4. **Setup modes:** (a) **Preset layouts** (diagrams, First Playable default), (b) **Slice draft** (deal 2 slices, pick 1 — the experienced-group mode).
5. **Tile inventory audit:** current `Components.md` counts (8 City tiles etc.) were scaled for 4p; the geometry table will produce the true manufacturing counts per count — feed `Production_Manifest.md`.

### 3.4 Real-time pacing guardrails (rulebook guidance, not rules)

- Production & Upkeep and Cleanup resolve **simultaneously** by default at 5+ players (already permitted; make it the stated default).
- Battles between two players run on a **2-minute negotiation clock** at 6+ players (guidance box in `Learn_to_Play.md`).

## 4. Rule-text changes and propagation checklist

| Doc | Change |
|---|---|
| `rules_and_systems/High_Council.md` | §3.2 rewritten to the Docket; §3.2a agenda card always votable; audit free-propose effects |
| `rules_and_systems/Whispers.md` | §2 draw-rate table by player count |
| `rules_and_systems/Map_Construction.md` | **New chapter** (§3.3 scope) |
| `rules_and_systems/Tiles.md` | Cross-reference Map_Construction for setup; no rule changes |
| `rules_and_systems/INDEX.md` | Register new chapter |
| `content-manifest.json` | Add Map_Construction.md |
| `playtest/First_Playable_Packet.md` | Point setup at the 3–4p preset layouts |
| `components/Components.md`, `components/Production_Manifest.md` | Tile counts from the geometry table; possible second Whisper deck at 7–8p |
| `rulebook/Learn_to_Play.md`, `rulebook/Player_Aid.md` | Setup section, council procedure, pacing boxes |
| `lords/*.md` (esp. `Ozren.md`), Whisper/agenda content | Docket-jump audit for propose-related effects |

## 5. Playtest validation

This plan needs **bodies at the table**; solo testing only validates §3.3 geometry.

**Milestones:**

1. **DONE 2026-07-13:** geometry table validated across 200 seeds per count (1,200 maps); corrected angular anchors and special access encoded; combat rebaseline green at 6p/8p.
2. **6-player session** with Docket + reduced draws: measure council phase length (target ≤ 15 min), round length, downtime complaints.
3. **8-player session**: same metrics plus map claustrophobia check (hexes per player, expansion room through round 4).

**Metrics:** council minutes per round; motions bid vs. walked away; Whisper deck reshuffle round; per-player hex count at rounds 3/6; session VP pacing vs. 3–4p baseline.

**Kill criteria:**

- Docket bidding stalls the phase (analysis paralysis on bids) → replace with rotating "docket seat" (round-robin right to propose, no bid).
- 8p map at feasible tile counts leaves < 8 hexes/player → this is the data that forces the 7–8-as-expansion SKU conversation; escalate to Campaign_Math rather than shrinking slices below playability.

## 6. Risks

- Docket is a significant political-feel change at *all* counts, not just 6–8 — it must be tested at 4p too (it likely *improves* 4p pacing, but verify).
- Map_Construction is the largest single authoring lift left in the project; it gates manufacturing numbers, so it can't slip behind the Kickstarter quote timeline in `marketing/Development_Plan.md`.

## 7. Sequencing

The Docket and Whisper draw-rate can be written immediately (small text changes). `Map_Construction.md` should start now in parallel with Plans 1–3 playtesting, because everything manufacturing-related waits on its geometry table.
