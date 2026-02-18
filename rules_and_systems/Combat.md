# Aeonis: Combat

This chapter defines the **canonical** combat system for *Aeonis: The Shattered Empire*.

Design goals:

- **Prevent doomstacking**: unit caps and positional commitments matter.
- **Keep combat fast**: dice rolled scale with the **battle line**, not with total armies.
- **Make sieges special**: **only** Cities/Fortresses can create multi-turn combat state.

Combat is initiated by the **Attack** action (see `Actions.md`) during the **Action Phase** (see `Round_Structure.md`).

---

## 1. Key Concepts

### 1.1 Attacks are declared (units do not automatically "move in to fight")

- When you attack, you **declare an attack against a target hex**.
- You and the defender **commit** units from adjacent hexes to support the battle.
- Units only **occupy** the target hex after a successful attack (see **Aftermath**).

### 1.2 Unit caps and the Battle Line (anti-doomstack core)

Each contested hex has a **Battle Line Cap**:

- **Standard hex**: 3 units
- **City / Fortress**: 5 units

Committed units beyond the cap are **Reserves**.

- Only units on the **Battle Line** roll dice.
- Reserves matter by replacing casualties and sustaining pressure over multiple battle rounds.

---

## 2. Unit Stats (baseline)

| Unit Type     | Attack Die | Defense Die | Hit Points | Notes                                  |
| ------------- | ---------- | ----------- | ---------- | -------------------------------------- |
| Infantry      | d6         | d6          | 1          | baseline                               |
| Cavalry       | d8         | d6          | 2          | tougher, punchier                      |
| Archers       | d6         | d4          | 1          | **Pre-Strike** when on the Battle Line |
| Lord (Leader) | (varies)   | (varies)    | (varies)   | defined on the Lord Sheet; see 2.1     |

---

## 2.1 Lords as Units (canon)

In *Aeonis*, each player's **Lord** is also a **unit on the board** (a single unique "Leader" token).

### 2.1.1 Lord stats (defined on each Lord Sheet)

Each Lord Sheet must specify the Lord unit's:

- **Attack Die**
- **Defense Die**
- **Hit Points**
- **Movement Range**

### 2.1.2 Lord rules (what makes them different)

- **Counts as a unit:** A Lord occupies hexes, moves, commits to battles, and can be placed on the Battle Line like any other unit.
- **Battle Line Cap:** A Lord **counts toward** the Battle Line Cap when on the line.
- **Not destroyed:** When a Lord's HP reaches 0, it is **defeated** (see 2.1.4) instead of being destroyed.
- **Ability gating (default):** Your Lord's abilities are available while your Lord is **not captured**. If an ability requires your Lord to be committed to a battle (or part of a moving group), it will say so.

### 2.1.3 Tracking Lord damage

- Lord HP can be tracked with a small dial, tokens, or a 3-step track.
- **Heal timing (default):** At **Round Start**, each Lord heals to full HP (unless a card/ability says otherwise).

### 2.1.4 Defeating and capturing a Lord

When a Lord's HP reaches 0 during a battle:

- The Lord is **captured** by the opposing side (remove the Lord token from the map and place it with the capturing player as a reminder).
- The capturing player immediately gains:
  - **+2 Renown** (see `Renown.md`)
  - **+1 VP** (see `Victory.md`)
- The captured Lord's owner:
  - May still take turns, score VP, and play normally.
  - **Cannot use Lord abilities** while their Lord is captured (passive and active abilities on the Lord Sheet are disabled).
  - Their Lord unit is unavailable (cannot commit to battles, cannot be part of movement groups).
- **Release timing (default):** At **Cleanup & Checks** of the current round, all captured Lords are **released** and return to their owner's **Home City** at full HP.

Note:

- A released Lord returning to the map does not cost AP and does not count as a Move action.

## 3. Battle Setup

### 3.1 Legal targets

You may declare an attack against a hex if:

