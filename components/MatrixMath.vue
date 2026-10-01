<script setup lang="ts">
// Two clicks: the multiplication, then the worked line for the first result.
defineProps<{ at: number }>();
</script>

<template>
  <div class="matrix-math" v-click="at">
    <div class="mat vec" aria-label="Eingabevektor x">
      <small>x · Vektor eines Tokens</small>
      <div class="cells one-row"><span>0,5</span><span>−1,0</span><span>2,0</span></div>
    </div>
    <span class="op">×</span>
    <div class="mat weights" aria-label="Gewichtsmatrix W">
      <small>W · gelernte Gewichte</small>
      <div class="cells three-by-two">
        <span>1,0</span><span>2,0</span>
        <span>0,0</span><span>−1,0</span>
        <span>3,0</span><span>1,0</span>
      </div>
    </div>
    <span class="op">=</span>
    <div class="mat vec out" aria-label="Ergebnisvektor h">
      <small>h · neuer Vektor</small>
      <div class="cells one-row"><span>6,5</span><span>4,0</span></div>
    </div>
  </div>
  <p class="calc-line" v-click="at + 1">0,5 · 1,0 &nbsp;+&nbsp; (−1,0) · 0,0 &nbsp;+&nbsp; 2,0 · 3,0 &nbsp;=&nbsp; <b>6,5</b></p>
</template>
