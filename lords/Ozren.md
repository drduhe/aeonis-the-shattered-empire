# Lord Sheet: Ozren, the Unveiled Flame

**Status:** Expansion roster — not yet in the First Playable rotation.

## Lord Overview

**Name:** Ozren, the Unveiled Flame
**Race:** Human
**Faction Theme:** The Ashen Creed
**Gameplay Style:** Religious schism — aggressive Influence conversion, council disruption, non-combat territorial takeover, and a martyr's engine that profits from every defeat.

## Lore

> "They veiled the flame in gold and called it holy. I tore the veil. The flame was ours all along."

Ozren was raised inside the old imperial faith and groomed for its highest offices — until, in the archives beneath a burned cathedral, he found the founding scriptures unredacted. The divine flame the priesthood claimed to mediate was never theirs to gatekeep: it burns in every farmer, every soldier, every heretic they ever put to the torch. Ozren walked out of the archive, preached what he had read in the public square, and was condemned by nightfall. The pyre they built for him would not light. Three times. By the fourth attempt, the crowd was his.

The Ashen Creed has no cathedrals, only converts — and it grows fastest where it is persecuted. Where Auriel's Radiant Accord consecrates and defends, Ozren's Creed infiltrates and flips: votes, hexes, hearts. Every soldier of his that falls becomes a sermon. Every motion of his the council strikes down becomes proof of the conspiracy he preaches against. His rivals slowly learn the awful arithmetic of fighting a martyr: each victory over Ozren makes him stronger.

## Starting Setup

### Starting Units (in Home City)

- **2 Infantry**
  - Attack: d6
  - Defense: d6
  - Health: 1
- **1 Archer**
  - Attack: d6
  - Defense: d4
  - Health: 1
  - Notes: Archers on the Battle Line have **Pre-Strike** (see `Combat.md`).

### Lord Unit (starts in Home City)

- **Ozren (Lord / Leader)**
  - Attack: d8
  - Defense: d6
  - Health: 3
  - Movement Range: 2
  - *Design note: A firebrand who fights harder than he guards. He wants to be where the crowd is — and is more dangerous martyred than most Lords are alive, so think twice before capturing him.*

### Starting Resources

**Gold:** 1
**Mana:** 1
**Influence:** 3

**Design note:** total 5 — Influence-heavy: the Creed's weapon is conviction, purchased in Influence.

### Population

**Population Cap / Pool:** 10 / 10

### Starting AP

**Starting AP:** 5

### Unique Starting Tile (replaces your Mountain)

**The First Pyre** (counts as **Mountain**)

- **Production:** +1 Gold and +1 Influence
- **Building permissions:** You may build a **Mine** here, but you may **not** build a **Tower** here.
- **Owner-only benefit (only while you control it):** Once per round, during the **High Council Phase**, when you propose a motion, the **1 Influence proposal cost is refunded** (you propose for free; see `High_Council.md` §3.2).

---

## Abilities

### 1) The Unveiled Word (Faction Mechanic — Conversion)

**Effect:** Once per round, during the **High Council Phase**, during **Voting** on a motion **you proposed** — after all players have declared their committed votes, but before votes are tallied (see `High_Council.md` §3.4) — you may spend **2 Influence** to **convert 1 vote** committed against your motion into a vote **for** it (a net swing of 2).
**Resolution order:** Resolves after Lobbying and after any COUNCIL Whispers played on vote declaration (e.g., **Backroom Deal**, see `Whispers.md`); a Whisper played in response to The Unveiled Word (e.g., **Sabotage**) resolves against it normally.
**Theme:** Somewhere in the chamber, one of your delegates has already heard the Word — they just haven't told you yet.

### 2) Ashes of the Faithful (Passive Ability — Martyrdom)

**Effect:** Two triggers, each usable **once per round**:

- When one of your units is **destroyed in a battle**, gain **+1 Influence**.
- When a motion **you proposed fails** at Voting, gain **+1 Renown**.

**Theme:** The Creed keeps a ledger of its martyrs, and the realm always pays.

### 3) Rite of Conversion (Active Ability)

**Effect:** Once per round during the **Action Phase**, on your turn, pay **1 AP** and spend **3 Influence**. Choose one hex **adjacent to a hex you control** that is either:

