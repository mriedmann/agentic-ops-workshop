import { defineConfig } from "unocss";

// Slidev merges this with its own UnoCSS config. Some deck class names are also
// UnoCSS utilities (`.ring` adds a focus-ring shadow, `.ml` a left margin); keep
// UnoCSS from generating them so only style.css applies.
export default defineConfig({
  blocklist: ["ring", "ml"],
});
