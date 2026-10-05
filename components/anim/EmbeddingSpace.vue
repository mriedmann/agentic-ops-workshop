<script setup lang="ts">
import { useTemplateRef } from "vue";
import { drawIn, fadeIn, fadeOut, slideIn, svg, useSceneTimeline } from "../../animations/scene";

// Words with similar meaning sit close together; equal relations share direction.
// Coordinates are in units of a 2D projection (illustrative), mapped to the 1280×720 canvas.
const UNIT = 92;
const px = (x: number) => 640 + x * UNIT;
const py = (y: number) => 300 - y * UNIT;

// Labels sit above their dot; where an arrow or line would cross the label, it moves aside.
const LABEL_SIDE: Record<string, "left" | "below"> = { Setzling: "left", Welpe: "left", Kalb: "left", Strauch: "below" };
function labelAt(word: string, x: number, y: number) {
  const side = LABEL_SIDE[word];
  if (side === "left") return { lx: x - 16, ly: y + 9, anchor: "end" };
  if (side === "below") return { lx: x, ly: y + 38, anchor: "middle" };
  return { lx: x, ly: y - 20, anchor: "middle" };
}

const CLUSTERS = [
  { part: "pflanzen", name: "Pflanzen", color: "var(--mint)", ring: { x: -4.09, y: -1.31, r: 1.85 }, words: { Setzling: [-4.5, -1.9], Baum: [-3.2, -1.2], Blume: [-4.9, -0.7], Strauch: [-3.4, -2.3] } },
  { part: "tiere", name: "Tiere", color: "var(--amber)", ring: { x: -0.69, y: 0.88, r: 1.9 }, words: { Welpe: [-1.5, 0.9], Hund: [-0.2, 1.6], Kalb: [-1.0, -0.2], Kuh: [0.3, 0.5] } },
  { part: "fahrzeuge", name: "Fahrzeuge", color: "var(--coral)", ring: { x: 3.69, y: -0.81, r: 1.93 }, words: { Fahrrad: [2.9, -1.9], Auto: [3.4, -0.8], LKW: [4.7, -0.1], Bus: [4.6, -1.4] } },
].map((cluster) => ({
  ...cluster,
  items: Object.entries(cluster.words).map(([word, [x, y]]) => ({ word, x: px(x), y: py(y), ...labelAt(word, px(x), py(y)) })),
  ring: { cx: px(cluster.ring.x), cy: py(cluster.ring.y), r: cluster.ring.r * UNIT },
}));
const at = Object.fromEntries(CLUSTERS.flatMap((c) => c.items.map((item) => [item.word, item])));

// A line between two words, shortened at both ends, with an arrow head at its end.
function arrow(from: string, to: string, gap = 14, head = 16) {
  const a = at[from];
  const b = at[to];
  const length = Math.hypot(b.x - a.x, b.y - a.y);
  const [ux, uy] = [(b.x - a.x) / length, (b.y - a.y) / length];
  const [x1, y1, x2, y2] = [a.x + ux * gap, a.y + uy * gap, b.x - ux * gap, b.y - uy * gap];
  const base = [x2 - ux * head, y2 - uy * head];
  const tip = `${x2},${y2} ${base[0] - uy * head * 0.55},${base[1] + ux * head * 0.55} ${base[0] + uy * head * 0.55},${base[1] - ux * head * 0.55}`;
  return { x1, y1, x2: base[0] + ux * 2, y2: base[1] + uy * 2, tip };
}
const ANALOGIES = [arrow("Setzling", "Baum"), arrow("Kalb", "Kuh"), arrow("Welpe", "Hund")];
const AXES = { x0: px(-6.2), y0: py(-3.68), x1: px(5.9), y1: py(3.0) };
const near = { a: at.Baum, b: at.Strauch };
const far = { a: at.Baum, b: at.Auto };

const root = useTemplateRef<SVGSVGElement>("root");

useSceneTimeline(root, (tl, q) => {
  tl.add(q("axes"), fadeIn({ duration: 1 }));
  tl.add(svg.createDrawable(q("axis-line")), drawIn({ duration: 600 }), "<<");
  tl.add(q("axis-head axis-label"), fadeIn(), "<<+=300");
  tl.add(q("item-pflanzen"), slideIn(0, 14, { delay: (_: unknown, i: number) => i * 120 }));
  tl.add(q("ring-pflanzen"), fadeIn({ duration: 1 }));
  tl.add(svg.createDrawable(q("ring-pflanzen-circle")), drawIn({ duration: 500 }), "<<");
  tl.add(q("ring-pflanzen-label"), fadeIn(), "<<");
  tl.label("s1");

  for (const part of ["tiere", "fahrzeuge"]) {
    tl.add(q(`item-${part}`), slideIn(0, 14, { delay: (_: unknown, i: number) => i * 100 }));
    tl.add(q(`ring-${part}`), fadeIn({ duration: 1 }));
    tl.add(svg.createDrawable(q(`ring-${part}-circle`)), drawIn({ duration: 400 }), "<<");
    tl.add(q(`ring-${part}-label`), fadeIn(), "<<");
  }
  tl.label("s2");

  tl.add(q("near"), fadeIn({ duration: 1 }));
  tl.add(svg.createDrawable(q("near-line")), drawIn({ duration: 500 }), "<<");
  tl.add(q("near-label"), fadeIn(), "<<");
  tl.add(q("far"), fadeIn({ duration: 1 }));
  tl.add(svg.createDrawable(q("far-line")), drawIn({ duration: 500 }), "<<");
  tl.add(q("far-label"), fadeIn(), "<<");
  tl.label("s3");

  tl.add(q("near far"), fadeOut({ duration: 400 }));
  tl.add(q("analogy"), fadeIn({ duration: 1 }));
  ANALOGIES.forEach((_, i) => {
    tl.add(svg.createDrawable(q(`analogy-line-${i}`)), drawIn({ duration: 450 }), i ? "<<+=200" : undefined);
    tl.add(q(`analogy-head-${i}`), fadeIn({ duration: 150 }));
  });
  tl.add(q("relation"), fadeIn());
  tl.label("s4");
});
</script>

