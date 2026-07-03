# Website Marketing Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split the GitHub Pages site into a story-led marketing homepage and a curated Imperial Codex, wire real email capture via Kit, and add SEO/analytics — all without a build step.

**Architecture:** Three JS modules on a no-build static site: `site-config.js` (owner-editable URLs/keys), `marketing.js` (homepage funnel), `codex.js` (markdown browser extracted from today's `app.js`). Marketing lives in `index.html`; the Codex browser moves to `codex.html`. `app.css` stays shared; new `marketing.css` holds homepage-only layout. `content-manifest.json` is rewritten to player-facing categories only; `openDoc()` is patched so direct `#/doc/…` links still fetch files not listed in the manifest.

**Tech Stack:** Plain HTML/CSS/JS, GitHub Pages (main branch, repo root), Kit form POST, GoatCounter script tag.

**Design spec:** `docs/plans/2026-07-02-website-marketing-redesign-design.md`

---

## File map (before you start)

| File | Role |
| --- | --- |
| `site-config.js` | **Create.** Owner config: Kit form URL, Kickstarter, social links, GoatCounter site code |
| `index.html` | **Rewrite.** Marketing funnel only; deep-link redirect to `codex.html` |
| `codex.html` | **Create.** Imperial Codex browser (extracted from old `index.html` `#browse` section) |
| `codex.js` | **Create.** Renamed/refactored `app.js` — browser logic only |
| `marketing.js` | **Create.** Waitlist, FAQ accordion, Lord card flips, marketing nav |
| `marketing.css` | **Create.** Homepage sections (lore opening, reveal, lords, FAQ, etc.) |
| `app.css` | **Modify.** Shared tokens/components; remove homepage-only rules moved to `marketing.css` |
| `app.js` | **Delete** after `codex.js` is wired (or keep as thin re-export — prefer delete) |
| `content-manifest.json` | **Rewrite.** Curated player-facing manifest |
| `marketing/assets/og-share.png` | **Create.** 1200×630 Open Graph image |
| `sitemap.xml` | **Create.** Two URLs |
| `robots.txt` | **Create.** Allow all + sitemap pointer |

---

## Task 1: Shared site config

**Files:**
- Create: `site-config.js`

- [ ] **Step 1: Create `site-config.js`**

```javascript
// Owner-editable runtime config for aeonis-the-shattered-empire GitHub Pages site.
// Fill in URLs after creating Kit + GoatCounter accounts.
window.AEONIS_WAITLIST_ENDPOINT = ""; // e.g. "https://app.convertkit.com/forms/1234567/subscriptions"
window.AEONIS_KICKSTARTER_URL = "";   // e.g. "https://www.kickstarter.com/projects/..."
window.AEONIS_GOATCOUNTER = "";       // e.g. "aeonis" → loads https://aeonis.goatcounter.com/count

window.AEONIS_SOCIAL = {
  discord: "",
  bgg: "",
  instagram: "",
  kickstarter: "" // duplicate of pre-launch page if different from AEONIS_KICKSTARTER_URL
};
```

- [ ] **Step 2: Commit**

```bash
git add site-config.js
git commit -m "feat(site): add shared runtime config for waitlist and social links"
```

---

## Task 2: Curate `content-manifest.json`

**Files:**
- Modify: `content-manifest.json`

- [ ] **Step 1: Rewrite manifest to player-facing categories**

Replace the entire file with a curated manifest. Required structure:

**Categories (in this order):**

1. **Start Here** (`id: "start"`) — docs:
   - `rulebook/Learn_to_Play.md`
   - `rulebook/Player_Aid.md`
   - `playtest/First_Playable_Packet.md`

2. **Rules & Systems** (`id: "rules"`) — all 21 files in `rules_and_systems/*.md`, including `INDEX.md`. Copy descriptions/tags from the current manifest where they exist; add minimal entries for any chapter missing.

3. **Lords** (`id: "lords"`) — all 12 Lord sheets. Launch Lords (Cassian through Thal'rik): `status: "playtest"`. Expansion four (Serathis, Morvane, Tsuvara, Ozren): `status: "draft"`, tag each with `"expansion"`.

4. **Lore** (`id: "lore"`) — `lore/Lore.md`, `lore/Naming_Bible.md`

5. **Components** (`id: "components"`) — `components/Components.md`

**Remove entirely:** marketing category, README, AGENTS.md, playtest/Balance_Dashboard, playtest/Full_Game_Scope, playtest/session_log.csv, components/Production_Manifest, lore/README.md, agents/**, docs/**.

**Journeys** — update to player paths only:

```json
"journeys": [
  {
    "id": "new",
    "label": "New to Aeonis? Read this path",
    "steps": [
      { "label": "Learn to Play", "path": "rulebook/Learn_to_Play.md" },
      { "label": "Round timing", "path": "rules_and_systems/Round_Structure.md" },
      { "label": "Actions", "path": "rules_and_systems/Actions.md" },
      { "label": "First Playable", "path": "playtest/First_Playable_Packet.md" }
    ]
  }
]
```

- [ ] **Step 2: Validate manifest parses**

Run:

```bash
python3 -c "import json; m=json.load(open('content-manifest.json')); print('OK', len(m['categories']), 'categories')"
```

Expected: `OK 5 categories`

- [ ] **Step 3: Commit**

```bash
git add content-manifest.json
git commit -m "feat(site): curate Codex manifest for player-facing docs only"
```

---

## Task 3: Extract Codex to `codex.html` + `codex.js`

**Files:**
- Create: `codex.html`
- Create: `codex.js` (from `app.js`)
- Modify: `app.js` → delete in Task 8 after verification

- [ ] **Step 1: Create `codex.html`**

Copy the `<head>` asset links from current `index.html` (fonts, marked, DOMPurify, highlight.js, `app.css`). Load order:

```html
<script src="site-config.js"></script>
<link rel="stylesheet" href="app.css?v=2026-07-02-1" />
<script defer src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/dompurify@3.0.8/dist/purify.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/highlight.js@11.9.0/lib/highlight.min.js"></script>
<script defer src="codex.js?v=2026-07-02-1"></script>
```

Body: slim topbar only:

```html
<header class="topbar">
  <div class="container topbar__inner">
    <a class="brand" href="index.html">…logo lockup…</a>
    <nav class="nav">
      <a class="nav__link" href="index.html">Home</a>
      <a class="nav__link is-active" href="codex.html">Codex</a>
    </nav>
    <div class="topbar__actions">
      <button id="themeToggle" …>Theme</button>
      <a class="btn btn--primary" href="index.html#waitlist">Get launch alerts</a>
    </div>
  </div>
</header>
<main id="browse" class="section section--browser">…existing browser markup from index.html #browse…</main>
<footer class="footer">…minimal footer with social links from site-config…</footer>
```

Page `<title>`: `The Imperial Codex — Aeonis: The Shattered Empire`

- [ ] **Step 2: Create `codex.js` from `app.js`**

Copy `app.js` → `codex.js`, then:

1. **Delete** `initDecrees()`, `initCampaignLinks()`, and their calls in `init()`.
2. **Delete** entire `initWaitlist()` function and its call in `init()`.
3. **Delete** marketing nav sync keys in `syncNavActive()` (`kickstarter|overview|lords|pillars|about`) — Codex nav is static.
4. **Patch `openDoc()`** so unlisted paths still load (design requirement for old shared links):

Replace the block:

```javascript
  if (!doc) {
    showViewerState("error", { message: `This document is not in the manifest: ${path}` });
    return;
  }

  showViewerState("doc");
```

With:

```javascript
  showViewerState("doc");
```

And update `renderCrumbs()` call to tolerate missing manifest entry:

```javascript
  renderCrumbs(doc || { path, title: path.split("/").pop().replace(/\.md$/, "") });
```

5. Update the catch block of `openDoc()`, if fetch 404s, *then* show error.

- [ ] **Step 3: Smoke-test Codex locally**

Run:

```bash
python3 -m http.server 8765
```

Open:
- `http://localhost:8765/codex.html` — sidebar shows 5 categories, no Marketing
- `http://localhost:8765/codex.html#/doc/playtest/Balance_Dashboard.md` — doc loads even though absent from sidebar (proves deep-link fix)

- [ ] **Step 4: Commit**

```bash
git add codex.html codex.js
git commit -m "feat(site): extract Imperial Codex to dedicated page"
```

---

## Task 4: Rewrite marketing `index.html`

**Files:**
- Modify: `index.html` (full rewrite)
- Create: `marketing.css`

- [ ] **Step 1: Add deep-link redirect in `<head>` (first script)**

```html
<script>
  if (/^#\/doc\//.test(location.hash)) {
    location.replace("codex.html" + location.hash);
  }
</script>
```

- [ ] **Step 2: Build homepage sections per design spec**

Section order and IDs:

| Section | ID | Notes |
| --- | --- | --- |
| Slim topbar | — | Brand → `index.html`, Codex → `codex.html`, CTA → `#waitlist` |
| Lore opening | `#opening` | Full viewport, hero banner bg, Speaking Stones kicker, Pilgrims' Gate quote, scroll cue |
| The reveal | `#waitlist` | Product pitch, fact chips, primary email form (`id="waitlistFormHero"`) |
| Lords gallery | `#lords` | 8 flip cards; expansion teaser below |
| The game | `#game` | 3 pillar cards linking to Codex chapters |
| Built in the open | `#open` | Credibility + Codex card |
| FAQ | `#faq` | Accordion (details/summary or button toggles) |
| Final CTA | `#cta` | Lore closer + second form (`id="waitlistFormFooter"`) |
| Footer | — | Social links populated by JS from `AEONIS_SOCIAL` |

**Approved copy anchors** (from design spec + `marketing/Positioning.md`):

- Reveal lede must include "in the tradition of the great epic 4X board games"
- FAQ TI4 answer: "Aeonis is inspired by the genre TI4 defined — reforged in epic fantasy. Same weight, new world." Never use "clone" or "reskin"
- Session length: 4–10 hours; player count: 3–8

**Lord cards** — reuse existing portrait paths under `marketing/assets/`. Each card:

```html
<article class="lordCard" data-lord="cassian">
  <div class="lordCard__front">…portrait, name, role…</div>
  <div class="lordCard__back">
    <blockquote>“Kingdoms fall to blades…”</blockquote>
    <a href="codex.html#/doc/lords/Cassian.md">Read their story</a>
  </div>
</article>
```

**Expansion teaser** (names only, no links):

> Shadows on the Horizon — Serathis • Morvane • Tsuvara • Ozren

- [ ] **Step 3: Create `marketing.css`**

Move homepage-specific rules out of `app.css` (hero, lords grid, waitlist, FAQ, lore opening). Add Arcane Night tokens if needed:

```css
:root {
  --gold-cta: #d8b45a;
  --teal-kicker: #24d1c4; /* matches existing --accent2 */
}
.opening { min-height: 100svh; … }
.lordCard.is-flipped .lordCard__front { … }
```

Dark-only on marketing page — do not include theme toggle on `index.html`.

- [ ] **Step 4: Wire assets in `<head>`**

```html
<script src="site-config.js"></script>
<link rel="stylesheet" href="app.css?v=2026-07-02-1" />
<link rel="stylesheet" href="marketing.css?v=2026-07-02-1" />
<script defer src="marketing.js?v=2026-07-02-1"></script>
```

- [ ] **Step 5: Commit**

```bash
git add index.html marketing.css
git commit -m "feat(site): story-led marketing homepage"
```

---

## Task 5: Marketing JS — waitlist, FAQ, social links

**Files:**
- Create: `marketing.js`

- [ ] **Step 1: Create `marketing.js`**

```javascript
function getConfig() {
  const w = window;
  return {
    waitlistEndpoint: (w.AEONIS_WAITLIST_ENDPOINT || "").trim(),
    kickstarterUrl: (w.AEONIS_KICKSTARTER_URL || "").trim(),
    goatcounter: (w.AEONIS_GOATCOUNTER || "").trim(),
    social: w.AEONIS_SOCIAL || {}
  };
}

function initSocialLinks() {
  const cfg = getConfig();
  document.querySelectorAll("[data-social]").forEach((a) => {
    const key = a.getAttribute("data-social");
    const url = cfg.social[key] || (key === "kickstarter" ? cfg.kickstarterUrl : "");
    if (url && /^https?:\/\//i.test(url)) {
      a.href = url;
      a.target = "_blank";
      a.rel = "noreferrer";
    } else {
      a.classList.add("is-disabled");
      a.setAttribute("aria-disabled", "true");
      a.removeAttribute("href");
    }
  });
}

function initKickstarterButton() {
  const cfg = getConfig();
  const btn = document.getElementById("kickstarterBtn");
  if (!btn || !cfg.kickstarterUrl) {
    if (btn) btn.hidden = true;
    return;
  }
  btn.href = cfg.kickstarterUrl;
  btn.target = "_blank";
  btn.rel = "noreferrer";
}

function trackSignup(source) {
  if (window.goatcounter && typeof window.goatcounter.count === "function") {
    window.goatcounter.count({ path: "/waitlist-signup/" + source, title: "Waitlist signup", event: true });
  }
}

function bindWaitlistForm(form, source) {
  if (!form) return;
  const cfg = getConfig();
  const emailEl = form.querySelector('input[type="email"]');
  const msgEl = form.querySelector(".waitlist__msg");
  const endpoint = cfg.waitlistEndpoint;

  if (!endpoint) {
    if (msgEl) msgEl.textContent = "Waitlist coming soon — check back shortly.";
    form.querySelector('button[type="submit"]')?.setAttribute("disabled", "true");
    return;
  }

  form.action = endpoint;
  form.method = "post";

  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const email = (emailEl?.value || "").trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      if (msgEl) msgEl.textContent = "That email doesn't look right. Try again.";
      return;
    }
    const body = new FormData();
    body.append("email_address", email);
    try {
      await fetch(endpoint, { method: "POST", body, mode: "no-cors" });
      if (msgEl) msgEl.textContent = "Check your inbox to confirm your subscription.";
      if (emailEl) emailEl.value = "";
      trackSignup(source);
    } catch (e) {
      if (msgEl) msgEl.textContent = "Couldn't submit right now. Please try again.";
    }
  });
}

