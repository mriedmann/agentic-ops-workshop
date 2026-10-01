<script setup lang="ts">
// Two clicks: one per card.
defineProps<{ at: number }>();
</script>

<template>
  <div class="compare">
    <article class="compare-card" v-click="at">
      <span class="tag">TRAINING</span>
      <h3>Gewichte lernen</h3>
      <ul><li>sehr viele Beispiele</li><li>Vorhersagefehler reduzieren</li><li>teuer, batch-orientiert, selten</li></ul>
      <div class="card-footer">Daten → Optimierung → Modell</div>
    </article>
    <article class="compare-card accent-card" v-click="at + 1">
      <span class="tag">INFERENZ</span>
      <h3>Gewichte anwenden</h3>
      <ul><li>Prompt + aktueller Kontext</li><li>Token für Token decodieren</li><li>latenzkritisch, ständig</li></ul>
      <div class="card-footer">Kontext → Modell → Ausgabe</div>
    </article>
  </div>
</template>
