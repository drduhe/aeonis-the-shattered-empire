# Ambiguity Ledger

Rules questions found while encoding the docs into the simulator
(`sim/`). Each entry: the question, the interpretation the engine uses, and
the doc that should own the canonical answer. Triage by either patching the
owning doc (then the engine) or accepting the engine interpretation into
canon.

**Milestone-1 fuzz baseline (100 chaos games, seeds 1000-1099):** `verdicts: {'completed': 98, 'degenerate': 2}`

| ID | Question | Engine interpretation | Owning doc | Status |
|---|---|---|---|---|
| AL-1 | Packet §3.3 says starting Pop Cap 10, but `Population.md` grants +3 cap per City — a starting player (1 City) would exceed 10 with any base ≥ 8. What is the base cap? | Base cap 7, so 1 starting City yields exactly 10 | `Population.md` | Open |
| AL-2 | Movement cost of Ruins hexes is undefined in `Movement.md` §2 | 1 AP (treated as easy terrain) | `Movement.md` | Open |
| AL-3 | (Sim fidelity, not rules) Deserts placed by shuffle, not "between each pair of home clusters" | Positional flavor only in M1 | `First_Playable_Packet.md` | Sim-only |
| AL-4 | Packet §3.3 says "Population Pool: 10 (full at start)" but starting units occupy 4 Population — is the pool 10 or 6? | Starting units consume Population: pool 6 of cap 10 | `First_Playable_Packet.md` | Open |
| AL-5 | When are objectives claimed/scored? No timing window in packet §4.4 or `Victory.md` | Auto-scored at Cleanup & Checks, once per card | `Victory.md` | Open |
| AL-6 | Does building a Bridge on a neutral Lake grant control of the Lake hex? | Yes — builder controls the bridged Lake | `Tiles.md` | Open |
| AL-7 | (Sim bound) Defender choice to Hold the Walls for Cities | M1 auto-declares Hold the Walls (strictly better: City retreat is banned anyway) | `Combat.md` | Sim-only |
| AL-8 | What happens when Castle upkeep (2 Gold) cannot be paid? `Trade_Taxes.md`/`Buildings.md` don't say | Castle effects suspended for the round; building persists | `Buildings.md` | Open |
| AL-9 | Lord release "returns to Home City" — what if the Home City is enemy-held or contains enemy units? | Returns to nearest controlled hex without enemy units; stays captured another round if none | `Combat.md` | Open |
| AL-10 | "Warlord: win 2 battles (attacker or defender)" — what counts as a defender win? | All attacker committed units eliminated | `Combat.md` | Open |
| AL-11 | Captured hex buildings "may be destroyed, downgraded, or taken over, depending on the circumstances" — which? | Taken over intact | `Tiles.md` / `Buildings.md` | Open |
| AL-12 | Do Archers strike again in the main Strike step after their Pre-Strike? | No — Pre-Strike is their strike for the round | `Combat.md` | Open |
| AL-13 | Cities produce "+2 Population and various combinations of resources" — which resources? | No Gold/Mana/Influence in M1 (cap, growth, and AP bonuses only) | `Tiles.md` | Open |
| AL-14 | Competing Adjacency Claims resolve by Influence bidding — a decision the M1 bots can't make | Contested claims stay neutral in M1 | `Tiles.md` | Sim-only |
