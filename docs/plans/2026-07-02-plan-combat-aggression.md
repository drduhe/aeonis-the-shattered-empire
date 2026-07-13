# Plan 1: Combat Aggression Tuning

- **Status:** **RESOLVED 2026-07-13 (sim-led): do not promote Edge or Pillage.** Corrected Plan 4 home spacing is the accepted non-Pre-Strike lever; 6p/8p contested attacker wins now sit inside the 55–65% band. `Combat.md` remains unchanged.
- **Date:** 2026-07-02
- **Owning doc:** `rules_and_systems/Combat.md`
- **Related plans:** Plan 3 (VP legibility — military VP), Plan 5 (Lords parity — Vharok/Rakhis signatures touch combat)

---

## 1. Problem

The current combat math makes initiating battle irrational against a peer-strength defender, which pushes a war game toward static turtling.

**The math (current rules):**

- A hit requires Attack roll **strictly greater** than Defense roll. Infantry d6 vs d6 = **15/36 ≈ 42%** hit chance. Ties favor the defender.
- A 3v3 Infantry battle line trades ~**1.25 expected kills per side per battle round** — a symmetric meat grinder.
- The costs are asymmetric: the attacker pays **2 AP per battle round** (3 with Press the Attack); the defender pays **0 AP**, commits units from adjacent hexes for free, and gets Hold the Walls in Cities.
- Result: attacking a comparable force is EV-neutral in units and EV-negative in AP. Rational players don't attack; borders freeze.

**Secondary problems:**

- **Commitment ambiguity:** committed units "stay in their origin hexes" while fighting. It is undefined what happens if a committed unit's origin hex is itself attacked, or whether committed units can join a second battle the same round.
- **Poke-war pacing:** one battle round per Attack action means an even fight can drag across many turns, each costing the attacker 2 AP and the defender nothing.

## 2. Goals / Non-goals

**Goals**

1. Attacking with local superiority is clearly EV-positive; attacking at parity is a real gamble, not a donation.
2. Most non-siege battles resolve within 1–2 Attack actions.
3. Aggression creates map-level tempo (openings elsewhere), not just attrition.
4. Keep the Battle Line anti-doomstack core and the "sieges are special" identity untouched.

**Non-goals**

- No new dice mechanics (no hit tables, no rerolls as a core rule).
- No change to Attack's 2 AP cost (Plan 2 owns AP; changing both at once destroys attribution).
- No change to siege structure.

## 3. Options considered

