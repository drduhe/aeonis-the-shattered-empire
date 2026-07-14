# Lord Sheet: Morvane, the Deathless

**Status:** Expansion roster — not yet in the First Playable rotation.

## Lord Overview

**Name:** Morvane, the Deathless
**Race:** Revenant
**Faction Theme:** The Pale Legion
**Gameplay Style:** Necromancy, attrition warfare, Population sacrifice for power, and grinding battles where every corpse — his or yours — becomes his soldier.

> **Content note:** Morvane's Faction Research uses the **NEC (Necromancy)** school. NEC is otherwise expansion-module content (see `Arcane.md` §1); it is **enabled for Morvane only** as his Lord-specific path. No other Lord may research NEC discoveries.

## Lore

> "Your dead do not mourn you. They march for me."

Morvane was the empire's last Grand Marshal — the man who held the walls while the empire burned behind him. He died at his post, and the histories would have honored him for it, had he stayed dead. Something in the empire's collapse cracked the boundary between the living and the fallen, and Morvane rose from the field still wearing his rank. The soldiers who died beside him rose too. They have been marching ever since.

The Pale Legion recruits from every battlefield in Aeonis, friend and foe alike. Morvane does not hate the living; he simply considers them soldiers who have not yet enlisted. He fights without haste and without mercy, because he has learned the one truth the living refuse: every war ends the same way, and he is what's waiting there.

## Starting Setup

### Starting Units (in Home City)

- **4 Infantry**
  - Attack: d6
  - Defense: d6
  - Health: 1
  - Notes: No starting Archer. The Legion is ranks of the risen dead — numerous, uniform, expendable. (4 Population total, matching the standard 3 Infantry + 1 Archer start.)

### Lord Unit (starts in Home City)

- **Morvane (Lord / Leader)**
  - Attack: d8
  - Defense: d8
  - Health: 4
  - Movement Range: 1
  - *Design note: The slowest Lord in the game alongside Vharok, and one of the hardest to put down. He cannot chase you. He does not need to.*

### Starting Resources

**Gold:** 1
**Mana:** 3
**Influence:** 1

**Design note:** total 5 — Mana-heavy: everything the Legion does is paid for in Mana and flesh.

### Population

**Population Cap / Pool:** 10 / 6

### Starting AP

**Starting AP:** 5

### Unique Starting Tile (replaces your Plains)

**The Barrowfield** (counts as **Plains**)

- **Production:** +1 Population and +1 Mana
- **Building permissions:** You may build a **Farm** here, but you may **not** build a **Tower** here.
- **Owner-only benefit (only while you control it):** Once per round, when one of your units is **destroyed in a battle** (anywhere on the map), gain **+1 Mana**.

---

## Abilities

### 1) Raise the Fallen (Faction Mechanic)

