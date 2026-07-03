# Sim implementation plan — Milestone 3 (card systems)

**Date:** 2026-07-03 · **Status:** ACTIVE (sim work, no canon changes except where marked PROPOSED)
**Owner scope:** `sim/` encode of First Playable card systems per the architecture doc (`2026-07-02-agent-playtest-simulation-design.md`, content milestone 3) — Whispers, full First Playable events, Artifacts/Remnants/Sites, Arcane Tier I, secret-objective completion.
**Prior state:** M1 core loop + Plan 3 MVP + M2 politics (events subset, draft, initiative, council, negotiation) — see `INDEX.md` sim track. 165 pytest green at plan time.

---

## 1. Why M3 now

M2 closed the politics layer; the sim still plays a **cardless** Aeonis. The biggest canon-vs-sim gaps left before Lord asymmetry (M4) are the shared decks: Whispers (26), Artifacts (24) + Remnants + Sites, Arcane Tier I (10), the 4 missing First Playable globals, all 9 exploration events, and half the packet's secret objectives. Until these land, balance findings (economist tempo, attacker win rate, council pass rate) carry a structural asterisk: bots race objectives in a world with no tactical interrupts, no relic economy, and no research.

M3 also carries one **PROPOSED canon experiment already landed** ahead of this plan: **Merchant Lord** (public objective, 8+ Gold) filling the row's sixth slot — economist memo Lever B (`../reports/2026-07-03-memo-economist-viability.md`). M3 gate reruns measure it at full system fidelity.

## 2. Gate (exit criteria)

Mirrors M1/M2 gates; all must hold at once on the final task's commit:

| Check | Bar |
| --- | --- |
| Pytest | green, including new per-card tests |
| Golden replays | regenerated post-M3; round-trip + determinism guard green |
| Chaos fuzz | no crash/invariant violation in chaos smoke |
| Mixed 4p smoke (`bracket-m2-smoke.json`, 100 games) | 100% completed, 0 crash/timeout/degenerate |
| Solo 4p (`bracket-m2-4p.json`, 200 games) | same |
| CI | new `bracket-m3-ci.json` added to `.github/workflows/sim.yml` (zero-fail gates + M3 sanity metrics) |
| Ledger | every M3 chapter ambiguity triaged in `playtest/Ambiguity_Ledger.md` (AL-25 closed or re-scoped) |
| Docs | baselines regenerated; `docs/reports/INDEX.md` + `docs/plans/INDEX.md` updated |

**Sanity metrics recorded (not hard gates initially):** first-artifact round distribution (packet target: round 3–4), whisper hand sizes at cleanup (≤7 without constant forced discards), research uptake per game, remnant income per round, mean rounds (Lever A watch: 8–10 target).

## 3. Tasks

Ordered by dependency; each task lands with unit tests, and regenerates goldens **only if** it changes decision-point sequence or resolution order (expected for Tasks 2, 3, 4, 5, 6, 7).

### Task 1 — Building roster completion (Forge, Academy, Bank, Market) — **DONE** (2026-07-03)

- [x] `BUILDING_SPECS` + build rules: **Forge**, **Academy**, **Bank**, **Market** (Cities only).
- [x] Upkeep in `production.py` — Forge/Academy mana upkeep with AL-8 suspension via `Tile.active()`.
- [x] Bank conversion auto-heuristic at Production & Upkeep (AL-26); Market 0-AP trade initiation (AL-27).
- [x] Tests: `sim/tests/test_advanced_buildings.py` + `test_types.py` specs.

### Task 2 — Remnants, exploration layer, missing FP globals

- [x] `PlayerState.remnants` + invariant (non-negative); Ruins hex control grants **1 Remnant/round** at Production & Upkeep (`Learn_to_Play` §Production step 5, `Artifacts.md` Remnant Sources).
- [x] **Explored flags**: hexes outside home clusters start unexplored; first unit entry (move, portal, retreat) triggers the entering player's exploration event, then marks explored. No fog — information stays open; only the trigger is tracked. **Log the interpretation as a new AL entry before encoding.**
- [x] **Exploration deck (9 FP cards, `Events.md`)**: Ancient Ruins (choice: search roll d6 vs leave for Renown), Trapped Vault (choice: lose unit vs 2 Gold), Speaking Stone Echo, Lost Cartographer (no-fog stub: +1 AP only — AL entry), Wandering Mercenaries, Cursed Ground (hex produces nothing until 2 Influence cleanse — cleanse as free-action decision point), Scattered Relics, Portal Instability, Ancient Vault Discovered (site + optional 1 AP claim).
- [x] **Missing FP globals**: `council_crisis` (Speaker must propose; −1 Renown on fail — wire into council phase), `open_roads` (Plains entry −1 AP min 1 this round), `ruins_unearthed` + `echo_of_the_old_empire` (create Artifact Sites; Echo also +1 Remnant to all).
- [x] Event deck grows 8 → 12; update event-frequency expectations in tests.
- [x] Tests: first-entry trigger uniqueness, each exploration card, each new global, remnant production.

