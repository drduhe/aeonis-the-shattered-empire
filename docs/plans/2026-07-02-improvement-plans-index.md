# Aeonis Improvement Plans — Index & Sequencing

- **Date:** 2026-07-02
- **Status:** All six plans PROPOSED. Nothing in them is canon until playtested and locked in `rules_and_systems/INDEX.md`.
- **Origin:** post-burn-down design review (see `2026-07-02-aeonis-design-roadmap.md` for the executed roadmap these follow).

## The six plans

| # | Plan | Core move | Test cost |
|---|---|---|---|
| 1 | [Combat aggression](2026-07-02-plan-combat-aggression.md) | Aggressor's Edge (attacker wins ties) + Pillage + Engaged state | Solo, today |
| 2 | [AP economy](2026-07-02-plan-ap-economy.md) | +2 AP bonus cap from all sources + Rally catch-up valve | Solo, after Plan 1 ladder |
| 3 | [VP legibility](2026-07-02-plan-vp-legibility.md) | Shared public objectives, permanent VP, Coronation Rite, cut purchased VP | Solo + group |
| 4 | [High player count](2026-07-02-plan-high-player-count.md) | Council Docket (2 items/round), Whisper draw scaling, new `Map_Construction.md` | Needs 6p/8p tables |
| 5 | [Core Lords parity](2026-07-02-plan-core-lords-parity.md) | Signature bar + 6 redesign briefs (Seraphel, Cassian, Elyndra, Vharok, Auriel, Rakhis) | Head-to-head pairs |
| 6 | [Bookkeeping](2026-07-02-plan-bookkeeping.md) | Renown → milestone track, kill building upkeep, rewrite `Trade_Taxes.md`, player-board ledger | Hygiene parts free |

## Sequencing (dependency-driven)

1. **Now, no gate:** Plan 6 §3.3–3.4 (Trade rewrite, player-board spec) and Plan 4 §3.3 start (`Map_Construction.md` authoring) — pure hygiene/authoring, no balance risk.
2. **Playtest ladder A (solo):** Plan 1 baseline → Edge → Pillage. Combat frequency data unblocks everything downstream.
3. **Playtest ladder B (solo):** Plan 2 cap + Rally, then cost variants. Run Plan 6 §3.1–3.2 (Renown/upkeep) in this ladder — same compounding loop.
4. **Plan 3 sweep:** apply the VP frame once military VP frequency has stabilized (largest doc blast radius; one atomic sweep).
5. **Plan 5 batches:** Seraphel+Cassian anytime; Elyndra+Vharok and Auriel+Rakhis after Plan 1 locks.
6. **Plan 4 group gates:** Docket + draw scaling text lands early, but the 6-player and 8-player validation sessions are the last gate before `Production_Manifest.md` numbers freeze.

## Shared rules of engagement

- One variable per playtest ladder step; log every session in `playtest/session_log.csv` against `playtest/Balance_Dashboard.md`.
- Every adopted change propagates in one atomic sweep per the canon rule (owning chapter + all dependents + First Playable packet + rulebook + player aid).
- Each plan carries its own kill criteria — a rolled-back experiment gets recorded in its plan file, not silently dropped.
