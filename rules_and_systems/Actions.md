# Aeonis: Action Points

## Overview

The Action Point (AP) system governs the number of actions a player can take during the Action Phase. Players perform one action per turn within a round, with each action deducting a variable amount of AP from their pool. This system emphasizes strategic decision-making, deepens synergies with other mechanics, and ensures balanced pacing throughout the game.

---

## Turn Structure and Action Limits

1. **One Action Per Turn**
    - Each player may perform one action per turn during the round.
    - The chosen action deducts AP from their pool based on its cost.

2. **Action Costs**
    - Different actions have different AP costs, reflecting their complexity or impact.
    - **Canonical Action Costs:**
        - **Move**: Pay AP equal to the movement cost of the chosen path for one group (typically 1 AP per hex, modified by terrain and effects). See `Movement.md`.
        - **Attack**: 2 AP per battle initiated. The attacker may pay +1 AP to Press the Attack (see `Combat.md`).
        - **Build**: 3 AP per building constructed.
        - **Recruit**: 1 AP. Place up to 2 units in one controlled City (see §Recruit below).
        - **Research**: 1 AP + the discovery's listed resource cost (see `Arcane.md`).
        - **Cast Spells**: 1-4 AP, depending on the spell's power.
        - **Trade**: 1 AP to initiate a trade (see `Trade_Taxes.md`).
        - **Activate Strategy Card Primary**: Varies based on the card (see `Strategy.md`).
        - **Play an ACTION Whisper**: 0 AP. Play a Whisper Card with ACTION timing from your hand (see `Whispers.md`).

3. **Rotating Turns**
    - Players take turns in initiative order (determined by Strategy Card numbers in the Strategy Selection Phase), performing one action per turn.
    - The rotation continues until all players pass or run out of AP.

4. **Passing**
    - Players may choose to pass on their turn, preserving their remaining AP.
    - Players who pass early may **bank up to 2 unused AP** for the next round.
    - Once a player passes, they cannot take further actions for the remainder of the round.

5. **End of Round**
    - The round ends when all players have passed or when all AP is depleted.

---

## Starting Action Points

Each Lord begins the game with a starting AP pool defined on their Lord Sheet (default: **5 AP**). The AP pool can be expanded during the game through:

- **Renown Thresholds:** +1 AP when reaching 5 Renown, and a free 1-AP action per round at 10 Renown (see `Renown.md`).
- **City Control Bonus:** Each controlled City adds +1 AP per round, **up to a maximum of +2 AP from Cities**.
- **Buildings:** The **Guild Hall** provides +1 AP per round (see `Buildings.md`).
- **Artifacts:** Acquiring specific artifacts may grant temporary or permanent AP boosts.

---

## Recruit (canonical rules)

Recruit is the action used to place new military units on the board.

### Cost

- **1 AP** per Recruit action.

### Procedure

1. Choose **one** controlled City.
2. Place up to **2 units** in that City.
3. Pay each unit's **recruitment cost** from your resources and **Population Pool** (see `Population.md`).

### Unit Recruitment Costs

| Unit Type | Gold Cost | Mana Cost | Population Cost |
| --------- | --------- | --------- | --------------- |
| Infantry  | 1 Gold    | -         | 1 Population    |
| Cavalry   | 2 Gold    | -         | 2 Population    |
| Archer    | 1 Gold    | 1 Mana    | 1 Population    |

### Placement Rules

- Recruited units are placed in the chosen City hex.
- You must have sufficient Population Pool available; recruited units immediately occupy Population (see `Population.md`).
- You may not recruit units you do not have tokens for (see `Components.md`).

### Limits

- Each City may be used for recruitment **at most once per round** (across all your Recruit actions that round).
- You may take the Recruit action multiple times per round (on different turns), but each must target a **different** City.
- A Lord's active abilities or Strategy Cards may override these limits when they explicitly say so.

---

## Gaining and Spending Action Points

### Gaining Additional AP

- **Renown Tiers:** Players gain +1 AP permanently upon reaching 5 Renown. At 10 Renown, players gain 1 free 1-AP action per round.
- **High Council Laws:** Certain laws passed in the High Council may grant temporary or permanent AP boosts.
- **City Control Bonus:** Each controlled City adds +1 AP per round, **maximum +2 AP from Cities total**.
- **Buildings:** The **Guild Hall** grants +1 AP per round.

### Spending Action Points

- **Move Units:** Pay AP equal to the movement cost of the chosen path for one group (see `Movement.md`).
- **Attack:** 2 AP per battle initiated; +1 AP optional to Press the Attack (see `Combat.md`).
- **Build:** 3 AP per building constructed.
- **Recruit:** 1 AP, place up to 2 units in one controlled City (see §Recruit above).
- **Research:** 1 AP + listed resource cost (see `Arcane.md`).
- **Cast Spells:** 1-4 AP, based on spell power.
- **Trade:** 1 AP to initiate (see `Trade_Taxes.md`).
- **Activate Strategy Card Primary:** Varies based on the card.
- **Play an ACTION Whisper:** 0 AP (see `Whispers.md`).

---

## Tile, Building, and Event Synergy

### Tile and Building Synergy

- **Guild Hall (Advanced Building):** +1 AP per round.
- **City Control Bonus:** Each controlled City provides +1 AP (max +2 from Cities), reinforcing their strategic value.

### Dynamic AP Events

- **Famine:** All players lose 1 AP unless they control sufficient food-producing tiles.
- **Festival (Cultural Event):** All players gain +1 AP during the round.
- **Migration:** Temporarily gain +2 AP when controlling specific key hexes or triggering events.

---

## Lord-Specific Actions

Each Lord has unique interactions with the AP system, detailed on their individual Lord Sheets. These traits can include:

- Reducing the AP cost of certain actions (e.g., building structures, attacking).
- Gaining bonus AP under specific conditions (e.g., controlling certain tiles, passing laws).
- Unlocking powerful abilities that consume AP.

---

## Strategic Implications

- **Deepened Synergy:** Population, Renown, and Tiles interact directly with the AP system, creating a unified design that rewards strategic planning.
- **Late-Game Scaling:** AP pools scale with player growth (Cities, Renown, buildings), but the +2 City cap prevents runaway advantage.
- **Recruitment Pacing:** The 2-units-per-city-per-round limit means expansion (more Cities) directly increases your military throughput.
- **Player Agency:** Banked AP, Lord-specific bonuses, and the Build-vs-Recruit tension ensure flexibility while maintaining balance.

---

## Example Scenario

### Setup:

A player (Player A) starts the round with 5 AP. They're competing against two other players.

1. **Turn 1:**
    - Player A moves a group of units into an adjacent hex (1 AP).
    - Player B constructs a building (3 AP).
    - Player C recruits 2 Infantry in their home city (1 AP).

2. **Turn 2:**
    - Player A initiates combat in the hex they moved into (2 AP).
    - Player B recruits units (1 AP).
    - Player C moves units (1 AP).

3. **Turn 3:**
    - Player A recruits reinforcements (1 AP), then passes with 1 AP banked.
    - Player B passes, preserving remaining AP for banking.
    - Player C activates a Strategy Card ability (2 AP).

4. **End of Round:**
    - The round ends once all players have passed.
