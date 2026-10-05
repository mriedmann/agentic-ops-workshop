<script setup lang="ts">
import { useTemplateRef } from "vue";
import { alongPath, drawIn, fadeIn, fadeOut, slideIn, svg, useSceneTimeline } from "../../animations/scene";

// Every path to a backend runs through LiteLLM — models, cluster tools and the knowledge base.
type Box = { x: number; y: number; width: number; height: number };
const box = (cx: number, cy: number, width: number, height = 54): Box => ({ x: cx - width / 2, y: cy - height / 2, width, height });
const right = (b: Box, dy = 0) => [b.x + b.width, b.y + b.height / 2 + dy] as const;
const leftOf = (b: Box, dy = 0) => [b.x, b.y + b.height / 2 + dy] as const;

const NODES = [
  { part: "operator", label: "Operator", color: "var(--cyan)", box: box(118, 360, 190) },
  { part: "opencode", label: "OpenCode", color: "var(--mint)", box: box(358, 360, 196) },
  { part: "model", label: "Modell", color: "var(--violet)", box: box(872, 184, 192) },
  { part: "mcp", label: "OpenShift MCP", color: "var(--coral)", box: box(872, 328, 240) },
  { part: "api", label: "OpenShift API", color: "var(--mint)", box: box(1146, 328, 230) },
];
const KNOWLEDGE_NODES = [
  { part: "knowledge", label: "AnythingLLM · MCP", color: "var(--mint)", box: box(872, 512, 272) },
  { part: "pgvector", label: "pgvector", color: "var(--muted)", box: box(1146, 512, 192) },
  { part: "ingest", label: "Ingest-Job", color: "var(--muted)", box: box(872, 624, 208) },
];
const node = (part: string) => [...NODES, ...KNOWLEDGE_NODES].find((n) => n.part === part)!.box;
const GATEWAY = box(600, 360, 224, 204);

// An arrow from a to b, kept 10px clear of both ends, with a separate head so it can follow the line.
// Heads are placed with a transform attribute and need transform-box: view-box (scenes default to fill-box).
const arrow = (part: string, color: string, a: readonly [number, number], b: readonly [number, number]) => {
  const angle = Math.atan2(b[1] - a[1], b[0] - a[0]);
  const [dx, dy] = [Math.cos(angle) * 10, Math.sin(angle) * 10];
  const end = [b[0] - dx, b[1] - dy];
  return {
    part,
    color,
    line: { x1: a[0] + dx, y1: a[1] + dy, x2: end[0] - dx, y2: end[1] - dy },
    head: `translate(${end[0]} ${end[1]}) rotate(${(angle * 180) / Math.PI})`,
  };
};
const CONNECTIONS = [
  arrow("c-operator", "var(--cyan)", right(node("operator")), leftOf(node("opencode"))),
  arrow("c-opencode", "var(--mint)", right(node("opencode")), leftOf(GATEWAY)),
  arrow("c-model", "var(--violet)", right(GATEWAY, -64), leftOf(node("model"))),
  arrow("c-mcp", "var(--coral)", right(GATEWAY, 8), leftOf(node("mcp"))),
  arrow("c-api", "var(--mint)", right(node("mcp")), leftOf(node("api"))),
];
const KNOWLEDGE_ARROWS = [
  arrow("k-knowledge", "var(--mint)", right(GATEWAY, 80), leftOf(node("knowledge"))),
  arrow("k-pgvector", "var(--muted)", right(node("knowledge")), leftOf(node("pgvector"))),
];
const INGEST_ARROW = arrow("k-ingest", "var(--muted)", [872, node("ingest").y], [872, node("knowledge").y + node("knowledge").height]);
const BACK = arrow("back", "var(--amber)", [node("knowledge").x - 8, 524], [600, GATEWAY.y + GATEWAY.height + 4]);
const PACKET_COLORS = ["var(--cyan)", "var(--mint)", "var(--violet)", "var(--coral)", "var(--mint)"];

const BOUNDARIES = [
  { x: 237, label: "Nutzer" },
  { x: 472, label: "Gateway" },
  { x: 726, label: "Backend" },
];

