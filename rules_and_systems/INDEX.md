# Rules & Systems Index

This folder is the current "rulebook draft" for **Aeonis: The Shattered Empire**.

## Chapters (current)

- **`../playtest/First_Playable_Packet.md`**: 3-8 player playtest packet (map setup, reduced decks, objectives/events, Lord sheets, and scaling guidance).
- **`../components/Components.md`**: Physical component checklist (First Playable).
- **`Lore.md`**: Setting foundation (fall of the empire, Speaking Stones, rediscovered magic, banished lords, artifacts, religion, throne).
- **`Round_Structure.md`**: Canonical timing diagram for a full round (round start -> events -> strategy selection -> council -> rotating actions -> production/upkeep -> cleanup).
- **`High_Council.md`**: Political procedure (speaker, proposals, negotiation, voting, laws/decrees/titles) that other systems reference.
- **`Actions.md`**: Action Point pool + rotating turns; variable action costs (Build at 3 AP); canonical Recruit rules (costs, placement, limits); passing and AP banking.
- **`Strategy.md`**: The canon 8-card Strategy deck; initiative order; primaries + opt-in secondaries; draft order (lowest VP picks first); 2-card draft at 3-4 players; bounty gold on undrafted cards.
- **`Movement.md`**: AP-based movement, terrain costs, portals/teleportation, Cavalry flanking, and council tie-ins.
- **`Tiles.md`**: Terrain production + buildings; special tiles; control/borders; canon ZOC framework (unit-based, not passive control).
- **`Combat.md`**: Canon combat (battle line + reserves, one battle round per Attack, sieges as the multi-turn exception); softened Lord capture (+1 VP, ability lockout).
- **`Arcane.md`**: Arcane discovery "tech tree" (schools, tiers, AP + resources), including Lord-specific paths.
- **`Population.md`**: Population pool + cap + growth; unit/building population costs; events and synergy notes.
- **`Trade_Taxes.md`**: Player-initiated trade (AP cost) + upkeep/taxes and consequences of non-payment.
- **`Events.md`**: Exploration/global/local/milestone events; triggers, examples, and catch-up events (Populist Uprising, Winds of Fortune).
- **`Renown.md`**: Renown gains/uses/threshold bonuses; optional decay.
- **`Victory.md`**: VP sources (objectives, council titles, artifacts/buildings, throne, combat captures, events); 10 VP threshold; 8 VP short-game variant.
- **`Buildings.md`**: Canon building list (including Guild Hall, Bridge), costs, and how buildings interact with Population/upkeep.
- **`Whispers.md`**: Whisper Cards -- shared tactical card deck representing Speaking Stone intelligence and secret preparations. Draw, hand limit, timing windows, 26-card First Playable list.
- **`Artifacts.md`**: Artifact deck (24 unique relics), Remnants, event-driven Artifact Sites, three categories (Lord Equipment, Building Relics, Utility), and VP-bearing artifacts.
- **`Objectives.md`**: Owning chapter for the objective system: Stage I/II public decks (24), secret deck (20), draw rules and secret-objective hand cap.
- **`Diplomacy.md`**: Which deals the rules enforce (immediate exchanges binding; promises not), the Accord system (formal alliances), and the NPC-factions decision (out of core).
- **`Advanced_Units.md`**: Faction Elite/Advanced/Mythic units: unlock gates (Forge / Tier II / Legendary), recruit costs, on-map limits, upkeep, and the design contract. Full game only.

## Lord design contract

Every new or redesigned Lord must meet all four signature tests:

1. **Bends one core system:** breaks or replaces a rule every other player follows, rather than only adding a numeric discount.
2. **Visible most rounds:** an observer can identify the Lord from normal play patterns during rounds 2–4.
3. **Creates a distinct victory lean:** the bend points toward a strategy and VP-source mix no other Lord executes in the same way.
4. **Teachable in one sentence:** the signature can be stated without introducing an undefined resource or global keyword.

Keep three abilities per sheet; redesigns replace weak abilities rather than inflating ability count. The teaching pair (Rakhis and Vharok) must remain setup-simple. Each signature must name its timing window, use existing system hooks, include counterplay or an opportunity cost, and be encoded in `sim/` when that system is in simulator scope.

## Design decisions (resolved)

These items were previously "red flags" and have been addressed:

