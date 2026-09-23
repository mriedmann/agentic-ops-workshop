"""Short, silent Manim scenes used by the RevealJS deck.

Render all scenes with:
    ./scripts/render-animations.sh

Each scene marks its main steps with ``self.step()``. The step timestamps are
written to ``media/<slug>.steps.json``; the deck plays the video from stop to
stop on each click instead of running it as a loop.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from manim import (
    AnimationGroup,
    Arrow,
    BLUE,
    Brace,
    Circle,
    Create,
    CubicBezier,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    GrowArrow,
    GrowFromCenter,
    LaggedStart,
    LEFT,
    Line,
    MoveAlongPath,
    ORANGE,
    PI,
    PURPLE,
    RED,
    RIGHT,
    RoundedRectangle,
    Scene,
    Succession,
    Text,
    UP,
    VGroup,
    WHITE,
    Write,
    YELLOW,
    config,
    linear,
    smooth,
)


config.background_color = "#07111f"
config.pixel_width = 1280
config.pixel_height = 720
config.frame_width = 16
config.frame_height = 9
Text.set_default(font="DejaVu Sans")

INK = "#e8f1fa"
MUTED = "#91a4b7"
CYAN = "#4de3ff"
MINT = "#54f5b1"
AMBER = "#ffca5c"
CORAL = "#ff6b6b"
PANEL = "#0d2035"
EDGE = "#21405d"

MEDIA_DIR = Path(__file__).parent / "media"


# Running example used by all LLM basics slides (token → … → next token).
# Token IDs are real o200k_base IDs (GPT-4o tokenizer), reproducible with:
#   uv run --with tiktoken python -c "import tiktoken; e = tiktoken.get_encoding('o200k_base'); \
#     print([(e.decode([i]), i) for i in e.encode('Aus dem kleinen Setzling wurde ein großer')])"
EXAMPLE_TOKENIZER = "o200k_base"
EXAMPLE_PROMPT = "Aus dem kleinen Setzling wurde ein großer"
EXAMPLE_TOKENS = [
    ("Aus", 57115),
    (" dem", 2019),
    (" kleinen", 42535),
    (" Set", 3957),
    ("z", 89),
    ("ling", 3321),
    (" wurde", 11653),
    (" ein", 1605),
    (" großer", 86085),
]
EXAMPLE_ANSWER = " Baum"

# Next-token candidates (each a single o200k_base token) with illustrative logits.
# The values are made up for teaching; probabilities are derived via softmax so
# that temperature can be shown consistently.
EXAMPLE_CANDIDATES = [
    (" Baum", 70581, 6.1),
    (" Busch", 151135, 4.6),
    (" Wald", 57653, 4.1),
    (" Mann", 23959, 3.8),
    (" Erfolg", 62279, 3.0),
]


def softmax(logits: list[float], temperature: float = 1.0) -> list[float]:
    scaled = np.array(logits) / temperature
    weights = np.exp(scaled - scaled.max())
    return list(weights / weights.sum())


class SteppedScene(Scene):
    """Scene whose main steps become click stops in the deck."""

    slug: str = ""

    def setup(self):
        self.stops: list[float] = []

    def step(self, hold: float = 0.3):
        """End a main step: hold the frame briefly and record a stop in the middle of the hold."""
        self.wait(hold)
        self.stops.append(round(self.renderer.time - hold / 2, 3))

    def tear_down(self):
        if not config.write_to_movie or not self.slug:
            return
        MEDIA_DIR.mkdir(exist_ok=True)
        data = {"stops": self.stops, "duration": round(self.renderer.time, 3)}
        (MEDIA_DIR / f"{self.slug}.steps.json").write_text(json.dumps(data, indent=2) + "\n")


def heading(text: str, kicker: str) -> VGroup:
    small = Text(kicker.upper(), font_size=18, color=CYAN, weight="BOLD")
    title = Text(text, font_size=42, color=INK, weight="BOLD")
    group = VGroup(small, title).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    group.to_edge(UP, buff=0.45).to_edge(LEFT, buff=0.65)
    return group


def pill(text: str, color: str = CYAN, width: float | None = None, height: float = 0.66, font_size: int = 23) -> VGroup:
    label = Text(text, font_size=font_size, color=INK)
    box = RoundedRectangle(
        width=width or label.width + 0.5,
        height=height,
        corner_radius=0.16,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.12,
    )
    return VGroup(box, label)


def flow_arrow(start, end, color=CYAN) -> Arrow:
    return Arrow(start, end, buff=0.12, color=color, stroke_width=3, max_tip_length_to_length_ratio=0.16)


class TokenPipeline(SteppedScene):
    """The running example is split into tokens and their vocabulary IDs."""

    slug = "token-pipeline"

    def construct(self):
        title = heading("Aus Text werden Tokens", "SCHRITT 1 · TOKEN")
        sentence = Text(EXAMPLE_PROMPT + " …", font_size=34, color=INK)
        sentence.move_to(UP * 2.1)
        self.play(FadeIn(title, shift=DOWN * 0.15), Write(sentence), run_time=0.9)
        self.step()

        # The three pieces of "Setzling" share one color: one word, three tokens.
        word_colors = [CYAN, MINT, CYAN, AMBER, AMBER, AMBER, MINT, CYAN, MINT]
        tokens = VGroup(
            *[pill(text.replace(" ", "␣"), color, height=0.6, font_size=20) for (text, _), color in zip(EXAMPLE_TOKENS, word_colors)]
        )
        tokens.arrange(RIGHT, buff=0.14).move_to(UP * 0.1)
        arrow1 = flow_arrow(sentence.get_bottom(), tokens.get_top())

        self.play(GrowArrow(arrow1), run_time=0.35)
        self.play(LaggedStart(*[GrowFromCenter(token) for token in tokens], lag_ratio=0.1), run_time=1.1)
        legend = Text("␣ steht für das führende Leerzeichen", font_size=17, color=MUTED)
        legend.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(legend), run_time=0.3)
        self.step()

        ids = VGroup()
        id_lines = VGroup()
        for token, (_, token_id), color in zip(tokens, EXAMPLE_TOKENS, word_colors):
            ident = Text(str(token_id), font_size=18, color=color, font="DejaVu Sans Mono")
            ident.next_to(token, DOWN, buff=0.4)
            ids.add(ident)
            id_lines.add(Line(token.get_bottom(), ident.get_top(), color=color, stroke_opacity=0.5))
        vocab = Text(f"IDs aus dem Vokabular des Tokenizers ({EXAMPLE_TOKENIZER})", font_size=18, color=MUTED)
        vocab.next_to(ids, DOWN, buff=0.35)
        self.play(Create(id_lines), FadeIn(ids, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(vocab), run_time=0.3)
        self.step()

        setzling = VGroup(*tokens[3:6])
        brace = Brace(setzling, UP, color=AMBER, buff=0.5)
        brace_label = Text("ein Wort → drei Tokens", font_size=20, color=AMBER)
        brace_label.next_to(brace, UP, buff=0.12)
        self.play(FadeOut(arrow1), run_time=0.25)
        self.play(GrowFromCenter(brace), FadeIn(brace_label, shift=DOWN * 0.1), run_time=0.6)
        self.step()


class TokenVector(SteppedScene):
    """A token becomes a vector: a list of learned numbers."""

    slug = "token-vector"

    NUMBERS = {
        "Baum": [0.21, -0.83, 0.04, 1.12, -0.47, 0.60],
        "Auto": [-0.66, 0.35, 0.88, -0.12, 0.74, -0.29],
    }

    def vector_row(self, word: str, color: str, y: float) -> tuple[VGroup, VGroup]:
        token = pill(word, color, width=2.0)
        numbers = Text(
            "[ " + "  ".join(f"{value:+.2f}" for value in self.NUMBERS[word]) + "  … ]",
            font_size=24,
            color=INK,
            font="DejaVu Sans Mono",
        )
        numbers.next_to(token, RIGHT, buff=1.1)
        arrow = flow_arrow(token.get_right(), numbers.get_left(), color)
        row = VGroup(token, arrow, numbers).move_to(UP * y)
        bars = VGroup(
            *[
                RoundedRectangle(
                    width=0.3,
                    height=0.25 + 0.5 * abs(value),
                    corner_radius=0.06,
                    stroke_width=0,
                    fill_color=color,
                    fill_opacity=0.35 + 0.45 * abs(value),
                )
                for value in self.NUMBERS[word]
            ]
        ).arrange(RIGHT, buff=0.12)
        bars.next_to(numbers, DOWN, buff=0.3).align_to(numbers, LEFT)
        return row, bars

    def construct(self):
        title = heading("Ein Token wird zu einem Vektor", "SCHRITT 2 · EMBEDDING")
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.5)

        baum_row, baum_bars = self.vector_row("Baum", MINT, 1.3)
        self.play(FadeIn(baum_row[0], shift=RIGHT * 0.2), run_time=0.5)
        self.play(GrowArrow(baum_row[1]), Write(baum_row[2]), run_time=0.9)
        size_note = Text("in echten Modellen einige tausend Zahlen je Token", font_size=19, color=MUTED)
        size_note.next_to(baum_row[2], UP, buff=0.35)
        self.play(FadeIn(size_note), run_time=0.35)
        self.step()

        self.play(LaggedStart(*[GrowFromCenter(bar) for bar in baum_bars], lag_ratio=0.1), run_time=0.7)
        learned = Text("Die Zahlen sind im Training gelernt, nicht von Hand gesetzt.", font_size=21, color=MUTED)
        learned.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(learned), run_time=0.4)
        self.step()

        auto_row, auto_bars = self.vector_row("Auto", CORAL, -1.4)
        self.play(FadeIn(auto_row[0], shift=RIGHT * 0.2), GrowArrow(auto_row[1]), Write(auto_row[2]), run_time=0.9)
        self.play(LaggedStart(*[GrowFromCenter(bar) for bar in auto_bars], lag_ratio=0.1), run_time=0.7)
        self.step()

        compare = pill("andere Bedeutung → anderes Zahlenmuster", AMBER, width=8.4)
        compare.move_to(DOWN * 3.05)
        self.play(FadeOut(learned), FadeIn(compare, shift=UP * 0.2), run_time=0.6)
        self.step()


class EmbeddingSpace(SteppedScene):
    """Words with similar meaning sit close together; equal relations share direction."""

    slug = "embedding-space"

    CLUSTERS = [
        ("Pflanzen", MINT, {"Setzling": (-4.5, -1.9), "Baum": (-3.2, -1.2), "Blume": (-4.9, -0.7), "Strauch": (-3.4, -2.3)}),
        ("Tiere", AMBER, {"Welpe": (-1.5, 0.9), "Hund": (-0.2, 1.6), "Kalb": (-1.0, -0.2), "Kuh": (0.3, 0.5)}),
        ("Fahrzeuge", CORAL, {"Fahrrad": (2.9, -1.9), "Auto": (3.4, -0.8), "LKW": (4.7, -0.1), "Bus": (4.6, -1.4)}),
    ]
    ANALOGIES = [("Setzling", "Baum"), ("Kalb", "Kuh"), ("Welpe", "Hund")]

    def construct(self):
        title = heading("Ähnliche Bedeutung liegt nah beieinander", "SCHRITT 2 · EMBEDDING")
        x_axis = Arrow(np.array([-6.2, -3.5, 0]), np.array([5.9, -3.5, 0]), buff=0, color=EDGE, stroke_width=2.5)
        y_axis = Arrow(np.array([-6.2, -3.5, 0]), np.array([-6.2, 3.0, 0]), buff=0, color=EDGE, stroke_width=2.5)
        x_label = Text("Dimension 1", font_size=17, color=MUTED).next_to(x_axis, DOWN, buff=0.12).align_to(x_axis, RIGHT)
        y_label = Text("Dimension 2", font_size=17, color=MUTED).rotate(PI / 2).next_to(y_axis, LEFT, buff=0.12)
        self.play(FadeIn(title, shift=DOWN * 0.15), Create(x_axis), Create(y_axis), FadeIn(x_label), FadeIn(y_label), run_time=0.8)

        self.dots: dict[str, Dot] = {}
        groups = []
        for name, color, words in self.CLUSTERS:
            items = VGroup()
            for word, (x, y) in words.items():
                dot = Dot(np.array([x, y, 0]), radius=0.08, color=color)
                label = Text(word, font_size=20, color=INK).next_to(dot, UP, buff=0.14)
                self.dots[word] = dot
                items.add(VGroup(dot, label))
            ring = Circle(color=color, stroke_width=1.6, stroke_opacity=0.5).surround(items, buffer_factor=1.12)
            ring_label = Text(name, font_size=18, color=color).next_to(ring, DOWN, buff=0.1)
            groups.append((items, VGroup(ring, ring_label)))

        first_items, first_ring = groups[0]
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.15) for item in first_items], lag_ratio=0.15), run_time=0.9)
        self.play(Create(first_ring[0]), FadeIn(first_ring[1]), run_time=0.5)
        self.step()

        for items, ring in groups[1:]:
            self.play(
                LaggedStart(*[FadeIn(item, shift=UP * 0.15) for item in items], lag_ratio=0.12),
                run_time=0.7,
            )
            self.play(Create(ring[0]), FadeIn(ring[1]), run_time=0.4)
        self.step()

        near = Line(self.dots["Baum"].get_center(), self.dots["Strauch"].get_center(), color=MINT, stroke_width=3)
        near_label = Text("nah = ähnlich", font_size=18, color=MINT).next_to(near, RIGHT, buff=0.18)
        far = Line(self.dots["Baum"].get_center(), self.dots["Auto"].get_center(), color=MUTED, stroke_width=2, stroke_opacity=0.7)
        far_label = Text("weit = unähnlich", font_size=18, color=MUTED).move_to(far.point_from_proportion(0.72) + DOWN * 0.42)
        self.play(Create(near), FadeIn(near_label), run_time=0.5)
        self.play(Create(far), FadeIn(far_label), run_time=0.5)
        self.step()

        self.play(FadeOut(near), FadeOut(near_label), FadeOut(far), FadeOut(far_label), run_time=0.4)
        arrows = VGroup(
            *[
                Arrow(
                    self.dots[start].get_center(),
                    self.dots[end].get_center(),
                    buff=0.12,
                    color=CYAN,
                    stroke_width=4,
                    max_tip_length_to_length_ratio=0.18,
                )
                for start, end in self.ANALOGIES
            ]
        )
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.2), run_time=1.0)
        relation = Text("gleiche Beziehung → gleiche Richtung und Länge", font_size=21, color=CYAN)
        relation.to_edge(DOWN, buff=0.22)
        self.play(FadeIn(relation), run_time=0.4)
        self.step()


class AttentionOps(SteppedScene):
    """Attention is visualized as contextual routing between tokens."""

    slug = "attention-ops"

    def construct(self):
        title = heading("Kontext wird gewichtet", "Transformer · Self-Attention")
        subtitle = Text("Welche Tokens helfen, „startet“ einzuordnen?", font_size=23, color=MUTED)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.2)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.7)

        words = ["Pod", "api-7f9", "startet", "wegen", "ConfigMap", "nicht"]
        colors = [MUTED, CYAN, AMBER, MUTED, MINT, CORAL]
        items = VGroup(*[pill(word, color) for word, color in zip(words, colors)])
        items.arrange(RIGHT, buff=0.25).move_to(DOWN * 0.6)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.1) for item in items], lag_ratio=0.1), run_time=0.9)
        self.step()

        focus = items[2]
        focus[0].set_fill(AMBER, opacity=0.32).set_stroke(AMBER, width=4)
        ripple = Circle(radius=0.5, color=AMBER, stroke_width=3).move_to(focus)
        self.play(Create(ripple), ripple.animate.scale(1.7).set_opacity(0), run_time=0.55)
        self.step()

        weights = {0: 0.18, 1: 0.36, 3: 0.15, 4: 0.82, 5: 0.91}
        arcs = VGroup()
        dots = VGroup()
        labels = VGroup()
        for idx, weight in weights.items():
            start = focus.get_top() + UP * 0.05
            end = items[idx].get_top() + UP * 0.05
            height = 0.75 + abs(idx - 2) * 0.2
            arc = CubicBezier(
                start,
                start + UP * height,
                end + UP * height,
                end,
                color=colors[idx],
                stroke_width=1.5 + 7 * weight,
                stroke_opacity=0.35 + 0.6 * weight,
            )
            arcs.add(arc)
            dot = Dot(radius=0.055, color=WHITE).move_to(start)
            dots.add(dot)
            label = Text(f"{weight:.2f}", font_size=16, color=colors[idx])
            label.move_to(arc.point_from_proportion(0.5) + UP * 0.18)
            labels.add(label)

        self.play(LaggedStart(*[Create(arc) for arc in arcs], lag_ratio=0.12), run_time=1.1)
        self.add(*dots)
        self.play(
            *[MoveAlongPath(dot, arc, rate_func=linear) for dot, arc in zip(dots, arcs)],
            FadeIn(labels),
            run_time=1.2,
        )
        self.remove(*dots)
        self.step()

        result = pill("startet  +  Kontext  →  Repräsentation im Satz", MINT, width=7.2)
        result.move_to(DOWN * 2.65)
        self.play(FadeIn(result, shift=UP * 0.25), run_time=0.7)
        note = Text("Gewichte sind kontextabhängig und werden in vielen Köpfen parallel berechnet.", font_size=20, color=MUTED)
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note), run_time=0.45)
        self.step()


class NextToken(SteppedScene):
    """A context update changes the next-token distribution."""

    slug = "next-token"

    def construct(self):
        title = heading("Eine Verteilung, dann eine Auswahl", "LLM · Ausgabe")
        prompt = Text("Der Pod ist im Status …", font_size=36, color=INK)
        prompt.move_to(UP * 2.0 + LEFT * 2.2)
        self.play(FadeIn(title), Write(prompt), run_time=0.85)

        names = ["CrashLoopBackOff", "Pending", "Running", "Unknown"]
        values = [0.43, 0.27, 0.21, 0.09]
        colors = [CORAL, AMBER, MINT, MUTED]
        rows = VGroup()
        bars = []
        percents = []
        for name, value, color in zip(names, values, colors):
            label = Text(name, font_size=22, color=INK, font="DejaVu Sans Mono")
            label.stretch_to_fit_width(2.7)
            track = RoundedRectangle(width=5.8, height=0.38, corner_radius=0.12, stroke_color=EDGE, fill_color=EDGE, fill_opacity=0.25)
            bar = RoundedRectangle(width=5.8 * value, height=0.38, corner_radius=0.12, stroke_width=0, fill_color=color, fill_opacity=0.9)
            bar.align_to(track, LEFT)
            pct = Text(f"{value:.0%}", font_size=19, color=color, font="DejaVu Sans Mono")
            row = VGroup(label, track, bar, pct).arrange(RIGHT, buff=0.2)
            rows.add(row)
            bars.append(bar)
            percents.append(pct)
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 0.2)
        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.25) for row in rows], lag_ratio=0.12), run_time=1.0)
        self.step()

        context = pill("+ Event: Back-off restarting failed container", CYAN, width=8.9)
        context.move_to(DOWN * 2.5)
        self.play(FadeIn(context, shift=UP * 0.2), run_time=0.55)

        new_values = [0.84, 0.08, 0.05, 0.03]
        bar_anims = []
        pct_anims = []
        for row, bar, pct, value, color in zip(rows, bars, percents, new_values, colors):
            target_bar = bar.copy().stretch_to_fit_width(5.8 * value).align_to(row[1], LEFT)
            target_pct = Text(f"{value:.0%}", font_size=19, color=color, font="DejaVu Sans Mono").move_to(pct)
            bar_anims.append(bar.animate.become(target_bar))
            pct_anims.append(pct.animate.become(target_pct))
        self.play(*bar_anims, *pct_anims, run_time=1.1, rate_func=smooth)
        self.step()

        chosen = Text("gewählt", font_size=18, color=CORAL, weight="BOLD").next_to(rows[0], RIGHT, buff=0.25)
        marker = Arrow(chosen.get_left(), rows[0].get_right(), buff=0.1, color=CORAL, stroke_width=3)
        self.play(FadeIn(chosen), GrowArrow(marker), rows[0].animate.scale(1.035), run_time=0.55)
        note = Text("Mehr Kontext verändert die Verteilung — er garantiert keine Wahrheit.", font_size=21, color=MUTED)
        note.to_edge(DOWN, buff=0.2)
        self.play(FadeOut(context), FadeIn(note), run_time=0.5)
        self.step()


class AgentLoop(SteppedScene):
    """Goal-directed tool use with explicit policy and approval gates."""

    slug = "agent-loop"

    def construct(self):
        title = heading("Vom Modell zum kontrollierten Loop", "Agent · Laufzeit")
        self.play(FadeIn(title), run_time=0.55)

        center = np.array([0.0, -0.3, 0.0])
        radius = 2.5
        labels = ["Ziel", "Beobachten", "Entscheiden", "Tool ausführen", "Ergebnis prüfen"]
        colors = [CYAN, MINT, AMBER, CORAL, PURPLE]
        angles = [PI / 2, PI / 2 + 2 * PI / 5, PI / 2 + 4 * PI / 5, PI / 2 + 6 * PI / 5, PI / 2 + 8 * PI / 5]
        nodes = VGroup()
        for text, color, angle in zip(labels, colors, angles):
            node = pill(text, color, width=2.35 if text != "Tool ausführen" else 2.75)
            node.move_to(center + radius * np.array([np.cos(angle), np.sin(angle), 0]))
            nodes.add(node)

        arrows = VGroup()
        for idx in range(len(nodes)):
            arrows.add(flow_arrow(nodes[idx].get_center(), nodes[(idx + 1) % len(nodes)].get_center(), colors[(idx + 1) % len(colors)]))
        self.play(LaggedStart(*[GrowFromCenter(node) for node in nodes], lag_ratio=0.1), run_time=0.9)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.1), run_time=0.9)
        self.step()

        policy = RoundedRectangle(width=3.15, height=1.35, corner_radius=0.18, stroke_color=EDGE, fill_color=PANEL, fill_opacity=0.94)
        policy.move_to(center)
        policy_text = VGroup(
            Text("POLICY", font_size=17, color=CYAN, weight="BOLD"),
            Text("Scope · Budget · Stop", font_size=18, color=INK),
        ).arrange(DOWN, buff=0.13).move_to(policy)
        self.play(FadeIn(policy), FadeIn(policy_text), run_time=0.55)
        self.step()

        pulse = Dot(radius=0.1, color=WHITE).move_to(nodes[0])
        self.add(pulse)
        for idx, arrow in enumerate(arrows):
            self.play(
                MoveAlongPath(pulse, arrow, rate_func=linear),
                nodes[(idx + 1) % len(nodes)][0].animate.set_fill(colors[(idx + 1) % len(colors)], opacity=0.35),
                run_time=0.35,
            )
        self.step()

        gate = pill("WRITE → Freigabe", CORAL, width=3.4).to_edge(RIGHT, buff=0.55).shift(DOWN * 2.65)
        gate_arrow = flow_arrow(nodes[3].get_right(), gate.get_left(), CORAL)
        self.play(GrowArrow(gate_arrow), FadeIn(gate), run_time=0.55)
        note = Text("Autonomie entsteht im Loop. Sicherheit entsteht an seinen Grenzen.", font_size=21, color=MUTED)
        note.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(note), run_time=0.4)
        self.step()


class TrustBoundary(SteppedScene):
    """A request moves through model and tool paths with separate controls."""

    slug = "trust-boundary"

    def construct(self):
        title = heading("Zwei Pfade, mehrere Trust Boundaries", "Agentic Ops · Architektur")
        self.play(FadeIn(title), run_time=0.55)

        specs = [
            ("Operator", CYAN, LEFT * 6),
            ("OpenCode", MINT, LEFT * 3.1),
            ("LiteLLM", AMBER, LEFT * 0.1 + UP * 1.35),
            ("Modell", PURPLE, RIGHT * 3.2 + UP * 1.35),
            ("MCP Gateway", CORAL, LEFT * 0.1 + DOWN * 1.45),
            ("OpenShift API", MINT, RIGHT * 3.2 + DOWN * 1.45),
        ]
        nodes = VGroup()
        for text, color, pos in specs:
            node = pill(text, color, width=2.35 if text != "OpenShift API" else 2.7).move_to(pos)
            nodes.add(node)
        self.play(LaggedStart(*[FadeIn(node, shift=RIGHT * 0.15) for node in nodes], lag_ratio=0.1), run_time=0.9)

        connections = VGroup(
            flow_arrow(nodes[0].get_right(), nodes[1].get_left(), CYAN),
            flow_arrow(nodes[1].get_right(), nodes[2].get_left(), AMBER),
            flow_arrow(nodes[2].get_right(), nodes[3].get_left(), PURPLE),
            flow_arrow(nodes[1].get_right(), nodes[4].get_left(), CORAL),
            flow_arrow(nodes[4].get_right(), nodes[5].get_left(), MINT),
        )
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in connections], lag_ratio=0.12), run_time=1.0)
        self.step()

        model_path = Text("Modellpfad · Routing · Budget", font_size=18, color=AMBER).move_to(UP * 2.25 + RIGHT * 1.5)
        tool_path = Text("Toolpfad · Schema · RBAC", font_size=18, color=CORAL).move_to(DOWN * 2.35 + RIGHT * 1.5)
        self.play(FadeIn(model_path), FadeIn(tool_path), run_time=0.45)

        packets = VGroup(*[Dot(radius=0.08, color=color) for color in [CYAN, AMBER, PURPLE, CORAL, MINT]])
        self.add(*packets)
        self.play(
            *[MoveAlongPath(packet, path, rate_func=linear) for packet, path in zip(packets, connections)],
            run_time=1.35,
        )
        self.remove(*packets)
        self.step()

        boundaries = VGroup()
        for x, label in [(-4.6, "User"), (-1.55, "Gateway"), (1.65, "Backend")]:
            line = Line(UP * 2.55, DOWN * 2.75, color=EDGE, stroke_width=2, stroke_opacity=0.8).move_to(RIGHT * x)
            caption = Text(label, font_size=15, color=MUTED).next_to(line, DOWN, buff=0.08)
            boundaries.add(VGroup(line, caption))
        self.play(LaggedStart(*[Create(boundary) for boundary in boundaries], lag_ratio=0.12), run_time=0.8)

        note = Text("MCP transportiert Fähigkeiten. Autorisierung bleibt Aufgabe der Plattform.", font_size=21, color=MUTED)
        note.to_edge(DOWN, buff=0.18)
        self.play(FadeIn(note), run_time=0.45)
        self.step()
