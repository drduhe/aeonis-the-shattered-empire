# Plan 6: Bookkeeping Reduction & Trade Chapter Rewrite

- **Status:** **RESOLVED 2026-07-13 — trade/player-board hygiene and no-building-upkeep promoted; slim Renown rejected.**
- **Date:** 2026-07-02
- **Owning docs:** `rules_and_systems/Trade_Taxes.md` (rewrite), `rules_and_systems/Renown.md` (threshold cleanup), player-board spec in `components/`
- **Related plans:** Plan 2 (Renown AP threshold), Plan 4 (Influence sink via Docket bids)

---

## 1. Problem

Players track **eight quantities**: Gold, Mana, Influence, Population, Remnants, Renown, AP, VP — refreshed through a Production & Upkeep phase, at up to 8 players, in a 4–10 hour game. Each currency is individually defensible, but the aggregate is a real table burden, and two specific spots are worse than burden:

1. **Renown does too many jobs.** It grants AP (+1 at 5), free actions (at 10), council votes (+1/+2), title eligibility, draft tiebreaks, and diplomacy flavor. It overlaps Influence conceptually (reputation vs. political capital) and is the engine of the leader-compounding problem Plan 2 attacks. Its bookkeeping cost (a second political track everyone must watch) exceeds its decision value.
2. **`Trade_Taxes.md` is the stalest chapter in the repo.** It allows trading "**Population points**" (population is a cap pool, not a currency — trading it is both thematically weird and mechanically undefined), references "**Trade Hubs**" granting income "within their region" (regions are not a rules term; the Market building in `Buildings.md` §Advanced does this job properly), names "**Arcane Forge**" where `Buildings.md` says Forge / Arcane Forge with different upkeep, and its building-maintenance section ("neglected buildings lose their effects or are downgraded") has **no defined downgrade procedure**.
3. **Upkeep micro-payments.** Forge and Academy each cost 1 Mana/round, Castle 2 Gold/round, Citadel of Iron 2 Gold/round, advanced units each with a listed upkeep. Every one is a per-round micro-transaction across every player, and the failure modes ("disabled or destroyed"?) are underdefined.

## 2. Goals / Non-goals

**Goals**

1. Production & Upkeep phase ≤ **5 minutes** at 6 players.
2. Every currency retains **one crisp identity** a new player can recite.
3. Zero underdefined economic rules (no "may be downgraded, depending on circumstances").
4. Physical mitigation: the player board does the remembering, not the player.

**Non-goals**

- Not merging Gold/Mana/Influence — the three-resource triangle is load-bearing (build/recruit vs. magic vs. politics) and maps to the tile system.
- Not removing Population (it is the anti-doomstack unit-cap engine) or Remnants (bounded, thematic, drives the Ruins/artifact loop).
- Not making trades non-binding — `Diplomacy.md` owns deal enforcement.

## 3. Recommended design (spec)

### 3.1 Slim Renown down to a milestone track

Renown keeps: earning rules, **title eligibility**, **draft tiebreaks**, diplomacy flavor, and VP-adjacent rewards. Renown loses its **passive per-round mechanical income**:

