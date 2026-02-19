# Aeonis: Tiles

The tile system in *Aeonis* forms the foundation of exploration, conquest, and resource management. Each hexagonal tile represents a unique area of the realm, offering resources, strategic opportunities, and challenges.

---

## Terrain Tiles

### PLAINS

- **Default Resource Production:** +1 Population.
- **Building Option:** Farm (enhances to +2 Population).
- **Strategic Role:** Essential for population growth and sustaining armies.

### FORESTS

- **Default Resource Production:** +1 Mana.
- **Building Option:** Grove (enhances production to +3 Mana).
- **Strategic Role:** Key for magical strategies and spellcasting.

### MOUNTAINS

- **Default Resource Production:** +1 Gold.
- **Building Option:** Mine (enhances production to +3 Gold).
- **Strategic Role:** Vital for economic development and wealth generation.

### DESERTS

- **Default Resource Production:** +1 Influence.
- **Building Option:** Embassy (enhances production to +3 Influence).
- **Strategic Role:** Focused on diplomacy, trade, and political dominance.

### LAKES

- **Default Resource Production:** None.
- **Building Options:** None by default. (See **Bridge** below for the one exception.)
- **Special Rule (baseline):** Lakes are **impassable** and cannot be occupied.
- **Strategic Role:** Creates natural barriers and chokepoints on the map.

#### Bridge (Infrastructure, Lake exception)

To keep maps from hard-stalling behind water, Lakes can be opened up via bridges:

- **Build condition:** You may build a Bridge on a Lake hex if you control at least one **adjacent non-Lake hex**.
- **Effect:** A bridged Lake becomes a **passable** hex:
  - Movement cost to enter: **1 AP**
  - It can be **occupied**, fought over, and controlled like a normal hex.
  - It produces **no resources**.
- Bridge details (costs, capture/destroy) are defined in `Buildings.md`.

---

## Special Tiles

### CITIES

- **Base Production:** +2 Population and various combinations of resources.
- **Building Capacity:** Supports up to 2 buildings (expandable to 3).

### RUINS

- **Base Production:** Varies by ruin.
- **Exploration Rewards:** Includes artifacts, Gold, Mana, or Influence.

### PORTALS

Mystical gateways that allow instant movement between distant locations on the map.

- **Rules:**
  - Portals are considered adjacent to all other Portal tiles, regardless of their physical placement on the map.
  - Portals produce **no resources**.
  - **Entering/exiting** a Portal hex follows normal movement costs (see `Movement.md`).
  - **Portal travel** (Portal to Portal) is a special move (see `Movement.md` for costs and permissions).
  - **Control:** Portals start **neutral**. A Portal is controlled if:
    - A player occupies it at the start of their turn, or
    - A player has a **Tower** on it.
- **Building Options:**
  - **Tower:** Grants control of the Portal and extends defensive influence to nearby tiles.
  - **Legendary Buildings:** Certain powerful structures may be tied to Portals, offering unique abilities.
- **Strategic Role:** Portals create dynamic movement options, connecting distant parts of the map and encouraging conflict over their control.

---

## Lord Regions

Each Lord's starting region can include standard tiles or unique tiles exclusive to their design. These unique tiles reflect the Lord's theme, abilities, and strategic focus. Not all Lords need to have unique tiles, allowing flexibility and variety in region design.

## Unique Tiles (canon rules)

Unique tiles are a lightweight way to introduce **asymmetry** without adding more units or cards. They are implemented as **normal hex tiles** with a small amount of extra rules text.

### 1) Defined on the Lord Sheet

- Unique tiles are detailed on the associated Lord Sheet, which provides their resource production, special rules, and any interactions with buildings or units.

### 2) What a Unique Tile must specify

Each unique tile definition should include:

- **Tile type**: what it counts as for movement (Plains/Forest/Mountain/Desert/City/Lake/etc.)
- **Production**: what the tile produces during Production & Upkeep
- **Building permissions**: whether it allows a production building (Farm/Mine/Grove/Embassy) and/or which buildings are restricted
- **Special rule text**, written as either:
  - **Controller benefit** (anyone controlling the tile gets it), and/or
  - **Owner-only benefit** (only the Lord/faction that owns the tile gets it, and only while they control it)

