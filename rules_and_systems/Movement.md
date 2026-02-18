# Aeonis: Movement System

## Core Movement Mechanics

### 1. Action Points (AP) for Movement

- **Move is an action**: on your turn, you may take a **Move** action and spend AP to move **one group** (any number of units stacked in one hex) along a path.
- **AP cost = path cost**: pay the total AP cost of the path you take, where each entered hex has a movement cost (terrain and effects can modify this).
- **Movement Range caps distance**: a group may enter at most X hexes during a single Move action, where X is the **lowest Movement Range** among units in the group (see Unit-Specific Movement Rules).

### Combat interaction (important)

- **Attacks are declared** into a target hex; units do not automatically "move into a hex to fight."
- To initiate combat, you must have units **adjacent** to the target hex (unless a spell/portal effect says otherwise) and spend an **Attack** action (see `Combat.md`).
- If the attacker wins, they may **occupy** the target hex with up to the hex's unit cap (see `Combat.md`).

---

## 2. Terrain Effects on Movement

Different terrain types impact movement costs and strategies.

| Terrain Type  | Base Movement Cost | Special Rules                                                                             |
| ------------- | ------------------ | ----------------------------------------------------------------------------------------- |
| **Plains**    | 1 AP per hex       | No restrictions, optimal for fast traversal.                                              |
| **Forests**   | 1 AP per hex       | Defensive bonus for units ending their movement here.                                     |
| **Mountains** | 2 AP per hex       | Difficult terrain; requires special abilities or infrastructure to traverse efficiently.   |
| **Deserts**   | 2 AP per hex       | Difficult terrain; units lose 1 Population if they spend more than 2 turns here.          |
| **Lakes**     | Impassable         | Cannot be entered/occupied unless they have a **Bridge** (see `Tiles.md` / `Buildings.md`). |
| **Cities**    | 1 AP per hex       | Acts as a hub for recruitment and faster travel.                                          |

- **Special Tile Effects:**
  - **Portals:** Units move between Portals without AP cost but must spend 1 AP to enter/exit.
  - **Trade Hubs:** Reduce AP costs for adjacent hexes by 1 for trade-related units or caravans.

---

### 3. Unit-Specific Movement Rules

Each unit type interacts with the movement system differently, creating strategic trade-offs.

| Unit Type          | Movement Range (hexes/Move) | Special Movement Rules                                                          |
| ------------------ | --------------------------- | ------------------------------------------------------------------------------- |
| **Infantry**       | 1 hex                       | No special movement bonuses, effective for defense.                             |
| **Cavalry**        | 2 hexes                     | Can traverse Plains at 1 AP per 2 hexes. **Ignores ZOC penalty on first ZOC hex per Move action (flanking).** |
| **Archers**        | 1 hex                       | No special movement bonuses.                                                    |
| **Lord (Leader)**  | varies                      | Defined on the Lord Sheet; uses normal terrain costs unless a Lord ability says otherwise. |
| **Advanced Units** | varies                      | Examples: Flying units ignore terrain penalties.                                |

### Cavalry Flanking (canon)

Cavalry have a unique battlefield role: they can outmaneuver defensive screens and exploit gaps.

- When a group containing Cavalry enters an enemy ZOC hex (a hex adjacent to enemy military units), the **ZOC +1 AP penalty is ignored for the first such hex** entered during that Move action.
- Subsequent enemy ZOC hexes entered during the same Move action still incur the +1 AP surcharge as normal.
- This interacts with Cavalry's 2-hex Movement Range to allow flanking maneuvers around enemy front lines.
- See `Tiles.md` for the full ZOC rules.

---

### 4. Portals and Teleportation

Portals and magical movement are key to strategic flexibility.

- **Portals:**
  - **Movement Rules:** Portals connect distant parts of the map and are considered adjacent for movement purposes.
  - **Cost:** Entering/exiting a Portal costs 1 AP.
  - **Portal travel (Portal to Portal):**
    - Cost: **0 AP** (you are "stepping through" the network).
    - Permission: you may use Portal travel if the **destination Portal** is **neutral** or **controlled by you**.
      - If the destination Portal is controlled by another player, you may only travel there if a treaty/motion allows it (e.g., **Open Borders Treaty** in `High_Council.md`).
  - **Strategic Role:** Portals create critical chokepoints and encourage territorial conflict.

- **Teleportation Spells:**
  - High-tier Arcane Discovery or artifact-based abilities allow unit teleportation:
    - Example: **Translocation (Tier II, TRN):** When you take a Move action, you may pay **1 AP** and spend **3 Mana** to teleport a unit group to any controlled hex (see `Arcane.md`).

---

### 5. Zone of Control and Movement

ZOC is generated by **military units** (Infantry, Cavalry, Archers, Lords), not by passive hex control or buildings. See `Tiles.md` for full ZOC rules.

- **ZOC penalty:** Entering a hex that is adjacent to one or more enemy military units costs **+1 AP** on top of normal terrain cost.
- **Cavalry exemption:** Cavalry ignore the ZOC penalty on the **first** enemy ZOC hex entered during a Move action (see Cavalry Flanking above).
- **Entering enemy-controlled hexes:** You cannot enter an enemy-controlled hex unless you pay ZOC surcharge (if applicable), have a treaty/motion, or are attacking.
- **Undefended territory:** Enemy-controlled hexes with no nearby enemy units are **not** in ZOC and can be entered at normal terrain cost (they are vulnerable to incursion).

---

### 6. High Council Integration

The High Council can influence movement through decrees or policies:

- **Road Networks Motion:** Reduces movement costs on Plains or between Cities by 1 AP.
- **Borders Motion:** Certain decrees block or restrict movement into specific regions or hexes.
- **Open Borders Treaty:** Allows movement through another player's controlled hexes without restriction.

---

## Strategic Implications of the Movement System

1. **Action Point Economy:** Movement consumes AP, creating tension between positioning and other actions like combat or building infrastructure.

2. **Terrain as a Strategic Resource:** Mountains, Deserts, and Lakes create natural barriers that shape the map and force tactical decisions. Controlling Portals or building infrastructure to mitigate terrain penalties becomes vital.

3. **ZOC as Active Defense:** Because ZOC is generated by units (not passive control), players must actively position units to create defensive screens. Ungarrisoned territory is strategically vulnerable even if nominally "controlled."

4. **Cavalry as Flankers:** The ZOC exemption means Cavalry can punch through the first layer of a defensive line at normal cost, making them the premiere unit for aggressive maneuvers and raids.

5. **Dynamic Engagements:** Portals and teleportation allow players to strike unexpectedly or reposition units quickly, fostering dynamic and unpredictable gameplay.

---

## Advanced Options

1. **Infrastructure (optional rules):**
    - **Bridges** can make Lakes passable (see `Tiles.md` / `Buildings.md`).
    - Broad "road network" effects are typically handled via High Council motions (see `High_Council.md`).

2. **Event-Based Modifiers:**
    - Events can temporarily alter movement rules:
        - **Winter's Grip:** All movement costs +1 AP for the round.
        - **Festival of Winds:** Reduce movement costs for Cavalry by 1 AP this round.

3. **Reinforcement Mechanic:**
    - Players can spend additional AP to fast-travel reinforcements from Cities to the frontlines (e.g., 2 AP to move a group of units to any controlled City).
