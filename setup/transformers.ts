import { expandSlide } from "./expand.mjs";

// Expands the compact slide syntax (see AGENTS.md) into HTML before Slidev renders the Markdown.
export default () => ({
  pre: [
    (ctx: any) => {
      const source = ctx.s.toString();
      if (!source.trim()) return;
      const html = expandSlide(source, ctx.slide.frontmatter);
      ctx.s.overwrite(0, ctx.s.original.length, html);
    },
  ],
});
