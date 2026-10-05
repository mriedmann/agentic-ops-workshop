<script setup lang="ts">
import { useTemplateRef } from "vue";
import { EXAMPLE_PROMPT, EXAMPLE_TOKENIZER, EXAMPLE_TOKENS, visibleSpace } from "../../animations/example";
import { drawIn, fadeIn, fadeOut, growFromCenter, slideIn, svg, useSceneTimeline } from "../../animations/scene";

// The running example is split into tokens and their vocabulary IDs.
// The three pieces of "Setzling" share one colour: one word, three tokens.
const COLORS = ["cyan", "mint", "cyan", "amber", "amber", "amber", "mint", "cyan", "mint"].map((c) => `var(--${c})`);
const PILL = { y: 320, height: 68, gap: 14, pad: 30, char: 18, font: 32 };
const widths = EXAMPLE_TOKENS.map(([text]) => PILL.pad + visibleSpace(text).length * PILL.char);
const total = widths.reduce((a, b) => a + b, 0) + PILL.gap * (widths.length - 1);
const tokens = EXAMPLE_TOKENS.map(([text, id], index) => {
  const x = (1280 - total) / 2 + widths.slice(0, index).reduce((a, b) => a + b, 0) + PILL.gap * index;
  return { text: visibleSpace(text), id, x, width: widths[index], center: x + widths[index] / 2, color: COLORS[index] };
});

// Brace over " Set", "z", "ling".
const BRACE = { left: tokens[3].x, right: tokens[5].x + tokens[5].width, y: 300, depth: 16 };
const mid = (BRACE.left + BRACE.right) / 2;
const bracePath = [
  `M ${BRACE.left} ${BRACE.y}`,
  `Q ${BRACE.left} ${BRACE.y - BRACE.depth} ${BRACE.left + 16} ${BRACE.y - BRACE.depth}`,
  `L ${mid - 16} ${BRACE.y - BRACE.depth}`,
  `Q ${mid} ${BRACE.y - BRACE.depth} ${mid} ${BRACE.y - 2 * BRACE.depth}`,
  `Q ${mid} ${BRACE.y - BRACE.depth} ${mid + 16} ${BRACE.y - BRACE.depth}`,
  `L ${BRACE.right - 16} ${BRACE.y - BRACE.depth}`,
  `Q ${BRACE.right} ${BRACE.y - BRACE.depth} ${BRACE.right} ${BRACE.y}`,
].join(" ");

const root = useTemplateRef<SVGSVGElement>("root");

useSceneTimeline(root, (tl, q) => {
  tl.add(q("sentence"), fadeIn({ duration: 700 }));
  tl.label("s1");

  tl.add(q("arrow"), fadeIn({ duration: 1 }));
  tl.add(svg.createDrawable(q("arrow-line")), drawIn({ duration: 350 }), "<<");
  tl.add(q("token"), growFromCenter({ delay: (_: unknown, i: number) => i * 90 }));
  tl.add(q("legend"), fadeIn());
  tl.label("s2");

  tl.add(svg.createDrawable(q("id-line")), drawIn({ duration: 500 }));
  tl.add(q("id"), slideIn(0, -8), "<<");
  tl.add(q("vocab"), fadeIn());
  tl.label("s3");

  tl.add(q("arrow"), fadeOut({ duration: 250 }));
  tl.add(q("brace"), growFromCenter({ duration: 600 }));
  tl.add(q("brace-label"), slideIn(0, 10), "<<");
  tl.label("s4");
});
</script>

<template>
  <svg ref="root" class="scene" viewBox="0 0 1280 720">
    <text data-part="sentence" x="640" y="170" font-size="52" text-anchor="middle" style="opacity: 0">{{ EXAMPLE_PROMPT }} …</text>

    <g data-part="arrow" style="opacity: 0">
      <line data-part="arrow-line" x1="640" y1="200" x2="640" y2="292" style="stroke: var(--cyan); stroke-width: 3" />
      <polygon points="629,288 651,288 640,308" style="fill: var(--cyan)" />
    </g>

    <g v-for="token in tokens" :key="token.x" data-part="token" style="opacity: 0; transform-origin: center">
      <rect :x="token.x" :y="PILL.y" :width="token.width" :height="PILL.height" rx="14" :style="{ fill: token.color, fillOpacity: 0.12, stroke: token.color, strokeWidth: 2 }" />
      <text :x="token.center" :y="PILL.y + 45" :font-size="PILL.font" text-anchor="middle">{{ token.text }}</text>
    </g>

    <line
      v-for="token in tokens"
      :key="`line-${token.x}`"
      data-part="id-line"
      :x1="token.center"
      :y1="PILL.y + PILL.height"
      :x2="token.center"
      :y2="PILL.y + PILL.height + 42"
      :style="{ stroke: token.color, strokeOpacity: 0.5, strokeWidth: 2 }"
    />
    <text v-for="token in tokens" :key="`id-${token.x}`" data-part="id" class="mono" :x="token.center" :y="PILL.y + PILL.height + 78" font-size="28" text-anchor="middle" :style="{ fill: token.color, opacity: 0 }">{{ token.id }}</text>
    <text data-part="vocab" class="muted" x="640" y="550" font-size="27" text-anchor="middle" style="opacity: 0">IDs aus dem Vokabular des Tokenizers ({{ EXAMPLE_TOKENIZER }})</text>

    <path data-part="brace" :d="bracePath" style="fill: none; stroke: var(--amber); stroke-width: 3; stroke-linecap: round; opacity: 0; transform-origin: center" />
    <text data-part="brace-label" :x="mid" :y="BRACE.y - 2 * BRACE.depth - 14" font-size="30" text-anchor="middle" style="fill: var(--amber); opacity: 0">ein Wort → drei Tokens</text>

    <text data-part="legend" class="muted" x="640" y="672" font-size="26" text-anchor="middle" style="opacity: 0">␣ steht für das führende Leerzeichen</text>
  </svg>
</template>
