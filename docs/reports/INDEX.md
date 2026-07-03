# Sim reports — index & current baselines

**Updated:** 2026-07-03 · Entry point for `docs/reports/`. Everything here is **sim-only** (persona bots, not humans) unless a report says otherwise.

**Engine state for current baselines:** M1 core loop + Plan 3 MVP (shared objective row, Coronation Rite) + M2 politics (events, strategy draft, initiative, council, structured negotiation) + persona parity fixes + **Merchant Lord row experiment** (PROPOSED sixth public, 8+ Gold). 165 pytest passing.

---

## Current baselines (regenerated 2026-07-03, post-Merchant-Lord)

| Report | Config | Games | What it answers |
|---|---|---|---|
| [Mixed 4p baseline](2026-07-03-baseline-mixed-4p.md) | `sim/configs/bracket-m2-smoke.json` | 100 | Persona balance under contention; council/event/strategy metrics; H1–H9 |
| [Solo 4p ladder](2026-07-03-baseline-solo-4p.md) | `sim/configs/bracket-m2-4p.json` | 200 | Pacing sanity per persona (win rate is 25% by construction); round length, VP mix |

**Headlines (mixed 4p):** 100% completed · mean 6.1 rounds · objectives 87.5% of all VP · contested attacker win 64.3% (inside Plan 1's 55–65% band) · council pass rate 28.8% · win rates: balanced 33.8%, expander 33.8%, warmonger 27.9%, diplomat 24.0%, economist 6.4%.

**Merchant Lord effect (same seeds, pre → post):** economist 2.5% → **6.4%** (crosses the ≥5% H8 direction bar), diplomat 12.8% → 24.0%, balanced 42.3% → 33.8%, warmonger 38.6% → 27.9%, expander 28.9% → 33.8%. Cost: mean rounds 6.4 → 6.1 mixed and 7.8 → 6.3 solo — an extra achievable public accelerates the race, moving further from the 8–10 round target (Lever A watch). Verdict at M3 gate via H12 (see plans INDEX).

Regenerate after engine changes:

    cd sim && python -m aeonis_sim.runner.tournament --config configs/bracket-m2-smoke.json --report ../docs/reports/<date>-baseline-mixed-4p.md --workers 4

## Hypothesis scoreboard (mixed 4p baseline)

| ID | Hypothesis | Status | Read |
|---|---|---|---|
| H1 | Seat+streak >50% of all VP | **killed** | 9% — Coronation Rite fixed the drip |
| H2 | Winning margin >5 VP | **killed** | 3.2 VP avg, 7% runaway |
| H3 | Objectives ≥60% of winner VP | **killed** (goal met) | 74.8% |
| H4 | 7p timeouts are pacing | inconclusive | needs 7p bracket rerun |
| H5 | Combat VP marginal even for Warmonger | inconclusive | 7.1% winner share |
| H6 | no_vp_progress is chaos artifact | **killed** | 0% degenerate |
| H7 | No persona dominates mixed seats | improving | Max persona 33.8% (balanced + expander tied), down from 42.3%; still above the ≤28% kill bar |
| H8 | Economist viable in mixed seats | **direction met (sim)** | 6.4% post-Merchant-Lord (bar: ≥5%); confirm at M3 gate (H12), human table later |
| H9 | Diplomat ≥3% mixed 4p | **killed** (goal met) | 24.0% |

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