- **Build AP cost**: Reduced from 4 to **3 AP** (see `Actions.md`).
- **City AP bonus cap**: Capped at **+2 AP from Cities** (see `Actions.md`).
- **Recruit rules**: Canonical Recruit action defined (1 AP, up to 2 units per City, resource + Population costs; see `Actions.md`).
- **Strategy draft order**: Committed to **lowest VP picks first** (see `Strategy.md`).
- **Event Phase timing**: Moved **before Strategy Selection** so events set the tone for the round (see `Round_Structure.md`).
- **VP threshold**: Standard game is **10 VP** (up from 8/12; aligns with TI4 scale). Short game variant at 8 VP (see `Victory.md`).
- **Secret objectives**: Reduced to **2 VP** (same as public) to prevent hidden blowouts (see `Victory.md`, `First_Playable_Packet.md`).
- **Lord capture**: Softened to **+1 VP** (down from 2); "cannot score VP" removed; replaced with **ability lockout** while captured (see `Combat.md`).
- **ZOC rules**: Clarified that ZOC is generated by **military units** (not passive hex control or buildings). Cavalry ignore ZOC penalty on first ZOC hex per Move (flanking). See `Tiles.md`, `Movement.md`.
- **Catch-up mechanics**: VP-based draft order + 2 catch-up global events (Populist Uprising, Winds of Fortune). See `Strategy.md`, `Events.md`.
- **Lord combat stats**: Differentiated across all 8 Lords to match faction identity (previously all identical d8/d8/3HP/2Move).
- **Player count**: First Playable now supports **3-8 players** with scaling guidance (see `First_Playable_Packet.md`).
- **Lord roster (8 Lords)**: Cassian (Human, economy), Seraphel (Human, arcane burst), Vharok (Human, fortress), Elyndra (Elven, growth), Rakhis (Djinnborn, cavalry raids), Nyxara (Umbral, espionage/Whispers), Auriel (Luminari, Renown/council), Thal'rik (Voidborn, portals).
- **Artifact system**: 24 unique relics in a shared deck; Remnant acquisition (3 Remnants = draw 1 artifact); event-driven Artifact Sites; 3 categories (Lord Equipment, Building Relics, Utility); 4 VP-bearing artifacts; full system in First Playable.
- **Buildings overhaul**: Forge/Academy/Bank finalized with concrete effects; upgrade system removed (covered by Arcane Discoveries + Building Relics); 8 Legendary Buildings defined as faction capstones (1 per Lord, 2 VP, +2 Renown, multi-gate prerequisites, 4 AP + resources to build); full building roster in First Playable.
- **Research AP is tiered**: Tier I = 1 AP, Tier II = 2 AP, Tier III = 3 AP (see `Arcane.md`; `Actions.md` matches).
- **"Cast Spells" removed**: There is no separate spellcasting action. Magic is expressed through Arcane Discoveries (passives, Rituals, Upgrades). Terminology sweep: "spell" is not a rules term.
- **Speaker rotation**: Clockwise at Cleanup & Checks (canon in `Round_Structure.md`; `High_Council.md` matches).
- **Control model unified**: Control is gained by unit presence at Round Start, conquest, occupation of neutral hexes, buildings, a 2-Cleanup-check Adjacency Claim near Cities/Towers, Influence/council, or explicit abilities. Cities/Towers project *influence* (claim priority), not instant control. See `Tiles.md`.
- **Cavalry movement**: Cavalry pay normal terrain costs (the "1 AP per 2 hexes on Plains" rate was cut); their identity is 2-hex range + ZOC flanking.
- **Renown from hex capture**: +1 Renown, at most once per round (see `Renown.md`).
- **Agenda deck**: Canonical rules live in `High_Council.md` §3.2a; the First Playable card list stays in the playtest packet.
- **Whisper deck size**: 26 cards in First Playable (see `Whispers.md`).
- **Terminology locked**: "Imperial Seat" (never "Throne of Power"), "Influence" (never "IP"), "Speaking Stones" (never "Palantír"), "Discovery/Ritual" (never "spell").
- **`TBD.md` retired**: Its open items were folded into "Remaining design work" below.
- **Plan 3 MVP — VP legibility (2026-07-03, sim-validated):** First Playable slice locked for sim and doc propagation: **shared public objective row** (6 cards; 2 revealed at setup, +1 per round from round 2); **Coronation Rite** replaces Imperial Seat +1/round drip (Lord on Seat hex → +1 VP/round; **third total** Rite → +2 VP once per player per game); **objective scoring at Cleanup & Checks** (AL-5); **VP permanence** for objectives and Rite; **population cap/pool** clarity (AL-1, AL-4). Lord capture stays **+1 VP**. Sim regression gates passed: Bracket A 4p (winner objective ~68%), mixed B/C 7–8p post persona-parity (winner objective ~71%, H7 persona parity). *Sim-only until human playtest.* See `../playtest/First_Playable_Packet.md`, `Victory.md`, `../docs/plans/2026-07-03-plan-vp-legibility-mvp.md`.
- **Ambiguity Ledger closed for M1 sim (2026-07-03):** All AL-1–AL-20 entries resolved in `../playtest/Ambiguity_Ledger.md` — map desert placement between home pairs (AL-3), City production clarity (AL-13), contested Adjacency sim rule (AL-14), involuntary Population overflow (AL-15), Coronation milestone once per game (AL-18), plus combat/map fidelity from the M1 sprint.
- **Plan 5 — Core Lords parity (2026-07-09, promoted):** Six launch signatures now bend core systems: Cassian's off-turn Trade/binding vote contract, Seraphel's Polymath research tempo, Elyndra's controlled-Forest network, Vharok's built-hex Bastions, Auriel's sanctified motion, and Rakhis's Sandstride. Nyxara's Whisper economy and Thal'rik's Portal topology remain unchanged anchors. The First Playable packet and derived rulebook carry signature reminders; the M4 simulator foundation encodes Lord identity, starting state/stats, rotating assignments, and deterministic signature hooks. See `../docs/plans/2026-07-02-plan-core-lords-parity.md`.
- **First Playable round pacing (2026-07-12):** Design and sim balance targets use **6–8 mean rounds** to game end at 10 VP (not the earlier Plan 3 aspirational 8–10). Post-M4 baselines land ~6.75–6.96; owner accepted that band. Do **not** stretch via VP12 alone (killed — see `../docs/reports/2026-07-03-vp12-pacing-memo.md`). Track in `../playtest/Balance_Dashboard.md` and `../playtest/First_Playable_Packet.md`.
- **Rakhis balance ladder Dial 1 (2026-07-12):** Removed Oasis Wellspring owner-only once-per-round Cavalry −1 Gold recruit. Tile keeps +1 Population / +1 Gold and Farm-yes / Tower-no. Sandstride and Hit and Run unchanged. Sim: `recruit.py`; sheet: `../lords/Rakhis.md`. See ladder memo in `../docs/reports/`.
- **Rakhis balance ladder Dial 2 (2026-07-12):** Hit and Run is **once per game** (was once per round). Sandstride unchanged. Sim: `lords/rakhis.py` + `game.py` (`lord_game` flag); sheet: `../lords/Rakhis.md`.
- **Rakhis balance ladder Dial 3 (2026-07-12):** Sandstride no longer ignores enemy ZOC surcharges. Keeps Desert 1 AP and once-per-battle pre-Pre-Strike retreat. Sim: `move.py`; docs: `Movement.md`, `Tiles.md`, sheet, First Playable, Learn to Play.
- **Rakhis balance ladder Dial 3b (2026-07-12):** Tried removing pre-Pre-Strike retreat — **reverted same day** (solo/mixed win rates rose vs Dial 3). See `../docs/reports/2026-07-12-rakhis-ladder-dial3b.md`. Current Sandstride = Dial 3.

