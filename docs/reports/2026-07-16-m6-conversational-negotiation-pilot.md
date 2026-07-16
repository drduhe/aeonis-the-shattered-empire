# Aeonis M6 Conversational Negotiation Pilot

Games: **1** · Qualitative seats: **3** · Providers: ollama

## M6 audit

- **Conversation path passed:** 24/24 sampled negotiation decisions produced valid engine-bounded choices and public messages, with zero retries or fallbacks.
- **Deals formed:** 17 proposals produced 15 acceptances and 10 counters. The acceptance rate is an observation from one politics-heavy game, not a tuning target.
- **Promises diverged by kind:** all 7 logged vote promises were kept; all 4 future-payment promises expired unpaid and were marked broken.
- **Important prose/terms finding:** several counteroffer messages described vote support even when the indexed counter had become a resource-only trade. The engine correctly used the structured terms, but future reports now print an authoritative term snapshot beside each utterance so this mismatch is visible.
- **Coverage limit:** the model decision budget was consumed by Council bargaining. Paid non-aggression, mutual non-aggression, and named attack contracts are implemented and covered by automated tests, but this pilot did not exercise them in live play.
- **No canon promotion:** this validates the M6 interaction pipeline. It does not establish balance, trust dynamics, or the right frequency of deals.

## Game facts

| Seed | Rounds | Final VP | Battles (attacker wins) | Council passed/proposed | Deals accepted/proposed |
| ---: | ---: | --- | ---: | ---: | ---: |
| 7616 | 4 | {0: 6, 1: 2, 2: 10} | 2 (2) | 5/9 | 15/17 |

> Treat one-game and low-battle observations as prompts for replication, not balance conclusions.

## Reliability

| Seat-game | Provider calls | Decision attempts | Valid decisions | Persona delegations | Retries | Decision fallbacks | Qualitative failures | Model seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| seed 7616 / seat 0 (warmonger) | 9 | 8 | 8 | 48 | 0 | 0 | 0 | 173.593 |
| seed 7616 / seat 1 (economist) | 9 | 8 | 8 | 46 | 0 | 0 | 0 | 117.11 |
| seed 7616 / seat 2 (diplomat) | 9 | 8 | 8 | 53 | 0 | 0 | 0 | 127.095 |

### Provider diagnostics

- No provider errors recorded.

## Round reflections

- No round reflections requested.

## Negotiation transcript

