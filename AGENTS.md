# AGENTS.md

Guidance for AI agents that create or modify workshop presentations in this repository.
It distils the planning outline and two rounds of review feedback on the "LLMs & Agentic
Operations" deck into rules that apply to any workshop built the same way.

The first half is about teaching (what a good workshop deck looks like), the second half
about this repository (how to build it with Slidev and anime.js). When a rule and a user
request conflict, the user wins; when a rule and your taste conflict, the rule wins.

## 1. Before writing slides

Clarify these points first. Ask the user for anything that is missing instead of guessing.

- **Audience:** who, how many, what they already know, what they explicitly do not know.
- **Duration:** total time including breaks.
- **Guiding question:** one question the whole day answers.
- **Outcome:** what participants can do afterwards, phrased as abilities ("explain …",
  "judge …", "decide …"), not as topics.
- **Scope:** what the workshop is about and what it is not about. Name the neighbouring
  topic that must not take over (in the reference deck: agents such as Claude Code or
  OpenCode, not chatbots).
- **Real setup:** if the workshop shows the customer's or team's own environment, get the
  actual architecture described. Diagrams must match reality, not a textbook version.

Then write an outline as a nested bullet list and have it confirmed before building slides.

## 2. Workshop structure

A workshop is not a lecture. Alternate input with interaction and move from understanding
to application. The reference structure:

1. **Warm-up (spoken, not on slides):** short introductions, show-of-hands questions,
   one or two experience reports from the room. Put these in the speaker notes of the
   first content slide.
2. **Learning goals:** three to four abilities, one card each.
3. **Agenda:** a timeline with the chapters and their durations, plus the guiding question.
4. **Foundations:** the concepts everyone needs, in a fixed sequence (see "guiding thread").
5. **Operations and limits:** what the foundations mean in practice, including failure modes.
6. **Comprehension check:** a short quiz before the break.
7. **Break:** its own slide, with a teaser for what follows.
8. **Application:** the building blocks of the actual subject and how they fit together.
9. **Showcase / demo:** incident or task, expectation exercise, demo, debrief.
10. **Transfer:** a structured group exercise in which participants apply the content to
    their own work.
11. **Close:** three takeaways and an exit ticket.

Every chapter gets a chapter slide. Give each chapter and each exercise step a time budget
and show it in the eyebrow (for example `BEGRIFFE · 8 MIN`).

## 3. Teaching rules

### Tone

- Factual and goal-oriented. The atmosphere may be relaxed, the wording must not sound
  like sales. No slogans, no hype, no rhetorical openers.
- Write in the language of the audience. Keep established technical terms in their
  original language.
