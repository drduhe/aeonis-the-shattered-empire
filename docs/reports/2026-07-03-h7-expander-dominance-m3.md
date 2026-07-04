# H7 Focus Report — Expander dominance at mixed 4p (M3)

**Date:** 2026-07-03 · **Sim-only** (not canon)  
**Hypothesis:** H7 — no persona should dominate mixed-seat win rate  
**Kill bar:** Expander ≤30% **and** max persona ≤28% in mixed brackets  
**Data:** `bracket-m2-smoke.json` (100 games, seed_base 70000) at **M3 fidelity**; solo ladder `bracket-m2-4p.json` (200 games) for isolation check

---

## 1. Verdict

| Metric | Value | vs kill bar |
| --- | ---: | --- |
| Expander mixed win % | **40.5%** | **Fail** (target ≤30%) |
| Max persona win % | **40.5%** (expander) | **Fail** (target ≤28%) |
| H7 status | **Confirmed** (dominance present) | — |

**Bottom line:** Expander dominance at **4p only** returned after M3 card systems landed. This is **not** a solo-persona bug and **not** fixed by M4 Lords. Treat as **packet/pacing + narrow bot gaps** until a design lever is tested.

---

## 2. Timeline (mixed 4p)

| Snapshot | Expander | Balanced | Economist | Notes |
| --- | ---: | ---: | ---: | --- |
| Pre parity fix (M2) | **68%** | 24% | 0% | [Parity diagnosis](2026-07-03-persona-parity-diagnosis.md) |
| Post parity fix (M2) | **31.5%** | 51.4% | 1.3% | Targeted brakes + persona-aware draft |
| Pre-M3 / Merchant Lord | **33.8%** | 33.8% | 6.4% | [Pre-M3 baseline](2026-07-03-baseline-mixed-4p.md) |
| **M3 full card systems** | **40.5%** | 37.1% | 5.3% | [M3 baseline](2026-07-03-baseline-mixed-4p-m3.md) |

**Read:** Parity fixes worked, then **M3 shifted the meta back toward map tempo** without breaking economist at 4p (H12 killed). Expander gained ~7 pp vs pre-M3; balanced lost ground.

**High-count contrast (same M3 engine):**

| Count | Expander win % | H7 |
| --- | ---: | --- |
| 4p mixed | **40.5%** | Confirmed |
| 6p mixed | 21.0% | Inconclusive |
| 8p mixed | 11.5% | Killed |

Dominance is **4p-specific** — more seats at the same ~5.8-round length dilute expander’s race advantage.

---

## 3. Winner profiles (mixed 4p M3, JSONL analysis)

Games where each persona **won** (100 completed games; winner persona from seat assignment):

| Winner | Wins | Mean rounds | Mean winner VP | Objective VP share | Rite+ milestone share | Lord capture share | Mean hexes controlled |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Expander** | 32 | **6.47** | 10.81 | **74.9%** | **16.1%** | 4.9% | 9.47 |
| Balanced | 27 | 6.63 | 10.70 | 78.1% | 19.0% | 2.1% | 9.63 |
| Warmonger | 20 | 7.25 | 11.15 | 80.9% | 5.2% | **12.3%** | **10.95** |
| Diplomat | 17 | 7.29 | 10.53 | 92.7% | 5.8% | 1.5% | 8.47 |
| Economist | 4 | 6.75 | 10.75 | 84.5% | 11.4% | 4.2% | 8.50 |

### Interpretation

1. **Expander wins are fast wins** — second-shortest mean rounds (after economist’s tiny n=4). Closes at **~6.5 rounds** with a **territory + rite** mix, not pure objective spam.
2. **Not “most hexes wins”** — warmonger winners hold **more hexes** (10.95) but win **less often** and **slower**. Expander wins are a **tempo** profile, not maximal map paint.
3. **Objective VP still ~75–80%** for military/expansion winners — the public row remains the spine; expander converts **frontier/seat pressure** into scored cards faster than economy personas.

When an expander is **seated** (78 of 100 games in mixed roster), expander wins **41%** of those games — the skew is real at-table, not a seat-count artifact.

---

## 4. Solo isolation check

| Persona | Solo 4p win % (200 games) |
| --- | ---: |
| All five | **25.0%** each |

**Verdict:** Expander is **not** overpowered in isolation. Skew is **mixed-seat interaction** — same conclusion as the 2026-07-03 parity diagnosis.

---

## 5. Design pressure vs bot artifact

### A. Design pressure (primary — ~70% of story)

| Factor | Evidence | Mechanism |
| --- | --- | --- |
| **Short games** | Mean **5.8** rounds (M3) vs 6.1 pre-M3 | Map/seat objectives pay before economy scales |
| **Public row tempo** | `frontier_lord`, `seat_of_empire`, `portal_mastery`, `warlord` still on row | Shared visible races favor expansion/military |
| **M3 territorial tools** | Exploration events, artifact sites, **Expansion Strategy** primary (17 uses/100 games) | More ways to gain/map-score in fewer rounds |
| **Combat volume** | Battles/player-round **0.274** (M3) vs **0.224** (pre-M3); uncontested captures **245**/100 games | Faster hex flip → faster frontier/seat scoring |
| **Coronation path** | Expander winner rite share **16.1%** vs diplomat **5.8%** | Seat + Lord-on-throne still closes games for expander line |

