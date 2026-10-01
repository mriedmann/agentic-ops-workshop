<script setup lang="ts">
defineProps<{ command: string }>();
</script>

<template>
  <div class="hero-terminal" aria-label="Terminal-Ausgabe">
    <span class="prompt">$</span> {{ command }}
    <span class="cursor"></span>
  </div>
</template>
