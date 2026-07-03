# Design memo — Economist viability & objective tempo

**Date:** 2026-07-03  
**Status:** Sim-led recommendation · **not canon** until playtested and registered in `rules_and_systems/INDEX.md`  
**Audience:** Owner / design review  
**Evidence:** [Persona parity diagnosis](2026-07-03-persona-parity-diagnosis.md), M2 smoke bracket (`bracket-m2-smoke.json`, 100 games); 7–8p parity-sprint data summarized in `../plans/INDEX.md` (executed plans)

---

## 1. Executive summary

Mixed-seat persona tournaments show **Economist at ~1% win rate** (4p M2 smoke) and **&lt;1% at 7–8p** even after obvious sim-bot bugs were fixed. Solo ladders stay flat at ~25% per persona. That pattern means:

1. **Economist is not a broken bot** — it wins its fair share when every seat plays the same persona.
2. **The mixed-seat gap is mostly game tempo and objective composition**, not another round of `PERSONA_WEIGHTS` tuning.
3. **Expander skew was partly bot artifact** (68% → 31.5% after targeted fixes) and partly real design pressure (short, objective-heavy races).

**Recommendation:** Stop sim weight inflation. Route Economist viability through **Plan 3 (VP legibility)** — shared-row composition and pacing targets — not through bot calibration. Plan 4 matters for 7–8p session length but does not fix 4p Economist on its own.

---

## 2. What the sim proved

### Bot artifacts (fixed — do not revert)

| Issue | Effect | Fix shipped |
| --- | --- | --- |
| Economist `builder_need` weight was negative | Penalized building toward Builder objective | Sign flip + `builder_push` feature |
| Expander runaway when ahead | Kept pressing after taking lead | `vp_lead` brake, stronger `territory_sat` |
| Persona-blind strategy draft/primary | All personas favored bounty + low initiative | Persona-aware draft/primary scoring |

### Design pressure (still open)

| Signal | Data |
| --- | --- |
| Game length | Mean **~6 rounds** (M2 smoke); Plan 3 MVP target is **8–10** |
| Winner VP mix | **~83% objectives**; expander winners often close via objective + Coronation Rite |
| Economist path timing | Builder (3 buildings ≈ 9 AP) + `golden_hoard` (10 gold) rarely completes before someone hits 10 VP |
| Public row bias | First Playable row rewards **map tempo** (`frontier_lord`, `seat_of_empire`) over economy buildup |
| Solo vs mixed | Economist **25% solo**, **1.3% mixed** (4p) — interaction + race, not persona definition |

**Calibration stop rule (locked for sim work):** If solo is flat and mixed is weak after bot bugs are fixed, treat as **canon/playtest input**. Do not chase H8 (Economist ≥5%) with another weight pass.

---

## 3. Diagnosis: over-calibration vs real design

| Question | Answer |
| --- | --- |
| Are we over-calibrating the sim? | **Yes, if we keep tuning weights.** Expander proved that targeted bot fixes move metrics; Economist did not move meaningfully after the bug fix (0% → 1.3%). |
| Is the game “wrong” for economy players? | **Possibly at current First Playable tempo.** Economy can score (Economist seats often reach 4+ objective VP) but loses the **race to 10** in ~6 rounds. |
| Is this a Lord problem? | **No signal yet.** Persona bots abstract Lord identity; Lord parity is a separate track (Plan 5). |
| Should we lower the VP threshold? | **Not from this data alone.** Shorter games are a symptom; lowering 10 VP would compress everyone, not specifically help Economist. |

---

## 4. Recommended levers (canon-side)

All items below are **PROPOSED** until playtested. They align with existing plans; none require sim weight changes.

### Lever A — Pacing target (Plan 3 MVP, primary)

**Owning intent:** `docs/plans/2026-07-03-plan-vp-legibility-mvp.md` §2, Plan 3 §6 — **8–10 rounds** to game end with shared-row pacing.

**Why it helps Economist:** Builder and gold accumulation need AP and Production cycles. At 6 rounds, expansion and military objectives reach payout before economy scales.

**Owner decision:** Treat sub-7-round sim means as a **pacing failure** for MVP validation, not a persona-tuning task. Human playtest should log round count and leader VP at rounds 3/6/8.

**Sim regression gate (after any pacing rule change):**

| Metric | Current (M2 smoke) | Target |
| --- | ---: | ---: |
| Mean rounds to win | ~6 | **8–10** |
| Economist mixed win % (4p) | 1.3% | **≥5%** (H8 direction) |
| Winner objective VP share | ~83% | **≥50%**, no single persona &gt;35% |

### Lever B — Shared-row composition (Plan 3 D1, primary)

**Owning intent:** Plan 3 MVP §3.1 — six-card First Playable row; everyone races the same visible goals.

**Problem:** Current row is expansion- and seat-heavy. Economist’s natural hooks (`builder`, `golden_hoard` secret) are slower than `frontier_lord` and `seat_of_empire`.

**PROPOSED options (pick one for next playtest packet):**

