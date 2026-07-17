# Aeonis Six-Player Lord and Persona Rotation

**Status:** completed, sim-only

## Executive readout

- All six canonical 10-VP games completed. Mean length was **7.17 rounds**; five of six landed in the accepted 6–8-round band.
- Lords rotated one seat per game while personas remained fixed. Each Lord therefore occupied every seat once and encountered the same persona distribution: diplomat, economist, two warmonger seats, expander, and balanced.
- Elyndra won three of six games, twice with a warmonger and once with an economist. Vharok, Seraphel, and Cassian won once each. This is a replication target, not a balance verdict: map/seed changed with assignment and the campaign is only six games.
- The qualitative layer was provider-clean: **36/36 sampled decisions** and **36/36 exit interviews** completed, with zero decision fallback.

## Next inference

Rotation removes the obvious fixed-seat/fixed-persona confound from the prior two-game pilot. The next comparative Lord test should use matched seeds and more repetitions around Elyndra rather than change a Lord sheet from this small sample.

Games: **6** · Qualitative seats: **36** · Providers: ollama

## Game facts

| Seed | Rounds | Final VP | Battles (attacker wins) | Council passed/proposed | Deals accepted/proposed |
| ---: | ---: | --- | ---: | ---: | ---: |
| 7690 | 6 | {0: 4, 1: 4, 2: 11, 3: 6, 4: 4, 5: 6} | 10 (6) | 5/30 | 21/35 |
| 7691 | 9 | {0: 8, 1: 8, 2: 10, 3: 4, 4: 8, 5: 7} | 11 (8) | 0/48 | 29/52 |
| 7692 | 7 | {0: 6, 1: 10, 2: 8, 3: 6, 4: 9, 5: 5} | 11 (7) | 10/36 | 27/40 |
| 7693 | 6 | {0: 6, 1: 6, 2: 7, 3: 2, 4: 12, 5: 7} | 4 (2) | 10/30 | 23/33 |
| 7694 | 8 | {0: 8, 1: 8, 2: 8, 3: 6, 4: 8, 5: 12} | 9 (8) | 5/42 | 16/46 |
| 7695 | 7 | {0: 8, 1: 10, 2: 5, 3: 4, 4: 8, 5: 6} | 7 (5) | 5/36 | 27/42 |

> Treat one-game and low-battle observations as prompts for replication, not balance conclusions.

## Reliability

| Seat-game | Control | Provider calls | Decision attempts | Valid decisions | Forced choices | Persona delegations | Retries | Decision fallbacks | Qualitative failures | Model seconds |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| seed 7690 / seat 0 (diplomat) | sampled | 2 | 1 | 1 | 0 | 120 | 0 | 0 | 0 | 24.547 |
| seed 7690 / seat 1 (economist) | sampled | 2 | 1 | 1 | 6 | 100 | 0 | 0 | 0 | 33.251 |
| seed 7690 / seat 2 (warmonger) | sampled | 2 | 1 | 1 | 0 | 121 | 0 | 0 | 0 | 25.015 |
| seed 7690 / seat 3 (expander) | sampled | 2 | 1 | 1 | 5 | 111 | 0 | 0 | 0 | 28.328 |
| seed 7690 / seat 4 (balanced) | sampled | 2 | 1 | 1 | 0 | 110 | 0 | 0 | 0 | 28.423 |
| seed 7690 / seat 5 (warmonger) | sampled | 2 | 1 | 1 | 1 | 108 | 0 | 0 | 0 | 27.374 |
| seed 7691 / seat 0 (diplomat) | sampled | 2 | 1 | 1 | 8 | 174 | 0 | 0 | 0 | 26.952 |
| seed 7691 / seat 1 (economist) | sampled | 2 | 1 | 1 | 6 | 165 | 0 | 0 | 0 | 25.141 |
| seed 7691 / seat 2 (warmonger) | sampled | 2 | 1 | 1 | 1 | 163 | 0 | 0 | 0 | 34.89 |
| seed 7691 / seat 3 (expander) | sampled | 2 | 1 | 1 | 9 | 171 | 0 | 0 | 0 | 25.156 |
| seed 7691 / seat 4 (balanced) | sampled | 2 | 1 | 1 | 1 | 178 | 0 | 0 | 0 | 29.797 |
| seed 7691 / seat 5 (warmonger) | sampled | 2 | 1 | 1 | 0 | 172 | 0 | 0 | 0 | 29.922 |
| seed 7692 / seat 0 (diplomat) | sampled | 2 | 1 | 1 | 0 | 144 | 0 | 0 | 0 | 29.657 |
| seed 7692 / seat 1 (economist) | sampled | 2 | 1 | 1 | 1 | 119 | 0 | 0 | 0 | 22.374 |
| seed 7692 / seat 2 (warmonger) | sampled | 2 | 1 | 1 | 1 | 134 | 0 | 0 | 0 | 27.157 |
| seed 7692 / seat 3 (expander) | sampled | 2 | 1 | 1 | 6 | 120 | 0 | 0 | 0 | 28.28 |
| seed 7692 / seat 4 (balanced) | sampled | 2 | 1 | 1 | 0 | 128 | 0 | 0 | 0 | 38.485 |
| seed 7692 / seat 5 (warmonger) | sampled | 2 | 1 | 1 | 7 | 125 | 0 | 0 | 0 | 37.438 |
| seed 7693 / seat 0 (diplomat) | sampled | 2 | 1 | 1 | 2 | 113 | 0 | 0 | 0 | 30.172 |
| seed 7693 / seat 1 (economist) | sampled | 2 | 1 | 1 | 1 | 99 | 0 | 0 | 0 | 27.188 |
| seed 7693 / seat 2 (warmonger) | sampled | 2 | 1 | 1 | 1 | 103 | 0 | 0 | 0 | 39.141 |
| seed 7693 / seat 3 (expander) | sampled | 2 | 1 | 1 | 0 | 113 | 0 | 0 | 0 | 31.015 |
| seed 7693 / seat 4 (balanced) | sampled | 2 | 1 | 1 | 5 | 102 | 0 | 0 | 0 | 31.312 |
| seed 7693 / seat 5 (warmonger) | sampled | 2 | 1 | 1 | 2 | 101 | 0 | 0 | 0 | 37.235 |
| seed 7694 / seat 0 (diplomat) | sampled | 2 | 1 | 1 | 2 | 143 | 0 | 0 | 0 | 31.312 |
| seed 7694 / seat 1 (economist) | sampled | 2 | 1 | 1 | 2 | 134 | 0 | 0 | 0 | 33.531 |
| seed 7694 / seat 2 (warmonger) | sampled | 2 | 1 | 1 | 1 | 156 | 0 | 0 | 0 | 28.5 |
| seed 7694 / seat 3 (expander) | sampled | 2 | 1 | 1 | 15 | 141 | 0 | 0 | 0 | 25.094 |
| seed 7694 / seat 4 (balanced) | sampled | 2 | 1 | 1 | 3 | 153 | 0 | 0 | 0 | 29.078 |
| seed 7694 / seat 5 (warmonger) | sampled | 2 | 1 | 1 | 0 | 151 | 0 | 0 | 0 | 29.86 |
| seed 7695 / seat 0 (diplomat) | sampled | 2 | 1 | 1 | 2 | 133 | 0 | 0 | 0 | 28.141 |
| seed 7695 / seat 1 (economist) | sampled | 2 | 1 | 1 | 1 | 124 | 0 | 0 | 0 | 27.282 |
| seed 7695 / seat 2 (warmonger) | sampled | 2 | 1 | 1 | 6 | 125 | 0 | 0 | 0 | 26.016 |
| seed 7695 / seat 3 (expander) | sampled | 2 | 1 | 1 | 6 | 136 | 0 | 0 | 0 | 34.062 |
| seed 7695 / seat 4 (balanced) | sampled | 2 | 1 | 1 | 1 | 136 | 0 | 0 | 0 | 29.782 |
| seed 7695 / seat 5 (warmonger) | sampled | 2 | 1 | 1 | 1 | 126 | 0 | 0 | 0 | 31.437 |

