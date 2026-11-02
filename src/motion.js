/* =====================================================================
   TRIFECTA CLEANING: Motion layer
   Adds scroll-linked and staggered animation on top of the page's own
   CSS animations (the logo intro and the 3D proof report build stay as they are).
   Uses the vanilla `motion` package, so no framework is needed.
   Everything here is off for prefers-reduced-motion, and the page works
   without it: the inline script in <head> unhides content after 4s if this never runs.
   ===================================================================== */
import { animate, inView, scroll, stagger } from "motion";

const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const root = document.documentElement;

const EASE_OUT = [0.16, 1, 0.3, 1]; // matches --ease-out in the CSS
const SPRING = { type: "spring", visualDuration: 0.8, bounce: 0.22 };

const $ = (sel, scope = document) => scope.querySelector(sel);
const $$ = (sel, scope = document) => Array.from(scope.querySelectorAll(sel));

if (reduce) {
  root.classList.remove("mo");
} else {
  window.__tfMotion = 1;
  try {
    heroEntrance();
    reveals();
    foundingPlaces();
    scrollEffects();
    faqAccordion();
  } catch (err) {
    // Never leave content hidden if something goes wrong
    console.error(err);
    root.classList.remove("mo");
  }
}

/* ---------- helpers ---------- */

/** Pre-set the "from" state so elements don't flash before their delay starts. */
function hide(els, y = 24) {
  els.forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = `translateY(${y}px)`;
  });
}

/** Rise-and-fade in. Pauses the element's own CSS transitions so they don't fight Motion's frames,
 *  then hands transform back to the stylesheet so CSS hover effects keep working. */
function rise(els, { y = 24, delay = 0, each = 0.07, spring = SPRING } = {}) {
  if (!els.length) return Promise.resolve();
  els.forEach((el) => (el.style.transition = "none"));
  return animate(
    els,
    { opacity: [0, 1], y: [y, 0] },
    { delay: stagger(each, { startDelay: delay }), opacity: { duration: 0.6, ease: EASE_OUT }, y: spring }
  ).then(() =>
    els.forEach((el) => {
      el.style.transform = "";
      el.style.transition = "";
    })
  );
}

/* ---------- 1. Hero: words of the headline lift in once the logo intro has gone ---------- */

function splitWords(el) {
  // Keep the heading readable to screen readers as one phrase
  el.setAttribute("aria-label", el.textContent.replace(/\s+/g, " ").trim());
  const words = [];
  const walk = (node) => {
    Array.from(node.childNodes).forEach((child) => {
      if (child.nodeType === Node.TEXT_NODE) {
        const frag = document.createDocumentFragment();
        child.textContent.split(/(\s+)/).forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) {
            frag.appendChild(document.createTextNode(part));
          } else {
            const w = document.createElement("span");
            w.className = "mo-word";
            w.setAttribute("aria-hidden", "true");
            w.style.display = "inline-block";
            w.textContent = part;
            frag.appendChild(w);
            words.push(w);
          }
        });
        child.replaceWith(frag);
      } else if (child.nodeType === Node.ELEMENT_NODE) {
        walk(child);
      }
    });
  };
  walk(el);
  return words;
}

function heroEntrance() {
  const copy = $$(".hero-copy > *, .hero-meta > *");
  const h1 = $("#hero-h");
  const words = h1 ? splitWords(h1) : [];
  const others = copy.filter((el) => el !== h1);

  hide(others, 18);
  words.forEach((w) => {
    w.style.opacity = "0";
    w.style.transform = "translateY(0.55em)";
  });

  const play = () => {
    if (h1) h1.style.opacity = "1";
    animate(
      words,
      { opacity: [0, 1], y: ["0.55em", "0em"], filter: ["blur(8px)", "blur(0px)"] },
      { delay: stagger(0.045), duration: 0.7, ease: EASE_OUT }
    ).then(() => words.forEach((w) => (w.style.filter = "")));
    rise(others, { y: 18, delay: 0.25, each: 0.09 });
    // Lime glow behind the report breathes in
    const glow = $(".stage-glow");
    if (glow) animate(glow, { opacity: [0, 1], scale: [0.7, 1] }, { duration: 1.4, ease: EASE_OUT });
  };

  if (window.__tfIntroDone) play();
  else document.addEventListener("tf:intro-done", play, { once: true });
}

/* ---------- 2. Sections: each [data-reveal] block rises in, and its lists stagger ---------- */

const CHILDREN = [
  ".proof-items > .pi",
  ".whys > li",
  ".benefits > li",
  ".next > li",
  ".ticks > li",
  ".values > span",
  ".faq > details",
].join(",");

