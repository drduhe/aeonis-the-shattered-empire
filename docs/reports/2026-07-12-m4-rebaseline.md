# Post-M4 rebaseline + pacing read

**Date:** 2026-07-12 · **Status:** sim-only · **Stack:** M3 engine + full M4 `lord_asymmetry` + S1 seat VP

First multi-count baseline with **full** Lord asymmetry enabled (unique tiles, abilities, discoveries, Legendaries). Compare to M3-off headlines in `2026-07-03-current-baselines.md`.

## Configs

| Config | Games | Seed |
| --- | ---: | ---: |
| `bracket-m4-baseline-4p.json` | 100 | 96000 |
| `bracket-m4-baseline-6p.json` | 200 | 96100 |
| `bracket-m4-baseline-8p.json` | 200 | 96200 |

All: mixed personas, rotating 8-Lord roster, `seat_of_empire_vp: 1`.

**Stability:** 500/500 completed · 0 crash / timeout / degenerate.

---

## Headlines vs prior M3-off

| Bracket | Mean rounds (M3 → M4) | Economist (M3 → M4) | Max persona (M4) |
| --- | ---: | ---: | ---: |
| Mixed 4p | 6.2 → **6.84** | 10.7% → **10.0%** | warmonger **36.4%** |
| Mixed 6p | 6.4 → **6.96** | 3.6% → **6.5%** | balanced **25.7%** |
| Mixed 8p | 6.2 → **6.75** | 2.0% → **5.2%** | balanced **23.0%** |

Neutral expectations: ~20% at 5-persona 4p; ~20% at 5-persona 6–8p (uneven seat counts).

---

## Pacing (open Lever A)

Target band remains **8–10 mean rounds**. M4 lengthens games slightly (~0.5–0.6 rounds) but does **not** close the gap.

| Read | Implication |
| --- | --- |
| Games still end ~round 7 | Objective tempo / VP threshold still dominate length |
| 12 VP stretch previously killed economist lift | Do not re-open VP12 without a paired economist plan |
| M4 content is not the pacing lever | Next pacing work is packet/objective design, not more Lord sheet encode |

**Owner decision still needed:** Lever A pacing — stretch without re-breaking H8/H12.

---

## Persona / hypothesis scoreboard (M4-on)

| ID | 4p | 6p | 8p | Note |
| --- | --- | --- | --- | --- |
| H7 (no persona dominate) | **confirmed** fail | killed | killed | 4p warmonger 36% > 28% gate |
| H8 (economist ≥5% at 6–8p) | n/a | **killed** (6.5%) | **killed** (5.2%) | First clear 6–8p economist pass since Merchant Lord |
| H12 (economist ≥5% at 4p) | killed (10%) | n/a | n/a | Holds at 4p |
| H3 (objectives ≥60% winner VP) | killed (81%) | killed (75%) | killed (72%) | Still objective-heavy |

Combat (contested attacker win): 4p **58%**, 6p **71%**, 8p **68%** — 4p inside Plan 1 band; high-count still hot.

---

## Lord win rates (watch only)

Neutral ~25% at 4p seats; ~12.5% at 8 seats.

### Mixed 4p (100)

| Lord | Games | Win % |
| --- | ---: | ---: |
| Rakhis | 49 | **46.9** |
| Thal'rik | 44 | 29.6 |
| Nyxara | 48 | 25.0 |
| Seraphel | 46 | 23.9 |
| Cassian | 45 | 22.2 |
| Vharok | 48 | 20.8 |
| Elyndra | 50 | 16.0 |
| Auriel | 46 | 15.2 |

### Mixed 6p (200)

| Lord | Games | Win % |
| --- | ---: | ---: |
| Thal'rik | 140 | **30.0** |
| Rakhis | 142 | 22.5 |
| Auriel | 141 | 17.7 |
| Cassian | 139 | 16.6 |
| Seraphel | 139 | 13.7 |
| Nyxara | 141 | 13.5 |
| Elyndra | 141 | 12.1 |
| Vharok | 139 | **7.2** |

### Mixed 8p (200)

| Lord | Games | Win % |
| --- | ---: | ---: |
| Thal'rik | 188 | **26.1** |
| Rakhis | 188 | 18.1 |
| Auriel | 188 | 14.4 |
| Elyndra | 188 | 10.6 |
| Nyxara | 188 | 9.0 |
| Vharok | 188 | 8.5 |
| Seraphel | 188 | 8.0 |
| Cassian | 188 | **5.3** |

**Watch items (not tune yet):** Rakhis spike at 4p; Thal'rik lead at 6–8p; Vharok (6p) and Cassian (8p) floors. Persona bots + sheet fantasy interact — separate Lord×persona sweeps before sheet nerfs.

---

## Default-on recommendation

**Keep `lord_asymmetry` opt-in** for default M3 CI brackets.

Reasons:
1. Pacing still short of 8–10 regardless of M4.
2. 4p persona imbalance (warmonger) reappears with M4 on.
3. Lord outliers need a dedicated Lord×persona bracket before calling sheets “balanced.”

Flip default-on only after: (a) pacing lever chosen, or (b) explicit owner call that M4 completeness > baseline continuity.

---

## Next actions (ordered)

1. **Owner: Lever A pacing** — pick a packet-side stretch (objective cadence / VP sources) that preserves H8/H12.
2. **Lord×persona sweep** — solo/rotate brackets with M4 on to separate sheet strength from persona fit (Rakhis / Thal'rik / Vharok / Cassian).
3. **Revisit default-on** after (1) or (2).

---

## Regenerate

```bash
cd sim
python -m aeonis_sim.runner.tournament --config configs/bracket-m4-baseline-4p.json --workers 4
python -m aeonis_sim.runner.tournament --config configs/bracket-m4-baseline-6p.json --workers 4
python -m aeonis_sim.runner.tournament --config configs/bracket-m4-baseline-8p.json --workers 4
```