### Provider diagnostics

- No provider errors recorded.

## Round reflections

- No round reflections requested.

## Negotiation transcript

- Seed 7690, round 2, seat 5 (negotiation_propose, vote_bargain): Player 4, support the 'Magister of Mana' motion, and I promise you 1 gold by round 3. Let's secure this together for mutual benefit. Terms: `{"gets": {}, "gives": {}, "promises": [{"from": 4, "kind": "vote", "motion": "magister_of_mana", "support": true, "to": 5}, {"amount": 1, "due_round": 3, "from": 5, "kind": "future_payment", "resource": "gold", "to": 4}]}`.
- Seed 7690, round 2, seat 0 (negotiation_propose, vote_agreement): I propose a vote agreement with Player 1. In exchange for their support on the 'magister_of_mana' motion, we can strengthen our alliance and work towards mutual goals in future councils. Terms: `{"gets": {}, "gives": {}, "promises": [{"from": 1, "kind": "vote", "motion": "magister_of_mana", "support": true, "to": 0}]}`.
- Seed 7691, round 2, seat 5 (negotiation_propose, vote_bargain): Player 4, I propose a bargain: support imperial annexation now, and I will ensure you receive 1 gold by round 3. This alliance strengthens both our positions. Will you commit? Terms: `{"gets": {}, "gives": {}, "promises": [{"from": 4, "kind": "vote", "motion": "imperial_annexation", "support": true, "to": 5}, {"amount": 1, "due_round": 3, "from": 5, "kind": "future_payment", "resource": "gold", "to": 4}]}`.
- Seed 7691, round 2, seat 0 (negotiation_propose, vote_bargain): Player 1, I propose a vote bargain: if you support imperial_annexation, I'll pay you 1 gold in round 3. Let's work together for mutual benefit. Terms: `{"gets": {}, "gives": {}, "promises": [{"from": 1, "kind": "vote", "motion": "imperial_annexation", "support": true, "to": 0}, {"amount": 1, "due_round": 3, "from": 0, "kind": "future_payment", "resource": "gold", "to": 1}]}`.
- Seed 7692, round 2, seat 0 (negotiation_propose, vote_bargain): To Player 2: I propose that you support my motion for border_arbitration. In return, I will ensure you receive 1 gold in round 3. This alliance benefits both our agendas. Terms: `{"gets": {}, "gives": {}, "promises": [{"from": 2, "kind": "vote", "motion": "border_arbitration", "support": true, "to": 0}, {"amount": 1, "due_round": 3, "from": 0, "kind": "future_payment", "resource": "gold", "to": 2}]}`.
- Seed 7692, round 2, seat 5 (negotiation_propose, vote_bargain): Player 5 proposes: In exchange for your vote on border_arbitration, I will pay you 1 gold by Round 3. Support this motion to strengthen our position and secure future gains. Terms: `{"gets": {}, "gives": {}, "promises": [{"from": 4, "kind": "vote", "motion": "border_arbitration", "support": true, "to": 5}, {"amount": 1, "due_round": 3, "from": 5, "kind": "future_payment", "resource": "gold", "to": 4}]}`.
- Seed 7693, round 2, seat 5 (negotiation_skip, unspecified): Decline to negotiate. Warmongers do not support demilitarization.
- Seed 7693, round 2, seat 0 (negotiation_propose, vote_bargain): I propose that you, Player 2, support the demilitarized_zone motion in exchange for a future payment of 1 gold in Round 3. This agreement would benefit both of us by securing your vote and providing me with the necessary resources later. Terms: `{"gets": {}, "gives": {}, "promises": [{"from": 2, "kind": "vote", "motion": "demilitarized_zone", "support": true, "to": 0}, {"amount": 1, "due_round": 3, "from": 0, "kind": "future_payment", "resource": "gold", "to": 2}]}`.
- Seed 7694, round 2, seat 5 (negotiation_propose, vote_agreement): I propose that you support the 'Hero of the Realm' motion. Your vote is crucial for its passage, and together we can strengthen our position in the council. Terms: `{"gets": {}, "gives": {}, "promises": [{"from": 0, "kind": "vote", "motion": "hero_of_the_realm", "support": true, "to": 5}]}`.
- Seed 7694, round 2, seat 0 (negotiation_counter, resource_trade): I appreciate your proposal, but I need something in return. How about exchanging 1 gold for 1 mana? This way, we both benefit from our alliance. Terms: `{"gets": {"mana": 1}, "gives": {"gold": 1}, "promises": []}`.
- Seed 7695, round 2, seat 0 (negotiation_propose, vote_bargain): Player 2, I offer you 1 gold in round 3 if you support my motion to be Hero of the Realm. This is a fair exchange that benefits both of us. Terms: `{"gets": {}, "gives": {}, "promises": [{"from": 2, "kind": "vote", "motion": "hero_of_the_realm", "support": true, "to": 0}, {"amount": 1, "due_round": 3, "from": 0, "kind": "future_payment", "resource": "gold", "to": 2}]}`.
- Seed 7695, round 2, seat 5 (negotiation_propose, vote_bargain): Player 1, I propose a bargain: you support the 'Hero of the Realm' motion, and in return, I will pay you 1 gold by round 3. This ensures our agenda passes while rewarding your contribution. What do you say? Terms: `{"gets": {}, "gives": {}, "promises": [{"from": 1, "kind": "vote", "motion": "hero_of_the_realm", "support": true, "to": 5}, {"amount": 1, "due_round": 3, "from": 5, "kind": "future_payment", "resource": "gold", "to": 1}]}`.

### Promise outcomes

- Seed 7690: vote from seat 4 to seat 5 — broken (vote_cast).
- Seed 7690: future_payment from seat 5 to seat 4 — broken (payment_not_transferred).
- Seed 7690: attack_target from seat 4 to seat 0 — broken (attack_not_declared).
- Seed 7690: non_aggression from seat 3 to seat 5 — kept (term_expired_without_attack).
- Seed 7690: non_aggression from seat 5 to seat 3 — kept (term_expired_without_attack).
- Seed 7690: non_aggression from seat 3 to seat 0 — kept (term_expired_without_attack).
- Seed 7691: vote from seat 4 to seat 5 — kept (vote_cast).
- Seed 7691: future_payment from seat 5 to seat 4 — broken (payment_not_transferred).
- Seed 7691: non_aggression from seat 3 to seat 4 — kept (term_expired_without_attack).
- Seed 7691: non_aggression from seat 4 to seat 3 — kept (term_expired_without_attack).
- Seed 7692: non_aggression from seat 3 to seat 0 — kept (term_expired_without_attack).
- Seed 7692: non_aggression from seat 0 to seat 3 — kept (term_expired_without_attack).
- Seed 7692: vote from seat 2 to seat 0 — broken (vote_cast).
- Seed 7692: future_payment from seat 0 to seat 2 — broken (payment_not_transferred).
- Seed 7692: vote from seat 4 to seat 5 — broken (vote_cast).
- Seed 7692: future_payment from seat 5 to seat 4 — broken (payment_not_transferred).
- Seed 7693: vote from seat 2 to seat 0 — broken (vote_cast).
- Seed 7693: future_payment from seat 0 to seat 2 — broken (payment_not_transferred).
- Seed 7694: attack_target from seat 4 to seat 3 — broken (attack_not_declared).
- Seed 7695: vote from seat 2 to seat 0 — broken (vote_cast).
- Seed 7695: future_payment from seat 0 to seat 2 — broken (payment_not_transferred).
- Seed 7695: attack_target from seat 1 to seat 3 — broken (attack_not_declared).
- Seed 7695: attack_target from seat 4 to seat 3 — broken (attack_not_declared).

