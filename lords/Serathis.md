# Lord Sheet: Serathis, the Tidecaller

**Status:** Expansion roster — not yet in the First Playable rotation.

## Lord Overview

**Name:** Serathis, the Tidecaller
**Race:** Tideborn
**Faction Theme:** The Drowned Court
**Gameplay Style:** Lake control, chokepoint fortresses, amphibious strikes, and Bridge denial — turning the map's impassable water into her private highway and citadel.

## Lore

> "You call them barriers. We call them thrones."

When the empire drowned its rebellious coastal provinces behind sorcerous floodwalls, it believed the matter settled. It was wrong. The survivors did not die in the deep places — they changed. The Tideborn emerged generations later: grey-eyed, salt-blooded, breathing water as easily as air, and carrying a long memory of what the dry world owed them.

Serathis rules the Drowned Court from beneath the surface of lakes no army can cross. Her halls are sunken, her sentries invisible, her borders drawn in water. Where other Lords see a Lake as a wall on the map, Serathis sees a road, a fortress, and a larder all at once — and every Bridge her rivals build is simply a door she has not yet closed.

---

## Starting Setup

### Starting Units (in Home City)

- **2 Infantry**
  - Attack: d6
  - Defense: d6
  - Health: 1
- **1 Archer**
  - Attack: d6
  - Defense: d4
  - Health: 1
  - Notes: Archers on the Battle Line have **Pre-Strike** (see `Combat.md`).

### Lord Unit (starts in Home City)

- **Serathis (Lord / Leader)**
  - Attack: d8
  - Defense: d8
  - Health: 3
  - Movement Range: 2
  - *Design note: A balanced duelist. Her real defense is positional — fighting her means fighting the water she stands on.*

### Starting Resources

**Gold:** 2
**Mana:** 2
**Influence:** 1

**Design note:** total 5, one below the core roster's 6 — a deliberate offset for the strength of Tideborn Passage. Validate in playtest.

### Population

**Population Cap / Pool:** 10 / 10

### Starting AP

**Starting AP:** 5

### Unique Starting Tile (replaces your Forest)

**Sunken Shrine** (counts as **Lake**)

- **Production:** +1 Mana and +1 Gold. *(Exception to the normal Lake rule of producing nothing; see `Tiles.md`. Production goes to the current controller — a rival must Bridge and hold this tile to profit from it.)*
- **Building permissions:** A **Bridge** may be built here under the normal Bridge rules (see `Buildings.md`). No other buildings may be built here.
- **Owner-only benefit (only while you control it):** You have a **GEO specialty** when checking discovery prerequisites (see `Arcane.md` §3.3).

---

## Abilities

### 1) Tideborn Passage (Faction Mechanic)

**Effect:** Your units treat **Lakes** as passable difficult terrain: entering an unbridged Lake hex costs **2 AP** during a Move action. Your units may **occupy and control** Lake hexes. Other players still follow the standard Lake rules (impassable and unoccupiable without a **Bridge**; see `Tiles.md`). If a Lake hex has a Bridge, all players (including you) use the Bridge rules instead (1 AP to enter).
**Resolution notes:**

- Other players **may** still declare an Attack against a Lake hex you occupy — combat is fought from adjacent hexes (see `Combat.md` §3). If the attacker wins, they gain control of the hex per `Combat.md` §5.1, but they may **not** occupy it unless they can legally enter it (via a Bridge). An unoccupied Lake hex is vulnerable to being retaken.
- Your units in a Lake hex generate ZOC into adjacent hexes as normal (see `Tiles.md`).

**Rules reference:** `Tiles.md` (Lakes, Bridge), `Movement.md` (terrain costs), `Combat.md` (Aftermath).
**Theme:** The Drowned Court does not cross the water. It lives there.

### 2) Bulwark of the Deep (Passive Ability)

**Effect:** Your units defending a **Lake** hex gain **+1 Defense** (add +1 to their Defense rolls). In addition, an attacker may not **Press the Attack** (see `Combat.md` §4.0) against a Lake hex you defend.
**Theme:** Assaulting the deep is done at the water's pace, not the attacker's.

### 3) Riptide (Active Ability)

**Requirement:** Serathis must be within **2 hexes** of the chosen Lake.
**Effect:** Once per round during the Action Phase, spend **2 Mana**. Choose one **Lake** hex you control. Until end of round, each hex adjacent to that Lake costs **+1 additional AP** for other players to enter.
**Cost:** 2 Mana
**Theme:** The shoreline itself pulls at the boots of those who march too close.

---

## Faction Research (The Drowned Court)

### Brackish Bounty

**School:** GEO
**Tier:** I (1 AP to research)
**Prerequisite:** none
**Cost:** 2 Mana, 1 Gold (Research action)
**Type:** Passive
**Effect:** During **Production & Upkeep**, if you control at least **1 Lake** hex, gain **+1 Gold**. If you control **2 or more Lake** hexes, also gain **+1 Mana**.
**Theme:** The dry world starves beside water it cannot harvest.

### Call the Deep

