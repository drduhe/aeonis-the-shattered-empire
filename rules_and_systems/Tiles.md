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
- **Strategic Role:** Key for magical strategies and Arcane research.

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

- **Base Production:** +2 Population growth per controlled City during Production & Upkeep (see `Population.md` §3). Cities do **not** print Gold, Mana, or Influence by themselves — only buildings on the City hex (or terrain production on other hexes) generate trade resources.
- **AP bonus:** +1 AP per controlled City, max +2 from Cities (see `Actions.md`).
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

2. **Control:** A player must **control** a tile to extract its resources during Production & Upkeep (see Tile Control below for how control is gained).

3. **Exploration:** Tiles are revealed when entered and immediately begin producing their base resources unless occupied by enemies or left neutral.

4. **Building Slots:**
   - **Basic Terrain Tiles:** 1 building each.
   - **Special Tiles (e.g., Cities, Portals):** Allow for multiple buildings.

---

## Tile Control (canon)

In *Aeonis*, controlling hexes is vital for resource generation, movement, and strategic dominance. **Control** and **ZOC** are different things: control determines who produces from a hex; ZOC (generated only by units) determines movement penalties.

### Ways to gain control of a hex

1. **Unit Presence:** At **Round Start**, each hex containing only your units becomes controlled by you.
2. **Conquest:** Winning a battle for a hex gives you control of it **immediately** (see `Combat.md`).
3. **Occupation:** Moving into a **neutral** hex claims it **immediately** if no other player's units are there. Moving into an **enemy-controlled** hex with no enemy units present flips it to you at the next **Round Start** (per rule 1) — walking into undefended territory takes it, but not instantly.
4. **Building Presence:** A hex containing your building remains under your control unless conquered, even with no units present.
5. **Adjacency Claim (passive expansion):** At **Cleanup & Checks**, each **neutral** hex that has been adjacent to a City or Tower you control for **two consecutive Cleanup checks**, and contains no other player's units, becomes controlled by you. (Track with a marker after the first check.)
6. **Influence & Council:** Annexation motions, arbitration, and Influence takeovers (see `High_Council.md`).
7. **Special Abilities:** Some Lords, discoveries (e.g., **Boundary Stones**, `Arcane.md`), or artifacts grant control in unique ways; they say so explicitly.

### Losing control

- You lose control of a hex the moment another player gains it by any method above.
- Controlled hexes with **no units and no buildings** stay yours until someone takes them — but they are undefended: enemies may enter them without ZOC surcharge and flip them (method 3).

---

## Borders & Zones of Control

### Influence vs control (borders)

Cities and Towers project **influence**, which is *not* control by itself:

- **Influence** gives you the **Adjacency Claim** (method 5 above) and **priority in contested neutral claims** (see Contested Neutral Hexes below).
- **Towers** project influence to hexes within **2 hexes**; Cities to **adjacent** hexes.
- **Fortresses** prevent adjacent hexes from being claimed by the Adjacency Claim or by Influence expenditure — enemies must use units (occupation or conquest).
- High Council motions may expand or restrict borders (see `High_Council.md`).

### Zone of Control (ZOC) Rules (canon)

ZOC is generated by **military units**, not by hex control alone. A hex is in a player's ZOC if it is **adjacent to one or more of that player's military units** (Infantry, Cavalry, Archers, or Lord).

- **ZOC AP penalty:** Entering an enemy's ZOC hex costs **+1 additional AP** on top of the normal terrain movement cost.
- **Moving through undefended territory:** You may enter enemy-controlled hexes that are **not** in ZOC without paying the surcharge. Controlling territory without units to back it up leaves it vulnerable to incursion.
- **Controlled hex restriction:** You cannot enter an **enemy-controlled hex** unless you:
  - Pay the ZOC surcharge (if in ZOC), or
  - Have a treaty or Open Borders motion allowing movement (see `High_Council.md`), or
  - Are initiating an Attack action against that hex (see `Combat.md`).
- **Cavalry flanking:** Cavalry ignore the ZOC AP penalty when entering the **first** enemy ZOC hex during a Move action. This represents their ability to outmaneuver defensive screens and create flanking opportunities. See also `Movement.md`.
- **Lord exceptions:** Rakhis's Sandstride ignores every ZOC surcharge during his Move actions. Elyndra's Deep Roots treats two controlled Forests as adjacent for one group Move per round. These abilities do not change which units generate ZOC; see `Movement.md` and the Lord sheets.
- **Buildings do not generate ZOC:** A Tower or Fortress extends **influence** (for control and border purposes) but does not generate ZOC by itself. Only units on the board generate ZOC.

---

## Neutral Hexes & Claiming Unclaimed Land

Neutral hexes represent **unclaimed land** that players must **actively secure**.

### Methods to Claim Neutral Hexes

1. **Moving a Unit into a Neutral Hex** (normal movement cost): The hex is **claimed immediately** if no other player's units are present (Tile Control method 3).

2. **Adjacency Claim from a City or Tower**: Neutral hexes within influence range become controlled after **two consecutive Cleanup checks** (Tile Control method 5).

3. **Diplomatic Influence**: Players can spend **Influence** to claim neutral hexes without sending units. Example: **Imperial Annexation (Decree)** can claim a neutral hex adjacent to your territory by paying Influence (see `High_Council.md`).

4. **Exploration & Event-Based Claims**: Some hexes require exploration events to be resolved before they can be claimed. A Lord may have a faction-specific ability allowing them to claim hexes faster.

### Contested Neutral Hexes

If two or more players attempt to claim the same hex:

1. **If exactly one player has units present, control goes to that player.**
2. **If no units are present** (e.g., competing Adjacency Claims resolving on the same Cleanup), control is decided by:
    - Influence expenditure (open bid; highest total Influence spent wins; spent Influence is discarded).
    - If no one bids (or bids tie), the hex **stays neutral**; a High Council motion (e.g., **Border Arbitration**) may settle it.

**First Playable sim rule:** When the automated simulator resolves Cleanup and two or more players both qualify for the same neutral Adjacency Claim with no units present, the hex **stays neutral** (no Influence bidding). Full-table play uses the Influence bid above.

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
  - Using Whisper Cards (e.g., **Saboteur**, see `Whispers.md`) or Rituals to temporarily disrupt control.
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

1. **Control is established through unit presence, conquest, buildings, the 2-round Adjacency Claim, Influence, or explicit abilities.**
2. **ZOC is generated by military units (not buildings or passive control) and costs +1 AP to enter.**
3. **Cavalry ignore the ZOC penalty on their first ZOC hex per Move action (flanking).**
4. **Neutral hexes can be claimed through movement, Influence, or High Council motions.**
5. **Strategic hexes provide key resources, encouraging conflict.**
6. **Control can shift through military conquest, diplomatic actions, or special abilities.**
7. **The High Council can influence borders, annexations, and trade routes.**
