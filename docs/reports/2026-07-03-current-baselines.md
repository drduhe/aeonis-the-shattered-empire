# Current sim baselines (M4-on)

**Updated:** 2026-07-13 · Regenerate tournament reports as needed — stored snapshots are optional.

**Default stack:** M3 engine + full M4 Lord asymmetry + Lever C expander brakes + S1 `seat_of_empire_vp: 1`. Use explicit `lord_asymmetry.enabled: false` only for neutral/legacy comparisons.

**Balance read stack:** same + full M4 asymmetry — see [post-M4 rebaseline](2026-07-12-m4-rebaseline.md).

---

## Configs (keep in repo)

| Config | Use |
| --- | --- |
| `bracket-m2-smoke.json` | Historical M2-named mixed 4p smoke; now inherits the M4-on default |
| `bracket-m2-4p.json` | Historical M2-named solo 4p ladder; now inherits the M4-on default |
| `bracket-6p-mixed.json` / `bracket-8p-mixed.json` | High-count mixed; now inherit the M4-on default |
| `bracket-m4-baseline-4p.json` / `-6p` / `-8p` | **M4-on** mixed baselines |
| `bracket-m4-default-review-4p.json` / `-6p` / `-8p` | Current canonical-stack M4 default review |
| `bracket-m4.json` / `bracket-m4-ci.json` | M4 completeness gates |
| `bracket-m2-ci.json` / `bracket-m3-ci.json` / `bracket-m4-ci.json` | CI gates |
| `regression-plan{1,2}-*.json` | Plan 1/2 metric gates (CI) |

---

## Headlines — canonical M4-on (2026-07-13)

### Mixed 4p (`bracket-m4-default-review-4p.json`, 100)

Mean **6.70** rounds · economist **12.2%** · warmonger **44.4%** · expander **22.0%**

### Mixed 6p (`bracket-m4-default-review-6p.json`, 80)

Mean **6.66** rounds · economist **5.4%** (H8 pass) · balanced **24.5%**

### Mixed 8p (`bracket-m4-default-review-8p.json`, 80)

Mean **6.38** rounds · economist **0.8%** (H8 watch/fail) · balanced **27.8%**

### Prior M3-off (2026-07-03) for comparison

| Bracket | Mean rounds | Economist |
| --- | ---: | ---: |
| 4p | 6.2 | 10.7% |
| 6p | 6.4 | 3.6% |
| 8p | 6.2 | 2.0% |

---

## Open

- **Pacing** — **6–8 mean rounds** is the design band (Lever A accepted 2026-07-12). Current canonical M4-on means (6.38–6.70) are in band.
- **Default-on M4** promoted after 520/520 matched canonical-stack games — see [default-on review](2026-07-13-m4-default-on-review.md).
- **Lord/persona watches** — Auriel/warmonger at 4p; Vharok floor and economist viability at 8p. These are tuning backlog items, not reasons to simulate a symmetric game by default.

---

## Regenerate

```bash
cd sim
python -m aeonis_sim.runner.tournament --config configs/bracket-m4-baseline-4p.json --workers 4
python -m aeonis_sim.runner.tournament --config configs/bracket-m4-baseline-6p.json --workers 4
python -m aeonis_sim.runner.tournament --config configs/bracket-m4-baseline-8p.json --workers 4
python scripts/m4_default_review.py
```