## Exit interviews

### Seed 7690 · Seat 0 · diplomat

- **Pacing:** Game had a steady pace with active negotiation but limited whisper use.
- **Map flow:** Controlled hexes varied widely, affecting influence and resources.
- **Politics:** Negotiation was frequent but ineffective in securing commitments.
- **Combat:** Combat balanced but may be too predictable.
- **Economy pressure:** Build disparity suggests varied strategies or opportunities.
- **Best moment:** Player 2's strategic capture of a lord for VP dominance.
- **Biggest friction:** Council motions rarely passed, leading to frustration.
- **Would play again:** Yes
- **Hypotheses:** Low council motion passage might indicate difficulty in achieving consensus. | VP reliance on objectives could overshadow other victory paths.

### Seed 7690 · Seat 1 · economist

- **Pacing:** The game concluded after 6 rounds, with Player 2's decisive moves leading to an early VP lead.
- **Map flow:** High variance in controlled hexes among players, with Player 5 controlling the most (14), indicating varied strategic focuses.
- **Politics:** Low trust among players, evidenced by more broken promises than kept, affecting diplomatic strategies.
- **Combat:** Combat was balanced with 6 attacker wins vs. 4 defender wins, suggesting an encouraging environment for aggressive strategies.
- **Economy pressure:** Player 2's focused strategy on objectives yielded high rewards, while others struggled to capitalize similarly.
- **Best moment:** Player 2 (vharok) achieved a dominant victory with 11 VP, primarily through objective completion and lord capture.
- **Biggest friction:** The council system was ineffective, with only 5 motions passing out of 30 proposed, indicating low collaboration among players.
- **Would play again:** Yes
- **Hypotheses:** Focusing on high-VP objectives early may be a winning strategy. | Adjustments to the council system could encourage more collaboration and impactful motions.

### Seed 7690 · Seat 2 · warmonger

- **Pacing:** The game maintained a steady pace with varied strategic opportunities.
- **Map flow:** Objective control was pivotal, indicating balanced game design around territorial objectives.
- **Politics:** Low influence usage and high motion failures point to possible issues in council engagement or mechanics.
- **Combat:** Attackers had a slight edge, but small sample size limits conclusions on combat balance.
- **Economy pressure:** Player 1's dominance in building suggests possible imbalance or effective strategy in resource management.
- **Best moment:** Player 2's decisive victory through objective control and lord capture highlights the game's depth in strategic paths.
- **Biggest friction:** Gridlock in council motions and low influence usage suggest potential issues with council mechanics or player engagement.
- **Would play again:** Yes
- **Hypotheses:** Adjust building mechanics to prevent single-player dominance. | Evaluate council dynamics for potential rule changes to reduce gridlock.

### Seed 7690 · Seat 3 · expander

- **Pacing:** The game maintained a steady pace with moderate action gaps, allowing players time to strategize without stalling.
- **Map flow:** Uncontested captures favored attackers, emphasizing the need for defensive alliances or support to counteract this trend.
- **Politics:** Negotiation attempts were frequent but often unfulfilled, indicating a need for more reliable promise-keeping mechanisms or clearer incentives for cooperation.
- **Combat:** Combat dynamics were balanced with split outcomes in supported battles and a clear edge for attackers in uncontested scenarios, highlighting the value of alliances.
- **Economy pressure:** Varied building activity with Player 1 leading at 6 builds, suggesting that economic control can significantly influence game outcomes.
- **Best moment:** Player 2 (Vharok) securing a dominant 11 VP lead through effective objective control and lord capture, showcasing the importance of strategic positioning.
- **Biggest friction:** The council's low influence impact with only 5 motions passed out of 30 proposed, indicating potential for improvement in player engagement with council mechanics.
- **Would play again:** Yes
- **Hypotheses:** Objective control is pivotal; enhancing their strategic importance could deepen gameplay. | Increasing council influence effectiveness might boost player engagement and reduce frustration.

### Seed 7690 · Seat 4 · balanced

- **Pacing:** Well-paced game with active rounds and no significant delays, supporting a balanced flow of actions.
- **Map flow:** Varied hex control, with Vharok controlling the most (14) and others having between 6-8, suggesting dynamic territorial competition.
- **Politics:** Active diplomacy with many offers (35 proposed, 21 accepted) but notable broken promises (3), indicating potential trust issues or strategic shifts.
- **Combat:** Active combat with 10 battles, balanced wins between attackers (6) and defenders (4), highlighting strategic depth.
- **Economy pressure:** Moderate action economy with an average of 3.4 actions per player round, manageable gaps, and varied builds by players.
- **Best moment:** Vharok's decisive victory in VP with 11 points, primarily from objectives and a lord capture.
- **Biggest friction:** Low council effectiveness with only 5 motions passed out of 30 proposed, indicating potential issues with cooperation or opposition dynamics.
- **Would play again:** Yes
- **Hypotheses:** The low success rate of council motions may stem from high opposition or insufficient incentives for cooperation. | Vharok's dominance in VP could be due to effective objective control or superior strategic play.

### Seed 7690 · Seat 5 · warmonger

- **Pacing:** The game had a steady pace, but the council phase was slower due to low motion success.
- **Map flow:** Player 2's control of key areas contributed significantly to their VP lead.
- **Politics:** Negotiation dynamics were active but fragile due to broken promises affecting alliances.
- **Combat:** Combat was balanced with attackers slightly more successful, but sample size is small.
- **Economy pressure:** The economy seemed manageable without excessive pressure from other players.
- **Best moment:** The most exciting moment was when Player 2 captured a lord to secure a significant VP lead.
- **Biggest friction:** Players found it challenging to pass motions in the council, leading to frustration.
- **Would play again:** Yes
- **Hypotheses:** Objective-based VP might be too dominant; consider balancing with other victory paths. | Council mechanics may need adjustment to increase motion success rates and player engagement.

### Seed 7691 · Seat 0 · diplomat

- **Pacing:** The game maintained a steady pace with an average of 3.27 actions per round, though action gaps varied, indicating potential for strategic depth in timing moves.
- **Map flow:** Player 2's strategic focus on both objectives and lord capture proved pivotal, while others relied more heavily on objectives, highlighting the significance of diverse victory paths.
- **Politics:** Negotiation dynamics were robust, with many offers and some promises made. The prevalence of non-aggression pacts suggests a preference for stability over conflict.
- **Combat:** Combat was frequent, with attackers having a significant advantage. Most battles were uncontested captures, suggesting that defense is less rewarding or that attackers dominate.
- **Economy pressure:** Player 4 emerged as the most active builder, constructing 10 buildings, which may have contributed to their economic strength despite not securing the highest VP.
- **Best moment:** The decisive moment was player 2's capture of a lord, granting them an additional VP boost and securing their victory.
- **Biggest friction:** Players faced challenges with the council system, as motions were proposed but none passed, indicating potential gridlock or resistance to collective action.
- **Would play again:** Yes
- **Hypotheses:** The council system's effectiveness in facilitating meaningful collective action requires further investigation. | Non-aggression pacts and future payment promises could be explored for their impact on long-term strategy and trust.

### Seed 7691 · Seat 1 · economist

