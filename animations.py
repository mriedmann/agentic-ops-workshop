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
    """The current token collects information from the other tokens."""

    slug = "attention-ops"

    # How strongly " großer" attends to each earlier token (illustrative).
    WEIGHTS = {0: 0.05, 1: 0.04, 2: 0.31, 3: 0.44, 4: 0.09, 5: 0.52, 6: 0.06, 7: 0.05}

    def construct(self):
        title = heading("Das aktuelle Token sammelt Kontext", "SCHRITT 3 · ATTENTION")
        subtitle = Text("Welche Tokens helfen, „großer“ einzuordnen?", font_size=22, color=MUTED)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.2)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.7)

        word_colors = [MUTED, MUTED, CYAN, AMBER, AMBER, AMBER, MUTED, MUTED, MINT]
        items = VGroup(
            *[pill(text.replace(" ", "␣"), color, height=0.6, font_size=20) for (text, _), color in zip(EXAMPLE_TOKENS, word_colors)]
        )
        items.arrange(RIGHT, buff=0.14).move_to(DOWN * 1.1)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.1) for item in items], lag_ratio=0.1), run_time=1.0)
        self.step()

        focus = items[8]
        focus[0].set_fill(MINT, opacity=0.3).set_stroke(MINT, width=4)
        ripple = Circle(radius=0.55, color=MINT, stroke_width=3).move_to(focus)
        question = Text("„… wurde ein großer  ___“", font_size=24, color=INK).move_to(DOWN * 2.6)
        self.play(Create(ripple), ripple.animate.scale(1.7).set_opacity(0), run_time=0.55)
        self.play(FadeIn(question, shift=UP * 0.15), run_time=0.4)
        self.step()

        arcs, dots, labels = VGroup(), VGroup(), VGroup()
        for idx, weight in self.WEIGHTS.items():
            start_point = focus.get_top() + UP * 0.05
            end_point = items[idx].get_top() + UP * 0.05
            height = 0.6 + (8 - idx) * 0.22
            arc = CubicBezier(
                start_point,
                start_point + UP * height,
                end_point + UP * height,
                end_point,
                color=word_colors[idx] if weight > 0.2 else MUTED,
                stroke_width=1.2 + 8 * weight,
                stroke_opacity=0.3 + 0.6 * weight,
            )
            arcs.add(arc)
            dots.add(Dot(radius=0.055, color=WHITE).move_to(start_point))
            if weight > 0.2:
                label = Text(f"{weight:.2f}", font_size=17, color=word_colors[idx])
                label.move_to(arc.point_from_proportion(0.88) + UP * 0.22)
                labels.add(label)

        self.play(LaggedStart(*[Create(arc) for arc in arcs], lag_ratio=0.1), run_time=1.1)
        self.add(*dots)
        self.play(
            *[MoveAlongPath(dot, arc, rate_func=linear) for dot, arc in zip(dots, arcs)],
            FadeIn(labels),
            run_time=1.2,
        )
        self.remove(*dots)
        self.step()

        result = pill("„großer“ + Kontext → es geht um eine Pflanze, die gewachsen ist", MINT, width=10.4, font_size=21)
        result.move_to(DOWN * 2.6)
        self.play(FadeOut(question), FadeIn(result, shift=UP * 0.2), run_time=0.7)
        note = Text("Die Gewichte hängen vom Satz ab und werden in vielen Köpfen parallel berechnet.", font_size=20, color=MUTED)
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note), run_time=0.45)
        self.step()


