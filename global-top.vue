<script setup lang="ts">
import { useNav } from "@slidev/client";
import { computed } from "vue";

const { currentSlideNo, currentSlideRoute, total } = useNav();

const section = computed(() => String(currentSlideRoute.value.meta?.slide?.frontmatter?.section ?? "Workshop").toUpperCase());
const progress = computed(() => (total.value > 1 ? (currentSlideNo.value - 1) / (total.value - 1) : 0));
</script>

<template>
  <div class="deck-chrome" aria-hidden="true">
    <span class="deck-brand">AGENTIC OPS · WORKSHOP</span>
    <span class="deck-section">{{ section }}</span>
  </div>
  <div class="deck-number">{{ currentSlideNo }}/{{ total }}</div>
  <div class="deck-progress" aria-hidden="true"><span :style="{ transform: `scaleX(${progress})` }" /></div>
</template>
