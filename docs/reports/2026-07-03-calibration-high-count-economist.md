# High-count economist read — Lever C + S1 calibration

**Date:** 2026-07-03 · **Sim-only**  
**Change:** Expander lead brakes (Lever C) + `seat_of_empire` 1 VP (S1) — now default on all mixed brackets  
**Question:** Does the **4p economist doubling** (5.3% → 10.7%) carry to 6p/8p?

---

## 1. Verdict

**No.** Economist lift is **4p-specific**. At 6p and 8p, win rate moves **+1.0 pp** and **−0.3 pp** respectively — both still **fail H8** (≥5% bar).

| Count | Economist (pre) | Economist (calibrated) | Δ | H8 (≥5%) |
| --- | ---: | ---: | ---: | --- |
| **4p** | 5.3% | **10.7%** | **+5.4** | **Pass** |
| **6p** | 2.6% | **3.6%** | +1.0 | Fail |
| **8p** | 2.3% | **2.0%** | −0.3 | Fail |

The “almost doubled” story is accurate at **4p only** (~2× relative). At 6p it is a **~38% relative** bump on a tiny base; at 8p it is **noise**.

---

## 2. Full persona comparison

### 4p (100 games, seed_base 70000)

| Persona | Pre | Calibrated |
| --- | ---: | ---: |
| expander | 40.5% | 23.3% |
| balanced | 37.1% | 33.8% |
| warmonger | 22.1% | 30.6% |
| economist | 5.3% | **10.7%** |
| diplomat | 21.6% | 26.7% |
| Mean rounds | 5.8 | 6.2 |

### 6p (200 games, seed_base 36000)

| Persona | Pre | Calibrated |
| --- | ---: | ---: |
| warmonger | 25.2% | **27.2%** |
| balanced | 21.3% | 23.6% |
| expander | 21.0% | **14.4%** |
| diplomat | 13.6% | 14.9% |
| economist | 2.6% | **3.6%** |
| Mean rounds | 5.8 | **6.4** |

### 8p (200 games, seed_base 38000)

| Persona | Pre | Calibrated |
| --- | ---: | ---: |
| balanced | 21.9% | 22.6% |
| warmonger | 15.4% | **17.6%** |
| expander | 11.5% | 10.8% |
| diplomat | 11.5% | 9.1% |
| economist | 2.3% | **2.0%** |
| Mean rounds | 5.8 | 6.2 |

**H7:** Killed at 6p and 8p before and after (expander already diluted). Calibration further lowers expander at 6p (21% → 14%).

---

## 3. Why 4p economist moves more

1. **Shorter absolute games at 4p** — even post-calibration (~6.2 rounds), 4p is the tightest race. Trimming seat double-dip (`seat_of_empire` 2→1) + slowing expander closes gives **Merchant Lord / builder** paths one extra round of relevance.
2. **Seat race less decisive at high count** — seat VP share drops (6p 5.7%, 8p 4.0% vs ~10% at 4p S1). Economist was never seat-dependent; the 4p bump is about **tempo**, not throne access.
3. **More seats = more tempo bots winning** — warmonger gains at 6p (+2 pp); council/whisper noise scales with player count. Economist still cannot convert gold/build into wins before someone hits 10 VP in ~6 rounds.
4. **Lever C is expander-only** — does not buff economist directly; 4p lift is an **indirect pacing effect**. High-count games need **Lever A pacing** (longer games) or **6–8p-specific packet** work per [economist memo](2026-07-03-memo-economist-viability.md).

---

## 4. Implications

| Finding | Action |
| --- | --- |
| S1 + Lever C fixes **4p H12** | Keep as default smoke stack |
| **6–8p H8 still open** | Do not infer 4p economist success transfers — need VP threshold / production sweep at 6–8p |
| Expander tamed at all counts | Calibration is safe for H7 at 6–8p; 4p expander now ~23% |
| Mean rounds +0.4–0.6 at high count | Modest stretch; not enough alone for economist |

---

## 5. Reports & configs

- [4p baseline](2026-07-03-baseline-mixed-4p-m3.md) · `bracket-m2-smoke.json`
- [6p baseline](2026-07-03-baseline-mixed-6p-m3.md) · `bracket-6p-mixed.json`
- [8p baseline](2026-07-03-baseline-mixed-8p-m3.md) · `bracket-8p-mixed.json`

Regenerate:

```bash
cd sim
py -3.11 -m aeonis_sim.runner.tournament --config configs/bracket-6p-mixed.json --report ../docs/reports/2026-07-03-baseline-mixed-6p-m3.md --workers 4
py -3.11 -m aeonis_sim.runner.tournament --config configs/bracket-8p-mixed.json --report ../docs/reports/2026-07-03-baseline-mixed-8p-m3.md --workers 4
```