<template>
  <svg ref="root" class="scene" viewBox="0 0 1280 720">
    <g data-part="axes" style="opacity: 0">
      <line data-part="axis-line" :x1="AXES.x0" :y1="AXES.y0" :x2="AXES.x1 - 4" :y2="AXES.y0" style="stroke: var(--line); stroke-width: 3" />
      <line data-part="axis-line" :x1="AXES.x0" :y1="AXES.y0" :x2="AXES.x0" :y2="AXES.y1 + 4" style="stroke: var(--line); stroke-width: 3" />
      <polygon data-part="axis-head" :points="`${AXES.x1},${AXES.y0} ${AXES.x1 - 22},${AXES.y0 - 11} ${AXES.x1 - 22},${AXES.y0 + 11}`" style="fill: var(--line); opacity: 0" />
      <polygon data-part="axis-head" :points="`${AXES.x0},${AXES.y1} ${AXES.x0 - 11},${AXES.y1 + 22} ${AXES.x0 + 11},${AXES.y1 + 22}`" style="fill: var(--line); opacity: 0" />
      <text data-part="axis-label" class="muted" :x="AXES.x1" :y="AXES.y0 + 36" font-size="24" text-anchor="end" style="opacity: 0">Dimension 1</text>
      <g style="transform-box: view-box" :transform="`translate(${AXES.x0 - 16} ${AXES.y0 - 150}) rotate(-90)`">
        <text data-part="axis-label" class="muted" x="0" y="0" font-size="24" text-anchor="middle" style="opacity: 0">Dimension 2</text>
      </g>
    </g>

    <template v-for="cluster in CLUSTERS" :key="cluster.part">
      <g :data-part="`ring-${cluster.part}`" style="opacity: 0">
        <circle :data-part="`ring-${cluster.part}-circle`" :cx="cluster.ring.cx" :cy="cluster.ring.cy" :r="cluster.ring.r" :style="{ fill: 'none', stroke: cluster.color, strokeWidth: 2, strokeOpacity: 0.5 }" />
        <text :data-part="`ring-${cluster.part}-label`" :x="cluster.ring.cx" :y="cluster.ring.cy + cluster.ring.r + 27" font-size="24" text-anchor="middle" :style="{ fill: cluster.color, opacity: 0 }">{{ cluster.name }}</text>
      </g>
      <g v-for="item in cluster.items" :key="item.word" :data-part="`item-${cluster.part}`" style="opacity: 0">
        <circle :cx="item.x" :cy="item.y" r="9" :style="{ fill: cluster.color }" />
        <text :x="item.lx" :y="item.ly" font-size="27" :text-anchor="item.anchor">{{ item.word }}</text>
      </g>
    </template>

    <g data-part="near" style="opacity: 0">
      <line data-part="near-line" :x1="near.a.x" :y1="near.a.y" :x2="near.b.x" :y2="near.b.y" style="stroke: var(--mint); stroke-width: 4" />
      <text data-part="near-label" :x="(near.a.x + near.b.x) / 2 + 22" :y="(near.a.y + near.b.y) / 2 + 8" font-size="25" style="fill: var(--mint); opacity: 0">nah = ähnlich</text>
    </g>
    <g data-part="far" style="opacity: 0">
      <line data-part="far-line" :x1="far.a.x" :y1="far.a.y" :x2="far.b.x" :y2="far.b.y" style="stroke: var(--muted); stroke-width: 3; stroke-opacity: 0.7" />
      <text data-part="far-label" class="muted" :x="far.a.x + (far.b.x - far.a.x) * 0.58" :y="far.a.y + (far.b.y - far.a.y) * 0.58 - 22" font-size="24" text-anchor="middle" style="opacity: 0">weit = unähnlich</text>
    </g>

    <g data-part="analogy" style="opacity: 0">
      <template v-for="(a, i) in ANALOGIES" :key="i">
        <line :data-part="`analogy-line-${i}`" :x1="a.x1" :y1="a.y1" :x2="a.x2" :y2="a.y2" style="stroke: var(--cyan); stroke-width: 5; stroke-linecap: round" />
        <polygon :data-part="`analogy-head-${i}`" :points="a.tip" style="fill: var(--cyan); opacity: 0" />
      </template>
    </g>
    <text data-part="relation" x="640" y="700" font-size="28" text-anchor="middle" style="fill: var(--cyan); opacity: 0">gleiche Beziehung → gleiche Richtung und Länge</text>
  </svg>
</template>
