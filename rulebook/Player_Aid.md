# Aeonis: Player Aid (First Playable)

> **Draft for First Playable — matches the rules chapters as of this writing. The chapter docs remain authoritative.**

---

## Round Sequence (7 phases)

1. **Round Start** — refresh abilities, reset AP (+ banked AP), draw **2 Whispers**, Lords heal to full.
2. **Event Phase** — draw and resolve one Global Event.
3. **Strategy Selection** — draft in ascending VP order (2 cards each at 3–4 players, 1 at 5–8); 1 Gold bounty on undrafted cards; lowest card number = initiative.
4. **High Council Phase** — proposals (1 Influence each), agenda card reveal (free proposal), negotiation, voting, enactment.
5. **Action Phase** — rotating turns in initiative order; one action per turn until all players pass.
6. **Production & Upkeep** — collect from controlled hexes/buildings, grow Population, pay advanced-unit/Law upkeep (buildings have none), gain 1 Remnant per controlled Ruins.
7. **Cleanup & Checks** — release captured Lords, discard Whispers to 7, score objectives and VP checks, check 10 VP threshold, pass Speaker clockwise.

---

## Action Costs

| Action | AP | Notes |
| --- | --- | --- |
| Move | Path cost | Terrain cost per hex; +1 per enemy ZOC hex (Cavalry: first ZOC hex free); one group per Move |
| Attack | 2 | One battle round; **+1 AP** to Press the Attack (one extra round, max once per Attack) |
| Build | 3 | Plus building's resource cost; **Legendary Building: 4 AP** |
| Recruit | 1 | Up to 2 units in one controlled City; once per City per round |
| Research | 1 | Tier I only in First Playable; plus resource cost (default 2 Mana); grants 1 Remnant |
| Trade | 1 | Initiate once per round; Market allows one at 0 AP |
| Strategy Card primary | Varies | Printed on card; once per round; others may then buy the secondary (no turn used) |
| Play ACTION Whisper | 0 | Uses your turn |
| Claim Artifact | 1 | Requires your unit on the Artifact Site hex |
| Pass | — | Out for the round; bank up to **2 AP** |

