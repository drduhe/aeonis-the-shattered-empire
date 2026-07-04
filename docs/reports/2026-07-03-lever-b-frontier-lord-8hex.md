# Lever B — `frontier_lord` 7→8 hexes (sim-only)

**Date:** 2026-07-03 · **Sim-only** (PROPOSED; not canon)  
**Parent:** [H7 Expander dominance report](2026-07-03-h7-expander-dominance-m3.md) §7 · follows [Lever A](2026-07-03-lever-a-pacing-vp-threshold.md)  
**Knob tested:** `config["objectives"]["frontier_lord_min_hexes"]` = **8** (canon 7)  
**Not stacked with:** VP threshold (10 VP canon throughout)

---

## 1. Verdict

| Metric | Baseline (7 hex) | Lever B (8 hex) | Interim bar |
| --- | ---: | ---: | --- |
| Mean rounds | 5.8 | **6.1** | — |
| Expander win % | 40.5% | **43.1%** | ≤35% **Fail** (worse) |
| Economist win % | 5.3% | **8.9%** | ≥5% **Pass** (H12) |
| Solo parity | 25% each | 25% each | Pass |

**Bottom line:** Softening `frontier_lord` **does not curb expander dominance** — win rate ticked up, not down. It **does** lift economist mixed 4p viability (H12 passes at 8.9%). Treat as a **partial packet win for economy personas**, not an H7 fix. Do **not** promote to canon without human playtest; proceed to **Lever 3 or 4** for expander skew.

---

## 2. Mixed 4p detail (100 games)

Config: `sim/configs/lever-b-frontier8-4p-smoke.json` · seed_base 74000

| Persona | Baseline | Lever B |
| --- | ---: | ---: |
| expander | 40.5% | **43.1%** |
| balanced | 37.1% | 26.0% |
| warmonger | 22.1% | 27.0% |
| diplomat | 21.6% | 22.0% |
| economist | 5.3% | **8.9%** |

### Read

1. **+0.3 rounds** — modest pacing stretch; less than Lever A at 12 VP (+1.7).
2. **Expander unchanged or slightly worse for H7** — delaying one map-tempo card did not shift the mixed-seat meta; expander still closes via seat/rite/objective mix (same profile as H7 §3).
3. **Economist beneficiary** — slower frontier race gives builder/gold paths more time; H12 **killed → pass** at 4p mixed.
4. **Balanced dropped** — from 37.1% to 26.0%; tempo reallocation, not zero-sum with expander.

---

## 3. Solo 4p isolation (200 games)

Config: `sim/configs/lever-b-frontier8-4p-solo.json` · seed_base 75000

| Persona | Win % |
| --- | ---: |
| All five | **25.0%** each |

Mean rounds: **6.5** (vs ~6.8 baseline at 10 VP). No collateral persona bug.

---

## 4. Sim implementation (not canon)

- `GameState.frontier_lord_min_hexes` defaults to `FRONTIER_LORD_MIN_HEXES` (7).
- Predicate in `objectives.py`; bot progress in `features.py` scales to threshold.
- **231 pytest** passing.

Regenerate:

```bash
cd sim
py -3.11 -m aeonis_sim.runner.tournament --config configs/lever-b-frontier8-4p-smoke.json --report ../docs/reports/_lever-b-smoke.md --workers 4
py -3.11 -m aeonis_sim.runner.tournament --config configs/lever-b-frontier8-4p-solo.json --report ../docs/reports/_lever-b-solo.md --workers 4
```

---

## 5. Recommendation

| Action | Rationale |
| --- | --- |
| **Do not stack with Lever A VP 12** | Test combined effect only after a single lever hits H7 interim bar alone. |
| **Keep 8-hex as PROPOSED economist packet option** | Sim evidence supports H12; expander cost is acceptable only if paired with a real H7 lever later. |
| **Next: Lever 3 or 4 (bot, narrow)** | [Expander primary scoring](2026-07-03-h7-expander-dominance-m3.md) or **lead brake re-tune** — note Lever 3 may *increase* expander unless paired with pacing. **Lever 4** (brake) is safer next step for H7. |
| **Defer canon patch to `Objectives.md`** | Until human playtest or owner promotes PROPOSED row change. |

---

## 6. Hypothesis flags (Lever B mixed)

| ID | Status | Note |
| --- | --- | --- |
| H7 | **Confirmed** | expander 43.1% |
| H12 | **Killed** | economist 8.9% (≥5%) |