1. **Row rebalance (minimal):** Swap one tempo card for an economy-tagged public (e.g. replace or alternate `seat_of_empire` with a **“Merchant League”**-style card: *“Score if you have 8+ Gold”* or *“Score if you have buildings on 3 different hexes”* — must be defined once in `Objectives.md` before inclusion.
2. **Staged reveal (pacing + variety):** Reveal **1 economy + 1 expansion** at setup instead of two expansion-leaning cards; keeps legibility, softens round-1 dogpiles on frontier.
3. **Charters lite (defer full variant):** One seat may hold a **personal** economic public in addition to the shared row — higher complexity; only if (1) fails playtest.

**Owner decision:** Author one new economy public for First Playable or accept that Economist is a **high-count / longer-game** persona until the full 24-card audit (Plan 3 §5).

### Lever C — Coronation Rite pacing (Plan 3 D3, secondary)

Coronation Rite already replaced seat drip in MVP. Sim winners still take **~23% of VP from Rite** on expander lines — fast seat control closes games.

**PROPOSED (playtest only):** Require **2 consecutive** rounds with Lord on Seat before the per-round Rite VP counts toward the streak bonus, or delay the +2 milestone until round 5+. *Do not change until human table confirms seat still feels contested.*

### Lever D — Plan 4 (7–8p only, contextual)

Plan 4 (`docs/plans/2026-07-02-plan-high-player-count.md`) addresses council throughput, Whisper draw scaling, and map geometry — not 4p Economist directly. It **does** matter because persona sprint data shows **~5-round games at 7–8p**, worse than 4p smoke.

**Use Plan 4 for:** session-length guardrails at high count (Docket, simultaneous upkeep default), map hexes per player, and comparing VP pacing vs 3–4p baseline (Plan 4 §5 metrics).

**Do not use Plan 4 for:** fixing 4p Economist without Lever A or B.

---

## 5. What we will not do (from this memo)

- Further inflation of `PERSONA_WEIGHTS` or `PERSONA_FEATURE_BOOSTS` to force H8 green.
- Change the **10 VP** threshold based on sim-only persona data.
- Promote any PROPOSED lever to canon without propagation per `agents/checklists/Canon_Change_Checklist.md`.
- Treat mixed-seat win rates as Lord balance signals.

---

## 6. Owner decisions (resolved 2026-07-03)

| # | Decision | Outcome |
| --- | --- | --- |
| 1 | Accept sim calibration stop rule? | **Yes** — locked; no further persona weight passes for H8 |
| 2 | Next canon experiment | **Lever B row rebalance** (option 1, minimal) |
| 3 | Author new economy public for First Playable? | **Yes — Merchant Lord** (*Have 8 or more Gold*), PROPOSED in `rules_and_systems/Objectives.md` §4.4, filling the row's sixth slot (Council Power stays deferred, nothing swapped out) |
| 4 | Register in `INDEX.md` when locked | Unchanged — after first human session, not from sim alone |

### First sim read (2026-07-03, mixed 4p, 100 games, same seeds)

| Metric | Pre | Post Merchant Lord |
| --- | ---: | ---: |
| Economist win % | 2.5% | **6.4%** (≥5% bar met) |
| Diplomat win % | 12.8% | 24.0% |
| Balanced / Warmonger win % | 42.3% / 38.6% | 33.8% / 27.9% |
| Expander win % | 28.9% | 33.8% |
| Mean rounds | 6.4 | 6.1 (solo: 7.8 → 6.3) |

Read: the row's sixth slot was doing real work — adding one economy-tagged card redistributed wins toward economy/politics personas without weight changes, exactly the Lever B prediction. Cost: games got slightly **faster**, moving further from the 8–10 round target — Lever A (pacing) remains open and is now the primary lever. Confirmation gate: **H12** at sim M3 (kill criteria in the M3 plan §5); human table required before promotion to canon.

---

## 7. Sim follow-up (status)

1. ~~Encode chosen row change in `playtest/First_Playable_Packet.md` + `Objectives.md` (PROPOSED section).~~ **Done 2026-07-03** (Merchant Lord).
2. ~~Re-run `bracket-m2-smoke.json` (100 games).~~ **Done** — see §6 read. 7–8p mixed brackets still pending (rerun with Merchant Lord row before trusting high-count H8 numbers).
3. Remaining: H12 confirmation at M3 gate (`../plans/2026-07-03-agent-playtest-sim-implementation-plan-m3.md` §5); Lever A pacing remains open — mean rounds moved the wrong way (6.4 → 6.1).
4. Unchanged: if Economist regresses &lt;5% at M3 gate **or** Merchant Lord proves free VP (scored by ≥60% of players per game), pull the card and escalate to the full Plan 3 card audit — not sim weights.

---

## 8. References

| Doc | Role |
| --- | --- |
| `docs/reports/2026-07-03-persona-parity-diagnosis.md` | Full pre/post metrics and bot vs design split |
| `docs/plans/INDEX.md` | Plan statuses; 7–8p parity-sprint outcome (H7/H8) under executed plans |
| `docs/plans/2026-07-03-plan-vp-legibility-mvp.md` | First Playable shared row + Rite |
| `docs/plans/2026-07-02-plan-vp-legibility.md` | Full Plan 3 budget and 8–10 round target |
| `docs/plans/2026-07-02-plan-high-player-count.md` | Plan 4 — high-count pacing and map |
| `playtest/Balance_Dashboard.md` | Human session metrics when table time resumes |

---

*Sim conclusions in this memo stay sim-only until the owner schedules human playtest per AGENTS.md playtest constraints (2026-07-03).*
