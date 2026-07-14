# Aeonis: Victory Points

Players earn **Victory Points (VP)** throughout the game by achieving key objectives, controlling powerful assets, and making strategic decisions. The first player to reach a certain VP threshold triggers the endgame, with the winner determined by the highest VP total at the conclusion of the round.

**Victory Threshold:** First to **10 VP** triggers the final round. Highest VP at end of that round wins.

**First Playable pacing:** Design and balance for **6–8 rounds** to game end at the 10 VP threshold (accepted 2026-07-12; see `INDEX.md`). Short-game variant: **8 VP** (see First Playable packet).

**Tiebreaker:** Most Renown, then most Influence.

**VP permanence:** Once scored, VP are never removed, even if the source (hex, artifact, building, title) is later lost.

**Objective scoring timing:** Public and secret objectives score at **Cleanup & Checks** when the condition is met. Each card scores **once per player per game**. A player may score at most 1 public objective per Cleanup. Cumulative public progress begins only after that card is revealed. No separate claim action.

---

## Key Sources

### 1. Variable Objective Cards (Core Feature)

**First Playable (shared row):** Reveal public objectives in a shared row; every player may score each revealed public objective once. See `playtest/First_Playable_Packet.md` §4.4.

**Full game (default):** At setup, reveal **2 Stage I** public objectives in the shared row. Reveal 1 more at each Round Start from Round 2; Stage II joins the remaining Stage I deck at Round Start of Round 4. Each revealed public objective can be scored by **every player, once each**, at Cleanup & Checks (limit: 1 public objective scored per player per round).

- **Public Objective:** Revealed to all players. Completing it earns **2 VP**.
- **Secret Objective:** Hidden from other players. Completing it earns **2 VP**.

- **Examples of Objectives:**
  - **Military Feats:** Maintain a standing army, win battles after a card is revealed, or hold against attacks.
  - **Economic Goals:** Stockpile 10 Gold, build 3 Farms, or control 3 resource-rich hexes.
  - **Cultural Influence:** Construct a Legendary Building or complete a Renown-based milestone.

*Replayability:* Objectives vary by game, encouraging diverse strategies.

---

### 2. Lord-Specific Objectives

- Each Lord has **unique thematic objectives** tied to their lore and abilities. VP values are defined on each Lord Sheet (typically 1-2 VP per objective).
- **Examples:**
  - **Seraphel:** "Ritual Ascendance" -- end a round with 10 Mana and control at least 2 Forest/Grove hexes.
  - **Vharok:** "Unbroken Line" -- control a Fortress hex and win a battle as defender.

*Why It Works:* Encourages players to lean into their Lord's identity and playstyle.

---

### 3. High Council Titles

- Players earn VP and bonuses by claiming **Titles** through High Council motions.
- **Examples of Titles:**
  - **Hero of the Realm:** Reach 5 Renown. **(2 VP + 1 Influence during Production & Upkeep each round while held)**
  - **Magister of Mana:** Control 3 Mana-producing hexes or Groves. **(2 VP)**

*Why It Works:* Makes the High Council a critical arena for indirect competition.

---

### 4. Artifacts and Legendary Buildings

**VP are permanent.** Once scored, VP are never removed, even if the source (hex, artifact, building, title) is later lost.

- **Artifact VP:** Only specific named artifacts award VP. Score **1 VP once** when you first gain control of that artifact. Stealing or capturing it scores the new holder **1 VP once**. Cap: a given artifact awards VP to at most **2 players** per game. VP-bearing artifacts:
  - **Crown of Aeonis** (Lord Equipment) — transfers when your Lord is captured.
  - **Eternal Forge** (Building Relic) — stays on the hex; new controller may score if under the 2-player cap.
  - **Shard of the Throne** (Utility) — transfers to the combat winner when you lose a battle where your Lord was present. May also be freely traded.
  - **Imperial Seal** (Utility) — may be purged to prevent a Law or Decree from being repealed.
- **Legendary Buildings:** Each Lord has one unique Legendary Building (faction capstone). Score **2 VP once on construction**. If the City containing a Legendary Building is captured, the captor scores **1 VP once** (per building, per capturer, per game) and gains control of the building's effects. Constructing a Legendary Building also grants **+2 Renown** immediately. See `Buildings.md`.
- See `Artifacts.md` for the full artifact system.

*Why It Works:* Score-once awards keep conflict over artifacts and Legendaries without Cleanup drip bookkeeping or VP transfer refunds.

---

### 5. Imperial Seat (Endgame Objective)

**Coronation Rite (First Playable):** At Cleanup & Checks, if you control the Imperial Seat **and** your Lord unit is in the Seat hex, score **1 VP** (max once per round). On your **third** total Rite (not necessarily consecutive), score an additional **+2 VP** (**once per player per game**). Missing rounds between Rites does not reset your Rite count or allow a second +2 VP award.

*Why It Works:* Creates a visible, attackable scoring moment at the thematic centerpiece instead of silent drip VP.

---

### 6. Combat and Capture

- **Defeating a Lord (canon):** When an enemy Lord unit is reduced to 0 HP, it is **captured** and you immediately gain **+1 VP** (see `Combat.md`, section 2.1.4).
- **Captured Lord penalty:** The captured Lord's abilities are **disabled** until release (see `Combat.md`). The captured player may still take turns, score VP, and play normally in all other respects.
- **Release timing:** Captured Lords are released at **Cleanup & Checks** and return to their owner's Home City at full HP.

*Why It Works:* Rewards aggression without creating a feel-bad spiral where the losing player is locked out of scoring.

---

### 7. Event-Driven Points

- Specific game events provide dynamic opportunities to earn VP, adding unpredictability:
  - **Example:** A Dragon's Hoard event offers VP to the first player who defeats the dragon.
  - **Example:** A Council Crisis event grants VP to the Lord who resolves it.

*Why It Works:* Keeps gameplay fresh and introduces situational opportunities.

---

### 8. Turn-Limited Victory (Optional Variant)

- The game can be played with a fixed turn limit (e.g., **10 rounds**) to add predictability. At the end, VP are tallied to determine the winner.
- **Short Game Variant:** Use a VP threshold of **8 VP** instead of 10 for faster games or learning sessions.

*Why It Works:* Provides a structured option for pacing.

---

## Innovative Mechanics to Enhance Victory Points

### 1. Purchased Points — removed

Players may **not** spend Influence or Gold to buy VP as a general action. Council motions and events may still award VP as printed effects (politics and drama, not a purchase market).

### 2. Secret Endgame Scoring

- At the game's conclusion, certain hidden scoring opportunities are revealed:
  - **Example:** Gain **2 VP** if you controlled the most hexes during the final round.
  - **Example:** Gain **2 VP** if you own the most Arcane Discoveries at game end.

---

## Summary of Victory Point System

1. **Variable Objective Cards (Public 2 VP, Secret 2 VP):** Core feature that drives diverse gameplay.
2. **Lord-Specific Objectives:** Ties into theme and lore.
3. **High Council Titles:** Rewards political play and council engagement.
4. **Artifacts and Legendary Buildings:** VP-bearing artifacts drive conflict; others provide power (see `Artifacts.md`).
5. **Imperial Seat:** Provides a dynamic endgame conflict point.
6. **Combat and Capture:** Rewards aggression with measured risk (+1 VP, ability lockout).
7. **Event-Driven Points:** Adds situational, thematic scoring moments.
8. **Turn-Limited Victory (Optional):** Ensures structured gameplay.

**Victory Threshold:** First to **10 VP** triggers the final round, with the winner crowned at the end.