- **Pacing:** Pacing was steady with a clear mid-game lull before the VP surge in rounds 7-9. This created tension as players scrambled to secure final objectives.
- **Map flow:** The game started in the north but shifted south after Player 2's lord captures. The map's central hexes became contested late-game hotspots.
- **Politics:** Politics were largely ineffective; no council motions passed, indicating either disinterest or strategic gridlock among players.
- **Combat:** Combat was frequent but lopsided; attackers won most battles. Retreats were common, suggesting players prefer avoiding losses over all-out confrontations.
- **Economy pressure:** The economy felt pressured in the mid-game as gold reserves dwindled for several players, forcing tough resource allocation decisions.
- **Best moment:** The most exciting moment was when Player 2 captured two lords in quick succession, jumping to the lead in VP.
- **Biggest friction:** Players expressed confusion about the Coronation Rites and how to properly score objectives at game end.
- **Would play again:** Yes
- **Hypotheses:** Objective VP may be too concentrated; consider spreading VP across more objectives to encourage diverse strategies. | Coronation Rites scoring needs clearer guidance to reduce confusion and ensure consistent application.

### Seed 7691 · Seat 2 · warmonger

- **Pacing:** The game maintained a steady pace with consistent combat opportunities, supporting an aggressive playstyle.
- **Map flow:** The game emphasized objective-based VP, with some strategic gains through lord captures, suggesting a balanced approach between objectives and key targets.
- **Politics:** Council dynamics were ineffective; alternative strategies like combat and objectives are more reliable for VP gain.
- **Combat:** Combat was highly effective with attackers winning 8 out of 11 battles, indicating that offensive strategies are advantageous.
- **Economy pressure:** Player 1's extensive building (9) provided economic strength but didn't translate to higher VP, highlighting the balance between economy and combat.
- **Best moment:** The decisive battle that secured a lord capture, demonstrating the effectiveness of aggressive tactics.
- **Biggest friction:** The high failure rate of council motions (48 failed), suggesting a competitive environment where collaboration is challenging.
- **Would play again:** Yes
- **Hypotheses:** Warmonger playstyle may benefit from focusing on aggressive tactics and lord captures over council motions. | Negotiations are frequent but unreliable; cautious promise-making is advisable.

### Seed 7691 · Seat 3 · expander

- **Pacing:** The game maintained steady progress, with an average of 3.27 actions per player round and minimal action gaps.
- **Map flow:** The game saw a fragmented control landscape, with no player dominating more than 14 hexes and several regions contested.
- **Politics:** Negotiation was active but tenuous, with many offers made (52) and a notable number broken (1).
- **Combat:** Combat was frequent but often inconclusive, with attackers winning only 73% of battles and many encounters ending in retreats.
- **Economy pressure:** Player 4 emerged as a dominant economic force, controlling the most hexes (10) and amassing significant gold (28).
- **Best moment:** Player 2's strategic focus on objectives and lord capture led to their decisive victory with 10 VP.
- **Biggest friction:** The council system saw no successful motions, suggesting potential ineffectiveness or underutilization by players.
- **Would play again:** Yes
- **Hypotheses:** The council system may need adjustments to encourage more successful motions. | Lord capture could be a more impactful VP source if balanced against objectives.

### Seed 7691 · Seat 4 · balanced

- **Pacing:** The game maintained a steady pace with slight acceleration in later rounds due to increased actions and VP contention.
- **Map flow:** Player 2 dominated the map with high controlled hexes, while others focused on specific objectives.
- **Politics:** Negotiation was active but fragile; broken promises suggest need for stronger enforcement or trust-building mechanics.
- **Combat:** Combat was decisive but lacked engagement; attackers dominated uncontested battles.
- **Economy pressure:** Economic pressure varied; some players focused on building while others prioritized VP objectives.
- **Best moment:** Player 2 achieving the highest VP through objective completion and lord capture.
- **Biggest friction:** The council system's ineffectiveness, with all motions failing despite active influence spending.
- **Would play again:** Yes
- **Hypotheses:** The council system may need adjustments to encourage successful motions and strategic use of influence. | Combat dynamics could benefit from more balanced engagement or incentives for defenders.

### Seed 7691 · Seat 5 · warmonger

- **Pacing:** Game maintained steady pace with consistent actions per round.
- **Map flow:** Controlled hexes suggest territorial balance, with Player Elyndra leading VP.
- **Politics:** Diplomacy active but council ineffectiveness hinders gameplay.
- **Combat:** Combat decisive but low engagement; high retreats suggest players avoid losses.
- **Economy pressure:** Player 1's dominance in building actions may indicate imbalance or strategic exploit.
- **Best moment:** Player Elyndra securing 10 VP through objectives and lord capture highlights effective strategy.
- **Biggest friction:** Council system dysfunction with no motions passed, indicating potential rule issues.
- **Would play again:** Yes
- **Hypotheses:** Council mechanics need adjustment to enable motion passage. | Building action allocation might require balancing to prevent dominance.

### Seed 7692 · Seat 0 · diplomat

- **Pacing:** The game maintained a steady pace with consistent action usage, allowing for thorough exploration of strategies without stagnation.
- **Map flow:** Player 4's success in capturing a lord contributed significantly to their VP, highlighting the importance of strategic positioning and combat effectiveness.
- **Politics:** The council was active but challenging to influence, with only 10 motions passing despite 36 proposals, suggesting a competitive political landscape.
- **Combat:** Combat was frequent with attackers having an edge, but the majority of battles were uncontested, suggesting effective use of retreats and strategic positioning.
- **Economy pressure:** The economy functioned smoothly with no stranded AP, allowing players to utilize their actions effectively across rounds.
- **Best moment:** The high number of motions proposed (36) and the active council votes suggest a lively political environment where players engaged deeply with influencing outcomes.
- **Biggest friction:** The low rate of promises kept (2 out of 6) indicates potential issues with trust or coordination among players, affecting strategic alliances.
- **Would play again:** Yes
- **Hypotheses:** Players may have focused on objectives over building special structures like the Bank or Forge, indicating a preference for direct VP gain. | The high number of offers rejected (13) could reflect differing priorities or cautious negotiation strategies.

### Seed 7692 · Seat 1 · economist

- **Pacing:** The game maintained a consistent pace across 7 rounds, with no significant delays or bottlenecks.
- **Map flow:** Player 3 (Lord Nyxara) controlled the most hexes (11), while Player 4 (Lord Cassian) had a strong presence with 12 controlled hexes.
- **Politics:** Council activity was high with 36 motions proposed but only 10 passed, highlighting the complexity of political negotiations.
- **Combat:** Combat was frequent with 11 battles, showing a slight edge for attackers (7 wins vs. 4 defender wins).
- **Economy pressure:** Economic activity was steady with an average of 3.36 actions per player round and no stranded AP.
- **Best moment:** The game concluded with a clear victory for Player 1 (Lord Elyndra) who secured 10 VP, primarily through objectives.
- **Biggest friction:** High number of failed motions in council (26 out of 36 proposed), indicating potential political challenges or misalignment among players.
- **Would play again:** Yes
- **Hypotheses:** The high number of failed motions in council may indicate a need for more effective political strategies or clearer objectives. | Combat dynamics suggest attackers have an advantage, which could influence future game balance considerations.

### Seed 7692 · Seat 2 · warmonger

- **Pacing:** Manageable action pace (3.36 actions/round), balanced gameplay.
- **Map flow:** Player 4 dominated gold and pop, while Player 5 excelled in mana.
- **Politics:** Negotiation active but with low offer acceptance (27/40).
- **Combat:** Active combat with 11 battles; attackers won more in contested areas.
- **Economy pressure:** Moderate builds (2 per player), Player 1 leading with 8 builds.
- **Best moment:** Player 1's decisive victory with 10 VP, highlighting objectives' importance.
- **Biggest friction:** Low council effectiveness (10/36 motions passed) and high promise broken rate (4/6).
- **Would play again:** Yes
- **Hypotheses:** Objectives may be too impactful compared to other VP sources. | Whisper underutilization could indicate mechanic ineffectiveness.

