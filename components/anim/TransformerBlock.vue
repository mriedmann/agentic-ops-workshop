<script setup lang="ts">
import { useTemplateRef } from "vue";
import { EXAMPLE_TOKENS, visibleSpace } from "../../animations/example";
import { drawIn, fadeIn, fadeOut, growFromLeft, slideIn, svg, useSceneTimeline } from "../../animations/scene";

// One transformer layer: attention, feed forward, each with residual + norm.
const ROW = 350;

// Token pills along the top, sized by their text; the last one (the current token) in mint.
const PILL = { height: 46, gap: 10, pad: 24, char: 13.5 };
const widths = EXAMPLE_TOKENS.map(([text]) => PILL.pad + visibleSpace(text).length * PILL.char);
const total = widths.reduce((a, b) => a + b, 0) + PILL.gap * (widths.length - 1);
let left = 640 - total / 2;
const tokens = EXAMPLE_TOKENS.map(([text], index) => {
  const token = { text: visibleSpace(text), x: left, width: widths[index], current: index === EXAMPLE_TOKENS.length - 1 };
  left += widths[index] + PILL.gap;
  return token;
});
const TOKEN_Y = 74;

// A vector as a row of bars: height and opacity follow the size of each value.
const vector = (values: number[], centerX: number) =>
  values.map((value, index) => {
    const height = 16 + 42 * Math.abs(value);
    return { x: centerX - 45 + index * 19, y: ROW - height / 2, height, opacity: 0.4 + 0.5 * Math.abs(value) };
  });
const START = vector([0.3, 0.9, 0.5, 0.7, 0.4], 110);
const OUT = vector([0.5, 0.6, 0.9, 0.3, 0.8], 1170);

const ATTENTION = { x: 215, width: 250, color: "var(--cyan)" };
const FEED_FORWARD = { x: 680, width: 240, color: "var(--violet)" };
const BOX = { y: ROW - 55, height: 110 };
const ADD = [575, 1010];
const R = 34;

// Horizontal arrows between the stations: [from x, to x, colour].
const ARROWS = {
  in: [160, 210, "var(--mint)"],
  a1: [470, ADD[0] - R - 5, "var(--cyan)"],
  a2: [ADD[0] + R + 5, FEED_FORWARD.x - 5, "var(--amber)"],
  a3: [FEED_FORWARD.x + FEED_FORWARD.width + 5, ADD[1] - R - 5, "var(--violet)"],
  out: [ADD[1] + R + 5, 1118, "var(--mint)"],
} as const;

const RESIDUAL_1 = `M 110 ${ROW - 40} C 110 ${ROW - 128} ${ADD[0]} ${ROW - 128} ${ADD[0]} ${ROW - R - 4}`;
const RESIDUAL_2 = `M ${ADD[0]} ${ROW - R - 4} C ${ADD[0]} ${ROW - 110} ${ADD[1]} ${ROW - 110} ${ADD[1]} ${ROW - R - 4}`;
const LOOP = `M 1170 ${ROW + 50} C 1170 ${ROW + 230} 110 ${ROW + 230} 110 ${ROW + 100}`;

const root = useTemplateRef<SVGSVGElement>("root");

