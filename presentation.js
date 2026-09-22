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

function updateSection(slide) {
  const label = document.querySelector("#deck-section");
  if (label && slide) label.textContent = (slide.dataset.section || "Workshop").toUpperCase();
}

function syncVideos(activeSlide) {
  document.querySelectorAll("video").forEach((video) => {
    const isActive = activeSlide?.contains(video);
    if (isActive) {
      video.currentTime = 0;
      video.play().catch(() => {});
    } else {
      video.pause();
    }
  });
}

document.querySelectorAll("video").forEach((video) => {
  video.addEventListener("error", () => video.closest(".media-frame")?.classList.add("missing"));
  video.querySelector("source")?.addEventListener("error", () => video.closest(".media-frame")?.classList.add("missing"));
});

deck.initialize().then(() => {
  updateSection(deck.getCurrentSlide());
  syncVideos(deck.getCurrentSlide());
});

deck.on("slidechanged", ({ currentSlide }) => {
  updateSection(currentSlide);
  syncVideos(currentSlide);
});
