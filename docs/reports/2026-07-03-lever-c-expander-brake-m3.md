# Lever C — Expander lead brake re-tune (M3)

**Date:** 2026-07-03 · **Sim-only** (bot weights; not canon)  
**Parent:** [H7 Expander dominance report](2026-07-03-h7-expander-dominance-m3.md) §7 Lever 4  
**Knob:** `sim/aeonis_sim/agents/persona.py` expander weights — stronger `vp_lead` / `territory_sat` brakes; lower seat/rite press when ahead  
**Not stacked with:** Levers A/B (canon 10 VP, frontier 7 hex)

---

## 1. Verdict

| Metric | Baseline (M3) | Lever C | Interim bar |
| --- | ---: | ---: | --- |
| **Expander win %** | **40.5%** | **20.0%** | ≤35% **Pass** |
| Max persona win % | 40.5% (expander) | **40.8% (balanced)** | ≤28% **Fail** |
| Economist win % | 5.3% | 5.3% | ≥5% **Pass** (H12) |
| Mean rounds | 5.8 | 5.8 | — |
| Solo parity | 25% each | 25% each | **Pass** |

**Bottom line:** Lever C **fixes expander mixed-seat dominance** (40.5% → 20%) with **no solo collateral damage**. H7 expander kill bar (≤30%) clears. **New skew:** balanced **40.8%** — max-persona bar still fails, now on balanced. Do **not** stack further bot nerfs without a balanced-brake audit or packet lever (seat sweep S1).

---

## 2. Weight changes (expander only)

| Weight | Pre (M3 parity) | Lever C |
| --- | ---: | ---: |
| `vp_lead` | -2.5 | **-4.0** |
| `next_vp_lead` | -2.0 | **-3.5** |
| `territory_sat` | -5.5 | **-8.0** |
| `next_territory_sat` | -4.0 | **-6.5** |
| `seat` / `seat_pull` / `rite_ready` | 0.55 | **0.40** |
| `seat_streak` / `next_seat` | 0.45 | **0.35** |

Pattern unchanged from [parity diagnosis](2026-07-03-persona-parity-diagnosis.md): **brake when ahead**, not baseline expansion nerf.

---

## 3. Mixed 4p detail (100 games)

Config: `sim/configs/bracket-m2-smoke.json` · seed_base 70000

| Persona | Baseline | Lever C |
| --- | ---: | ---: |
| expander | 40.5% | **20.0%** |
| balanced | 37.1% | **40.8%** |
| warmonger | 22.1% | 31.0% |
| diplomat | 21.6% | 28.0% |
| economist | 5.3% | 5.3% |

Coronation rite VP share dropped (4.4% of all VP vs 5.2% baseline) — expander presses seat less when leading.

---

## 4. Solo 4p (200 games)

Config: `sim/configs/bracket-m2-4p.json`

All personas **25.0%** — expander not overpowered in isolation; skew remains mixed-seat interaction.

---

## 5. Next steps

| Priority | Action |
| ---: | --- |
| 1 | **Seat reward sweep** — [plan](../plans/2026-07-03-plan-seat-reward-sweep.md); start **S1** (`seat_of_empire` 2→1 VP) to test packet pacing without re-breaking expander |
| 2 | Monitor **balanced 40.8%** — if seat sweep lifts expander, may re-hit H7; if balanced stays high, consider narrow balanced lead brake (mirror Lever C pattern) |
| 3 | **Defer Lever 3** (Expansion Strategy primary boost) until expander + balanced both ≤35% |
| 4 | Human 4p table when scheduled — log round count + winner objective row |

---

## 6. Hypothesis flags (Lever C mixed)

| ID | Status | Note |
| --- | --- | --- |
| H7 | **Killed** (expander) | expander 20.0%; max persona 40.8% still fails bar |
| H12 | **Killed** | economist 5.3% |