useSceneTimeline(root, (tl, q) => {
  tl.add(q("token"), slideIn(0, -8, { delay: (_: unknown, i: number) => i * 60 }));
  tl.add(q("start"), slideIn(-16, 0));
  tl.label("s1");

  tl.add(q("arrow-in"), growFromLeft(1, { duration: 400 }));
  tl.add(q("attention"), fadeIn(), "<<");
  tl.add(q("feeds"), fadeIn({ duration: 1 }));
  tl.add(svg.createDrawable(q("feed")), drawIn({ duration: 700 }), "<<");
  tl.label("s2");

  tl.add(q("arrow-a1"), growFromLeft(1, { duration: 400 }));
  tl.add(q("add-1"), fadeIn(), "<<");
  tl.add(q("residual-1"), fadeIn({ duration: 1 }));
  tl.add(svg.createDrawable(q("residual-1-path")), drawIn({ duration: 700 }), "<<");
  tl.add(q("residual-label"), fadeIn(), "<<");
  tl.label("s3");

  tl.add(q("arrow-a2"), growFromLeft(1, { duration: 400 }));
  tl.add(q("feed-forward"), fadeIn(), "<<");
  tl.add(q("arrow-a3"), growFromLeft(1, { duration: 400 }));
  tl.add(q("add-2 weights-note"), fadeIn(), "<<");
  tl.add(q("residual-2"), fadeIn({ duration: 1 }), "<<");
  tl.add(svg.createDrawable(q("residual-2-path")), drawIn({ duration: 700 }), "<<");
  tl.label("s4");

  tl.add(q("arrow-out"), growFromLeft(1, { duration: 400 }));
  tl.add(q("out"), fadeIn(), "<<");
  tl.add(q("loop"), fadeIn({ duration: 1 }));
  tl.add(svg.createDrawable(q("loop-path")), drawIn({ duration: 900 }), "<<");
  tl.add(q("loop-label"), fadeIn(), "<<");
  tl.label("s5");

  tl.add(q("weights-note"), fadeOut());
  tl.add(q("final out-amber"), fadeIn({ duration: 700 }), "<<");
  tl.label("s6");
});
</script>

