# 8-player economist diagnosis

**Date:** 2026-07-13

**Status:** sim-only diagnosis; no canon balance change

**Final gate:** 420/420 completed games (320 at 8p, 100 at 4p)

**Stack:** M4 default-on, audited objectives, no building upkeep, corrected geometry, S1 Seat reward

## Decision

Do not apply another economy knob or persona-weight pass. The 8-player economist floor is primarily an **objective-access problem**, amplified by **Lord fit**, rather than failure to execute an economy.

Retain one bot-correctness change: Builder-specific features now apply only while **Builder is revealed and unscored**. Do not retain the exploratory building-effect value table; although it increased resource retention, it introduced subjective values and pushed balanced to 45.1% in the matched 4p guard.

## Matched 8p results

Each arm used 160 games and the same 249 economist seats. `Full deck` is the current audited 24-card public deck with Archmage removed for the Tier-I-only packet. `Six-card row` is the complete First Playable public set.

| Objective access | Bot state | Mean rounds | Economist wins | Avg VP | Objective VP | Gold | Buildings | Controlled hexes |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Full deck | Before fix | 6.78 | 7 / 249 (**2.8%**) | 4.47 | 4.24 | 6.11 | 5.39 | 7.57 |
| Full deck | Objective-aware | 6.74 | 3 / 249 (**1.2%**) | 4.67 | 4.45 | 8.68 | 6.10 | 7.69 |
| Six-card row | Before fix | 6.21 | 12 / 249 (**4.8%**) | 5.43 | 5.16 | 5.89 | 5.29 | 7.43 |
| Six-card row | Objective-aware | 6.03 | 16 / 249 (**6.4%**) | 5.74 | 5.44 | 7.49 | 5.59 | 7.37 |

The objective-aware change improves legibility but does not manufacture a pass: the full deck remains below H8, while the six-card row crosses the 5% watch floor. The concentrated row adds about 1.1 average VP without meaningfully changing territory or build volume.

## Attribution

### Objective access is the main effect

The economist already builds aggressively: 5.6-6.1 buildings per seat in the retained arms. Its persistent gap is conversion into the public VP race. The complete six-card row keeps Builder and Merchant Lord continuously available; the full deck reveals only a subset of its 24 cards before a typical round-7 finish.

This does **not** reopen E3. The killed E3 lever fixed Builder and Merchant Lord as the opening pair and failed its prior 6p/max-persona gates. The useful signal here is broader objective availability, not a recommendation to stage those two cards again.

### Lord fit amplifies the result

Under the six-card row, Thal'rik supplied **10 of the economist's 16 wins** and won 35.7% across 28 economist pairings. Nyxara supplied four wins; Auriel and Rakhis supplied one each; the other four Lords supplied none. Under the full deck, Thal'rik supplied two of only three economist wins.

The economist is therefore not broadly viable at 8p merely because the aggregate six-card result passes. The concentration is consistent with Thal'rik's Portal access providing a conversion route that most Lords lack, but a dedicated pairing ladder would be required to attribute that mechanism.

### Rejected modeling trial

An exploratory table valued buildings by ongoing effect instead of construction cost. It raised full-deck economist Gold from 6.11 to 19.77 and average VP to 4.86, but win rate remained 3.2%. In the 4p guard it pushed balanced from 32.9% to 45.1%. The trial was reverted: it was a broad calibration change with subjective cross-system exchange values, not the narrow correctness fix this diagnosis needed.

## 4p paired regression guard

The retained objective-awareness change was rerun on the same 100 seeds as the M4 default-on review.

| Metric | M4 default review | Objective-aware |
|---|---:|---:|
| Mean rounds | 6.70 | 6.31 |
| Auriel win rate | 51.1% | 33.3% |
| Warmonger win rate | 44.4% | 43.3% |
| Economist win rate | 12.2% | 5.3% |
| Balanced win rate | 32.9% | 27.1% |

The paired Auriel/warmonger watch is not worsened, but warmonger remains above its old 35% persona gate. Rakhis (39.1%) and Thal'rik (37.8%) also remain Lord watches. These are sim-only signals; no Lord-sheet dial is justified by this economist diagnosis.

## Next experiment

If economist viability remains the next design priority, test **random public-objective throughput at 8p** while keeping the audited deck and every card unchanged. This is distinct from killed E3: vary the number or cadence of random reveals, not which objectives are guaranteed.

Required gates:

- Economist at least 5% in aggregate, with wins spread beyond one Lord pairing.
- Mean game length remains 6-8 rounds.
- No 4p persona worsens by more than 5 points, and warmonger does not exceed the retained 43.3% guard.
- Winner objective share remains at least 60%.
- Do not combine with E1/E2/E3/E5 or change persona weights.

## Reproduce

```powershell
python sim/scripts/economist_8p_diagnosis.py
```

The script writes the regenerable detailed summary to `sim/tmp-economist-8p-diagnosis.json` (ignored). The committed inputs are `sim/configs/bracket-economist-diagnosis-8p.json` and the existing 4p M4 default-review config.