### Seed 7692 · Seat 3 · expander

- **Pacing:** The pacing was steady, though the game could benefit from a mid-game event to refresh strategies and keep players engaged.
- **Map flow:** The map flow was logical, but some areas felt underutilized. More varied terrain types could offer strategic advantages.
- **Politics:** Politics were vibrant with active participation in council motions. However, the high number of failed motions suggests players might need more tools to sway votes effectively.
- **Combat:** Combat was engaging but could benefit from more strategic depth, such as introducing different tactics or terrain effects.
- **Economy pressure:** The economy felt balanced, with a good flow of resources. However, the lack of bank conversions suggests players might prefer other economic strategies.
- **Best moment:** The intense council debate where a motion to increase trade tariffs was narrowly passed by a single vote, leading to significant shifts in player alliances.
- **Biggest friction:** Players often found themselves in conflicting interests during combat, which sometimes led to unexpected betrayals and strained alliances.
- **Would play again:** Yes
- **Hypotheses:** Introducing consequences for broken promises in negotiations could add strategic depth and encourage more reliable diplomacy. | Expanding council dynamics with alliances or议题提案机制 might enhance player engagement and strategy.

### Seed 7692 · Seat 4 · balanced

- **Pacing:** Pacing was steady with a consistent action spread, though the max_action_gap of 4 rounds suggests occasional strategic waiting periods that could affect gameplay dynamics.
- **Map flow:** The game featured significant battles and contested areas, with retreats common, indicating dynamic territorial shifts and cautious player strategies.
- **Politics:** Active council engagement with many motions proposed but few passed highlights a vibrant political landscape marked by debate and indecision.
- **Combat:** Combat was decisive with attackers often prevailing, highlighting the importance of strategic positioning and strength advantages.
- **Economy pressure:** The economy showed moderate pressure with a balanced spread of actions, indicating players managed resources efficiently without extreme scarcity.
- **Best moment:** The final round where Player 1 secured 10 VP through objectives stands out as a pivotal moment, showcasing strategic focus and execution.
- **Biggest friction:** Low utilization of bank conversions and forge recruits suggests potential confusion or underappreciation of these buildings' benefits.
- **Would play again:** Yes
- **Hypotheses:** Player 1's dominance in building construction may indicate a strategic emphasis on infrastructure that could be explored for balance implications. | The low number of market trades might suggest players found other economic strategies more rewarding or effective.

### Seed 7692 · Seat 5 · warmonger

- **Pacing:** The game maintained a steady pace with 7 rounds, allowing for strategic development without dragging.
- **Map flow:** Player 4's control of 12 hexes and Player 3's 11 indicate strong territorial influence, affecting gameplay dynamics.
- **Politics:** Negotiation was frequent but unreliable, with many promises broken, emphasizing cautious alliance-building.
- **Combat:** Attackers had an edge with 7 wins vs. 4 for defenders, though this trend is based on a limited sample of 11 battles.
- **Economy pressure:** Player 3's high gold (41) and Player 5's mana (22) highlight diverse resource strategies.
- **Best moment:** Player 1's decisive victory with 10 VP triggered a 2 VP bonus, solidifying their dominance.
- **Biggest friction:** Players struggled to pass motions in the council, with only 10 successful out of 36 proposed.
- **Would play again:** Yes
- **Hypotheses:** Lord captures significantly impact VP; targeting enemy lords could be a key strategy. | The council's low pass rate suggests that influencing votes is challenging but impactful.

### Seed 7693 · Seat 0 · diplomat

- **Pacing:** Generally smooth with occasional delays due to action gaps, but overall engaging.
- **Map flow:** Active player interaction with frequent motions and offers, though some promises went unkept.
- **Politics:** Dynamic with strategic alliances and broken promises, reflecting a competitive yet collaborative environment.
- **Combat:** Balanced with even wins, but reliance on uncontested captures may reduce strategic depth.
- **Economy pressure:** Uneven building activity suggests some players dominated resource conversion while others focused elsewhere.
- **Best moment:** The intense council negotiations where motions were hotly debated and narrowly passed.
- **Biggest friction:** Disparity in VP gains leading to some players feeling disconnected as others surged ahead.
- **Would play again:** Yes
- **Hypotheses:** Coronation rites significantly impact VP, potentially overshadowing other objectives. | Limited use of Forge and Market might indicate unclear or less rewarding mechanics.

### Seed 7693 · Seat 1 · economist

- **Pacing:** The game maintained steady progress over 6 rounds without significant stalls.
- **Map flow:** Player 4 dominated with 12 controlled hexes and high VP, while others had scattered influence.
- **Politics:** Council dynamics were competitive with motions passed (10) vs. failed (20), showing a challenging legislative environment.
- **Combat:** Combat was balanced with 2 attacker wins vs. 2 defender wins, suggesting strong defensive strategies.
- **Economy pressure:** The economy operated smoothly with an average of 3.07 actions per player round and no stranded AP, indicating efficient resource use.
- **Best moment:** The moment Player 4 secured the Coronation Rite for 3 VP, solidifying their lead.
- **Biggest friction:** The high number of failed motions (20 out of 30) in the council indicated a lack of consensus and made passing beneficial legislation challenging.
- **Would play again:** Yes
- **Hypotheses:** Players may prioritize objectives over building interactions (forge_recruits=0, market_trades=0). | Promises made (2) but not kept (0) could indicate cautious or unreliable diplomacy.

### Seed 7693 · Seat 2 · warmonger

- **Pacing:** The game maintained a steady pace with consistent action counts per round, though max_action_gap indicated occasional downtime for some players.
- **Map flow:** VP sources varied, with some players excelling through objectives while others leveraged coronation milestones, highlighting diverse strategic paths.
- **Politics:** Council dynamics were tense, with high counters and influence spending suggesting active political maneuvering but also potential for gridlock.
- **Combat:** Combat was balanced with equal attacker/defender wins, though some battles were uncontested, suggesting potential for more player engagement in combat scenarios.
- **Economy pressure:** The action economy showed variance, with some players building significantly more than others, indicating diverse strategies but possible imbalance risks.
- **Best moment:** The Coronation Rites mechanic was pivotal in shaping the endgame dynamics, allowing players to secure significant VP through strategic milestones.
- **Biggest friction:** High motion failure rates and broken promises in the council and negotiations created tension and mistrust among players.
- **Would play again:** Yes
- **Hypotheses:** High motion failure rates may reflect a need for clearer council objectives or reduced influence costs to pass motions. | Low promise-keeping rates could indicate a lack of trust or strategic use of deception in negotiations.

### Seed 7693 · Seat 3 · expander

- **Pacing:** Evenly distributed actions and balanced building suggest a strategic focus on resource management.
- **Map flow:** Active negotiation (33 offers proposed, 23 accepted) shows diplomacy efforts, though some promises were broken.
- **Politics:** Low council motion pass rate may indicate opposition or difficulty in gaining support.
- **Combat:** Combat dynamics show that a slight numerical advantage favors attackers, while close battles favor defenders.
- **Economy pressure:** Balanced action economy with moderate influence spending indicates strategic focus on building and objectives.
- **Best moment:** The high VP concentration on objectives and coronation milestones highlights their strategic importance.
- **Biggest friction:** Difficulty in passing council motions (30 proposed, 10 passed) suggests challenges in achieving consensus.
- **Would play again:** Yes
- **Hypotheses:** Players may prioritize objectives over other VP sources due to their reliability. | The coronation milestone could be a key strategy for high VP gains.

### Seed 7693 · Seat 4 · balanced

