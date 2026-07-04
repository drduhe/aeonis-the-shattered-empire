# Plan — Imperial Seat reward sweep (PROPOSED)

**Date:** 2026-07-03 · **Status:** PROPOSED (sim-only until promoted)  
**Parent:** [H7 Expander dominance](2026-07-03-h7-expander-dominance-m3.md) · [Seat/rite analysis](../reports/2026-07-03-seat-rite-analysis-m3.md)  
**Runs after:** [Lever 4](../reports/2026-07-03-lever-c-expander-brake-m3.md) (bot brake) — **one knob per bracket**, no stacking with Levers A/B/C unless a follow-up combo study is explicitly scoped.

---

## 1. Question

Is **Imperial Seat double-dip** (Coronation Rite drip + `seat_of_empire` public card + milestone) too rewarding in **short ~6-round** mixed 4p games — and does that drive expander dominance?

**Seat analysis verdict (2026-07-03):** Expander does **not** hold the seat more than balanced. Seat VP is ~**15.5%** of all VP globally; balanced actually captures **more** end-game seat control and **more** `seat_of_empire` scores. Expander wins via **faster conversion** (74% win when holding seat at end; 38% of wins without end-seat control).

**Implication:** A seat reward sweep tests **pacing and close density**, not “expander monopolizes the throne.” Pass bars should include **H7 expander ≤35%** *and* **solo 25% parity** *and* **balanced/diplomat not collapsed**.

---

## 2. Canon baseline (unchanged until promoted)

| Source | Timing | VP | Owning doc |
| --- | --- | ---: | --- |
| Coronation Rite | Cleanup & Checks; Lord on Imperial Seat | +1 / round (max once/round) | `Victory.md` §5 |
| Coronation milestone | 3rd total Rite (non-consecutive OK) | +2 once/game | `Victory.md` §5 |
| Seat of Empire | Public row; control Seat at Cleanup | +2 once/card | `Objectives.md` |

**Theoretical seat stack:** up to **~7 VP** (2 obj + 3 rites + 2 milestone) in a fast game — material at **10 VP** threshold.

---

## 3. Sweep knobs (ranked, one-at-a-time)

Re-run `bracket-m2-smoke.json` (100 games) + `bracket-m2-4p.json` solo (200 games) after each. Encode via `config["seat_rewards"]` toggles in `sim/` (to be added when sweep starts — not canon doc edits until promotion).

| ID | Knob | PROPOSED value | Expected effect | Priority |
| --- | --- | --- | --- | ---: |
| **S1** | `seat_of_empire` public VP | **2 → 1** | Cuts fastest double-dip; smallest rules surface | **1** |
| **S2** | Coronation Rite VP | **1 → 0** until **round 4+** | Delays seat drip in short games; rites still “count” toward milestone | 2 |
| **S3** | Coronation milestone | **3rd → 4th** rite, or **+2 → +1** | Reduces spike closes; test separately (S3a vs S3b) | 3 |
| **S4** | Mutual exclusion | Rite **or** `seat_of_empire` scores same Cleanup (not both) | Hard anti-double-dip; high rules friction — sim-only probe | 4 |
| **S5** | Row composition | Remove `seat_of_empire` from **opening** shared reveal pool | Delays visible race; pairs with pacing levers | 5 |

**Do not stack** S1–S5 in one bracket without a dedicated combo report.

---

## 4. Pass / fail bars

| Metric | Interim | Kill (H7) |
| --- | ---: | ---: |
| Expander mixed 4p win % | ≤ **35%** | ≤ **30%** |
| Economist mixed 4p (H12) | ≥ **5%** | — |
| Solo 4p each persona | **20–30%** | — |
| Mean rounds (4p mixed) | Track; target drift toward **7–8** if paired with Lever A | — |
| Seat VP share of all VP | Track; expect drop from **~15.5%** baseline | — |

Regenerate seat breakdown: `py -3.11 scripts/analyze_seat_rite.py <jsonl>`.

---

## 5. Sim encoding checklist (when sweep starts)

1. Add `GameState` / `config["seat_rewards"]` fields mirroring S1–S4 (row pool = setup change).
2. Wire `cleanup.py` (_score_coronation), `objectives.py` (_seat_of_empire or scoring path).
3. Log interpretation in `playtest/Ambiguity_Ledger.md` (AL-43+).
4. `pytest` + mixed smoke + solo ladder per knob.
5. Report under `docs/reports/2026-07-03-seat-sweep-<knob>.md`.
6. **Promotion:** only via `rules_and_systems/INDEX.md` decision log + `Victory.md` / `Objectives.md` + `First_Playable_Packet.md` + sim defaults.

---

## 6. References

- [Seat/rite analysis](../reports/2026-07-03-seat-rite-analysis-m3.md)
- [Lever A VP threshold](../reports/2026-07-03-lever-a-pacing-vp-threshold.md)
- [Lever B frontier_lord](../reports/2026-07-03-lever-b-frontier-lord-8hex.md)
- [Lever C expander brake](../reports/2026-07-03-lever-c-expander-brake-m3.md) (bot)
