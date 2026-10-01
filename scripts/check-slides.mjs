import { readFileSync, existsSync } from "node:fs";
import { parseSync } from "@slidev/parser/core";
import { expandSlide } from "../setup/expand.mjs";

// --strict turns every warning into a failure; used by CI before deploying.
const strict = process.argv.includes("--strict");
const warnings = [];
const warn = (message) => {
  warnings.push(message);
  console.warn(message);
};

const root = new URL("../", import.meta.url);
const publicFile = (path) => new URL(`public/${path}`, root);
const { slides } = parseSync(readFileSync(new URL("slides.md", root), "utf8"), "slides.md");

// The checks run on the HTML each slide expands to (see setup/expand.mjs).
const syntaxErrors = [];
const decks = slides.map((slide, index) => {
  const title = slide.frontmatter.eyebrow ?? `Folie ${index + 1}`;
  try {
    return { ...slide, title, html: expandSlide(slide.content, slide.frontmatter) };
  } catch (error) {
    syntaxErrors.push(`Folie ${index + 1} (${title}): ${error.message}`);
    return { ...slide, title, html: "" };
  }
});
syntaxErrors.forEach((problem) => warn(`Syntax: ${problem}`));

const videos = decks.filter((slide) => slide.frontmatter.video).map((slide) => `media/${slide.frontmatter.video}.mp4`);
const missing = videos.filter((src) => !existsSync(publicFile(src)));

console.log(`Slides: ${slides.length}`);
console.log(`Manim videos referenced: ${videos.length}`);
if (missing.length) {
  warn(`Not rendered yet: ${missing.join(", ")}`);
  warn("Run: ./scripts/render-animations.sh");
} else {
  console.log("All referenced videos exist.");
}

// Stepped videos: the bullets and [video] steps of a slide must match the stops of its video.
const problems = [];
for (const { html, title } of decks) {
  const stepsFile = html.match(/<StepVideo[^>]*\ssteps="([^"]+)"/)?.[1];
  const steps = [...html.matchAll(/data-video-step="(\d+)"/g)].map((match) => Number(match[1]));
  if (/<video\b/.test(html)) problems.push(`${title}: <video> direkt in der Folie (video: im Frontmatter verwenden).`);
  if ([...html.matchAll(/<[^>]*data-video-step[^>]*>/g)].some(([tag]) => !/\bv-click\b/.test(tag))) {
    problems.push(`${title}: data-video-step ohne v-click am selben Element.`);
  }
  if (!stepsFile) continue;
  if (!existsSync(publicFile(stepsFile))) {
    problems.push(`${stepsFile} fehlt – Animationen neu rendern.`);
    continue;
  }
  const { stops } = JSON.parse(readFileSync(publicFile(stepsFile), "utf8"));
  const expected = stops.map((_, index) => index + 1).join(",");
  const actual = [...new Set(steps)].sort((a, b) => a - b).join(",");
  if (expected !== actual) problems.push(`${stepsFile}: ${stops.length} Stops, Folie nutzt Schritte [${actual}] (Aufzählungspunkte + [video]).`);
}
problems.forEach((problem) => warn(`Video-Steps: ${problem}`));
if (!problems.length) console.log("All stepped videos match their clicks.");

// Components: must exist, and `clicks="N"` must match the clicks the component uses (v-click="at", "at + 1", …).
const componentProblems = [];
const STATIC_SLIDE = /\b(hero|break-slide)\b/;
for (const { content, frontmatter, title } of decks) {
  for (const [tag, name] of content.matchAll(/<([A-Z]\w+)\b[^>]*>/g)) {
    const file = new URL(`components/${name}.vue`, root);
    if (!existsSync(file)) {
      componentProblems.push(`${title}: Komponente ${name} fehlt (components/${name}.vue).`);
      continue;
    }
    const source = readFileSync(file, "utf8");
    const offsets = [...source.matchAll(/v-click="at(?:\s*\+\s*(\d+))?"/g)].map((match) => Number(match[1] ?? 0));
    const used = offsets.length ? Math.max(...offsets) + 1 : 0;
    const declared = tag.match(/\sclicks="(\d+)"/)?.[1];
    if (used && Number(declared) !== used) componentProblems.push(`${title}: ${name} nutzt ${used} Klick(s), in der Folie steht clicks="${declared ?? "–"}".`);
    if (!used && declared) componentProblems.push(`${title}: ${name} hat keine eigenen Klicks, clicks="${declared}" entfernen (ggf. v-click setzen).`);
    const isStatic = STATIC_SLIDE.test(frontmatter.class ?? "") || frontmatter.chapter != null;
    if (!used && !isStatic && !/\sv-click\b/.test(tag)) componentProblems.push(`${title}: ${name} ist schon beim Folienwechsel sichtbar (v-click fehlt).`);
  }
}
componentProblems.forEach((problem) => warn(`Komponenten: ${problem}`));

// Slide conventions: content slides start empty (only eyebrow + heading) and carry a key message.
// Anything with v-click, the eyebrow, the heading and the static fineprint may be present;
// everything else would already be readable on slide change.
const SKIP_CLASS = /\b(eyebrow|fineprint)\b/;

function visibleText(slide) {
  const tag = /<(\/?)([A-Za-z0-9]+)([^>]*)>/g;
  let text = "";
  let skipDepth = 0;
  let depth = 0;
  let last = 0;
  let match;
  while ((match = tag.exec(slide))) {
    if (!skipDepth) text += slide.slice(last, match.index);
    last = tag.lastIndex;
    const [, closing, name, attrs] = match;
    if (name === "br" || attrs.endsWith("/")) continue;
    if (closing) {
      depth -= 1;
      if (skipDepth && depth < skipDepth) skipDepth = 0;
      continue;
    }
    depth += 1;
    if (!skipDepth && (SKIP_CLASS.test(attrs) || /\bv-click\b/.test(attrs) || ["h1", "h2", "StepVideo"].includes(name))) skipDepth = depth;
  }
  if (!skipDepth) text += slide.slice(last);
  return text.replace(/&[a-z]+;/g, "").replace(/\s+/g, " ").trim();
}

const noKeyMessage = [];
const notEmptyOnEnter = [];
for (const { html, frontmatter, title } of decks) {
  if (frontmatter.chapter != null || /\b(hero|break-slide|closing|quiz-slide)\b/.test(frontmatter.class ?? "")) continue;
  if (!/class="[^"]*\b(bottom-line|callout)\b/.test(html)) noKeyMessage.push(title);
  const rest = visibleText(html);
  if (rest) notEmptyOnEnter.push(`${title}: „${rest.slice(0, 40)}…“`);
}
if (noKeyMessage.length) warn(`Ohne Kernaussage: ${noKeyMessage.join(" · ")}`);
if (notEmptyOnEnter.length) warn(`Sichtbar schon beim Folienwechsel: ${notEmptyOnEnter.join(" · ")}`);
if (!noKeyMessage.length && !notEmptyOnEnter.length) console.log("All content slides start empty and carry a key message.");

if (slides.length < 25) {
  throw new Error("Expected at least 25 slides.");
}

if (strict && warnings.length) {
  throw new Error(`${warnings.length} Warnung(en) im strikten Modus – siehe oben.`);
}
