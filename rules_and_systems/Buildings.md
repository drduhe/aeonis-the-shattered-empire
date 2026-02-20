# Aeonis: Buildings

## Overview

**Buildings** are a key part of resource production, defense, and advancing a player’s strategy. They interact dynamically with the terrain and Lords, encouraging players to balance growth, offense, and economic development. Each building serves a specific role and comes with trade-offs, ensuring meaningful decisions.

This chapter also acts as the **canonical reference** for buildings mentioned in other chapters (e.g., `Actions.md`, `Tiles.md`, `Trade_Taxes.md`, `Population.md`).

---

## Building “cost types” (how buildings interact with Population and upkeep)

- **Build cost**: resources paid once when constructing the building (and the Build action AP cost, see `Actions.md`).
- **Population capacity**: if a building is “Population-maintained,” it occupies Population while it exists (see `Population.md`).
- **Resource upkeep**: only **advanced/legendary buildings** should have Gold/Mana/Influence upkeep (see `Trade_Taxes.md`). Basic production buildings generally do **not**.

## Building Categories

Buildings fall into three main categories:

- **Production Buildings**: Enhance resource generation on tiles and form the backbone of a Lord’s economy. Can only be built on terrain that supports their resource type (e.g., Farms on Plains).
- **Military/Defensive Buildings**: Provide defense, control, and strategic advantages. Can be built on most terrain tiles, offering flexibility in placement.
- **Advanced/Special Buildings**: Unlock unique abilities, units, or late-game bonuses. Require specific conditions or resources to construct.

### Production Buildings

These enhance the resource output of a tile. Only one production building can be constructed per tile.

- **Farm** (Plains):
  - Build cost: 2 Gold
  - Population capacity: occupies 1 Population (as long as it exists)
  - Effect: increases Plains production from **+1 Population** to **+2 Population** (aligns with `Tiles.md`) and increases your **Population Cap by +2** (aligns with `Population.md`).
- **Mine** (Mountains):
  - Build cost: 3 Gold
  - Population capacity: occupies 1 Population
  - Effect: increases Mountains production from **+1 Gold** to **+3 Gold**.
- **Grove** (Forests):
  - Build cost: 2 Mana
  - Population capacity: occupies 1 Population
  - Effect: increases Forest production from **+1 Mana** to **+3 Mana**.
- **Embassy** (Deserts):
  - Build cost: 3 Influence
  - Population capacity: occupies 1 Population
  - Effect: increases Desert production from **+1 Influence** to **+3 Influence**.

### Military/Defensive Buildings

These buildings strengthen a player’s position and allow for strategic control of key tiles.

- **Tower** (Any Tile, including Portals):
  - Build cost: 4 Gold
  - Population capacity: occupies 1 Population
  - Effect:
    - Units defending the tower’s hex gain **+1 Defense**.
    - The tower extends control/influence **two hexes outward** (aligns with `Tiles.md`).
    - If built on a **Portal**, it also establishes control of that Portal (aligns with `Tiles.md`).
- **Fortress** (Any Tile):
  - Build cost: 5 Gold, 2 Mana
  - Population capacity: occupies 2 Population
  - Effect:
    - Units defending the fortress hex gain **+2 Defense**.
    - A Fortress hex is always treated as a **Siege** when attacked (the defender is assumed to “Hold the Walls”). See `Combat.md`.
- **Bridge** (Lake hex only):
  - Build cost: 4 Gold
  - Population capacity: none
  - Resource upkeep: none (default)
  - Build condition: you must control at least one **adjacent non-Lake hex**.
  - Effect: the Lake hex becomes **passable** and can be occupied/controlled, but produces **no resources** (see `Tiles.md`).

### Advanced/Special Buildings

These buildings unlock powerful abilities and game-altering effects.

