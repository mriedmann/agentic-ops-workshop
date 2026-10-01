<script setup lang="ts">
import { computed } from "vue";

// Rails at the top of a slide show where we are in a sequence: the GPT pipeline
// (frontmatter `step`) during the basics, the exercise steps (`exercise`) in chapter 6.
const RAILS = {
  pipeline: {
    label: "Station in der GPT-Pipeline",
    stations: [
      ["text", "Text"],
      ["token", "Token"],
      ["embedding", "Embedding"],
      ["attention", "Attention"],
      ["ffn", "Feed Forward"],
      ["residual", "Residual"],
      ["logits", "Logits"],
      ["probs", "Probabilities"],
    ],
    layer: new Set(["attention", "ffn", "residual"]),
  },
  exercise: {
    label: "Schritt in der Übung",
    stations: [
      ["allein", "Allein"],
      ["zu-zweit", "Zu zweit"],
      ["zu-viert", "Zu viert"],
      ["alle", "Alle"],
      ["canvas", "Canvas"],
    ],
    layer: new Set(),
  },
} as const;

const props = defineProps<{ kind: keyof typeof RAILS; current: string }>();

const rail = computed(() => RAILS[props.kind]);
const items = computed(() => {
  const { stations, layer } = rail.value;
  const current = props.current.split(/\s+/);
  const first = Math.min(...current.map((key) => stations.findIndex(([k]) => k === key)));
  return stations.map(([key, text], index) => ({
    key,
    text,
    layer: layer.has(key),
    current: current.includes(key),
    done: !current.includes(key) && index < first,
  }));
});
</script>

<template>
  <ol class="step-rail" :aria-label="rail.label">
    <li v-for="item in items" :key="item.key" :class="{ layer: item.layer, current: item.current, done: item.done }">
      {{ item.text }}
    </li>
  </ol>
</template>
