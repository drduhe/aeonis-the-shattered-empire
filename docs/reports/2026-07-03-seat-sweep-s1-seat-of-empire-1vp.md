# Seat sweep S1 — `seat_of_empire` 2→1 VP (sim-only)

**Date:** 2026-07-03 · **Sim-only** (PROPOSED; not canon)  
**Plan:** [Seat reward sweep](../plans/2026-07-03-plan-seat-reward-sweep.md) · **Stacked with:** [Lever C](2026-07-03-lever-c-expander-brake-m3.md) persona weights only (canon 10 VP, frontier 7 hex)  
**Knob:** `config["seat_rewards"]["seat_of_empire_vp"]` = **1** (canon 2)

---

## 1. Verdict

| Metric | Lever C only | S1 + Lever C | Interim bar |
| --- | ---: | ---: | --- |
| Expander win % | 20.0% | **20.5%** | ≤35% **Pass** |
| Balanced win % | **40.8%** | **29.3%** | — |
| Max persona | 40.8% (balanced) | **37.3% (warmonger)** | ≤28% **Fail** |
| Economist win % | 5.3% | **10.7%** | ≥5% **Pass** (H12) |
| Mean rounds | 5.8 | **6.3** | — |
| Seat VP share (all VP) | ~15.5%* | **10.5%** | Track |
| Solo parity | 25% each | 25% each | **Pass** |

\*Pre-S1 seat analysis at M3 persona weights; Lever C alone ~4.4% rite share.

**Bottom line:** S1 **fixes the balanced spike** left by Lever C (40.8% → 29.3%) while **holding expander at ~20%**. Spread improves; **warmonger** becomes max persona (37.3%). Strong candidate for PROPOSED packet promotion alongside Lever C bot weights — still sim-only until human playtest.

---

## 2. Mixed 4p detail (100 games)

Config: `sim/configs/seat-sweep-s1-4p-smoke.json` · seed_base 76000

| Persona | Lever C | S1 + Lever C |
| --- | ---: | ---: |
| expander | 20.0% | 20.5% |
| balanced | 40.8% | **29.3%** |
| warmonger | 31.0% | **37.3%** |
| diplomat | 28.0% | 28.6% |
| economist | 5.3% | **10.7%** |

### Read

1. **Balanced was seat-obj dependent** — cutting `seat_of_empire` from 2→1 VP disproportionately trims balanced’s seat-heavy wins (88% of balanced wins had end-seat control under S1).
2. **Expander stable** — lead brakes + less seat double-dip keeps expander ~20% without re-opening H7.
3. **Warmonger uptick** — military persona benefits from longer mean rounds (+0.5) and less seat-race closure; monitor before S2.
4. **Economist lift** — H12 margin widens (10.7%); pacing + less seat rush helps builder/gold paths.

---

## 3. Seat metrics (S1 JSONL)

| Signal | Value |
| --- | ---: |
| Global seat-related VP | **10.5%** of all VP (was ~15.5%) |
| Per-game avg seat VP | 2.96 (4 players) |
| Balanced end-seat hold | 50% of games |
| Expander end-seat hold | 20% |

Regenerate: `py -3.11 scripts/analyze_seat_rite.py <jsonl>`

---

## 4. Solo 4p (200 games)

Config: `sim/configs/seat-sweep-s1-4p-solo.json` · seed_base 77000

All personas **25.0%** · mean rounds **7.1** (vs 6.1 Lever C solo).

---

## 5. Sim encoding

- `GameState.seat_of_empire_vp` (default 2); `public_objective_vp()` in `objectives.py`.
- **232 pytest** passing.

---

## 6. Recommendation

| Action | Rationale |
| --- | --- |
| **Promote S1 + Lever C as sim default pair** | **Done** — `bracket-m2-smoke.json` + `bracket-m3-ci.json`; [re-baselined](../reports/2026-07-03-baseline-mixed-4p-m3.md) |
| **Defer S2** until warmonger ≤35% or owner scopes combo study | S2 (rite delay) may further stretch rounds |
| **Do not stack S1 + VP 12** without explicit combo bracket | One knob discipline |

---

## 7. Hypothesis flags (S1 mixed)

| ID | Status | Note |
| --- | --- | --- |
| H7 | **Killed** (expander) | 20.5%; max persona warmonger 37.3% |
| H12 | **Killed** | economist 10.7% |
