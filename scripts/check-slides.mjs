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

if (sections < 25) {
  throw new Error("Expected at least 25 slides.");
}
