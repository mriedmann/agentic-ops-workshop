// Slide syntax: turns the compact Markdown of slides.md into the HTML the deck is styled for.
//
// A slide is a frontmatter block (eyebrow, chapter, video, …) plus a body of headings, lists,
// `::: kind` blocks, a key message (`> …`) and components. expandSlide() returns the HTML for
// one slide and numbers every click in reading order, so slides.md never contains click numbers.
// Used by setup/transformers.ts (Slidev) and scripts/check-slides.mjs. See AGENTS.md for the syntax.

const esc = (text) => text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const nn = (index) => String(index + 1).padStart(2, "0");

// Inline markup: `code`, **strong**, *accent*.
const INLINE = /`([^`]+)`|\*\*([^*]+)\*\*|\*([^*]+)\*/g;

function tokens(text) {
  const out = [];
  let last = 0;
  for (const match of text.matchAll(INLINE)) {
    if (match.index > last) out.push({ type: "text", value: text.slice(last, match.index) });
    const type = match[1] != null ? "code" : match[2] != null ? "strong" : "em";
    out.push({ type, value: match[1] ?? match[2] ?? match[3] });
    last = match.index + match[0].length;
  }
  if (last < text.length) out.push({ type: "text", value: text.slice(last) });
  return out;
}

function inline(text) {
  return tokens(text)
    .map(({ type, value }) => {
      if (type === "code") return `<code>${esc(value)}</code>`;
      if (type === "strong") return `<b>${esc(value)}</b>`;
      if (type === "em") return `<span class="accent">${esc(value)}</span>`;
      return esc(value);
    })
    .join("");
}

// Trailing `{.class .other}` sets the classes of a line.
function splitClasses(text) {
  const match = text.match(/\s*\{((?:\s*\.[\w-]+)+)\s*\}\s*$/);
  if (!match) return { text, classes: null };
  return { text: text.slice(0, match.index), classes: match[1].trim().split(/\s+/).map((c) => c.slice(1)).join(" ") };
}

// An item split into its parts: the first **strong**, *em* and `code`, and the plain text around them.
function parts(raw, index) {
  const { text, classes } = splitClasses(raw);
  const all = tokens(text);
  const first = (type) => {
    const token = all.find((t) => t.type === type);
    return token ? esc(token.value) : "";
  };
  return {
    index,
    nn: nn(index),
    classes,
    strong: first("strong"),
    em: first("em"),
    code: first("code"),
    text: esc(all.filter((t) => t.type === "text").map((t) => t.value).join("").replace(/\s+/g, " ").trim()),
    html: inline(text.trim()),
    tokens: all,
  };
}

const ARROW = "<span>→</span>";

// Block kinds for `::: kind`. `item(p, click)` renders one list item; `click` is the v-click
// attribute for that item, or empty when the whole block appears at once (`once`).
const KINDS = {
  cards: { cls: "question-grid", item: (p, c) => `<div class="question-card"${c}><span class="question-number">${p.nn}</span><p>${p.text}</p></div>` },
  timeline: { cls: "timeline", item: (p, c) => `<div class="timeline-item"${c}><b>${p.nn}</b><span>${p.text}</span><small>${p.em}</small></div>` },
  notes: { cls: "note-grid", item: (p, c) => `<div${c}><b>${p.strong}</b><span>${p.text}</span></div>` },
  calc: { cls: "calc", item: (p, c) => `<div${c}><b>${p.strong}</b><span>${p.text}</span><i>${p.em}</i></div>` },
  definitions: { cls: "definition-list", item: (p, c) => `<div${c}><b>${p.strong}</b><span>${p.text}</span><code>${p.code}</code></div>` },
  failures: { cls: "failure-grid", item: (p, c) => `<article class="failure"${c}><b>${p.nn}</b><h3>${p.strong}</h3><p>${p.text}</p><span>${p.em}</span></article>` },
  controls: { cls: "control-layers", item: (p, c) => `<div class="control"${c}><span>${p.nn}</span><b>${p.strong}</b><small>${p.text}</small></div>` },
  takeaways: { cls: "takeaways", item: (p, c) => `<div${c}><b>${p.nn}</b><p>${p.text}</p></div>` },
  truths: { cls: "two-truths", item: (p, c) => `<p${c}>${p.html}</p>` },
  scale: { cls: "autonomy-scale", separator: "<i></i>", item: (p, c) => `<article${c}><span>${p.text}</span><b>${p.strong}</b><small>${p.em}</small></article>` },
  statement: { cls: "big-statement", item: (p, c) => (p.index === 0 ? `<span${c}>${p.html}</span>` : `<strong${c}>${p.html}</strong>`) },
  // Question on one click, answer on the next.
  "quiz-cards": { cls: "note-grid wide quiz-cards", clicksPerItem: 2, item: (p, c, c2) => `<div${c}><b>${p.strong}</b><span${c2}>${p.text}</span></div>` },
  roadmap: {
    cls: "roadmap",
    tag: "ol",
    item: (p, c) => `<li${p.classes ? ` class="${p.classes}"` : ""}${c}><b>${p.nn}</b><strong>${p.strong}</strong><span>${p.text}</span><code>${p.code}</code></li>`,
    caption: (text, c) => `<div class="layer-label"${c}>${inline(text)}</div>`,
  },
  // Blocks that appear as a whole.
  flow: { cls: "rag-flow", once: true, separator: ARROW, item: (p, _c, _c2, last) => `<div class="rag-node${last ? " hot" : ""}">${p.text}${p.em ? `<small>${p.em}</small>` : ""}</div>` },
  trace: { cls: "trace", once: true, separator: ARROW, item: (p) => `<div><small>${p.text}</small><b>${p.strong}</b></div>` },
  chips: { cls: "chips", once: true, item: (p) => `<span>${p.text}</span>` },
  observability: { cls: "observability", once: true, item: (p) => `<span>${p.text}</span>` },
  canvas: { cls: "canvas-grid", once: true, item: (p) => `<div><small>${p.nn}</small><b>${p.strong}</b><span>${p.text}</span></div>` },
  example: { cls: "inject-example", once: true, item: (p) => `<small>${p.text}</small><code>${p.code}</code>` },
  sentence: {
    cls: "sentence-template",
    once: true,
    line: (text) => tokens(text).map((t) => (t.type === "strong" ? `<b>${esc(t.value)}</b>` : `<span>${esc(t.value.trim())}</span>`)).join(""),
  },
  // Options appear together; the caption "Lösung: B — …" takes two clicks (label, then answer).
  quiz: {
    cls: "quiz-options",
    once: true,
    item: (p) => {
      const [, letter, rest] = p.text.match(/^(\S+)\s+(.*)$/) ?? [];
      return `<div class="quiz-option">${letter} <span>${rest}</span></div>`;
    },
    caption: (text, c, c2) => {
      const match = text.match(/^([^:]+:)\s*(\S+)\s+(.*)$/);
      if (!match) throw new Error(`quiz: caption needs the form "Lösung: B — text", got "${text}"`);
      return `<p class="answer-label"${c}>${esc(match[1])}</p>\n<div class="answer"${c2}>${esc(match[2])} <span>${esc(match[3])}</span></div>`;
    },
    captionClicks: 2,
  },
};

export const BLOCK_KINDS = Object.keys(KINDS);

const ITEM = /^(?:-|\d+\.)\s+(.*)$/;

function parseBody(content) {
  const lines = content.replace(/\r/g, "").split("\n");
  const blocks = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) {
      i += 1;
      continue;
    }
    let match;
    if ((match = line.match(/^(#{1,2})\s+(.*)$/))) {
      const level = match[1].length;
      const rows = [];
      while (i < lines.length && (match = lines[i].match(/^(#{1,2})\s+(.*)$/)) && match[1].length === level) {
        rows.push(match[2].trim());
        i += 1;
      }
      blocks.push({ type: "heading", level, rows });
    } else if ((match = line.match(/^:::\s*([\w-]+)\s*(.*)$/))) {
      const block = { type: "block", kind: match[1], words: match[2].trim().split(/\s+/).filter(Boolean), items: [], lines: [] };
      i += 1;
      while (i < lines.length && lines[i].trim() !== ":::") {
        const row = lines[i].trim();
        const item = row.match(ITEM);
        if (item) block.items.push(item[1]);
        else if (row) block.lines.push(row);
        i += 1;
      }
      if (i >= lines.length) throw new Error(`"::: ${block.kind}" is not closed with ":::"`);
      i += 1;
      blocks.push(block);
    } else if ((match = line.match(/^>\s+(.*)$/))) {
      blocks.push({ type: "key", ...splitClasses(match[1].trim()) });
      i += 1;
    } else if (line.trim() === "[video]") {
      blocks.push({ type: "videostep" });
      i += 1;
    } else if (/^-\s+/.test(line) || /^\d+\.\s+/.test(line)) {
      const ordered = /^\d/.test(line);
      const marker = ordered ? /^\d+\.\s+(.*)$/ : /^-\s+(.*)$/;
      const items = [];
      while (i < lines.length && (match = lines[i].match(marker))) {
        items.push(match[1]);
        i += 1;
      }
      blocks.push({ type: ordered ? "steps" : "bullets", items });
    } else if (line.startsWith("<")) {
      const rows = [];
      while (i < lines.length && lines[i].trim()) {
        rows.push(lines[i]);
        i += 1;
      }
      blocks.push({ type: "html", html: rows.join("\n") });
    } else {
      blocks.push({ type: "paragraph", ...splitClasses(line.trim()) });
      i += 1;
    }
  }
  return blocks;
}

/**
 * @param {string} content  slide body (Markdown, without frontmatter and notes)
 * @param {Record<string, any>} frontmatter
 * @returns {string} HTML for the slide
 */
export function expandSlide(content, frontmatter = {}) {
  const slideClasses = String(frontmatter.class ?? "").split(/\s+/);
  const isHero = slideClasses.includes("hero");
  const isBreak = slideClasses.includes("break-slide");
  const isChapter = frontmatter.chapter != null;
  const isStatic = isHero || isBreak || isChapter;
  const video = frontmatter.video;

  let clicks = 0;
  let videoSteps = 0;
  const click = () => ` v-click="${++clicks}"`;
  const videoStep = () => (video ? ` data-video-step="${++videoSteps}"` : "");

  const blocks = parseBody(content);
  const keyIndex = blocks.findIndex((b) => b.type === "key");
  if (blocks.filter((b) => b.type === "key").length > 1) throw new Error("Only one key message (> …) per slide.");
  const hasKey = keyIndex !== -1;

  const head = [];
  const body = [];
  const tail = [];
  let key = "";

  if (frontmatter.eyebrow != null) head.push(`<div class="eyebrow">${esc(String(frontmatter.eyebrow))}</div>`);

  blocks.forEach((block, index) => {
    if (hasKey && index > keyIndex && !["paragraph"].includes(block.type)) {
      throw new Error("The key message (> …) must be the last click of the slide; only fineprint may follow it.");
    }
    switch (block.type) {
      case "heading":
        head.push(`<h${block.level}>${block.rows.map(inline).join("<br />")}</h${block.level}>`);
        break;
      case "bullets":
        body.push(`<ul class="clean-list">\n${block.items.map((item) => `  <li${click()}${videoStep()}>${inline(item)}</li>`).join("\n")}\n</ul>`);
        break;
      case "steps":
        body.push(
          `<ol class="demo-steps">\n${block.items
            .map((item, i) => {
              const p = parts(item, i);
              return `  <li${click()}><b>${p.strong || p.nn}</b><span>${p.text}</span></li>`;
            })
            .join("\n")}\n</ol>`,
        );
        break;
      case "videostep":
        if (!video) throw new Error("[video] is only allowed on slides with `video:` in the frontmatter.");
        body.push(`<span class="video-step"${click()}${videoStep()}></span>`);
        break;
      case "block":
        body.push(renderBlock(block, click));
        break;
      case "html":
        body.push(renderHtml(block.html, click, () => clicks, (n) => (clicks += n)));
        break;
      case "paragraph": {
        const classes = block.classes ?? (isHero ? "lede" : isBreak ? "break-prompt" : "");
        if (classes.split(" ").includes("fineprint")) {
          tail.push(`<p class="${classes}${hasKey ? " stacked" : ""}">${inline(block.text)}</p>`);
        } else if (hasKey && index > keyIndex) {
          throw new Error("The key message (> …) must be the last click of the slide; only fineprint may follow it.");
        } else if (isBreak && block.classes == null) {
          body.push(`<div class="break-prompt">${inline(block.text)}</div>`);
        } else {
          body.push(`<p${classes ? ` class="${classes}"` : ""}${isStatic ? "" : click()}>${inline(block.text)}</p>`);
        }
        break;
      }
      case "key":
        break;
    }
  });

  if (hasKey) {
    const block = blocks[keyIndex];
    key = `<p class="${block.classes ?? "bottom-line"}"${click()}>${inline(block.text)}</p>`;
  }

  if (isChapter) {
    const number = String(frontmatter.chapter).padStart(2, "0");
    return [`<div class="chapter-number">${number}</div>`, `<div>${head.join("")}</div>`, ...body, ...tail].join("\n");
  }

  if (video) {
    const label = inline(String(frontmatter.videoLabel ?? `Animation ${video}`));
    return [
      `<div class="video-copy">`,
      ...head,
      ...body,
      ...(key ? [key] : []),
      `</div>`,
      `<StepVideo src="media/${video}.mp4" steps="media/${video}.steps.json">${label}</StepVideo>`,
      ...tail,
    ].join("\n");
  }

  return [...head, ...body, ...tail, ...(key ? [key] : [])].join("\n");
}

function renderBlock(block, click) {
  const kind = KINDS[block.kind];
  if (!kind) throw new Error(`Unknown block "::: ${block.kind}". Known: ${BLOCK_KINDS.join(", ")}`);
  const once = kind.once || block.words.includes("once");
  const extra = block.words.filter((word) => word !== "once");
  const cls = [kind.cls, ...extra].join(" ");
  const tag = kind.tag ?? "div";
  const wrapperClick = once ? click() : "";

  let inner;
  if (kind.line) {
    if (block.lines.length !== 1) throw new Error(`"::: ${block.kind}" takes exactly one line of text.`);
    inner = kind.line(block.lines[0]);
  } else {
    if (!block.items.length) throw new Error(`"::: ${block.kind}" needs list items (- … or 1. …).`);
    inner = block.items
      .map((item, index) => {
        const c = once ? "" : click();
        const c2 = !once && kind.clicksPerItem === 2 ? click() : "";
        return kind.item(parts(item, index), c, c2, index === block.items.length - 1);
      })
      .join(kind.separator ?? "");
  }

  let html = `<${tag} class="${cls}"${wrapperClick}>${inner}</${tag}>`;
  if (!kind.line && block.lines.length) {
    if (!kind.caption) throw new Error(`"::: ${block.kind}" takes list items only, found: "${block.lines[0]}"`);
    if (block.lines.length > 1) throw new Error(`"::: ${block.kind}" takes one caption line.`);
    const c = click();
    const c2 = kind.captionClicks === 2 ? click() : "";
    html += `\n${kind.caption(block.lines[0], c, c2)}`;
  }
  return html;
}

// Raw HTML and components: a bare `v-click` gets the next click number; `clicks="N"` on a
// component reserves N clicks and passes the first one as `:at`.
function renderHtml(html, click, current, reserve) {
  return html.replace(/\sclicks="(\d+)"|\sv-click(?![=\w-])/g, (match, count) => {
    if (count == null) return click();
    const at = current() + 1;
    reserve(Number(count));
    return ` :at="${at}"`;
  });
}
