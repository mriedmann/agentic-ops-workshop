<script setup lang="ts">
import { useSlideContext } from "@slidev/client";
import type { Timeline } from "animejs";
import { computed, onBeforeUnmount, provide, shallowRef, useTemplateRef, watch, type Component } from "vue";
import { SCENE_TIMELINE } from "../animations/scene";

// Stepped animation: renders the scene components/anim/<Name>.vue for `name` (kebab-case).
// Clicks on the same slide whose element carries data-anim-step="N" play the scene's
// timeline to label "sN"; going back, print, export and overview jump there directly.
const props = defineProps<{ name: string }>();

const scenes = import.meta.glob<Component>("./anim/*.vue", { eager: true, import: "default" });
const pascal = (slug: string) => slug.replace(/(^|-)(\w)/g, (_, _dash, char: string) => char.toUpperCase());
const scene = computed(() => scenes[`./anim/${pascal(props.name)}.vue`]);

const { $clicks, $page, $nav, $renderContext } = useSlideContext();
const frame = useTemplateRef<HTMLDivElement>("frame");
const timeline = shallowRef<Timeline>();

const isLive = computed(() => ["slide", "presenter"].includes($renderContext.value) && $nav.value.currentSlideNo === $page.value);

// Click index at which each step starts, read from the v-click elements of this slide.
function stepClicks(): Map<number, number> {
  const slide = frame.value?.closest(".deck");
  const map = new Map<number, number>();
  slide?.querySelectorAll<HTMLElement>("[data-anim-step]").forEach((el) => {
    const start = Number(el.dataset.slidevClicksStart ?? el.getAttribute("v-click") ?? 0);
    map.set(Number(el.dataset.animStep), start);
  });
  return map;
}

function targetTime(clicks: number): number {
  const tl = timeline.value;
  if (!tl) return 0;
  let step = 0;
  for (const [animStep, start] of stepClicks()) if (clicks >= start) step = Math.max(step, animStep);
  return step === 0 ? 0 : (tl.labels[`s${step}`] ?? tl.duration);
}

// The timeline never runs on its own: playing means seeking forward frame by frame up to the target.
let frameRequest = 0;
const stopPlayback = () => cancelAnimationFrame(frameRequest);

function playTo(target: number) {
  const tl = timeline.value!;
  stopPlayback();
  let last = performance.now();
  const tick = (now: number) => {
    const time = Math.min(target, tl.currentTime + (now - last));
    last = now;
    tl.seek(time);
    if (time < target) frameRequest = requestAnimationFrame(tick);
  };
  frameRequest = requestAnimationFrame(tick);
}

function sync(animate: boolean) {
  const tl = timeline.value;
  if (!tl) return;
  const target = targetTime($clicks.value);
  if (animate && isLive.value && target > tl.currentTime) playTo(target);
  else {
    stopPlayback();
    tl.seek(target);
  }
}

// The scene registers its timeline when it is mounted, before this component is.
provide(SCENE_TIMELINE, (tl) => {
  timeline.value = tl;
  // Tooling (forward/backward seek comparison) sets window.__sceneDebug to reach the timelines.
  if ((window as any).__sceneDebug) ((window as any).__sceneTimelines ??= {})[props.name] = tl;
  tl.seek(0);
  queueMicrotask(() => sync(false));
});

watch($clicks, (now, before) => sync(now > before));
watch(isLive, () => sync(false));
onBeforeUnmount(stopPlayback);
</script>

<template>
  <div ref="frame" class="media-frame scene-frame">
    <component :is="scene" v-if="scene" />
    <div v-else class="media-fallback">Animation „{{ name }}“ fehlt (components/anim/{{ pascal(name) }}.vue)</div>
  </div>
</template>
