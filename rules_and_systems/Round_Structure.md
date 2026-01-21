# Aeonis: Round Structure

This chapter defines the **canonical timing** of a round in *Aeonis: The Shattered Empire*. When any other rule refers to “start of round,” “during the round,” or “end of round,” it refers to the steps below.

---

## Overview (one-page flow)

Each round follows this order:

1. **Round Start**
2. **Strategy Selection Phase**
3. **High Council Phase**
4. **Action Phase (Rotating Turns)**
5. **Production & Upkeep Phase**
6. **Event Phase**
7. **Cleanup & Checks**

---

## 1. Round Start

- **Refresh** any “once per round” abilities and effects.
- **Return banked AP** (if banking is used) and reset each player’s available AP for the round.
- **Check persistent effects** (ongoing events, curses, laws) that specify “at the start of the round.”

Notes:

- “Refresh AP” and “banked AP” are defined in `Actions.md` (this phase is where those rules happen).

---

## 2. Strategy Selection Phase

1. **Reveal available Strategy Cards** for this round.
2. **Players choose Strategy Cards** (draft method to be specified by the rules variant):
   - Option A: lowest Renown chooses first
   - Option B: reverse VP chooses first
   - Option C: clockwise from the Speaker / First Player marker
3. **Set initiative order** by Strategy Card numbers (lowest acts first during the Action Phase).

Timing rules:

- A Strategy Card’s **primary ability** may be activated **only during the Action Phase** (on your turn), unless the card explicitly says otherwise.
- A Strategy Card’s **secondary ability** may be triggered **only when its condition occurs**, and only within the window defined on that card.

---

## 3. High Council Phase

This is the political phase where players propose and vote on motions, laws, and titles.

Default structure (until the full procedure is defined in `High_Council.md`):

1. **Council Agenda Opens**
2. **Proposal Window**: each player may propose up to **one** motion (in initiative order, or clockwise).
3. **Negotiation Window**: table talk and trades are allowed (subject to trade rules).
4. **Voting**: resolve motions one at a time in the order proposed.
5. **Enactment**: apply passed laws, borders, titles, and immediate effects.

Timing rules:

- Any rule that says “by High Council decree” resolves **here**, before the Action Phase begins.
- Motions that change borders, movement permissions, or demilitarized zones take effect **immediately** when passed (unless the motion says “next round”).

---

## 4. Action Phase (Rotating Turns)

Players take turns in **initiative order** (from Strategy Cards). On your turn you do **exactly one** action, paying its AP cost, then play passes to the next player.

The Action Phase continues until **all players have passed** or **cannot take actions** (no AP remaining, or no legal actions).

### 4.1 What you can do on your turn

On your turn, choose one action (examples; see system chapters for details):

- **Move** (see `Movement.md`)
- **Attack / Initiate Battle** (see `Combat.md`)
- **Build** (see `Buildings.md`)
- **Recruit** (unit rules TBD / referenced in `Combat.md` and `Population.md`)
- **Research / Arcane Discovery** (see `Arcane.md`)
- **Trade** (see `Trade_Taxes.md`)
- **Activate your Strategy Card primary**
- **Pass**

### 4.2 Combat timing

- Battles are initiated as part of an **Attack** action.
- Each **Attack** action resolves **one battle round** (optionally two if the attacker “Presses the Attack”), and then the action ends.
- **Sieges** (Cities/Fortresses) can persist across turns/rounds and are continued by spending additional **Attack** actions (see `Combat.md`).

### 4.3 Exploration timing

- If entering an unexplored hex triggers an Exploration Event, resolve it **immediately upon entry** (see `Events.md`).

### 4.4 Passing

- When you **Pass**, you take no further turns this round.
- If AP banking is enabled, record any banked AP during this step (see `Actions.md`).

---

## 5. Production & Upkeep Phase

All players resolve this phase (typically in initiative order, but it may be simultaneous if your group prefers).

1. **Production**:
   - Gain resources from controlled tiles and buildings (see `Tiles.md` and `Buildings.md`).
2. **Population growth**:
   - Replenish population up to cap (see `Population.md`).
3. **Upkeep / maintenance**:
   - Pay any required upkeep costs for units/buildings (see `Trade_Taxes.md` and/or `Population.md` depending on which constraint model is used).
4. **Resolve “end of round” resource effects**:
   - Any laws, artifacts, or discoveries that say “each round” resolve here unless they specify a different window.

---

## 6. Event Phase

Resolve any event(s) scheduled for the round.

Default structure:

1. **Global Event**: draw and resolve one global event (if using a global event deck).
2. **Localized / persistent events**: advance ongoing events and apply their effects.
3. **Milestone checks**: if a milestone triggers an event, resolve it now (see `Events.md`).

Note:

- If you prefer the TI4 feel of “event first,” you can move this phase to **Round Start**. If you do, keep it consistent and update all event references accordingly.

---

## 7. Cleanup & Checks

1. **Discard / refresh** round-limited cards and effects.
2. **Return tokens / reset** “once per round” markers.
3. **Victory checks**:
   - If a player reached the VP threshold **during the round**, the game ends **at the end of this phase** (end of the round), unless a scenario/variant says otherwise (see `Victory.md`).
4. **Advance the round marker** and pass any first-player / speaker marker (if used).

---

## Rules Priority

If a card, motion, or Lord ability contradicts this chapter, apply the following priority:

1. **Card / motion / Lord ability text**
2. **System chapter text** (e.g., `Combat.md`, `Movement.md`)
3. **This Round Structure chapter**
