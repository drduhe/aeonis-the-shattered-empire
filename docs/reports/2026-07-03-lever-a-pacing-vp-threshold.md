# Lever A — VP threshold pacing sweep (sim-only)

**Date:** 2026-07-03 · **Sim-only** (PROPOSED; not canon)  
**Parent:** [H7 Expander dominance report](2026-07-03-h7-expander-dominance-m3.md) §7 lever order  
**Knob tested:** `config["pacing"]["vp_threshold"]` — single pacing lever, no stacking  
**Baseline:** [Mixed 4p M3](2026-07-03-baseline-mixed-4p-m3.md) at canon **10 VP**

---

## 1. Verdict

| Setting | Mean rounds | Expander win % | Economist win % | H7 interim (≤35%) | FP pacing (7–8 r) |
| --- | ---: | ---: | ---: | --- | --- |
| **Baseline (10 VP)** | **5.8** | **40.5%** | **5.3%** | Fail | Fail (short) |
| VP 11 | 6.3 | **43.4%** | 1.3% | Fail (worse) | Fail |
| **VP 12** | **7.5** | **39.2%** | 3.8% | Fail | **Pass** |

**Bottom line:** Raising the win threshold **stretches games** (12 VP → ~7.5 mixed rounds, ~8.6 solo) but **does not materially fix expander dominance**. VP 11 made expander **worse**. VP 12 is the only variant that hits First Playable pacing targets — use it only as a **sim experiment default** until a human packet decision; **do not stack** with Lever 2 until re-tested alone.

---

## 2. Mixed 4p detail (100 games each)

Configs: `sim/configs/lever-a-vp11-4p-smoke.json`, `lever-a-vp12-4p-smoke.json`  
Matchmaking: mixed · seed_base 71000 / 72000 · M3 engine unchanged otherwise

| Persona | Baseline 10 VP | VP 11 | VP 12 |
| --- | ---: | ---: | ---: |
| expander | 40.5% | 43.4% | 39.2% |
| balanced | 37.1% | 28.6% | 29.9% |
| warmonger | 22.1% | 31.9% | 29.7% |
| diplomat | 21.6% | 19.2% | 23.1% |
| economist | 5.3% | 1.3% | 3.8% |

### Read

1. **Pacing works at 12 VP** — +1.7 rounds vs baseline; median 7. Aligns with FP economy goal (8–10 rounds internal target) without touching production or objectives.
2. **Expander dominance persists** — 39.2% is only ~1.3 pp below baseline; still far from H7 kill bar (≤30%) and interim bar (≤35%). Longer games slightly **help warmonger/balanced** but expander still leads.
3. **Economist regresses at higher thresholds** — H12 was killed at 10 VP (5.3%); at 11 VP economist collapses to 1.3%. At 12 VP, 3.8% (H12 **inconclusive**). Slower games favor **tempo/map** personas over builder/gold paths.
4. **VP 11 is a dead end** — worse on both expander and economist for +0.5 rounds only.

---

## 3. Solo 4p isolation (VP 12, 200 games)

Config: `sim/configs/lever-a-vp12-4p-solo.json` · seed_base 73000

| Persona | Win % |
| --- | ---: |
| All five | **25.0%** each |

Mean rounds: **8.6** (vs ~6.8 at 10 VP solo baseline).  
**Verdict:** No persona is overpowered in isolation at 12 VP — expander skew remains **mixed-seat interaction**, same as H7 §4.

---

## 4. Sim implementation (not canon)

- `GameState.vp_threshold` defaults to `VP_THRESHOLD` (10).
- Tournament configs pass `"pacing": {"vp_threshold": N}`.
- Bot closing multipliers in `features.py` scale to `state.vp_threshold`.
- **230 pytest** passing after wiring.

Regenerate:

```bash
cd sim
py -3.11 -m aeonis_sim.runner.tournament --config configs/lever-a-vp12-4p-smoke.json --report ../docs/reports/_lever-a-vp12-smoke.md --workers 4
py -3.11 -m aeonis_sim.runner.tournament --config configs/lever-a-vp12-4p-solo.json --report ../docs/reports/_lever-a-vp12-solo.md --workers 4
```

---

## 5. Recommendation (next lever)

| Action | Rationale |
| --- | --- |
| **Do not promote VP 12 to canon yet** | Sim-only PROPOSED; human packet decision required. |
| **Proceed to Lever 2 alone** | [Row tempo audit](2026-07-03-h7-expander-dominance-m3.md) — e.g. `frontier_lord` 7→8 hexes — without stacking VP threshold. |
| **Keep VP 12 as optional sim pacing preset** | Useful for 6–8p economist viability sweeps (longer games) if Lever B needs a longer runway. |
| **Defer persona weights / M4 Lords** | Unchanged from H7 §7. |

---

## 6. Hypothesis flags (VP 12 mixed only)

| ID | Status | Note |
| --- | --- | --- |
| H7 | **Confirmed** | expander 39.2% |
| H12 | **Inconclusive** | economist 3.8% (<5% bar) |
| H9 | **Killed** | diplomat 23.1% |