- **Neutral** (containing no other player's units), or
- **Enemy-controlled** but containing **no enemy units and no buildings**.

You gain control of that hex immediately. *(This is the Influence-takeover method from `Tiles.md` — "Hex Conflicts & Retaking Control" — codified as a faction action.)*
**Restrictions:** You cannot target a hex adjacent to an enemy **Fortress** (Fortresses block claims by Influence expenditure; see `Tiles.md`), and you cannot target City or Portal hexes.
**Cost:** 1 AP, 3 Influence
**Theme:** No garrison, no walls, no faith — the village converted a week ago and simply hadn't mentioned it.

---

## Faction Research (The Ashen Creed)

### Creed of Embers

**School:** DIV
**Tier:** I (1 AP to research)
**Prerequisite:** none
**Cost:** 1 Mana, 1 Influence (Research action)
**Type:** Passive
**Effect:** When **Lobbying** on a motion **you proposed** (see `High_Council.md` §2.3), your **first** lobby vote each round costs **1 Influence** instead of 2. In addition, once per round, when **another player's motion fails** at Voting, gain **+1 Influence**.
**Theme:** Every failed law is a recruiting sermon; every chamber has ears that answer to the Creed.

### Trial by Fire

**School:** DIV
**Tier:** II (2 AP to research)
**Prerequisite:** DIV 1
**Cost:** 2 Mana, 2 Influence (Research action)
**Type:** Ritual
**Effect:** Once per round, when a battle you were part of ends and you **lost the battle** (you retreated or your committed units were eliminated), you may spend **1 Mana**. If you do, gain **+2 Influence** and **+1 Renown**.
**Theme:** The Creed does not count its defeats. It counts its witnesses.

---

## Legendary Building: The Ashen Basilica

- **Prerequisite:** Gain control of 3 hexes previously controlled by other players **without initiating an Attack action** (via Rite of Conversion, council motions, or other non-combat means; cumulative across the game).
- **Build cost:** 4 AP + 4 Gold, 2 Mana, 4 Influence
- **Population:** 3
- **Upkeep:** none
- **VP:** 2 VP (checked at Cleanup & Checks)
- **Renown:** +2 immediately when constructed (standard Legendary rule, see `Buildings.md`)
- **Effect:** **PRODUCTION:** Gain +2 Influence. **COUNCIL:** Once per round, when you use **The Unveiled Word**, you may convert **1 additional** opposing vote at no extra Influence cost. Units defending this hex gain **+1 Defense**.

---

## Special Units (Future Content)

These are intended for an expanded unit roster beyond the First Playable components.

### Zealot of the Flame

- **Type:** Elite Unit
- **Stats:**
  - Attack: d8
  - Defense: d6
  - Health: 1
- **Special Ability:** When this unit is destroyed on the **Battle Line**, deal **1 damage** to the enemy Battle Line unit that destroyed it, and gain **+1 Influence** (this Influence gain stacks with Ashes of the Faithful).
- **Theme:** A Zealot's death costs the enemy twice — once in blood, once in doubt.

### Flamespeaker

- **Type:** Advanced Unit
- **Stats:**
  - Attack: d6
  - Defense: d6
  - Health: 2
- **Upkeep (suggested):** 1 Influence per round
- **Special Ability:** Once per battle, at the start of a battle round (if committed to the battle), you may spend **2 Influence**. Choose one enemy **Battle Line** unit (not a Lord). That unit does not roll its Attack Die during this battle round's Strike/Counterstrike (it still defends normally).
- **Theme:** Mid-battle, one soldier lowers their blade — they have heard the Word before, in another town, from another pyre.

---

## Faction Objectives

### Primary Objective (2 VP): "The Realm Converts"

Gain control of **3 hexes previously controlled by other players** without initiating an Attack action (via Rite of Conversion, council motions, Whisper effects, or other non-combat means; cumulative across the game).

### Secondary Objective (1 VP): "One Voice Turns the Chamber"

Use **The Unveiled Word** to convert a vote, and have that motion **pass** in the same High Council Phase.

---

## Faction Strategy

### Strengths

- **Council coercion:** The Unveiled Word makes close votes on Ozren's motions nearly unloseable — a 2-vote swing after declarations punishes anyone who opposes him by a thin margin.
- **Bloodless expansion:** Rite of Conversion annexes undefended borderland every round without a single battle, and feeds his Primary Objective while doing it.
- **Loss-proof morale:** Ashes of the Faithful and Trial by Fire mean lost units, lost battles, and failed motions all pay out. Ozren has no truly bad round — only cheap sermons and expensive ones.
- **Influence engine:** The First Pyre, Creed of Embers, and the Basilica make him the richest Influence economy in the game after Auriel — and he spends it far more aggressively than she does.

### Weaknesses

- **Garrisons stop the Creed cold:** Rite of Conversion only flips *undefended* hexes. Opponents who screen their borders with even single Infantry shut down his expansion entirely.
- **Influence bottleneck:** The Unveiled Word, Rite of Conversion, and Lobbying all drink from the same cup. Ozren is always one conversion away from being politically broke.
- **Poor and unarmored:** 1 starting Gold, no defensive bonuses, d6 Defense on the Lord. When the realm finally marches on him, the Creed's arithmetic gets grim fast.
- **Martyrdom invites farming caution, not immunity:** His per-round triggers are capped, so a patient aggressor who accepts feeding him +1 Influence per round can still dismantle him militarily.

---

## Faction Flavor Text

> "Go on — vote against me. Burn my chapels. Kill my faithful. I have built a religion out of exactly that."

## Notes for Playtesting

- **The Unveiled Word (biggest risk):** A guaranteed 2-vote swing *after* declarations may make Ozren's motions effectively unbeatable in 3-4 player games (fewer total votes). If it warps council play, move the window to *before* declarations (opponents can react) or raise the cost to 3 Influence.
- **Rite of Conversion pacing:** At 1 AP + 3 Influence per round with no combat risk, verify he can't quietly out-expand military factions — especially combined with the once-per-round +1 Renown for hex capture (see `Renown.md`). If needed, restrict it to once per two rounds or exclude hexes adjacent to any enemy building.
- **Martyrdom incentives:** Trial by Fire pays for *losing* battles. Watch for degenerate play (deliberately feeding 1 Infantry into hopeless attacks to farm Influence/Renown) — the once-per-round caps are the intended brake; confirm they hold.
- **Auriel overlap check:** Both Lords are council-centric. Confirm in mixed games that they *feel* different at the table — Auriel accumulating legitimacy on motions that pass, Ozren strong-arming outcomes and profiting when things fail. If they converge, sharpen Ozren toward hex conversion and away from vote count.
