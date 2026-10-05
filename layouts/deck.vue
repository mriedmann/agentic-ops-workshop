<script setup lang="ts">
import { useSlideContext } from "@slidev/client";
import StepRail from "../components/StepRail.vue";

// Frontmatter keys arrive as attributes; only `class` belongs on the slide element.
defineOptions({ inheritAttrs: false });

const { $frontmatter } = useSlideContext();
</script>

<template>
  <section
    class="deck"
    :class="[{ chapter: $frontmatter.chapter != null, 'video-slide': $frontmatter.video || $frontmatter.anim }, $attrs.class]"
    :style="$frontmatter.bg ? { background: $frontmatter.bg } : undefined"
  >
    <StepRail v-if="$frontmatter.step" kind="pipeline" :current="$frontmatter.step" />
    <StepRail v-if="$frontmatter.exercise" kind="exercise" :current="$frontmatter.exercise" />
    <slot />
  </section>
</template>