- **Pacing:** Pacing was steady, though the endgame saw Player 4 surge ahead due to Coronation Rites.
- **Map flow:** The game had a dynamic flow with strategic battles shaping control and influence effectively.
- **Politics:** Negotiation was limited, suggesting either low reliance or ineffective promises among players.
- **Combat:** Combat was balanced with attackers excelling in even matches and defenders holding in uneven ones.
- **Economy pressure:** The economy seemed stable, but the council's low motion success rate hinted at potential contention or inefficiency.
- **Best moment:** The intense battle dynamics where attackers had an edge in balanced conflicts, while defenders held strong in lopsided ones.
- **Biggest friction:** Player 4's dominant VP from Coronation Rites skewed the game balance significantly.
- **Would play again:** Yes
- **Hypotheses:** Coronation Rites may offer too much VP, overshadowing other objectives. | Combat mechanics might encourage aggressive strategies in balanced scenarios. | The council system could be either too challenging for consensus or underutilized.

### Seed 7693 · Seat 5 · warmonger

- **Pacing:** Consistent action counts (avg. 3.07 per round) suggest a well-paced game without significant bottlenecks.
- **Map flow:** Centralized building by Player 4 likely influenced their VP lead, emphasizing the value of strategic hex control.
- **Politics:** Negotiation dynamics with unkept promises highlight trust issues, suggesting strategies for reliability in future games.
- **Combat:** Balanced combat outcomes with 2 attacker and 2 defender wins highlight the importance of strategic positioning and strength assessment.
- **Economy pressure:** No stranded AP indicates efficient resource utilization, but Player 4's building dominance (4/15) underscores economic control's impact on VP.
- **Best moment:** Player 4's decisive victory with 12 VP, securing multiple objectives and Coronation Rites.
- **Biggest friction:** High council motion failure rate (20/30) suggests potential for improved coordination or reduced proposal volume.
- **Would play again:** Yes
- **Hypotheses:** Reducing council motion proposals could increase passage rates and player satisfaction. | Encouraging more Coronation Rite participation might balance VP distribution.

### Seed 7694 · Seat 0 · diplomat

- **Pacing:** The game maintained a steady pace without significant delays, though the avg_action_gap of 2.43 suggests occasional waiting periods between player actions.
- **Map flow:** Player 1 dominated building construction with 7 buildings, significantly outpacing others. This concentration could influence future game dynamics by creating economic or strategic advantages early on.
- **Politics:** Negotiation saw limited success with only 16 offers accepted out of 46 proposed. This indicates challenges in reaching agreements, potentially due to competitive pressures or mistrust among players.
- **Combat:** Combat was heavily skewed towards attackers, who won 8 out of 9 battles. The lone defender victory highlights potential for strategic defense improvements.
- **Economy pressure:** The economy showed moderate action distribution with an average of 3.14 actions per player round, but some players (like player 3 and 5) underperformed in building construction, indicating possible economic stagnation or strategic focus elsewhere.
- **Best moment:** The final round was particularly intense as players scrambled to secure their last objectives, with player 5 emerging victorious with a decisive 12 VP.
- **Biggest friction:** Players experienced difficulty in passing motions through the council, with only 5 motions passed out of 42 proposed. This suggests challenges in collaboration or dominance dynamics.
- **Would play again:** Yes
- **Hypotheses:** The council's low motion passage rate may indicate a need for revised voting mechanics to encourage more constructive collaboration. | Combat mechanics might benefit from adjustments to balance attacker and defender outcomes more evenly.

### Seed 7694 · Seat 1 · economist

- **Pacing:** The game maintained a steady pace with an average of 3.14 actions per player round, indicating balanced engagement without overwhelming any participant.
- **Map flow:** Player 5's control of 10 hexes and high VP suggests effective territorial management and objective achievement, possibly leveraging strategic locations for resource advantage.
- **Politics:** With only 5 motions passed out of 42 proposed, council effectiveness was low. This could indicate challenges in consensus-building or a preference for unilateral action among players.
- **Combat:** Attackers dominated with an 89% win rate, suggesting that aggressive strategies are rewarded. However, the lone defender victory highlights opportunities for strategic defense when resources permit.
- **Economy pressure:** The economy showed disparities, with Player 1 leading in builds (7) while others lagged, impacting their resource generation and VP potential.
- **Best moment:** The final round where Player 5 secured 12 VP through objectives stands out as a pivotal moment, showcasing their strategic focus and execution.
- **Biggest friction:** Players 3 and 5 had limited influence (2 and 0 respectively), indicating potential disengagement or challenges in participating effectively in council decisions.
- **Would play again:** Yes
- **Hypotheses:** High attacker success rate may encourage early aggressive play, potentially skewing game dynamics towards offensive strategies. | Low council motion passage could reflect either ineffective proposals or a fragmented player base, warranting further exploration in future games.

### Seed 7694 · Seat 2 · warmonger

- **Pacing:** The game maintained a steady pace with no significant delays or bottlenecks.
- **Map flow:** Player 5's control of 8 hexes and 6 buildings contributed significantly to their victory.
- **Politics:** Negotiation was frequent but challenging, with many offers rejected and only one promise broken.
- **Combat:** Attackers had a significant advantage, winning 8 out of 9 battles.
- **Economy pressure:** The economy was active with an average of 3.14 actions per player round and no stranded AP.
- **Best moment:** The final round was intense with player 5 securing a dominant victory by reaching 12 VP.
- **Biggest friction:** Players struggled to pass motions in the council, with only 5 passing out of 42 proposed.
- **Would play again:** Yes
- **Hypotheses:** Defense mechanics may need strengthening to balance the high attacker win rate. | Influence costs in the council might be too high, leading to low motion success rates.

### Seed 7694 · Seat 3 · expander

- **Pacing:** The game maintained a steady pace with consistent VP accumulation, peaking in the final round as per rules.
- **Map flow:** Uncontested captures and retreats (4 and 2 respectively) point to strategic territorial expansions without significant resistance.
- **Politics:** Frequent offers and rejections in negotiations (46 proposed, 30 rejected) suggest a competitive political landscape with trust issues from broken promises.
- **Combat:** Attackers dominated combat, winning 8 out of 9 battles, indicating strategic advantages when strength was sufficient.
- **Economy pressure:** High gold reserves among some players (e.g., Seraphel with 40 gold) suggest economic pressures or hoarding strategies.
- **Best moment:** Player 5's decisive victory with 12 VP highlights a dominant performance in objective achievement.
- **Biggest friction:** The council's inefficiency, with only 5 motions passed out of 42 proposed, suggests challenges in collaborative governance.
- **Would play again:** Yes
- **Hypotheses:** The council's low success rate may indicate either poor proposal quality or strong opposition dynamics.

### Seed 7694 · Seat 4 · balanced

- **Pacing:** Average actions per player round of ~3.14 and no stranded APs suggest a well-paced game without bottlenecks.
- **Map flow:** Controlled hexes varied widely (7-11), suggesting diverse territorial strategies among players.
- **Politics:** High influence spending (36) and low motion passage indicate intense political maneuvering.
- **Combat:** Combat was decisive with attackers winning 8 of 9 battles, highlighting the effectiveness of offensive strategies.
- **Economy pressure:** No stranded APs indicate a smooth economy flow, supporting active gameplay throughout.
- **Best moment:** The final round saw player 5 surge ahead with 12 VP, creating a dramatic conclusion.
- **Biggest friction:** Low council motion passage rate (5/42) suggests potential for改进 in the council system's balance.
- **Would play again:** Yes
- **Hypotheses:** Low council motion passage rate may reflect strategic voting patterns rather than system imbalance. | Player 5's high VP could be due to effective objective scoring or advantageous positioning.

### Seed 7694 · Seat 5 · warmonger

