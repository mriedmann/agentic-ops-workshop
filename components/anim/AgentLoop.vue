<script setup lang="ts">
import { useTemplateRef } from "vue";
import { alongPath, drawIn, fadeIn, growFromCenter, svg, useSceneTimeline } from "../../animations/scene";

// Goal-directed tool use with explicit policy and approval gates.
// Nodes sit on an ellipse, wider than high, so the bottom pair has room for its arrow.
const CENTER = { x: 640, y: 318 };
const RADIUS = { x: 335, y: 238 };
const PILL_H = 60;
const NODES = [
  { text: "Ziel", color: "var(--cyan)", width: 200 },
  { text: "Beobachten", color: "var(--mint)", width: 250 },
  { text: "Entscheiden", color: "var(--amber)", width: 262 },
  { text: "Tool ausführen", color: "var(--coral)", width: 290 },
  { text: "Ergebnis prüfen", color: "var(--violet)", width: 290 },
].map((node, index) => {
  const angle = Math.PI / 2 + (index * 2 * Math.PI) / 5;
  return { ...node, x: CENTER.x + RADIUS.x * Math.cos(angle), y: CENTER.y - RADIUS.y * Math.sin(angle) };
});

type Point = { x: number; y: number };
type Box = Point & { width: number };
// Point where the line from the box centre towards `to` leaves the pill, plus a gap.
function edge(box: Box, to: Point, gap = 10): Point {
  const dx = to.x - box.x;
  const dy = to.y - box.y;
  const t = Math.min(box.width / 2 / Math.abs(dx || 1e-9), PILL_H / 2 / Math.abs(dy || 1e-9));
  const length = Math.hypot(dx, dy);
  return { x: box.x + dx * t + (dx / length) * gap, y: box.y + dy * t + (dy / length) * gap };
}
// Straight arrow from box to box: the line (ends short of the tip) and its head.
function arrow(from: Box, to: Box) {
  const start = edge(from, to);
  const tip = edge(to, from);
  const angle = Math.atan2(tip.y - start.y, tip.x - start.x);
  const back = (d: number, side: number) => ({
    x: tip.x - d * Math.cos(angle) - side * Math.sin(angle),
    y: tip.y - d * Math.sin(angle) + side * Math.cos(angle),
  });
  const base = back(14, 0);
  const [left, right] = [back(18, 9), back(18, -9)];
  return {
    line: `M ${start.x} ${start.y} L ${base.x} ${base.y}`,
    head: `${tip.x},${tip.y} ${left.x},${left.y} ${right.x},${right.y}`,
  };
}

const arrows = NODES.map((node, index) => {
  const next = NODES[(index + 1) % NODES.length];
  return { ...arrow(node, next), color: next.color };
});

const GATE = { x: 1060, y: 608, width: 310, text: "WRITE → Freigabe" };
const gateArrow = arrow(NODES[3], GATE);

const root = useTemplateRef<SVGSVGElement>("root");

useSceneTimeline(root, (tl, q) => {
  tl.add(q("node"), growFromCenter({ delay: (_: unknown, i: number) => i * 90 }));
  tl.add(svg.createDrawable(q("arrow-line")), drawIn({ duration: 450, delay: (_: unknown, i: number) => i * 90 }));
  tl.add(q("arrow-head"), fadeIn({ duration: 200, delay: (_: unknown, i: number) => i * 90 }), "<<+=300");
  tl.label("s1");

  tl.add(q("policy"), fadeIn({ duration: 550 }));
  tl.add(q("policy"), { scale: [0.94, 1], duration: 550 }, "<<");
  tl.label("s2");

  // One pulse runs once around the loop; each node it reaches fills up.
  tl.add(q("pulse"), { opacity: [0, 1], duration: 80 });
  q("arrow-line").forEach((line, i) => {
    tl.add(q("pulse"), alongPath(line, { duration: 380, ease: "linear" }));
    tl.add(q(`fill-${(i + 1) % NODES.length}`), fadeIn({ duration: 380 }), "<<");
  });
  tl.add(q("pulse"), { opacity: [1, 0], duration: 150 });
  tl.label("s3");

  tl.add(svg.createDrawable(q("gate-line")), drawIn({ duration: 450 }));
  tl.add(q("gate-head gate"), fadeIn({ duration: 400 }), "<<+=250");
  tl.add(q("note"), fadeIn());
  tl.label("s4");
});
</script>

<template>
  <svg ref="root" class="scene" viewBox="0 0 1280 720">
    <path v-for="(a, i) in arrows" :key="`line-${i}`" data-part="arrow-line" :d="a.line" :style="{ fill: 'none', stroke: a.color, strokeWidth: 3 }" />
    <polygon v-for="(a, i) in arrows" :key="`head-${i}`" data-part="arrow-head" :points="a.head" :style="{ fill: a.color, opacity: 0 }" />

    <g v-for="(node, i) in NODES" :key="node.text" data-part="node" style="opacity: 0; transform-origin: center">
      <rect :x="node.x - node.width / 2" :y="node.y - PILL_H / 2" :width="node.width" :height="PILL_H" rx="14" :style="{ fill: node.color, fillOpacity: 0.12, stroke: node.color, strokeWidth: 2 }" />
      <rect :data-part="`fill-${i}`" :x="node.x - node.width / 2" :y="node.y - PILL_H / 2" :width="node.width" :height="PILL_H" rx="14" :style="{ fill: node.color, fillOpacity: 0.3, opacity: 0 }" />
      <text :x="node.x" :y="node.y + 10" font-size="30" text-anchor="middle">{{ node.text }}</text>
    </g>

    <g data-part="policy" style="opacity: 0; transform-origin: center">
      <rect :x="CENTER.x - 160" :y="CENTER.y - 20" width="320" height="110" rx="16" style="fill: var(--panel); fill-opacity: 0.94; stroke: var(--line); stroke-width: 2" />
      <text :x="CENTER.x" :y="CENTER.y + 20" font-size="22" font-weight="700" text-anchor="middle" style="fill: var(--cyan); letter-spacing: 0.08em">POLICY</text>
      <text :x="CENTER.x" :y="CENTER.y + 60" font-size="26" text-anchor="middle">Scope · Budget · Stop</text>
    </g>

    <circle data-part="pulse" cx="0" cy="0" r="9" style="fill: var(--ink); opacity: 0" />

    <path data-part="gate-line" :d="gateArrow.line" style="fill: none; stroke: var(--coral); stroke-width: 3" />
    <polygon data-part="gate-head" :points="gateArrow.head" style="fill: var(--coral); opacity: 0" />
    <g data-part="gate" style="opacity: 0">
      <rect :x="GATE.x - GATE.width / 2" :y="GATE.y - PILL_H / 2" :width="GATE.width" :height="PILL_H" rx="14" style="fill: var(--coral); fill-opacity: 0.12; stroke: var(--coral); stroke-width: 2" />
      <text :x="GATE.x" :y="GATE.y + 10" font-size="30" text-anchor="middle">{{ GATE.text }}</text>
    </g>

    <text data-part="note" class="muted" x="640" y="678" font-size="25" text-anchor="middle" style="opacity: 0">Autonomie entsteht im Loop. Sicherheit entsteht an seinen Grenzen.</text>
  </svg>
</template>
