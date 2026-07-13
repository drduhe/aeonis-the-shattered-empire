# Plan 1 — Pre-Strike Edge mixed ladder (M4-on)

**Date:** 2026-07-13 · **Sim-only** · Mixed personas + full Lord asymmetry  
**Configs:** `bracket-plan1-baseline-mixed-{4,6,8}p.json` vs `bracket-plan1-prestrike-mixed-{4,6,8}p.json`  
**Games:** 50 (4p) / 40 (6p) / 40 (8p) · matched seed bases · script `sim/scripts/plan1_prestrike_mixed_ladder.py`

Plan 1 target band (design): contested attacker win **~55–65%**. Prior warmonger-solo ladder (2026-07-03) was far hotter; this is the mixed M4-on check.

| Players | Edge | Attacker win % (all) | Contested attacker % | Battles / player-round | Mean rounds |
|---|---|---|---|---|---|
| 4 | off | 80.6% | **67.6%** | 0.252 | 6.94 |
| 4 | pre_strike | 79.0% | **64.9%** | 0.239 | 6.88 |
| 6 | off | 85.1% | **72.0%** | 0.229 | 7.38 |
| 6 | pre_strike | 86.4% | **74.3%** | 0.236 | 7.25 |
| 8 | off | 86.9% | **72.5%** | 0.303 | 7.45 |
| 8 | pre_strike | 85.5% | **70.0%** | 0.306 | 7.55 |

## Read

- **4p:** Pre-Strike cools contested attacker ~2.7 pp into the top of the Plan 1 band (~65%). Battle frequency does not rise.
- **6–8p:** Still **hot** (~70–74% contested) with or without Pre-Strike. At 6p Pre-Strike is slightly *worse* than off; at 8p it trims ~2.5 pp but stays above the band.
- Mean rounds stay in the accepted **6–8** pacing band under both modes.

## Recommendation (no canon change)

**Do not promote Pre-Strike Edge to default.** Keep Plan 1 PROPOSED / opt-in.

- Human-first experiment (when playtests resume): **4p Pre-Strike only** — only count where mixed bots land near the band.
- For 6–8p attacker heat: need a different lever (map spacing, Docket pacing, or a stronger Edge mitigator) — Pre-Strike alone is insufficient.

Elyndra Entangling Roots EV already treats Edge as main-strike-only (`aggressors_edge_mode == "full"`); Pre-Strike correctly does not inflate that peek. Collateral: `bump_renown(..., rng=None)` no longer raises during persona lookahead when Sacred Rite is owned (milestones skipped on peeks).

**Not canon** — Plan 1 remains PROPOSED in `docs/plans/INDEX.md`.
