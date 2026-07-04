# H7 calibration sweep — conclusion (sim-only)

**Date:** 2026-07-03 · **Status:** closed · **Default stack:** Lever C persona brakes + S1 `seat_of_empire_vp: 1`

---

## Problem (diagnosis)

After M3 card systems, expander returned to **40.5%** mixed 4p win rate (H7 fail). Dominance is **4p-specific** (6p 21%, 8p 11.5% at pre-calibration). Expander wins via **conversion efficiency**, not seat monopolization — balanced holds the seat more often; seat VP is ~15% of all VP.

**Root cause:** M3 increased map-scoring velocity faster than economy paths in ~6-round games.

---

## Lever results (one knob each — do not re-run killed levers)

| Lever | Knob | Expander 4p | Economist 4p | Mean rounds | Verdict |
| --- | --- | ---: | ---: | ---: | --- |
| Baseline (M3) | — | 40.5% | 5.3% | 5.8 | H7 fail |
| **A** | VP threshold 11 / 12 | 43.4% / 39.2% | 1.3% / 3.8% | 6.3 / **7.5** | **KILLED** — no H7 fix; 12 VP hurts economist |
| **B** | `frontier_lord` 7→8 hex | 43.1% | 8.9% | 6.1 | **KILLED** for H7; economist lift only |
| **C** | Expander lead brakes | **20.0%** | 5.3% | 5.8 | **ADOPTED** (code in `persona.py`) |
| **S1** | `seat_of_empire` 2→1 VP | **20.5%** | **10.7%** | 6.3 | **ADOPTED** (default in smoke/6p/8p/ci configs) |

Post **C + S1** (current default): expander **23.3%**, balanced **33.8%**, economist **10.7%**, mean **6.2** rounds at 4p.

---

## High-count (C + S1)

Economist lift is **4p-only**. H8 still fails at 6–8p.

| Count | Economist | Expander | Mean rounds | Max persona |
| --- | ---: | ---: | ---: | --- |
| 4p | **10.7%** | 23.3% | 6.2 | balanced 33.8% |
| 6p | **3.6%** | 14.4% | 6.4 | warmonger 27.2% |
| 8p | **2.0%** | 10.8% | 6.2 | balanced 22.6% |

---

## Sim toggles (PROPOSED — recreate on baseline bracket)

```json
"pacing": {"vp_threshold": 12},
"objectives": {"frontier_lord_min_hexes": 8},
"seat_rewards": {"seat_of_empire_vp": 1}
```

Copy `bracket-m2-smoke.json`, add one block, `--report` to a dated path. AL-41/42/43.

**Seat analysis tool:** `sim/scripts/analyze_seat_rite.py` on tournament JSONL.

---

## Deferred

- Lever A at 6–8p (owner prefers current pace)
- Seat S2–S5, Expansion Strategy primary boost (Lever 3)
- See [early economy sweep](2026-07-03-early-economy-sweep-conclusion.md) — E1/E2/E5 also killed

---

## References

- [Persona parity diagnosis](2026-07-03-persona-parity-diagnosis.md)
- [Economist viability memo](2026-07-03-memo-economist-viability.md)
- [Seat reward sweep plan](../plans/2026-07-03-plan-seat-reward-sweep.md)
- [Current baselines](2026-07-03-current-baselines.md)