- Seed 7616, round 1, seat 0 (negotiation_propose, vote_bargain): I propose a bargain: if you support the road_networks motion, I will pay you 1 gold in round 2.
- Seed 7616, round 1, seat 2 (negotiation_accept, vote_bargain): I agree to support the road_networks motion in exchange for 1 gold in round 2. This arrangement suits both of us well.
- Seed 7616, round 1, seat 2 (negotiation_propose, vote_bargain): Player 2 offers Player 1: If you support 'road_networks', I will pay you 1 gold in round 2.
- Seed 7616, round 1, seat 1 (negotiation_counter, resource_trade): Player 1 counters Player 2's offer: I will support 'road_networks' if you pay me 1 gold in round 2.
- Seed 7616, round 1, seat 2 (negotiation_accept, resource_trade): Player 2 accepts Player 1's counter: I will support 'road_networks' if you pay me 1 gold in round 2.
- Seed 7616, round 1, seat 1 (negotiation_propose, vote_agreement): I propose a vote agreement with Player 0 to support road_networks. This simple agreement aligns our interests without immediate cost, ensuring we can pass the motion together.
- Seed 7616, round 1, seat 0 (negotiation_accept, vote_agreement): I accept your proposal. Aligning our votes ensures we can pass road_networks together without immediate cost, keeping our options open for future moves.
- Seed 7616, round 1, seat 0 (negotiation_propose, vote_bargain): Player 2, let's secure the future. Support road_networks, and I'll ensure you receive 1 gold by round 2.
- Seed 7616, round 1, seat 2 (negotiation_accept, vote_bargain): Player 0, I agree to support road_networks in exchange for your promise of 1 gold by round 2. Let's move forward together.
- Seed 7616, round 1, seat 2 (negotiation_propose, vote_bargain): I agree to support your motion on road networks in exchange for a future payment of 1 gold in round 2. This arrangement benefits both parties and ensures mutual support.
- Seed 7616, round 1, seat 0 (negotiation_counter, resource_trade): I accept the support for road networks but propose exchanging 1 gold for 1 mana instead.
- Seed 7616, round 1, seat 2 (negotiation_reject, resource_trade): I must respectfully decline this counteroffer. The original agreement for a future payment of gold remains the most straightforward and mutually beneficial arrangement.
- Seed 7616, round 1, seat 1 (negotiation_propose, vote_bargain): Player 0, I propose a vote bargain. In exchange for your support on the road_networks motion, I will pay you 1 gold in round 2.
- Seed 7616, round 1, seat 0 (negotiation_accept, vote_bargain): Player 1, I accept your proposal. Your support for road_networks is secured, and I look forward to receiving the gold in round 2. This alliance strengthens our position in the council.
- Seed 7616, round 1, seat 0 (negotiation_propose, vote_bargain): Player 0 to Player 2: I propose a vote bargain. You support the 'road_networks' motion, and I promise you 1 gold in Round 2. Let's strengthen our infrastructure together.
- Seed 7616, round 1, seat 2 (negotiation_accept, vote_bargain): Player 2 accepts Player 0's vote bargain. I will support 'road_networks' in exchange for 1 gold in Round 2.
- Seed 7616, round 1, seat 2 (negotiation_propose, vote_bargain): Player 1, I propose a bargain: in exchange for your support on 'road_networks', I will pay you 1 gold by Round 2. This benefits both of us as we can advance our objectives together.
- Seed 7616, round 1, seat 1 (negotiation_counter, resource_trade): Player 2, I counter your proposal. Instead of paying me gold, let's trade: you give me 1 mana for my 1 gold. This keeps our resources balanced while securing the vote.
- Seed 7616, round 1, seat 1 (negotiation_propose, vote_agreement): Player 1 proposes a vote agreement: I will support your motion if you support mine.
- Seed 7616, round 2, seat 1 (negotiation_propose, vote_bargain): Player 0, I propose that you support my border_arbitration motion, and in return, I will pay you 1 gold in round 3. This is a strategic exchange that benefits both of us.
- Seed 7616, round 2, seat 0 (negotiation_counter, resource_trade): Player 1, I accept your proposal to support border_arbitration in exchange for 1 gold in round 3. This is a fair and strategic arrangement that aligns our interests.
- Seed 7616, round 2, seat 1 (negotiation_reject, resource_trade): Player 1, I reject your counterproposal. This arrangement does not align with my strategic interests at this time.
- Seed 7616, round 2, seat 0 (negotiation_counter, resource_trade): I counter with a trade: 1 mana for 1 gold. Support border_arbitration in exchange.
- Seed 7616, round 2, seat 1 (negotiation_propose, vote_agreement): I propose a vote agreement with Player 2: they support border_arbitration, I reciprocate. This secures our position without unnecessary expenditure.

### Promise outcomes

- Seed 7616: vote from seat 2 to seat 0 — kept (vote_cast).
- Seed 7616: future_payment from seat 0 to seat 2 — broken (payment_not_transferred).
- Seed 7616: vote from seat 0 to seat 1 — kept (vote_cast).
- Seed 7616: vote from seat 2 to seat 0 — kept (vote_cast).
- Seed 7616: future_payment from seat 0 to seat 2 — broken (payment_not_transferred).
- Seed 7616: vote from seat 0 to seat 1 — kept (vote_cast).
- Seed 7616: future_payment from seat 1 to seat 0 — broken (payment_not_transferred).
- Seed 7616: vote from seat 2 to seat 0 — kept (vote_cast).
- Seed 7616: future_payment from seat 0 to seat 2 — broken (payment_not_transferred).
- Seed 7616: vote from seat 2 to seat 1 — kept (vote_cast).
- Seed 7616: vote from seat 2 to seat 1 — kept (vote_cast).

