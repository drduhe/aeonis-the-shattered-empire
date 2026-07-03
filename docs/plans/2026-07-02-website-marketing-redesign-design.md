# Website marketing redesign — design spec

**Status:** APPROVED design (brainstormed 2026-07-02). Implementation plan to follow.
**Scope:** The GitHub Pages site served from this repo root (`index.html`, `app.css`, `app.js`, `content-manifest.json`) at https://drduhe.github.io/aeonis-the-shattered-empire/.
**Goal:** Make the site maximally effective at (1) marketing the game toward the Kickstarter and (2) giving players clean access to rules/lore — measured by email waitlist signups.

---

## Decisions locked during brainstorm

| Decision | Choice |
| --- | --- |
| Primary conversion goal | Email waitlist signup |
| Email backend | Kit (formerly ConvertKit) free tier — form POSTs client-side to the form's public action URL |
| Codex exposure | Curated player-facing manifest; internal docs removed from the UI (files stay in repo) |
| Site structure | Two pages: marketing homepage + separate Codex page |
| Homepage structure | Story-led ("book cover" lore opening, product reveal second) |
| Visual direction | "Arcane Night" — near-black indigo, glowing teal arcana, warm gold CTAs (evolution of current palette) |
| Tech constraint | No build step; plain HTML/CSS/JS on GitHub Pages (main branch, root) |
| Art | Existing assets + AI-generated art on demand |
| Social links | Discord, BoardGameGeek, Instagram, Kickstarter pre-launch page (config slots until URLs exist) |

---

## 1. Site architecture

Two pages, one funnel:

- **`index.html` — marketing page.** Pure marketing funnel; no embedded doc browser.
- **`codex.html` — the Imperial Codex.** The existing browser UI (sidebar + markdown viewer) moved wholesale to its own page, loading a curated manifest.

**Deep-link compatibility:** existing shared URLs like `index.html#/doc/rules_and_systems/Combat.md` must keep working. `index.html` detects a `#/doc/…` hash on load and redirects to `codex.html` preserving the hash. The Codex viewer continues to render **any** repo path requested via direct hash link (even docs not listed in the curated sidebar), so previously shared links to internal docs don't break.

**Theming:** the marketing page is dark-only (Arcane Night is the brand). The Codex page keeps the existing light/dark toggle for long-form reading.

---

## 2. Homepage (`index.html`) — section order and content

Mockup validated in brainstorm session (`.superpowers/brainstorm/…/homepage-mockup.html`). Sections top to bottom:

1. **Lore opening (full viewport).** Key art background (existing `aeonis_hero_banner.png`, upgradeable later), kicker "From the Speaking Stones", the Pilgrims' Gate inscription as the headline: *"The empire did not fall in a day. It fell in a single breath — and the world has spent a hundred years learning to breathe again."* Attribution line, scroll cue. No form here — mood only. Slim top nav (brand + Codex link + "Get launch alerts" anchor button).
2. **The reveal.** Kicker "A grand-strategy board game"; title; lede: empty throne that kills its claimants, eight banished Lords, "in the tradition of the great epic 4X board games" (approved positioning language). Fact chips: **3–8 players • 4–10 hours • 8 Lords**. **Primary email capture card** ("Be first to the Kickstarter" / "One email at launch, plus occasional faction reveals. No spam."). Secondary "Follow on Kickstarter" button beside it once the pre-launch URL exists.
3. **Lords gallery.** All 8 launch Lords: portrait, name, role + faction. Hover/tap flips to the Lord's signature quote + "Read their story" link into the Codex. Below the grid, a teaser strip for the 4 expansion contenders ("Shadows on the Horizon" — names only, no sheets linked).
4. **The game (3 pillars).** One action per turn (AP economy, low downtime) • The High Council (player-authored motions, laws, titles) • Battle lines & sieges (commitment, reserves, campaigns not coin flips). Each pillar links to its owning Codex chapter.
5. **Built in the open.** Short credibility section: active playtesting toward Kickstarter, design is public. Card linking to the Codex ("Rules chapters • Lorebook • Lord sheets • How to play").
6. **FAQ (accordion).** At minimum: When does the Kickstarter launch? / Is this a Twilight Imperium clone? (use approved positioning answer) / How long does a game take? / Can I playtest it? (points to Discord + waitlist).
7. **Final CTA.** Lore closer ("The stones are whispering. The roads are open.") + email form repeat.
8. **Footer.** Brand line + social links: Discord, BoardGameGeek, Instagram, Kickstarter.

