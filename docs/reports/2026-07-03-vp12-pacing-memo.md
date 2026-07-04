# Memo — 12 VP pacing variant (sim-only)

**Date:** 2026-07-03 · **Status:** closed · **Verdict:** **KILLED** — do not promote

**Stack:** M3 + Lever C expander brakes + S1 `seat_of_empire_vp: 1` (current default). Toggle: `config["pacing"]["vp_threshold"]` (canon remains **10**; AL-41).

**Question:** Does raising the win threshold to **12 VP** stretch games toward the Plan 3 MVP **8–10 round** target and lift economist at 6–8p?

---

## Results (mixed seats, same seeds as baselines)

| Count | VP | Games | Mean rounds | Economist | Expander | Max persona |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 4p | 10 | 100 | 6.2 | **10.7%** | 23.3% | balanced 33.8% |
| 4p | 12 | 100 | **8.4** | **4.1%** | 27.4% | balanced 34.8% |
| 6p | 10 | 200 | 6.4 | 3.6% | 14.4% | warmonger 27.2% |
| 6p | 12 | 200 | **8.8** | **1.7%** | 15.5% | warmonger 28.8% |
| 8p | 10 | 200 | 6.2 | 2.0% | 10.8% | balanced 22.6% |
| 8p | 12 | 200 | **8.2** | **1.6%** | 13.4% | balanced 26.2% |

---

## Conclusion

12 VP **lengthens games** (~+2 rounds; 6p/8p land in the 8–10 band) but **regresses economist everywhere**, including 4p where baseline already passes H12 (10.7% → 4.1%). Extra runway favors balanced/warmonger objective racing, not builder/gold paths. Aligns with H7 Lever A (killed 2026-07-03).

**Do not promote** without a paired design change (row composition, Lord asymmetry, structural VP pacing). VP threshold alone is not a viable economist lever.

---

## Re-run (no stored configs)

Copy any baseline bracket and add:

```json
"pacing": {"vp_threshold": 12}
```

Example: `bracket-m2-smoke.json` (4p), `bracket-6p-mixed.json`, `bracket-8p-mixed.json`.