## Exit interviews

### Seed 7616 · Seat 0 · warmonger

- **Pacing:** The game maintained steady pacing with no stranded action points and consistent rounds, contributing to smooth gameplay progression.
- **Map flow:** Player 2 dominated with 10 VP and controlled 8 hexes, suggesting a strong focus on territorial control and objective achievement early in the game.
- **Politics:** Council dynamics showed collaboration with more yes votes than no, despite motions failing. This might reflect a tendency towards agreement or strategic voting patterns.
- **Combat:** Combat was decisive but brief, with all battles resulting in uncontested captures and attacker victories. This suggests that combat mechanics led to quick resolutions without prolonged resistance.
- **Economy pressure:** The action economy remained balanced with an average of 3.56 actions per player round and low spread, indicating even distribution. Player 1's higher building count may offer future strategic advantages.
- **Best moment:** The final round where Player 2 secured an overwhelming 10 VP through objectives stands out as a pivotal moment, showcasing their strategic focus on achieving game goals.
- **Biggest friction:** Players faced challenges with negotiation commitments, as evidenced by more promises broken than kept, indicating potential difficulties in fulfilling agreements within the game's constraints.
- **Would play again:** Yes
- **Hypotheses:** The game length might have limited exploration of victory paths beyond objectives, as VP sources were entirely from objectives. | Low influence spent in council motions despite high proposals could indicate either collaborative play or strategic saving of influence.

### Seed 7616 · Seat 1 · economist

- **Pacing:** Fast-paced with 4 rounds completed, no delays noted.
- **Map flow:** Active political play with motions proposed (9), votes cast (27), and offers exchanged (32).
- **Politics:** High engagement in council and negotiation mechanics, with promise-keeping (7/11) indicating moderate trust.
- **Combat:** Uncontested battles (2 total) indicate limited combat engagement; all attacker wins may suggest asymmetric power dynamics.
- **Economy pressure:** Balanced economy with average actions per player round (3.56), no stranded AP, and moderate spread (0.67).
- **Best moment:** The decisive final-round victory point trigger for Player 2 with 10 VP, achieved through objective completion.
- **Biggest friction:** Low influence spent (4 total) relative to motions proposed (9), suggesting potential disengagement or imbalance in council mechanics.
- **Would play again:** Yes
- **Hypotheses:** The high number of future payment promises broken (4) may correlate with mistrust or miscalibration in negotiation dynamics. | Player 1's higher building count (4) did not translate to VP dominance, suggesting alternative victory paths.

### Seed 7616 · Seat 2 · diplomat

- **Pacing:** The game maintained a steady pace with moderate action usage, suggesting balanced player strategies but no significant bottlenecks.
- **Map flow:** The map dynamics were influenced by Player 2's strong objective performance, while others focused on building and resource control.
- **Politics:** Council dynamics were active, with motions reflecting strategic priorities. The high number of offers and promises kept indicates effective negotiation but may also point to underenforced commitments.
- **Combat:** Combat was decisive, with attackers winning both battles. However, limited combat instances (2) suggest a cautious approach to conflict or imbalanced incentives for engagement.
- **Economy pressure:** The economy operated smoothly with no stranded AP, indicating efficient resource management but potentially underutilized strategic opportunities.
- **Best moment:** The final round's VP distribution, with Player 2 securing 10 VP from objectives alone, highlights the need for objective balance and player engagement strategies.
- **Biggest friction:** The uneven VP distribution raises concerns about objective strength and player access to critical resources or opportunities.
- **Would play again:** Yes
- **Hypotheses:** Objective strength may disproportionately favor certain players, skewing VP distribution. | Influence spending patterns suggest either conservative use or limited impact on game outcomes.

