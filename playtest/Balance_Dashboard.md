# Aeonis: Balance Dashboard

This is the living balance-tracking doc for playtesting. Every logged session (see `../agents/templates/Playtest_Report_Template.md`) feeds the tables below. Update after each session; review trends every 4-6 sessions.

**Companion file:** `session_log.csv` — one row per game, structured for spreadsheet analysis.

---

## 1. What to record per session (minimum)

| Metric | How to record |
| --- | --- |
| Date, player count, VP variant | header row |
| Total time & time per round | wall clock; note round count |
| Lords in play + final VP each | one line per player |
| Winner + winning VP sources | break the winner's 10 VP down by source |
| VP pace | VP of the leader at end of each round (list) |
| First artifact drawn (round) | target: round 3-4 |
| First Legendary built (round) | target: round 4-5 |
| Imperial Seat | rounds held by each player |
| Lord captures | count + were the +1 VP / +2 Renown moments dramatic or feel-bad? |
| Council | motions proposed / passed; did anyone lobby? |
| Catch-up | did last place close the gap after Populist Uprising / Winds of Fortune / draft order? |
| Downtime | worst wait between turns (estimate) |
| "Would you play again?" | yes/no per player, one-line why |

---

## 2. Lord performance tracker

Update cumulative rows after each session.

**Parity baseline:** The six Plan 5 signature redesigns (Cassian, Seraphel, Vharok, Elyndra, Rakhis, Auriel) landed on 2026-07-09. Do not combine pre-redesign and post-redesign matchup results; record `plan5` in session notes. Nyxara and Thal'rik are unchanged comparison anchors.

| Lord | Games | Wins | Avg VP | Avg finish position | Notes |
| --- | --- | --- | --- | --- | --- |
| Cassian | 0 | 0 | – | – | |
| Seraphel | 0 | 0 | – | – | |
| Vharok | 0 | 0 | – | – | |
| Elyndra | 0 | 0 | – | – | |
| Rakhis | 0 | 0 | – | – | |
| Nyxara | 0 | 0 | – | – | |
| Auriel | 0 | 0 | – | – | |
| Thal'rik | 0 | 0 | – | – | |

**Red flags:** any Lord above ~2x or below ~0.5x expected win rate after 8+ games; any Lord nobody voluntarily picks.

## 3. VP source distribution

Tally the winner's VP by source each game. Healthy state: no single source dominating across games.

| Source | Game 1 | Game 2 | Game 3 | ... |
| --- | --- | --- | --- | --- |
| Public objectives | | | | |
| Secret objectives | | | | |
| Lord objectives | | | | |
| Council titles | | | | |
| Imperial Seat (Coronation Rite + milestone) | | | | |
| Legendary Buildings | | | | |
| VP artifacts | | | | |
| Lord captures | | | | |

**Plan 3 MVP target (winner's 10 VP):** objectives ≥60% · Coronation/military ~20% · lord capture ≤25% of winner VP.

## 4. Pacing tracker

| Metric | Target | Observed (rolling) |
| --- | --- | --- |
| Rounds per game | 6-8 (accepted 2026-07-12; was 7-10 / aspirational 8-10) | |
| Time per round (4p) | 25-40 min | |
| Full-game session (4-6p) | 4-10 hours (locked D1) | |
| First battle | by round 2 | |
| First council motion passed | round 1-2 | |
| Leader VP at end of round 4 | 4-6 | |

---

## 5. Tuning levers (hot spots and their dials)

When a problem shows up, reach for the matching dial. Change **one dial at a time**, then re-test.

### 5.1 Imperial Seat scoring
- **Symptom:** Seat-holder snowballs / nobody contests the Seat.
- **Dials:** Coronation Rite Lord-presence requirement; third-Rite milestone timing; Seat hex production; defender terrain bonuses on the Seat hex.

### 5.2 Lord capture loop
- **Symptom:** Lord-sniping dominates (capture = +1 VP +2 Renown + ability lockout is 3 rewards) or Lords never leave home.
- **Dials:** drop the +2 Renown to +1; release timing (end of round → immediately after battle); captured Lord ability lockout → lockout of active ability only.

### 5.3 AP economy stacking
- **Symptom:** wide players run away on tempo. Max stack today: 5 base +2 Cities +1 Guild Hall +1 Renown(5) + free 1-AP action (Renown 10) + banked 2.
- **Dials:** City AP cap +2 → +1; Guild Hall +1 AP → once per game rebate; bank max 2 → 1; Renown 10 free action → once per two rounds.

### 5.4 Catch-up sufficiency
- **Symptom:** last place at round 4 never finishes better than last.
- **Dials:** Winds of Fortune +2 AP → +2 AP and +2 resources; draft order (already lowest-VP-first); add a "bounty on the leader" event; Populist Uprising also grants 1 Whisper.

### 5.5 Economy conversion (Bank / Golden Alchemy / Cassian)
- **Symptom:** one conversion engine outperforms raw production.
- **Dials:** Bank 2:3 → 1:1 plus a flat +1; Golden Alchemy once per round cap (already); Cassian's Letters of Credit rate.

### 5.6 Whisper draw rate
- **Symptom:** hands hit the 7 limit routinely (too many) or players never hold a counter (too few).
- **Dials:** Round Start draw 2 → 1; VP-score draw → remove; hand limit 7 → 5.

### 5.7 Battle line cap
- **Symptom:** doomstacks still win everything / defenders always hold.
- **Dials:** cap 3 → 4 in open field; City/Fortress cap 5 → 4; Archer Pre-Strike damage.

### 5.8 Strategy card balance
- **Symptom:** one card always drafted first (or last) across games.
- **Watch specifically:** Imperial Mandate (VP on card), Tactical Reinforcements (free units), Diplomatic Decree (Speaker + forced vote). Dials: AP costs of primaries, bounty rule (§1.3 of `Strategy.md`) usually self-corrects mild imbalance — check it's being used.

### 5.9 Adjacency Claim (passive expansion)
- **Symptom:** map fills with unguarded claims; too little contact.
- **Dials:** 2 Cleanup checks → 3; Cities only (drop Towers); claimed hexes produce nothing until garrisoned once.

---

## 6. Blind-test readiness gate (Phase 4 exit)

Do not schedule blind playtests until all are true:

- [ ] 6+ logged games; every Lord picked ≥2 times
- [ ] No designer ruling needed in the last 2 games
- [ ] Median session inside the 4-10 hour target (full scope) or 90-180 min (First Playable scope)
- [ ] No Lord win-rate red flag open
- [ ] Winner VP source spread: no source >50% of winning VP across last 4 games