function initFaq() {
  document.querySelectorAll(".faq__item").forEach((item) => {
    const btn = item.querySelector(".faq__q");
    const panel = item.querySelector(".faq__a");
    if (!btn || !panel) return;
    btn.addEventListener("click", () => {
      const open = item.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      panel.hidden = !open;
    });
  });
}

function initLordCards() {
  document.querySelectorAll(".lordCard").forEach((card) => {
    card.addEventListener("click", () => card.classList.toggle("is-flipped"));
    card.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter" || ev.key === " ") {
        ev.preventDefault();
        card.classList.toggle("is-flipped");
      }
    });
    card.setAttribute("tabindex", "0");
  });
}

function initGoatCounter() {
  const code = getConfig().goatcounter;
  if (!code) return;
  const s = document.createElement("script");
  s.async = true;
  s.dataset.goatcounter = `https://${code}.goatcounter.com/count`;
  s.src = "https://gc.zgo.at/count.js";
  document.head.appendChild(s);
}

document.addEventListener("DOMContentLoaded", () => {
  initGoatCounter();
  initSocialLinks();
  initKickstarterButton();
  bindWaitlistForm(document.getElementById("waitlistFormHero"), "hero");
  bindWaitlistForm(document.getElementById("waitlistFormFooter"), "footer");
  initFaq();
  initLordCards();
});
```

Each waitlist form in HTML must include `<div class="waitlist__msg" aria-live="polite"></div>`.

- [ ] **Step 2: Add GoatCounter to `codex.html`**

Add the same `initGoatCounter` call — either duplicate the 6-line loader inline in `codex.js` init, or extract to a tiny `analytics.js`. Prefer duplicating in `codex.js` init for YAGNI.

- [ ] **Step 3: Commit**

```bash
git add marketing.js
git commit -m "feat(site): waitlist, FAQ, and social link wiring for marketing page"
```

---

## Task 6: SEO, sharing, and crawl files

**Files:**
- Create: `marketing/assets/og-share.png`
- Create: `sitemap.xml`
- Create: `robots.txt`
- Modify: `index.html`, `codex.html` (meta tags)

- [ ] **Step 1: Create OG share image (1200×630)**

Generate from `marketing/assets/aeonis_hero_banner.png` + wordmark. Save as `marketing/assets/og-share.png`. Must be ≤ 1 MB, readable at thumbnail size.

- [ ] **Step 2: Add homepage meta tags to `index.html`**

```html
<meta name="description" content="Aeonis: The Shattered Empire — an epic fantasy grand strategy board game for 3–8 players. Join the Kickstarter waitlist." />
<link rel="canonical" href="https://drduhe.github.io/aeonis-the-shattered-empire/" />
<meta property="og:type" content="website" />
<meta property="og:url" content="https://drduhe.github.io/aeonis-the-shattered-empire/" />
<meta property="og:title" content="Aeonis: The Shattered Empire" />
<meta property="og:description" content="Epic fantasy grand strategy for 3–8 players. Eight banished Lords. One empty throne." />
<meta property="og:image" content="https://drduhe.github.io/aeonis-the-shattered-empire/marketing/assets/og-share.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://drduhe.github.io/aeonis-the-shattered-empire/marketing/assets/og-share.png" />
```

Add JSON-LD before `</head>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Game",
  "name": "Aeonis: The Shattered Empire",
  "description": "Epic fantasy grand strategy board game for 3–8 players.",
  "numberOfPlayers": { "@type": "QuantitativeValue", "minValue": 3, "maxValue": 8 },
  "genre": "Strategy",
  "gamePlatform": "Tabletop",
  "url": "https://drduhe.github.io/aeonis-the-shattered-empire/"
}
</script>
```

- [ ] **Step 3: Create `sitemap.xml` and `robots.txt`**

`sitemap.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://drduhe.github.io/aeonis-the-shattered-empire/</loc></url>
  <url><loc>https://drduhe.github.io/aeonis-the-shattered-empire/codex.html</loc></url>
