# Plan — Imperial Seat reward sweep (PROPOSED)

**Date:** 2026-07-03 · **Status:** PROPOSED · **S1:** **ADOPTED** as sim default (not canon)  
**Conclusion:** [H7 calibration sweep](../reports/2026-07-03-h7-calibration-sweep-conclusion.md)

---

## S1 result (adopted in sim defaults)

`seat_of_empire_vp: 1` on `bracket-m2-smoke.json`, `bracket-m3-ci.json`, `bracket-6p-mixed.json`, `bracket-8p-mixed.json`.

| Metric | Lever C only | C + S1 |
| --- | ---: | ---: |
| Expander | 20.0% | 20.5% |
| Balanced | 40.8% | **29.3%** |
| Economist | 5.3% | **10.7%** |

Seat analysis showed expander does **not** monopolize the seat — S1 trims balanced spike and lifts economist without reopening expander dominance.

---

## Open tracks (if revisited)

| ID | Knob | Status |
| --- | --- | --- |
| S1 | `seat_of_empire` 2→1 VP | **ADOPTED** (sim default) |
| S2 | Rite VP delayed until round 4+ | open |
| S3 | Milestone 3rd→4th rite or +2→+1 | open |
| S4 | Mutual exclusion rite vs seat obj | open |

Re-run via `seat_rewards` block on `bracket-m2-smoke.json` copy. AL-43.

---

## References

- [Seat/rite analysis](2026-07-03-h7-calibration-sweep-conclusion.md) (condensed; full tables in git history)
- [Current baselines](../reports/2026-07-03-current-baselines.md)
