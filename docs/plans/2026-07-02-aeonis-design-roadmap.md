# Aeonis Design Roadmap — Assessment & Plan

**Date:** 2026-07-02
**Status:** Executed (doc workstreams) — Phase 0 register complete; Phase 2/3 content built; Phase 4-6 artifacts drafted. Remaining work is real-world: playtesting, art, quotes, audience.
**Scope:** Full-project stocktake and phased plan to take Aeonis from "documented design" to "fun, playable, Kickstarter-ready fantasy counterpart to TI4."

## Execution log (2026-07-02)

- **Phase 0:** all 15 register items fixed (see §4; `INDEX.md` "Design decisions (resolved)" updated; `TBD.md` retired).
- **Phase 2:** canon 8-card Strategy deck rewritten in `Strategy.md` (opt-in secondaries, 2-card draft at 3-4p, bounty gold, Imperial Mandate replaces Arcane Convergence); `Objectives.md` (24 public Stage I/II + 20 secret); agenda deck to 20 cards incl. Elections (`High_Council.md`); event decks to 24+24 + 6 milestones (`Events.md`); `Advanced_Units.md` chapter; `Diplomacy.md` chapter (binding-deal rules, Accords, NPCs out of core).
- **Phase 3:** 4 expansion Lords drafted (Serathis/water, Morvane/necromancy, Tsuvara/nomad, Ozren/schism); `lore/Lore.md` rewritten to canon + `lore/Naming_Bible.md`; Whisper deck expanded to 44; `playtest/Full_Game_Scope.md` defines the Tier II/III + advanced-units scope.
- **Phase 4:** `playtest/Balance_Dashboard.md` (metrics, Lord tracker, tuning levers, blind-test gate) + `playtest/session_log.csv`.
- **Phase 5:** `rulebook/Learn_to_Play.md` + `rulebook/Player_Aid.md` drafts; `components/Production_Manifest.md` (manufacturing BOM).
- **Phase 6:** `marketing/Pitch.md`, `marketing/Comps_Analysis.md`, `marketing/Campaign_Math.md`.
- Codex manifest updated for all new docs.

---

## 1. Where the game stands today

### Strong (keep building on this)

- **Rules spine is real.** `Round_Structure.md` gives a clean TI4-shaped round (Events → Strategy draft → High Council → rotating Action Phase → Production & Upkeep → Cleanup) and most chapters respect its timing windows.
- **Mature subsystems:** Combat (battle line + reserves, sieges, Lord capture), Buildings (full roster + 8 Legendary capstones), Artifacts (24 relics, Remnants, Sites), Whispers (26-card tactical deck), Arcane Tier I (20 discoveries across 5 schools).
- **8 fully specced Lords** with consistent sheets: faction mechanic, passive, active, unique tile, 2 faction discoveries, Legendary Building, objectives, strategy notes, playtest watch-items.
- **First Playable Packet** defines a coherent 3–8 player test contract with explicit inclusions/exclusions and 11 observation goals.
- **Working infrastructure:** Codex app + manifest, agent roles/templates/checklists, dated design-plan workflow in `docs/plans/`.

### Weak or missing (the gaps this plan closes)

1. **Zero logged playtests.** The single biggest risk. Everything downstream (balance, pacing, Kickstarter claims) is speculative until the game hits a table repeatedly.
2. **Card decks are frameworks, not decks.** Strategy cards: 8 loose examples with at least one broken effect (Economic Boom: 5 Gold → 3 VP vs a 10 VP win). Events: ~18 samples. Objectives: 12. Agenda deck: 8 cards, defined only in the playtest packet, not in `High_Council.md`.
3. **Lore is a skeleton (~10%)** and contradicts canon — it names placeholder factions (Magi Guild, Iron Vanguard, Kaelthar) instead of the 8 real Lords; no geography, timeline, or racial encyclopedia.
4. **Orphaned/deferred systems:** "Cast Spells" is costed in `Actions.md` with no owning chapter; advanced/mythic units exist on Lord sheets as "Future Content" with no unlock/upkeep rules; alliances, NPCs/neutral armies, and espionage are mentioned but undefined.
5. **Known inconsistencies** (full list in §4): Research AP (1 flat vs 1/2/3 by tier), Whisper deck size (24 vs 26), High Council step numbering, "Imperial Seat" vs "Throne of Power," passive city-adjacency control vs unit-based ZOC, Cavalry plains movement wording, Speaker rotation ambiguity.
6. **Components list is incomplete for its own First Playable:** Forge/Academy/Bank/Castle and all 8 Legendary Buildings have no physical tokens specified; no scaling math for 5–8 players; zero cost/manufacturing data.
7. **Marketing is aspirational only:** checklists and a phased outline, but no pitch assets, audience data, or budget. Positioning is now locked (see §2) — execution remains.

