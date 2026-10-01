import { readFileSync, existsSync } from "node:fs";
import { parseSync } from "@slidev/parser/core";

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

const videos = slides.flatMap((slide) => [...slide.content.matchAll(/<StepVideo\s+src="([^"]+)"/g)].map((match) => match[1]));
const missing = videos.filter((src) => !existsSync(publicFile(src)));

console.log(`Slides: ${slides.length}`);
console.log(`Manim videos referenced: ${videos.length}`);
if (missing.length) {
  warn(`Not rendered yet: ${missing.join(", ")}`);
  warn("Run: ./scripts/render-animations.sh");
} else {
  console.log("All referenced videos exist.");
}

// Stepped videos: every data-video-step on a slide must map to a stop in its steps file.
const problems = [];
for (const { content } of slides) {
  const stepsFile = content.match(/<StepVideo[^>]*\ssteps="([^"]+)"/)?.[1];
  const steps = [...content.matchAll(/data-video-step="(\d+)"/g)].map((match) => Number(match[1]));
  if (/<video\b/.test(content)) problems.push("<video> direkt in der Folie gefunden (StepVideo verwenden).");
  if ([...content.matchAll(/<[^>]*data-video-step[^>]*>/g)].some(([tag]) => !/\bv-click\b/.test(tag))) {
    problems.push("data-video-step ohne v-click am selben Element.");
  }
  if (!stepsFile) {
    if (steps.length) problems.push("data-video-step ohne StepVideo mit steps.");
    continue;
  }
  if (!existsSync(publicFile(stepsFile))) {
    problems.push(`${stepsFile} fehlt – Animationen neu rendern.`);
    continue;
  }
  const { stops } = JSON.parse(readFileSync(publicFile(stepsFile), "utf8"));
  const expected = stops.map((_, index) => index + 1).join(",");
  const actual = [...new Set(steps)].sort((a, b) => a - b).join(",");
  if (expected !== actual) problems.push(`${stepsFile}: ${stops.length} Stops, Folie nutzt Schritte [${actual}].`);
}
problems.forEach((problem) => warn(`Video-Steps: ${problem}`));
if (!problems.length) console.log("All stepped videos match their clicks.");

// Slide conventions: content slides start empty (only eyebrow + heading) and carry a key message.
// Anything with v-click, the eyebrow, the heading and the static fineprint may be present;
// everything else would already be readable on slide change.
const SKIP_CLASS = /\b(eyebrow|fineprint)\b/;

function visibleText(markdown) {
  const slide = markdown.replace(/<!--[\s\S]*?-->/g, "");
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
slides.forEach(({ content, frontmatter }, index) => {
  if (/\b(hero|chapter|break-slide|closing|quiz-slide)\b/.test(frontmatter.class ?? "")) return;
  const title = content.match(/class="eyebrow">([^<]*)</)?.[1]?.trim() ?? `Folie ${index + 1}`;
  if (!/class="[^"]*\b(bottom-line|callout)\b/.test(content)) noKeyMessage.push(title);
  const rest = visibleText(content);
  if (rest) notEmptyOnEnter.push(`${title}: „${rest.slice(0, 40)}…“`);
});
if (noKeyMessage.length) warn(`Ohne Kernaussage: ${noKeyMessage.join(" · ")}`);
if (notEmptyOnEnter.length) warn(`Sichtbar schon beim Folienwechsel: ${notEmptyOnEnter.join(" · ")}`);
if (!noKeyMessage.length && !notEmptyOnEnter.length) console.log("All content slides start empty and carry a key message.");

if (slides.length < 25) {
  throw new Error("Expected at least 25 slides.");
}

if (strict && warnings.length) {
  throw new Error(`${warnings.length} Warnung(en) im strikten Modus – siehe oben.`);
}
