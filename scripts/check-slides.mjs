import { readFileSync, existsSync } from "node:fs";

const html = readFileSync(new URL("../index.html", import.meta.url), "utf8");
const sources = [...html.matchAll(/<source\s+src="([^"]+)"/g)].map((match) => match[1]);
const sections = [...html.matchAll(/<section(?:\s|>)/g)].length;
const missing = sources.filter((source) => !existsSync(new URL(`../${source}`, import.meta.url)));

console.log(`Slides: ${sections}`);
console.log(`Manim videos referenced: ${sources.length}`);
if (missing.length) {
  console.warn(`Not rendered yet: ${missing.join(", ")}`);
  console.warn("Run: ./scripts/render-animations.sh");
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
problems.forEach((problem) => console.warn(`Video-Steps: ${problem}`));
if (!problems.length) console.log("All stepped videos match their fragments.");

if (sections < 25) {
  throw new Error("Expected at least 25 slides.");
}