- **Guild Hall** (Cities):
  - Build cost: 4 Gold, 2 Influence
  - Population capacity: occupies 1 Population
  - Resource upkeep: none (default)
  - Effect: **+1 AP per round** (aligns with `Actions.md`).
- **Forge / Arcane Forge** (Cities):
  - Build cost: 5 Gold
  - Population capacity: occupies 1 Population
  - Resource upkeep: 1 Mana per round (see `Trade_Taxes.md`)
  - Effect: Once per round, when you Recruit at this City, you may recruit **1 additional unit** beyond the normal 2-unit limit. Units recruited at this City cost **−1 Gold** (minimum 1).
- **Academy** (Cities):
  - Build cost: 4 Gold, 3 Mana
  - Population capacity: occupies 2 Population
  - Resource upkeep: 1 Mana per round (see `Trade_Taxes.md`)
  - Effect: You gain a **School Specialty** of your choice (counts as +1 sigil when checking Arcane prerequisites; see `Arcane.md` section 3.3). Once per round, when you take a Research action, reduce its resource cost by **1 Mana** (minimum 0).
- **Bank** (Cities):
  - Build cost: 5 Gold
  - Population capacity: occupies 1 Population
  - Resource upkeep: none
  - Effect: Once per round during **Production & Upkeep**, you may convert resources at a 2:3 rate. Choose one: **2 Mana → 3 Gold**, **2 Gold → 3 Mana**, or **2 Gold → 3 Influence**.
- **Castle** (Cities):
  - Build cost: 6 Gold
  - Population capacity: occupies 2 Population
  - Resource upkeep: 2 Gold per round (aligns with `Trade_Taxes.md` example)
  - Effect: increases your **Population Cap by +3** and grants **+2 Defense** to units defending this City.
- **Market** (Cities):
  - Build cost: 2 Gold, 2 Influence
  - Population capacity: occupies 1 Population
  - Resource upkeep: none (default)
  - Effect: once per round, you may **initiate one Trade at 0 AP cost** (does not increase the “one trade initiation per round” limit unless you choose to make it do so; see `Trade_Taxes.md`).

## Legendary Buildings (Faction Capstones)

Each Lord has exactly **1 Legendary Building** unique to them. No other Lord may build it.

### Rules

- Legendary Buildings may be built in **any City you control**.
- Building a Legendary costs **4 AP** (not the standard 3 AP) plus the building's listed resource cost.
- Each Legendary has a **faction prerequisite** that must be met before construction.
- Legendary Buildings occupy **3 Population**.
- A Legendary Building is worth **2 VP** (checked at Cleanup & Checks). If the City is captured, the captor gains control of the Legendary and its VP.
- Constructing a Legendary Building grants **+2 Renown** immediately (see `Renown.md`).
- A Lord may only build **one copy** of their Legendary Building.
- Cities have a 2-building limit (3 with research). The Legendary counts as one of those slots.

### Grand Exchange (Cassian)

- **Prerequisite:** Control 2 Markets and have 8+ Gold in reserve.
- **Cost:** 6 Gold, 3 Influence
- **Upkeep:** none
- **Effect:** **PRODUCTION:** Gain +1 Gold for each Trade action completed this round (by any player, including trades with you). Once per round, you may initiate a Trade at **0 AP** (in addition to any Market benefit).

### Arcane Sanctum (Seraphel)

- **Prerequisite:** Complete 3 Arcane Discoveries (any school).
- **Cost:** 4 Gold, 6 Mana
- **Upkeep:** none
- **Effect:** **PRODUCTION:** Gain +2 Mana. Once per round, you may Research a Tier I discovery for **free** (0 AP, 0 resources). Your Lord gains +1 Attack die size while in this hex.

### Iron Citadel (Vharok)

- **Prerequisite:** Control at least 1 Fortress.
- **Cost:** 8 Gold, 2 Mana
- **Upkeep:** 2 Gold per round
- **Effect:** This City is treated as a **Fortress** (Siege rules apply to attackers; see `Combat.md`). Units defending this hex gain **+3 Defense**.

