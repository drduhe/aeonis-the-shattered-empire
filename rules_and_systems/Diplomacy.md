# Aeonis: Diplomacy

Aeonis is a negotiation game: promises, threats, and bargains are constant. This chapter defines exactly **which agreements the rules enforce** and which are left to honor. It also defines the one formal diplomatic instrument, the **Accord**.

Trade mechanics (the AP-costed Trade action, what may be exchanged) are owned by `Trade_Taxes.md`. The High Council (motions, treaties by decree) is owned by `High_Council.md`.

---

## 1. Deals (canon)

A **deal** is any agreement between two or more players.

### 1.1 Binding vs non-binding

- **Immediate exchanges are binding.** If components change hands as part of a deal (resources, artifacts per `Artifacts.md` trade rules, hex transfers via the Trade action), the exchange must be completed as agreed, at the moment of the deal.
- **Promises about the future are non-binding.** "I'll vote for your motion," "I won't attack you next round," "I'll give you 2 Gold at Production" — none of these are enforced by the rules. Breaking them has social consequences, not mechanical ones (but see Accords, §2).

**Cassian — Consortium's Ledger exception:** Once per round during the High Council Phase, when a deal Cassian proposed is accepted, he may make one included promise about the **current motion's vote** binding. The promised player must vote as agreed when that motion resolves. The exception cannot bind a later round, movement, combat, production, or a future resource transfer. During the Action Phase, Cassian may also initiate one Trade per round at 0 AP before or after any player's action; resolve it before play continues. See `../lords/Cassian.md`.

### 1.2 When you can deal

- **Negotiation is always allowed** — any phase, any turn. Talk is free.
- **Component exchanges** require a legal window: a **Trade** action during the Action Phase (see `Trade_Taxes.md`), or an explicit rule that allows an exchange (e.g., a motion, an artifact, the High Council Negotiation Window if your table uses instant council deals — see `High_Council.md` §3.3).
- Deals may not exchange things the rules give no way to transfer (VP, Renown, Whisper Cards in hand, objectives, control of Legendary Buildings).

### 1.3 Table rules

- Deals must be made **openly enough to resolve**: the parts of a deal that move components must be stated to the table when they resolve. Side conversations are allowed (and encouraged), but hidden component transfers are not.

---

## 2. Accords (formal alliances)

An **Accord** is the game's one enforced alliance instrument. It is deliberately lightweight: it makes cooperation visible, gives it a small reward, and makes betrayal cost something.

### 2.1 Forming an Accord

- **Timing:** during the High Council Phase (Negotiation Window) or as part of a Trade action.
- **Procedure:** two players publicly declare the Accord and each takes a matching **Accord token**.
- Each player may be in at most **2 Accords** at once.

### 2.2 Effects while an Accord stands

- **Open borders:** Accord partners may move through each other's controlled hexes without the enemy-controlled-hex restriction (ZOC surcharges from *units* still apply; see `Movement.md`).
- **Renown:** each partner gains **+1 Renown** while the Accord stands (temporary; see `Renown.md`). Lose it when the Accord ends for any reason.
- **Portals:** partners count each other's Portals as "controlled by you" for Portal-travel permission (see `Movement.md`).
- Accords do **not** pool votes, share production, or restrict either partner's council behavior.

### 2.3 Ending an Accord

- **Amicable dissolution:** both partners agree, at any time. Each simply loses the Accord's benefits (including the +1 Renown).
- **Betrayal:** if a player **declares an Attack** against their Accord partner's units or hexes, the Accord breaks immediately. The attacker loses the Accord Renown **and 1 additional Renown** (see `Renown.md`, decay). The defender keeps no penalty.
- An Accord also breaks automatically if a motion or effect says so.

### 2.4 Design intent

Accords are not team play. They are a tempo tool (borders, portals) with a public trust signal (tokens on the table). The betrayal cost is real but small — treachery at the right moment should still be worth it.

---

## 3. Ceasefires and treaties

- There is **no separate ceasefire mechanic**. Non-aggression promises are non-binding deals (§1.1).
- Tables that want enforceable peace should use the council: **Demilitarized Zone** and **Open Borders Treaty** motions (see `High_Council.md` §6) are the enforced instruments, because the whole table voted for them.

---

## 4. NPC and neutral factions (decision)

**Out of the core game.** Neutral armies, mercenary factions, and roaming threats are reserved for a future expansion module. Core-game events that create shared threats do so through hex states (storms, blights, uprisings — see `Events.md`), not neutral units. This keeps the diplomacy space purely player-vs-player.

---

## 5. Components

- **Accord tokens:** 8 matched pairs (see `../components/Components.md`).

## 6. Playtest watch-items

- Do Accords form and break, or do they calcify into permanent teams? (If calcified: consider limiting Accords to 3-round terms.)
- Is the betrayal penalty (−1 Renown beyond losing the bonus) enough to make Accords trusted but not sacred?
- Does the 2-Accord cap matter at 7-8 players?
