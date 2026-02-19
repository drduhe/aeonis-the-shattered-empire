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
  - Resource upkeep (suggested): 1 Mana per round (aligns with `Trade_Taxes.md` example)
  - Effect: unlocks advanced crafting / unit upgrade research hooks (exact upgrade lists TBD).
- **Academy** (Cities):
  - Build cost: 4 Gold, 3 Mana
  - Population capacity: occupies 2 Population (aligns with `Population.md`)
  - Resource upkeep (optional): 1 Gold or 1 Mana per round (tune in playtests)
  - Effect: enables advanced magical research (extra Arcane options / discounts / unique actions—TBD).
- **Bank** (Cities):
  - Build cost: 5 Gold
  - Population capacity: occupies 1 Population
  - Resource upkeep: none (default)
  - Effect: convert resources at a favorable rate once per round (exact rate TBD; placeholder: 2 Mana → 3 Gold or 2 Gold → 3 Mana).
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
- **Legendary Building** (Cities or Special Locations):
  - Build cost: varies (expensive)
  - Population capacity: varies (typically 2–4 Population)
  - Resource upkeep: may apply (typically Gold or Mana)
  - Effect: unique and game-changing; define each Legendary Building as a named card/entry.

## New Mechanics: Building Upgrades

To add flexibility and late-game scaling, players can upgrade certain buildings to enhance their effects.

- **Upgrade Examples:** Improved Farm: Increases Population production to +4. Reinforced Tower: Adds +1 defense bonus to adjacent units. Advanced Forge: Unlocks advanced unit upgrades. For artifact interaction, see `Artifacts.md` (Building Relics).
- **Cost of Upgrades:** Upgrades cost additional Gold, Mana, or Influence and require a specific building (e.g., Forge or Academy).
- **Upgrade Slots:** Cities and some special tiles may gain an additional upgrade slot through research or construction.

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
| Archive of the Fallen | Academy or Library |

---

## Special Rules for Buildings

- **Construction Limits:** Basic terrain tiles (Plains, Forests, Mountains, Deserts): 1 building per tile. Cities: Up to 2 buildings (expandable to 3 via upgrades or research).
- **Maintenance Costs:** As a default, **only advanced/legendary buildings** require Gold/Mana/Influence upkeep (see `Trade_Taxes.md`). Basic production and defensive buildings are typically maintained via **Population capacity**.
- **Destruction of Buildings:** If a tile is captured, its building may be destroyed, downgraded, or taken over, depending on the circumstances.

## Synergy with Lords and Unique Tiles

- **Lord-Specific Buildings:** Each Lord may have access to a unique building that reinforces their identity (one per Lord is a good default).

Recommended Lord-building template:

- **Name / Type**: (Production / Defensive / Advanced)
- **Where it can be built**: (terrain/city/special)
- **Build cost**: resources + Build action AP
- **Population capacity**: how much capacity it occupies
- **Upkeep** (if any): Gold/Mana/Influence per round
- **Effect**: concise rules text
- **Balance hook**: what trade-off keeps it fair (cost, upkeep, prerequisites, limited uses, etc.)