**Merchant Lord** helped economist (H12) but **did not cap expander** — row rebalance is not zero-sum in sim; faster games helped both tempo personas.

### B. Bot artifact (secondary — ~30%, actionable but narrow)

| Gap | Evidence | Fix class |
| --- | --- | --- |
| **Expansion Strategy under-scored on primary** | `persona.py`: expander primary boost for `military_maneuvers` (3.5) and `resource_surge` (2.5); **`expansion_strategy` not listed** (defaults 1.0). Draft boost (+2 tempo) exists but primary use is weak. | Persona-aware **primary** scoring only |
| **Global primary pool** | `economic_boom` **69** uses vs `expansion_strategy` **17** among all personas | Expander isn’t driving Expansion Strategy; other personas still spam Boom/Surge |
| **Balanced regained no brake refresh** | M3 added systems; expander brakes from parity sprint not re-validated against new VP sources | Re-audit `vp_lead` / `territory_sat` weights vs M3 features |

**Not recommended:** blanket +20% weight cuts to expander or global weight inflation.

---

## 6. M3 deltas that likely reopened the gap

Compared to [pre-M3 mixed 4p](2026-07-03-baseline-mixed-4p.md):

| Signal | Pre-M3 | M3 | Direction |
| --- | ---: | ---: | --- |
| Expander win % | 33.8% | **40.5%** | ↑ dominance |
| Balanced win % | 33.8% | 37.1% | ↑ slightly |
| Mean rounds | 6.1 | **5.8** | Faster |
| Battles / player-round | 0.224 | **0.274** | More combat |
| Contested att win % | 64.3% | **73.4%** | Attacker-favorable |
| Expansion Strategy primary | N/A (stub) | **17 uses** | New tempo tool |
| Whispers / artifacts / research | Off | On | More map hooks |

**Hypothesis H7a (design):** M3 increased **map scoring velocity** faster than it increased **economy scoring velocity**, restoring expander’s mixed-seat edge.

**Hypothesis H7b (bot):** Expander bots do not yet **prefer Expansion Strategy primary** enough to be realistic — but other personas still win the game when expander is seated, so bot gap alone cannot explain 40%.

---

## 7. Recommended levers (ranked, one-at-a-time)

Do **not** stack. Re-run `bracket-m2-smoke.json` (100 games) after each PROPOSED change.

| Priority | Lever | Type | Expected effect |
| ---: | --- | --- | --- |
| **1** | **Lever A pacing** — stretch mean rounds toward 7–8 at 4p (VP threshold, objective thresholds, or production — pick one) | Packet / rules | Slows expander closes; helps economist at 6–8p too |
| **2** | **Row tempo audit** — soften `frontier_lord` threshold (7→8 hexes) or delay `seat_of_empire` scoring window | Packet (PROPOSED) | Direct expander/seat race nerf without touching bots |
| **3** | **Expander primary scoring** — add `expansion_strategy` primary boost (3.5–4.0) in `persona.py`; verify draft→primary coherence | Bot (narrow) | Better bot realism; may **increase** expander unless paired with (1) or (2) |
| **4** | **Re-tune expander lead brake** — stronger `vp_lead` / `territory_sat` when ahead post-M3 | Bot (narrow) | Repeat parity sprint pattern; cap without killing solo 25% |

**Defer:** M4 Lords, global persona rebalance, 10 VP threshold change.

---

## 8. Test plan

| Step | Action | Pass bar |
| ---: | --- | --- |
| 1 | Accept this report; pick **one** lever from §7 | Owner choice |
| 2 | Encode PROPOSED change (packet or sim-only bot) | Checklist if canon |
| 3 | Re-run mixed 4p smoke (100 games) | Expander **≤35%** interim; stretch **≤30%** |
| 4 | Re-run solo 4p ladder (200 games) | All personas **20–30%** (no collateral) |
| 5 | If expander still >35% after two levers | Escalate to human 4p table; log round count + winner row objectives |

---

## 9. References

- [Mixed 4p M3 baseline](2026-07-03-baseline-mixed-4p-m3.md)
- [Mixed 4p pre-M3 baseline](2026-07-03-baseline-mixed-4p.md)
- [Persona parity diagnosis](2026-07-03-persona-parity-diagnosis.md)
- [Economist viability memo](2026-07-03-memo-economist-viability.md) — calibration stop rule
- `sim/aeonis_sim/agents/persona.py` — weights and draft/primary scoring
- `playtest/First_Playable_Packet.md` §4.4 — shared public row

**Analysis artifacts:** JSONL export `docs/reports/_tmp-h7-4p-m3.jsonl` (regenerable; not a durable baseline).
