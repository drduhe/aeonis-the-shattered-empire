# Lord Sheet: Rakhis, the Sandlord

## Lord Overview

**Name:** Rakhis, the Sandlord
**Race:** Djinnborn
**Faction Theme:** The Windsworn Horde
**Gameplay Style:** Fast cavalry aggression, desert mastery, wide territorial expansion, and hit-and-run warfare.

## Lore

> "The desert does not conquer. It simply outlasts everything that stands still."

The Djinnborn are the descendants of imperial outriders who bound wind spirits into their bloodline during the empire's golden age. When the empire fell, they retreated into the deep deserts and thrived where others perished. Rakhis commands the largest mounted host in Aeonis -- not through gold or titles, but through the simple promise that those who ride with him will never be cornered. His Horde moves like weather: visible on the horizon, impossible to catch, devastating when it arrives.

---

## Starting Setup

### Starting Units (in Home City)

- **2 Infantry**
  - Attack: d6
  - Defense: d6
  - Health: 1
- **1 Cavalry**
  - Attack: d8
  - Defense: d6
  - Health: 2
  - Notes: Cavalry have Movement Range 2 and ignore ZOC penalty on first ZOC hex per Move (see `Movement.md`).

### Lord Unit (starts in Home City)

- **Rakhis (Lord / Leader)**
  - Attack: d8
  - Defense: d6
  - Health: 3
  - Movement Range: 3
  - *Design note: The fastest Lord on the board. Fragile defenses force him to use speed, not armor, to survive.*

### Starting Resources

**Gold:** 3
**Mana:** 1
**Influence:** 2

### Population

**Population Cap / Pool:** 10 / 6

### Starting AP

**Starting AP:** 5

### Unique Starting Tile (replaces your Plains)

**Oasis Wellspring** (counts as **Plains**)

- **Production:** +1 Population and +1 Gold
- **Building permissions:** You may build a **Farm** here, but you may **not** build a **Tower** here.

---

## Abilities

### 1) Sandstride (Faction Mechanic)

**Timing:** During your Move actions, and once per battle before the first **Pre-Strike** step resolves.

**Effect:** Your groups treat **Deserts** as costing **1 AP per hex**. Once per battle, before the first Pre-Strike step, you may retreat your committed group using the normal attacker or defender retreat destination rules.

**Limits:** Sandstride does not permit a defender to retreat from a City, Fortress, or a hex where it chose to Hold the Walls. Sandstride does **not** ignore enemy ZOC surcharges (removed 2026-07-12 — balance ladder Dial 3); Cavalry still use the normal first-ZOC flanking exemption. (Dial 3b retreat removal was tried and **reverted** the same day — metrics regressed.)
**Theme:** You cannot pin the wind.

### 2) Hit and Run (Passive Ability)

**Effect:** **Once per game**, when you **win a battle as the attacker**, your surviving committed units may immediately move **1 hex** to any adjacent hex you control or any adjacent neutral hex. This movement does not cost AP and does not count as a Move action.
**Theme:** The Horde strikes and vanishes before the dust settles.

### 3) Desert Tempest (Active Ability)

**Requirement:** Rakhis must be within **2 hexes** of the chosen Desert.
**Effect:** Once per round during the Action Phase, spend **2 Mana**. Choose one **Desert** hex you control. Until end of round, that hex costs **+2 additional AP** for other players to enter (total 4 AP for opponents).
**Cost:** 2 Mana
**Theme:** Wind and sand become a wall when Rakhis commands them.

---

## Faction Research (Windsworn Horde)

### Mirage Riders

**Cost:** 3 Gold, 1 Mana (Research action)
**Effect:** Your Cavalry gain **+1 Attack** (add +1 to their Attack rolls) when attacking from a **Desert** hex (the hex they committed from is a Desert).
**Theme:** Heat shimmer and speed make the charge impossible to read.

### Sandsworn Pact

**Cost:** 2 Influence, 2 Gold (Research action)
**Effect:** Once per round, when you claim a **neutral hex** by moving a unit into it, gain **+1 Gold**.
**Theme:** Every new territory is a trade route waiting to open.

---

## Legendary Building: Windsworn Warcamp

- **Prerequisite:** Win 2 battles as the attacker.
- **Build cost:** 4 AP + 5 Gold, 3 Influence
- **Population:** 3
- **Upkeep:** none
- **VP:** 2 VP once on construction
- **Effect:** Units recruited at this City gain +1 Movement for their first move each round. Once per round, one Cavalry unit group may take a free Move action (1 hex) at 0 AP.

---

## Special Units (Future Content)

These are intended for an expanded unit roster beyond the First Playable components.

### Windrunner

- **Type:** Elite Unit (Cavalry)
- **Stats:**
  - Attack: d10
  - Defense: d6
  - Health: 2
- **Special Ability:** Movement Range 3 (instead of the normal Cavalry 2). During a Move action, this unit's group treats all terrain as costing **1 AP per hex** (including Mountains).
- **Theme:** Riders who have fully bonded with their wind spirits.

### Dust Wraith

- **Type:** Advanced Unit
- **Stats:**
  - Attack: d8
  - Defense: d8
  - Health: 2
- **Upkeep (suggested):** 1 Mana per round
- **Special Ability:** When this unit enters a battle as part of the attacking force, choose one enemy **Reserve** unit. That unit must be placed on the enemy Battle Line (if there is room), potentially displacing the defender's preferred lineup.
- **Theme:** A sandstorm given form -- it reaches behind the front line.

---

## Faction Objectives

### Primary Objective (2 VP): "Endless Horizon"

Control **3 Desert** hexes at **Cleanup & Checks**.

### Secondary Objective (1 VP): "Lightning Raid"

Win a battle as **attacker** and use **Hit and Run** to move your units afterward in the same round.

---

## Faction Strategy

### Strengths

- **Map mobility:** Movement Range 3 plus Desert 1 AP keeps him fast on sand; ZOC screens now work normally against him.
- **Desert dominance:** Desert Tempest makes contested deserts punishingly expensive for opponents.
- **Aggressive tempo:** Hit and Run (once per game) lets you win a fight and immediately reposition, denying counterattack.
- **Cavalry start:** Beginning with Cavalry gives an early expansion advantage no other Lord has.

### Weaknesses

- **Mana drought:** 1 starting Mana makes Desert Tempest and research expensive early.
- **Fragile in sieges:** Speed doesn't help when assaulting fortified positions; the Horde is weakest when forced to stand still.
- **Desert dependency:** If the map has few Deserts near your position, Desert Tempest and the Desert 1 AP path lose value.
- **Thin defenses:** d6 Defense on Rakhis and most units means any sustained fight is risky.
- **Screenable:** Without blanket ZOC immunity, infantry screens can tax his approach.

---

## Faction Flavor Text

> "You built walls. I built legs. Let's see which lasts longer."

## Notes for Playtesting

- **Sandstride:** Desert 1 AP + pre-Pre-Strike retreat; full ZOC ignore removed 2026-07-12 (Dial 3). Dial 3b (drop retreat) was tried and reverted.
- **Hit and Run:** Once per game as of 2026-07-12 (ladder Dial 2); track whether single-use reposition still enables Lightning Raid without raid stickiness.
- **Oasis Wellspring:** Cavalry −1 Gold recruit discount removed 2026-07-12 (ladder Dial 1); watch whether early cavalry tempo still spikes without it.
- **Desert Tempest:** At 4 AP total for opponents, this can effectively lock a hex. Confirm 2 Mana is the right cost and that it doesn't stall the game.
- **Cavalry start:** Validate that starting with Cavalry instead of an Archer isn't too strong for Round 1 aggression.