const root = useTemplateRef<SVGSVGElement>("root");

useSceneTimeline(root, (tl, q) => {
  // Draws arrows in parallel (stagger 0) or one after another; heads appear when their line arrives.
  const drawArrows = (parts: string[], stagger = 120) => {
    parts.forEach((part, i) => {
      tl.add(svg.createDrawable(q(`${part}-line`)), drawIn({ duration: 450 }), i ? `<<+=${stagger}` : undefined);
      tl.add(q(`${part}-head`), fadeIn({ duration: 150 }), "<-=150");
    });
  };

  tl.add(q("node-main"), slideIn(-12, 0, { delay: (_: unknown, i: number) => i * 100 }));
  tl.add(q("arrows-main"), fadeIn({ duration: 1 }));
  drawArrows(CONNECTIONS.map((c) => c.part));
  tl.label("s1");

  tl.add(q("model-path tool-path"), fadeIn({ duration: 450 }));
  q("packet").forEach((packet, i) => {
    tl.add(packet, fadeIn({ duration: 1 }), i ? "<<" : undefined);
    tl.add(packet, alongPath(q(`${CONNECTIONS[i].part}-line`)[0], { duration: 1350, ease: "linear" }), "<<");
  });
  tl.add(q("packet"), fadeOut({ duration: 1 }));
  tl.label("s2");

  tl.add(q("boundaries"), fadeIn({ duration: 1 }));
  tl.add(svg.createDrawable(q("boundary-line")), drawIn({ duration: 600, delay: (_: unknown, i: number) => i * 120 }), "<<");
  tl.add(q("boundary-label"), fadeIn({ delay: (_: unknown, i: number) => i * 120 }), "<<");
  tl.add(q("note"), fadeIn({ duration: 450 }));
  tl.label("s3");

  tl.add(q("note"), fadeOut());
  tl.add(q("node-knowledge node-pgvector"), slideIn(12, 0, { duration: 600 }), "<<");
  tl.add(q("arrows-knowledge"), fadeIn({ duration: 1 }));
  drawArrows(["k-knowledge", "k-pgvector"], 0);
  tl.add(q("knowledge-path"), fadeIn({ duration: 700 }), "<<");
  tl.add(q("back"), fadeIn({ duration: 600 }));
  tl.add(q("node-ingest ingest"), slideIn(0, 12, { duration: 700 }));
  tl.add(svg.createDrawable(q("k-ingest-line")), drawIn({ duration: 600 }), "<<");
  tl.add(q("k-ingest-head"), fadeIn({ duration: 150 }), "<-=150");
  tl.add(q("closing"), fadeIn());
  tl.label("s4");
});
</script>

