# Buildings Overhaul Design

**Date:** 2026-02-19
**Status:** Approved — ready for implementation
**Scope:** Finalize TBD buildings, add 8 Legendary capstones, cut upgrade system, full roster in First Playable

---

## 1. Finalized TBD Buildings

### Academy (absorbs Library)

- **Build cost:** 4 Gold, 3 Mana
- **Population:** 2
- **Upkeep:** 1 Mana per round
- **Where:** Cities
- **Effect:** You gain a **School Specialty** of your choice (counts as +1 sigil when checking Arcane prerequisites; see `Arcane.md` section 3.3). Once per round, when you take a Research action, reduce its resource cost by **1 Mana** (minimum 0).

The Academy replaces all references to "Library" in the project. The Archive of the Fallen artifact's eligible buildings change from "Academy or Library" to "Academy."

### Forge

- **Build cost:** 5 Gold
- **Population:** 1
- **Upkeep:** 1 Mana per round
- **Where:** Cities
- **Effect:** Once per round, when you Recruit at this City, you may recruit **1 additional unit** beyond the normal 2-unit limit. Units recruited at this City cost **−1 Gold** (minimum 1).

### Bank

- **Build cost:** 5 Gold
- **Population:** 1
- **Upkeep:** none
- **Where:** Cities
- **Effect:** Once per round during Production & Upkeep, you may convert resources at a 2:3 rate. Choose one: **2 Mana → 3 Gold**, **2 Gold → 3 Mana**, or **2 Gold → 3 Influence**.

---

## 2. Upgrade System — Removed

The "New Mechanics: Building Upgrades" section is cut from `Buildings.md`. Rationale:

- **Arcane Discoveries** already modify buildings (Enchantment school effects, Geomancy infrastructure).
- **Building Relics** from the Artifact system already enhance specific buildings.
- A third upgrade layer adds complexity without sufficient payoff.

All placeholder upgrade examples (Improved Farm, Reinforced Tower, Advanced Forge) are removed.

---

## 3. Legendary Buildings (Faction Capstones)

### System Rules

- Each Lord has exactly **1 Legendary Building** unique to them. No other Lord may build it.
- Legendary Buildings may be built in **any City you control**.
- Building a Legendary costs **4 AP** (higher than the standard 3 AP Build action) plus the building's listed resource cost.
- Each Legendary has a **faction prerequisite** — a condition matching that Lord's playstyle that must be met before construction.
- Legendary Buildings occupy **3 Population**.
- A Legendary Building is worth **2 VP** (checked at Cleanup & Checks). If the City is captured, the captor gains control of the Legendary and its VP.
- Constructing a Legendary Building grants **+2 Renown** immediately (per `Renown.md`).
- A Lord may only build **one copy** of their Legendary Building.
- Cities have a 2-building limit (3 with research). The Legendary counts as one of those slots.

### The 8 Legendary Buildings

#### 1. Grand Exchange (Cassian)

- **Prerequisite:** Control 2 Markets and have 8+ Gold in reserve.
- **Cost:** 6 Gold, 3 Influence
- **Upkeep:** none
- **Effect:** **PRODUCTION:** Gain +1 Gold for each Trade action completed this round (by any player, including trades with you). Once per round, you may initiate a Trade at **0 AP** (in addition to any Market benefit).

#### 2. Arcane Sanctum (Seraphel)

- **Prerequisite:** Complete 3 Arcane Discoveries (any school).
- **Cost:** 4 Gold, 6 Mana
- **Upkeep:** none
- **Effect:** **PRODUCTION:** Gain +2 Mana. Once per round, you may Research a Tier I discovery for **free** (0 AP, 0 resources). Your Lord gains +1 Attack die size while in this hex.

#### 3. Iron Citadel (Vharok)

- **Prerequisite:** Control at least 1 Fortress.
- **Cost:** 8 Gold, 2 Mana
- **Upkeep:** 2 Gold per round
- **Effect:** This City is treated as a **Fortress** (Siege rules apply to attackers; see `Combat.md`). Units defending this hex gain **+3 Defense**.

#### 4. Heartwood Sanctum (Elyndra)

