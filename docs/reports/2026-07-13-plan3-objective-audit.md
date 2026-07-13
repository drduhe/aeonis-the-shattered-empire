# Plan 3 — 24-card Public Objectives audit

**Date:** 2026-07-13 · **Sim-only** · Mixed personas + full M4 Lord asymmetry  
**Configs:** `bracket-plan3-objectives-{4,6,8}p.json`  
**Games:** matched reduced-row baseline vs audited deck: 50 (4p) / 40 (6p) / 40 (8p) per variant; 260 total  
**Script:** `sim/scripts/plan3_objective_audit_ladder.py`

## Verdict

**Promote the audited 24-card public deck and full-game shared-row contract.** All primary gates pass:

| Players | Reduced-row mean rounds | Audited mean rounds | Reduced winner objective share | Audited winner objective share | Completed |
|---:|---:|---:|---:|---:|---:|
| 4 | 6.02 | **6.30** | 82.7% | **74.1%** | 50/50 |
| 6 | 5.88 | **6.83** | 76.4% | **81.9%** | 40/40 |
| 8 | 5.98 | **6.33** | 80.3% | **76.9%** | 40/40 |

- Audited pacing stays inside the accepted **6–8 round** band at every count; at 6p/8p it corrects the matched reduced row's sub-6 mean.
- Winner objective share stays above the Plan 3 **60%** floor at every count.
- Every sim-compatible public card except `Hold the Line` scored at least once across the audit. `Hold the Line` remains a human-playtest watch because the current bots do not model defensive intent well; `Archmage` was correctly excluded because First Playable enables Tier I only.
- No crashes, timeouts, or degenerate verdicts occurred.

## Audit changes

1. Full-game publics use the same shared-row contract as First Playable: reveal 2 Stage I at setup; reveal 1 per Round Start from round 2; mix Stage II into the remainder at Round Start of round 4; each player may score each card once, with a one-public-per-Cleanup limit.
2. Cumulative public progress begins only when the card is revealed and uses player-colored control markers. Earlier events do not count.
3. `Crossroads of Empire` replaces `Heir of Aeonis`, removing a redundant Imperial Seat reward.
4. `Hold the Line` replaces `Kingslayer`, removing another reward from the already-loaded Lord-capture loop and adding a defensive path.
5. `Council Power` and `Lawgiver` now reward successful participation, remaining viable under the proposed Plan 4 Docket.
6. `Merchant Lord` replaces `Realm of Plenty`. Ladder 1 found Realm effectively automatic: 340 scores across 60 revealed games.
7. `Prosperous Realm` replaces `Master of Cities`. The final canonical no-upkeep ladder produced **36 scores across 25 revealed games**, while Master of Cities recorded no scores at 4p/6p in the earlier ladders.

## Reachability watchlist

The final aggregate low-frequency cards are intentionally demanding Stage II goals:

| Card | Revealed games | Scores | Read |
|---|---:|---:|---|
| Hold the Line | 14 | 0 | Opponent-dependent defensive goal; keep on the human-playtest watchlist |
| Conqueror | 33 | 10 | Five post-reveal wins is a true late military goal |
| Reliquary | 25 | 9 | Three-Artifact ceiling is aspirational |
| Breaker of Walls | 22 | 5 | Siege availability is board-dependent |
| Living Legend | 22 | 4 | Legendary construction remains rare before game end |

Do not tune these together. If later evidence shows dead cards at the table, test one threshold at a time.

## Persona read

On the final canonical no-upkeep rebaseline, audited economist win rates were 2.4% (4p), 2.3% (6p), and 0.0% (8p). Balanced recorded 50.0%/19.2%/27.7%. The deck still passes its objective-share and pacing gates, but economist viability remains a cross-system watch rather than evidence for more objective changes; Lord tuning remains paused per the 2026-07-12 owner decision.

## Promotion scope

Promote the rules framing, all seven audit substitutions/rewrites, and simulator support. Keep conclusions labeled **sim-only** until human confirmation resumes. The First Playable reduced six-card row remains the teaching packet; `full_public_deck` is the full-game simulator mode, with `Archmage` excluded while Tier II is disabled.
