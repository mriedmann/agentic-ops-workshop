<script setup lang="ts">
import { useSlideContext } from "@slidev/client";
import StepRail from "../components/StepRail.vue";

const { $frontmatter } = useSlideContext();
</script>

<template>
  <section class="deck" :style="$frontmatter.bg ? { background: $frontmatter.bg } : undefined">
    <StepRail v-if="$frontmatter.step" kind="pipeline" :current="$frontmatter.step" />
    <StepRail v-if="$frontmatter.exercise" kind="exercise" :current="$frontmatter.exercise" />
    <slot />
  </section>
</template>