- It is **enemy-controlled**, **contested**, or otherwise attackable by scenario rules, and
- You have at least one unit in a hex **adjacent** to the target hex (unless a spell/portal rule allows otherwise).

### 3.2 Commit units

When an attack is declared:

- **Attacker commits** any number of units from adjacent hexes.
- **Defender commits**:
  - Any units already in the target hex, plus
  - Any number of units from adjacent hexes.

Committed units stay in their origin hexes; they are simply "in the fight."

### 3.3 Form the Battle Lines

Each side chooses up to the **Battle Line Cap** units from among their committed units to be **on the Battle Line**.

All other committed units are **Reserves**.

---

## 4. Battle Round (resolution loop)

Each time the attacker spends an **Attack** action against a target hex, resolve **exactly one** battle round using the loop below (with an optional extra round if the attacker "Presses the Attack").

1. **Reinforce Battle Lines**
2. **Archer Pre-Strike**
3. **Attacker Strike**
4. **Defender Counterstrike**
5. **Retreat Check**
6. **Victory Check**

After this battle round is complete, the battle ends for now. If both sides still have surviving committed units, the conflict continues only if the attacker spends another **Attack** action on a later turn (or immediately via **Press the Attack**, below).

### 4.0 Press the Attack (optional, recommended)

After resolving the battle round, the attacker may choose to **Press the Attack**:

- **Cost**: pay **+1 AP** immediately.
- **Effect**: resolve **one additional** battle round immediately using section 4.
- **Limit**: at most once per Attack action (max 2 battle rounds per Attack).

### 4.1 Reinforce Battle Lines

If your Battle Line has fewer units than the cap, you may promote units from your Reserves onto your Battle Line until you reach the cap (or run out of committed units).

### 4.2 Archer Pre-Strike

If you have Archers on your Battle Line:

- All attacking Archers roll first, then all defending Archers roll (simultaneous is fine if your table prefers).
- Each Archer chooses a target enemy Battle Line unit.

### 4.3 Strike / Counterstrike (attack and defense rolls)

For each unit on your Battle Line:

1. Choose a target enemy Battle Line unit.
2. Roll your **Attack Die**.
3. The defender rolls that target's **Defense Die**.
4. If **Attack > Defense**, deal **1 damage** to the target.
5. If a unit's HP reaches 0, remove it from the Battle Line (it is destroyed).

Ties:

- If **Attack == Defense**, no damage is dealt.

### 4.4 Retreat (end of each battle round)

At the end of a battle round, in initiative order (attacker first), each side may choose to retreat:

- **Attacker retreat**: all surviving committed units remain in (or return to) their origin hexes; the attack ends.
- **Defender retreat** (standard hexes only): move the defender's Battle Line units to an adjacent hex they control (if none, defender cannot retreat).

Restriction:

- **Defenders cannot retreat from Cities/Fortresses** unless a card, spell, or motion explicitly allows it.

---

## 5. Aftermath (control and occupation)

### 5.1 If the defender is eliminated (attacker victory)

- The attacker gains control of the target hex.
- The attacker may move up to the **Battle Line Cap** surviving committed units into the hex to **occupy** it.
- Any additional surviving committed units remain in their origin hexes.

### 5.2 If the attacker retreats or is eliminated (defender holds)

- The defender retains control of the target hex.
- All surviving committed units remain in (or return to) their origin hexes.

---

## 6. Sieges (the only multi-turn combat state)

Cities and Fortresses are intended to be hard points that can create prolonged conflict.

### 6.1 When a siege happens

If the target hex contains a **Fortress**, the battle is automatically a **Siege** (the defender is assumed to **Hold the Walls**).

If the target hex contains a **City**, the defender may declare **Hold the Walls** when the attack is declared.

- If declared, the battle becomes a **Siege**.
- Place a **Siege marker** on the target hex.

### 6.2 Siege round pacing (across turns/rounds)