- **5 Renown:** ~~+1 AP; +1 Council vote~~ → **one-time reward**: draw 2 Whispers and gain 2 Influence (feels like fame arriving).
- **10 Renown:** ~~free 1-AP action; +1 vote~~ → **one-time reward**: score 1 VP and claim-eligibility for Hero of the Realm regardless of other prerequisites.
- Council votes become: **1 base vote + Lobbying** (Influence), full stop. Political weight is bought with the political currency — one system, one track. (This also absorbs Plan 2's threshold change and removes the tempo/votes double-dip.)
- The Renown *Decay* optional mechanic (`Renown.md` §Optional) is deleted — a decaying track multiplies bookkeeping for tension the capture/betrayal penalties already provide.

**Rejected alternative:** merging Renown into Influence entirely. Rejected because titles/tiebreaks need a non-spendable measure of standing; making them Influence-based would let players *buy* fame directly, which breaks the fiction and the draft tiebreak.

### 3.2 Kill per-round building maintenance; price it up front

- All building **Resource upkeep lines are removed** (Forge, Academy, Castle, Citadel of Iron). Build costs rise to compensate: +1 to +2 of the same resource, tuned per building (e.g., Castle 6 Gold → 8 Gold, Forge 5 Gold + 1 Mana/round → 6 Gold 1 Mana flat).
- Buildings are maintained by **Population capacity only** (already the stated default for basic buildings in `Buildings.md` — this makes it universal).
- **Advanced unit upkeep stays** (per `Advanced_Units.md` §4 — it's a deliberate cap on elite armies and has a clean failure rule: disband + refund Population). This becomes the *only* per-round upkeep in the game, which makes it teachable: "only fancy units eat gold."

### 3.3 Rewrite `Trade_Taxes.md` → `Trade.md` (scope cut + fixes)

The rewritten chapter contains only the trade system:

- **Tradeable:** Gold, Mana, Influence, Remnants, Utility Artifacts, hex control transfers, unit gifts (existing rules). **Population is removed from the tradeable list.**
- **Trade Hub section deleted**; the Market building (`Buildings.md`) and Cassian's kit own trade-economy effects. Portal 0-AP trades survive (clean, thematic, drives Portal value).
- **Upkeep/taxes section deleted** — §3.2 removes building upkeep; advanced-unit upkeep already lives in `Advanced_Units.md` §4. What remains of "taxes" (council tax laws) is owned by `High_Council.md` agenda content.
- Keep the file at the same path with a redirect note, or rename and update every cross-reference (9 files reference `Trade_Taxes.md`) — decide at execution; renaming is cleaner, redirect is safer for the Codex manifest.

### 3.4 Physical mitigation: the player board is the ledger

Add to the component spec (feeds `components/Components.md` + `Production_Manifest.md`):

- Player board tracks: Gold / Mana / Influence dials or tracks, Population pool wells, Renown track (0–10 with the two milestone boxes), AP tokens, and a **printed Production summary strip** ("at Production: collect per controlled tile + buildings — see your control markers").
- Design rule for all future content: **any recurring effect must be markable** (a token on a card/track), never memory-dependent. This is already the objectives-system standard (progress markers, `Objectives.md` §1.2) — generalize it to a repo-wide authoring rule in `INDEX.md`.

## 4. Rule-text changes and propagation checklist

| Doc | Change |
|---|---|
| `rules_and_systems/Renown.md` | §Thresholds one-time rewards; delete Decay; keep earning/tiebreak/titles |
| `rules_and_systems/High_Council.md` | §2.2 delete Renown bonus votes (base 1 + Lobbying); audit agenda cards referencing vote counts |
| `rules_and_systems/Actions.md` | Remove Renown AP mentions (coordinates with Plan 2's cap) |
| `rules_and_systems/Buildings.md` | Strip upkeep lines; raise build costs; universal "Population-maintained" statement |
| `rules_and_systems/Trade_Taxes.md` | Rewrite per §3.3 |
| `rules_and_systems/Advanced_Units.md` | §4 note: "the only per-round upkeep in the game" |
| `rules_and_systems/Population.md` | Cross-check building capacity statements |
| `rules_and_systems/INDEX.md` | Register decisions; add "recurring effects must be markable" authoring rule |
| `components/Components.md`, `components/Production_Manifest.md` | Player-board spec per §3.4 |
| `playtest/First_Playable_Packet.md`, `rulebook/Learn_to_Play.md`, `rulebook/Player_Aid.md` | Upkeep/vote/threshold text |
| Lord sheets | Audit: any Lord ability referencing Renown votes or building upkeep (Auriel's Divine Mandate survives — it earns Renown, doesn't spend votes) |

## 5. Playtest validation

**Metrics:**

- **Phase-length stopwatch:** Production & Upkeep minutes per round (target ≤ 5 at 6 players; measure before/after §3.2).
- **Rules-lookup count:** log every mid-game rules lookup in `session_log.csv`; economic lookups should drop measurably.
- **Forgotten-income audit:** count "oh wait, I forgot my X" moments per session — target ~0 after the player-board strip exists (proxy: printed crib sheet in PnP kit).
- **Renown relevance check:** titles still contested? draft tiebreak still fires? If Renown stops mattering entirely after §3.1, add one mid-track milestone (7 Renown: 1 Whisper) rather than restoring passive income.

**Kill criteria:**

- If removing building upkeep makes Castle/Citadel auto-builds, raise their build costs further or gate them (prerequisites), not upkeep.
- If base-1-vote councils feel flat (no vote asymmetry), reintroduce vote weight through *title effects only* (Hero of the Realm: +1 vote), keeping it visible and claimable rather than accruing silently.

## 6. Sequencing

§3.3 (Trade rewrite) and §3.4 (player-board spec) are pure hygiene — execute immediately, no playtest gate. §3.1 and §3.2 change balance; run them with Plan 2's ladder since they touch the same compounding loop (Renown AP + votes).

## 7. Execution record (2026-07-13)

The matched Plan 6 ladder completed **520/520 games** at 4p/6p/8p.

- **§3.2 promoted:** no-building-upkeep reduced the sim proxy from 0.21–0.28 checks per player-round to zero while preserving 2.46–2.66 builds per player-game and 6.22–6.63 mean rounds. Canonical up-front costs are Forge 6 Gold + 1 Mana, Academy 4 Gold + 4 Mana, Castle 8 Gold, and Iron Citadel 10 Gold + 2 Mana.
- **§3.1 rejected:** slim Renown did not materially improve action gaps, its 5-Renown reward fired for only 14–18% of seats, and the 6p economist fell from 7.9% to 2.3%.
- **§3.3/§3.4 remain landed:** `Trade_Taxes.md` is trade-only and player boards carry the printed production ledger.

See `../reports/2026-07-13-plan2-plan6-tempo-bookkeeping.md`.