<template>
  <svg ref="root" class="scene" viewBox="0 0 1280 720">
    <defs>
      <marker id="tb-head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" style="fill: context-stroke" />
      </marker>
    </defs>

    <g v-for="token in tokens" :key="token.x" data-part="token" style="opacity: 0">
      <rect
        :x="token.x"
        :y="TOKEN_Y - PILL.height / 2"
        :width="token.width"
        :height="PILL.height"
        rx="10"
        :style="token.current ? { fill: 'var(--mint)', fillOpacity: 0.22, stroke: 'var(--mint)', strokeWidth: 3 } : { fill: 'var(--muted)', fillOpacity: 0.12, stroke: 'var(--muted)', strokeWidth: 2 }"
      />
      <text :x="token.x + token.width / 2" :y="TOKEN_Y + 8" font-size="24" text-anchor="middle">{{ token.text }}</text>
    </g>

    <g data-part="feeds" style="opacity: 0">
      <line
        v-for="token in tokens"
        :key="token.x"
        data-part="feed"
        :x1="token.x + token.width / 2"
        :y1="TOKEN_Y + PILL.height / 2"
        :x2="ATTENTION.x + ATTENTION.width / 2"
        :y2="BOX.y"
        style="stroke: var(--cyan); stroke-width: 1.5; stroke-opacity: 0.35"
      />
    </g>

    <g data-part="start" style="opacity: 0">
      <rect v-for="bar in START" :key="bar.x" :x="bar.x" :y="bar.y" width="14" :height="bar.height" rx="4" :style="{ fill: 'var(--mint)', opacity: bar.opacity }" />
      <text class="muted" x="132" :y="ROW + 78" font-size="21" text-anchor="middle">Vektor von „␣großer“</text>
    </g>

    <g v-for="(arrow, key) in ARROWS" :key="key" :data-part="`arrow-${key}`" style="opacity: 1; transform: scaleX(0)">
      <line :x1="arrow[0]" :y1="ROW" :x2="arrow[1]" :y2="ROW" marker-end="url(#tb-head)" :style="{ stroke: arrow[2], strokeWidth: 3 }" />
    </g>

    <g data-part="attention" style="opacity: 0">
      <rect :x="ATTENTION.x" :y="BOX.y" :width="ATTENTION.width" :height="BOX.height" rx="14" :style="{ fill: 'var(--panel)', stroke: ATTENTION.color, strokeWidth: 2 }" />
      <text :x="ATTENTION.x + ATTENTION.width / 2" :y="ROW - 4" font-size="28" text-anchor="middle">Self-Attention</text>
      <text class="muted" :x="ATTENTION.x + ATTENTION.width / 2" :y="ROW + 26" font-size="21" text-anchor="middle">mischt über alle Tokens</text>
    </g>

    <g data-part="feed-forward" style="opacity: 0">
      <rect :x="FEED_FORWARD.x" :y="BOX.y" :width="FEED_FORWARD.width" :height="BOX.height" rx="14" :style="{ fill: 'var(--panel)', stroke: FEED_FORWARD.color, strokeWidth: 2 }" />
      <text :x="FEED_FORWARD.x + FEED_FORWARD.width / 2" :y="ROW - 4" font-size="28" text-anchor="middle">Feed Forward</text>
      <text class="muted" :x="FEED_FORWARD.x + FEED_FORWARD.width / 2" :y="ROW + 26" font-size="21" text-anchor="middle">jedes Token für sich</text>
    </g>

    <g v-for="(x, index) in ADD" :key="x" :data-part="`add-${index + 1}`" style="opacity: 0">
      <circle :cx="x" :cy="ROW" :r="R" style="fill: var(--panel); stroke: var(--amber); stroke-width: 2" />
      <text :x="x" :y="ROW + 11" font-size="32" text-anchor="middle" style="fill: var(--amber)">+</text>
      <text class="muted" :x="x" :y="ROW + R + 26" font-size="19" text-anchor="middle">Residual</text>
      <text class="muted" :x="x" :y="ROW + R + 48" font-size="19" text-anchor="middle">+ Norm</text>
    </g>

    <g data-part="residual-1" style="opacity: 0">
      <path data-part="residual-1-path" :d="RESIDUAL_1" style="fill: none; stroke: var(--amber); stroke-width: 2.5" />
    </g>
    <text data-part="residual-label" x="342" :y="ROW - 128" font-size="22" text-anchor="middle" style="fill: var(--amber); opacity: 0">der alte Vektor bleibt erhalten</text>
    <g data-part="residual-2" style="opacity: 0">
      <path data-part="residual-2-path" :d="RESIDUAL_2" style="fill: none; stroke: var(--amber); stroke-width: 2.5" />
    </g>
    <text data-part="weights-note" class="muted" :x="FEED_FORWARD.x + FEED_FORWARD.width / 2" :y="ROW + 112" font-size="21" text-anchor="middle" style="opacity: 0">hier sitzt der größte Teil der Gewichte</text>

    <g data-part="out" style="opacity: 0">
      <rect v-for="bar in OUT" :key="bar.x" :x="bar.x" :y="bar.y" width="14" :height="bar.height" rx="4" :style="{ fill: 'var(--mint)', opacity: bar.opacity }" />
    </g>
    <g data-part="out-amber" style="opacity: 0">
      <rect v-for="bar in OUT" :key="bar.x" :x="bar.x" :y="bar.y" width="14" :height="bar.height" rx="4" style="fill: var(--panel)" />
      <rect v-for="bar in OUT" :key="bar.x" :x="bar.x" :y="bar.y" width="14" :height="bar.height" rx="4" :style="{ fill: 'var(--amber)', opacity: bar.opacity }" />
    </g>

    <g data-part="loop" style="opacity: 0">
      <path data-part="loop-path" :d="LOOP" style="fill: none; stroke: var(--cyan); stroke-width: 3" />
    </g>
    <text data-part="loop-label" x="640" :y="ROW + 230" font-size="26" text-anchor="middle" style="fill: var(--cyan); opacity: 0">× N Layer – in großen Modellen einige Dutzend</text>

    <text data-part="final" x="640" y="680" font-size="27" text-anchor="middle" style="opacity: 0">Nach dem letzten Layer wird der Vektor des letzten Tokens zu Logits.</text>
  </svg>
</template>