- **Six improvement plans (2026-07-02, PROPOSED — not canon):** combat aggression tuning, AP economy flattening, VP legibility, 6–8 player scaling (incl. a future `Map_Construction.md` chapter), core-Lords parity pass, and bookkeeping reduction. See `../docs/plans/INDEX.md`. None of their changes apply until playtested and recorded under "Design decisions (resolved)" above.
- **Lakes / water**: Core rules are defined (impassable, Bridge exception). Consider adding more water-related events or abilities.
- **Additional Lords**: Roster is now **8 Lords** (sufficient for 8-player games). Long-term goal: a much larger roster of Lords with unique races and playstyles so that every session feels different even at the same player count. Future Lords should explore untapped design space (naval/coastal, necromancy, nomadic alliances, religious schisms, etc.) and introduce new faction mechanics that interact with existing systems in novel ways.
- **Dynamic market** (from retired `TBD.md`): fluctuating resource values driven by events/supply. Unscheduled.
- **Tutorial scenario** (from retired `TBD.md`): a simplified learning mode; belongs with the rulebook work (`../rulebook/`).
- **Faction Strategy Cards**: optional variant contract exists in `Strategy.md` §5.1; no cards designed yet.
- **Expansion Lord balance**: Lords 9-12 (Serathis, Morvane, Tsuvara, Ozren) are drafted as expansion roster and need dedicated playtest passes before joining the rotation.

## Related docs outside this folder

- `../lords/`: 12 faction sheets (8 launch + 4 expansion roster). Each new Lord brings a unique race, faction mechanic, and playstyle.
- `../rulebook/Learn_to_Play.md` + `../rulebook/Player_Aid.md`: teaching book and quick reference.
- `../playtest/First_Playable_Packet.md` + `../playtest/Full_Game_Scope.md`: the two test scopes.
- `../playtest/Balance_Dashboard.md`: metrics, Lord win rates, and tuning levers.
- `../components/Components.md` (prototype) + `../components/Production_Manifest.md` (manufacturing BOM).
- `../marketing/Positioning.md`: locked product decisions (4-10 hours, 3-8 players, standees + minis stretch).

_End of index._
