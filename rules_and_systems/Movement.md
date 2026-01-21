# **Aeonis: The Shattered Empire - Movement System**

## **Core Movement Mechanics**

### **1. Action Points (AP) for Movement**

- **Move is an action**: on your turn, you may take a **Move** action and spend AP to move **one group** (any number of units stacked in one hex) along a path.
- **AP cost = path cost**: pay the total AP cost of the path you take, where each entered hex has a movement cost (terrain and effects can modify this).
- **Movement range caps distance**: a group may enter at most \(X\) hexes during a single Move action, where \(X\) is the **lowest Movement Range** among units in the group (see Unit-Specific Movement Rules).

### **Combat interaction (important)**

- **Attacks are declared** into a target hex; units do not automatically “move into a hex to fight.”
- To initiate combat, you must have units **adjacent** to the target hex (unless a spell/portal effect says otherwise) and spend an **Attack** action (see `Combat.md`).
- If the attacker wins, they may **occupy** the target hex with up to the hex’s unit cap (see `Combat.md`).

---

## **Worked Examples (AP cost + Movement Range)**

### **Example 1: Infantry across mixed terrain**

- Group: 2 Infantry (Movement Range 1)
- Path: Plains → Forest (2 hexes total)
- Result: The group may enter **only 1 hex** this Move action (because Infantry range is 1). If it enters the Plains, it pays **1 AP**.

### **Example 2: Cavalry on Plains**

- Group: 1 Cavalry (Movement Range 2)
- Path: Plains → Plains (2 hexes total)
- Result: The group may enter **2 hexes** this Move action. Because Cavalry can traverse Plains at **1 AP per 2 hexes**, the total cost is **1 AP**.

### **2. Terrain Effects on Movement**

Different terrain types impact movement costs and strategies, emphasizing the importance of terrain control and map awareness.

| Terrain Type     | Base Movement Cost | Special Rules                                                   |
|-------------------|--------------------|-----------------------------------------------------------------|
| **Plains**        | 1 AP per hex       | No restrictions, optimal for fast traversal.                   |
| **Forests**       | 1 AP per hex       | Defensive bonus for units ending their movement here.          |
| **Mountains**     | 2 AP per hex       | Requires special abilities, infrastructure, or Lords to traverse efficiently. |
| **Deserts**       | 2 AP per hex       | Units lose 1 Population if they spend more than 2 turns here.  |
| **Lakes**         | Impassable         | Lakes cannot be entered/occupied unless they have a **Bridge** (see `Tiles.md` / `Buildings.md`). |
| **Cities**        | 1 AP per hex       | Acts as a hub for faster travel (see Teleportation below).      |

- **Special Tile Effects:**
  - **Portals:** Units move between Portals without AP cost but must spend 1 AP to enter/exit.
  - **Trade Hubs:** Reduce AP costs for adjacent hexes by 1 for trade-related units or caravans.

---

### **3. Unit-Specific Movement Rules**

Each unit type interacts with the movement system differently, creating strategic trade-offs.

| Unit Type         | Movement Range (Hexes/Turn) | Special Movement Rules                                    |
|--------------------|----------------------------|----------------------------------------------------------|
| **Infantry**       | 1 hex                      | No special movement bonuses, effective for defense.       |
| **Cavalry**        | 2 hexes                    | Can traverse Plains at 1 AP per 2 hexes for rapid movement.|
| **Archers**        | 1 hex                      | Gain bonuses when moving into Forests.                   |
| **Advanced Units** | Varies                     | Examples: Flying units ignore terrain penalties.          |

---

### **4. Portals and Teleportation**

Portals and magical movement are key to the strategic flexibility and dynamic nature of *Aeonis*.

- **Portals:**
  - **Movement Rules:** Portals connect distant parts of the map and are considered adjacent for movement purposes.
  - **Cost:** Entering/exiting a Portal costs 1 AP.
  - **Portal travel (Portal → Portal):**
    - Cost: **0 AP** (you are “stepping through” the network).
    - Permission: you may use Portal travel if the **destination Portal** is **neutral** or **controlled by you**.
      - If the destination Portal is controlled by another player, you may only travel there if a treaty/motion allows it (e.g., **Open Borders Treaty** in `High_Council.md`).
  - **Strategic Role:** Portals create critical chokepoints and encourage territorial conflict.

- **Teleportation Spells:**
  - High-tier **Arcane Discovery** or artifact-based abilities allow unit teleportation:
    - Example: **Translocation (Tier 2):** Spend 3 Mana and 1 AP to teleport a unit group to any controlled hex.

---

### **5. High Council Integration**

The High Council can influence movement through decrees or policies:

- **Road Networks Motion:** Reduces movement costs on Plains or between Cities by 1 AP.
- **Borders Motion:** Certain decrees block or restrict movement into specific regions or hexes.

---

## **Strategic Implications of the Movement System**

1. **Action Point Economy:**
    - Movement consumes AP, creating tension between positioning and other actions like combat or building infrastructure.
    - Players must optimize their movement paths to conserve AP for other critical actions.

2. **Terrain as a Strategic Resource:**
    - Mountains, Deserts, and Lakes create natural barriers that shape the map and force tactical decisions.
    - Controlling Portals or building infrastructure to mitigate terrain penalties becomes vital.

3. **Dynamic Engagements:**
    - Portals and teleportation allow players to strike unexpectedly or reposition units quickly, fostering dynamic and unpredictable gameplay.

4. **Faction-Specific Bonuses:**
    - Lords with movement-based bonuses (e.g., Cavalry-focused factions or Lords with magical teleportation abilities) gain unique advantages, creating asymmetry.

---

## **Advanced Options**

1. **Infrastructure (optional rules):**
    - **Bridges** can make Lakes passable (see `Tiles.md` / `Buildings.md`).
    - Broad “road network” effects are typically handled via High Council motions (see `High_Council.md`, e.g. **Road Networks**).

2. **Event-Based Modifiers:**
    - Events can temporarily alter movement rules:
        - **Winter’s Grip:** All movement costs +1 AP for the round.
        - **Festival of Winds:** Reduce movement costs for Cavalry by 1 AP this round.

3. **Reinforcement Mechanic:**
    - Players can spend additional AP to **fast-travel** reinforcements from Cities to the frontlines (e.g., 2 AP to move a group of units to any controlled City).

---

### **Example Gameplay Scenarios**

1. **Cavalry Exploits Plains:**
    - Player A uses Cavalry to rapidly traverse 2 hexes of Plains for 1 AP, flanking Player B’s slower Infantry-heavy army.

2. **Portal Choke Point:**
    - Player C blocks access to a Portal hex, forcing Player D to take the long way around, costing additional AP and time.

3. **Winter’s Grip:**
    - A Global Event increases all movement costs, stranding Player E’s army in a Mountain hex as Player F capitalizes with faster units on Plains.

---
