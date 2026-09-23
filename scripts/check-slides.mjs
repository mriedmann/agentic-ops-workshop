import { readFileSync, existsSync } from "node:fs";

// --strict turns every warning into a failure; used by CI before deploying.
const strict = process.argv.includes("--strict");
const warnings = [];
const warn = (message) => {
  warnings.push(message);
  console.warn(message);
};

const html = readFileSync(new URL("../index.html", import.meta.url), "utf8");
const sources = [...html.matchAll(/<source\s+src="([^"]+)"/g)].map((match) => match[1]);
const sections = [...html.matchAll(/<section(?:\s|>)/g)].length;
const missing = sources.filter((source) => !existsSync(new URL(`../${source}`, import.meta.url)));

console.log(`Slides: ${sections}`);
console.log(`Manim videos referenced: ${sources.length}`);
if (missing.length) {
  warn(`Not rendered yet: ${missing.join(", ")}`);
  warn("Run: ./scripts/render-animations.sh");
} else {
  console.log("All referenced videos exist.");
}

// Stepped videos: every data-video-step on a slide must map to a stop in its steps file.
const problems = [];
for (const [, slide] of html.matchAll(/<section[^>]*>([\s\S]*?)<\/section>/g)) {
  const stepsFile = slide.match(/data-steps="([^"]+)"/)?.[1];
  const steps = [...slide.matchAll(/data-video-step="(\d+)"/g)].map((match) => Number(match[1]));
  if (/data-autoplay/.test(slide)) problems.push("Video mit data-autoplay gefunden (Videos werden per Klick gesteuert).");
  if (!stepsFile) {
    if (steps.length) problems.push("data-video-step ohne Video mit data-steps.");
    continue;
  }
  const file = new URL(`../${stepsFile}`, import.meta.url);
  if (!existsSync(file)) {
    problems.push(`${stepsFile} fehlt – Animationen neu rendern.`);
    continue;
  }
  const { stops } = JSON.parse(readFileSync(file, "utf8"));
  const expected = stops.map((_, index) => index + 1).join(",");
  const actual = [...new Set(steps)].sort((a, b) => a - b).join(",");
  if (expected !== actual) problems.push(`${stepsFile}: ${stops.length} Stops, Folie nutzt Schritte [${actual}].`);
}
problems.forEach((problem) => warn(`Video-Steps: ${problem}`));
if (!problems.length) console.log("All stepped videos match their fragments.");

// Slide conventions: content slides start empty (only eyebrow + heading) and carry a key message.
// Anything inside a .fragment, the notes, the eyebrow, the heading and the static
// fineprint may be present; everything else would already be readable on slide change.
const SKIP_CLASS = /\b(fragment|notes|eyebrow|fineprint|media-fallback)\b/;

function visibleText(slide) {
  const tag = /<(\/?)([a-z0-9]+)([^>]*)>/gi;
  let text = "";
  let skipDepth = 0;
  let depth = 0;
  let last = 0;
  let match;
  while ((match = tag.exec(slide))) {
    if (!skipDepth) text += slide.slice(last, match.index);
    last = tag.lastIndex;
    const [, closing, name, attrs] = match;
    if (name === "br" || name === "source" || attrs.endsWith("/")) continue;
    if (closing) {
      depth -= 1;
      if (skipDepth && depth < skipDepth) skipDepth = 0;
      continue;
    }
    depth += 1;
    if (!skipDepth && (SKIP_CLASS.test(attrs) || name === "h1" || name === "h2" || name === "video")) skipDepth = depth;
  }
  if (!skipDepth) text += slide.slice(last);
  return text.replace(/&[a-z]+;/g, "").replace(/\s+/g, " ").trim();
}

const noKeyMessage = [];
const notEmptyOnEnter = [];
let index = 0;
for (const [, attrs, slide] of html.matchAll(/<section([^>]*)>([\s\S]*?)<\/section>/g)) {
  index += 1;
  if (/class="[^"]*\b(hero|chapter|break-slide|closing|quiz-slide)\b/.test(attrs)) continue;
  const title = slide.match(/class="eyebrow">([^<]*)</)?.[1]?.trim() ?? `Folie ${index}`;
  if (!/class="[^"]*\b(bottom-line|callout)\b/.test(slide)) noKeyMessage.push(title);
  const rest = visibleText(slide);
  if (rest) notEmptyOnEnter.push(`${title}: „${rest.slice(0, 40)}…“`);
}
if (noKeyMessage.length) warn(`Ohne Kernaussage: ${noKeyMessage.join(" · ")}`);
if (notEmptyOnEnter.length) warn(`Sichtbar schon beim Folienwechsel: ${notEmptyOnEnter.join(" · ")}`);
if (!noKeyMessage.length && !notEmptyOnEnter.length) console.log("All content slides start empty and carry a key message.");

if (sections < 25) {
  throw new Error("Expected at least 25 slides.");
}

if (strict && warnings.length) {
  throw new Error(`${warnings.length} Warnung(en) im strikten Modus – siehe oben.`);
}
