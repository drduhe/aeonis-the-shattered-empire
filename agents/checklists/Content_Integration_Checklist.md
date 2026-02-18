# Content Integration Checklist (Aeonis)

Use this when adding a new Lord, event, objective, strategy card, building, or tile.

## 1) Decide scope

- [ ] First Playable compatible, or “full game later”?
- [ ] If First Playable: what is the minimum subset needed?

## 2) Use an existing system hook

- [ ] Every effect maps to existing systems (AP / resources / Influence / Renown / Population / Council / combat / movement).
- [ ] Any new term is defined once and referenced elsewhere.

## 3) Place the content

- [ ] Lords: `lords/<Name>.md`
- [ ] Rules additions: `rules_and_systems/<Chapter>.md`
- [ ] Playtest-only overrides: `playtest/First_Playable_Packet.md`

## 4) Update the browsing layer (Codex)

- [ ] Add the doc to `content-manifest.json` in the right category (if desired).
- [ ] Confirm the `path` is correct relative to `new/`.

## 5) Update components

- [ ] If it requires a printed piece (card/token/tile), update `components/Components.md`.

## 6) Balance sanity check

- [ ] The content has a timing window and clear resolution order.
- [ ] The content has counterplay or opportunity cost.
- [ ] The content doesn’t create runaway “win more” without table interaction.

