/* Aeonis Codex — lightweight markdown browser */

const state = {
  manifest: null,
  docsFlat: [],
  categoryById: new Map(),
  docByPath: new Map(),
  selectedPath: null,
  cache: new Map(), // path -> { text, html }
  contentIndex: new Map(), // path -> normalizedText (lazy)
  search: {
    query: "",
    category: "all",
    searchContent: false
  }
};

function $(id) {
  return document.getElementById(id);
}

function clamp(n, a, b) {
  return Math.max(a, Math.min(b, n));
}

function normalizeText(s) {
  return (s || "")
    .toLowerCase()
    .replace(/\s+/g, " ")
    .replace(/[^\p{L}\p{N}\s]/gu, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function encodeHashDocPath(path) {
  // Keep it human-ish, but safe.
  return `#/doc/${encodeURIComponent(path)}`;
}

function parseHash() {
  const raw = window.location.hash || "";
  const m = raw.match(/^#\/doc\/(.+)$/);
  if (!m) return { route: "home" };
  try {
    return { route: "doc", path: decodeURIComponent(m[1]) };
  } catch {
    return { route: "doc", path: m[1] };
  }
}

function setTheme(next) {
  const root = document.documentElement;
  if (next === "light") root.setAttribute("data-theme", "light");
  else root.removeAttribute("data-theme");
  try {
    localStorage.setItem("aeonis.theme", next);
  } catch {
    // ignore
  }
}

function getTheme() {
  try {
    const stored = localStorage.getItem("aeonis.theme");
    if (stored === "light" || stored === "dark") return stored;
  } catch {
    // ignore
  }
  return "dark";
}

function categoryColorDotClass(color) {
  if (color === "teal") return "pill__dot pill__dot--teal";
  if (color === "gold") return "pill__dot pill__dot--gold";
  if (color === "rose") return "pill__dot pill__dot--rose";
  return "pill__dot";
}

function buildFlatIndex(manifest) {
  const docsFlat = [];
  const categoryById = new Map();
  const docByPath = new Map();

  for (const cat of manifest.categories || []) {
    categoryById.set(cat.id, cat);
    for (const doc of cat.docs || []) {
      const item = {
        categoryId: cat.id,
        categoryLabel: cat.label,
        categoryColor: cat.color || "purple",
        title: doc.title,
        path: doc.path,
        description: doc.description || "",
        status: doc.status || "",
        minutes: typeof doc.minutes === "number" ? doc.minutes : null,
        tags: Array.isArray(doc.tags) ? doc.tags : [],
        // computed:
        titleNorm: normalizeText(doc.title),
        pathNorm: normalizeText(doc.path),
        descNorm: normalizeText(doc.description || "")
      };
      docsFlat.push(item);
      docByPath.set(item.path, item);
    }
  }

  docsFlat.sort((a, b) => a.title.localeCompare(b.title));

  state.docsFlat = docsFlat;
  state.categoryById = categoryById;
  state.docByPath = docByPath;
}

function renderCategorySelect() {
  const el = $("categorySelect");
  if (!el || !state.manifest) return;

  const opts = [
    { value: "all", label: "All categories" },
    ...(state.manifest.categories || []).map((c) => ({ value: c.id, label: c.label }))
  ];

  el.innerHTML = "";
  for (const o of opts) {
    const opt = document.createElement("option");
    opt.value = o.value;
    opt.textContent = o.label;
    el.appendChild(opt);
  }

  el.value = state.search.category;
}

function statusBadgeClass(status) {
  const s = (status || "").toLowerCase();
  if (s === "core") return "badge badge--core";
  if (s === "playtest") return "badge badge--playtest";
  if (s === "draft") return "badge badge--draft";
  if (s === "internal") return "badge badge--internal";
  if (s === "notes") return "badge badge--notes";
  return "badge";
}

function scoreDoc(doc, qNorm, qWords) {
  if (!qNorm) return 1;

  let score = 0;
  if (doc.titleNorm.includes(qNorm)) score += 90;
  if (doc.pathNorm.includes(qNorm)) score += 30;
  if (doc.descNorm.includes(qNorm)) score += 20;

  // word-based fallbacks
  for (const w of qWords) {
    if (!w) continue;
    if (doc.titleNorm.includes(w)) score += 12;
    if (doc.pathNorm.includes(w)) score += 4;
    if (doc.descNorm.includes(w)) score += 3;
  }

  return score;
}

async function ensureContentIndexed(doc) {
  if (state.contentIndex.has(doc.path)) return;
  try {
    const text = await fetchText(doc.path);
    state.contentIndex.set(doc.path, normalizeText(text));
  } catch {
    state.contentIndex.set(doc.path, "");
  }
}

async function filterDocs() {
  const qNorm = normalizeText(state.search.query);
  const qWords = qNorm.split(" ").filter(Boolean);
  const cat = state.search.category;
  const wantContent = state.search.searchContent && qNorm.length >= 3;

  let candidates = state.docsFlat;
  if (cat !== "all") candidates = candidates.filter((d) => d.categoryId === cat);

  // quick pass on metadata
  let scored = candidates
    .map((d) => ({ d, s: scoreDoc(d, qNorm, qWords) }))
    .filter((x) => x.s > 0)
    .sort((a, b) => b.s - a.s);

  if (!wantContent) {
    // If query is empty, show category order (manifest order), otherwise keep scored.
    if (!qNorm) {
      scored = candidates.map((d) => ({ d, s: 1 }));
      // stable-ish: by category order then title
      const catOrder = new Map();
      (state.manifest?.categories || []).forEach((c, i) => catOrder.set(c.id, i));
      scored.sort((a, b) => {
        const ca = catOrder.get(a.d.categoryId) ?? 999;
        const cb = catOrder.get(b.d.categoryId) ?? 999;
        if (ca !== cb) return ca - cb;
        return a.d.title.localeCompare(b.d.title);
      });
    }

    return scored.map((x) => x.d);
  }

  // content search: index lazily, but only for the top slice first for speed
  const topSlice = scored.slice(0, clamp(scored.length, 0, 40)).map((x) => x.d);
  await Promise.all(topSlice.map(ensureContentIndexed));

  const withContent = scored
    .map(({ d, s }) => {
      const content = state.contentIndex.get(d.path) || "";
      let s2 = s;
      if (content.includes(qNorm)) s2 += 110;
      for (const w of qWords) {
        if (w.length >= 3 && content.includes(w)) s2 += 9;
      }
      return { d, s: s2 };
    })
    .sort((a, b) => b.s - a.s)
    .filter((x) => x.s > 0);

  return withContent.map((x) => x.d);
}

function renderDocList(docs) {
  const list = $("docList");
  const count = $("resultsCount");
  if (!list) return;

  list.innerHTML = "";
  count.textContent = `${docs.length} doc${docs.length === 1 ? "" : "s"}`;

  for (const d of docs) {
    const a = document.createElement("a");
    a.className = "docItem";
    a.href = encodeHashDocPath(d.path);
    a.setAttribute("role", "link");
    a.setAttribute("data-path", d.path);

    if (state.selectedPath === d.path) {
      a.setAttribute("aria-current", "page");
    }

    const title = document.createElement("div");
    title.className = "docItem__title";
    title.textContent = d.title;

    const desc = document.createElement("div");
    desc.className = "docItem__desc";
    desc.textContent = d.description || "";

    const meta = document.createElement("div");
    meta.className = "docItem__meta";

    const pill = document.createElement("span");
    pill.className = "pill";
    const dot = document.createElement("span");
    dot.className = categoryColorDotClass(d.categoryColor);
    dot.setAttribute("aria-hidden", "true");
    const pillText = document.createElement("span");
    pillText.textContent = d.categoryLabel;
    pill.appendChild(dot);
    pill.appendChild(pillText);

    const path = document.createElement("span");
    path.textContent = d.path;
    path.style.opacity = "0.95";

    meta.appendChild(pill);
    meta.appendChild(path);

    const badges = document.createElement("div");
    badges.className = "docItem__badges";
    if (d.status) {
      const b = document.createElement("span");
      b.className = statusBadgeClass(d.status);
      b.textContent = d.status;
      badges.appendChild(b);
    }
    if (typeof d.minutes === "number") {
      const m = document.createElement("span");
      m.className = "badge";
      m.textContent = `${d.minutes} min`;
      badges.appendChild(m);
    }

    a.appendChild(title);
    if (d.description) a.appendChild(desc);
    a.appendChild(meta);
    if (badges.childNodes.length) a.appendChild(badges);

    list.appendChild(a);
  }
}

function renderJourneys() {
  const host = $("journeys");
  if (!host) return;
  const journeys = state.manifest?.journeys || [];
  if (!Array.isArray(journeys) || journeys.length === 0) {
    host.innerHTML = "";
    return;
  }

  host.innerHTML = "";
  for (const j of journeys) {
    const wrap = document.createElement("div");
    wrap.className = "journey";

    const title = document.createElement("div");
    title.className = "journey__title";
    title.textContent = j.label || "Suggested path";

    const steps = document.createElement("div");
    steps.className = "journey__steps";

    for (const s of j.steps || []) {
      const btn = document.createElement("a");
      btn.className = "journeyStep";
      btn.href = encodeHashDocPath(s.path);
      btn.textContent = s.label || s.path;
      steps.appendChild(btn);
    }

    wrap.appendChild(title);
    wrap.appendChild(steps);
    host.appendChild(wrap);
  }
}

function renderCrumbs(doc) {
  const el = $("crumbs");
  if (!el) return;
  if (!doc) {
    el.innerHTML = "";
    return;
  }

  const frag = document.createDocumentFragment();

  const c1 = document.createElement("span");
  c1.className = "crumb";
  c1.textContent = doc.categoryLabel;
  frag.appendChild(c1);

  const sep = document.createElement("span");
  sep.className = "dot";
  sep.setAttribute("aria-hidden", "true");
  sep.textContent = "•";
  frag.appendChild(sep);

  const c2 = document.createElement("span");
  c2.className = "crumb";
  const code = document.createElement("code");
  code.textContent = doc.path;
  c2.appendChild(code);
  frag.appendChild(c2);

  el.innerHTML = "";
  el.appendChild(frag);
}

function showViewerState(kind, payload) {
  const empty = $("emptyState");
  const md = $("markdown");
  const err = $("errorBox");
  const errText = $("errorText");

  if (!empty || !md || !err) return;

  if (kind === "empty") {
    empty.hidden = false;
    md.hidden = true;
    err.hidden = true;
    return;
  }
  if (kind === "error") {
    empty.hidden = true;
    md.hidden = true;
    err.hidden = false;
    errText.textContent = payload?.message || "Unknown error.";
    return;
  }
  if (kind === "doc") {
    empty.hidden = true;
    md.hidden = false;
    err.hidden = true;
    return;
  }
}

async function fetchText(path) {
  const res = await fetch(path, { cache: "no-store" });
  if (!res.ok) throw new Error(`HTTP ${res.status} when fetching ${path}`);
  return await res.text();
}

function markdownToHtml(mdText, basePath) {
  // Configure marked once (safe to call multiple times).
  if (window.marked && !window.__aeonisMarkedConfigured) {
    window.__aeonisMarkedConfigured = true;
    window.marked.setOptions({
      gfm: true,
      breaks: false,
      mangle: false,
      headerIds: true
    });
  }

  // Rewrite relative markdown links to stay inside the app when possible.
  // - Links to *.md become hash routes
  // - Other relative links become normal links relative to the doc's folder
  const renderer = new window.marked.Renderer();
  const baseDir = basePath.includes("/") ? basePath.split("/").slice(0, -1).join("/") + "/" : "";

  renderer.link = (href, title, text) => {
    const safeText = text || "";
    const safeTitle = title ? ` title="${escapeHtmlAttr(title)}"` : "";
    if (!href) return `<a${safeTitle}>${safeText}</a>`;

    // keep absolute / anchors
    const isAbs = /^(https?:\/\/|mailto:|#)/i.test(href);
    if (isAbs) {
      return `<a href="${escapeHtmlAttr(href)}"${safeTitle} target="_blank" rel="noreferrer">${safeText}</a>`;
    }

    // strip leading ./
    const clean = href.replace(/^\.\//, "");
    const resolved = baseDir ? baseDir + clean : clean;

    if (resolved.toLowerCase().endsWith(".md")) {
      const hash = encodeHashDocPath(resolved);
      return `<a href="${escapeHtmlAttr(hash)}"${safeTitle}>${safeText}</a>`;
    }

    return `<a href="${escapeHtmlAttr(resolved)}"${safeTitle} target="_blank" rel="noreferrer">${safeText}</a>`;
  };

  const rawHtml = window.marked.parse(mdText, { renderer });
  const cleanHtml = window.DOMPurify.sanitize(rawHtml, {
    USE_PROFILES: { html: true }
  });
  return cleanHtml;
}

function escapeHtmlAttr(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function highlightCodeBlocks(container) {
  if (!container) return;
  if (!window.hljs) return;
  const blocks = container.querySelectorAll("pre code");
  blocks.forEach((b) => {
    try {
      window.hljs.highlightElement(b);
    } catch {
      // ignore
    }
  });
}

function setViewerLinks(path) {
  const rawBtn = $("openRawBtn");
  const fallbackBtn = $("fallbackBtn");
  if (rawBtn) rawBtn.href = path || "#";
  if (fallbackBtn) fallbackBtn.href = path || "#";
}

async function openDoc(path, { scrollIntoView = false } = {}) {
  const doc = state.docByPath.get(path);
  state.selectedPath = path;

  renderCrumbs(doc || null);
  setViewerLinks(path);

  const retryBtn = $("retryBtn");
  if (retryBtn) retryBtn.href = encodeHashDocPath(path);

  if (!doc) {
    showViewerState("error", { message: `This document is not in the manifest: ${path}` });
    return;
  }

  showViewerState("doc");

  const mdEl = $("markdown");
  if (!mdEl) return;

  // Render from cache first (fast), then refresh in background.
  const cached = state.cache.get(path);
  if (cached?.html) {
    mdEl.innerHTML = cached.html;
    highlightCodeBlocks(mdEl);
  } else {
    mdEl.innerHTML = `<p><em>Loading…</em></p>`;
  }

  try {
    const text = await fetchText(path);
    const html = markdownToHtml(text, path);
    state.cache.set(path, { text, html });
    mdEl.innerHTML = html;
    highlightCodeBlocks(mdEl);

    // Ensure list highlighting updates immediately
    refreshDocListSoon();

    if (scrollIntoView) {
      mdEl.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  } catch (e) {
    showViewerState("error", { message: e?.message || String(e) });
  }
}

let refreshTimer = null;
function refreshDocListSoon() {
  if (refreshTimer) window.clearTimeout(refreshTimer);
  refreshTimer = window.setTimeout(async () => {
    const docs = await filterDocs();
    renderDocList(docs);
  }, 30);
}

function wireEvents() {
  const themeBtn = $("themeToggle");
  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      const now = document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
      setTheme(now === "light" ? "dark" : "light");
    });
  }

  const mobileNav = $("mobileNav");
  const menuToggle = $("menuToggle");
  function setMobileNavOpen(open) {
    if (!mobileNav || !menuToggle) return;
    mobileNav.hidden = !open;
    menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
  }
  if (menuToggle && mobileNav) {
    menuToggle.addEventListener("click", () => setMobileNavOpen(!!mobileNav.hidden));
    mobileNav.addEventListener("click", (ev) => {
      const t = ev.target;
      if (t && t.closest && t.closest("a")) setMobileNavOpen(false);
    });
  }

  const searchInput = $("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      state.search.query = searchInput.value || "";
      refreshDocListSoon();
    });
  }

  const categorySelect = $("categorySelect");
  if (categorySelect) {
    categorySelect.addEventListener("change", () => {
      state.search.category = categorySelect.value || "all";
      refreshDocListSoon();
    });
  }

  const searchContentToggle = $("searchContentToggle");
  if (searchContentToggle) {
    searchContentToggle.addEventListener("change", () => {
      state.search.searchContent = !!searchContentToggle.checked;
      refreshDocListSoon();
    });
  }

  const copyLinkBtn = $("copyLinkBtn");
  if (copyLinkBtn) {
    copyLinkBtn.addEventListener("click", async () => {
      const path = state.selectedPath;
      const url = path ? new URL(encodeHashDocPath(path), window.location.href).toString() : window.location.href;
      try {
        await navigator.clipboard.writeText(url);
        copyLinkBtn.textContent = "Copied";
        window.setTimeout(() => (copyLinkBtn.textContent = "Copy link"), 900);
      } catch {
        // fallback: prompt
        window.prompt("Copy link:", url);
      }
    });
  }

  const collapseSidebarBtn = $("collapseSidebarBtn");
  const browser = document.querySelector(".browser");
  if (collapseSidebarBtn && browser) {
    let collapsed = false;
    collapseSidebarBtn.addEventListener("click", () => {
      collapsed = !collapsed;
      browser.classList.toggle("browser--collapsed", collapsed);
      collapseSidebarBtn.textContent = collapsed ? "Expand" : "Collapse";
    });
  }

  function syncNavActive() {
    const hash = window.location.hash || "";
    let active = "";
    if (/^#\/doc\//.test(hash)) active = "browse";
    else if (/^#(overview|lords|pillars|browse|about)\b/.test(hash)) active = hash.slice(1).split("?")[0];

    const desktopLinks = document.querySelectorAll(".nav__link");
    desktopLinks.forEach((a) => {
      const href = a.getAttribute("href") || "";
      const key = href.startsWith("#") ? href.slice(1) : "";
      a.classList.toggle("is-active", !!active && key === active);
    });

    const mobileLinks = document.querySelectorAll(".mobileNav__link[data-nav]");
    mobileLinks.forEach((a) => {
      const key = a.getAttribute("data-nav") || "";
      a.classList.toggle("is-active", !!active && key === active);
    });
  }

  window.addEventListener("hashchange", () => {
    // close mobile menu on navigation
    const mobileNav = $("mobileNav");
    if (mobileNav) mobileNav.hidden = true;
    const menuToggle = $("menuToggle");
    if (menuToggle) menuToggle.setAttribute("aria-expanded", "false");
    syncNavActive();
    route();
  });
  // `wireEvents()` runs after DOMContentLoaded, so call immediately.
  syncNavActive();
}

async function route() {
  const r = parseHash();
  if (r.route === "doc") {
    const path = r.path;
    await openDoc(path, { scrollIntoView: true });
    return;
  }
  state.selectedPath = null;
  renderCrumbs(null);
  setViewerLinks("#");
  showViewerState("empty");
  refreshDocListSoon();
}

function initDecrees() {
  const el = $("decreeText");
  if (!el) return;
  try {
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  } catch {
    // ignore
  }
  const decrees = [
    "“Empires fall to blades. Kingdoms fall to ledgers.”",
    "“The High Council convenes. All debts come due.”",
    "“A treaty signed in gold is harder to break than one signed in blood.”",
    "“The grove regrows faster than the war can burn it.”",
    "“Knowledge is not power; it is permission.”",
    "“Strike the wall if you must. Learn what it costs to move the unmovable.”",
    "“All have sought the throne. All have perished.”"
  ];

  let i = 0;
  window.setInterval(() => {
    i = (i + 1) % decrees.length;
    el.style.opacity = "0";
    window.setTimeout(() => {
      el.textContent = decrees[i];
      el.style.opacity = "1";
    }, 180);
  }, 4200);
}

function initWaitlist() {
  const form = $("waitlistForm");
  const emailEl = $("waitlistEmail");
  const msg = $("waitlistMsg");
  const exportBtn = $("exportWaitlistBtn");
  if (!form || !emailEl || !msg || !exportBtn) return;

  function load() {
    try {
      return JSON.parse(localStorage.getItem("aeonis.waitlist") || "[]");
    } catch {
      return [];
    }
  }
  function save(list) {
    try {
      localStorage.setItem("aeonis.waitlist", JSON.stringify(list));
    } catch {
      // ignore
    }
  }
  function setMsg(t) {
    msg.textContent = t || "";
  }
  function normalizeEmail(e) {
    return String(e || "").trim().toLowerCase();
  }
  function validEmail(e) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e);
  }

  const existing = load();
  if (existing.length) setMsg(`${existing.length} oath${existing.length === 1 ? "" : "s"} recorded on this device.`);

  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const email = normalizeEmail(emailEl.value);
    if (!validEmail(email)) {
      setMsg("That email doesn’t look right. Try again.");
      return;
    }

    const list = load();
    if (!list.some((x) => normalizeEmail(x.email) === email)) {
      list.push({ email, ts: new Date().toISOString() });
      save(list);
    }

    try {
      await navigator.clipboard.writeText(email);
      setMsg(`Oath recorded. (Copied: ${email})`);
    } catch {
      setMsg(`Oath recorded: ${email}`);
    }

    emailEl.value = "";
  });

  exportBtn.addEventListener("click", () => {
    const list = load();
    const rows = [["email", "timestamp"], ...list.map((x) => [x.email, x.ts])];
    const csv = rows
      .map((r) =>
        r
          .map((cell) => `"${String(cell ?? "").replace(/"/g, '""')}"`)
          .join(",")
      )
      .join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "aeonis-waitlist.csv";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    setMsg(`Exported ${list.length} email${list.length === 1 ? "" : "s"}.`);
  });
}

async function init() {
  // Theme first (avoid flash)
  setTheme(getTheme());

  wireEvents();
  initDecrees();
  initWaitlist();

  try {
    const res = await fetch("content-manifest.json", { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status} when loading content-manifest.json`);
    state.manifest = await res.json();
  } catch (e) {
    state.manifest = {
      appName: "Aeonis Codex",
      version: 1,
      categories: [
        {
          id: "start",
          label: "Start Here",
          color: "gold",
          docs: [{ title: "Repo README", path: "README.md", description: "High-level overview." }]
        }
      ]
    };
    showViewerState("error", { message: `Failed to load content-manifest.json: ${e?.message || e}` });
  }

  buildFlatIndex(state.manifest);
  renderCategorySelect();
  renderJourneys();

  // Initial list render
  const docs = await filterDocs();
  renderDocList(docs);

  // Route (hash deep link)
  await route();
}

document.addEventListener("DOMContentLoaded", init);