### TI4-parity snapshot

| TI4(+PoK) system | Aeonis equivalent | Status |
|---|---|---|
| Strategy cards | Strategy cards (primary/secondary, initiative) | Framework + 8 rough examples |
| Agenda phase | High Council (player-authored motions + agenda deck) | Procedure solid; deck thin; split across two docs |
| Tech tree | Arcane Discoveries (schools, sigils, tiers) | Tier I done; II/III drafted, untested |
| Objectives | Public/secret 2 VP objectives | Rules done; only 12 cards |
| Action cards | Whispers | Strong for First Playable; scale to 40–60 later |
| Relics/exploration | Artifacts + Remnants + hex-entry events | Strong (best-developed system) |
| Mecatol Rex | Imperial Seat (+1 VP/round held) | Defined; needs playtest pressure |
| Factions (17–25) | Lords (target 12–16) | 8 done |
| Leaders/heroes | Lord-on-the-map with capture rules | Distinctive; a genuine differentiator |
| Mechs/war suns/fleets | Advanced & mythic units | "Future Content" — no system chapter |
| Trade goods economy | Negotiated trade + Influence lobbying | No tokenized economy; may be fine, needs testing |
| Command tokens | AP pool + banking | Simpler; core identity choice |

---

## 2. Strategic decisions — LOCKED 2026-07-02

Recorded in `marketing/Positioning.md` (canonical) and propagated to `Development_Plan.md` and `Components.md`.

- **D1 — Session length: 4–10 hours.** The complexity and length are part of the allure to the hardcore strategy audience; this matches the real-world TI4 experience. The First Playable packet stays compressed for iteration speed — that's a testing convenience, not the product target.
- **D2 — Positioning: "If you love TI4, you will probably love Aeonis."** Differentiation is the fantasy setting and the mechanics it unlocks (capturable Lords, sieges/flanking/ZOC, Arcane Discovery, Whispers, Artifacts, player-authored council motions). The pitch is additive, not adversarial.
- **D3 — Components: acrylic standees baseline; custom Lord miniatures as the flagship Kickstarter stretch goal.** All cost/MSRP modeling assumes standees.
- **D4 — Player count: 3–8 committed.** 2-player is out of scope for launch.
- **D5 — Language: "in the tradition of" / "inspired by."** Friendly "for fans of TI" comparisons are fine in community contexts; never "clone/derivative/reskin." All terminology, lore, and card text stay original.

---

## 3. Phased plan

### Phase 0 — Canon hygiene sprint (1–2 weeks of doc work)

Fix every known inconsistency so playtesting starts from one truth. Use `agents/checklists/Canon_Change_Checklist.md` for each.

1. **Research AP:** pick tiered (1/2/3, per `Arcane.md`) and propagate to `Actions.md`.
2. **Whisper deck size:** reconcile 24 vs 26 across `INDEX.md`, `Whispers.md`, `Components.md`, `First_Playable_Packet.md`.
3. **High Council step number** in `High_Council.md` → step 4, matching `Round_Structure.md`.
4. **Terminology:** enforce "Imperial Seat" everywhere (per `INDEX.md` preference); sweep for "Throne of Power," "Palantír," "IP," "spell" (→ Discovery).
5. **Speaker rotation:** commit to clockwise (as `Round_Structure.md` says) and delete the "pick one" in `High_Council.md`.
6. **Cast Spells:** remove from `Actions.md` (Arcane uses Discoveries/Rituals) or write the owning chapter. Recommendation: remove for now.
7. **Control vs ZOC:** resolve the tension between passive city-adjacency control and unit-based ZOC in `Tiles.md` — define exactly when unoccupied controlled hexes flip.
8. **Cavalry movement:** delete or formalize "1 AP per 2 hexes on Plains" against the standard path-cost table in `Movement.md`.
9. **Economic Boom:** kill the 5 Gold → 3 VP option in `Strategy.md`.
10. **Legendary Build cost exception (4 AP):** cross-reference in `Actions.md`.
11. **Agenda deck:** give it a canonical home in `High_Council.md` (rules) with the card list in the playtest packet.
12. **Components audit:** add Forge/Academy/Bank/Castle/Legendary tokens and 5–8p scaling counts to `Components.md`.
13. **Retire `TBD.md`** into `INDEX.md`'s "Remaining design work" or a living backlog; delete the stale duplicate.
14. **Renown earn rates:** define frequency/timing for hex-capture Renown (per hex? once/round?) in `Renown.md`.

