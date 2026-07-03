# Canon Change Checklist (Aeonis)

Use this when making any rules change that could ripple.

## 1) Define the change

- [ ] What exact concept is changing? (term + definition)
- [ ] Where is its canonical definition located? (file + section)
- [ ] What player-facing behavior changes?

## 2) Timing + windows

- [ ] Does this change affect `rules_and_systems/Round_Structure.md` windows?
- [ ] Does it create a new trigger window? If yes, it must be named explicitly.

## 3) Downstream docs (update all that apply)

- [ ] `rules_and_systems/INDEX.md` (if chapter list, red flags, or references change)
- [ ] `playtest/First_Playable_Packet.md` (if First Playable rules are impacted)
- [ ] `components/Components.md` (if components/cards/tokens are impacted)
- [ ] `rules_and_systems/Actions.md` (AP changes)
- [ ] `rules_and_systems/Movement.md` and/or `rules_and_systems/Tiles.md` (control/borders/ZOC changes)
- [ ] `rules_and_systems/Combat.md` (combat changes)
- [ ] `rules_and_systems/High_Council.md` (politics/influence/voting changes)
- [ ] `rules_and_systems/Victory.md` (VP pacing or scoring changes)
- [ ] `rulebook/Learn_to_Play.md` + `rulebook/Player_Aid.md` (derived teaching docs — update for any player-facing change)
- [ ] `lore/Naming_Bible.md` (if a term, name, or keyword is added or renamed)

## 4) Codex surfacing (optional)

- [ ] If you want the doc visible in the Codex, update `content-manifest.json`.

## 5) Simulator sync (when behavior changes)

- [ ] Map the change to `sim/aeonis_sim/engine/` (correct module for the system).
- [ ] Add or update tests in `sim/tests/`; run `cd sim && python -m pytest`.
- [ ] Regenerate golden replays if outcomes or resolution order changed (`sim/scripts/generate_golden_replays.py`).
- [ ] Update `sim/configs/regression-*.json` and run regression checks if balance gates move.
- [ ] Log unresolved doc gaps in `playtest/Ambiguity_Ledger.md` before encoding a guess.

## 6) Playtest intent

- [ ] Add a one-paragraph “why” note near the change (what problem it fixes).
- [ ] Add 1–3 testable hypotheses for the next playtest (sim-led until human table time returns).

