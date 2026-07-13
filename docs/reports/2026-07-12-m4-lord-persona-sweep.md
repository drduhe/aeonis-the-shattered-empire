# M4 Lord × persona sweep

**Date:** 2026-07-12 · **Status:** sim-only · **Stack:** full M4 `lord_asymmetry` + S1 seat VP

Separates **sheet strength** (solo: all seats same persona, Lords rotate) from **mixed-seat fit** (personas + Lords both vary). Focus watch from [post-M4 rebaseline](2026-07-12-m4-rebaseline.md): Rakhis, Thal'rik, Vharok, Cassian.

## Configs

| Config | Mode | Games | Seed |
| --- | --- | ---: | ---: |
| `bracket-m4-lord-persona-solo-4p.json` | solo | 200 | 97000 |
| `bracket-m4-lord-persona-mixed-4p.json` | mixed | 100 | 97100 |
| `bracket-m4-lord-persona-mixed-6p.json` | mixed | 150 | 97200 |

Regenerate: `cd sim && python scripts/m4_lord_persona_sweep.py`

**Stability:** 450/450 completed.

**Neutral win rate when seated:** ~**25%** at 4p · ~**16.7%** at 6p.

---

## Headlines

| Bracket | Mean rounds | Top Lord | Floor Lords |
| --- | ---: | --- | --- |
| Solo 4p | 7.50 | Rakhis **51.0%** | Elyndra 12.2%, Seraphel 16.7% |
| Mixed 4p | 7.04 | Thal'rik 37.5% / Rakhis 36.7% | Cassian 15.2%, Elyndra 14.9% |
| Mixed 6p | 6.89 | Thal'rik **28.4%** | Elyndra **3.6%**, Vharok **8.3%** |

Solo personas are flat at **25%** each (expected) — skew below is **Lord sheet**, not persona identity.

---

## Solo 4p — sheet strength under each persona

Overall Lord win % (seated games):

| Lord | Win % | Read |
| --- | ---: | --- |
| Rakhis | **51.0** | Sheet spike (not just warmonger) |
| Thal'rik | **37.9** | Consistent second |
| Cassian | 23.2 | Near neutral overall |
| Auriel | 21.6 | |
| Vharok | 18.8 | Soft |
| Nyxara | 18.6 | Soft |
| Seraphel | 16.7 | Soft |
| Elyndra | **12.2** | Floor |

Watch Lords × persona (solo win % when that Lord is seated):

| Persona | Rakhis | Thal'rik | Vharok | Cassian |
| --- | ---: | ---: | ---: | ---: |
| warmonger | **85.0** | 35.0 | 21.1 | 15.8 |
| economist | 25.0 | **55.0** | 25.0 | **5.0** |
| expander | 35.0 | 22.2 | 16.7 | **44.4** |
| diplomat | **61.1** | 29.4 | 21.1 | 27.8 |
| balanced | **50.0** | 45.0 | 10.0 | 25.0 |

**Fit vs sheet:**

- **Rakhis** — overperforms under *every* persona except economist (still neutral there). **Sheet problem**, amplified by warmonger/diplomat bots.
- **Thal'rik** — strong under economist/balanced; still above neutral overall. Portal kit is a real edge, not only war bots.
- **Cassian** — **fit-sensitive**: crushed as economist (5%) / weak warmonger (16%); thrives as expander (44%). Mixed 4p floor is partly persona pairing, not a dead sheet.
- **Vharok** — soft across the board in solo (no persona rescues him above ~25%).

---

## Mixed 4p / 6p — interaction with persona diversity

### Mixed 4p Lords

| Lord | Win % |
| --- | ---: |
| Thal'rik | 37.5 |
| Rakhis | 36.7 |
| Seraphel | 28.9 |
| Vharok | 28.3 |
| Auriel | 20.4 |
| Nyxara | 18.0 |
| Cassian | **15.2** |
| Elyndra | 14.9 |

Personas: expander 35.4% · warmonger 33.3% · balanced 23.4% · diplomat 20.3% · economist **11.7%**.

### Mixed 6p Lords

| Lord | Win % | vs ~16.7% neutral |
| --- | ---: | --- |
| Thal'rik | **28.4** | high |
| Rakhis | **25.9** | high |
| Cassian | 21.3 | slightly high |
| Seraphel | 17.6 | ~neutral |
| Nyxara | 15.3 | ~neutral |
| Auriel | 12.7 | soft |
| Vharok | **8.3** | floor |
| Elyndra | **3.6** | severe floor |

Personas: balanced 27.2% · warmonger 24.7% · expander 14.3% · diplomat 12.3% · economist **5.6%** (H8 still passes at ≥5%).

---

## Conclusions (sim-only)

1. **Rakhis is the clearest sheet outlier.** Solo 51% / warmonger 85% cannot be explained as persona matchmaking noise. Investigate Sandstride, cavalry economy, and unique-tile income before default-on.
2. **Thal'rik is a real high-count / solo second.** Prefer relative tuning *after* Rakhis, or a paired soft touch — do not ignore portal edge.
3. **Cassian’s 4p mixed floor is mostly fit.** Solo overall ~neutral; expander pairing is strong. Hold sheet nerfs; optional bot/economy path work if economist+Cassian stays near-zero.
4. **Vharok + Elyndra are high-count floors.** Vharok soft even in solo; Elyndra collapses at 6p mixed (3.6%). New watch: Elyndra (was not on the original four).
5. **Keep `lord_asymmetry` opt-in.** Sheet spread is too wide for default CI baselines.

---

## Next actions

1. **Owner call:** open a **Rakhis sheet ladder** (one dial at a time) vs accept “strong cavalry fantasy” with a documented band.
2. **Secondary ladder candidates:** Elyndra 6p floor, Vharok fortress payoff, Thal'rik soft cap only if Rakhis moves and he remains >35% solo.
3. **Do not** flip M4 default-on until Rakhis (and preferably Elyndra/Vharok) have a first pass or an explicit accept-as-is note.

---

## Regenerable artifact

Raw JSON: `sim/tmp-m4-lord-persona.json` (local; not committed).