function reveals() {
  $$("[data-reveal]").forEach((block) => {
    const kids = $$(CHILDREN, block);
    const tags = $$(".tags > li", block);
    hide([block], 28);
    hide(kids, 16);
    tags.forEach((t) => {
      t.style.opacity = "0";
      t.style.transform = "scale(0.85)";
    });

    // Cards in a row carry --d (0, 1, 2) for their position: use it to cascade them
    const d = parseFloat(getComputedStyle(block).getPropertyValue("--d")) || 0;

    inView(
      block,
      () => {
        rise([block], { y: 28, delay: d * 0.09 });
        if (kids.length) rise(kids, { y: 16, delay: 0.2 + d * 0.09, each: 0.08 });
        if (tags.length) {
          animate(
            tags,
            { opacity: [0, 1], scale: [0.85, 1] },
            { delay: stagger(0.035, { startDelay: 0.15 }), opacity: { duration: 0.4 }, scale: { type: "spring", visualDuration: 0.5, bounce: 0.45 } }
          ).then(() => tags.forEach((t) => (t.style.transform = "")));
        }
      },
      { margin: "0px 0px -8% 0px", amount: 0.08 }
    );
  });
}

/* ---------- 3. Founding Five: the five places drop in and their lime bars draw across ---------- */

function foundingPlaces() {
  const list = $(".places");
  if (!list) return;
  const places = $$("li", list);
  const bars = $$("li i", list);
  places.forEach((p) => {
    p.style.opacity = "0";
    p.style.transform = "translateY(30px) scale(0.92)";
  });
  bars.forEach((b) => {
    b.style.transformOrigin = "0 50%";
    b.style.transform = "scaleX(0)";
  });

  inView(
    list,
    () => {
      animate(
        places,
        { opacity: [0, 1], y: [30, 0], scale: [0.92, 1] },
        { delay: stagger(0.1, { startDelay: 0.3 }), opacity: { duration: 0.5 }, y: SPRING, scale: SPRING }
      );
      animate(bars, { scaleX: [0, 1] }, { delay: stagger(0.1, { startDelay: 0.65 }), duration: 0.6, ease: EASE_OUT });
    },
    { amount: 0.4 }
  );
}

/* ---------- 4. Scroll-linked: progress bar, hero parallax, founder initial drift ---------- */

function scrollEffects() {
  const prog = $("#scroll-prog");
  if (prog) scroll(animate(prog, { scaleX: [0, 1] }, { ease: "linear" }));

  const hero = $("#hero");
  if (hero) {
    const heroOut = { target: hero, offset: ["start start", "end start"] };
    const bg = $(".hero-bg", hero);
    const grid = $(".hero-grid-lines", hero);
    const copy = $(".hero-copy", hero);
    if (bg) scroll(animate(bg, { y: [0, 160] }, { ease: "linear" }), heroOut);
    if (grid) scroll(animate(grid, { y: [0, 80] }, { ease: "linear" }), heroOut);
    if (copy) scroll(animate(copy, { y: [0, -50], opacity: [1, 0.35] }, { ease: "linear" }), heroOut);
  }

  const mark = $(".portrait-mark span");
  const portrait = $(".portrait");
  if (mark && portrait) {
    scroll(animate(mark, { y: [-50, 50], rotate: [-4, 4] }, { ease: "linear" }), {
      target: portrait,
      offset: ["start end", "end start"],
    });
  }

  const qmark = $(".qmark");
  if (qmark) {
    qmark.style.opacity = "0";
    inView(qmark, () => {
      animate(qmark, { opacity: [0, 1], scale: [0.4, 1], rotate: [-20, 0] }, { delay: 0.2, opacity: { duration: 0.3 }, scale: { type: "spring", visualDuration: 0.6, bounce: 0.5 }, rotate: SPRING });
    });
  }
}

/* ---------- 5. FAQ: answers slide open and closed instead of snapping ---------- */

function faqAccordion() {
  $$(".faq details").forEach((details) => {
    const summary = $("summary", details);
    const answer = $("p", details);
    if (!summary || !answer) return;
    let wantOpen = details.open;
    let running = null;
    const clear = () => {
      answer.style.height = answer.style.paddingBottom = answer.style.overflow = answer.style.opacity = "";
    };

    summary.addEventListener("click", (e) => {
      e.preventDefault();
      wantOpen = !wantOpen;
      // Start from wherever the answer is now, so a quick double-click reverses smoothly
      const fromH = details.open ? answer.offsetHeight : 0;
      const fromPad = details.open ? getComputedStyle(answer).paddingBottom : "0px";
      const fromO = details.open ? getComputedStyle(answer).opacity : "0";
      if (running) running.stop();

      details.open = true;
      clear();
      const toH = wantOpen ? answer.offsetHeight : 0;
      const toPad = wantOpen ? getComputedStyle(answer).paddingBottom : "0px";
      answer.style.overflow = "hidden";

      running = animate(
        answer,
        { height: [fromH, toH], paddingBottom: [fromPad, toPad], opacity: [fromO, wantOpen ? 1 : 0] },
        wantOpen ? { duration: 0.4, ease: EASE_OUT } : { duration: 0.28, ease: [0.4, 0, 1, 1] }
      );
      const mine = running;
      mine.then(() => {
        if (running !== mine) return;
        running = null;
        if (!wantOpen) details.open = false;
        clear();
      });
    });
  });
}
