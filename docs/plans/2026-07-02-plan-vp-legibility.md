# Plan 3: VP Legibility & Consolidation

- **Status:** **PROMOTED 2026-07-13 (sim-validated)** — shared full-game row, audited 24-card deck, permanent score-once VP, Coronation Rite, purchased-VP removal, and event budget are registered in `rules_and_systems/INDEX.md`. Human confirmation remains pending.
- **Date:** 2026-07-02
- **Owning docs:** `rules_and_systems/Victory.md` (VP budget), `rules_and_systems/Objectives.md` (objective mechanics)
- **Related plans:** Plan 1 (military VP), Plan 2 (Rally valve reads VP), Plan 6 (Renown/title overlap)

---

## 1. Problem

The VP economy has **8+ scoring streams**: personal public objectives, secret objectives, Lord-specific objectives, Council Titles, Imperial Seat drip (+1/round, +2 for 3-round hold), while-held VP (4 artifacts, Legendary Buildings), Lord-capture VP, event VP, purchasable VP (5 Influence → 1 VP; 10 Gold → 1 VP), and secret endgame scoring.

Three concrete failures:

1. **Threat illegibility.** Public objectives are *personal* — each player races their own revealed card. To know who's about to win, you must track up to 8 different public cards, hidden secrets, drip income, and held assets. TI4's shared public objectives make the race legible at a glance; Aeonis currently doesn't.
2. **Anticlimax risk.** Drip sources (Seat +1/round, held-asset VP "checked at Cleanup") can quietly push someone over 10 VP with no dramatic play. The endgame can trigger from accounting.
3. **Ambiguity.** `Victory.md` says artifacts are "worth 1 VP **while you control it** (checked at Cleanup & Checks)" and Legendary Buildings "worth 2 VP (checked at Cleanup & Checks)... the captor gains control and its VP." It is undefined whether VP already counted are **lost** when the asset is lost. If yes: the score can go down, "first to 10" needs re-checking every round, and the tracker becomes a spreadsheet. If no: holding an asset one round mints permanent VP, which is worse.

Also, purchased VP (buy 1 VP for 5 Influence / 10 Gold) converts economy directly into win condition — historically feel-bad and warping.

## 2. Goals / Non-goals

**Goals**

1. Objectives are the spine: **≥ 60%** of a typical winner's 10 VP comes from objective cards (public + secret + Lord).
2. Any player can assess "who is threatening to win" in under ~30 seconds of looking at the table.
3. **VP never go down.** Scored VP are permanent; assets grant scoring *moments*, not held totals.
4. The endgame triggers on plays, not drips.

**Non-goals**

- Secret-objective redesign remains out of scope. The public audit keeps 24 cards but replaces four cards whose incentives or reachability failed the shared-row contract.
- Not removing the Imperial Seat as a VP source — it's the thematic centerpiece.
- Not changing the 10 VP threshold / final-round structure until data says otherwise.

## 3. Key decisions

### D1 — Shared vs. personal public objectives → **Shared (TI4-style), with a personal-draw variant retained**

Convert the Stage I/II public deck from personal draws to a **shared revealed row**:

> During setup, reveal **2 Stage I** public objectives. At each Round Start from Round 2, reveal 1 more (Stage I through Round 3, Stage II from Round 4 — reusing the existing staging rule). Every revealed public objective can be scored by **every player, once each**, during Cleanup & Checks (limit: **1 public objective scored per player per round**).