**Copy rules:** all public copy respects `lore/Naming_Bible.md` (Imperial Seat, Speaking Stones, Influence, Discovery/Ritual, Renown) and `marketing/Positioning.md` approved language (never "clone/reskin").

**Mobile:** single column; lore opening stays full-viewport; Lords grid 2-up; fact chips wrap.

---

## 3. Codex page (`codex.html`) — curation

Existing sidebar/search/viewer UI is reused. `content-manifest.json` is rewritten to player-facing categories:

**Public categories**

- **Start Here:** `rulebook/Learn_to_Play.md`, `rulebook/Player_Aid.md`, `playtest/First_Playable_Packet.md`
- **Rules & Systems:** all `rules_and_systems/*.md` chapters (INDEX included)
- **Lords:** all 12 sheets; the 4 expansion Lords grouped/labelled "Shadows on the Horizon"
- **Lore:** `lore/Lore.md`, `lore/Naming_Bible.md`
- **Components:** `components/Components.md`

**Removed from manifest** (files stay in repo; direct links still render): `agents/**`, `marketing/**`, `docs/plans/**`, `mcp/**`, `sim/**`, `data/**`, `playtest/Balance_Dashboard.md`, `playtest/session_log.csv`, `playtest/Full_Game_Scope.md`, `components/Production_Manifest.md`, `AGENTS.md`, `CLAUDE.md`, `README.md`.

Codex page keeps a slim version of the top nav (brand → homepage, "Get launch alerts" anchor → homepage form) so doc readers can convert too.

---

## 4. Email capture pipeline

- **Service:** Kit free tier (up to 10,000 subscribers; sending, confirmation, and the eventual launch blast all handled in Kit). Owner action: create account + one form, copy the form's public action URL (`https://app.convertkit.com/forms/{FORM_ID}/subscriptions`).
- **Site wiring:** the existing `window.AEONIS_WAITLIST_ENDPOINT` config slot holds the Kit URL. The form POSTs `email_address` (Kit's expected field) with a JS-disabled fallback of a plain HTML form POST to the same URL. Success state: "Check your inbox to confirm." Error state keeps the email in the field and shows a retry message.
- **Removals:** the localStorage "local mode" and the visitor-facing "Export CSV" button are deleted — they silently lose real signups today and mislead visitors.
- **Both forms** (reveal section + final CTA) post to the same endpoint, tagged with a `source` hidden field (`hero` / `footer`) if Kit custom fields are configured, else omitted.

---

## 5. SEO, sharing, measurement

- **Share image:** generate a real 1200×630 Open Graph image from key art (title + tagline baked in). Referenced by `og:image` / `twitter:image` (currently a favicon — broken share cards). `twitter:card` becomes `summary_large_image`.
- **Metadata:** per-page `<title>`/description (homepage: "Aeonis: The Shattered Empire — epic fantasy grand strategy board game, 3–8 players"; codex: "The Imperial Codex — rules, lore, and Lords"). Canonical URLs on both pages.
- **Structured data:** JSON-LD `Game` (board game) + `Organization` block on the homepage.
- **Crawling:** `sitemap.xml` (two pages) + `robots.txt`. Accepted tradeoff: Codex docs are client-rendered (hash routes) and won't index individually; the homepage carries SEO.
- **Analytics:** GoatCounter (free, no cookie banner). One script tag on both pages + a custom event on successful waitlist signup so conversion is visible. Owner action: create GoatCounter account (config slot for the site code).

---

## 6. Assets to produce (AI-generated, on demand)

1. OG share image 1200×630 (from hero key art + wordmark).
2. Optional upgraded wide key art for the lore opening if the existing banner crops poorly at full viewport (test first; reuse if acceptable).

No other new art is required for v1; Lord portraits and logo lockup already exist.

---

## Out of scope (fast follows, not in this pass)

- Press kit page (planned after Kickstarter pre-launch page exists — serves influencer outreach phase).
- Per-Lord standalone pages (SEO surface; revisit when content stabilizes).
- Blog/devlog. "Built in the open" section links to the Codex instead.

---

## Success criteria

1. A real email submitted on the live site arrives in the Kit subscriber list (end-to-end test).
2. Existing deep links (`index.html#/doc/…`) land on the correct doc in `codex.html`.
3. Curated sidebar shows only the public categories above; internal docs are absent from search results in the UI.
4. Share card renders correctly in Discord and on X (validator check).
5. `content-manifest.json` parses (`python3 -c "import json; json.load(open('content-manifest.json'))"`), and public copy passes the terminology sweep in `AGENTS.md` §Validate.
6. GoatCounter records pageviews and a signup event.
7. No build step introduced; site works served statically from repo root.