### 3) Control and capture

- Unique tiles follow the **standard control rules**: they can be occupied, fought over, and captured like any other hex.
- Unless a tile explicitly says otherwise, **production goes to the current controller**.
- Any **Owner-only** rule on a unique tile is active **only if the owning Lord controls the tile**.

### 4) Balance defaults

To keep unique tiles flavorful but fair:

- If a unique tile has "above-rate" production, it should usually have a **building restriction** (e.g., "cannot build Groves here").
- If a unique tile grants a powerful effect, prefer writing it as **Owner-only** so opponents can disrupt it by capturing the tile (counterplay).

## Flexibility in Region Design

- Some Lords may have **0 unique tiles**, relying on standard terrain and tiles for balance.
- Others may have **1 or more unique tiles** in their starting region, enhancing their strategic options or thematic flavor.

---

## Synergy with Other Systems

1. **Resource Production:** All basic terrain tiles inherently produce one resource by default. Placing the appropriate building on the tile enhances its production but does not replace the base resource.

2. **Control:** A player must control a tile (via units, buildings, or adjacent cities) to extract its resources.

3. **Exploration:** Tiles are revealed when entered and immediately begin producing their base resources unless occupied by enemies or left neutral.

4. **Building Slots:**
   - **Basic Terrain Tiles:** 1 building each.
   - **Special Tiles (e.g., Cities, Portals):** Allow for multiple buildings.

---

## Tile Control

In *Aeonis*, controlling hexes is vital for resource generation, movement, and strategic dominance.

### Ways to Control a Tile

- **Unit Presence:** A hex is controlled if a player has units stationed there at the start of their turn.
- **Building Control:** If a player constructs a building on a hex, it remains under their control unless conquered.
- **City Influence:** Cities exert control over adjacent hexes unless another player contests them.
- **Special Abilities or Spells:** Some Lords, abilities, or artifacts grant control over hexes in unique ways.

---

## Borders & Zones of Control

### Border Mechanics

- **City Influence Borders:**
  - A City exerts control over **all adjacent hexes**, even if they do not contain units or buildings.
  - Cities can exert influence over **neutral hexes**, allowing passive expansion.
  - High Council motions may expand or restrict borders (see `High_Council.md`).

- **Unit-Based Borders:**
  - Units stationed in a hex claim it at the **start of a round** if no enemy units are present.
  - Units in controlled hexes extend influence to **adjacent neutral hexes** but do not claim them immediately.

- **Fortifications & Towers:**
  - **Towers** extend influence **two hexes outward**, making them strong strategic points.
  - **Fortresses** prevent adjacent hexes from being claimed without military conquest.

### Zone of Control (ZOC) Rules (canon)

ZOC is generated by **military units**, not by hex control alone. A hex is in a player's ZOC if it is **adjacent to one or more of that player's military units** (Infantry, Cavalry, Archers, or Lord).

- **ZOC AP penalty:** Entering an enemy's ZOC hex costs **+1 additional AP** on top of the normal terrain movement cost.
- **Moving through undefended territory:** You may enter enemy-controlled hexes that are **not** in ZOC without paying the surcharge. Controlling territory without units to back it up leaves it vulnerable to incursion.
- **Controlled hex restriction:** You cannot enter an **enemy-controlled hex** unless you:
  - Pay the ZOC surcharge (if in ZOC), or
  - Have a treaty or Open Borders motion allowing movement (see `High_Council.md`), or
  - Are initiating an Attack action against that hex (see `Combat.md`).
- **Cavalry flanking:** Cavalry ignore the ZOC AP penalty when entering the **first** enemy ZOC hex during a Move action. This represents their ability to outmaneuver defensive screens and create flanking opportunities. See also `Movement.md`.
- **Buildings do not generate ZOC:** A Tower or Fortress extends **influence** (for control and border purposes) but does not generate ZOC by itself. Only units on the board generate ZOC.

---

## Neutral Hexes & Claiming Unclaimed Land

Neutral hexes represent **unclaimed land** that players must **actively secure**.

### Methods to Claim Neutral Hexes

1. **Moving a Unit into a Neutral Hex** (normal movement cost): The hex is **claimed immediately** if uncontested. If another player contests the claim within the same round, a diplomatic or military resolution occurs.