- A Siege does **not** fully resolve in one Attack action.
- Each time the attacker spends an **Attack** action against the sieged hex, resolve **exactly one** battle round (using section 4).
- The Siege marker remains between turns and between rounds until the siege is lifted or the defender is defeated.

### 6.3 Maintaining or lifting a siege

At the end of each siege round:

- The attacker may **lift the siege** (remove the Siege marker; all surviving units remain where they are).
- If the attacker has **no committed units adjacent** to the sieged hex, the siege automatically ends.

### 6.4 Reinforcements during a siege (bounded)

During a siege, at the start of each siege round:

- Each side may add up to **3 units total** from adjacent hexes to their committed Reserves for that siege round.

### 6.5 Siege victory

If the defender's Battle Line and Reserves are eliminated, the attacker captures the hex and occupies it per section 5.1.

---

## 7. Optional Variant: "Assault Instead of Siege"

If you want faster games, allow the attacker to declare **Assault** against a City/Fortress:

- Resolve combat immediately using the normal battle loop (section 4) until victory/retreat.
- Defenders still cannot retreat.
- Recommended: defenders gain **+1 Defense** on their Battle Line units during an Assault.

---

## 8. Example Battles (walkthrough)

These examples are written to demonstrate the intended **pacing**: one battle round per **Attack** action (optionally two with **Press the Attack**).

### 8.1 Standard Hex Battle (one round per Attack)

#### Situation (Standard Hex Battle)

- Target hex is a **standard hex** -- **Battle Line Cap = 3** per side.
- Attacker has units in two adjacent hexes:
  - Hex A: 2 Infantry, 1 Archer
  - Hex B: 1 Cavalry, 1 Infantry
- Defender controls the target hex and has:
  - Target hex: 2 Infantry
  - Adjacent Hex C: 1 Archer, 1 Infantry

#### Attack action (cost: 2 AP)

1. **Declare attack** into the target hex.
2. **Commit units**
   - Attacker commits all 5 units (from Hex A + Hex B).
   - Defender commits all 4 units (in target + Hex C).
3. **Form Battle Lines (cap 3)**
   - Attacker Battle Line: Cavalry (2 HP), Infantry, Archer
   - Attacker Reserves: 2 Infantry
   - Defender Battle Line: Infantry, Infantry, Archer
   - Defender Reserves: 1 Infantry
4. **Resolve exactly one battle round**
   - **Reinforce**: both sides already at cap.
   - **Archer Pre-Strike**:
     - Attacking Archer targets defending Infantry.
     - Defending Archer targets attacking Infantry.
     - (Rolls happen; apply damage as normal.)
   - **Attacker Strike**, then **Defender Counterstrike**:
     - Each Battle Line unit rolls attack vs its target's defense.
     - Any unit reduced to 0 HP is destroyed and removed from the line.
   - **Retreat check**: either side may retreat (defender may retreat because this is not a City/Fortress).
   - **Victory check**: if one side has no committed units remaining, the battle is decided.

#### End of the Attack action

- Even if both sides still have units committed, the battle **pauses** here.
- If the attacker wants to continue fighting this hex, they must spend another **Attack** action on a later turn.

#### Press the Attack (optional)

- Instead of ending, the attacker may pay **+1 AP** to immediately resolve **one additional** battle round right now.

### 8.2 Siege Example (City/Fortress persists)

#### Situation (Siege Example)

- Target hex is a **City** -- **Battle Line Cap = 5**.
- Attacker declares an attack against the City.
- Defender declares **Hold the Walls** -- place a **Siege marker**.

#### Attack action #1 (cost: 2 AP)

- Resolve **exactly one** siege battle round (same battle-round loop).
- If the City is not captured, the **Siege marker remains**.

#### Later, Attack action #2 (cost: 2 AP)

- Attacker spends another Attack action against the same City.
- Resolve **exactly one** siege battle round.
- The siege continues until lifted or the defender is defeated (see section 6).
