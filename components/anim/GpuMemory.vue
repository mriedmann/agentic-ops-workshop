<script setup lang="ts">
import { useTemplateRef } from "vue";
import { fadeIn, fadeOut, growFromLeft, slideIn, useSceneTimeline } from "../../animations/scene";

// What actually fills the VRAM of an inference GPU. Example: 8B model in FP16 on an 80 GB card.
const TOTAL = 80;
const BAR = { x: 120, y: 70, width: 1040, height: 170 };
const gb = (amount: number) => (amount / TOTAL) * BAR.width;
const at = (start: number) => BAR.x + gb(start);

// Legend rows; the 40 GB KV row replaces the 4 GB one on the same line.
const ROWS = [
  { part: "weights", line: 0, color: "var(--cyan)", name: "Gewichte", value: "16 GB", note: "8 Mrd. Parameter × 2 Byte – ab dem Start belegt" },
  { part: "kv", line: 1, color: "var(--amber)", name: "KV-Cache", value: "4 GB", note: "ein Request mit 8.000 Tokens" },
  { part: "kv-big", line: 1, color: "var(--amber)", name: "KV-Cache", value: "40 GB", note: "zehn Requests gleichzeitig, jeder mit eigenem Kontext" },
  { part: "act", line: 2, color: "var(--coral)", name: "Aktivierungen", value: "8 GB", note: "nur während der Rechnung, danach wieder frei" },
  { part: "free", line: 3, color: "var(--muted)", name: "Reserve", value: "16 GB", note: "reicht für mehr Kontext – oder für mehr Requests" },
].map((row) => ({ ...row, y: 340 + row.line * 96 }));

const root = useTemplateRef<SVGSVGElement>("root");

useSceneTimeline(root, (tl, q) => {
  tl.add(q("outline scale"), fadeIn({ duration: 600 }));
  tl.label("s1");

  tl.add(q("seg-weights"), growFromLeft());
  tl.add(q("row-weights"), slideIn());
  tl.label("s2");

  // The KV segment is drawn at its 40 GB size and starts scaled down to 4 GB.
  tl.add(q("seg-kv"), growFromLeft(4 / 40));
  tl.add(q("row-kv"), slideIn(), "<<");
  tl.label("s3");

  tl.add(q("seg-kv"), { scaleX: [4 / 40, 1], duration: 1000, ease: "inOutSine" });
  tl.add(q("row-kv"), fadeOut(), "<<");
  tl.add(q("row-kv-big"), fadeIn(), "<<+=300");
  tl.label("s4");

  tl.add(q("seg-act"), growFromLeft());
  tl.add(q("row-act"), slideIn(), "<<");
  tl.add(q("seg-act"), { opacity: [0.85, 0.3], duration: 300 });
  tl.add(q("seg-act"), { opacity: [0.3, 0.85], duration: 300 });
  tl.label("s5");

  tl.add(q("seg-free row-free"), fadeIn({ duration: 600 }));
  tl.label("s6");
});
</script>

<template>
  <svg ref="root" class="scene" viewBox="0 0 1280 720">
    <text data-part="scale" class="muted" :x="BAR.x + BAR.width" :y="BAR.y - 18" text-anchor="end" font-size="26" style="opacity: 0">eine GPU · 80 GB</text>
    <rect data-part="outline" v-bind="BAR" style="fill: var(--panel); stroke: var(--line); stroke-width: 2; opacity: 0" />

    <rect data-part="seg-weights" :x="at(0)" :y="BAR.y" :width="gb(16)" :height="BAR.height" style="fill: var(--cyan); opacity: 0.85; transform: scaleX(0)" />
    <rect data-part="seg-kv" :x="at(16)" :y="BAR.y" :width="gb(40)" :height="BAR.height" style="fill: var(--amber); opacity: 0.85; transform: scaleX(0)" />
    <rect data-part="seg-act" :x="at(56)" :y="BAR.y" :width="gb(8)" :height="BAR.height" style="fill: var(--coral); opacity: 0.85; transform: scaleX(0)" />
    <rect data-part="seg-free" :x="at(64)" :y="BAR.y" :width="gb(16)" :height="BAR.height" style="fill: var(--muted); fill-opacity: 0.15; opacity: 0" />

    <g v-for="row in ROWS" :key="row.part" :data-part="`row-${row.part}`" style="opacity: 0">
      <rect :x="BAR.x" :y="row.y - 24" width="28" height="28" :style="{ fill: row.color, opacity: 0.85 }" />
      <text :x="BAR.x + 46" :y="row.y" font-size="34">{{ row.name }}</text>
      <text class="mono" x="530" :y="row.y" font-size="34" text-anchor="end" :style="{ fill: row.color }">{{ row.value }}</text>
      <text class="muted" x="565" :y="row.y" font-size="24">{{ row.note }}</text>
    </g>
  </svg>
</template>
