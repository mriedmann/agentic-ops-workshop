<script setup lang="ts">
// Two clicks: the nested rings, then the focus card.
defineProps<{ at: number }>();
</script>

<template>
  <div class="nested-map" aria-label="Einordnung von AI-Begriffen">
    <div class="ring ai" v-click="at"><span>Artificial Intelligence</span>
      <div class="ring ml"><span>Machine Learning</span>
        <div class="ring dl"><span>Deep Learning</span>
          <div class="ring llm"><span>LLM</span></div>
        </div>
      </div>
    </div>
    <div class="product-card" v-click="at + 1">
      <small>UNSER FOKUS HEUTE</small>
      <strong>AI Agent</strong>
      <span>Modell + Loop + Tools + Berechtigungen</span>
      <span class="examples">Claude Code · OpenCode · Codex</span>
    </div>
  </div>
</template>
