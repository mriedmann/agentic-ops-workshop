<script setup lang="ts">
import { useTemplateRef } from "vue";
import { EXAMPLE_TOKENS, visibleSpace } from "../../animations/example";
import { alongPath, drawIn, fadeIn, fadeOut, slideIn, svg, useSceneTimeline } from "../../animations/scene";

// The current token (" großer") collects information from the other tokens.
// How strongly " großer" attends to each earlier token (illustrative).
const WEIGHTS = [0.05, 0.04, 0.31, 0.44, 0.09, 0.52, 0.06, 0.05];
const COLORS = ["var(--muted)", "var(--muted)", "var(--cyan)", "var(--amber)", "var(--amber)", "var(--amber)", "var(--muted)", "var(--muted)", "var(--mint)"];

// Token pills in one row; monospace, so widths follow the character count.
const FONT = 28;
const CHAR = FONT * 0.6;
const PAD = 28;
const GAP = 12;
const ROW_Y = 430;
const PILL_H = 58;
const widths = EXAMPLE_TOKENS.map(([text]) => text.length * CHAR + PAD);
const total = widths.reduce((a, b) => a + b, 0) + GAP * (widths.length - 1);
const tokens = EXAMPLE_TOKENS.map(([text], index) => {
  const x = (1280 - total) / 2 + widths.slice(0, index).reduce((a, b) => a + b, 0) + GAP * index;
  return { text: visibleSpace(text), x, width: widths[index], cx: x + widths[index] / 2, color: COLORS[index] };
});
const focus = tokens[8];

// One arc from the focus token to each earlier token; farther tokens get higher arcs.
const top = ROW_Y - PILL_H / 2 - 4;
const arcs = WEIGHTS.map((weight, index) => {
  const height = 70 + (8 - index) * 25;
  const [sx, ex] = [focus.cx, tokens[index].cx];
  const strong = weight > 0.2;
  // Label near the target end of the arc (cubic Bézier at t = 0.88).
  const t = 0.88;
  const bez = (p0: number, p1: number, p2: number, p3: number) =>
    (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3;
  return {
    d: `M ${sx} ${top} C ${sx} ${top - height}, ${ex} ${top - height}, ${ex} ${top}`,
    color: strong ? tokens[index].color : "var(--muted)",
    width: 1.5 + 10 * weight,
    opacity: 0.3 + 0.6 * weight,
    label: strong ? weight.toFixed(2) : null,
    lx: bez(sx, sx, ex, ex),
    ly: bez(top, top - height, top - height, top) - 18,
  };
});

const root = useTemplateRef<SVGSVGElement>("root");

useSceneTimeline(root, (tl, q) => {
  tl.add(q("subtitle"), fadeIn());
  tl.add(q("token"), slideIn(0, 10, { delay: (_: unknown, i: number) => i * 80 }), "<<");
  tl.label("s1");

  tl.add(q("focus"), fadeIn({ duration: 300 }));
  // The ripple first appears, then expands and fades; it is hidden before and after.
  tl.add(q("ripple"), { opacity: [0, 1], duration: 30 }, "<<");
  tl.add(q("ripple"), { opacity: [1, 0], scale: [1, 1.7], duration: 550, ease: "outQuad" });
  tl.add(q("question"), slideIn(0, 12));
  tl.label("s2");

  tl.add(svg.createDrawable(q("arc")), drawIn({ duration: 600, delay: (_: unknown, i: number) => i * 90 }));
  // A dot runs along every arc from " großer" to the token it looks at, all at once.
  const dotsStart = tl.duration;
  q("dot").forEach((dot, i) => {
    tl.add(dot, { opacity: [0, 1], duration: 100 }, dotsStart);
    tl.add(dot, alongPath(q("arc")[i], { duration: 1200, ease: "linear" }), dotsStart);
    tl.add(dot, { opacity: [1, 0], duration: 100 }, dotsStart + 1150);
  });
  tl.add(q("weight"), fadeIn({ duration: 600 }), dotsStart);
  tl.label("s3");

  tl.add(q("question"), fadeOut());
  tl.add(q("result"), slideIn(0, 16, { duration: 600 }), "<<");
  tl.add(q("note"), fadeIn());
  tl.label("s4");
});
</script>

<template>
  <svg ref="root" class="scene" viewBox="0 0 1280 720">
    <text data-part="subtitle" class="muted" x="640" y="80" font-size="32" text-anchor="middle" style="opacity: 0">Welche Tokens helfen, „großer“ einzuordnen?</text>

    <path
      v-for="(arc, i) in arcs"
      :key="`arc-${i}`"
      data-part="arc"
      :d="arc.d"
      :style="{ fill: 'none', stroke: arc.color, strokeWidth: arc.width, strokeOpacity: arc.opacity }"
    />
    <template v-for="(arc, i) in arcs" :key="`label-${i}`">
      <text v-if="arc.label" data-part="weight" class="mono" :x="arc.lx" :y="arc.ly" font-size="26" text-anchor="middle" :style="{ fill: arc.color, opacity: 0 }">{{ arc.label }}</text>
    </template>

    <g v-for="(token, i) in tokens" :key="i" data-part="token" style="opacity: 0">
      <rect :x="token.x" :y="ROW_Y - PILL_H / 2" :width="token.width" :height="PILL_H" rx="13" :style="{ fill: token.color, fillOpacity: 0.12, stroke: token.color, strokeWidth: 2 }" />
      <text class="mono" :x="token.cx" :y="ROW_Y + 10" :font-size="FONT" text-anchor="middle">{{ token.text }}</text>
    </g>

    <rect data-part="focus" :x="focus.x" :y="ROW_Y - PILL_H / 2" :width="focus.width" :height="PILL_H" rx="13" style="fill: var(--mint); fill-opacity: 0.3; stroke: var(--mint); stroke-width: 4; opacity: 0" />
    <circle data-part="ripple" :cx="focus.cx" :cy="ROW_Y" r="50" style="fill: none; stroke: var(--mint); stroke-width: 3; opacity: 0; transform-origin: center" />
    <circle v-for="i in arcs.length" :key="`dot-${i}`" data-part="dot" cx="0" cy="0" r="6" style="fill: var(--ink); opacity: 0" />

    <text data-part="question" x="640" y="570" font-size="32" text-anchor="middle" style="opacity: 0">„… wurde ein großer  ___“</text>

    <g data-part="result" style="opacity: 0">
      <rect x="150" y="535" width="980" height="64" rx="14" style="fill: var(--mint); fill-opacity: 0.12; stroke: var(--mint); stroke-width: 2" />
      <text x="640" y="577" font-size="30" text-anchor="middle">„großer“ + Kontext → es geht um eine Pflanze, die gewachsen ist</text>
    </g>

    <text data-part="note" class="muted" x="640" y="680" font-size="25" text-anchor="middle" style="opacity: 0">Die Gewichte hängen vom Satz ab und werden in vielen Köpfen parallel berechnet.</text>
  </svg>
</template>
