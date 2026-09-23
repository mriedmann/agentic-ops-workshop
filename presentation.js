const deck = new Reveal({
  hash: true,
  history: true,
  center: false,
  controls: true,
  controlsTutorial: false,
  progress: true,
  slideNumber: "c/t",
  transition: "fade",
  backgroundTransition: "fade",
  width: 1280,
  height: 720,
  margin: 0,
  minScale: 0.2,
  maxScale: 2,
  plugins: [RevealNotes],
});

// GPT pipeline stations (see the "Leitfaden" slide). Slides with data-step="<key> …"
// get a small rail at the top that highlights their station(s).
const PIPELINE = [
  ["text", "Text"],
  ["token", "Token"],
  ["embedding", "Embedding"],
  ["attention", "Attention"],
  ["ffn", "Feed Forward"],
  ["residual", "Residual"],
  ["logits", "Logits"],
  ["probs", "Probabilities"],
];
const LAYER_STEPS = new Set(["attention", "ffn", "residual"]);

function renderStepRails() {
  document.querySelectorAll(".slides section[data-step]").forEach((slide) => {
    const current = slide.dataset.step.split(/\s+/);
    const first = Math.min(...current.map((key) => PIPELINE.findIndex(([k]) => k === key)));
    const rail = document.createElement("ol");
    rail.className = "step-rail";
    rail.setAttribute("aria-label", "Station in der GPT-Pipeline");
    PIPELINE.forEach(([key, label], index) => {
      const item = document.createElement("li");
      item.textContent = label;
      if (LAYER_STEPS.has(key)) item.classList.add("layer");
      if (current.includes(key)) item.classList.add("current");
      else if (index < first) item.classList.add("done");
      rail.append(item);
    });
    slide.prepend(rail);
  });
}

renderStepRails();

function updateSection(slide) {
  const label = document.querySelector("#deck-section");
  if (label && slide) label.textContent = (slide.dataset.section || "Workshop").toUpperCase();
}

// Stepped videos: <video data-steps="media/x.steps.json"> holds the stop timestamps
// written by animations.py. Fragments on the same slide with data-video-step="N"
// advance the video to stop N; hiding them rewinds to the previous stop.
const stepCache = new Map();

// Seeking needs HTTP range requests, which `python3 -m http.server` does not support.
// Loading the (small) video as a blob keeps it seekable with any static server.
async function loadAsBlob(video) {
  const source = video.querySelector("source");
  if (!source) return;
  const response = await fetch(source.src);
  if (!response.ok) throw new Error(`${source.src}: ${response.status}`);
  video.preload = "auto";
  video.src = URL.createObjectURL(await response.blob());
}

function loadStops(video) {
  if (!stepCache.has(video)) {
    const stops = fetch(video.dataset.steps)
      .then((response) => response.json())
      .then((data) => data.stops)
      .catch(() => []);
    const media = loadAsBlob(video).catch(() => video.closest(".media-frame")?.classList.add("missing"));
    stepCache.set(video, Promise.all([stops, media]).then(([result]) => result));
  }
  return stepCache.get(video);
}

function targetTime(slide, stops, video) {
  const shown = [...slide.querySelectorAll(".fragment.visible[data-video-step]")].map((f) => Number(f.dataset.videoStep));
  const step = Math.max(0, ...shown);
  if (step === 0) return 0;
  return stops[step - 1] ?? video.duration;
}

function stopPlayback(video) {
  video.targetTime = null;
  video.pause();
}

function playTo(video, target) {
  video.targetTime = target;
  if (!video.paused) return;
  video.play().catch(() => {});
  const tick = () => {
    if (video.targetTime == null) return;
    if (video.currentTime >= video.targetTime || video.ended) {
      const reached = video.targetTime;
      stopPlayback(video);
      if (Number.isFinite(reached)) video.currentTime = reached;
      return;
    }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

async function driveVideo(slide, { animate }) {
  const video = slide?.querySelector("video[data-steps]");
  if (!video) return;
  const stops = await loadStops(video);
  const target = targetTime(slide, stops, video);
  if (animate && target > video.currentTime) {
    playTo(video, target);
  } else {
    stopPlayback(video);
    video.currentTime = target;
  }
}

function syncVideos(activeSlide) {
  document.querySelectorAll("video").forEach((video) => {
    if (!activeSlide?.contains(video)) stopPlayback(video);
  });
  driveVideo(activeSlide, { animate: false });
}

// Print view renders one page per fragment state; each page shows the frame of its step.
function showPrintFrames() {
  document.querySelectorAll("video[data-steps]").forEach(async (video) => {
    const stops = await loadStops(video);
    const seek = () => {
      const target = targetTime(video.closest("section"), stops, video);
      video.currentTime = Math.min(target, video.duration - 0.05);
    };
    if (video.readyState >= 1) seek();
    else video.addEventListener("loadedmetadata", seek, { once: true });
  });
}

document.querySelectorAll("video").forEach((video) => {
  video.addEventListener("error", () => video.closest(".media-frame")?.classList.add("missing"));
  video.querySelector("source")?.addEventListener("error", () => video.closest(".media-frame")?.classList.add("missing"));
});

deck.initialize().then(() => {
  document.querySelectorAll("video[data-steps]").forEach(loadStops);
  updateSection(deck.getCurrentSlide());
  if (!deck.isPrintView()) syncVideos(deck.getCurrentSlide());
});

deck.on("pdf-ready", showPrintFrames);

deck.on("slidechanged", ({ currentSlide }) => {
  updateSection(currentSlide);
  syncVideos(currentSlide);
});

deck.on("fragmentshown", () => driveVideo(deck.getCurrentSlide(), { animate: true }));
deck.on("fragmenthidden", () => driveVideo(deck.getCurrentSlide(), { animate: false }));