- **Pacing:** The game maintained steady progression without significant stalls, though the council's low effectiveness could indicate pacing issues in later rounds.
- **Map flow:** Player 5's control of 8 hexes with no buildings suggests a focus on territorial dominance over economic infrastructure, a strategy that proved highly effective.
- **Politics:** Player 1's high influence (7) and renown (1) highlight their political prowess. However, the council's inefficiency suggests that players may need better tools to leverage influence effectively.
- **Combat:** Attackers dominated with an 89% win rate, underscoring the game's bias towards offensive play. This trend supports a warmonger strategy focused on aggressive expansion and targeting weaker opponents.
- **Economy pressure:** Player 3's high gold (40) and pop pool (10) indicate potential economic pressures or strategic choices that others didn't leverage effectively.
- **Best moment:** The final round where player 5 secured an overwhelming 12 VP from objectives stands out as a pivotal moment. This dominance highlights the importance of objective control in Aeonis.
- **Biggest friction:** The council's ineffectiveness, with only 5 motions passing, suggests that players either struggle to collaborate or prioritize other strategies over council influence.
- **Would play again:** Yes
- **Hypotheses:** The council system may need adjustments to encourage more successful motions, fostering a balance between competition and collaboration. | Objective VP concentration might be too high; distributing VP sources could create a more dynamic endgame.

### Seed 7695 · Seat 0 · diplomat

- **Pacing:** The game maintained a steady pace, with no significant delays or bottlenecks, allowing for strategic progression throughout the rounds.
- **Map flow:** Player 1 dominated with 9 builds, likely controlling key areas and influencing the game flow towards their objectives.
- **Politics:** Negotiation was active but trust issues arose, as evidenced by broken promises (4), affecting alliance reliability.
- **Combat:** Combat was impactful, with attackers winning 5 out of 7 battles, suggesting that offensive strategies were more rewarding.
- **Economy pressure:** The economy showed moderate pressure, with a consistent average of 3.33 actions per player round and limited stranded AP, indicating efficient resource use.
- **Best moment:** The decisive battle where Player 1 captured a contested hex with a narrow margin, securing a significant VP gain.
- **Biggest friction:** The low passage rate of council motions (5/36) indicated difficulty in reaching consensus, potentially hindering strategic coordination.
- **Would play again:** Yes
- **Hypotheses:** The high number of failed motions (31) may reflect a fragmented council dynamic, affecting players' ability to collaborate effectively.

### Seed 7695 · Seat 1 · economist

- **Pacing:** Game pacing was steady with no significant delays, though the max action gap of 7 suggests occasional waiting periods that could be smoothed.
- **Map flow:** The map was evenly contested with uncontested captures and retreats, suggesting dynamic territorial shifts without overwhelming dominance by any player.
- **Politics:** The council proved ineffective with only 5 motions passing. High influence spending but low passage rates may indicate resistance to collaboration or a need for more incentives.
- **Combat:** Combat was highly decisive with attackers winning 71% of battles. However, when defenders had stratagems, they failed to secure any wins, suggesting a possible imbalance in defender mechanics.
- **Economy pressure:** The economy showed moderate pressure with an average of 3.33 actions per player round and low stranded AP, indicating efficient resource use but potential for further optimization.
- **Best moment:** The final round saw Player 1 secure a decisive victory by achieving 10 VP through objectives alone. This highlights the effectiveness of focusing on objective-based strategies.
- **Biggest friction:** Players 2 and 3 built no structures throughout the game, indicating potential disengagement or resource allocation challenges that may warrant further investigation.
- **Would play again:** Yes
- **Hypotheses:** Low building activity from some players may reflect disengagement or strategic oversight. | Defenders' inability to win stratagem battles could indicate a need for balance adjustments.

### Seed 7695 · Seat 2 · warmonger

- **Pacing:** Game pacing was consistent with an average of 3.33 actions per player round, but some rounds had higher action gaps, suggesting potential for more dynamic gameplay.
- **Map flow:** The map flow was dominated by Player 1, who controlled the most hexes and objectives, leading to their high VP score.
- **Politics:** Politics were tense due to broken promises and low trust among players, affecting negotiation dynamics.
- **Combat:** Combat was biased towards attackers, with all uncontested battles won by them. This might encourage an aggressive playstyle.
- **Economy pressure:** The economy felt pressured due to low builds per player, averaging around 2-3 buildings each.
- **Best moment:** The decisive battle where Player 1 captured a key objective, securing their victory.
- **Biggest friction:** Players found the council motions system confusing and ineffective, with only 5 out of 36 motions passing.
- **Would play again:** Yes
- **Hypotheses:** Low council motion passage rate may indicate a need for clearer rules or more incentives for collaboration. | Combat bias towards attackers could be balanced by adjusting strength ratios or introducing defensive bonuses.

### Seed 7695 · Seat 3 · expander

- **Pacing:** The game maintained a steady pace with an average of 3.33 actions per player round, indicating smooth gameplay flow.
- **Map flow:** The map was evenly contested with multiple players controlling around 9-10 hexes each, showing balanced territorial gains.
- **Politics:** Council dynamics were tense with few motions passing, highlighting challenges in forming coalitions.
- **Combat:** Combat was frequent with 7 battles, but the low number of uncontested captures (3) suggests strong defense strategies.
- **Economy pressure:** The economy saw high influence spending (34 total), indicating active political maneuvering.
- **Best moment:** The final round when Player 1 reached 10 VP with their objectives was a pivotal moment.
- **Biggest friction:** Players struggled to pass council motions, with only 5 passed out of 36 proposed.
- **Would play again:** Yes
- **Hypotheses:** High influence spending may indicate a need for more efficient ways to convert influence into tangible benefits. | Low market trades and forge recruits suggest underutilized economic opportunities.

### Seed 7695 · Seat 4 · balanced

- **Pacing:** 7 rounds with average actions per player round, indicating a balanced pace.
- **Map flow:** Game flow was steady with manageable action gaps and spreads.
- **Politics:** Council system underutilized; only 5 motions passed out of 36 proposed.
- **Combat:** Attackers had an edge in contested battles, suggesting defense may be underpowered.
- **Economy pressure:** High building counts for some players indicate potential resource allocation issues.
- **Best moment:** The final round where Player 1 reached 10 VP, triggering a canon change discussion.
- **Biggest friction:** Building disparity among players; Player 1 built significantly more than others.
- **Would play again:** Yes
- **Hypotheses:** Player 1's high VP might be a fluke due to small sample size. | Building disparity could signal an imbalance in resource distribution.

### Seed 7695 · Seat 5 · warmonger

- **Pacing:** The game concluded quickly at Round 7 due to Player 1's VP trigger, suggesting efficient gameplay.
- **Map flow:** Player 1's objective control was central, while others struggled to convert resources into VP.
- **Politics:** Council contention and negotiation challenges highlight the need for stronger alliances or intimidation tactics.
- **Combat:** Combat was decisive with 5 attacker wins vs. 2 defender wins in 7 battles, favoring aggressive strategies.
- **Economy pressure:** Player 1's economy dominated with 9 buildings, while Player 4 underperformed with fewer VP despite similar builds.
- **Best moment:** Player 1's aggressive building strategy leading to 10 VP via objectives, triggering the final-round condition.
- **Biggest friction:** Low council motion passage rate (5/36) and high promise-breaking (4/4), indicating contentious gameplay.
- **Would play again:** Yes
- **Hypotheses:** High promise-breaking may reflect trust issues; more enforcement could stabilize negotiations. | Low whisper usage (2/103) might indicate limited strategic impact or player unfamiliarity.

## Candidate rules questions

These are triage inputs, not automatic canon or Ambiguity Ledger entries.

