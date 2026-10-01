<script setup lang="ts">
// Two clicks: one per phase.
defineProps<{ at: number }>();
</script>

<template>
  <div class="phase-cards">
    <article class="phase-card" v-click="at">
      <header><small>01</small><b>Prefill</b></header>
      <div class="token-strip">
        <span>Aus</span><span>␣dem</span><span>␣kleinen</span><span>␣Set</span><span>z</span><span>ling</span><span>␣wurde</span><span>␣ein</span><span>␣großer</span>
      </div>
      <p>Alle Tokens des Prompts laufen gleichzeitig durch das Modell. Dabei entsteht der KV-Cache.</p>
      <footer>bestimmt die Zeit bis zum ersten Token · <b>TTFT</b></footer>
    </article>
    <article class="phase-card decode" v-click="at + 1">
      <header><small>02</small><b>Decode</b></header>
      <div class="token-strip">
        <span class="done">␣großer</span><span class="new">␣Baum</span><span class="next">?</span><span class="next">?</span>
      </div>
      <p>Je Durchlauf entsteht genau ein Token. Der Cache wird gelesen und um das neue Token erweitert.</p>
      <footer>bestimmt die Ausgabegeschwindigkeit · <b>Tokens/s</b></footer>
    </article>
  </div>
</template>