<template>
  <svg ref="root" class="scene" viewBox="0 0 1280 720">
    <!-- The diagram is drawn on the full canvas and scaled down to leave room for the notes below. -->
    <g transform="translate(38 4) scale(0.94)">
    <g data-part="boundaries" style="opacity: 0">
      <template v-for="b in BOUNDARIES" :key="b.x">
        <line data-part="boundary-line" :x1="b.x" y1="70" :x2="b.x" y2="640" style="stroke: var(--line); stroke-width: 2; stroke-opacity: 0.8" />
        <text data-part="boundary-label" class="muted" :x="b.x" y="668" font-size="19" text-anchor="middle" style="opacity: 0">{{ b.label }}</text>
      </template>
    </g>

    <g v-for="n in NODES" :key="n.part" :data-part="`node-main node-${n.part}`" style="opacity: 0">
      <rect v-bind="n.box" rx="12" :style="{ fill: n.color, fillOpacity: 0.12, stroke: n.color, strokeWidth: 2 }" />
      <text :x="n.box.x + n.box.width / 2" :y="n.box.y + n.box.height / 2 + 9" font-size="26" text-anchor="middle">{{ n.label }}</text>
    </g>
    <g data-part="node-main node-gateway" style="opacity: 0">
      <rect v-bind="GATEWAY" rx="16" style="fill: var(--panel); stroke: var(--amber); stroke-width: 2" />
      <text :x="GATEWAY.x + GATEWAY.width / 2" y="314" font-size="30" font-weight="700" text-anchor="middle">LiteLLM</text>
      <text class="muted" :x="GATEWAY.x + GATEWAY.width / 2" y="350" font-size="21" text-anchor="middle">Model-Proxy</text>
      <text class="muted" :x="GATEWAY.x + GATEWAY.width / 2" y="382" font-size="21" text-anchor="middle">MCP-Proxy</text>
      <text :x="GATEWAY.x + GATEWAY.width / 2" y="416" font-size="17" text-anchor="middle" style="fill: var(--amber)">Access Control · Metering</text>
    </g>

    <g data-part="arrows-main" style="opacity: 0">
      <g v-for="c in CONNECTIONS" :key="c.part">
        <line :data-part="`${c.part}-line`" v-bind="c.line" :style="{ stroke: c.color, strokeWidth: 3 }" />
        <path :data-part="`${c.part}-head`" d="M 0 0 L -13 -7 L -13 7 z" :transform="c.head" :style="{ fill: c.color, opacity: 0, transformBox: 'view-box' }" />
      </g>
    </g>

    <text data-part="model-path" x="928" y="108" font-size="22" text-anchor="middle" style="fill: var(--violet); opacity: 0">Modellpfad · Routing · Budget</text>
    <text data-part="tool-path" x="1008" y="410" font-size="22" text-anchor="middle" style="fill: var(--coral); opacity: 0">Toolpfad · Tool-Schema · RBAC</text>
    <circle v-for="(color, i) in PACKET_COLORS" :key="i" data-part="packet" cx="0" cy="0" r="7" :style="{ fill: color, opacity: 0 }" />

    <g v-for="n in KNOWLEDGE_NODES" :key="n.part" :data-part="`node-${n.part}`" style="opacity: 0">
      <rect v-bind="n.box" rx="12" :style="{ fill: n.color, fillOpacity: 0.12, stroke: n.color, strokeWidth: 2 }" />
      <text :x="n.box.x + n.box.width / 2" :y="n.box.y + n.box.height / 2 + 9" font-size="26" text-anchor="middle">{{ n.label }}</text>
    </g>
    <text data-part="ingest" class="muted" :x="node('ingest').x + node('ingest').width + 22" y="630" font-size="18" style="opacity: 0">läuft im Hintergrund</text>
    <g data-part="arrows-knowledge" style="opacity: 0">
      <g v-for="c in [...KNOWLEDGE_ARROWS, INGEST_ARROW]" :key="c.part">
        <line :data-part="`${c.part}-line`" v-bind="c.line" :style="{ stroke: c.color, strokeWidth: 3 }" />
        <path :data-part="`${c.part}-head`" d="M 0 0 L -13 -7 L -13 7 z" :transform="c.head" :style="{ fill: c.color, opacity: 0, transformBox: 'view-box' }" />
      </g>
    </g>
    <text data-part="knowledge-path" x="1064" y="594" font-size="22" text-anchor="middle" style="fill: var(--mint); opacity: 0">Wissenspfad · Belege</text>
    <g data-part="back" style="opacity: 0">
      <line v-bind="BACK.line" style="stroke: var(--amber); stroke-width: 2; stroke-dasharray: 10 8" />
      <path d="M 0 0 L -13 -7 L -13 7 z" :transform="BACK.head" style="fill: var(--amber); transform-box: view-box" />
      <text x="672" y="554" font-size="17" text-anchor="middle" style="fill: var(--amber)">Modelle + Embeddings</text>
    </g>

    </g>

    <text data-part="note" class="muted" x="640" y="684" font-size="23" text-anchor="middle" style="opacity: 0">Ein Weg nach draußen. Autorisiert wird trotzdem an jeder Grenze einzeln.</text>
    <text data-part="closing" class="muted" x="640" y="684" font-size="23" text-anchor="middle" style="opacity: 0">Auch die Wissensbasis ist ein MCP-Server hinter demselben Gateway.</text>
  </svg>
</template>