- Seed 7690, seat 4, round post-game: Why were there no bank conversions or market trades despite active gameplay?
- Seed 7690, seat 4, round post-game: What factors contribute to the low success rate of council motions?
- Seed 7690, seat 5, round 2: Is the future_payment due_round correctly set to 3?
- Seed 7690, seat 5, round post-game: Is there clarity on how to handle promise-breaking in negotiations?
- Seed 7690, seat 5, round post-game: Could the council mechanics be adjusted to encourage more successful motions?
- Seed 7691, seat 1, round 2: nil
- Seed 7691, seat 1, round post-game: Clarify the exact steps for scoring objectives at game end, especially regarding overlapping VP sources.
- Seed 7691, seat 1, round post-game: Provide examples of proper Coronation Rites application to avoid confusion in future games.
- Seed 7691, seat 5, round post-game: Why did no motions pass despite influence spent?
- Seed 7691, seat 5, round post-game: How to prevent single-player dominance in building?
- Seed 7692, seat 0, round 2: Does the future_payment count against my current Influence? Clarification needed on whether this affects my lobbying capacity in future rounds.
- Seed 7692, seat 4, round post-game: Clarification on the effectiveness of bank conversions and forge recruits in game strategy.
- Seed 7692, seat 5, round 2: , but I need to ensure this aligns with council rules and doesn't violate any hidden terms.
- Seed 7693, seat 4, round 2: , but I'm unclear on how exactly the movement and attack costs are adjusted with this strategy.
- Seed 7695, seat 1, round post-game: Why did some players achieve VP through varied sources while others relied solely on objectives?
- Seed 7695, seat 1, round post-game: Is the council's ineffectiveness by design, or does it reflect a mechanical imbalance?
- Seed 7695, seat 2, round post-game: Clarification on the definition of 'contested' vs. 'uncontested' battles in combat stats.
- Seed 7695, seat 2, round post-game: Understanding how Coronation Rites contribute to VP and ensuring players are aware of this mechanic.

## Decision moments

- Seed 7690, seat 0, round 2 (negotiation): highlight=vote_agreement. friction=f0.
- Seed 7690, seat 1, round 2 (action): highlight=Using 'tactical_reinforcements' to recruit units strategically increases military strength while efficiently utilizing available resources.
- Seed 7690, seat 2, round 2 (action): highlight=Attacking is a direct way to weaken opponents and gain battlefield advantage as a warmonger.
- Seed 7690, seat 3, round 2 (council_vote): highlight=Opposing the motion is the safer play as I cannot influence others and my objective doesn't align with this proposal.
- Seed 7690, seat 4, round 2 (action): highlight=Played 'military_maneuvers' strategy card to enhance unit mobility and attack capability.
- Seed 7690, seat 5, round 2 (negotiation): highlight=vote_bargain. friction=I need your vote to pass this crucial motion. In exchange, I'll ensure you receive a steady gold flow in the coming rounds. It's a win-win.
- Seed 7691, seat 0, round 2 (negotiation): highlight=I propose a vote bargain with Player 1: in exchange for their support on imperial_annexation, I will pay them 1 gold in round 3. This is a fair trade that benefits both of us. friction=, but I need more resources to secure their support.
- Seed 7691, seat 1, round 2 (action): highlight=Yes. friction=No apparent ambiguity in rules.
- Seed 7691, seat 2, round 2 (action): highlight=Playing tactical_reinforcements allows recruiting up to 2 units for 1 AP, efficiently increasing military strength.
- Seed 7691, seat 3, round 2 (council_vote): highlight=Supporting the motion without lobbying is chosen as it directly contributes towards its passage, aligning with potential strategic goals despite limited Influence.
- Seed 7691, seat 4, round 2 (action): highlight=Playing resource_surge as a Primary Action is optimal for gaining immediate resources without AP cost.
- Seed 7691, seat 5, round 2 (negotiation): highlight=I will secure your vote with a modest future payment, ensuring our victory in the council.
- Seed 7692, seat 0, round 2 (negotiation): highlight=Player 2's support is crucial, and this bargain ensures their vote with a manageable future cost. friction=I need to secure votes for the border_arbitration motion. Player 2 has significant influence and would be a valuable ally. Offering them a future payment aligns our interests and strengthens our position in the council.
- Seed 7692, seat 1, round 2 (action): highlight=Played 'arcane_ascendancy' for 1 AP: gained 2 Mana (total 7) and researched a Tier I discovery free. This efficiently increases resources and unlocks future options.
- Seed 7692, seat 2, round 2 (action): highlight=Moving to [0,-1] positions the unit strategically for future attacks while conserving AP.
- Seed 7692, seat 3, round 2 (council_vote): highlight=Supporting with lobbying maximizes influence towards passing border_arbitration, aligning with expansion goals.
- Seed 7692, seat 4, round 2 (action): highlight=Played 'military_maneuvers' strategy card for efficient movement and attack, aligning with borderbreaking objective.
- Seed 7692, seat 5, round 2 (negotiation): highlight=I propose a vote bargain with Player 4: they support border_arbitration, and I promise them 1 gold by Round 3. This secures their vote while keeping my costs low. friction=, but I need to secure votes for strategic advantage.
- Seed 7693, seat 1, round 2 (action): highlight=Immediate resource gain with no cost. friction=No apparent ambiguity; straightforward choice.
- Seed 7693, seat 2, round 2 (action): highlight=As a warmonger, I prioritize aggressive actions to weaken opponents and gain control. Attacking the target at [-3,4] is strategically beneficial as it can disrupt enemy plans and strengthen my position.
- Seed 7693, seat 3, round 2 (council_vote): highlight=As player 3, supporting the demilitarized zone motion with lobbying is strategically advantageous. Spending 2 Influence to sway another vote increases the likelihood of achieving a strict majority, ensuring the motion's passage and advancing my objectives.
- Seed 7693, seat 4, round 2 (action): highlight=I choose to play the 'military_maneuvers' strategy card for its ability to enhance movement and attack efficiency, providing a strategic advantage in positioning units and executing attacks effectively. friction=, but I'm not sure if this is the best use of my AP given other options.
- Seed 7694, seat 0, round 2 (negotiation): highlight=resource_trade. friction=calm.
- Seed 7694, seat 1, round 2 (action): highlight=Using 'tactical_reinforcements' to recruit two units for free is strategically advantageous as it allows Player 1 to strengthen their forces without resource expenditure, enhancing their position on the board. friction=0.
- Seed 7694, seat 2, round 2 (action): highlight=Moving units closer to enemy territories positions them for potential combat, aligning with the warmonger strategy of seeking conflict and dominance.
- Seed 7694, seat 3, round 2 (council_vote): highlight=Player 3 has no influence to lobby but can still vote against the motion to prevent it from passing, aligning with their secret objective of maintaining a hidden arsenal. This strategic choice aims to keep power dynamics favorable without expending resources.
- Seed 7694, seat 4, round 2 (action): highlight=Using 'arcane_ascendancy' gains 2 Mana and allows free research of a Tier I discovery, enhancing flexibility for future actions.
- Seed 7695, seat 0, round 2 (negotiation): highlight=I propose a vote bargain with Player 2: they support my motion, and I'll pay them 1 gold in round 3. friction=, but let's see if we can make this work.
- Seed 7695, seat 1, round 2 (action): highlight=Played economic_boom to gain 5 Gold.
- Seed 7695, seat 2, round 2 (action): highlight=Attacking Player 0's unit at [-3, 0] is a strategic move to weaken their forces and gain control of the hex.
- Seed 7695, seat 3, round 2 (council_vote): highlight=Spend Influence to Support Motion. friction=, but it's uncertain if others will follow.
- Seed 7695, seat 4, round 2 (action): highlight=Playing 'imperial_mandate' for VP or a secret card plus Influence. friction=No apparent frustration.

---

Model feedback is directional sim-only evidence. It does not replace human table play or promote rules to canon.
