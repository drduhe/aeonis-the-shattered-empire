# Rakhis balance ladder — Dial 1 (Oasis Cavalry −1 Gold)

**Date:** 2026-07-12 · **Status:** sim-only · **Change:** canon + sim

## Decision

Owner chose **tune** (not accept-as-is) after the [Lord×persona sweep](2026-07-12-m4-lord-persona-sweep.md).

**Dial 1 (softest):** Remove Oasis Wellspring owner-only once-per-round **Cavalry −1 Gold** recruit. Tile keeps **+1 Population / +1 Gold** and Farm-yes / Tower-no. Sandstride and Hit and Run unchanged.

**Encoded in:** `lords/Rakhis.md`, `sim/aeonis_sim/engine/recruit.py`, `rules_and_systems/INDEX.md`.

## Gate (same configs / seeds as pre-ladder sweep)

| Bracket | Metric | Pre (Dial 0) | Post Dial 1 | Δ |
| --- | --- | ---: | ---: | ---: |
| Solo 4p | Rakhis win % | **51.0** | **49.5** | −1.5 |
| Solo 4p | Rakhis × warmonger | **85.0** | **70.0** | −15 |
| Solo 4p | Rakhis × balanced | 50.0 | 50.0 | 0 |
| Mixed 4p | Rakhis win % | 36.7 | 34.7 | −2.0 |
| Mixed 6p | Rakhis win % | 25.9 | 25.0 | −0.9 |

Solo personas remain flat at 25%. Full pytest: **332 passed**.

## Verdict

**Dial 1 is a weak lever.** Overall solo spike barely moved (~51% → ~49.5%). Warmonger pairing eased (85% → 70%) but Rakhis remains far above the ~25–35% solo target band.

**Do not stop here.** Next soft→hard step:

### Dial 2 (recommended next)

**Hit and Run** — once per round, after winning as attacker, free 1-hex reposition. Touch identity less than Sandstride; still cuts raid stickiness.

### Dial 3 (if needed)

**Sandstride** — ZOC ignore and/or pre-Pre-Strike retreat (core fantasy; change last).

## Default-on

Still **deferred**. Rakhis sheet outlier remains.

## Regenerate

```bash
cd sim
python scripts/m4_lord_persona_sweep.py
```