| Option | Effect | Verdict |
|---|---|---|
| A. **Aggressor's Edge** — the attacking side's Attack rolls win ties (defender's Counterstrike rolls still must exceed) | d6-vs-d6 hit rate 42% → **58%** for the attacker only | **Rejected by sim** |
| B. **Pillage** — capturing a hex immediately grants its printed production once (Cities: 2 Gold) | Pays back part of the AP cost of a successful attack; makes conquest economically rational | **Rejected with Edge ladder; keep off** |
| C. **Engagement pins** — committed defenders are locked until the battle ends | Aggression creates openings elsewhere; also fixes the commitment ambiguity | **Adopt the state, defer the pin** (see §4.3) |
| D. Attack cost 2 AP → 1 AP | Fixes EV but invites low-cost harassment spam and drags round length | Rejected |
| E. Both sides win ties on their own Attack rolls | Faster and bloodier but symmetric — doesn't fix the attacker's AP tax | Rejected |
| F. Attacker chooses casualties on win | Too swingy; punishes elite units disproportionately | Rejected |

## 4. Recommended design (spec)

### 4.1 Aggressor's Edge (rule text direction)

> **Aggressor's Edge:** During a battle round, when a unit on the **attacking side** rolls its Attack Die (including Archer Pre-Strike), it deals damage if the roll is **greater than or equal to** the target's Defense roll. Units on the **defending side** still deal damage only on a strictly greater roll.

Resulting math for a 3v3 Infantry line: attacker expects ~1.75 kills per battle round vs. defender's ~1.25 — a ~1.4 : 1 material edge that compensates the 2 AP cost without making defense pointless. Cavalry (d8) as attacker rises from 56% to ~69% vs d6 defense; watch this in testing (see §6 kill criteria).

### 4.2 Pillage (rule text direction)

> **Pillage:** When you gain control of a hex via a won battle (Aftermath §5.1 or Siege victory §6.5), immediately gain that hex's printed production once (for Cities: 2 Gold). Pillaging does not deny the defender anything; it is a one-time bounty to the conqueror.

Interacts with `Renown.md` (first capture each round already grants +1 Renown, capped) — keep both; they answer "why attack?" from two directions (economy + progression).

### 4.3 Engaged state (rules-hole fix now, pin experiment later)

Adopt terminology now, because the ambiguity is a real hole:

> **Engaged:** While a battle is unresolved (units committed on both sides, e.g., a paused battle or an active Siege), all committed units are **Engaged**. An Engaged unit cannot move, cannot be committed to a different battle, and defends its own origin hex normally if that hex is attacked (resolving that new battle removes it from the original engagement).

The stronger version — Engaged defenders cannot be *chosen* as defenders' adjacent commits elsewhere, creating true map openings — is **experiment 2**, only if post-Edge data still shows turtling.

### 4.4 Explicitly unchanged

Attack = 2 AP; Press the Attack = +1 AP; Battle Line caps 3/5; retreat rules; siege pacing; Lord capture rewards (Plan 3 owns VP).

## 5. Rule-text changes and propagation checklist

| Doc | Change |
|---|---|
| `rules_and_systems/Combat.md` | §4.2/§4.3: Aggressor's Edge wording; §5: Pillage in Aftermath; §1/§3: Engaged definition; update §8 examples' math |
| `rules_and_systems/Renown.md` | Cross-reference Pillage (no rule change) |
| `rules_and_systems/Tiles.md` | Confirm "printed production" wording supports Pillage for unique tiles |
| `playtest/First_Playable_Packet.md` | Add the two rules as "First Playable rule" experiment toggles |
| `rulebook/Learn_to_Play.md` | Combat walkthrough dice examples (currently assume strict-greater everywhere) |
| `rulebook/Player_Aid.md` | Battle-round table: add Edge and Pillage lines |
| `rules_and_systems/Whispers.md` | Audit COMBAT cards for any that reference ties or re-rolls |
| `playtest/Balance_Dashboard.md` | Add metrics below |

## 6. Playtest validation

Run as an A/B ladder, changing one thing per ladder step: **baseline (current rules) → +Aggressor's Edge → +Pillage → (+Engagement pins only if needed).**

**Metrics (log per session in `session_log.csv`):**

- Battles initiated per player per round — target **≥ 0.75** from round 3 onward (baseline expected near 0.3).
- Attacker win rate when initiating — target **55–65%**.
- Hexes changing control per round — target ≥ 1 per 2 players.
- Share of winner's VP from military sources — should rise but stay under Plan 3's budget.

**Kill criteria (roll back or dial down):**

- Attacker win rate > 70%, or defenders report defense "feels pointless" → restrict Edge to Pre-Strike only, or grant Cities +1 Defense while Hold the Walls is declared.
- Pillage makes early rushing dominant (first-attacker win rate spikes) → Pillage capped at 1 Gold or Cities only.

## 7. Risks

- **Elite-unit skew:** d8/d10 attackers benefit more from Edge in absolute terms. Watch Cavalry and Advanced Units; mitigation is per-unit, not systemic.
- **Interaction with Plan 2:** if AP flattening lands simultaneously, attribute combat-frequency changes carefully — run Plan 1 ladder first (see index plan sequencing).
- **Whisper economy:** more battles = more COMBAT Whisper demand; deck cycling accelerates (Plan 4 owns deck scaling).

## 8. Sequencing

**Executed.** Full Edge ran hot; Pre-Strike failed its mixed M4 ladder. After Plan 4 corrected clustered home anchors and restored exact four-tile starts, the canonical no-upkeep Edge-off rebaseline recorded 66.7% / 64.2% / 62.3% contested attacker wins at 4p/6p/8p with ~7-round pacing. The 4p result remains a narrow watch; Pre-Strike worsened every count and stays off. See `../reports/2026-07-13-plan4-geometry-spacing.md`.