**Free action (0 AP, doesn't use your turn):** purge 3 Remnants on your turn to draw 1 Artifact Card.

---

## Unit Stats

| Unit | Attack | Defense | HP | Move | Notes |
| --- | --- | --- | --- | --- | --- |
| Infantry | d6 | d6 | 1 | 1 | 1 Gold, 1 Population |
| Cavalry | d8 | d6 | 2 | 2 | 2 Gold, 2 Population; ignores first ZOC hex per Move (flanking) |
| Archer | d6 | d4 | 1 | 1 | 1 Gold + 1 Mana, 1 Population; Pre-Strike on the Battle Line |

**Lords** (occupy 0 Population; captured at 0 HP: captor gains +1 VP, +2 Renown; released at Cleanup):

| Lord | Race | Attack | Defense | HP | Move | Identity |
| --- | --- | --- | --- | --- | --- | --- |
| Cassian | Human | d6 | d8 | 3 | 2 | Diplomat |
| Seraphel | Human | d10 | d6 | 3 | 2 | Glass cannon |
| Vharok | Human | d8 | d10 | 4 | 1 | Slow tank |
| Elyndra | Elven | d6 | d8 | 4 | 2 | Resilient guardian |
| Rakhis | Djinnborn | d8 | d6 | 3 | 3 | Fast raider |
| Nyxara | Umbral | d10 | d4 | 2 | 2 | Assassin |
| Auriel | Luminari | d6 | d10 | 3 | 2 | Faith tank |
| Thal'rik | Voidborn | d8 | d8 | 3 | 2 | Portal master |

### Launch-Lord signatures

| Lord | Signature reminder |
| --- | --- |
| Cassian | One off-turn 0-AP Trade; one binding current-motion vote promise per round |
| Seraphel | +1 virtual sigil in every school; second paid Research in the same turn once per round |
| Vharok | Built hexes may Hold the Walls; +1 defending Battle Line slot there |
| Elyndra | One 1-AP group Move between any two controlled Forests per round |
| Rakhis | Deserts cost 1; one pre-Pre-Strike retreat per battle (normal ZOC) |
| Nyxara | Draw 3 Whispers at Round Start; hand limit 8 |
| Auriel | Sanctify one motion per round: own votes ×2; +2 Renown if supported and passed |
| Thal'rik | Portal travel to any Portal without permission |

---

## Terrain

| Terrain | Move cost | Production | Notes |
| --- | --- | --- | --- |
| Plains | 1 AP | +1 Population | Farm upgrades to +2 |
| Forest | 1 AP | +1 Mana | Grove upgrades to +3; defensive bonus for units ending movement here |
| Mountain | 2 AP | +1 Gold | Mine upgrades to +3 |
| Desert | 2 AP | +1 Influence | Embassy upgrades to +3; units lose 1 Population if they spend more than 2 turns here |
| Lake | Impassable | — | Bridge makes it passable (1 AP, no production) |
| City | 1 AP | +2 Population + various | Recruitment hub; +1 AP/round to controller (max +2 from Cities) |
| Ruins | — | Varies | Controller gains 1 Remnant per round |
| Portal | 1 AP enter/exit | None | Portal-to-Portal travel 0 AP (destination must be neutral or yours) |

---

## Buildings

3 AP to Build (Legendary: 4 AP), plus the costs below. "Pop" = Population occupied while the building exists.

| Building | Where | Cost | Pop | Effect |
| --- | --- | --- | --- | --- |
| Farm | Plains | 2 Gold | 1 | Plains produces +2 Population; +2 Population Cap |
| Mine | Mountains | 3 Gold | 1 | Mountain produces +3 Gold |
| Grove | Forests | 2 Mana | 1 | Forest produces +3 Mana |
| Embassy | Deserts | 3 Influence | 1 | Desert produces +3 Influence |
| Tower | Any tile | 4 Gold | 1 | +1 Defense in hex; influence 2 hexes out; controls a Portal if built on one |
| Fortress | Any tile | 5 Gold, 2 Mana | 2 | +2 Defense in hex; attacks on it are always Sieges |
| Bridge | Lake | 4 Gold | 0 | Lake becomes passable/controllable; needs adjacent controlled non-Lake hex |
| Guild Hall | City | 4 Gold, 2 Influence | 1 | +1 AP per round |
| Forge | City | 6 Gold, 1 Mana | 1 | +1 unit per Recruit here (once/round); units here cost −1 Gold (min 1) |
| Academy | City | 4 Gold, 4 Mana | 2 | School Specialty of choice; −1 Mana on one Research per round (min 0) |
| Bank | City | 5 Gold | 1 | Once per round at Production: convert 2 Mana→3 Gold, 2 Gold→3 Mana, or 2 Gold→3 Influence |
| Castle | City | 8 Gold | 2 | +3 Population Cap; +2 Defense in this City |
| Market | City | 2 Gold, 2 Influence | 1 | Once per round: initiate one Trade at 0 AP |
| Legendary | Your City | Per Lord sheet | 3 | Unique per Lord; prerequisite; **2 VP once on build** (+ **1 VP once** to City captor); +2 Renown on build |

Slots: 1 building per basic terrain tile; 2 per City (3 with research).

---

## Combat Sequence (one battle round per Attack action)

Battle Line Cap: **3** (standard hex) / **5** (City or Fortress). Committed units beyond the cap are Reserves.

1. **Reinforce Battle Lines** — promote Reserves up to the cap.
2. **Archer Pre-Strike** — attacking Archers roll first, then defending Archers; each targets an enemy line unit.
3. **Attacker Strike** — each line unit picks a target: Attack die vs. Defense die; Attack > Defense = 1 damage (ties: nothing).
4. **Defender Counterstrike** — same, for surviving defenders.
5. **Retreat Check** — attacker decides first. Defender may retreat from standard hexes only (to an adjacent controlled hex) — never from Cities/Fortresses.
6. **Victory Check** — a side with no committed units left loses; otherwise the battle pauses.

**Press the Attack:** +1 AP after step 6 for one extra battle round (max once per Attack action).
**Aftermath:** attacker victory = immediate control; occupy with up to the cap. **Sieges** (Fortress always; City if defender Holds the Walls) persist across rounds; each side may add up to 3 units per siege round.

---

## High Council

**Sequence:** agenda opens → proposals (1 Influence, max 1 per player) → Speaker reveals 1 agenda card (anyone may propose it free) → negotiation → vote motions in order proposed → enact.

**Deals:** talk is always allowed. Immediate exchanges resolve only in a legal Trade window and are binding. Future vote, payment, attack, and non-aggression promises are non-binding. Population is never tradeable. Formal Accords are off in First Playable.

**Vote math:**

- Base: **1 vote** per player
- **+1 vote** at 5+ Renown; **+1 more** at 10+ Renown
- Lobbying: **2 Influence = +1 vote** (this motion only; minimum spend 2; declared in initiative order)
- Passes on **strict majority of votes cast — ties fail**
- Passing your own motion: **+1 Renown**

---

## VP Sources

| Source | VP |
| --- | --- |
| Public objective (each) | 2 |
| Secret objective (each) | 2 |
| Coronation Rite (control Seat + Lord present) | +1 per Cleanup; third total Rite +2 once |
| Capture an enemy Lord | +1 (plus +2 Renown) |
| Construct your Legendary Building | 2 once; a later City captor scores 1 once |
| Gain a VP artifact (Crown of Aeonis, Eternal Forge, Shard of the Throne, Imperial Seal) | 1 once; max 2 scorers per artifact |
| Title first claimed (Hero of the Realm, Magister of Mana) | 2 |
| Imperial Mandate primary while controlling the Imperial Seat | 1 |

**10 VP triggers the final round** (8 VP short variant). Highest VP at end of that round wins; ties: most Renown, then most Influence. Scoring VP from any source: **draw 1 Whisper Card**.

---

## Whisper Timing Windows

| Timing | When you can play it | Uses your turn? |
| --- | --- | --- |
| ACTION | On your turn in the Action Phase, instead of your action (0 AP) | Yes |
| COMBAT | During the named step of a battle you are in | No |
| COUNCIL | At the named moment of the High Council Phase | No |
| WHEN [X] | Immediately after the described trigger occurs | No |

Max **1 Whisper per timing window per occurrence**. Sabotage cancels a Whisper as it is played and cannot be Sabotaged.

---

## Key Limits

- **Whisper hand limit:** 7 (discard down at Cleanup & Checks)
- **Battle Line Cap:** 3 standard hex / 5 City or Fortress
- **Recruit:** once per City per round; up to 2 units per Recruit action
- **AP banking:** max 2 AP carried over when you pass
- **Secret objectives:** max 3 unscored in hand
- **Public objectives:** shared row; score at most 1 per Cleanup, each card once per player. Cumulative progress begins when the card is revealed.
- **Lord Equipment artifacts:** max 2 per Lord
- **City AP bonus:** max +2 from Cities
- **Trade:** initiate once per round
- **Council proposals:** 1 motion per player per round (agenda card is extra)
- **Strategy Card primary:** once per round; each secondary once per player per round
- **Population:** starting Cap 10; global maximum 25 (default)
- **Building slots:** 1 per basic tile; 2 per City (3 with research)
