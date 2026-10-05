<script setup lang="ts">
import { useTemplateRef } from "vue";
import { EXAMPLE_ANSWER, EXAMPLE_CANDIDATES, EXAMPLE_PROMPT, softmax, visibleSpace } from "../../animations/example";
import { fadeIn, fadeOut, slideIn, useSceneTimeline } from "../../animations/scene";

// Logits become probabilities; temperature reshapes them; one token is picked.
const COLORS = ["var(--mint)", "var(--amber)", "var(--cyan)", "var(--coral)", "var(--muted)"];
const TRACK = { x: 500, width: 460, height: 42 };
const rows = EXAMPLE_CANDIDATES.map(([text, , logit], index) => ({
  word: visibleSpace(text),
  logit: `${logit >= 0 ? "+" : ""}${logit.toFixed(1)}`,
  color: COLORS[index],
  y: 210 + index * 82,
}));
const logits = EXAMPLE_CANDIDATES.map(([, , logit]) => logit);

// The temperatures in the order the scene shows them, with the hint shown next to each.
const TEMPERATURES = [
  { part: "t1", value: 1.0 },
  { part: "cold", value: 0.4, hint: "schärfer", color: "var(--cyan)" },
  { part: "hot", value: 1.6, hint: "flacher", color: "var(--coral)" },
  { part: "t1b", value: 1.0 },
].map((t) => ({ ...t, probabilities: softmax(logits, t.value) }));

// Bars are drawn at full track width and scaled to their probability (never fully empty).
const scaleFor = (p: number) => Math.max(0.02, p);

const root = useTemplateRef<SVGSVGElement>("root");

useSceneTimeline(root, (tl, q) => {
  // Bars and percentages move from temperature `from` (none: empty bars) to temperature `to`.
  const distribute = (from: number | null, to: number) => {
    const before = from == null ? rows.map(() => 0) : TEMPERATURES[from].probabilities;
    const after = TEMPERATURES[to].probabilities;
    if (from != null) tl.add(q(`pct-${TEMPERATURES[from].part}`), fadeOut({ duration: 250 }));
    q("bar").forEach((bar, i) => {
      tl.add(bar, { scaleX: [scaleFor(before[i]), scaleFor(after[i])], duration: 900, ease: "inOutSine" }, i ? "<<" : undefined);
    });
    tl.add(q(`pct-${TEMPERATURES[to].part}`), fadeIn(), "<<+=300");
  };
  // Swaps the temperature value and its hint, then redistributes.
  const setTemperature = (from: number, to: number) => {
    tl.add(q(`temp-${TEMPERATURES[from].part} hint-${TEMPERATURES[from].part}`), fadeOut({ duration: 250 }));
    tl.add(q(`temp-${TEMPERATURES[to].part} hint-${TEMPERATURES[to].part}`), fadeIn());
    distribute(from, to);
  };

  tl.add(q("prompt blank"), fadeIn({ duration: 600 }));
  tl.add(q("row"), slideIn(-16, 0, { delay: (_: unknown, i: number) => i * 90 }));
  tl.add(q("caption-logits"), fadeIn());
  tl.label("s1");

  tl.add(q("temperature temp-t1"), fadeIn());
  tl.add(q("caption-logits"), fadeOut(), "<<");
  tl.add(q("caption-softmax"), fadeIn(), "<<");
  distribute(null, 0);
  tl.label("s2");

  setTemperature(0, 1);
  tl.label("s3");

  setTemperature(1, 2);
  tl.label("s4");

  setTemperature(2, 3);
  tl.add(q("picked"), fadeIn());
  tl.add(q("blank"), fadeOut());
  tl.add(q("answer"), slideIn(0, 10));
  tl.add(q("note"), fadeIn());
  tl.label("s5");
});
</script>

<template>
  <svg ref="root" class="scene" viewBox="0 0 1280 720">
    <text data-part="prompt" x="850" y="76" text-anchor="end" font-size="34" style="opacity: 0">{{ EXAMPLE_PROMPT }}</text>
    <text data-part="blank" x="866" y="76" font-size="34" style="fill: var(--mint); opacity: 0">____</text>
    <text data-part="answer" x="866" y="76" font-size="34" style="fill: var(--mint); opacity: 0">{{ EXAMPLE_ANSWER.trim() }}</text>

    <text data-part="caption-logits" class="muted" x="230" y="146" font-size="24" style="opacity: 0">Logits – eine Punktzahl je Token im Vokabular</text>
    <text data-part="caption-softmax" class="muted" x="230" y="146" font-size="24" style="opacity: 0">Softmax macht daraus Wahrscheinlichkeiten</text>

    <g v-for="row in rows" :key="row.word" data-part="row" style="opacity: 0">
      <text class="mono" x="230" :y="row.y + 10" font-size="30">{{ row.word }}</text>
      <text class="mono" x="465" :y="row.y + 10" font-size="28" text-anchor="end" :style="{ fill: row.color }">{{ row.logit }}</text>
      <rect :x="TRACK.x" :y="row.y - TRACK.height / 2" :width="TRACK.width" :height="TRACK.height" rx="10" style="fill: var(--line); fill-opacity: 0.25; stroke: var(--line); stroke-width: 2" />
      <rect data-part="bar" :x="TRACK.x" :y="row.y - TRACK.height / 2" :width="TRACK.width" :height="TRACK.height" rx="10" :style="{ fill: row.color, opacity: 0.9, transform: 'scaleX(0.02)' }" />
    </g>

    <g v-for="t in TEMPERATURES" :key="t.part" :data-part="`pct-${t.part}`" style="opacity: 0">
      <text v-for="(p, i) in t.probabilities" :key="i" class="mono" x="1070" :y="rows[i].y + 10" font-size="28" text-anchor="end" :style="{ fill: rows[i].color }">{{ Math.round(p * 100) }}%</text>
    </g>

    <text data-part="temperature" class="muted" x="1180" y="196" font-size="24" text-anchor="middle" style="opacity: 0">Temperatur</text>
    <template v-for="t in TEMPERATURES" :key="t.part">
      <text :data-part="`temp-${t.part}`" x="1180" y="240" font-size="38" text-anchor="middle" :style="{ fill: t.color ?? 'var(--ink)', opacity: 0 }">{{ t.value.toFixed(1) }}</text>
      <text v-if="t.hint" :data-part="`hint-${t.part}`" x="1180" y="284" font-size="24" text-anchor="middle" :style="{ fill: t.color, opacity: 0 }">{{ t.hint }}</text>
    </template>

    <g data-part="picked" style="opacity: 0">
      <rect x="205" :y="rows[0].y - 35" width="890" height="70" rx="14" style="fill: none; stroke: var(--mint); stroke-width: 3" />
      <text x="190" :y="rows[0].y + 8" font-size="24" text-anchor="end" style="fill: var(--mint)">gewählt</text>
    </g>

    <text data-part="note" class="muted" x="640" y="660" font-size="26" text-anchor="middle" style="opacity: 0">Das Modell liefert die Verteilung. Die Auswahl daraus ist eine eigene Entscheidung.</text>
  </svg>
</template>