**School:** GEO
**Tier:** II (2 AP to research)
**Prerequisite:** GEO 1 (the Sunken Shrine's GEO specialty can satisfy this; see `Arcane.md` §3.3)
**Cost:** 4 Mana, 1 Influence (Research action)
**Type:** Ritual
**Effect:** **Once per game**, on your turn during the Action Phase (0 AP, but consumes your turn like an ACTION), spend **3 Mana**. Choose a **neutral Plains or Desert** hex adjacent to a hex you control that contains **no units and no buildings**. That hex becomes a **Lake** (place a Lake tile or marker over it). It follows all Lake rules from then on (see `Tiles.md`), including your Tideborn Passage.
**Theme:** Where the Tidecaller sings, the old waters remember their beds.
*Design note: Lakes are rare (2-3 per map). This is Serathis's guaranteed access to her own terrain when the map placement is unkind — limited to once per game because map-editing is the strongest thing a Lord can do.*

---

## Legendary Building: Throne of the Drowned Court

- **Prerequisite:** Control 2 Lake hexes (the Sunken Shrine counts).
- **Build cost:** 4 AP + 5 Gold, 4 Mana
- **Population:** 3
- **Upkeep:** none
- **VP:** 2 VP (checked at Cleanup & Checks)
- **Renown:** +2 immediately when constructed (standard Legendary rule, see `Buildings.md`)
- **Effect:** **PRODUCTION:** Gain +1 Gold and +1 Mana if you control at least 1 Lake hex. Once per round, you may move one of your unit groups between this City and any Lake hex you control (either direction) at **0 AP** (does not count as a Move action).

---

## Special Units (Future Content)

These are intended for an expanded unit roster beyond the First Playable components.

### Depthguard

- **Type:** Elite Unit
- **Stats:**
  - Attack: d6
  - Defense: d10
  - Health: 2
- **Special Ability:** While defending a **Lake** hex, or a hex adjacent to a Lake you control, this unit cannot be targeted by **Archer Pre-Strike** (enemy Archers must choose a different target).
- **Theme:** Half-seen shapes below the surface — arrows find only water.

### Leviathan of the Old Deep

- **Type:** Advanced Unit
- **Stats:**
  - Attack: d12
  - Defense: d6
  - Health: 3
- **Upkeep (suggested):** 1 Mana per round
- **Special Ability:** This unit may only enter or occupy **Lake** hexes and hexes **adjacent** to a Lake. It may commit to battles targeting hexes adjacent to the Lake it occupies (see `Combat.md` §3.2).
- **Theme:** Something ancient answers the Tidecaller's summons — but it will not leave the water far behind.

---

## Faction Objectives

### Primary Objective (2 VP): "Mistress of the Deep"

Control **3 Lake hexes** at **Cleanup & Checks** (the Sunken Shrine counts).

### Secondary Objective (1 VP): "Death by Water"

Win a battle in which at least one of your committed units was committed **from a Lake hex**.

---

## Faction Strategy

### Strengths

- **Untouchable garrisons:** Units parked in unbridged Lakes can only be dislodged by attacks that cannot follow up with occupation — Serathis holds chokepoints more cheaply than any other Lord.
- **Chokepoint economics:** Lakes sit at map choke points by design (see `First_Playable_Packet.md` §3.1). Riptide plus Bulwark of the Deep makes those corridors miserable for everyone else.
- **Terrain on demand:** Call the Deep guarantees her theme functions even on a lake-poor map, and can close a corridor permanently.
- **Solid Lord:** d8/d8/3 is a fair fight against nearly anyone — she doesn't need to hide.

### Weaknesses

- **Slow in the water:** 2 AP per Lake hex means her "highway" is expensive; she trades speed for safety.
- **Bridge counterplay:** Any rival can build a Bridge (4 Gold, see `Buildings.md`) onto a Lake she holds, and suddenly her fortress has a front door.
- **Sparse theme terrain:** With only 2-3 Lakes on the map, losing contests for them hurts her more than losing a Desert hurts Rakhis.
- **Thin Influence:** 1 starting Influence makes her nearly voiceless in the early High Council rounds.

---

## Faction Flavor Text

> "Build your bridge. I'll wait under it."

## Notes for Playtesting

- **Lake garrisons (biggest risk):** A unit in an unbridged Lake can be attacked but never followed up with occupation. Watch whether attacking her Lake positions ever feels worthwhile, or whether opponents simply concede every Lake — if so, consider letting a battle winner place a free temporary "pontoon" marker, or raising her enter cost to 3 AP.
- **Riptide:** +1 AP on every hex ringing a Lake is up to 6 hexes affected — much wider than Rakhis's Desert Tempest. Confirm 2 Mana is expensive enough and that it can't lock the only corridor on small maps.
- **Call the Deep:** Permanent map-editing. Verify "once per game, adjacent, empty, neutral Plains/Desert only" is restrictive enough that it can't wall off a player's home cluster.
- **Sunken Shrine production:** +1 Mana +1 Gold on a tile that opponents must spend 4 Gold (Bridge) just to contest may be too safe an economic engine. Track how often it is ever seriously threatened.