- Avoid words the audience cannot place. Abstract labels such as "geometry", "addressable"
  or "injected" were all flagged; say what happens instead ("text from logs lands in the
  context and reads like an instruction").

### Every slide carries one statement

- A slide must be understandable later without the spoken track. The question "what is
  this slide trying to teach me?" needs one clear answer.
- Every content slide ends with a key message: one sentence at the bottom that states the
  takeaway (`> …` in the slide syntax).
- One central statement per slide. If the information on a slide is uneven or points in
  several directions, split it or cut it.
- A slide that adds no value is removed, not polished.
- Terms that deserve an explanation get their own slide. A list of three terms with one
  line each is too thin if the terms matter later.

### Slides start empty

- On slide change only the eyebrow and the title are visible. The speaker introduces the
  topic first; content then appears click by click.
- Nothing animates or appears on its own after a slide change.

### Guiding thread

- If the content follows a sequence (in the reference deck: Text → Token → Embedding →
  Attention → Feed Forward → Residual → Logits → Probabilities), introduce the whole
  sequence on one roadmap slide first.
- Each following slide shows where it is in that sequence (the step rail at the top right).
- Follow the established order of the field so participants can hold on to it and find it
  again in other material.

### One running example

- Use the same example on all slides of a chapter. Switching examples mid-way confuses
  more than it helps.
- Prefer a classic, non-technical example for foundations (reference deck: "Aus dem kleinen
  Setzling wurde ein großer …" → "Baum"). It shows that the concept is general, and it
  keeps the mechanism visible.
- Define the example once, in code, and derive all visuals from it (see `EXAMPLE_*` in
  `animations/example.ts`).

### Visuals

- Explanatory text needs visual support. If a slide explains a mechanism in words only,
  add a diagram or an animation.
- On slides with an animation the visual is large and the text small, not the other way round.
- Diagrams are simple and accessible: plain axes, few elements, labelled parts.
- Show real examples with real numbers and correct results instead of abstract shapes
  (a worked matrix multiplication rather than grid boxes). Abstract shapes invite wrong
  conclusions, for example about dimensions.
- Mark invented numbers as illustrative, in the fineprint or the notes.
- Do not oversimplify the core mechanism. Where good, detailed depictions exist in the
  field, a more complete animation is worth the effort.
- Position implies relation. Do not place unrelated elements next to each other, and give
  separate groups visible distance.

### Animations

- Animations never run on their own. They advance in their main steps by click, in sync
  with the bullet points.
- Each main step holds briefly so it can be discussed.

### Interaction

- **Quiz:** show all answer options at once (a short staggered entrance is fine). The
  solution takes two clicks: first only "Lösung:", then the answer. This prevents giving
  it away by accident.
- **Mini quiz:** for question cards, show the question on one click and the answer on the
  next, so the room can answer first.
- **Exercises:** state exactly what participants do, for how long, in which group size,
  and what the result is. A prompt that needs explaining is rewritten.
- **Group work:** use a recognised facilitation format and explain it on one slide before
  it starts (reference deck: 1-2-4-All). Then one slide per step, with a rail showing the
  current step.
- **Naming:** an exercise title must not promise something else. "Lab" sounds hands-on;
  do not use it for a discussion.

### Demo

- Before the demo, let participants form their own expectation (for example: which three
  pieces of evidence would you fetch first, and in which order?).
- Insert a placeholder slide that just says "Demo" so the switch is visible to the room.
  Put the preparation checklist and the fallback in its notes.
- After the demo, debrief with a few concrete questions and refer back to the expectation.

### Close

- Takeaways: three sentences.
- The last slide explains itself: what participants should write down, what happens with
  it, and why.

### Speaker notes

Every content slide has notes with:

- the learning goal of the slide ("Lernziel: …"),
- facilitation instructions (what to ask, when to wait, when to click),
- caveats and background for likely questions.

## 4. Repository

| Path | Purpose |
|---|---|
| `slides.md` | All slides in the compact slide syntax, speaker notes included |
| `setup/expand.mjs` | The slide syntax: turns a slide into HTML and numbers the clicks |
| `setup/transformers.ts` | Hooks `expand.mjs` into Slidev |
| `style.css` | The whole visual design |
| `layouts/deck.vue` | Slide frame, renders the step rail |
| `global-top.vue` | Footer: brand, chapter label, slide number, progress line |
| `components/StepRail.vue` | Step rails and their stations |
| `components/StepAnim.vue` | Click-stepped animation: plays a scene's timeline to the current step |
| `components/anim/*.vue` | Scene animations, one per animation |
| `components/*.vue` (others) | One-off diagrams used by a single slide |
| `animations/scene.ts` | Timeline setup and motion presets for the scenes |
| `animations/example.ts` | The running example and `softmax` |
| `scripts/check-slides.mjs` | Convention checks, run in CI |
| `scripts/export-handout.mjs` | Condensed handout PDF |

Commands:

```bash
npm install                     # once; Node 22.12 or newer
npm start                       # dev server on http://localhost:3030
npm run check                   # conventions, prints warnings
npm run check:strict            # same, fails on any warning; runs in CI
npm run build                   # static site
npm run export                  # PDF, one page per click
npm run export:handout          # condensed PDF for participants, plus notes PDF
```

`npm run check` expands every slide with `setup/expand.mjs` and enforces the conventions
below. It warns when:

- a slide uses the syntax wrongly (unknown block, key message not last, …),
- a referenced scene component is missing,
- the bullets and `[anim]` steps of a slide do not match the `tl.label("sN")` steps of its scene,
- a component is missing, its `clicks="N"` does not match the clicks it uses, or it is
  visible on a content slide before the first click,
- a content slide shows anything besides eyebrow, title and fineprint before the first click,
- a content slide has no key message.

Extend the check when you add a convention that can be verified mechanically.

### Where information lives

- `README.md` is for people: what the project is and how to run it locally. Keep it free
  of authoring rules. Update it when prerequisites or commands change.
- `AGENTS.md` (this file) holds everything about how to build and change a deck.
- Project specifics stay next to what they describe, not in either document:
  - reasons for a setting: a comment at the setting (`slides.md` headmatter,
    `.github/workflows/pages.yml`, `uno.config.ts`),
  - the running example: the `EXAMPLE_*` constants in `animations/example.ts`,
  - rail stations and brand text: `components/StepRail.vue`, `global-top.vue`,
  - anything the presenter must prepare or remember: the speaker notes of the slide
    where it matters (for example the demo checklist on the demo slide).

## 5. Writing slides

Slides are written in a compact Markdown syntax in `slides.md`, separated by `---` with a
frontmatter block. `setup/expand.mjs` turns each slide into the HTML that `style.css`
styles and numbers the clicks in reading order. Never write click numbers by hand.

```md
---
section: Betrieb
eyebrow: SPEICHER 2 · KV-CACHE
---

## Der Cache wächst mit
## dem *Kontext*

::: notes
- **Was liegt drin?** Pro Token, Layer und Head die Zwischenergebnisse K und V
- **Wozu?** Ohne Cache müsste das Modell den ganzen Text neu durchrechnen
:::

::: calc once
- **je Token** 2 (K und V) × 32 Layer × 4096 Werte × 2 Byte *≈ 0,5 MB*
- **8.000 Tokens** ein Request mit vollem Kontext *≈ 4 GB*
:::

> Kontextlänge × Parallelität ist die eigentliche Speichergrenze im Betrieb.

<!--
Lernziel: …

Hinweis für die Moderation …
-->
```

### Frontmatter

| Key | Effect |
|---|---|
| `section` | Chapter label in the footer |
| `eyebrow` | Small label above the title (category, time) |
| `chapter` | Makes the slide a chapter slide and shows this number (`chapter: 3` → "03") |
| `class` | Slide type: `hero` (cover, exit ticket), `break-slide` (break, demo placeholder), `quiz-slide`, `closing`; on animation slides `reverse` puts the animation left, `architecture-anim` gives it more width |
| `step` / `exercise` | Shows the step rail with these stations highlighted |
| `anim` | Makes the slide an animation slide showing `components/anim/<Name>.vue` (see Animations) |
| `bg` | Overrides the background colour |

Quote a value that contains `: ` or starts with a special character. Prose belongs in
the body, not in the frontmatter, so this rarely matters.

### Body

| Write | Result | Click |
|---|---|---|
| `## Title` | Title. Consecutive `##` lines are one title with a line break. `#` on the cover. | – |
| `- item` | Bullet list | one per item |
| `1. item` | Numbered steps (01, 02, …). `1. **5 MIN** text` shows the bold part instead of the number. | one per item |
| `::: kind` … `:::` | A block, see below | per kind |
| `> text` | Key message. Add ` {.callout}` for the centred box. Must be the last click. | last |
| `text {.fineprint}` | Small static note above the key message | – |
| `text {.class}` | Paragraph with that class | one |
| `[anim]` | A click that only advances the animation | one |
| `<Component v-click />` | A component that appears as a whole | one |
| `<Component clicks="2" />` | A component with its own clicks | as stated |

Inline markup: `*text*` is the accent colour, `**text**` the title part of an item,
`` `text` `` code. On hero and break slides plain paragraphs are static (lede, prompt);
chapter slides contain only the title.

Raw HTML still works for something no block covers: start the line with `<`, keep the
block free of blank lines, and write a bare `v-click` on every element that should
appear on a click. The numbers are filled in for you.

### Blocks

Every block takes a Markdown list, one item per line. Items appear one per click; add
`once` after the kind to show the whole block on one click. Further words after the kind
are added as CSS classes (`::: notes wide`, `::: cards two-by-two`).

| Kind | Item format | Notes |
|---|---|---|
| `cards` | `1. text` | Numbered cards |
| `timeline` | `1. label *duration*` | Agenda |
| `notes` | `- **Title** text` | Boxes with title and text |
| `quiz-cards` | `- **Question** answer` | Question on one click, answer on the next |
| `calc` | `- **Label** text *result*` | Calculation rows |
| `definitions` | ``- **Term** text `code` `` | Term, description, example |
| `failures` | `1. **Title** text *remedy*` | Numbered failure cards |
| `controls` | `1. **Title** text` | Numbered columns |
| `takeaways` | `1. text` | Numbered statements |
| `truths` | `- **Lead-in** rest of sentence` | Two contrasting statements |
| `scale` | `- LABEL **statement** *note*` | Steps on a scale, joined by a line |
| `statement` | `- sentence` | First item small, second large |
| `roadmap` | ``1. **Station** text `example` `` | ` {.layer}` marks a row; one extra line is the caption |
| `flow` | `- Node *detail*` | Always `once`; nodes joined by arrows, last one highlighted |
| `trace` | `- LABEL **text**` | Always `once`; boxes joined by arrows |
| `chips`, `observability` | `- text` | Always `once`; pills |
| `canvas` | `1. **Title** text` | Always `once`; numbered grid |
| `example` | ``- LABEL `code` `` | Always `once`; labelled code line |
| `sentence` | one line, `**gaps**` in bold | Always `once`; sentence template |
| `quiz` | `- A text`, then `Lösung: B — text` | Options together, then label, then answer |

Rules:

- **Slides start empty by construction:** everything in the body except the title and
  fineprint appears on a click.
- **Reuse a block kind** before inventing a new one. A new kind is one entry in `KINDS`
  in `setup/expand.mjs` plus its CSS; add a row to the table above.
- **One-off diagrams** (a figure used on one slide) are Vue components in `components/`.
  A component that appears as a whole takes `v-click` in the slide. A component with
  several clicks takes the prop `at` and uses `v-click="at"`, `v-click="at + 1"`, …; the
  slide states the count with `clicks="N"`.
- **Notes:** an HTML comment at the end of the slide. Separate paragraphs with blank lines.
- **New workshop:** adjust the brand text in `global-top.vue` and the stations in
  `components/StepRail.vue`; a `step`/`exercise` value must match a station key there.
- **Changing the syntax:** `expand.mjs` is the only place that produces slide HTML. After
  touching it, take screenshots of one slide per affected block kind before and after
  the change and confirm they are identical.

## 6. Animations

Animations are Vue components in `components/anim/`, drawn as SVG and animated with one
anime.js timeline each. There is nothing to render: the dev server shows changes at once.

- **One component per animation:** `anim: token-pipeline` in the frontmatter shows
  `components/anim/TokenPipeline.vue` (kebab-case → PascalCase).
- **Steps:** every bullet and every `[anim]` line of the slide is one step, in order: the
  first plays the timeline to `s1`, the second to `s2`, and so on. Put `[anim]` before or
  after the bullets for steps that have no bullet. The key message does not move the
  animation. `StepAnim.vue` plays forward on a live click and jumps to the step everywhere
  else (going back, overview, print, handout).

  ```md
  ---
  eyebrow: SCHRITT 1 · TOKEN
  anim: token-pipeline
  ---

  ## Text wird in Tokens
  ## *zerlegt und nummeriert*

  [anim]

  - Tokens sind Textstücke, keine Wörter
  - Jedes Token hat eine feste ID im Vokabular
  - „Setzling“ allein wird zu drei Tokens

  > Das Modell sieht keine Buchstaben, sondern nur eine Folge von Token-IDs.

  Tokenisierung ist kein Stemming. {.fineprint}
  ```

- **Template:** an SVG with `class="scene" viewBox="0 0 1280 720"` holding every element
  in its initial state (`style="opacity: 0"`, `transform: scaleX(0)`). The slide heading
  already names the topic; do not repeat it inside the scene. Use the space for large text.
- **Names:** mark animated elements with `data-part="…"`, not classes: deck classes
  (`answer`, `prompt`) and UnoCSS utilities would style them. `q("prompt blank")` returns
  every element with one of these parts. Text styles: `class="muted"`, `class="mono"`.
- **Timeline:** `useSceneTimeline(root, (tl, q) => { … })` from `animations/scene.ts`. The
  script reads top to bottom like the slide: `tl.add(q("row"), slideIn())`, … and ends
  each step with `tl.label("s1")`, `tl.label("s2")`, … written as literal strings; the
  check counts them against the slide's step lines.
- **Presets** in `animations/scene.ts`: `fadeIn`, `fadeOut`, `slideIn`, `growFromLeft`,
  `growFromCenter` (needs `style="transform-origin: center"`), `drawIn` for strokes
  (`tl.add(svg.createDrawable(q("arc")), drawIn())`) and `alongPath` for dots moving along
  a path. Reuse them before writing raw tweens.
- **Seeking must work both ways.** Give every tween explicit `[from, to]` values. A drawn
  line is visible before its step unless it sits in a group that starts at `opacity: 0`.
  A tween that starts exactly on a label shows its start value at that label; if that
  value is visible (a ripple starting at opacity 1), precede it with a short fade-in.
  Several `"<<"` positions in a loop chain onto each other; for parallel tweens take
  `const start = tl.duration` first and pass that number.
- **Transforms:** use `translateX`/`translateY`, not `x`/`y` (anime.js would animate the
  SVG attributes). Tweened transforms work on the element's own box; a static
  `transform="rotate(…)"` attribute keeps canvas coordinates.
- **Colours** come from the CSS tokens (`var(--cyan)`) in `style` bindings. anime.js cannot
  interpolate them; change a colour by crossfading two copies.
- **Data** of the running example comes from `animations/example.ts`. Mark invented
  values as illustrative in the slide's fineprint or notes.
- **Verify** with screenshots of every click state (`#/<slide>?clicks=<n>`, a fresh page per
  state so the animation has settled) and by clicking forwards and backwards in the
  browser. When a scene's timeline is needed in the console, set `window.__sceneDebug = true`
  before loading; `window.__sceneTimelines[<name>]` then holds it.

## 7. Export and publishing

- **PDF export** uses the Chromium that Playwright installs; `CHROME_PATH` selects another
  browser.
- **Handout:** `scripts/export-handout.mjs` writes a temporary deck in which each animation
  slide is repeated once per step (bullets cut off after that step, key message and
  notes only on the last copy) and exports it without clicks. Other slides appear once,
  in their final state. Keep animation slides to step lines, key message and fineprint, so
  this cut stays correct.
- **GitHub Pages:** `.github/workflows/pages.yml` runs the strict check on every push and
  pull request and deploys `main`. The site is built with the repository name as base
  path, and slide URLs use hash routing (`#/12`) so direct links work there. Reference
  assets relative to the base (`media/…`, not `/media/…`).
- A change is not done until the strict check passes and `npm run build` succeeds.

## 8. Design

- Canvas 1280×720, dark theme. Use the colour tokens in `:root` of `style.css` only:
  cyan for emphasis, amber/mint/coral for categories and states, muted for secondary text.
- Sizes are relative (`em`) to the 30px base. Follow the scale of comparable components.
- **Bottom zone:** the key message sits at `--key-bottom`, the footer at `--chrome-bottom`.
  Content must end at least 16px above the key message. If a slide is too full, reduce its
  content or its internal gaps; do not move the key message.
- Class names that are also UnoCSS utilities pick up unwanted styles (`ring` and `ml` did).
  Either avoid such names or add them to the blocklist in `uno.config.ts`.
- Do not add decoration that carries no information.
- The deck must work without an internet connection: no web fonts, no images, scripts
  or styles loaded from external hosts.

## 9. Working method

1. Outline first, confirmed by the user.
2. Build the slides, then the animations.
3. Run `npm run check:strict`.
4. Look at the result. Open the changed slides in the browser (or take screenshots with
   Playwright against the dev server, `#/<slide>?clicks=<n>`) with no clicks and with all
   clicks. Check for overlaps, tight spacing, text that wraps badly and elements too close
   to the footer.
5. On animation slides, click forwards and backwards and confirm the animation stops where
   the bullets say.
6. Expect review feedback per slide number. Fix the named slide, then check whether the
   same problem exists on other slides and fix it there too.
7. Put new information where it belongs (see "Where information lives").

Review checklist for every slide:

- [ ] Can I say in one sentence what this slide teaches?
- [ ] Is that sentence on the slide as the key message?
- [ ] Is the slide empty on entry apart from eyebrow and title?
- [ ] Does it use the running example and the terms of the audience?
- [ ] Does every explanation have a visual, and is the visual large enough?
- [ ] Are diagrams true to the real setup and numbers correct or marked as illustrative?
- [ ] Do the notes state the learning goal and what the speaker does?
