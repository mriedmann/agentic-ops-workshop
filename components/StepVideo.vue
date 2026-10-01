<script setup lang="ts">
import { useSlideContext } from "@slidev/client";
import { computed, nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef, watch } from "vue";

// Stepped video: `steps` holds the stop timestamps written by animations.py.
// Clicks on the same slide whose element carries data-video-step="N" advance the
// video to stop N; going back rewinds to the previous stop.
const props = defineProps<{ src: string; steps: string }>();

const { $clicks, $page, $nav, $renderContext } = useSlideContext();
const frame = useTemplateRef<HTMLDivElement>("frame");
const video = useTemplateRef<HTMLVideoElement>("video");
const missing = ref(false);
const stops = ref<number[]>([]);
const blobUrl = ref<string>();

const base = import.meta.env.BASE_URL;
const url = (path: string) => `${base}${path}`.replace(/\/{2,}/g, "/");

const isLive = computed(() => ["slide", "presenter"].includes($renderContext.value) && $nav.value.currentSlideNo === $page.value);

// Click index at which each video step becomes visible, read from the v-click elements of this slide.
function stepClicks(): Map<number, number> {
  const slide = frame.value?.closest(".deck");
  const map = new Map<number, number>();
  slide?.querySelectorAll<HTMLElement>("[data-video-step]").forEach((el) => {
    const start = Number(el.dataset.slidevClicksStart ?? el.getAttribute("v-click") ?? 0);
    map.set(Number(el.dataset.videoStep), start);
  });
  return map;
}

function targetTime(clicks: number): number {
  let step = 0;
  for (const [videoStep, start] of stepClicks()) if (clicks >= start) step = Math.max(step, videoStep);
  if (step === 0) return 0;
  return stops.value[step - 1] ?? video.value?.duration ?? 0;
}

let targetPlay: number | null = null;

function stopPlayback() {
  targetPlay = null;
  video.value?.pause();
}

function seek(target: number) {
  const el = video.value;
  if (!el) return;
  stopPlayback();
  const apply = () => {
    const time = Math.min(target, Math.max(0, el.duration - 0.05));
    if (Number.isFinite(time)) el.currentTime = time;
  };
  if (el.readyState >= 1) apply();
  else el.addEventListener("loadedmetadata", apply, { once: true });
}

function playTo(target: number) {
  const el = video.value;
  if (!el) return;
  targetPlay = target;
  if (!el.paused) return;
  el.play().catch(() => {});
  const tick = () => {
    if (targetPlay == null) return;
    if (el.currentTime >= targetPlay || el.ended) {
      const reached = targetPlay;
      stopPlayback();
      if (Number.isFinite(reached)) el.currentTime = reached;
      return;
    }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

function sync(animate: boolean) {
  const el = video.value;
  if (!el) return;
  const target = targetTime($clicks.value);
  if (!Number.isFinite(target)) return;
  if (animate && isLive.value && target > el.currentTime) playTo(target);
  else seek(target);
}

// Seeking needs HTTP range requests, which simple static servers (`python3 -m http.server`)
// do not support. Loading the (small) video as a blob keeps it seekable with any server.
async function loadVideo() {
  const response = await fetch(url(props.src));
  if (!response.ok) throw new Error(`${props.src}: ${response.status}`);
  blobUrl.value = URL.createObjectURL(await response.blob());
}

async function loadStops() {
  try {
    const response = await fetch(url(props.steps));
    stops.value = (await response.json()).stops ?? [];
  } catch {
    stops.value = [];
  }
}

onMounted(async () => {
  await Promise.all([loadStops(), loadVideo().catch(() => (missing.value = true))]);
  await nextTick();
  sync(false);
});

watch($clicks, (now, before) => sync(now > before));
watch(isLive, (live) => {
  if (!live) stopPlayback();
  sync(false);
});

onBeforeUnmount(() => {
  stopPlayback();
  if (blobUrl.value) URL.revokeObjectURL(blobUrl.value);
});
</script>

<template>
  <div ref="frame" class="media-frame" :class="{ missing }">
    <video ref="video" muted playsinline preload="auto" :src="blobUrl" @error="blobUrl && (missing = true)" />
    <div class="media-fallback"><slot /></div>
  </div>
</template>