- **Prerequisite:** Reach Population Cap of 15+.
- **Cost:** 3 Gold, 4 Mana, 2 Influence
- **Upkeep:** none
- **Effect:** **PRODUCTION:** +3 Population growth at this hex. Adjacent hexes you control produce +1 of their primary resource. Units in this hex regenerate 1 HP at Round Start.

#### 5. Windsworn Warcamp (Rakhis)

- **Prerequisite:** Win 2 battles as the attacker.
- **Cost:** 5 Gold, 3 Influence
- **Upkeep:** none
- **Effect:** Units recruited at this City gain **+1 Movement** for their first move each round. Once per round, one Cavalry unit group may take a free Move action (1 hex) at **0 AP**.

#### 6. Hall of Whispers (Nyxara)

- **Prerequisite:** Play 4 Whisper Cards (cumulative across the game).
- **Cost:** 4 Gold, 4 Mana, 2 Influence
- **Upkeep:** none
- **Effect:** Draw **+1 Whisper Card** at Round Start. **WHEN** another player plays a Whisper Card: You may look at their hand. Once per round, you may play a Whisper Card from your hand as if it had **any** timing window.

#### 7. Cathedral of Radiance (Auriel)

- **Prerequisite:** Reach 5 Renown.
- **Cost:** 4 Gold, 3 Mana, 3 Influence
- **Upkeep:** none
- **Effect:** **COUNCIL:** Your Influence counts double when voting on proposals you initiated. **PRODUCTION:** Gain +1 Renown if you are currently the Speaker. Units defending this hex gain +2 Defense.

#### 8. Dimensional Nexus (Thal'rik)

- **Prerequisite:** Control 2 Portal hexes.
- **Cost:** 5 Gold, 5 Mana
- **Upkeep:** none
- **Effect:** This City counts as a **Portal** for all Portal travel rules. Once per round, you may teleport a unit group from this hex to any Portal on the map for **0 AP** (you must still control or have a unit at the destination Portal).

### Design Notes

- Prerequisites match playstyle: Cassian builds Markets, Seraphel researches, Vharok fortifies, Elyndra grows, Rakhis fights, Nyxara plays Whispers, Auriel earns Renown, Thal'rik controls Portals.
- Effects amplify existing strengths rather than introducing new mechanics.
- VP transfer on capture makes Legendary Cities high-value late-game targets.
- Earliest realistic build: round 4-5 for most Lords.

---

## 4. Integration — Files Requiring Updates

| File | Change |
|---|---|
| **`Buildings.md`** | Major rewrite: finalize Forge/Academy/Bank, add 8 Legendary capstones, cut upgrade system, update Lord-building section |
| **`Artifacts.md`** | Fix Archive of the Fallen: "Academy or Library" → "Academy" |
| **`Victory.md`** | Update Legendary Buildings: 1 per Lord, 2 VP each, transfers on capture |
| **`Renown.md`** | Verify +2 Renown on Legendary construction cross-reference |
| **`Population.md`** | Add note that Legendary Buildings occupy 3 Population |
| **`First_Playable_Packet.md`** | Remove building exclusions (Academy, Forge, Bank, Castle, Legendary all now allowed). Add Legendary Building rules summary and playtest goal. |
| **`INDEX.md`** | Remove Legendary Buildings from remaining work, add to resolved decisions |
| **`content-manifest.json`** | Update Buildings.md description |
| **`lords/Cassian.md`** | Add Grand Exchange Legendary Building entry |
| **`lords/Seraphel.md`** | Add Arcane Sanctum Legendary Building entry |
| **`lords/Vharok.md`** | Add Iron Citadel Legendary Building entry |
| **`lords/Elyndra.md`** | Add Heartwood Sanctum Legendary Building entry |
| **`lords/Rakhis.md`** | Add Windsworn Warcamp Legendary Building entry |
| **`lords/Nyxara.md`** | Add Hall of Whispers Legendary Building entry |
| **`lords/Auriel.md`** | Add Cathedral of Radiance Legendary Building entry |
| **`lords/Thalrik.md`** | Add Dimensional Nexus Legendary Building entry |
