function getConfig() {
  const w = window;
  return {
    waitlistEndpoint: (w.AEONIS_WAITLIST_ENDPOINT || "").trim(),
    kickstarterUrl: (w.AEONIS_KICKSTARTER_URL || "").trim(),
    goatcounter: (w.AEONIS_GOATCOUNTER || "").trim(),
    social: w.AEONIS_SOCIAL || {}
  };
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
  if (!btn) return;
  if (!cfg.kickstarterUrl || !/^https?:\/\//i.test(cfg.kickstarterUrl)) {
    btn.hidden = true;
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
  const submitBtn = form.querySelector('button[type="submit"]');

  if (!endpoint) {
    if (msgEl) msgEl.textContent = "Waitlist coming soon — check back shortly.";
    if (submitBtn) submitBtn.disabled = true;
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
    } catch {
      if (msgEl) msgEl.textContent = "Couldn't submit right now. Please try again.";
    }
  });
}

function initFaq() {
  document.querySelectorAll(".faq__item").forEach((item) => {
    const btn = item.querySelector(".faq__q");
    const panel = item.querySelector(".faq__a");
    if (!btn || !panel) return;
    panel.hidden = true;
    btn.addEventListener("click", () => {
      const open = item.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      panel.hidden = !open;
    });
  });
}

function initLordCards() {
  document.querySelectorAll(".lordCard").forEach((card) => {
    card.setAttribute("tabindex", "0");
    card.setAttribute("role", "button");
    const toggle = () => card.classList.toggle("is-flipped");
    card.addEventListener("click", (ev) => {
      if (ev.target.closest("a")) return;
      toggle();
    });
    card.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter" || ev.key === " ") {
        ev.preventDefault();
        toggle();
      }
    });
  });
}

function initMobileNav() {
  const menuToggle = document.getElementById("menuToggle");
  const mobileNav = document.getElementById("mobileNav");
  if (!menuToggle || !mobileNav) return;
  menuToggle.addEventListener("click", () => {
    const open = mobileNav.hidden;
    mobileNav.hidden = !open;
    menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
  });
  mobileNav.addEventListener("click", (ev) => {
    if (ev.target.closest("a")) {
      mobileNav.hidden = true;
      menuToggle.setAttribute("aria-expanded", "false");
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initGoatCounter();
  initSocialLinks();
  initKickstarterButton();
  bindWaitlistForm(document.getElementById("waitlistFormHero"), "hero");
  bindWaitlistForm(document.getElementById("waitlistFormFooter"), "footer");
  initFaq();
  initLordCards();
  initMobileNav();
});
