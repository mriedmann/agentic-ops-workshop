import { execFileSync, spawnSync } from "node:child_process";
import { readFileSync, rmSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { parseSync, stringify } from "@slidev/parser/core";

// Condensed PDF for participants: every slide once in its final state, except video
// slides, which get one page per video stop. The script writes a temporary deck in which
// each video slide is repeated with its step lines cut off after step 1, 2, …, and exports
// that deck without --with-clicks. Notes go into a separate PDF (Slidev cannot combine them).
const root = fileURLToPath(new URL("../", import.meta.url));
const entry = "slides-handout.md";

// A step line advances the video (see "Animations" in AGENTS.md).
const isStep = (line) => /^(- |\d+\. |\[(video|anim)\]\s*$)/.test(line);

function videoCopies(slide) {
  const raw = slide.raw;
  const frontmatterEnd = raw.indexOf("\n---\n", 4) + 5;
  const notesStart = raw.lastIndexOf("<!--") >= frontmatterEnd ? raw.lastIndexOf("<!--") : raw.length;
  const head = raw.slice(0, frontmatterEnd);
  const body = raw.slice(frontmatterEnd, notesStart).split("\n");
  const notes = raw.slice(notesStart);
  const steps = body.filter(isStep).length;

  return Array.from({ length: steps }, (_, index) => {
    const last = index === steps - 1;
    let seen = 0;
    const lines = body.filter((line) => {
      if (isStep(line)) return ++seen <= index + 1;
      return last || !line.startsWith(">");
    });
    return { ...slide, raw: head + lines.join("\n") + (last ? notes : "\n") };
  });
}

const deck = parseSync(readFileSync(`${root}slides.md`, "utf8"), "slides.md");
deck.slides = deck.slides.flatMap((slide) => (slide.frontmatter.video || slide.frontmatter.anim ? videoCopies(slide) : [slide]));
// export-notes opens /presenter/print without a hash and would get the cover slide instead.
deck.slides[0].raw = deck.slides[0].raw.replace(/^routerMode: hash$/m, "routerMode: history");

// Playwright needs an absolute path; its bundled Chromium cannot play the H.264 videos.
const chrome =
  process.env.CHROME_PATH || spawnSync("sh", ["-c", "command -v google-chrome"], { encoding: "utf8" }).stdout.trim();
if (!chrome) throw new Error("Google Chrome not found; set CHROME_PATH.");

const slidev = (...args) => execFileSync("npx", ["slidev", ...args], { cwd: root, stdio: "inherit" });

writeFileSync(`${root}${entry}`, stringify(deck));
try {
  slidev("export", entry, "--output", "slides-handout.pdf", "--executable-path", chrome);
  slidev("export-notes", entry, "--output", "slides-handout-notes.pdf");
} finally {
  rmSync(`${root}${entry}`, { force: true });
}
console.log(`${deck.slides.length} pages: slides-handout.pdf, notes: slides-handout-notes.pdf`);
