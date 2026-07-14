# Aeonis M5 Local-Model Agent Playtest Pilot

Games: **1** · Qualitative seats: **3** · Providers: ollama

## Game facts

| Seed | Rounds | Final VP | Battles (attacker wins) | Council passed/proposed | Deals accepted/proposed |
| ---: | ---: | --- | ---: | ---: | ---: |
| 7311 | 7 | {'0': 10, '1': 5, '2': 10} | 3 (2) | 4/18 | 4/18 |

> Treat one-game and low-battle observations as prompts for replication, not balance conclusions.

## Reliability

| Seat-game | Provider calls | Decision attempts | Valid decisions | Persona delegations | Retries | Decision fallbacks | Qualitative failures | Model seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| seed 7311 / seat 0 (warmonger) | 3 | 1 | 1 | 107 | 0 | 0 | 0 | 35.89 |
| seed 7311 / seat 1 (economist) | 3 | 1 | 1 | 93 | 0 | 0 | 0 | 33.391 |
| seed 7311 / seat 2 (diplomat) | 4 | 1 | 1 | 93 | 1 | 0 | 0 | 64.234 |

### Provider diagnostics

- Seed 7311, seat 2, decision: `provider response did not contain a JSON object`

## Round reflections

- Seed 7311, seat 0, round 1: None reported. Highlight: Vharok leads in influence and renown, suggesting early focus on social or political objectives over military might. Friction: No battles have occurred yet. As a warmonger, I crave conflict to break the stalemate and create opportunities for decisive victories.
- Seed 7311, seat 1, round 1: None reported. Highlight: Vharok leads in controlled hexes (6), gold (6), and influence (1), signaling a strong early position. Friction: Low influence (1) and mana (2) across players may hinder future motion passing or ability usage.
- Seed 7311, seat 2, round 1: Vharok's strategic control and resource management are notable strengths in the first round. Highlight: Vharok leads with 6 controlled hexes, 6 gold, and early influence and mana gains, setting a strong foundation for future rounds. Friction: None reported.

## Exit interviews

### Seed 7311 · Seat 0 · warmonger

- **Pacing:** Average actions per player round (2.94) with minimal spread (0.83) indicates smooth pacing; no significant bottlenecks noted.
- **Map flow:** Player 2 controlled the most hexes (12) and buildings (5), suggesting a strong positional advantage.
- **Politics:** High council activity (18 motions proposed, 4 passed) but low collaboration (only 4 offers accepted out of 18).
- **Combat:** Balanced with 2 attacker wins vs. 1 defender win across 3 battles; no retreats or uncontested captures noted.
- **Economy pressure:** Player 2's dominance in building (5/10) may have pressured others, but stranded AP was 0.
- **Best moment:** The VP triggers for Players 0 and 2 hitting 10 VP in Round 7, ending the game early.
- **Biggest friction:** Player 1's limited VP (5) despite controlling hexes and objectives, suggesting potential imbalance in VP sources.
- **Would play again:** Yes
- **Hypotheses:** The VP trigger at 10 VP may be too easily attainable for some players, leading to early game ends. | Building limits or costs might need adjustment given Player 2's significant advantage.

### Seed 7311 · Seat 1 · economist

- **Pacing:** Pacing felt brisk with consistent action counts (~3 per player/round), though early builds by Players 1 and 2 set a strategic tempo.
- **Map flow:** Player 2's hex control (12) and Player 0's objective focus created a dynamic spatial competition, while Player 1's influence dominance (6) was underutilized.
- **Politics:** Gridlock in the council (4 passed / 18 proposed) may reflect either robust opposition or underpowered motion mechanics.
- **Combat:** Attacker dominance in contested battles (2-0) may indicate an imbalance, though sample size is small (3 battles).
- **Economy pressure:** Low stranded AP (0) and balanced action spread (avg 0.83) suggest a healthy economy with equitable resource access.
- **Best moment:** Player 0 securing 10 VP through objectives while Player 2 mirrored the achievement, highlighting the game's balance and multiple victory paths.
- **Biggest friction:** High negotiation activity with low success rates (4/18 offers accepted) suggests potential friction in collaboration mechanics.
- **Would play again:** Yes
- **Hypotheses:** Objective-based VP paths may be overpowered compared to lord capture or building strategies. | Negotiation mechanics may benefit from reduced complexity or increased incentives for cooperation.

### Seed 7311 · Seat 2 · diplomat

- **Pacing:** The pacing was steady with no major bottlenecks, allowing for consistent player engagement throughout the rounds.
- **Map flow:** The game saw a competitive control of hexes, with Player 2 controlling the most at 12, while Players 0 and 1 had 7 and 6 respectively.
- **Politics:** Council activity was high with many motions proposed but few passed, indicating potential gridlock or ineffective proposals.
- **Combat:** Combat was balanced with attackers having a slight edge but defenders managing some notable wins.
- **Economy pressure:** The action economy functioned smoothly with no significant gaps or stranded APs, indicating efficient resource management.
- **Best moment:** The final round was particularly intense as two players tied at 10 VP, creating a dramatic conclusion.
- **Biggest friction:** Players experienced some tension due to broken promises during negotiations, which may have impacted trust and gameplay dynamics.
- **Would play again:** Yes
- **Hypotheses:** High council motion failures might suggest either too many proposals or difficulty in passing them effectively. | Broken promises during negotiations could have influenced the game's trust dynamics and outcomes.

## Candidate rules questions

These are triage inputs, not automatic canon or Ambiguity Ledger entries.

- None reported.

## Decision moments

- Seed 7311, seat 0, round 3 (action): highlight=Attacking opponent's hex [1,-2] with cost 2 AP. This aggressive move aims to weaken the enemy and gain territorial control, aligning with the warmonger strategy of direct confrontation.
- Seed 7311, seat 1, round 2 (action): highlight=Played arcane_ascendancy to gain mana and research a discovery, enhancing resource management and strategic options.
- Seed 7311, seat 2, round 2 (council_vote): highlight=Lobbying for border arbitration aligns with my objective of expanding control. By spending Influence to sway votes, I increase the motion's chances of passing, stabilizing borders and preventing future skirmishes.

---

Model feedback is directional sim-only evidence. It does not replace human table play or promote rules to canon.
