# Aeonis: Round Structure

This chapter defines the **canonical timing** of a round in *Aeonis: The Shattered Empire*. When any other rule refers to "start of round," "during the round," or "end of round," it refers to the steps below.

---

## Overview (one-page flow)

Each round follows this order:

1. **Round Start**
2. **Event Phase**
3. **Strategy Selection Phase**
4. **High Council Phase**
5. **Action Phase (Rotating Turns)**
6. **Production & Upkeep Phase**
7. **Cleanup & Checks**

---

## 1. Round Start

- **Refresh** any "once per round" abilities and effects.
- **Return banked AP** (if banking is used) and reset each player's available AP for the round.
- **Draw Whispers**: each player draws **2 Whisper Cards** from the shared deck (see `Whispers.md`).
- **Check persistent effects** (ongoing events, curses, laws) that specify "at the start of the round."

Notes:

- "Refresh AP" and "banked AP" are defined in `Actions.md` (this phase is where those rules happen).
- Whisper draws from other sources (scoring VP, events, abilities) happen at the moment specified, not here.

---

## 2. Event Phase

Resolve any event(s) scheduled for the round. Events happen **before** Strategy Selection so they set the tone for the round and force players to adapt their strategy pick and council votes.

Default structure:

1. **Global Event**: draw and resolve one global event (if using a global event deck).
2. **Localized / persistent events**: advance ongoing events and apply their effects.
3. **Milestone checks**: if a milestone triggers an event, resolve it now (see `Events.md`).

Notes:

- Exploration Events are **not** resolved here; they trigger immediately when a player enters an unexplored hex during the Action Phase (see `Events.md`).
- WHEN-triggered Whispers related to events may be played here.

---

## 3. Strategy Selection Phase

1. **Reveal available Strategy Cards** for this round (remove cards for player count if needed).
2. **Players choose Strategy Cards** in **ascending VP order** (lowest VP picks first):
   - **Ties:** broken by lowest Renown, then clockwise from the Speaker.
   - See `Strategy.md` for full draft rules.
3. **Set initiative order** by Strategy Card numbers (lowest number acts first during the Action Phase).

Timing rules:

- A Strategy Card's **primary ability** may be activated **only during the Action Phase** (on your turn), unless the card explicitly says otherwise.
- A Strategy Card's **secondary ability** may be triggered **only when its condition occurs**, and only within the window defined on that card.

---

## 4. High Council Phase

This is the political phase where players propose and vote on motions, laws, and titles.

Default structure (see `High_Council.md` for full procedure):

1. **Council Agenda Opens**
2. **Proposal Window**: each player may propose up to **one** motion (in initiative order, or clockwise). COUNCIL Whispers that affect proposals may be played here.
3. **Negotiation Window**: table talk and trades are allowed (subject to trade rules).
4. **Voting**: resolve motions one at a time in the order proposed. COUNCIL Whispers that affect voting may be played here.
5. **Enactment**: apply passed laws, borders, titles, and immediate effects.

Timing rules:

- Any rule that says "by High Council decree" resolves **here**, before the Action Phase begins.
- Motions that change borders, movement permissions, or demilitarized zones take effect **immediately** when passed (unless the motion says "next round").

---

## 5. Action Phase (Rotating Turns)

Players take turns in **initiative order** (from Strategy Cards). On your turn you do **exactly one** action, paying its AP cost, then play passes to the next player.

The Action Phase continues until **all players have passed** or **cannot take actions** (no AP remaining, or no legal actions).

### 5.1 What you can do on your turn

On your turn, choose one action (see `Actions.md` for costs and details):

- **Move** (see `Movement.md`)
- **Attack / Initiate Battle** (see `Combat.md`)
- **Build** (see `Buildings.md`)
- **Recruit** (see `Actions.md`, Recruit section)
- **Research / Arcane Discovery** (see `Arcane.md`)
- **Trade** (see `Trade_Taxes.md`)
- **Activate your Strategy Card primary**
- **Play an ACTION Whisper** (see `Whispers.md`; does not cost AP)
- **Pass**

### 5.2 Combat timing

- Battles are initiated as part of an **Attack** action.
- Each **Attack** action resolves **one battle round** (optionally two if the attacker "Presses the Attack"), and then the action ends.
- **COMBAT Whispers** may be played during the battle round at the step specified on the card (see `Whispers.md`).
- **Sieges** (Cities/Fortresses) can persist across turns/rounds and are continued by spending additional **Attack** actions (see `Combat.md`).

### 5.3 Exploration timing

- If entering an unexplored hex triggers an Exploration Event, resolve it **immediately upon entry** (see `Events.md`).

### 5.4 WHEN-triggered Whispers

- Throughout the Action Phase, players may play WHEN-triggered Whispers at the moment their condition is met (see `Whispers.md`). These do not consume your turn.

### 5.5 Passing

- When you **Pass**, you take no further turns this round.
- If AP banking is enabled, record any banked AP during this step (see `Actions.md`).

---

## 6. Production & Upkeep Phase

All players resolve this phase (typically in initiative order, but it may be simultaneous if your group prefers).

1. **Production**:
   - Gain resources from controlled tiles and buildings (see `Tiles.md` and `Buildings.md`).
2. **Population growth**:
   - Replenish population up to cap (see `Population.md`).
3. **Upkeep / maintenance**:
   - Pay any required upkeep costs for units/buildings (see `Trade_Taxes.md` and/or `Population.md` depending on which constraint model is used).
4. **Resolve "end of round" resource effects**:
   - Any laws, artifacts, or discoveries that say "each round" resolve here unless they specify a different window.

---

## 7. Cleanup & Checks

1. **Discard / refresh** round-limited cards and effects.
2. **Return tokens / reset** "once per round" markers.
3. **Release captured Lords**: all captured Lords return to their owner's Home City at full HP (see `Combat.md`).
4. **Whisper hand limit**: players with more than **7 Whisper Cards** must discard down to 7 (their choice).
5. **Victory checks**:
   - If a player reached the VP threshold **during the round**, the game ends **at the end of this phase** (end of the round), unless a scenario/variant says otherwise (see `Victory.md`).
6. **Advance the round marker** and pass the Speaker marker clockwise.

---

## Rules Priority

If a card, motion, or Lord ability contradicts this chapter, apply the following priority:

1. **Whisper Card / Strategy Card / motion / Lord ability text**
2. **System chapter text** (e.g., `Combat.md`, `Movement.md`)
3. **This Round Structure chapter**