### Task 3 — Artifacts, Sites, VP relics

- [ ] Artifact deck (24 ids per `Artifacts.md`), face-down draw, **purge 3 Remnants → draw** as free action on your Action-Phase turn.
- [ ] **Artifact Sites**: markers created by events; face-up card on site; claim by occupying + 1 AP (per `Artifacts.md` Acquisition); contested sites are territorial bait — no new combat rules.
- [ ] Ownership model: Lord Equipment (carry limit 2, attach to Lord; on Lord capture follow `Artifacts.md` transfer rules), Building Relics (attach to a controlled building; captured with the hex), Utility (held).
- [ ] **VP artifacts** (Crown of Aeonis, Eternal Forge, Shard of the Throne, Imperial Seal): +1 VP each checked at Cleanup & Checks (source tag `artifact`).
- [ ] Effects: encode faithfully where systems exist (stat mods, resource gains, recruit/build riders, combat riders); **stub with AL entry** where they need fog or unbuilt systems (e.g. Cartographer's Glass reveal). One-time purge effects as free-action decision points.
- [ ] Tests: purge-draw, carry limit, site claim, VP artifact scoring, at least one effect per category, transfer on capture.

### Task 4 — Arcane Tier I

- [ ] **Research action** (`Arcane.md` §4.2): 1 AP + listed cost, one discovery per action, grants **1 Remnant**; Tier I only (all Tier I have no prerequisites — sigil system deferred until Tier II, AL note).
- [ ] The **10 Tier I discoveries** (§7): encode effects (passives into combat/production/movement hooks; rituals as one-shot decision points). Stub-with-ledger any that reference disabled systems.
- [ ] Academy Specialty + once/round −1 Mana research discount (Task 1 hook).
- [ ] **Arcane Ascendancy primary** goes real: 2 Mana + free Tier I research (closes AL-25 for this card).
- [ ] Tests: research costs/limits, remnant grant, each discovery's effect, Academy discount.

### Task 5 — Secret objectives completion + objective draws

- [ ] Encode packet secrets missing from sim: **Hidden Arsenal** (built Fortress + win battle on that hex — track built-by), **The Quiet Knife** (gain hex via Influence: annexation/arbitration/Influence takeover — wire M2 council motions), **Borderbreaker** (units in 3 hexes pairwise ≥3 apart, `Objectives.md` concrete rule).
- [ ] **Round 3 second secret draw** (packet §4.4 setup; sim currently deals only 1 at setup) + secret cap 3 with draw-2-keep-1 at cap (`Objectives.md` §3.3).
- [ ] Real objective-draw effects: `winds_of_fortune` (draw public/secret choice; currently AP-only stub), Imperial Mandate primary (draw 1 secret when not holding Seat).
- [ ] Tests: each new secret, round-3 draw, cap behavior, draw effects.

### Task 6 — Whispers (26-card deck, timing windows, Sabotage)

The engineering core of M3 — reactive windows on top of the sequential decision-point model (pattern precedent: M2 negotiation sessions).

- [ ] Deck/discard/reshuffle; setup draw 2; Round Start draw 2; **draw 1 on any VP score** (`Whispers.md` §2); hand limit 7 with discard decision at Cleanup.
- [ ] **ACTION whispers** (0 AP, consume turn): enumerate alongside actions.
- [ ] **COUNCIL whispers** (5): windows at proposal (Political Leverage, Leaked Intelligence on agenda reveal), pre-tally (Backroom Deal), post-pass (Veto).
- [ ] **COMBAT whispers** (8): windows at Pre-Strike / Strike / Counterstrike / Retreat / Reinforce steps; one whisper per window per player per occurrence.
- [ ] **WHEN triggers**: event-keyed offers to eligible hands (Rallying Cry, War Profiteer, Emergency Conscription, Iron Resolve, Fortify Position…), initiative-ordered.
- [ ] **Sabotage**: response window after any whisper play; cancels, both discard, cannot be sabotaged.
- [ ] Movement/Arcane + Subterfuge cards (Forced March, Blink, Ley Line Surge, Waystone Activation, Saboteur, Mercenary Company, Relic Thief) — encode with AL entries where interpretation is needed.
- [ ] Bot heuristics: value model per category (combat swing, vote swing, economy delta); skip-by-default with targeted triggers, so games don't drown in offer windows. Cap enumeration per window.
- [ ] Observations: register new dp kinds → phases (`observations.py`); record whisper stats (played by category, sabotage rate).
- [ ] Tests: draw economy, hand limit, each timing window, sabotage counter-play, ACTION-consumes-turn, per-card effects (26).

### Task 7 — Strategy primaries/secondaries completion (close AL-25)

- [ ] **Diplomatic Decree** primary (2 Influence + Speaker token + immediate emergency motion via council machinery) and secondary (+2 Influence).
- [ ] **Expansion Strategy** primary (claim adjacent empty neutral + 1 pop) and secondary (2 Influence claim).
- [ ] **Tactical Reinforcements** primary (free recruit ≤2 ignoring city limit) and secondary (paid extra Recruit).
- [ ] **Imperial Mandate** primary (Seat → 1 VP else draw secret; +1 Influence) and secondary (2 Influence → draw 1 Whisper — Task 6 hook).
- [ ] Arcane Ascendancy secondary (research at cost +1 Mana, no AP).
- [ ] Update `PRIMARY_IMPLEMENTED` / `SECONDARY_EFFECTS`; remove stubs; persona draft scoring reviewed (no weight inflation — see Task 8 guardrail).
- [ ] Tests per card, including VP-source tagging for Imperial Mandate.

### Task 8 — Agents & reports

- [ ] Features: remnant/artifact value (progress toward purge-3, VP relics), research value, whisper hand pressure, new-building economy deltas. **Guardrail: calibration stop rule holds** — new features get modest cross-persona weights; no persona weight inflation to chase H8. Economist gets only fantasy-aligned hooks (Bank/Market/gold banking already covered by `gold_track`).
- [ ] Report sections: whispers (plays by category, sabotage rate), artifacts (first-artifact round, VP-relic share), research (discoveries/game), remnant economy; VP-source table gains `artifact` row.
- [ ] New hypotheses wired into evaluators: **H10** whisper draw rate keeps hands ≤7 without flooding (packet goal 9), **H11** first artifact by round 3–4 (packet goal 10), **H12** Merchant Lord lifts economist mixed win rate ≥5% without balanced/warmonger exceeding 40% (memo follow-up).

### Task 9 — M3 gate run

- [ ] Regenerate goldens; chaos smoke; 100-game mixed + 200-game solo brackets green per §2 table.
- [ ] Add `sim/configs/bracket-m3-ci.json` (20 mixed 4p, zero-fail + completed=1.0) to CI matrix.
- [ ] Regenerate `docs/reports/` baselines; update both INDEX files; triage ledger; record gate in `docs/plans/INDEX.md` sim track.

## 4. Sequencing & risks

**Order:** 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9. Remnants (2) precede artifacts (3) and research (4); whispers (6) come after artifacts because three cards reference relics/remnants; strategy completion (7) needs research (4) and whisper draws (6).

| Risk | Mitigation |
| --- | --- |
| Whisper reactive windows explode decision count / runtime | Offer windows only to hands holding a matching card; skip-by-default heuristics; per-window enumeration caps; watch runtime in CI smoke |
| Artifact effect sprawl (24 unique cards) | Category-pattern encode (persistent / one-time purge / WHEN); stub-with-ledger anything needing fog or M4 systems |
| Round length drifts further from the 8–10 target as VP sources multiply | Track mean rounds at every task commit; if <6 or >12, pause and report before continuing (Lever A escalation per memo §7) |
| Golden replay churn across 6 tasks | Regenerate per task that shifts sequence; keep per-task commits so bisection stays cheap |
| Ambiguity backlog (Whispers/Artifacts wording) | AL entry **before** encoding any interpretation; expected new entries: unexplored-hex definition, no-fog stubs, whisper response ordering details |

## 5. Merchant Lord experiment (landed with this plan)

- **Canon (PROPOSED):** `rules_and_systems/Objectives.md` §4.4 + packet §4.4 sixth slot; Council Power stays out until the full-deck audit.
- **Sim:** `objectives.py` (+`merchant_lord`, row = 6 cards), features progress, tests; goldens + baselines regenerated at land time (see `docs/reports/INDEX.md` for the post-change numbers).
- **Measure:** H12 at M3 gate. **Kill criteria:** if after M3 gate (full card systems) economist mixed 4p stays <5% **or** the card is scored by ≥60% of players per game (free VP, no tension), pull it from the row and record the outcome here and in the memo.
- Promotion to canon (Stage I deck) only after a human table per playtest constraints.

## 6. References

`../reports/2026-07-03-memo-economist-viability.md` (Lever B, H12) · `2026-07-02-agent-playtest-simulation-design.md` §5 · `playtest/First_Playable_Packet.md` §4 · `rules_and_systems/{Whispers,Artifacts,Arcane,Events,Objectives,Buildings,Strategy}.md` · `.cursor/rules/aeonis-mechanics-sim-sync.mdc`
