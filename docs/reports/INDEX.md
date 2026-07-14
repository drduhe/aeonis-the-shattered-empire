# Sim reports — index

**Updated:** 2026-07-13 · Sim-only unless noted. Full tournament dumps are **regenerable** — conclusions live in the memos below.

**Engine:** M3 card systems + full M4 Lord asymmetry (default-on) + audited objectives + validated map geometry + Lever C brakes + S1 seat VP + M5 qualitative agent layer. **357 pytest** passing.

---

## Conclusions (read these)

| Doc | What it answers |
| --- | --- |
| [Current baselines](2026-07-03-current-baselines.md) | Active configs, headline metrics, regenerate commands |
| [H7 calibration sweep](2026-07-03-h7-calibration-sweep-conclusion.md) | Expander dominance fix (C+S1); Levers A/B killed |
| [Early economy sweep](2026-07-03-early-economy-sweep-conclusion.md) | E1/E2/E3/E5 killed — single-knob easing fails |
| [12 VP pacing memo](2026-07-03-vp12-pacing-memo.md) | VP threshold 12 stretches rounds but kills economist lift |
| [Economist viability memo](2026-07-03-memo-economist-viability.md) | Owner decision: stop bot tuning; packet levers |
| [8p economist diagnosis](2026-07-13-economist-8p-diagnosis.md) | Full audited deck vs six-card row; objective access is primary, Thal'rik fit amplifies; no economy knob promoted |
| [Persona parity diagnosis](2026-07-03-persona-parity-diagnosis.md) | Bot vs design-pressure methodology |
| [Plan 1 combat ladder](2026-07-03-plan1-combat-ladder.md) | Edge/Pillage variants; Pre-Strike for human test |
| [Plan 1 Pre-Strike mixed (M4)](2026-07-13-plan1-prestrike-mixed.md) | Mixed 4/6/8p baseline vs pre_strike; **do not promote**; 4p near band, 6–8p still hot |
| [Plan 3 Public Objectives audit](2026-07-13-plan3-objective-audit.md) | 24-card shared-row audit; 130/130 complete; 6.33–6.73 rounds; **promote** |
| [Plan 4 geometry + Plan 1 spacing](2026-07-13-plan4-geometry-spacing.md) | 1,200-map gate; fixes clustered homes; 6p/8p attacker heat enters band; 91-tile BOM |
| [Plan 2 AP + Plan 6 bookkeeping](2026-07-13-plan2-plan6-tempo-bookkeeping.md) | 910-game ladder; reject AP cap/Rally and slim Renown; promote no-building-upkeep |
| [Plan 5 / M4 foundation](2026-07-09-plan5-m4-foundation.md) | Six signature redesigns promoted; 40/40 stability smoke; full M4 entry scope |
| [M4 full encode gate](2026-07-12-m4-gate.md) | 100/100 completed; unique tiles, abilities, discoveries, Legendaries; AL-49 closed |
| [Post-M4 rebaseline + pacing](2026-07-12-m4-rebaseline.md) | M4-on 4/6/8p mixed; economist H8 pass at 6–8p; Lever A → design for **6–8 rounds** (accepted) |
| [M4 Lord × persona sweep](2026-07-12-m4-lord-persona-sweep.md) | Historical pre-Dial-3 sheet/persona signals; superseded default decision, retained tuning context |
| [M4 default-on review](2026-07-13-m4-default-on-review.md) | 520/520 matched canonical-stack games; promote M4 default-on; preserve explicit neutral regression path |
| [Synchronization + PnP readiness sprint](2026-07-13-pnp-readiness-sprint.md) | Canon/derived-doc synchronization plus the 45-page, 109-card First Playable print-and-play kit |
| [M5 deterministic pipeline](2026-07-13-m5-agent-playtest-dry-run.md) | Two-game, six-seat orchestration dry run; validates artifacts but contains no qualitative evidence |
| [M5 local-model pilot](2026-07-13-m5-agent-playtest-ollama-pilot.md) | Three-persona qualitative pilot with reliability, sampled decisions, reflections, and interviews |
| [Rakhis ladder Dial 1](2026-07-12-rakhis-ladder-dial1.md) | Oasis Cavalry −1 Gold removed; solo ~51%→49.5% — weak lever; Dial 2 = Hit and Run |
| [Rakhis ladder Dial 2](2026-07-12-rakhis-ladder-dial2.md) | Hit and Run once/game; solo ~48.5%; warmonger 85%→60%; Dial 3 = Sandstride |
| [Rakhis ladder Dial 3](2026-07-12-rakhis-ladder-dial3.md) | Sandstride ZOC ignore removed; solo 43%; mixed 4p 27.5%; first real lever |
| [Rakhis ladder Dial 3b](2026-07-12-rakhis-ladder-dial3b.md) | Pre-Pre-Strike retreat cut **tried and reverted** (regressed vs Dial 3) |

---

## CI / regression (no stored reports)

- `regression-plan1-baseline.json`, `regression-plan1-prestrike.json`
- `regression-plan2-baseline.json`, `regression-plan2-cap-rally.json`
- `bracket-m2-ci.json`, `bracket-m3-ci.json`

Local: `cd sim && python scripts/regression_check.py --config configs/<config>`

---

## Removed artifacts (2026-07-03 cleanup)

Per-bracket tournament snapshots, one-off experiment configs (lever-a/b, seat-sweep, early-economy, legacy bracket-a/b/c), and pre-M3 baselines removed. Conclusions preserved in the docs above; recover deleted files via `git log --diff-filter=D --summary -- docs/reports/` or `sim/configs/`.