2. **Extending Influence from a Controlled City or Tower**: Some hexes may **passively become controlled** if they are adjacent to a City or Tower for two consecutive rounds.

3. **Diplomatic Influence**: Players can spend **Influence** to claim neutral hexes without sending units. Example: **Imperial Annexation (Decree)** can claim a neutral hex adjacent to your territory by paying Influence (see `High_Council.md`).

4. **Exploration & Event-Based Claims**: Some hexes require exploration events to be resolved before they can be claimed. A Lord may have a faction-specific ability allowing them to claim hexes faster.

### Contested Neutral Hexes

If two or more players attempt to claim the same hex:

1. **If a unit is present, control goes to the player with the unit.**
2. **If no units are present**, control is decided by:
    - Influence expenditure (highest bid of Influence wins).
    - A High Council ruling (if a motion is proposed).

---

## Strategic Hexes & Unique Control Bonuses

Some hexes offer unique benefits when controlled, incentivizing competition over key locations.

### Types of Strategic Hexes

| Hex Type           | Control Benefit                                                    |
| :----------------- | :----------------------------------------------------------------- |
| **Artifact Sites** | Temporary markers placed by Events. A face-up Artifact Card is displayed; spend 1 AP to claim it (see `Artifacts.md`). |
| **Mana Wells**     | Produces +1 extra Mana per round for the controlling player.       |
| **Trade Hubs**     | Provides 1 extra Gold per round and +1 Gold per trade in region.   |
| **Ancient Ruins**  | Exploring grants relics, VP, or hidden event-based effects.        |
| **Sacred Sites**   | Controlling grants +1 Influence per round and may affect Renown.   |
| **Portals**        | Provides free movement between Portal hexes for the controller.    |

### Hexes That Change Over Time

Some hexes shift control conditions based on game events:

- A **Mana Well** could become corrupted, reducing its yield unless cleansed.
- A **Ruined City** could be rebuilt into a functional City with enough investment.
- A **Trade Hub** could be destroyed by an event, removing its benefits.

---

## Hex Conflicts & Retaking Control

Losing control of hexes can occur through:

- **Military Conquest**: If an enemy wins an attack against a controlled hex, they claim the hex (and may occupy it up to the hex's unit cap).
- **Diplomatic Pressure**: A High Council ruling could strip control of a hex from one player and transfer it to another.
- **Influence Takeovers**: Players may spend Influence to take control of an adjacent hex if the original owner lacks units or buildings.

### Hex Retaking & Sabotage

- Players can attempt to sabotage a controlled hex by:
  - Spending Influence to incite rebellion (forcing the owner to spend resources or lose control).
  - Using Espionage or Spells to temporarily disrupt control.
  - Destroying buildings or improvements, rendering the hex useless.

---

## High Council & Global Influence on Hex Control

The **High Council** plays a role in determining border disputes and hex control through various motions. See `High_Council.md` for the full procedure and ready-to-play motion templates.

| Motion (type)                      | Effect                                                                              |
| :--------------------------------- | :---------------------------------------------------------------------------------- |
| **Imperial Annexation (Decree)**   | Claim a neutral adjacent hex by paying Influence.                                   |
| **Border Arbitration (Decree)**    | Resolve a contested border hex by Influence commits / Speaker tie-break.            |
| **Demilitarized Zone (Decree)**    | Prevent attacks into a region until end of round.                                   |
| **Open Borders Treaty (Decree)**   | Allow movement through another player's territory under specified terms.            |
| **Road Networks (Law)**            | Reduce movement costs in specified terrain (often Plains).                          |

---

## Summary of Hex Control & Influence

1. **Control is established through units, buildings, or City influence.**
2. **ZOC is generated by military units (not buildings or passive control) and costs +1 AP to enter.**
3. **Cavalry ignore the ZOC penalty on their first ZOC hex per Move action (flanking).**
4. **Neutral hexes can be claimed through movement, Influence, or High Council motions.**
5. **Strategic hexes provide key resources, encouraging conflict.**
6. **Control can shift through military conquest, diplomatic actions, or special abilities.**
7. **The High Council can influence borders, annexations, and trade routes.**