## Candidate rules questions

These are triage inputs, not automatic canon or Ambiguity Ledger entries.

- Seed 7616, seat 2, round 1: Is accepting a future payment for vote support within the allowed negotiation actions?
- Seed 7616, seat 2, round 1: Is changing the deal kind allowed during a counteroffer?
- Seed 7616, seat 2, round post-game: Clarification on objective scoring criteria to ensure balanced access.
- Seed 7616, seat 2, round post-game: Investigation into influence spending mechanics to assess impact.

## Decision moments

- Seed 7616, seat 0, round 1 (negotiation): friction=0.
- Seed 7616, seat 0, round 1 (negotiation): highlight=Accepting the vote agreement allows us to pass the road_networks agenda without cost, ensuring our interests align while preserving resources for other strategic opportunities.
- Seed 7616, seat 0, round 1 (negotiation): highlight=I propose a vote bargain with Player 2: they support road_networks, and I pay them 1 gold in round 2. friction=, but let's make this clear: I need your vote to pass road_networks, which will benefit us all by improving infrastructure for military movements. In return, I promise 1 gold in round 2.
- Seed 7616, seat 0, round 1 (negotiation): highlight=I propose a trade where you receive 1 gold in exchange for 1 mana. This allows me to strengthen my economy while supporting your motion. friction=, but I need to secure resources for my military campaigns.
- Seed 7616, seat 0, round 1 (negotiation): highlight=Accept. friction=I need that gold to fund my expansion and military buildup. Accepting the deal secures me resources while maintaining my influence in the council.
- Seed 7616, seat 0, round 1 (negotiation): highlight=I propose a vote bargain with Player 2: they will support 'road_networks,' and I will pay them 1 gold in Round 2. This secures their vote while managing our resources effectively.
- Seed 7616, seat 1, round 1 (negotiation): highlight=I will support your motion in exchange for receiving 1 gold in round 2.
- Seed 7616, seat 1, round 1 (negotiation): highlight=vote_bargain with Player 0. friction=, I'm willing to offer you 1 gold next round for your support.
- Seed 7616, seat 1, round 1 (negotiation): highlight=I propose a vote agreement with Player 2 to secure their support for the road_networks motion. This straightforward deal aligns our interests without additional costs, ensuring we can pass the agenda efficiently. friction=, but I'm confident in this strategic move.
- Seed 7616, seat 1, round 2 (negotiation): highlight=I propose a vote bargain with Player 0: I will pay them 1 gold in round 3 if they support my border_arbitration motion. This is a fair trade for their crucial vote.
- Seed 7616, seat 1, round 2 (negotiation): highlight=reject.
- Seed 7616, seat 1, round 2 (negotiation): highlight=vote_agreement. friction=0.
- Seed 7616, seat 2, round 1 (negotiation): highlight=accept. friction=I'm inclined to accept this proposal as it aligns with my interests and maintains simplicity in our negotiation.
- Seed 7616, seat 2, round 1 (negotiation): highlight=I offer Player 1 a future payment to support road_networks, ensuring our proposal passes. friction=, but I must ensure we secure enough votes.
- Seed 7616, seat 2, round 1 (negotiation): friction=, but I think we're on the same page here.
- Seed 7616, seat 2, round 1 (negotiation): highlight=vote_bargain with future_payment for road_networks support.
- Seed 7616, seat 2, round 1 (negotiation): highlight=Reject. friction=:thinking:.
- Seed 7616, seat 2, round 1 (negotiation): highlight=, so accepting ensures future gold and supports infrastructure. friction=, but I'm not sure if changing the deal kind is allowed during a counteroffer.
- Seed 7616, seat 2, round 1 (negotiation): highlight=future_payment. friction=factual.

---

Model feedback is directional sim-only evidence. It does not replace human table play or promote rules to canon.