</urlset>
```

`robots.txt`:

```
User-agent: *
Allow: /
Sitemap: https://drduhe.github.io/aeonis-the-shattered-empire/sitemap.xml
```

- [ ] **Step 4: Commit**

```bash
git add marketing/assets/og-share.png sitemap.xml robots.txt index.html codex.html
git commit -m "feat(site): SEO meta, OG image, sitemap, and robots"
```

---

## Task 7: CSS cleanup and delete legacy `app.js`

**Files:**
- Modify: `app.css`
- Delete: `app.js`

- [ ] **Step 1: Move homepage-only CSS from `app.css` to `marketing.css`**

Grep `app.css` for rules targeting removed homepage sections (`.hero`, `.decree`, `.sigil`, `.lordCard`, `.waitlist`, `.pillars`, `.loreDivider`, marketing `.section` variants). Move them; leave Codex/browser styles in `app.css`.

- [ ] **Step 2: Delete `app.js`**

Confirm nothing references it:

```bash
grep -r 'app\.js' --include='*.html' .
```

Expected: no matches (only `codex.js` and `marketing.js`).

```bash
git rm app.js
git commit -m "chore(site): remove legacy app.js after codex/marketing split"
```

---

## Task 8: Owner setup checklist (manual, not code)

These block live conversion but aren't code changes. Document in a comment at the top of `site-config.js`:

- [ ] Create free **Kit** account → Forms → create "Aeonis Waitlist" form → copy embed HTML → extract `action` URL → paste into `AEONIS_WAITLIST_ENDPOINT`
- [ ] Create **GoatCounter** site → paste site code into `AEONIS_GOATCOUNTER`
- [ ] Paste Discord, BGG, Instagram, Kickstarter pre-launch URLs into `AEONIS_SOCIAL`
- [ ] Submit one test email on the live site → confirm it appears in Kit subscriber list

---

## Task 9: Validation pass (required before calling done)

Run from repo root (`new/`):

- [ ] **Manifest parses**

```bash
python3 -c "import json; json.load(open('content-manifest.json'))" && echo OK
```

- [ ] **Terminology sweep** (expect hits only in allowed files per `AGENTS.md`)

```bash
grep -rnE "Palantír|Throne of Power|Magi Guild|Iron Vanguard|Sacred Order" --include='*.md' . ; grep -rnw "IP" --include='*.md' .
```

Also grep new HTML/JS copy:

```bash
grep -rnE "Palantír|Throne of Power|clone|reskin" index.html marketing.js
```

Expected: no matches in marketing copy.

- [ ] **Deep-link redirect**

`index.html#/doc/rules_and_systems/Combat.md` → lands on `codex.html#/doc/rules_and_systems/Combat.md` with Combat rendered.

