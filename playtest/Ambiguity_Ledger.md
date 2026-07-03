# Ambiguity Ledger

Rules questions found while encoding the docs into the simulator
(`sim/`). Each entry: the question, the interpretation the engine uses, and
the doc that should own the canonical answer. Triage by either patching the
owning doc (then the engine) or accepting the engine interpretation into
canon.

**Milestone-1 fuzz baseline (100 chaos games, seeds 1000-1099):** `verdicts: {'completed': 98, 'degenerate': 2}`

| ID | Question | Engine interpretation | Owning doc | Status |
|---|---|---|---|---|
| AL-1 | Packet §3.3 says starting Pop Cap 10, but `Population.md` grants +3 cap per City — a starting player (1 City) would exceed 10 with any base ≥ 8. What is the base cap? | **Base cap 7** + 3 per controlled City = 10 at start with one home City | `Population.md` | **Resolved** (2026-07-03, Plan 3 MVP) |
| AL-2 | Movement cost of Ruins hexes is undefined in `Movement.md` §2 | 1 AP (treated as easy terrain) | `Movement.md` | **Resolved** (engine: `TERRAIN_COST[RUINS]=1`) |
| AL-3 | Deserts placed by shuffle, not "between each pair of home clusters" | One Desert per adjacent home-cluster pair on the neutral ring | `First_Playable_Packet.md` §3.1 | **Resolved** (2026-07-03, M1 fidelity sprint) |
| AL-4 | Packet §3.3 says "Population Pool: 10 (full at start)" but starting units occupy 4 Population — is the pool 10 or 6? | **Pool 6** — starting units consume Population (cap 10, 4 in units) | `First_Playable_Packet.md` §3.3 | **Resolved** (2026-07-03, Plan 3 MVP) |
| AL-5 | When are objectives claimed/scored? No timing window in packet §4.4 or `Victory.md` | **Cleanup & Checks**; once per card per player; no claim action | `Victory.md` | **Resolved** (2026-07-03, Plan 3 MVP) |
| AL-6 | Does building a Bridge on a neutral Lake grant control of the Lake hex? | Yes — builder controls the bridged Lake | `Tiles.md` | **Resolved** (engine: `build.py`) |
| AL-7 | Defender choice to Hold the Walls for Cities | Auto-declare in First Playable / sim (City retreat banned) | `Combat.md` §6.1 | **Resolved** (2026-07-03, doc + engine) |
| AL-8 | What happens when Castle upkeep (2 Gold) cannot be paid? | Castle effects suspended for the round; building persists | `Buildings.md` | **Resolved** (engine: `production.py`) |
| AL-9 | Lord release when Home City is enemy-held | Nearest safe controlled hex; stay captured if none | `Combat.md` | **Resolved** (engine: `cleanup.py`) |
| AL-10 | Defender win definition for objectives | All attacker committed units eliminated | `Combat.md` | **Resolved** (engine: `combat.py`) |
| AL-11 | Captured hex buildings fate | Taken over intact | `Tiles.md` / `Buildings.md` | **Resolved** (engine: `combat.py`) |
| AL-12 | Archers strike again in main Strike step? | No — Pre-Strike only | `Combat.md` | **Resolved** (engine: `combat.py`) |
| AL-13 | Cities produce "+2 Population and various combinations of resources" — which resources? | +2 growth only; no Gold/Mana/Influence from the City hex itself | `Tiles.md` | **Resolved** (2026-07-03, doc + engine) |
| AL-14 | Competing Adjacency Claims resolve by Influence bidding | Full game: Influence bid; **First Playable sim:** stays neutral | `Tiles.md` | **Resolved** (2026-07-03, doc + engine) |
| AL-15 | Involuntary acquisition vs global cap 25 | Overflow allowed; Pool gates voluntary recruit/build only | `Population.md` | **Resolved** (2026-07-03, doc + engine) |
| AL-16 | Fortresses block enemy Adjacency Claims | Enemy Fortresses block adjacent neutral claims | `Tiles.md` | **Resolved** (2026-07-03, M1 fidelity sprint) |
| AL-17 | Forest defensive bonus in combat | +1 Defense for defenders on Forest terrain | `Movement.md` / `Combat.md` | **Resolved** (2026-07-03, M1 fidelity sprint) |
| AL-18 | Coronation milestone re-trigger after broken streak? | Third **total** Rite awards +2 VP once per player per game | `Victory.md` | **Resolved** (2026-07-03, doc + engine) |
| AL-19 | Portal-to-Portal ZOC and 0 AP hops | No ZOC surcharge; 0-AP hops legal at 0 AP | `Movement.md` | **Resolved** (engine: `move.py`) |
| AL-20 | Siege reinforcement +3/round cap | Persist committed uids; ≤3 reinforcements per siege round | `Combat.md` | **Resolved** (2026-07-03, M1 fidelity sprint) |
| AL-21 | Event phase frequency in First Playable | **Every round** at Round Start (before Strategy); 8-card global deck auto-resolves | `Events.md` / `Round_Structure.md` | **Resolved** (2026-07-03, M2 sim; plan draft said every 3 rounds) |
| AL-22 | High Council custom motions / negotiation | Bots propose revealed agenda only; binding deals deferred to Task 6 | `High_Council.md` / `Diplomacy.md` | **Open** (M2 simplification) |
| AL-23 | Council tie-break when yes/no votes equal | **Motion fails** (no Speaker auto-pass in sim) | `High_Council.md` | **Resolved** (2026-07-03, M2 sim) |
| AL-24 | Sim round cap with no player at VP threshold | Game **completes** at `DEFAULT_ROUND_CAP` (25) with `round_cap_finish`; tiebreak by current VP | `sim/README.md` pacing | **Resolved** (2026-07-03, sim-only) |
| AL-25 | Strategy primaries referencing Arcane Tier II+ | Stub to resource/movement effects until M3 Task 7 | `Strategy.md` | **Open** (M2 simplification) |
| AL-26 | Bank conversion timing / player choice | Auto-heuristic at end of Production & Upkeep: surplus mana→gold, else gold→mana when mana=0; one use per player per round | `Buildings.md` | **Resolved** (2026-07-03, M3 Task 1 sim) |
| AL-27 | Market free trade vs one-trade-per-round limit | Market makes trade **initiation** 0 AP; still one initiation per player per round | `Buildings.md` / `Trade_Taxes.md` | **Resolved** (2026-07-03, M3 Task 1 sim) |
| AL-28 | Lost Cartographer with no fog in sim | +1 AP this round only; no tile reveal | `Events.md` | **Resolved** (2026-07-03, M3 Task 2 sim) |
| AL-29 | Portal Instability timing | Sets flag for next portal move at 0 AP (not immediate extra decision) | `Events.md` | **Resolved** (2026-07-03, M3 Task 2 sim) |
| AL-30 | Echo of the Old Empire site tie-break | Closest hex to Seat; ties broken by axial sort from Speaker home | `Events.md` | **Resolved** (2026-07-03, M3 Task 2 sim) |
| AL-31 | Unexplored hex definition in sim | Home-cluster controlled tiles explored at setup; first unit entry elsewhere triggers exploration draw; board stays fully visible (no fog) | `Events.md` / `First_Playable_Packet.md` §4.5 | **Resolved** (2026-07-03, M3 Task 2 sim) |
| AL-32 | Wellspring Chalice production choice | Auto-pick +2 Gold at Production & Upkeep | `Artifacts.md` | **Resolved** (2026-07-03, M3 Task 3 sim) |
| AL-33 | Whisper/Arcane-linked artifact effects | Cards referencing Whispers (Whisperer's Mask, Shroud), Arcane (Archive, Ley Line discovery bonus), fog (Cartographer's Glass), or extra turns deferred until Tasks 4–6 | `Artifacts.md` | **Open** (M3 Task 3 stubs) |
| AL-34 | Scepter of Command / Windcaller's Horn | Free move riders deferred — no remote-order action enumeration yet | `Artifacts.md` | **Open** (M3 Task 3 stubs) |