class TransformerBlock(SteppedScene):
    """One transformer layer: attention, feed forward, each with residual + norm."""

    slug = "transformer-block"

    def vector_bars(self, values, color, width=0.16) -> VGroup:
        return VGroup(
            *[
                RoundedRectangle(
                    width=width,
                    height=0.16 + 0.4 * abs(value),
                    corner_radius=0.04,
                    stroke_width=0,
                    fill_color=color,
                    fill_opacity=0.4 + 0.5 * abs(value),
                )
                for value in values
            ]
        ).arrange(RIGHT, buff=0.05)

    def block(self, label: str, sub: str, color: str, width: float = 2.5) -> VGroup:
        box = RoundedRectangle(width=width, height=1.15, corner_radius=0.16, stroke_color=color, stroke_width=2, fill_color=PANEL, fill_opacity=0.9)
        name = Text(label, font_size=21, color=INK)
        detail = Text(sub, font_size=15, color=MUTED)
        text = VGroup(name, detail).arrange(DOWN, buff=0.12).move_to(box)
        return VGroup(box, text)

    def add_node(self, color: str) -> VGroup:
        circle = Circle(radius=0.3, color=color, stroke_width=2, fill_color=PANEL, fill_opacity=0.95)
        plus = Text("+", font_size=26, color=color).move_to(circle)
        caption = Text("Residual\n+ Norm", font_size=14, color=MUTED, line_spacing=0.6)
        caption.next_to(circle, DOWN, buff=0.16)
        return VGroup(circle, plus, caption)

    def construct(self):
        title = heading("Ein Layer: mischen, verarbeiten, dazuzählen", "TRANSFORMER · EIN LAYER")
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.5)

        row_y = 0.35
        tokens = VGroup(
            *[pill(text.replace(" ", "␣"), MUTED, height=0.5, font_size=16) for text, _ in EXAMPLE_TOKENS]
        )
        tokens.arrange(RIGHT, buff=0.1).move_to(UP * 2.75)
        tokens[8][0].set_stroke(MINT, width=3).set_fill(MINT, opacity=0.22)
        start_vector = self.vector_bars([0.3, 0.9, 0.5, 0.7, 0.4], MINT)
        start_vector.move_to(np.array([-6.3, row_y, 0]))
        start_label = Text("Vektor von „␣großer“", font_size=15, color=MUTED).next_to(start_vector, DOWN, buff=0.22)
        self.play(LaggedStart(*[FadeIn(token, shift=DOWN * 0.1) for token in tokens], lag_ratio=0.07), run_time=0.8)
        self.play(FadeIn(start_vector, shift=RIGHT * 0.2), FadeIn(start_label), run_time=0.5)
        self.step()

        attention = self.block("Self-Attention", "mischt über alle Tokens", CYAN, width=2.9)
        attention.move_to(np.array([-3.6, row_y, 0]))
        feeds = VGroup(
            *[
                Line(token.get_bottom(), attention.get_top(), color=CYAN, stroke_width=1.2, stroke_opacity=0.35)
                for token in tokens
            ]
        )
        in_arrow = flow_arrow(start_vector.get_right(), attention[0].get_left(), MINT)
        self.play(GrowArrow(in_arrow), FadeIn(attention), run_time=0.6)
        self.play(Create(feeds), run_time=0.7)
        self.step()

        add1 = self.add_node(AMBER)
        add1.move_to(np.array([-1.0, row_y, 0]))
        arrow1 = flow_arrow(attention[0].get_right(), add1[0].get_left(), CYAN)
        residual1 = CubicBezier(
            start_vector.get_top() + UP * 0.1,
            start_vector.get_top() + UP * 1.1,
            add1[0].get_top() + UP * 1.1,
            add1[0].get_top() + UP * 0.05,
            color=AMBER,
            stroke_width=2.5,
        )
        residual_label = Text("der alte Vektor bleibt erhalten", font_size=15, color=AMBER)
        residual_label.move_to(residual1.point_from_proportion(0.5) + UP * 0.25)
        self.play(GrowArrow(arrow1), FadeIn(add1), run_time=0.5)
        self.play(Create(residual1), FadeIn(residual_label), run_time=0.7)
        self.step()

        feed_forward = self.block("Feed Forward", "jedes Token für sich", PURPLE, width=2.7)
        feed_forward.move_to(np.array([1.6, row_y, 0]))
        add2 = self.add_node(AMBER)
        add2.move_to(np.array([3.9, row_y, 0]))
        arrow2 = flow_arrow(add1[0].get_right(), feed_forward[0].get_left(), AMBER)
        arrow3 = flow_arrow(feed_forward[0].get_right(), add2[0].get_left(), PURPLE)
        residual2 = CubicBezier(
            add1[0].get_top() + UP * 0.05,
            add1[0].get_top() + UP * 0.9,
            add2[0].get_top() + UP * 0.9,
            add2[0].get_top() + UP * 0.05,
            color=AMBER,
            stroke_width=2.5,
        )
        weights_note = Text("hier sitzt der größte Teil der Gewichte", font_size=15, color=MUTED)
        weights_note.next_to(feed_forward, DOWN, buff=0.7)
        self.play(GrowArrow(arrow2), FadeIn(feed_forward), run_time=0.5)
        self.play(GrowArrow(arrow3), FadeIn(add2), Create(residual2), FadeIn(weights_note), run_time=0.7)
        self.step()

        out_vector = self.vector_bars([0.5, 0.6, 0.9, 0.3, 0.8], MINT)
        out_vector.move_to(np.array([5.6, row_y, 0]))
        out_arrow = flow_arrow(add2[0].get_right(), out_vector.get_left(), MINT)
        loop = CubicBezier(
            out_vector.get_bottom() + DOWN * 0.15,
            out_vector.get_bottom() + DOWN * 1.9,
            start_vector.get_bottom() + DOWN * 1.9,
            start_vector.get_bottom() + DOWN * 0.5,
            color=CYAN,
            stroke_width=3,
        )
        loop_label = Text("× N Layer – in großen Modellen einige Dutzend", font_size=19, color=CYAN)
        loop_label.move_to(loop.point_from_proportion(0.5) + DOWN * 0.3)
        self.play(GrowArrow(out_arrow), FadeIn(out_vector), run_time=0.5)
        self.play(Create(loop), FadeIn(loop_label), run_time=0.9)
        self.step()

        final = Text("Nach dem letzten Layer wird der Vektor des letzten Tokens zu Logits.", font_size=21, color=INK)
        final.to_edge(DOWN, buff=0.25)
        self.play(FadeOut(weights_note), FadeIn(final), out_vector.animate.set_color(AMBER), run_time=0.7)
        self.step()


