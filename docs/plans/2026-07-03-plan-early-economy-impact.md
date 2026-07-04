# Plan — Early economy impact (PROPOSED)

**Date:** 2026-07-03 · **Status:** PROPOSED (sim-led) · **E1/E2/E5:** **KILLED** — see [sweep conclusion](../reports/2026-07-03-early-economy-sweep-conclusion.md)  
**Goal:** Make economy-focused play **threatening in rounds 2–3** without stretching game length (~6–7 rounds at 4p is acceptable).  
**Stacked with:** Lever C expander brakes + S1 `seat_of_empire` 1 VP (current sim defaults).

---

## 1. Problem

Tempo objectives score on the same cleanup they complete. Economy paths (`merchant_lord`, `builder`) typically pay one round later. Merchant Lord (canon 8 gold) helped 4p economist (10.7%) but did not move 6–8p.

---

## 2. Tracks

| ID | Knob | Status |
| --- | --- | --- |
| E1 | `merchant_lord` 8→6 gold | **KILLED** 2026-07-03 |
| E2 | `builder` 3→2 buildings | **KILLED** 2026-07-03 |
| E5 | Tier-1 production build 3→2 AP | **KILLED** 2026-07-03 |
| E3 | Staged row reveal (economy in opening 2) | open — packet |
| E4 | New early economy public | open — design |
| E6 | City +1 gold production | open — rules |
| E7 | Economic Boom initiative | open — strategy card |

**Do not re-run E1/E2/E5** or stack killed levers without a combo study.

---

## 3. Sim encoding (live)

| Config key | Default |
| --- | ---: |
| `economy.merchant_lord_min_gold` | 8 |
| `economy.builder_min_buildings` | 3 |
| `economy.tier1_production_build_ap` | 3 (Farm/Mine/Grove/Embassy only) |

---

## 4. References

- [Sweep conclusion](../reports/2026-07-03-early-economy-sweep-conclusion.md)
- [Economist viability memo](../reports/2026-07-03-memo-economist-viability.md)
- [H7 calibration sweep](../reports/2026-07-03-h7-calibration-sweep-conclusion.md)
- [Current baselines](../reports/2026-07-03-current-baselines.md)
