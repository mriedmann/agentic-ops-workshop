# AGENTS.md

Guidance for AI agents that create or modify workshop presentations in this repository.
It distils the planning outline and two rounds of review feedback on the "LLMs & Agentic
Operations" deck into rules that apply to any workshop built the same way.

The first half is about teaching (what a good workshop deck looks like), the second half
about this repository (how to build it with Slidev and Manim). When a rule and a user
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
  `animations.py`).

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
| `components/StepVideo.vue` | Click-stepped video |
| `components/*.vue` (others) | One-off diagrams used by a single slide |
| `animations.py` | Manim scenes, one class per animation |
| `public/media/` | Rendered videos and their `*.steps.json` |
| `scripts/check-slides.mjs` | Convention checks, run in CI |
| `scripts/render-animations.sh` | Renders all scenes |

Commands:

```bash
npm install                     # once; Node 22.12 or newer
uv sync                         # once, only needed to render animations
npm start                       # dev server on http://localhost:3030
npm run check                   # conventions, prints warnings
npm run check:strict            # same, fails on any warning; runs in CI
npm run build                   # static site
npm run export                  # PDF, one page per click
./scripts/render-animations.sh  # after changing animations.py
```

`npm run check` expands every slide with `setup/expand.mjs` and enforces the conventions
below. It warns when:

- a slide uses the syntax wrongly (unknown block, key message not last, …),
- a referenced video or its `*.steps.json` is missing,
- the bullets and `[video]` steps of a slide do not match the stops of its video,
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
  - the running example: the `EXAMPLE_*` constants in `animations.py`,
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
| `class` | Slide type: `hero` (cover, exit ticket), `break-slide` (break, demo placeholder), `quiz-slide`, `closing`; on video slides `reverse` puts the video left |
| `step` / `exercise` | Shows the step rail with these stations highlighted |
| `video`, `videoLabel` | Makes the slide a video slide (see Animations); the label is the fallback text when the file is missing |
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
| `[video]` | A click that only advances the video | one |
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

- One `SteppedScene` subclass per animation in `animations.py`, with a `slug`. Call
  `self.step()` at the end of each main step; the timestamps are written to
  `public/media/<slug>.steps.json`.
- In the slide: `video: <slug>` and `videoLabel: …` in the frontmatter. Every bullet and
  every `[video]` line is one video step, in order: the first plays the video to stop 1,
  the second to stop 2, and so on. Put `[video]` before or after the bullets for steps
  that have no bullet. The key message does not move the video.

  ```md
  ---
  eyebrow: SCHRITT 1 · TOKEN
  video: token-pipeline
  videoLabel: Manim · Token-Pipeline
  ---

  ## Text wird in Tokens
  ## *zerlegt und nummeriert*

  [video]

  - Tokens sind Textstücke, keine Wörter
  - Jedes Token hat eine feste ID im Vokabular
  - „Setzling“ allein wird zu drei Tokens

  > Das Modell sieht keine Buchstaben, sondern nur eine Folge von Token-IDs.

  Tokenisierung ist kein Stemming. {.fineprint}
  ```

- The number of stops must equal the number of bullets plus `[video]` lines; the check
  enforces this.
- Use the colour constants and the running-example constants at the top of `animations.py`.
  Scenes render at 1280×720 on the deck background, so they blend into the slide.
- While working on one scene, render it alone in low quality:
  `uv run manim -ql --format=mp4 animations.py <SceneClass>`. Use
  `./scripts/render-animations.sh` for the final files; only that script copies them to
  `public/media/`.
- Videos are committed. Rendering does not run in CI: render locally and commit the files
  from `public/media/`.

## 7. Export and publishing

- **PDF export** runs through Google Chrome (`--executable-path`, overridable with
  `CHROME_PATH`). The Chromium bundled with Playwright cannot play H.264, so the video
  frames would be blank.
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
5. On video slides, click forwards and backwards and confirm the video stops where the
   bullets say.
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