class NextToken(SteppedScene):
    """Logits become probabilities; temperature reshapes them; one token is picked."""

    slug = "next-token"

    TRACK = 5.6

    def make_bar(self, track: RoundedRectangle, color: str, value: float) -> RoundedRectangle:
        bar = RoundedRectangle(
            width=max(0.12, self.TRACK * value),
            height=0.4,
            corner_radius=0.12,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.9,
        )
        return bar.move_to(track.get_center()).align_to(track, LEFT)

    def construct(self):
        title = heading("Von Punktzahlen zur Auswahl", "SCHRITT 4 · LOGITS & PROBABILITIES")
        prompt = VGroup(
            Text(EXAMPLE_PROMPT, font_size=27, color=INK),
            Text("____", font_size=27, color=MINT),
        ).arrange(RIGHT, buff=0.2)
        prompt.move_to(UP * 2.6 + LEFT * 0.7)
        self.play(FadeIn(title), Write(prompt), run_time=0.9)

        words = [text.replace(" ", "␣") for text, _, _ in EXAMPLE_CANDIDATES]
        logits = [logit for _, _, logit in EXAMPLE_CANDIDATES]
        colors = [MINT, AMBER, CYAN, CORAL, MUTED]

        rows, tracks, pct_slots, pct_texts = VGroup(), [], [], []
        for word, logit, color in zip(words, logits, colors):
            label = Text(word, font_size=21, color=INK, font="DejaVu Sans Mono")
            label_slot = VGroup(RoundedRectangle(width=1.9, height=0.42, stroke_width=0, fill_opacity=0), label)
            score = Text(f"{logit:+.1f}", font_size=19, color=color, font="DejaVu Sans Mono")
            score_slot = VGroup(RoundedRectangle(width=1.0, height=0.42, stroke_width=0, fill_opacity=0), score)
            track = RoundedRectangle(width=self.TRACK, height=0.4, corner_radius=0.12, stroke_color=EDGE, fill_color=EDGE, fill_opacity=0.25)
            pct_slot = RoundedRectangle(width=1.1, height=0.42, stroke_width=0, fill_opacity=0)
            rows.add(VGroup(label_slot, score_slot, track, pct_slot).arrange(RIGHT, buff=0.3))
            tracks.append(track)
            pct_slots.append(pct_slot)
        rows.arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.75)

        caption = Text("Logits – eine Punktzahl je Token im Vokabular", font_size=17, color=MUTED)
        caption.next_to(rows, UP, buff=0.5).align_to(rows, LEFT)
        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.2) for row in rows], lag_ratio=0.12), run_time=1.0)
        self.play(FadeIn(caption), run_time=0.35)
        self.step()

        temperature = VGroup(
            Text("Temperatur", font_size=17, color=MUTED),
            Text("1.0", font_size=26, color=INK),
        ).arrange(DOWN, buff=0.1)
        temperature.to_edge(RIGHT, buff=0.8).shift(UP * 1.1)

        bars = [self.make_bar(track, color, 0.02) for track, color in zip(tracks, colors)]
        pct_texts = [
            Text("", font_size=19, color=color, font="DejaVu Sans Mono").move_to(slot)
            for slot, color in zip(pct_slots, colors)
        ]

        def distribute(temp: float, run_time: float = 1.0):
            probabilities = softmax(logits, temp)
            self.play(
                *[bar.animate.become(self.make_bar(track, color, p)) for bar, track, color, p in zip(bars, tracks, colors, probabilities)],
                *[
                    text.animate.become(
                        Text(f"{p:.0%}", font_size=19, color=color, font="DejaVu Sans Mono").move_to(slot)
                    )
                    for text, slot, color, p in zip(pct_texts, pct_slots, colors, probabilities)
                ],
                run_time=run_time,
                rate_func=smooth,
            )

        softmax_caption = Text("Softmax macht daraus Wahrscheinlichkeiten", font_size=17, color=MUTED).move_to(caption, LEFT)
        self.add(*bars, *pct_texts)
        self.play(FadeIn(temperature), FadeOut(caption), FadeIn(softmax_caption), run_time=0.5)
        distribute(1.0)
        self.step()

        def set_temperature(temp: float, hint: str | None, color: str):
            new_value = Text(f"{temp:.1f}", font_size=26, color=color).move_to(temperature[1])
            note = Text(hint, font_size=18, color=color) if hint else None
            animations = [temperature[1].animate.become(new_value)]
            if note:
                note.next_to(temperature, DOWN, buff=0.25)
                animations.append(FadeIn(note))
            self.play(*animations, run_time=0.4)
            distribute(temp, run_time=0.9)
            return note

        cold = set_temperature(0.4, "schärfer", CYAN)
        self.step()

        self.play(FadeOut(cold), run_time=0.25)
        hot = set_temperature(1.6, "flacher", CORAL)
        self.step()

        self.play(FadeOut(hot), run_time=0.25)
        set_temperature(1.0, None, INK)
        highlight = RoundedRectangle(
            width=rows[0].width + 0.4,
            height=0.75,
            corner_radius=0.14,
            stroke_color=MINT,
            stroke_width=2.5,
            fill_opacity=0,
        ).move_to(rows[0])
        picked = Text("gewählt", font_size=17, color=MINT).next_to(highlight, LEFT, buff=0.25)
        chosen = Text("Baum", font_size=27, color=MINT).move_to(prompt[1], aligned_edge=LEFT)
        self.play(Create(highlight), FadeIn(picked), run_time=0.5)
        self.play(FadeOut(prompt[1]), FadeIn(chosen, shift=UP * 0.15), run_time=0.6)
        note = Text("Das Modell liefert die Verteilung. Die Auswahl daraus ist eine eigene Entscheidung.", font_size=20, color=MUTED)
        note.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note), run_time=0.4)
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
    """Model calls and tool calls both pass through LiteLLM, but stay separate paths."""

    slug = "trust-boundary"

    def construct(self):
        title = heading("Zwei Pfade, ein Gateway", "AGENTIC OPS · ARCHITEKTUR")
        self.play(FadeIn(title), run_time=0.55)

        operator = pill("Operator", CYAN, width=2.4).move_to(np.array([-6.9, 0, 0]))
        opencode = pill("OpenCode", MINT, width=2.5).move_to(np.array([-3.6, 0, 0]))

        gateway_box = RoundedRectangle(width=2.9, height=2.5, corner_radius=0.2, stroke_color=AMBER, stroke_width=2, fill_color=PANEL, fill_opacity=0.95)
        gateway_text = VGroup(
            Text("LiteLLM", font_size=25, color=INK, weight="BOLD"),
            Text("Model-Proxy", font_size=17, color=MUTED),
            Text("MCP-Proxy", font_size=17, color=MUTED),
            Text("Access Control · Metering", font_size=14, color=AMBER),
        ).arrange(DOWN, buff=0.18)
        gateway = VGroup(gateway_box, gateway_text.move_to(gateway_box)).move_to(np.array([-0.6, 0, 0]))

        model = pill("Modell", PURPLE, width=2.4).move_to(np.array([2.9, 1.6, 0]))
        mcp = pill("OpenShift MCP", CORAL, width=3.0).move_to(np.array([2.9, -1.6, 0]))
        api = pill("OpenShift API", MINT, width=2.9).move_to(np.array([6.5, -1.6, 0]))

        nodes = VGroup(operator, opencode, gateway, model, mcp, api)
        self.play(LaggedStart(*[FadeIn(node, shift=RIGHT * 0.15) for node in nodes], lag_ratio=0.1), run_time=1.0)

        connections = VGroup(
            flow_arrow(operator.get_right(), opencode.get_left(), CYAN),
            flow_arrow(opencode.get_right(), gateway_box.get_left(), MINT),
            flow_arrow(gateway_box.get_right() + UP * 0.6, model.get_left(), PURPLE),
            flow_arrow(gateway_box.get_right() + DOWN * 0.6, mcp.get_left(), CORAL),
            flow_arrow(mcp.get_right(), api.get_left(), MINT),
        )
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in connections], lag_ratio=0.12), run_time=1.0)
        self.step()

        model_path = Text("Modellpfad · Routing · Budget", font_size=18, color=PURPLE).move_to(np.array([2.9, 2.6, 0]))
        tool_path = Text("Toolpfad · Tool-Schema · RBAC", font_size=18, color=CORAL).move_to(np.array([4.4, -2.6, 0]))
        self.play(FadeIn(model_path), FadeIn(tool_path), run_time=0.45)

        packets = VGroup(*[Dot(radius=0.08, color=color) for color in [CYAN, MINT, PURPLE, CORAL, MINT]])
        self.add(*packets)
        self.play(
            *[MoveAlongPath(packet, path, rate_func=linear) for packet, path in zip(packets, connections)],
            run_time=1.35,
        )
        self.remove(*packets)
        self.step()

        boundaries = VGroup()
        for x, label in [(-5.0, "Nutzer"), (-2.2, "Gateway"), (1.5, "Backend")]:
            line = Line(UP * 3.0, DOWN * 3.1, color=EDGE, stroke_width=2, stroke_opacity=0.8).move_to(RIGHT * x)
            caption = Text(label, font_size=15, color=MUTED).next_to(line, DOWN, buff=0.08)
            boundaries.add(VGroup(line, caption))
        self.play(LaggedStart(*[Create(boundary) for boundary in boundaries], lag_ratio=0.12), run_time=0.8)

        note = Text("Ein Weg nach draußen. Autorisiert wird trotzdem an jeder Grenze einzeln.", font_size=21, color=MUTED)
        note.to_edge(DOWN, buff=0.18)
        self.play(FadeIn(note), run_time=0.45)
        self.step()
