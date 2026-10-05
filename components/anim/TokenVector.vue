<script setup lang="ts">
import { useTemplateRef } from "vue";
import { drawIn, fadeIn, fadeOut, growFromCenter, slideIn, svg, useSceneTimeline } from "../../animations/scene";

// A token becomes a vector: a list of learned numbers. The numbers are illustrative.
const NUMBERS = { x: 370, font: 30 };
const BAR = { width: 44, gap: 16, base: 30, perUnit: 66 };
const rows = [
  { part: "baum", word: "Baum", color: "var(--mint)", y: 170, values: [0.21, -0.83, 0.04, 1.12, -0.47, 0.6] },
  { part: "auto", word: "Auto", color: "var(--coral)", y: 420, values: [-0.66, 0.35, 0.88, -0.12, 0.74, -0.29] },
].map((row) => ({
  ...row,
  numbers: `[ ${row.values.map((v) => `${v >= 0 ? "+" : "−"}${Math.abs(v).toFixed(2)}`).join("  ")}  … ]`,
  // Bar height and opacity follow the size of the value; bars sit centred on one line below the numbers.
  bars: row.values.map((v, i) => {
    const height = BAR.base + BAR.perUnit * Math.abs(v);
    return { x: NUMBERS.x + 8 + i * (BAR.width + BAR.gap), y: row.y + 110 - height / 2, height, opacity: 0.35 + 0.45 * Math.abs(v) };
  }),
}));

const root = useTemplateRef<SVGSVGElement>("root");

useSceneTimeline(root, (tl, q) => {
  tl.add(q("token-baum"), slideIn(-16));
  tl.add(q("arrow-baum"), fadeIn({ duration: 1 }));
  tl.add(svg.createDrawable(q("arrow-baum-line")), drawIn({ duration: 400 }), "<<");
  tl.add(q("numbers-baum"), fadeIn({ duration: 600 }), "<<+=200");
  tl.add(q("size-note"), fadeIn());
  tl.label("s1");

  tl.add(q("bar-baum"), growFromCenter({ delay: (_: unknown, i: number) => i * 70 }));
  tl.add(q("learned"), fadeIn());
  tl.label("s2");

  tl.add(q("token-auto"), slideIn(-16));
  tl.add(q("arrow-auto"), fadeIn({ duration: 1 }), "<<");
  tl.add(svg.createDrawable(q("arrow-auto-line")), drawIn({ duration: 400 }), "<<");
  tl.add(q("numbers-auto"), fadeIn({ duration: 600 }), "<<+=200");
  tl.add(q("bar-auto"), growFromCenter({ delay: (_: unknown, i: number) => i * 70 }));
  tl.label("s3");

  tl.add(q("learned"), fadeOut());
  tl.add(q("compare"), slideIn(0, 16, { duration: 500 }), "<<");
  tl.label("s4");
});
</script>

<template>
  <svg ref="root" class="scene" viewBox="0 0 1280 720">
    <text data-part="size-note" class="muted" :x="NUMBERS.x + 410" y="96" font-size="25" text-anchor="middle" style="opacity: 0">in echten Modellen einige tausend Zahlen je Token</text>

    <template v-for="row in rows" :key="row.part">
      <g :data-part="`token-${row.part}`" style="opacity: 0">
        <rect x="70" :y="row.y - 34" width="190" height="68" rx="14" :style="{ fill: row.color, fillOpacity: 0.12, stroke: row.color, strokeWidth: 2 }" />
        <text x="165" :y="row.y + 11" font-size="32" text-anchor="middle">{{ row.word }}</text>
      </g>
      <g :data-part="`arrow-${row.part}`" style="opacity: 0">
        <line :data-part="`arrow-${row.part}-line`" x1="272" :y1="row.y" :x2="NUMBERS.x - 18" :y2="row.y" :style="{ stroke: row.color, strokeWidth: 3 }" />
        <polygon :points="`${NUMBERS.x - 22},${row.y - 9} ${NUMBERS.x - 4},${row.y} ${NUMBERS.x - 22},${row.y + 9}`" :style="{ fill: row.color }" />
      </g>
      <text :data-part="`numbers-${row.part}`" class="mono" :x="NUMBERS.x" :y="row.y + 10" :font-size="NUMBERS.font" style="white-space: pre; opacity: 0">{{ row.numbers }}</text>
      <rect
        v-for="(bar, i) in row.bars"
        :key="i"
        :data-part="`bar-${row.part}`"
        :x="bar.x"
        :y="bar.y"
        :width="BAR.width"
        :height="bar.height"
        rx="7"
        :style="{ fill: row.color, fillOpacity: bar.opacity, opacity: 0, transformOrigin: 'center' }"
      />
    </template>

    <text data-part="learned" class="muted" x="640" y="660" font-size="27" text-anchor="middle" style="opacity: 0">Die Zahlen sind im Training gelernt, nicht von Hand gesetzt.</text>
    <g data-part="compare" style="opacity: 0">
      <rect x="250" y="608" width="780" height="70" rx="16" style="fill: var(--amber); fill-opacity: 0.12; stroke: var(--amber); stroke-width: 2" />
      <text x="640" y="653" font-size="32" text-anchor="middle">andere Bedeutung → anderes Zahlenmuster</text>
    </g>
  </svg>
</template>
