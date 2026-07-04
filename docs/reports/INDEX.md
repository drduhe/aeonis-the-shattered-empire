# Sim reports — index

**Updated:** 2026-07-03 · Sim-only unless noted. Full tournament dumps are **regenerable** — conclusions live in the memos below.

**Engine:** M3 card systems + Lever C brakes + S1 seat VP. **236 pytest** passing.

---

## Conclusions (read these)

| Doc | What it answers |
| --- | --- |
| [Current baselines](2026-07-03-current-baselines.md) | Active configs, headline metrics, regenerate commands |
| [H7 calibration sweep](2026-07-03-h7-calibration-sweep-conclusion.md) | Expander dominance fix (C+S1); Levers A/B killed |
| [Early economy sweep](2026-07-03-early-economy-sweep-conclusion.md) | E1/E2/E3/E5 killed — single-knob easing fails |
| [12 VP pacing memo](2026-07-03-vp12-pacing-memo.md) | VP threshold 12 stretches rounds but kills economist lift |
| [Economist viability memo](2026-07-03-memo-economist-viability.md) | Owner decision: stop bot tuning; packet levers |
| [Persona parity diagnosis](2026-07-03-persona-parity-diagnosis.md) | Bot vs design-pressure methodology |
| [Plan 1 combat ladder](2026-07-03-plan1-combat-ladder.md) | Edge/Pillage variants; Pre-Strike for human test |

---

## CI / regression (no stored reports)

- `regression-plan1-baseline.json`, `regression-plan1-prestrike.json`
- `regression-plan2-baseline.json`, `regression-plan2-cap-rally.json`
- `bracket-m2-ci.json`, `bracket-m3-ci.json`

Local: `cd sim && python scripts/regression_check.py --config configs/<config>`

---

## Removed artifacts (2026-07-03 cleanup)

Per-bracket tournament snapshots, one-off experiment configs (lever-a/b, seat-sweep, early-economy, legacy bracket-a/b/c), and pre-M3 baselines removed. Conclusions preserved in the docs above; recover deleted files via `git log --diff-filter=D --summary -- docs/reports/` or `sim/configs/`.