- Buys: shared race tension, at-a-glance legibility (the row + each player's scored markers = the whole public race), natural pacing rhythm.
- Costs: less per-player variety. Mitigation: keep the current personal-draw rules in `Objectives.md` as a **variant** ("Charters variant") rather than deleting them.
- Card audit needed: ~6 of the 24 public cards were written assuming a single owner ("*your* Legendary Building"); reword to player-relative form. Content survives.

### D2 — VP permanence → **Scored VP are never lost**

New canon line in `Victory.md`:

> **VP are permanent.** Once scored, VP are never removed, even if the source (hex, artifact, building, title) is later lost.

Consequences for each while-held source:

| Source | Current | New |
|---|---|---|
| Legendary Building | "worth 2 VP (checked at Cleanup)", captor "gains its VP" | **Score 2 VP once, on construction.** If captured, the captor scores **1 VP once** (per building, per game) — conquest moment, no VP transfer bookkeeping |
| VP artifacts (Crown, Eternal Forge, Shard, Imperial Seal) | 1 VP while held | **1 VP once, when first gained**; stealing it scores the thief 1 VP once. Cap: a given artifact can award VP to at most 2 players per game |
| Imperial Seat | +1 VP/round drip + 2 VP for 3-round hold | See D3 |
| Titles | VP while held (implied) | Score once on claim; losing the title doesn't refund |

### D3 — Imperial Seat: from drip to public event → **Coronation Rite**

Replace the per-round drip with a visible, interactive scoring moment:

> **Coronation Rite:** At Cleanup & Checks, if you control the Imperial Seat **and** your Lord unit is in the Seat hex, score **1 VP** (max once per round, announced aloud). If you have scored the Rite in **3 total rounds** (not necessarily consecutive), additionally score 2 VP — once per game.

Same expected VP as today, but it requires the Lord's body on the throne (attackable, visible, dramatic) and announces itself.

### D4 — Cut purchased VP → **Remove both**

Delete "5 Influence → 1 VP" and "10 Gold → 1 VP" from `Victory.md`. Council motions may still award VP as *motion effects* (that's politics, not purchase). Audit the agenda deck in `High_Council.md` §6a for any buy-a-VP motion and rework to Renown or objective-progress rewards.

### D5 — Event VP → **Cap, don't cut**

Keep event-driven VP (they're dramatic by nature) but audit `Events.md` full decks with a budget: **no single event awards more than 1 VP**, and the decks together should not be able to award more than ~2 VP to one player per game in expectation.

## 4. The VP budget (design target)

A typical 10 VP winner, by design intent:

| Source | Target VP | Share |
|---|---|---|
| Shared public objectives | 3–4 | ~35% |
| Secret objectives (cap 3 held) | 2–4 | ~30% |
| Lord-specific objectives | 1–2 | ~15% |
| Coronation Rite / military (capture) / artifacts | 1–3 | ~20% |
| Titles | 0–2 | ~10% |

`Balance_Dashboard.md` already has a VP-source distribution tracker — this table becomes its target row.

## 5. Rule-text changes and propagation checklist

| Doc | Change |
|---|---|
| `rules_and_systems/Victory.md` | Rewrite §1 (shared publics), §4 (asset scoring, D2 table), §5 (Coronation Rite); delete Purchased Points; add "VP are permanent" |
| `rules_and_systems/Objectives.md` | §1.1/§3: shared-row draw/score rules; demote personal draws to "Charters variant"; reword ~6 owner-assuming cards |
| `rules_and_systems/High_Council.md` | Titles score-once wording; agenda-deck audit for purchased VP |
| `rules_and_systems/Buildings.md` | Legendary Building VP wording |
| `rules_and_systems/Artifacts.md` | 4 VP-artifact entries → score-once wording |
| `rules_and_systems/Events.md` | VP audit per D5 |
| `rules_and_systems/Renown.md` | No change; cross-check secret-objective Renown bonus still coherent |
| `playtest/First_Playable_Packet.md` | §4.4 objective setup → shared row (6 public cards support it: reveal 2 + 1/round works) |
| `rulebook/Learn_to_Play.md`, `rulebook/Player_Aid.md` | Scoring sections and VP-source table |
| `playtest/Balance_Dashboard.md` | Add §4 budget as target distribution |

## 6. Playtest validation

**Metrics:**

- VP-source distribution of the winner vs. the §4 budget.
- **Threat-legibility probe:** mid-game, ask each player "who is closest to winning?" — target ≥ 75% correct.
- Rounds to game end — target **6–8** with the shared-row pacing (updated 2026-07-12; superseded prior 8–10 aspirational band).
- "Surprise wins" (players report not seeing the win coming) — target ~0.

**Kill criteria:**

- If shared publics homogenize strategy (everyone chases the same 2 cards), reveal 3 at setup and widen card variety per stage.
- If the Coronation Rite makes the Seat a death-trap nobody contests, drop the Lord-presence requirement but keep the announcement.

## 7. Risks

- Largest doc blast radius of the six plans (10 files). Do it as one atomic sweep per the canon-propagation rule — a half-applied D1 is worse than none.
- D1 changes the *content assumptions* of the objective decks; budget one focused re-read of all 24 public cards.

## 8. Sequencing

**Executed 2026-07-13.** Final integrated M4 ladders completed 130/130 audited games at 6.33–6.73 mean rounds with 74–80% winner objective share. See `../reports/2026-07-13-plan3-objective-audit.md`.