- [ ] **Unlisted doc deep link**

`codex.html#/doc/playtest/Balance_Dashboard.md` → doc renders (not "not in manifest" error).

- [ ] **Curated sidebar**

Search "Balance Dashboard" in Codex UI → zero results.

- [ ] **Share card**

Paste homepage URL into Discord or https://www.opengraph.xyz/ → shows `og-share.png` preview.

- [ ] **No build step**

Site works with `python3 -m http.server` — no npm, no bundler.

---

## Spec coverage checklist (self-review)

| Design spec section | Task |
| --- | --- |
| Two-page architecture | Tasks 3, 4 |
| Deep-link compatibility | Tasks 3 (openDoc patch), 4 (redirect script) |
| Story-led homepage sections | Task 4 |
| Curated manifest | Task 2 |
| Kit email capture | Tasks 1, 5, 8 |
| Remove localStorage/export CSV | Task 5 (not ported) |
| SEO + OG image | Task 6 |
| GoatCounter analytics | Tasks 5, 8 |
| Arcane Night visual direction | Tasks 4, 7 |
| Social links | Tasks 1, 5 |
| Success criteria 1–7 | Task 9 |

---

## Execution order summary

1. Task 1 (config) → Task 2 (manifest)
2. Task 3 (Codex extraction) — testable standalone
3. Tasks 4 + 5 + 7 (homepage + JS + CSS cleanup) — parallelizable after Task 3
4. Task 6 (SEO assets)
5. Task 8 (owner fills config) → deploy → Task 9 (validation)

**Estimated effort:** one focused session (~3–4 hours) for an agent; owner Kit/GoatCounter setup ~15 minutes.
