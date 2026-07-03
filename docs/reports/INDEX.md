# Sim reports — index & current baselines

**Updated:** 2026-07-03 · Entry point for `docs/reports/`. Everything here is **sim-only** (persona bots, not humans) unless a report says otherwise.

**Engine state for current baselines:** M1 core loop + Plan 3 MVP + M2 politics + **M3 card systems** (Remnants/exploration, Artifacts/Sites, Arcane Tier I, secrets, Whispers, strategy primaries). 229 pytest passing.

---

## Current baselines (regenerated 2026-07-03, post-M3 gate)

| Report | Config | Games | What it answers |
|---|---|---|---|
| [Mixed 4p M3 baseline](2026-07-03-baseline-mixed-4p-m3.md) | `sim/configs/bracket-m2-smoke.json` | 100 | Full M3 fidelity: whispers/artifacts/research metrics; H1–H12 |
| [Solo 4p M3 ladder](2026-07-03-baseline-solo-4p-m3.md) | `sim/configs/bracket-m2-4p.json` | 200 | Pacing sanity per persona at M3 fidelity |
| [Mixed 4p pre-M3 baseline](2026-07-03-baseline-mixed-4p.md) | `sim/configs/bracket-m2-smoke.json` | 100 | Pre-M3 comparison (Merchant Lord only) |
| [Mixed 7p baseline](2026-07-03-baseline-mixed-7p.md) | `sim/configs/bracket-c-mixed.json` | 200 | High-count pacing (pre-M3 card systems) |
| [Mixed 8p baseline](2026-07-03-baseline-mixed-8p.md) | `sim/configs/bracket-b-mixed.json` | 600 | High-count persona parity (pre-M3) |
| [Solo 4p pre-M3 ladder](2026-07-03-baseline-solo-4p.md) | `sim/configs/bracket-m2-4p.json` | 200 | Pre-M3 solo ladder |

**Headlines (mixed 4p M3):** 100% completed · mean **5.8** rounds · economist **5.3%** (H12 killed) · expander 40.5% · H10 killed (1.3% forced whisper discards).

**Headlines (solo 4p M3):** 200/200 completed · see report for per-persona round length.

Regenerate after engine changes:

    cd sim && python -m aeonis_sim.runner.tournament --config configs/bracket-m2-smoke.json --report ../docs/reports/<date>-baseline-mixed-4p.md --workers 4

## Hypothesis scoreboard (mixed 4p baseline)

| ID | Hypothesis | Status | Read |
|---|---|---|---|
| H1 | Seat+streak >50% of all VP | **killed** | 9% — Coronation Rite fixed the drip |
| H2 | Winning margin >5 VP | **killed** | 3.2 VP avg, 7% runaway |
| H3 | Objectives ≥60% of winner VP | **killed** (goal met) | 74.8% |
| H4 | 7p timeouts are pacing | **killed** | 0% timeout at 7p (200 games, post-Merchant Lord) |
| H5 | Combat VP marginal even for Warmonger | inconclusive | 7.1% winner share |
| H6 | no_vp_progress is chaos artifact | **killed** | 0% degenerate |
| H7 | No persona dominates mixed seats | improving | Max persona 33.8% at 4p; balanced leads at 7–8p (~29%) |
| H8 | Economist viable in mixed seats | **4p met, 7–8p not** | 4p 6.4% · 7p 2.7% · 8p 1.8% (bar ≥5%) |
| H9 | Diplomat ≥3% mixed 4p | **killed** (goal met) | 21.6% (M3 baseline) |
| H10 | Whisper hands manageable | **killed** | 1.3% forced discard rate (M3) |
| H11 | First artifact round 3–4 | **killed** | Median round 3 (M3) |
| H12 | Economist ≥5% mixed 4p at M3 | **killed** (goal met) | 5.3% (M3 baseline) |

## Design memos & calibration (keep)

| Doc | Role |
|---|---|
| [Economist viability memo](2026-07-03-memo-economist-viability.md) | Owner decision memo: stop bot tuning; levers are Plan 3 pacing (8–10 rounds) + row composition. Checklist in §6 |
| [Persona parity diagnosis](2026-07-03-persona-parity-diagnosis.md) | Bot-artifact vs design-pressure methodology; pre/post-fix data; calibration stop rule |
| [Plan 1 combat ladder](2026-07-03-plan1-combat-ladder.md) | Edge/Pillage variant sweep; recommends Pre-Strike Edge for first human test |

## Regression gates (CI-enforced, no stored reports)

CI (`.github/workflows/sim.yml`) re-runs these every push — green means gates hold; stored snapshots add nothing:

- Plan 1/2: `sim/configs/regression-plan{1,2}-*.json` (4 bracket matrix)
- M2 gate: `sim/configs/bracket-m2-ci.json` (20 mixed 4p, zero crash/timeout/degenerate)
- M3 gate: `sim/configs/bracket-m3-ci.json` (20 mixed 4p, zero crash/timeout/degenerate)

Local check: `cd sim && python scripts/regression_check.py --config <config> --report <optional.md>`

---

## Removed reports (git history has full text)

Superseded snapshots removed 2026-07-03: M1-era bracket/persona HTML reports (2026-07-02), milestone-1 gate and playtest HTML, Plan B synthesis, MVP/parity/parity-v2 bracket generations, pre-Task-6 M2 gate/smoke/impact reports, and regression markdown snapshots. Their surviving conclusions:

- **M1 gate (2026-07-02):** engine crash-free at all counts; chaos-bot timeouts expected (no VP pursuit).
- **Plan B brackets:** H1 killed (seat drip dominated pre-MVP — motivated Plan 3 MVP), H5 killed, H6 killed.
- **MVP encode brackets:** winner objective share ~68–72% — Plan 3 MVP promoted to canon (see `rules_and_systems/INDEX.md`).
- **Parity v2 (7–8p):** expander tamed at 8p via full-roster mixed matchmaking; economist <1% at 7–8p (H8 origin).
- **M2 gate (pre-negotiation):** 100/100 smoke, solo 200/200, CI 20/20 — gate recorded in `docs/plans/INDEX.md`.

Recover any file: `git log --diff-filter=D --summary -- docs/reports/`
