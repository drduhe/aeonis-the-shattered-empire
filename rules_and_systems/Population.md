# Aeonis: Population

## Overview

Population represents the Lord’s ability to sustain and field military units, as well as maintain key infrastructure. It acts as a soft limit on a Lord’s growth and strategic options, encouraging careful planning and resource allocation.

**Core constraint model (canon):**

- **Population is the primary hard cap** on how many units/buildings you can have in play. In general, you cannot “temporarily overbuild” beyond your available Population Pool.
- **Basic units have no Gold upkeep**. Infantry/Cavalry/Archers are constrained by Population, not by per-round resource taxes.
- **Resource upkeep (Gold/Mana/Influence)**, if used, is reserved for **advanced units** and **advanced/legendary buildings** (see `Trade_Taxes.md`).

---

## Core Mechanics

### 1. **Population Pool**

- Each Lord starts with a **base Population Pool** (e.g., 10 Population Points).
- Population Points represent **available capacity**.
- When you recruit a unit or build a Population-maintained building, you must have enough Population Points available; those points remain **tied up** while the unit/building remains in play.
- Population Points are **refunded immediately** when a unit is destroyed/dismissed or a building is demolished/destroyed.

Examples (baseline):

- **Infantry**: occupies 1 Population
- **Cavalry**: occupies 2 Population
- **Archers**: occupies 1 Population
- **Tower**: occupies 1 Population

Note:

- This is a **hard cap** system; players can always “free capacity” by dismissing/scuttling units and then building/recruiting new ones.

---

### 2. **Population Cap**

- The **Population Cap** limits the maximum Population Pool a Lord can sustain.
- **Ways to Increase the Population Cap:**
  - **Plains and Cities:**
    - **Plains with Farms:** +2 Population Cap per Farm.
    - **Cities:** Each controlled City increases the Population Cap by +3.
  - **Special Buildings:**
    - Example: **Castle:** Increases Population Cap by +3.
  - **Research and Abilities:**
    - Example: Certain spells or technologies may temporarily or permanently increase the Population Cap.
- A **Global Cap** (e.g., maximum 25 Population Points per Lord) ensures balance.

---

### 3. **Population Growth**

- **Base Growth Rate:** Lords replenish +1 Population Point per round, up to their current Population Cap.
- **Modifiers to Growth Rate:**
  - **Plains:** Each controlled Plains tile adds +1 to the Growth Rate.
  - **Cities:** Each controlled City adds +2 to the Growth Rate.
  - **Unique Abilities:** Certain Lords, tiles, or buildings can further boost growth.
- **Population Overflow:** Population Growth cannot exceed the current Population Cap; any surplus is lost.

---

### 4. **Building Costs and Maintenance**

- Some buildings require **Population Points** to construct and operate (i.e., to be maintained by population capacity):
  - **Farm:** Costs 1 Population to construct but increases Population Cap by +2.
  - **Tower:** Costs 1 Population to construct and maintain.
  - **Academy:** Costs 2 Population to maintain but grants powerful magical abilities.
  - **Legendary Buildings:** Each occupies **3 Population** (reserved capacity while the building exists). See `Buildings.md`.
- Population costs for buildings are **not paid each round**; they are **reserved capacity** while the building exists.

---

### 5. **Unit Costs and Maintenance**

- **Recruitment Cost:** When a new unit is recruited, it immediately consumes Population Points from the current Population Pool.
- **Ongoing Maintenance:** Units continue to occupy Population Points while they remain active on the board.
  - Example:
    - **Infantry:** Occupies 1 Population
    - **Cavalry:** Occupies 2 Population
- Population Points are refunded when a unit is destroyed or dismissed.

---

## Advanced Mechanics

### 1. **Population Attrition**

- **Costs of Expansion and War:**
  - Losing battles reduces the Population Pool as units are destroyed.
  - Losing control of key tiles (e.g., Cities or Plains) may lower the Population Cap, leading to penalties (e.g., -1 resource production per excess Population Point).
- **Repopulation Mechanic:**
  - Lords naturally replenish lost Population Points each round based on growth mechanics.
  - Example: Recover +1 Population Point per round per controlled City or Plains.

---

### 2. **Population Events**

- Thematic events may impact Population, creating dynamic gameplay:
  - **Famine:** Reduce Population Pool by -2 unless sufficient Food resources are stockpiled.
  - **Migration:** Gain +3 Population Points if a specific event is triggered (e.g., capturing specific hexes).
  - **Plague:** All Lords lose -1 Population Point per round for 3 rounds.

---

### 3. **Population Synergy with Other Systems**

- **Renown Synergy:**
  - High Renown may attract temporary Population boosts.
    - Example: “Hero of the Realm” adds +5 Population Points for 3 rounds.
  - Infamous Lords may face Population penalties due to unrest or rebellion.
- **Tile Synergy:**
  - Population-heavy strategies encourage the control of Plains and Cities, creating hotspots for conflict.
- **Building Synergy:**
  - Advanced buildings may reduce the Population cost of certain units.
    - Example: **Academy:** Reduces the Population cost of magical units by -1.

---

## Strategic Role of Population

This system maintains strategic depth while simplifying management:

1. **Trade-Offs:** Players must decide between fielding larger armies or building infrastructure that consumes Population Points.
2. **Expansion Pressure:** Controlling key tiles becomes essential to sustain growth and maintain dominance.
3. **Dynamic Balance:** Population costs for buildings and units create a natural ebb and flow, rewarding efficient resource and territory management.