**Exit criteria:** a fresh reader can build the First Playable from the docs with zero contradictions.

### Phase 1 — Playtest engine (start immediately; runs forever)

The game's fun is unproven. Everything else in this plan is subordinate to table time.

- **Build the physical PnP kit** from `Components.md` (post-audit). Text cards are fine.
- **Build a digital table** (Tabletop Simulator or Screentop.gg) — this multiplies test volume and later doubles as the Kickstarter demo.
- **Solo-test first:** run 2–3 full games playing all seats yourself to catch rules that don't function at all, before spending friends' goodwill.
- **Then group tests:** target a cadence (e.g., 2 sessions/month minimum). Vary player count (3, 5, 8) and Lord matchups.
- **Log every session** with `agents/templates/Playtest_Report_Template.md`, tracking the packet's 11 observation goals plus: total time, time-per-round, downtime between turns, VP pace per round, kingmaking/runaway-leader incidents, and each player's "would you play again?" answer.
- **After each session:** 3–5 hypotheses → doc patches → next session. This is workflow D in `AGENTS.md`; actually run it.

**Exit criteria for "First Playable validated":** 6+ logged games; full-game sessions trending inside the 4–10 hour target (D1) with downtime players accept; every Lord picked at least twice; no rules argument that required a designer ruling mid-game.

### Phase 2 — Complete the core systems (parallel with Phase 1 iteration)

Turn frameworks into finished, testable content. Priority order:

1. **Strategy card deck:** finalize 8 tuned cards (TI4's most load-bearing system). Each needs: number, primary with AP cost, secondary with trigger window, and a reason to be picked at every game stage. Use `agents/templates/Strategy_Card_Template.md`.
2. **Objective decks:** expand to ~20 public (consider TI4-style Stage I/II escalation) + ~20 secret. Every objective must be verifiable at Cleanup and reference existing systems only.
3. **Agenda/Council deck:** 16–24 cards mixing laws (persistent), directives (one-shot), and elections (titles), so the High Council phase has drawn content in addition to player motions.
4. **Event decks:** ~24 global + ~24 exploration, using `agents/templates/Event_Template.md`, with explicit timing windows.
5. **Advanced units chapter:** the system rules (unlock gates, upkeep, recruit limits) for the 16 already-designed faction units — this is the Prophecy-of-Kings-style depth lever, and it matters more now that the full game targets 4–10 hours (D1).
6. **Diplomacy formalization:** decide whether alliances/ceasefires get components (support-for-the-throne analogue?) or stay table-talk. Write the answer down either way.
7. **NPC/neutral forces:** decide in or out for launch. Recommendation: out of the core box; expansion hook.

### Phase 3 — Content breadth & world

- **Lords 8 → 12** (launch target; 12–16 per dev plan). The `INDEX.md` wishlist is good: naval/coastal, necromancy (unlocks the deferred NEC school), nomadic alliances, religious schism. Each new Lord must explore mechanical space the current 8 don't touch.
- **Lore rewrite:** replace the placeholder `lore/Lore.md` content with canon — the 8+ real Lords and races, the Eternal Empire timeline, a named world map whose regions justify the tile types, Speaking Stones (drop "Palantír"), and the Imperial Seat. The Lord sheets already contain the best lore in the repo; harvest and unify it.
- **Naming bible:** one doc of defined terms, faction/race names, and pronunciation — feeds rulebook, cards, and marketing copy.
- **Whispers to 40–60 cards** and Arcane Tiers II/III enabled, once First Playable balance is stable.

### Phase 4 — Balance & full-game scope

- Stand up a lightweight **balance dashboard** (even a spreadsheet): win rate by Lord, VP source distribution, average round count, resource-income curves. The `Balance_Analyst` role prompt exists; give it data.
- Tune the known hot spots: Imperial Seat VP rate, Lord-capture reward loop (+1 VP, +2 Renown, ability lockout), catch-up events, AP economy (+2 City cap, Guild Hall, Renown thresholds stacking).
- **Pacing across the 4–10 hour arc:** with long sessions locked in (D1), mid-game sag is the enemy — verify each game hour introduces something new (arcane tiers unlocking, agenda escalation, artifact sites, advanced units).
- Run **blind playtests** (groups learning from the rulebook alone, no designer present) — the gate between "works with the author in the room" and "publishable."

### Phase 5 — Production readiness

- **Real rulebook:** the chapter docs are a designer's reference, not a rulebook. Write a learn-to-play + reference split (TI4's own two-book model is the right pattern), with setup diagrams and worked examples.
- **Player aids:** the round-flow / action-cost / unit-stat card `INDEX.md` already calls for.
- **Final component manifest with counts and target costs**, on the standee baseline (D3): acrylic standees for all units and Lords, tokens/tiles for the rest. Spec the Lord miniature stretch-goal sculpts separately. Get 2–3 manufacturer quotes (e.g., LongPack, Panda, Whatz) at 1,500/3,000/5,000 units to set the funding goal and MSRP.
- **Art direction:** style guide first, then key art (box cover, 2–3 Lords, one map spread) — the minimum for a credible campaign page. Full card art can follow funding.