### Heartwood Sanctum (Elyndra)

- **Prerequisite:** Reach Population Cap of 15+.
- **Cost:** 3 Gold, 4 Mana, 2 Influence
- **Upkeep:** none
- **Effect:** **PRODUCTION:** +3 Population growth at this hex. Adjacent hexes you control produce +1 of their primary resource. Units in this hex regenerate 1 HP at Round Start.

### Windsworn Warcamp (Rakhis)

- **Prerequisite:** Win 2 battles as the attacker.
- **Cost:** 5 Gold, 3 Influence
- **Upkeep:** none
- **Effect:** Units recruited at this City gain **+1 Movement** for their first move each round. Once per round, one Cavalry unit group may take a free Move action (1 hex) at **0 AP**.

### Hall of Whispers (Nyxara)

- **Prerequisite:** Play 4 Whisper Cards (cumulative across the game).
- **Cost:** 4 Gold, 4 Mana, 2 Influence
- **Upkeep:** none
- **Effect:** Draw **+1 Whisper Card** at Round Start. **WHEN** another player plays a Whisper Card: You may look at their hand. Once per round, you may play a Whisper Card from your hand as if it had **any** timing window.

### Cathedral of Radiance (Auriel)

- **Prerequisite:** Reach 5 Renown.
- **Cost:** 4 Gold, 3 Mana, 3 Influence
- **Upkeep:** none
- **Effect:** **COUNCIL:** Your Influence counts double when voting on proposals you initiated. **PRODUCTION:** Gain +1 Renown if you are currently the Speaker. Units defending this hex gain +2 Defense.

### Dimensional Nexus (Thal'rik)

- **Prerequisite:** Control 2 Portal hexes.
- **Cost:** 5 Gold, 5 Mana
- **Upkeep:** none
- **Effect:** This City counts as a **Portal** for all Portal travel rules. Once per round, you may teleport a unit group from this hex to any Portal on the map for **0 AP** (you must still control or have a unit at the destination Portal).

---

## Building Relics (Artifact Attachments)

Certain artifacts in the Artifact Deck are **Building Relics** — ancient power sources that attach to a specific building type. See `Artifacts.md` for the full system.

- When you gain a Building Relic, you must assign it to an eligible building you control.
- A building may hold at most **1 Building Relic**.
- The relic's effect activates immediately upon attachment.
- If the attached building's hex changes control, the new controller claims the relic.
- If the attached building is destroyed and no player occupies the hex, the relic returns to the bottom of the Artifact Deck.

| Relic | Eligible Buildings |
|---|---|
| Ley Line Conduit | Academy or Mana-producing building |
| Titan's Cornerstone | Fortress or Tower |
| Eternal Forge | Forge |
| Verdant Hearthstone | Farm or City |
| Astral Beacon | Any building on a Portal hex |
| Archive of the Fallen | Academy |

---

## Special Rules for Buildings

- **Construction Limits:** Basic terrain tiles (Plains, Forests, Mountains, Deserts): 1 building per tile. Cities: Up to 2 buildings (expandable to 3 via upgrades or research).
- **Maintenance Costs:** As a default, **only advanced/legendary buildings** require Gold/Mana/Influence upkeep (see `Trade_Taxes.md`). Basic production and defensive buildings are typically maintained via **Population capacity**.
- **Destruction of Buildings:** If a tile is captured, its building may be destroyed, downgraded, or taken over, depending on the circumstances.

## Synergy with Lords and Unique Tiles

- **Legendary Buildings as Lord-Specific Buildings:** Each Lord's unique building is their Legendary Building (see above). No additional Lord-specific buildings exist.
- **Unique Starting Tiles:** Each Lord's unique starting tile may interact with specific buildings (e.g., Vharok's Ironworks Ridge reduces Fortress cost). See individual Lord sheets for details.