**Effect:** **Once per battle**, immediately after a **battle round** resolves (after the Victory Check step, see `Combat.md` §4), you may spend **1 Mana**. Choose **1 non-Lord unit that was destroyed during that battle round** (yours or the enemy's). Place it in your committed **Reserves** for this battle as a **1-HP Infantry** under your control. You must have **1 Population Point available**; the raised Infantry occupies 1 Population as normal.
**Resolution order:**

- Resolve after Retreat Check and Victory Check. If the battle already ended this battle round (one side eliminated or retreated), the raised Infantry is instead placed in the hex Morvane's side committed it from (or your nearest committed hex).
- Raised units are ordinary Infantry from then on (d6/d6/1 HP); any Elite/Advanced traits of the original unit are lost.
- Lords are **captured**, not destroyed (see `Combat.md` §2.1.4), and can never be raised.

**Rules reference:** `Combat.md` (battle round, Reserves), `Population.md` (Population Pool).
**Theme:** The battle is not over when you win. It is over when Morvane says the dead may rest.

### 2) Deathless (Passive Ability)

**Effect:** Once per round, at the start of a battle round in which **Morvane is committed**, he heals **1 HP** (up to his 4 HP maximum). If Morvane is captured, the captor gains the full rewards per `Combat.md` §2.1.4; when he is released at **Cleanup & Checks**, he returns at full HP to **any City you control** (instead of only your Home City).
**Theme:** He has died before. It did not take.

### 3) Soul Tithe (Active Ability)

**Effect:** Once per round during the **Action Phase**, on your turn (costs **0 AP**, but consumes your turn like an ACTION), **sacrifice 1 Population Point** from your available Population Pool to gain **2 Mana**. Sacrificed Population is **not refunded**; it must regrow through normal Population growth (see `Population.md`).
**Cost:** 1 Population Point
**Theme:** The Legion's coffers are its people. Morvane spends both the same way.

---

## Faction Research (The Pale Legion)

*Both discoveries below are **NEC (Necromancy)** school — Lord-specific to Morvane (see the Content note above and `Arcane.md` §8). Researching the Tier I discovery grants NEC 1 for prerequisite purposes as normal.*

### Grave Pact

**School:** NEC
**Tier:** I (1 AP to research)
**Prerequisite:** none
**Cost:** 2 Mana (Research action)
**Type:** Ritual
**Effect:** Once per battle round, after one of your Battle Line units rolls its Attack Die, you may **sacrifice 1 Population Point** (not refunded; regrows via Population growth). If you do, add **+1** to that Attack roll.
**Theme:** Strength is borrowed from the unborn ranks of the Legion.

### Bone Ramparts

**School:** NEC
**Tier:** II (2 AP to research)
**Prerequisite:** NEC 1
**Cost:** 3 Mana, 1 Gold (Research action)
**Type:** Ritual
**Effect:** Once per round, when another player declares an **Attack** against a hex you control, before Battle Lines are formed, you may **sacrifice 1 Population Point**. If you do, place **1 Infantry** for free in the defended hex; it is committed to the battle. (The Infantry also occupies 1 Population as normal — 2 Population total.)
**Theme:** The ground itself gives up its dead to hold the line.

---

## Legendary Building: The Ossuary Throne

- **Prerequisite:** Raise units with **Raise the Fallen** in 3 different battles (cumulative across the game).
- **Build cost:** 4 AP + 5 Gold, 4 Mana
- **Population:** 3
- **Upkeep:** none
- **VP:** 2 VP once on construction
- **Renown:** +2 immediately when constructed (standard Legendary rule, see `Buildings.md`)
- **Effect:** **PRODUCTION:** You may sacrifice up to **2 Population Points**; gain **2 Mana** per point sacrificed (in addition to Soul Tithe). Once per round, when you take a **Recruit** action at this City, you may recruit **1 additional Infantry** beyond the normal 2-unit limit by paying **1 Mana** instead of its Gold cost (Population as normal).

---

## Special Units (Future Content)

These are intended for an expanded unit roster beyond the First Playable components.

### Bonewrought Colossus

- **Type:** Elite Unit
- **Stats:**
  - Attack: d10
  - Defense: d8
  - Health: 3
- **Special Ability:** When this unit is destroyed in a battle, you may immediately place **2 Infantry** (1 HP each) in your committed Reserves for that battle, if you have 2 Population Points available.
- **Theme:** A siege engine built of the Legion's honored dead — break it, and it becomes soldiers again.

### Wraith Herald

- **Type:** Advanced Unit
- **Stats:**
  - Attack: d6
  - Defense: d8
  - Health: 2
- **Upkeep (suggested):** 1 Mana per round
- **Special Ability:** At the start of each battle round (if committed to the battle), choose one enemy **Battle Line** unit. That unit's Attack rolls get **-1** this battle round (minimum 1).
- **Theme:** Its wail reminds the living of exactly where they are going.

---

## Faction Objectives

### Primary Objective (2 VP): "The Dead Outnumber the Living"

Use **Raise the Fallen** in **3 different battles** (cumulative across the game).

### Secondary Objective (1 VP): "Enlisted in Death"

Win a battle in which at least one Infantry you raised with **Raise the Fallen** was on your **Battle Line**.

---

## Faction Strategy

### Strengths

- **Attrition immunity:** Every battle round can end with Morvane one unit richer than the dice say — long fights and sieges favor him more than any other Lord.
- **Two economies:** Soul Tithe and the NEC discoveries let Morvane convert Population into Mana and combat power, so he is never resource-locked while he holds Plains and Cities.
- **Nearly unkillable Lord:** d8/d8/4 HP with an in-battle heal makes capturing Morvane a campaign in itself, and Deathless means even capturing him barely dents his position.
- **Defensive teeth:** Bone Ramparts punishes attackers before dice are even rolled.

### Weaknesses

- **Move 1:** Morvane cannot project force. Enemies choose when and where to fight him, and objectives across the map are simply out of his reach.
- **Population death spiral:** Soul Tithe, Grave Pact, and Bone Ramparts all spend the same Population that recruits his armies. Overspending leaves the Legion unable to field the units it raises.
- **No reach, no burst:** No starting Archer (no Pre-Strike), no Cavalry, no mobility tools — the Legion wins slow fights and loses races.
- **Influence-blind:** 1 starting Influence and no political hooks; the High Council will happily legislate against a player who cannot lobby back.

---

## Faction Flavor Text

> "I accept your surrender. I also accept your refusal."

## Notes for Playtesting

- **Raise the Fallen (biggest risk):** A 1-Mana swing of up to 2 units (their loss becomes your gain) once per battle. Deliberately tuned conservative — 1 per battle, Infantry only, Population still paid. Watch multi-round sieges especially: over 3+ Attack actions this compounds. If it overperforms, first restrict it to **your own** destroyed units, then to once per **round**.
- **Deathless heal + d8/d8/4 HP:** Confirm Morvane can actually be captured by a committed effort. If he proves effectively immortal on defense, remove the in-battle heal before touching his dice.
- **Population sacrifice stacking:** Soul Tithe + Grave Pact + Bone Ramparts + Ossuary Throne can burn 4-5 Population in a round. Verify the death spiral is a real deterrent (self-balancing) rather than a trap that makes the faction feel unplayable — and that it is not trivially outgrown by holding 2-3 Plains.
- **4-Infantry start:** No Pre-Strike makes his Round 1 defense slightly weaker than standard despite equal Population. Confirm this is a fair trade for his battle economy.