### Phase 6 — Kickstarter runway (start audience-building 6–12 months before launch)

- **Positioning execution** from `marketing/Positioning.md` (D2/D5): every asset leads with "If you love TI4, you will probably love Aeonis" framed additively; comps analysis (TI4, Eclipse, Heroes of Land Air & Sea, Arcs, Oath — what they promised, charged, and delivered).
- **Community:** BGG page, Discord, devlog cadence; share Lord reveals and playtest stories. The email list size at launch is the single best funding predictor.
- **Demo assets:** the digital table from Phase 1 becomes the reviewer/preview copy; send physical prototypes to 3–5 reviewers whose audience overlaps TI4/4X fans.
- **Campaign math:** funding goal = (manufacturing at MOQ + freight + fulfillment + art/graphics + platform fees + 15% contingency); price tiers from Phase 5 quotes on the standee baseline; stretch goals from already-designed-but-cut content (Lord miniatures first, then Lords 13–16, advanced units).

---

## 4. Known inconsistency register (Phase 0 backlog)

| # | Issue | Owning doc | Also touch |
|---|---|---|---|
| 1 | Research AP: flat 1 vs 1/2/3 by tier | `Arcane.md` | `Actions.md` |
| 2 | Whisper deck 24 vs 26 | `Whispers.md` | `INDEX.md`, `Components.md`, `First_Playable_Packet.md` |
| 3 | High Council labeled "Step 3" | `High_Council.md` | — |
| 4 | "Imperial Seat" vs "Throne of Power" / "Palantír" | `Victory.md`, `Lore.md` | global sweep |
| 5 | Speaker rotation "clockwise or initiative — pick one" | `High_Council.md` | `Round_Structure.md` (canon: clockwise) |
| 6 | "Cast Spells" costed but undefined | `Actions.md` | `Arcane.md` |
| 7 | Passive city-adjacency control vs unit-based ZOC | `Tiles.md` | `Movement.md`, `Combat.md` |
| 8 | Cavalry "1 AP per 2 hexes on Plains" | `Movement.md` | — |
| 9 | Economic Boom 5 Gold → 3 VP | `Strategy.md` | `Victory.md` |
| 10 | Legendary Build 4 AP exception not cross-referenced | `Buildings.md` | `Actions.md` |
| 11 | Agenda deck has no rules-chapter home | `High_Council.md` | `First_Playable_Packet.md` |
| 12 | Missing component counts (Forge/Academy/Bank/Castle/Legendaries; 5–8p scaling) | `Components.md` | `Buildings.md` |
| 13 | `TBD.md` stale | `TBD.md` | `INDEX.md` |
| 14 | Renown-per-hex-capture frequency undefined | `Renown.md` | `Combat.md` |
| 15 | Strategy cards say "spell," canon is "Discovery" | `Strategy.md` | — |

---

## 5. Next 30 days

1. ~~Lock decisions D1–D5~~ — **Done 2026-07-02** (`marketing/Positioning.md`).
2. ~~Execute the Phase 0 register~~ — **Done 2026-07-02** (see Execution log).
3. ~~Pitch copy draft~~ — **Done 2026-07-02** (`marketing/Pitch.md`).
4. **Print/assemble the PnP kit** from `components/Components.md` and run **two solo playtests**; log them in `playtest/Balance_Dashboard.md` + `playtest/session_log.csv`. ← the critical path now
5. Start the digital tabletop build (TTS or Screentop) in parallel.
6. Read the new Strategy deck, Objectives, agenda deck, and event decks with fresh eyes; sanity-pass numbers before printing.
7. Begin audience groundwork: BGG page draft + landing page from `marketing/Pitch.md`.
