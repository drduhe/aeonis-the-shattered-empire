# Plan 2: AP Economy Flattening & Catch-Up

- **Status:** PROPOSED — nothing here is canon until playtested and locked in `rules_and_systems/INDEX.md`. `Actions.md` remains authoritative.
- **Date:** 2026-07-02
- **Owning doc:** `rules_and_systems/Actions.md`
- **Related plans:** Plan 1 (combat — Attack cost held constant there), Plan 6 (bookkeeping — Renown threshold cleanup overlaps)

---

## 1. Problem

Action Points are the game's tempo currency, and right now tempo compounds toward the leader.

**Current AP income (all sources):**

| Source | Bonus |
|---|---|
| Base (Lord sheet default) | 5 AP |
| Controlled Cities | +1 each, max +2 |
| 5 Renown threshold | +1 permanently |
| 10 Renown threshold | 1 free 1-AP action per round |
| Guild Hall building | +1 per round |
| Banking (pass early) | up to +2 carried forward |

A developed leader plays with an effective **9–10 AP** against a trailing player's **5** — nearly double the actions per round in a genre where action advantage compounds (more actions → more hexes → more production → more actions). The Renown thresholds double-dip: the same milestones also grant **+1/+2 Council votes** (`High_Council.md` §2.2), so the military/economic leader also outvotes the table.

The only current catch-up lever is lowest-VP-picks-first in the Strategy draft.

**Secondary problem — untested cost ratios:** Build (3 AP) consumes 60% of a base round for one building while Recruit is 1 AP for 2 units. If building feels miserable, development strategies die and the game flattens into recruit-and-fight.

## 2. Goals / Non-goals

**Goals**

1. AP spread between the best- and worst-positioned player is **≤ 2** at any point in the game.
2. Growth still *feels* rewarding — expanding must buy something visible (resources, options), just not unbounded tempo.
3. A bounded, non-humiliating catch-up valve exists.
4. Action costs are proportional to how fun the action is to take.

**Non-goals**

- Not removing AP as a system (no move to TI4-style command tokens — that's a different game).
- Not touching Whisper "0 AP" actions or Strategy Card primary costs (owned by `Strategy.md`).
- Not deciding combat costs (Plan 1 holds Attack at 2 AP deliberately).

## 3. Options considered

| Option | Verdict |
|---|---|
| A. Flat 6 AP for everyone, no growth | Rejected — kills the growth fantasy entirely |
| B. **Unified bonus cap:** total AP bonuses from all sources capped at +2 | **Adopt** |
| C. **Rally valve:** the player last in VP gains +1 AP at Round Start | **Adopt** |
| D. Convert excess City AP into resources | **Adopt** (folds into B) |
| E. Progressive costs (leader's actions cost more) | Rejected — punishes success invisibly, terrible to teach |
| F. Remove banking | Rejected for now — banking rewards passing early, which is good for round pacing; revisit only if data shows abuse |

## 4. Recommended design (spec)

### 4.1 Unified AP cap (rule text direction)

> **AP bonuses (all sources) are capped at +2 total.** Your per-round AP is your Lord sheet base (default 5) plus at most +2 from any combination of Cities, Renown, buildings, laws, and artifacts. Effects that grant *free actions* (rather than AP) count against this cap as 1 each.

Consequences to propagate:

- **Cities:** first City bonus still +1 AP; further Cities instead produce **+1 Gold each** during Production & Upkeep (growth converts to economy, not tempo).
- **Renown 5:** keep +1 AP (counts against cap). **Renown 10:** replace the free 1-AP action with **+1 VP once** or a Whisper draw per round — decide in playtest; the free action almost always breaches the cap anyway.
- **Guild Hall:** effect becomes "+1 AP per round (counts against your +2 AP cap). If you are already at the cap: +2 Gold per round instead." Overflow-into-resources keeps the building purchasable late.
- **Renown council votes are out of scope here** but flagged to Plan 6's Renown cleanup — the double-dip (tempo + votes from the same track) is part of the same leader-compounding problem.

### 4.2 The Rally valve (rule text direction)

> **The Realm Rallies:** At Round Start, the player with the **fewest VP** (ties: fewest Renown, then fewest total resources) gains **+1 AP this round**. This bonus ignores and does not count against the +2 AP cap.

Bounded (+1, one player), thematic (the realm backs the underdog), and self-cancelling as positions equalize.

### 4.3 Action cost review (hypotheses to test, not pre-committed changes)

| Action | Current | Hypothesis | Test variant |
|---|---|---|---|
| Build | 3 AP (Legendary 4) | Too expensive next to Recruit 1 AP; development starved | **2 AP** (Legendary 3) |
| Research | 1/2/3 AP by tier + Mana | Tier III at 3 AP + 6 Mana may be unreachable in practice | Tier III → 2 AP |
| Trade | 1 AP | Fine (also gated once/round) | no change |
| Move / Recruit | 1 AP-ish | Baseline; fine | no change |

Run cost variants **only after** §4.1/§4.2 have baseline data — cap first, then calibrate prices.

## 5. Rule-text changes and propagation checklist

| Doc | Change |
|---|---|
| `rules_and_systems/Actions.md` | New "AP cap" section; rewrite *Starting Action Points* and *Gaining Additional AP* lists; Rally valve; update example scenario |
| `rules_and_systems/Renown.md` | Thresholds section: 5-Renown AP note "(counts against the +2 cap)"; replace the 10-Renown free action |
| `rules_and_systems/Buildings.md` | Guild Hall overflow wording |
| `rules_and_systems/Tiles.md` | City control bonus wording (first City AP, further Cities Gold) |
| `rules_and_systems/Round_Structure.md` | Round Start: add Rally valve resolution point |
| `rules_and_systems/High_Council.md` | Audit laws granting AP: add "(counts against the AP cap)" boilerplate |
| `playtest/First_Playable_Packet.md` | First Playable rule toggles for cap + Rally |
| `rulebook/Learn_to_Play.md`, `rulebook/Player_Aid.md` | AP summary boxes |
| `playtest/Balance_Dashboard.md` | Metrics below |

## 6. Playtest validation

**Metrics:**

- **AP spread** (max effective AP − min effective AP per round) — target ≤ 2 every round.
- **Actions taken per player per round** — the trailing player should act within 1–2 actions of the leader.
- **Pass timing:** who passes first each round and with how much AP stranded (feel-bad indicator).
- **Build actions per game per player** — if < 2 under baseline costs, run the 2 AP Build variant.

**Kill criteria:**

- If capped growth makes Cities feel pointless (players stop expanding past 2 Cities), raise the City overflow to +2 Gold or add a production multiplier instead.
- If the Rally valve is exploited (sandbagging VP to farm AP), convert it to "fewest VP **and** fewer than half the leader's VP."

## 7. Risks

- **Simultaneous change with Plan 1:** both alter how many attacks happen per round. Sequencing (index plan): Plan 1 ladder first, then apply the cap.
- **Lord sheets:** any Lord whose signature grants AP (audit all 12) needs an "ignores/counts against cap" call, one line each. Do this in the same pass as Plan 5.

## 8. Sequencing

Second plan to test, immediately after Plan 1's ladder. The cap + Rally are two rule lines — cheap to toggle in solo playtests. The §4.3 cost variants ride along afterwards, one at a time.
