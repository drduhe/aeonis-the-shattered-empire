# Current sim baselines (M4-on)

**Updated:** 2026-07-12 · Regenerate tournament reports as needed — stored snapshots are optional.

**Default stack for CI / M3 gates:** M3 engine + Lever C expander brakes + S1 `seat_of_empire_vp: 1` (**`lord_asymmetry` still opt-in**).

**Balance read stack:** same + full M4 asymmetry — see [post-M4 rebaseline](2026-07-12-m4-rebaseline.md).

---

## Configs (keep in repo)

| Config | Use |
| --- | --- |
| `bracket-m2-smoke.json` | Mixed 4p smoke (100) — M3-off primary CI-adjacent balance |
| `bracket-m2-4p.json` | Solo 4p ladder (200) |
| `bracket-6p-mixed.json` / `bracket-8p-mixed.json` | High-count mixed (M3-off) |
| `bracket-m4-baseline-4p.json` / `-6p` / `-8p` | **M4-on** mixed baselines |
| `bracket-m4.json` / `bracket-m4-ci.json` | M4 completeness gates |
| `bracket-m2-ci.json` / `bracket-m3-ci.json` / `bracket-m4-ci.json` | CI gates |
| `regression-plan{1,2}-*.json` | Plan 1/2 metric gates (CI) |

---

## Headlines — M4-on (2026-07-12)

### Mixed 4p (`bracket-m4-baseline-4p.json`, 100)

Mean **6.84** rounds · economist **10.0%** · warmonger **36.4%** · expander **13.3%**

### Mixed 6p (`bracket-m4-baseline-6p.json`, 200)

Mean **6.96** rounds · economist **6.5%** (H8 pass) · balanced **25.7%**

### Mixed 8p (`bracket-m4-baseline-8p.json`, 200)

Mean **6.75** rounds · economist **5.2%** (H8 pass) · balanced **23.0%**

### Prior M3-off (2026-07-03) for comparison

| Bracket | Mean rounds | Economist |
| --- | ---: | ---: |
| 4p | 6.2 | 10.7% |
| 6p | 6.4 | 3.6% |
| 8p | 6.2 | 2.0% |

---

## Open

- **Pacing** — **6–8 mean rounds** is the design band (Lever A accepted 2026-07-12). Current M4-on means (~6.75–6.96) are in band.
- **Default-on M4** deferred pending Lord×persona sweep — see rebaseline recommendation.
- **Lord outliers** (Rakhis 4p; Thal'rik high-count; Vharok/Cassian floors) → Lord×persona sweep before sheet tuning.

---

## Regenerate

```bash
cd sim
python -m aeonis_sim.runner.tournament --config configs/bracket-m4-baseline-4p.json --workers 4
python -m aeonis_sim.runner.tournament --config configs/bracket-m4-baseline-6p.json --workers 4
python -m aeonis_sim.runner.tournament --config configs/bracket-m4-baseline-8p.json --workers 4
```
