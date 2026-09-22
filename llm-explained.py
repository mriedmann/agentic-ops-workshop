from manim import *
import numpy as np

class IntroScene(Scene):
    def construct(self):
        # Dark blue tinted background rectangle
        bg = Rectangle(width=16, height=10, fill_color="#0a0a1a", fill_opacity=1, stroke_width=0)
        bg.set_z_index(-100)
        self.add(bg)

        # Corner decorations with breathing effect
        corner_lines = VGroup()
        circuit_dots = VGroup()  # For electric pulse effect
        for corner, angle in [(UL, 0), (UR, -PI/2), (DL, PI/2), (DR, PI)]:
            line1 = Line(ORIGIN, RIGHT * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            line2 = Line(ORIGIN, DOWN * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            corner_group = VGroup(line1, line2)
            corner_group.rotate(angle, about_point=ORIGIN)
            corner_group.move_to(corner * np.array([6.5, 3.5, 0]))
            corner_lines.add(corner_group)

            # Electric pulse dots for each corner
            pulse_dot1 = Dot(radius=0.04, color=BLUE_B).set_opacity(0.8)
            pulse_dot2 = Dot(radius=0.04, color=BLUE_B).set_opacity(0.8)
            circuit_dots.add(VGroup(pulse_dot1, pulse_dot2, line1.copy(), line2.copy()))

        self.play(Create(corner_lines), run_time=0.5)

        # Electric pulse animation along circuit lines
        pulse_anims = []
        for i, (corner_group, dot_group) in enumerate(zip(corner_lines, circuit_dots)):
            line1, line2 = corner_group[0], corner_group[1]
            pulse_dot1, pulse_dot2 = dot_group[0], dot_group[1]
            pulse_dot1.move_to(line1.get_start())
            pulse_dot2.move_to(line2.get_start())
            self.add(pulse_dot1, pulse_dot2)
            pulse_anims.append(MoveAlongPath(pulse_dot1, line1, rate_func=linear))
            pulse_anims.append(MoveAlongPath(pulse_dot2, line2, rate_func=linear))

        self.play(*pulse_anims, run_time=0.6)
        for dot_group in circuit_dots:
            self.remove(dot_group[0], dot_group[1])

        # Title
        title = Text("Large Language Models", font_size=56, color=BLUE)
        title.to_edge(UP, buff=0.5)

        # Add glow effect to title
        title_glow = title.copy()
        title_glow.set_color(BLUE)
        title_glow.set_opacity(0.3)
        title_glow.set_stroke(BLUE, width=8, opacity=0.2)

        subtitle = Text("How AI Understands Language", font_size=32, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)

        # Radial gradient background for brain
        gradient_circles = VGroup()
        for i in range(5):
            circle = Circle(radius=2.5 - i * 0.3, color=BLUE, fill_opacity=0.02 + i * 0.01, stroke_width=0)
            gradient_circles.add(circle)
        gradient_circles.move_to(DOWN * 0.5)

        # Soft glow behind brain
        brain_glow = Circle(radius=2, color=BLUE, fill_opacity=0.1, stroke_width=0)
        brain_glow.move_to(DOWN * 0.5)

        # Animated brain/network icon with dashed stroke
        brain_circle = Circle(radius=1.5, color=BLUE, fill_opacity=0.15, stroke_width=2)
        brain_circle.move_to(DOWN * 0.5)
        brain_circle.set_stroke(BLUE, width=2, opacity=0.8)

        # Create dashed circle overlay for animation effect
        dashed_brain = DashedVMobject(Circle(radius=1.5), num_dashes=30, dashed_ratio=0.5)
        dashed_brain.set_stroke(BLUE_C, width=1.5, opacity=0.6)
        dashed_brain.move_to(DOWN * 0.5)

        # Create neural network nodes inside
        nodes = VGroup()
        positions = [
            [-0.8, 0.6, 0], [0, 0.8, 0], [0.8, 0.6, 0],
            [-0.6, 0, 0], [0.6, 0, 0],
            [-0.8, -0.6, 0], [0, -0.8, 0], [0.8, -0.6, 0]
        ]
        for pos in positions:
            node = Dot(point=np.array(pos) + DOWN * 0.5, radius=0.12, color=YELLOW)
            nodes.add(node)

        # Create connections with fixed seed and distance-based opacity
        np.random.seed(42)
        connections = VGroup()
        connection_pairs = []
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                if i < j and np.random.random() > 0.4:
                    # Calculate distance for opacity
                    dist = np.linalg.norm(node1.get_center() - node2.get_center())
                    opacity = max(0.3, 0.8 - dist * 0.2)  # Closer = brighter
                    line = Line(node1.get_center(), node2.get_center(),
                               stroke_width=1.5, color=BLUE_C, stroke_opacity=opacity)
                    connections.add(line)
                    connection_pairs.append((node1, node2))

        brain_group = VGroup(brain_glow, brain_circle, dashed_brain, connections, nodes)

        # Circuit-like decorative lines in background
        circuit_lines = VGroup()
        circuit_positions = [
            (LEFT * 5 + UP * 1, RIGHT * 0.8, DOWN * 0.5),
            (LEFT * 5 + DOWN * 1.5, RIGHT * 1.2, UP * 0.3),
            (RIGHT * 4 + UP * 0.5, LEFT * 0.6, DOWN * 0.8),
            (RIGHT * 4.5 + DOWN * 2, LEFT * 1, UP * 0.4),
        ]
        for start, dir1, dir2 in circuit_positions:
            l1 = Line(start, start + dir1, stroke_width=1, color=BLUE_E, stroke_opacity=0.2)
            l2 = Line(start + dir1, start + dir1 + dir2, stroke_width=1, color=BLUE_E, stroke_opacity=0.2)
            dot = Dot(start + dir1 + dir2, radius=0.03, color=BLUE_E).set_opacity(0.3)
            circuit_lines.add(l1, l2, dot)

        # Shimmer effect for title
        shimmer = Rectangle(width=0.5, height=1.2, fill_color=WHITE, fill_opacity=0.15, stroke_width=0)
        shimmer.move_to(title.get_left() + LEFT * 1)
        shimmer.rotate(PI/6)

        # Animations
        self.play(Write(title), FadeIn(title_glow), run_time=1.5)

        # Shimmer across title
        self.play(
            shimmer.animate.move_to(title.get_right() + RIGHT * 1),
            run_time=0.8,
            rate_func=linear
        )
        self.remove(shimmer)

        # Subtitle with delay and fade from below
        self.wait(0.2)
        self.play(FadeIn(subtitle, shift=UP * 0.5), run_time=1)

        # Settling pause
        self.wait(0.25)

        self.play(FadeIn(gradient_circles), FadeIn(brain_glow), run_time=0.5)
        self.play(Create(brain_circle), Create(dashed_brain), Create(circuit_lines), run_time=1)
        self.play(Create(connections), run_time=1.5)
        self.play(LaggedStart(*[GrowFromCenter(node) for node in nodes], lag_ratio=0.1), run_time=1.5)

        # Rotate dashed circle
        self.play(Rotate(dashed_brain, angle=PI/6, about_point=dashed_brain.get_center()), run_time=1)

        # Traveling dots along connections for neural activity
        traveling_dots = VGroup()
        for i, line in enumerate(connections[:6]):
            dot = Dot(radius=0.05, color=YELLOW).move_to(line.get_start())
            traveling_dots.add(dot)

        # Node pulsing animation
        def pulse_nodes():
            anims = []
            for i, node in enumerate(nodes):
                anims.append(Succession(
                    Wait(i * 0.15),
                    node.animate.scale(1.3).set_color(WHITE),
                    node.animate.scale(1/1.3).set_color(YELLOW),
                ))
            return anims

        # Animate traveling dots
        travel_anims = []
        for i, (dot, line) in enumerate(zip(traveling_dots, connections[:6])):
            travel_anims.append(MoveAlongPath(dot, line, rate_func=linear))

        self.add(*traveling_dots)
        self.play(
            *travel_anims,
            *pulse_nodes(),
            run_time=2
        )
        self.remove(*traveling_dots)

        # Brief flash when all nodes finish pulsing
        flash_circle = Circle(radius=1.8, color=WHITE, stroke_width=3, fill_opacity=0)
        flash_circle.move_to(DOWN * 0.5)
        self.play(
            Create(flash_circle),
            flash_circle.animate.set_stroke(opacity=0).scale(1.3),
            run_time=0.4
        )
        self.remove(flash_circle)

        # Pulse animation
        self.play(
            brain_group.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=1
        )

        # Corner breathing effect
        self.play(
            corner_lines.animate.set_opacity(0.5),
            rate_func=there_and_back,
            run_time=0.8
        )

        self.wait(0.5)

        # Fade out with transition to black
        all_elements = VGroup(title, title_glow, subtitle, brain_group, gradient_circles, circuit_lines, corner_lines)
        self.play(FadeOut(all_elements), run_time=1)

        # Brief black pause for transition
        self.wait(0.3)


class TokenizationScene(Scene):
    def construct(self):
        # Dark blue background
        bg = Rectangle(width=16, height=10, fill_color="#0a0a1a", fill_opacity=1, stroke_width=0)
        bg.set_z_index(-100)
        self.add(bg)

        # Corner decorations
        corner_lines = VGroup()
        for corner, angle in [(UL, 0), (UR, -PI/2), (DL, PI/2), (DR, PI)]:
            line1 = Line(ORIGIN, RIGHT * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            line2 = Line(ORIGIN, DOWN * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            corner_group = VGroup(line1, line2)
            corner_group.rotate(angle, about_point=ORIGIN)
            corner_group.move_to(corner * np.array([6.5, 3.5, 0]))
            corner_lines.add(corner_group)

        self.play(FadeIn(corner_lines), run_time=0.3)

        # Title with glow
        title = Text("Step 1: Tokenization", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        title_glow = title.copy().set_opacity(0.3).set_stroke(BLUE, width=6, opacity=0.2)

        self.play(Write(title), FadeIn(title_glow), run_time=1)

        # Original sentence
        sentence = Text("The cat sat on the mat", font_size=36)
        sentence.move_to(UP * 1.8)

        self.play(Write(sentence), run_time=1.5)

        # Split/crack effect - vertical lines between words
        word_positions = ["The", "cat", "sat", "on", "the", "mat"]
        split_lines = VGroup()
        current_x = sentence.get_left()[0]

        for i, word in enumerate(word_positions[:-1]):
            # Approximate position after each word
            word_width = len(word) * 0.22  # Approximate character width
            current_x += word_width + 0.15
            split_line = Line(
                UP * 0.35, DOWN * 0.35,
                stroke_width=2, color=YELLOW, stroke_opacity=0.8
            )
            split_line.move_to(sentence.get_left() + RIGHT * (current_x - sentence.get_left()[0]) + UP * 1.8)
            split_lines.add(split_line)
            current_x += 0.2  # Space between words

        # Brief flash of split lines
        self.play(
            LaggedStart(*[Create(line) for line in split_lines], lag_ratio=0.08),
            run_time=0.5
        )
        self.play(
            *[line.animate.set_opacity(0) for line in split_lines],
            run_time=0.3
        )
        self.remove(split_lines)

        # Highlight sweep across sentence - more visible
        highlight_rect = Rectangle(width=0.3, height=0.7, fill_color=YELLOW, fill_opacity=0.4, stroke_width=0)
        highlight_rect.move_to(sentence.get_left() + LEFT * 0.2)

        self.play(FadeIn(highlight_rect), run_time=0.1)
        self.play(
            highlight_rect.animate.move_to(sentence.get_right() + RIGHT * 0.2),
            run_time=1,
            rate_func=linear
        )
        self.play(FadeOut(highlight_rect), run_time=0.1)

        # Break into tokens
        words = ["The", "cat", "sat", "on", "the", "mat"]
        colors = [RED, ORANGE, YELLOW, GREEN, TEAL, BLUE]

        tokens = VGroup()
        corner_accents = VGroup()
        for i, (word, color) in enumerate(zip(words, colors)):
            token_box = RoundedRectangle(
                width=1.3, height=0.8, corner_radius=0.1,
                fill_color=color, fill_opacity=0.2, stroke_color=color, stroke_width=2
            )
            token_text = Text(word, font_size=26)

            # Animated corner accent (larger, more visible)
            corner_accent = Dot(radius=0.06, color=color)
            corner_accent.set_opacity(0)  # Start invisible

            token_group = VGroup(token_box, token_text, corner_accent)
            tokens.add(token_group)
            corner_accents.add(corner_accent)

        tokens.arrange(RIGHT, buff=0.25)
        tokens.move_to(UP * 0.2)

        # Reposition corner accents after arrangement
        for token in tokens:
            token[2].move_to(token[0].get_corner(UR) + LEFT * 0.12 + DOWN * 0.12)

        # Centered "Tokenize" label above arrow
        arrow_label = Text("Tokenize", font_size=26, color=WHITE)
        arrow_label.move_to(UP * 1.1)

        # Arrow below label
        arrow = Arrow(UP * 0.9, UP * 0.6, buff=0, color=WHITE, stroke_width=3)
        arrow.next_to(arrow_label, DOWN, buff=0.15)

        self.play(FadeIn(arrow_label, shift=DOWN * 0.2), run_time=0.5)
        self.play(GrowArrow(arrow), run_time=0.5)

        # Token animation with corner accent glow
        token_anims = []
        accent_anims = []
        for i, (token, accent) in enumerate(zip(tokens, corner_accents)):
            token_anims.append(
                Succession(
                    Wait(i * 0.12),
                    GrowFromCenter(token),
                )
            )
            accent_anims.append(
                Succession(
                    Wait(i * 0.12 + 0.3),
                    accent.animate.set_opacity(1),
                    accent.animate.scale(1.5).set_opacity(0.5),
                    accent.animate.scale(1/1.5).set_opacity(0.7),
                )
            )

        self.play(*token_anims, run_time=1.5)
        self.play(*accent_anims, run_time=1)

        # Snappier bounce effect (1.08 instead of 1.1)
        bounce_anims = []
        for i, token in enumerate(tokens):
            bounce_anims.append(
                Succession(
                    Wait(i * 0.06),
                    token.animate.scale(1.08),
                    token.animate.scale(1/1.08),
                )
            )
        self.play(*bounce_anims, run_time=0.8)

        # Settling pause
        self.wait(0.25)

        # Show token IDs with connecting lines
        ids_title = Text("Token IDs:", font_size=26, color=GRAY)
        ids_title.move_to(DOWN * 1.2)

        token_ids = ["1045", "3287", "2068", "1012", "1045", "4562"]
        ids_group = VGroup()
        dashed_lines = VGroup()

        for i, (tid, token, color) in enumerate(zip(token_ids, tokens, colors)):
            id_text = Text(tid, font_size=22, color=color)
            id_text.move_to(token.get_center() + DOWN * 2)
            ids_group.add(id_text)

            # Dashed connecting line
            dashed_line = DashedLine(
                token.get_bottom() + DOWN * 0.1,
                id_text.get_top() + UP * 0.1,
                dash_length=0.1,
                stroke_width=1.5,
                color=color,
                stroke_opacity=0.5
            )
            dashed_lines.add(dashed_line)

        self.play(Write(ids_title), run_time=0.5)
        self.play(
            LaggedStart(*[Create(line) for line in dashed_lines], lag_ratio=0.1),
            run_time=1
        )

        # Token IDs with white flash highlight
        id_anims = []
        flash_anims = []
        for i, id_text in enumerate(ids_group):
            id_anims.append(
                Succession(
                    Wait(i * 0.1),
                    Write(id_text),
                )
            )

        self.play(*id_anims, run_time=1.5)

        # White flash on each ID
        for id_text in ids_group:
            flash_copy = id_text.copy().set_color(WHITE)
            self.play(
                FadeIn(flash_copy),
                FadeOut(flash_copy),
                run_time=0.15
            )

        # Settling pause
        self.wait(0.3)

        self.wait(1.2)
        all_elements = VGroup(title, title_glow, sentence, arrow, arrow_label, tokens, ids_title, ids_group, dashed_lines, corner_lines)
        self.play(FadeOut(all_elements), run_time=1)
        self.wait(0.3)


class EmbeddingScene(Scene):
    def construct(self):
        # Dark blue background
        bg = Rectangle(width=16, height=10, fill_color="#0a0a1a", fill_opacity=1, stroke_width=0)
        bg.set_z_index(-100)
        self.add(bg)

        # Corner decorations
        corner_lines = VGroup()
        for corner, angle in [(UL, 0), (UR, -PI/2), (DL, PI/2), (DR, PI)]:
            line1 = Line(ORIGIN, RIGHT * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            line2 = Line(ORIGIN, DOWN * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            corner_group = VGroup(line1, line2)
            corner_group.rotate(angle, about_point=ORIGIN)
            corner_group.move_to(corner * np.array([6.5, 3.5, 0]))
            corner_lines.add(corner_group)

        self.play(FadeIn(corner_lines), run_time=0.3)

        # Title
        title = Text("Step 2: Embeddings", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        title_glow = title.copy().set_opacity(0.3).set_stroke(BLUE, width=6, opacity=0.2)
        self.play(Write(title), FadeIn(title_glow), run_time=1)

        # Explanation
        explanation = Text("Words become vectors in high-dimensional space", font_size=26, color=GRAY)
        explanation.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(explanation), run_time=1)

        # LEFT SIDE: Embedding space visualization
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=4,
            tips=False,
            axis_config={"stroke_color": GRAY, "stroke_width": 1}
        )
        axes.move_to(LEFT * 3.2 + DOWN * 0.8)

        # Axis labels
        x_axis_label = Text("Semantic Dim 1", font_size=12, color=GRAY).set_opacity(0.6)
        x_axis_label.next_to(axes.x_axis, DOWN, buff=0.15)
        y_axis_label = Text("Semantic Dim 2", font_size=12, color=GRAY).set_opacity(0.6)
        y_axis_label.rotate(PI/2)
        y_axis_label.next_to(axes.y_axis, LEFT, buff=0.15)

        # Add subtle grid
        grid = VGroup()
        for x in range(-3, 4):
            line = Line(axes.c2p(x, -2.5), axes.c2p(x, 2.5), stroke_width=0.5, color=GRAY, stroke_opacity=0.15)
            grid.add(line)
        for y in range(-2, 3):
            line = Line(axes.c2p(-3, y), axes.c2p(3, y), stroke_width=0.5, color=GRAY, stroke_opacity=0.15)
            grid.add(line)

        # Word points with semantic categories
        word_points = {
            "cat": (1.5, 1.2, ORANGE),
            "dog": (1.8, 0.8, YELLOW),
            "king": (-1.5, 0.8, BLUE),
            "queen": (-1.2, 0.4, PURPLE),
            "car": (-0.3, -1.5, GREEN)
        }

        dots = VGroup()
        labels = VGroup()
        dot_data = []  # Store for floating animation
        sparkle_groups = VGroup()  # For sparkle effects

        for word_name, (x, y, color) in word_points.items():
            # Create glowing dot
            dot_glow = Dot(axes.c2p(x, y), color=color, radius=0.15).set_opacity(0.3)
            dot = Dot(axes.c2p(x, y), color=color, radius=0.1)
            label = Text(word_name, font_size=16, color=color)
            label.next_to(dot, UP, buff=0.1)

            dot_group = VGroup(dot_glow, dot)
            dots.add(dot_group)
            labels.add(label)
            dot_data.append((dot_group, label, x, y))

            # Create sparkle effect (3-4 small triangles)
            sparkles = VGroup()
            for angle in [0, PI/2, PI, 3*PI/2]:
                sparkle = Triangle().scale(0.05)
                sparkle.set_fill(color, opacity=0.8)
                sparkle.set_stroke(width=0)
                sparkle.rotate(angle)
                sparkle.move_to(dot.get_center())
                sparkles.add(sparkle)
            sparkle_groups.add(sparkles)

        # RIGHT SIDE: Word to vector transformation
        word = Text("cat", font_size=44, color=ORANGE)
        word.move_to(RIGHT * 2.5 + UP * 1.2)

        # Word box
        word_box = RoundedRectangle(width=1.5, height=0.9, corner_radius=0.1,
                                     stroke_color=ORANGE, fill_color=ORANGE, fill_opacity=0.1)
        word_box.move_to(word.get_center())

        arrow = Arrow(RIGHT * 2.5 + UP * 0.6, RIGHT * 2.5 + DOWN * 0.2, buff=0, color=WHITE, stroke_width=2)

        # Vector representation
        vector_text = MathTex(
            r"\begin{bmatrix} 0.23 \\ -0.45 \\ 0.78 \\ 0.12 \\ -0.89 \\ \vdots \end{bmatrix}",
            font_size=32
        )
        vector_text.move_to(RIGHT * 2.5 + DOWN * 1.5)

        # Dimension label - positioned to the RIGHT of the vector matrix (FIXED)
        dim_label = Text("768 dimensions", font_size=18, color=YELLOW)
        dim_label.next_to(vector_text, RIGHT, buff=0.3)

        # Bracket indicator on the right side
        bracket_left = Line(UP * 0.8, DOWN * 0.8, stroke_width=2, color=YELLOW)
        bracket_top = Line(ORIGIN, LEFT * 0.15, stroke_width=2, color=YELLOW)
        bracket_bottom = Line(ORIGIN, LEFT * 0.15, stroke_width=2, color=YELLOW)
        bracket_top.move_to(bracket_left.get_top(), RIGHT)
        bracket_bottom.move_to(bracket_left.get_bottom(), RIGHT)
        bracket = VGroup(bracket_left, bracket_top, bracket_bottom)
        bracket.next_to(vector_text, RIGHT, buff=0.08)
        dim_label.next_to(bracket, RIGHT, buff=0.15)

        # Animate left side (embedding space)
        self.play(Create(grid), Create(axes), run_time=1)
        self.play(FadeIn(x_axis_label), FadeIn(y_axis_label), run_time=0.5)

        # Dots with sparkle effect
        dot_anims = []
        for i, (dot, label, sparkles) in enumerate(zip(dots, labels, sparkle_groups)):
            dot_anims.append(
                Succession(
                    Wait(i * 0.2),
                    GrowFromCenter(dot),
                )
            )

        self.play(*dot_anims, run_time=1.5)

        # Sparkle animation - radiate outward and fade
        for sparkles, dot in zip(sparkle_groups, dots):
            for sparkle in sparkles:
                sparkle.move_to(dot[1].get_center())
            self.add(sparkles)

        sparkle_anims = []
        for sparkles in sparkle_groups:
            for j, sparkle in enumerate(sparkles):
                direction = [RIGHT, UP, LEFT, DOWN][j]
                sparkle_anims.append(
                    sparkle.animate.shift(direction * 0.3).set_opacity(0)
                )

        self.play(*sparkle_anims, run_time=0.5)
        for sparkles in sparkle_groups:
            self.remove(sparkles)

        self.play(
            LaggedStart(*[FadeIn(label) for label in labels], lag_ratio=0.15),
            run_time=1
        )

        # Settling pause
        self.wait(0.25)

        # Animate right side (word to vector)
        self.play(FadeIn(word_box), Write(word), run_time=0.8)
        self.play(GrowArrow(arrow), run_time=0.5)
        self.play(Write(vector_text), run_time=1.2)
        self.play(FadeIn(dim_label), Create(bracket), run_time=0.8)

        # Floating animation for dots - using updaters with sine waves
        time_tracker = ValueTracker(0)

        original_positions = []
        for dot_group, label, x, y in dot_data:
            original_positions.append((axes.c2p(x, y), dot_group, label))

        # Show similarity with measurement line and pulsing connection
        similarity_text = Text("Similar words cluster together!", font_size=22, color=GREEN)
        similarity_text.move_to(DOWN * 2.8)  # Moved lower to avoid overlap

        # Animated connection line between cat and dog
        cat_pos = axes.c2p(1.5, 1.2)
        dog_pos = axes.c2p(1.8, 0.8)

        # Measurement line with distance indicator
        connection_line = Line(cat_pos, dog_pos, color=GREEN, stroke_width=3)

        # Small perpendicular ticks at ends of measurement line
        tick_length = 0.1
        direction = (dog_pos - cat_pos) / np.linalg.norm(dog_pos - cat_pos)
        perp = np.array([-direction[1], direction[0], 0])

        tick1 = Line(cat_pos - perp * tick_length, cat_pos + perp * tick_length, color=GREEN, stroke_width=2)
        tick2 = Line(dog_pos - perp * tick_length, dog_pos + perp * tick_length, color=GREEN, stroke_width=2)
        measurement_group = VGroup(connection_line, tick1, tick2)

        # Circle around animals with breathing animation
        animal_circle = Circle(radius=0.7, color=GREEN, stroke_width=2)
        animal_circle.move_to(axes.c2p(1.65, 1))

        # Circle around royalty with breathing animation
        royalty_circle = Circle(radius=0.6, color=PURPLE, stroke_width=2, stroke_opacity=0.7)
        royalty_circle.move_to(axes.c2p(-1.35, 0.6))

        self.play(
            Write(similarity_text),
            Create(measurement_group),
            Create(animal_circle),
            Create(royalty_circle),
            run_time=1.5
        )

        # Synchronized pulse for cat and dog dots when similarity appears
        cat_dot = dots[0]
        dog_dot = dots[1]
        self.play(
            cat_dot.animate.scale(1.4),
            dog_dot.animate.scale(1.4),
            connection_line.animate.set_stroke(width=5),
            rate_func=there_and_back,
            run_time=0.8
        )

        # Category labels
        animal_label = Text("Animals", font_size=14, color=GREEN)
        animal_label.next_to(animal_circle, DOWN, buff=0.1)
        royalty_label = Text("Royalty", font_size=14, color=PURPLE)
        royalty_label.next_to(royalty_circle, DOWN, buff=0.1)

        self.play(FadeIn(animal_label), FadeIn(royalty_label), run_time=0.5)

        # Breathing animation for category circles
        self.play(
            animal_circle.animate.scale(1.03),
            royalty_circle.animate.scale(1.03),
            rate_func=there_and_back,
            run_time=1.5
        )

        # Brief floating animation with circle breathing
        self.play(
            time_tracker.animate.set_value(2),
            animal_circle.animate.scale(1.02),
            royalty_circle.animate.scale(1.02),
            rate_func=there_and_back,
            run_time=1.5
        )

        self.wait(0.8)
        all_elements = VGroup(title, title_glow, explanation, word, word_box, arrow, vector_text,
                             dim_label, bracket, axes, grid, dots, labels, similarity_text,
                             measurement_group, animal_circle, royalty_circle, animal_label, royalty_label,
                             corner_lines, x_axis_label, y_axis_label)
        self.play(FadeOut(all_elements), run_time=1)
        self.wait(0.3)


class AttentionScene(Scene):
    def construct(self):
        # Dark blue background
        bg = Rectangle(width=16, height=10, fill_color="#0a0a1a", fill_opacity=1, stroke_width=0)
        bg.set_z_index(-100)
        self.add(bg)

        # Corner decorations
        corner_lines = VGroup()
        for corner, angle in [(UL, 0), (UR, -PI/2), (DL, PI/2), (DR, PI)]:
            line1 = Line(ORIGIN, RIGHT * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            line2 = Line(ORIGIN, DOWN * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            corner_group = VGroup(line1, line2)
            corner_group.rotate(angle, about_point=ORIGIN)
            corner_group.move_to(corner * np.array([6.5, 3.5, 0]))
            corner_lines.add(corner_group)

        self.play(FadeIn(corner_lines), run_time=0.3)

        # Title
        title = Text("Step 3: Self-Attention", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        title_glow = title.copy().set_opacity(0.3).set_stroke(BLUE, width=6, opacity=0.2)
        self.play(Write(title), FadeIn(title_glow), run_time=1)

        subtitle = Text("How words relate to each other", font_size=26, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=0.5)

        # Sentence with attention visualization
        words = ["The", "cat", "sat", "on", "the", "mat"]
        attention_weights = [0.1, 1.0, 0.3, 0.15, 0.05, 0.4]
        word_objects = VGroup()
        word_boxes = VGroup()
        underlines = VGroup()

        # Colors based on attention weight for each word
        arc_colors = [RED_C, YELLOW, ORANGE, TEAL, GRAY, BLUE_C]

        for i, word in enumerate(words):
            word_text = Text(word, font_size=32)

            # Attention heatmap effect - fill opacity based on weight
            fill_opacity = attention_weights[i] * 0.3
            word_box = RoundedRectangle(width=1, height=0.7, corner_radius=0.08,
                                        stroke_color=GRAY, stroke_width=1,
                                        fill_color=arc_colors[i], fill_opacity=fill_opacity)
            word_box.move_to(word_text.get_center())

            # Colored underline matching attention arc color
            underline = Line(LEFT * 0.4, RIGHT * 0.4, stroke_width=2, color=arc_colors[i], stroke_opacity=0.7)

            word_objects.add(word_text)
            word_boxes.add(word_box)
            underlines.add(underline)

        word_objects.arrange(RIGHT, buff=0.7)
        word_objects.move_to(DOWN * 0.3)

        # Reposition boxes and underlines
        for word_text, word_box, underline in zip(word_objects, word_boxes, underlines):
            word_box.move_to(word_text.get_center())
            underline.next_to(word_text, DOWN, buff=0.05)

        self.play(
            Write(word_objects),
            *[Create(box) for box in word_boxes],
            *[Create(underline) for underline in underlines],
            run_time=1.5
        )

        # Settling pause
        self.wait(0.25)

        # Highlight "cat" with ripple ring effect
        cat_index = 1

        # Ripple ring effect
        ripple = Circle(radius=0.4, color=YELLOW, stroke_width=2)
        ripple.move_to(word_objects[cat_index].get_center())

        self.play(Create(ripple), run_time=0.3)
        self.play(
            ripple.animate.scale(1.8).set_stroke(opacity=0),
            run_time=0.5
        )
        self.remove(ripple)

        cat_glow = word_boxes[cat_index].copy()
        cat_glow.set_stroke(YELLOW, width=4, opacity=0.5)
        cat_glow.set_fill(YELLOW, opacity=0.2)

        word_objects[cat_index].set_color(YELLOW)
        word_boxes[cat_index].set_stroke(YELLOW, width=2)

        self.play(FadeIn(cat_glow), run_time=0.3)

        # Create curved arcs ABOVE the words with gradient effect
        attention_arcs = VGroup()
        weight_labels = VGroup()
        arc_glows = VGroup()

        cat_pos = word_objects[cat_index].get_top() + UP * 0.15

        for i, (word_obj, weight) in enumerate(zip(word_objects, attention_weights)):
            if i != cat_index:
                target_pos = word_obj.get_top() + UP * 0.15

                # Calculate arc height based on distance
                distance = abs(i - cat_index)
                arc_height = 0.4 + distance * 0.25

                # Create arc using CubicBezier for smooth curve
                # Use gradient coloring - darker at source, brighter at target
                arc_color = interpolate_color(BLUE_C, RED, weight)
                arc = CubicBezier(
                    cat_pos,
                    cat_pos + UP * arc_height * 0.7,
                    target_pos + UP * arc_height * 0.7,
                    target_pos,
                    stroke_width=weight * 6 + 1,
                    color=arc_color,
                    stroke_opacity=0.6 + weight * 0.4
                )

                # Glow for high attention arcs
                if weight > 0.3:
                    arc_glow = arc.copy()
                    arc_glow.set_stroke(width=weight * 10, opacity=0.2)
                    arc_glows.add(arc_glow)

                    # Glow border pulse on high attention word boxes
                    box_glow = word_boxes[i].copy()
                    box_glow.set_stroke(arc_color, width=3, opacity=0.5)
                    arc_glows.add(box_glow)

                attention_arcs.add(arc)

                # Weight label at peak of arc
                mid_x = (cat_pos[0] + target_pos[0]) / 2
                label_pos = np.array([mid_x, cat_pos[1] + arc_height + 0.15, 0])
                weight_label = Text(f"{weight:.2f}", font_size=14, color=WHITE)
                weight_label.move_to(label_pos)
                weight_labels.add(weight_label)

        # Pulsing animation for cat
        self.play(
            word_objects[cat_index].animate.scale(1.2),
            run_time=0.5
        )

        # Animate arcs with traveling dots
        self.play(
            *[FadeIn(glow) for glow in arc_glows],
            run_time=0.3
        )

        self.play(
            LaggedStart(*[Create(arc) for arc in attention_arcs], lag_ratio=0.15),
            run_time=2
        )

        self.play(
            LaggedStart(*[FadeIn(label, scale=0.5) for label in weight_labels], lag_ratio=0.1),
            run_time=1
        )

        # Traveling dots along arcs
        traveling_dots = VGroup()
        for arc in attention_arcs[:3]:  # Just do first 3 for clarity
            dot = Dot(radius=0.05, color=YELLOW)
            traveling_dots.add(dot)

        travel_anims = []
        for dot, arc in zip(traveling_dots, attention_arcs[:3]):
            travel_anims.append(MoveAlongPath(dot, arc, rate_func=linear))

        self.add(*traveling_dots)
        self.play(*travel_anims, run_time=1.5)
        self.remove(*traveling_dots)

        # Explanation box with scale-up animation
        explanation_box = RoundedRectangle(
            width=6.5, height=1.3, corner_radius=0.2,
            fill_color="#1a1a3a", fill_opacity=0.8, stroke_color=BLUE, stroke_width=2
        )
        explanation_box.move_to(DOWN * 2.5)
        explanation_box.scale(0.9)

        explanation_text = Text(
            '"cat" attends to context words\nHigher weights = stronger relationships',
            font_size=22, color=WHITE, line_spacing=1.3
        )
        explanation_text.move_to(DOWN * 2.5)
        explanation_text.scale(0.9)

        self.play(
            explanation_box.animate.scale(1/0.9),
            explanation_text.animate.scale(1/0.9),
            Write(explanation_text),
            run_time=1
        )

        # Pulse the cat glow
        self.play(
            cat_glow.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=0.8
        )

        self.wait(2)
        all_elements = VGroup(title, title_glow, subtitle, word_objects, word_boxes,
                             attention_arcs, weight_labels, explanation_box, explanation_text,
                             cat_glow, arc_glows, underlines, corner_lines)
        self.play(FadeOut(all_elements), run_time=1)
        self.wait(0.3)


class TransformerArchitectureScene(Scene):
    def construct(self):
        # Dark blue background
        bg = Rectangle(width=16, height=10, fill_color="#0a0a1a", fill_opacity=1, stroke_width=0)
        bg.set_z_index(-100)
        self.add(bg)

        # Corner decorations
        corner_lines = VGroup()
        for corner, angle in [(UL, 0), (UR, -PI/2), (DL, PI/2), (DR, PI)]:
            line1 = Line(ORIGIN, RIGHT * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            line2 = Line(ORIGIN, DOWN * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            corner_group = VGroup(line1, line2)
            corner_group.rotate(angle, about_point=ORIGIN)
            corner_group.move_to(corner * np.array([6.5, 3.5, 0]))
            corner_lines.add(corner_group)

        self.play(FadeIn(corner_lines), run_time=0.3)

        # Title
        title = Text("The Transformer Architecture", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        title_glow = title.copy().set_opacity(0.3).set_stroke(BLUE, width=6, opacity=0.2)
        self.play(Write(title), FadeIn(title_glow), run_time=1)

        # Create transformer block with gradient
        def create_block(label, color, width=2.8, height=0.55):
            rect = RoundedRectangle(
                width=width, height=height, corner_radius=0.1,
                stroke_color=color, stroke_width=2
            )
            rect.set_fill(color, opacity=0.3)
            inner_rect = RoundedRectangle(
                width=width-0.1, height=height-0.1, corner_radius=0.08,
            )
            inner_rect.set_fill(color, opacity=0.1)
            inner_rect.move_to(rect.get_center())

            text = Text(label, font_size=17, color=WHITE)

            # Simple icon based on block type
            icon = None
            if "Attention" in label:
                icon = VGroup(
                    Circle(radius=0.12, stroke_width=1.5, color=WHITE),
                    Dot(radius=0.05, color=WHITE)
                )
            elif "Feed" in label:
                icon = Arrow(LEFT * 0.15, RIGHT * 0.15, stroke_width=2, color=WHITE,
                           max_tip_length_to_length_ratio=0.5)
            elif "Norm" in label:
                icon = VGroup(
                    Line(LEFT * 0.1, RIGHT * 0.1, stroke_width=1.5, color=WHITE),
                    Line(LEFT * 0.1 + DOWN * 0.08, RIGHT * 0.1 + DOWN * 0.08, stroke_width=1.5, color=WHITE),
                )

            if icon:
                icon.scale(0.8)
                icon.next_to(text, LEFT, buff=0.15)
                return VGroup(rect, inner_rect, icon, text)
            return VGroup(rect, inner_rect, text)

        # Build the architecture
        input_block = create_block("Input Embeddings", GREEN, width=3)

        # Input label with chevron
        input_label = Text("Tokens", font_size=14, color=GREEN)
        input_chevron = VGroup(
            Line(LEFT * 0.1 + UP * 0.08, ORIGIN, stroke_width=2, color=GREEN),
            Line(ORIGIN, RIGHT * 0.1 + UP * 0.08, stroke_width=2, color=GREEN)
        )

        # Transformer layers
        attention_block = create_block("Self-Attention", BLUE)
        norm1_block = create_block("Layer Norm", GRAY_B)
        ffn_block = create_block("Feed Forward", ORANGE)
        norm2_block = create_block("Layer Norm", GRAY_B)

        # Stack them
        transformer_stack = VGroup(attention_block, norm1_block, ffn_block, norm2_block)
        transformer_stack.arrange(UP, buff=0.12)

        # Surrounding box for transformer layer
        layer_box = RoundedRectangle(
            width=3.5, height=3,
            corner_radius=0.15,
            stroke_color=YELLOW, stroke_width=2,
            fill_color=YELLOW, fill_opacity=0.03
        )

        output_block = create_block("Output Probabilities", PURPLE, width=3)

        # Output label with chevron
        output_label = Text("Logits", font_size=14, color=PURPLE)
        output_chevron = VGroup(
            Line(LEFT * 0.1 + DOWN * 0.08, ORIGIN, stroke_width=2, color=PURPLE),
            Line(ORIGIN, RIGHT * 0.1 + DOWN * 0.08, stroke_width=2, color=PURPLE)
        )

        # Position everything
        input_block.move_to(DOWN * 2.8)
        input_label.next_to(input_block, DOWN, buff=0.1)
        input_chevron.next_to(input_label, DOWN, buff=0.05)
        layer_box.move_to(DOWN * 0.2)
        transformer_stack.move_to(layer_box.get_center())
        output_block.move_to(UP * 2.2)
        output_label.next_to(output_block, UP, buff=0.1)
        output_chevron.next_to(output_label, UP, buff=0.05)

        # Skip connections with plus symbols - MORE VISIBLE
        skip_connection_1 = VGroup()
        skip_left_1 = ArcBetweenPoints(
            attention_block.get_left() + LEFT * 0.15 + DOWN * 0.2,
            norm1_block.get_left() + LEFT * 0.15 + UP * 0.1,
            angle=PI/4,
            stroke_width=2.5,
            color=TEAL,
            stroke_opacity=0.9
        )
        # Plus symbol for skip connection merge
        plus_1 = Text("+", font_size=18, color=TEAL)
        plus_1.move_to(norm1_block.get_left() + LEFT * 0.35)
        skip_connection_1.add(skip_left_1, plus_1)

        # Skip around FFN
        skip_left_2 = ArcBetweenPoints(
            ffn_block.get_left() + LEFT * 0.15 + DOWN * 0.2,
            norm2_block.get_left() + LEFT * 0.15 + UP * 0.1,
            angle=PI/4,
            stroke_width=2.5,
            color=TEAL,
            stroke_opacity=0.9
        )
        plus_2 = Text("+", font_size=18, color=TEAL)
        plus_2.move_to(norm2_block.get_left() + LEFT * 0.35)
        skip_connection_2 = VGroup(skip_left_2, plus_2)

        # Skip connection label
        skip_label = Text("Residual\nConnections", font_size=12, color=TEAL, line_spacing=0.8)
        skip_label.next_to(layer_box, LEFT, buff=0.4)

        # Layer label
        layer_label = Text("Ã— N Layers", font_size=20, color=YELLOW)
        layer_label.next_to(layer_box, RIGHT, buff=0.25)

        # Arrows with flow indicators
        arrow1 = Arrow(input_block.get_top(), layer_box.get_bottom(), buff=0.1,
                      color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        arrow2 = Arrow(layer_box.get_top(), output_block.get_bottom(), buff=0.1,
                      color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.1)

        # Animate
        self.play(FadeIn(input_block, shift=UP), FadeIn(input_label), Create(input_chevron), run_time=0.8)
        self.play(GrowArrow(arrow1), run_time=0.5)
        self.play(Create(layer_box), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(block, shift=UP) for block in transformer_stack], lag_ratio=0.2),
            run_time=1.5
        )

        # Settling pause
        self.wait(0.25)

        # Show skip connections with labels
        self.play(
            Create(skip_connection_1),
            Create(skip_connection_2),
            FadeIn(skip_label),
            run_time=1
        )

        # Layer duplication effect - hold longer
        layer_copies = VGroup()
        for i in range(2):
            copy = layer_box.copy()
            copy.set_stroke(YELLOW, opacity=0.3 - i * 0.1)
            copy.shift(RIGHT * 0.15 * (i + 1) + UP * 0.1 * (i + 1))
            layer_copies.add(copy)

        self.play(
            *[FadeIn(copy) for copy in layer_copies],
            Write(layer_label),
            run_time=0.8
        )

        # Hold the stacked layers visible longer
        self.wait(0.5)

        self.play(
            *[FadeOut(copy) for copy in layer_copies],
            run_time=0.5
        )

        self.play(GrowArrow(arrow2), run_time=0.5)
        self.play(FadeIn(output_block, shift=UP), FadeIn(output_label), Create(output_chevron), run_time=0.8)

        # Data flow animation with block pulsing
        data_dot = Dot(color=YELLOW, radius=0.12)
        data_dot.move_to(input_block.get_center())

        # Trail effect
        trail = TracedPath(data_dot.get_center, stroke_color=YELLOW, stroke_width=2, stroke_opacity=0.5)

        self.play(GrowFromCenter(data_dot), run_time=0.3)
        self.add(trail)

        # Path through architecture with block pulses
        blocks_to_pulse = [input_block, attention_block, norm1_block, ffn_block, norm2_block, output_block]

        # Move to input top
        self.play(data_dot.animate.move_to(input_block.get_top()), run_time=0.3)
        self.play(input_block[0].animate.set_stroke(width=4), rate_func=there_and_back, run_time=0.3)

        # Move into layer box
        self.play(data_dot.animate.move_to(layer_box.get_bottom() + UP * 0.2), run_time=0.3)

        # Through each transformer block with pulse
        for block in [attention_block, norm1_block, ffn_block, norm2_block]:
            self.play(data_dot.animate.move_to(block.get_center()), run_time=0.4)
            self.play(block[0].animate.set_stroke(width=4), rate_func=there_and_back, run_time=0.25)

        # Exit layer box
        self.play(data_dot.animate.move_to(layer_box.get_top() + UP * 0.1), run_time=0.3)

        # To output
        self.play(data_dot.animate.move_to(output_block.get_center()), run_time=0.4)

        # Completion checkmark at output
        checkmark = VGroup(
            Line(ORIGIN, RIGHT * 0.1 + DOWN * 0.1, stroke_width=3, color=GREEN),
            Line(RIGHT * 0.1 + DOWN * 0.1, RIGHT * 0.25 + UP * 0.15, stroke_width=3, color=GREEN)
        )
        checkmark.next_to(output_block, RIGHT, buff=0.2)

        self.play(
            output_block[0].animate.set_stroke(width=4),
            Create(checkmark),
            rate_func=there_and_back,
            run_time=0.5
        )

        # Pulse at output
        self.play(
            data_dot.animate.scale(1.5),
            rate_func=there_and_back,
            run_time=0.5
        )

        self.play(FadeOut(data_dot), FadeOut(trail), FadeOut(checkmark), run_time=0.3)

        self.wait(1)
        all_elements = VGroup(title, title_glow, input_block, input_label, input_chevron, layer_box, transformer_stack,
                             layer_label, output_block, output_label, output_chevron, arrow1, arrow2, skip_connection_1,
                             skip_connection_2, skip_label, corner_lines)
        self.play(FadeOut(all_elements), run_time=1)
        self.wait(0.3)


class GenerationScene(Scene):
    def construct(self):
        # Dark blue background
        bg = Rectangle(width=16, height=10, fill_color="#0a0a1a", fill_opacity=1, stroke_width=0)
        bg.set_z_index(-100)
        self.add(bg)

        # Corner decorations
        corner_lines = VGroup()
        for corner, angle in [(UL, 0), (UR, -PI/2), (DL, PI/2), (DR, PI)]:
            line1 = Line(ORIGIN, RIGHT * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            line2 = Line(ORIGIN, DOWN * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            corner_group = VGroup(line1, line2)
            corner_group.rotate(angle, about_point=ORIGIN)
            corner_group.move_to(corner * np.array([6.5, 3.5, 0]))
            corner_lines.add(corner_group)

        self.play(FadeIn(corner_lines), run_time=0.3)

        # Title
        title = Text("Text Generation", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        title_glow = title.copy().set_opacity(0.3).set_stroke(BLUE, width=6, opacity=0.2)
        self.play(Write(title), FadeIn(title_glow), run_time=1)

        subtitle = Text("Predicting the next token", font_size=26, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=0.5)

        # LEFT SIDE: Input and output text
        prompt_label = Text("Input:", font_size=22, color=GRAY)
        prompt_label.move_to(LEFT * 4.5 + UP * 1.5)
        prompt_label.align_to(LEFT * 5, LEFT)

        prompt_text = Text("The weather today is", font_size=26)
        prompt_text.next_to(prompt_label, DOWN, buff=0.3)
        prompt_text.align_to(prompt_label, LEFT)

        # Blinking cursor
        cursor = Rectangle(width=0.1, height=0.4, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        cursor.next_to(prompt_text, RIGHT, buff=0.08)

        self.play(Write(prompt_label), Write(prompt_text), run_time=1)

        # Cursor blink animation
        self.play(FadeIn(cursor), run_time=0.1)
        for _ in range(3):
            self.play(cursor.animate.set_opacity(0), run_time=0.3)
            self.play(cursor.animate.set_opacity(1), run_time=0.3)

        # RIGHT SIDE: Probability distribution
        prob_title = Text("Next Word Probabilities:", font_size=20, color=GRAY)
        prob_title.move_to(RIGHT * 2.5 + UP * 1.5)

        next_words = ["sunny", "rainy", "cold", "nice", "bad"]
        probabilities = [0.35, 0.25, 0.18, 0.15, 0.07]
        colors = [YELLOW, BLUE, TEAL, GREEN, RED]

        bars = VGroup()
        labels = VGroup()
        prob_labels = VGroup()
        fill_lines = VGroup()  # For sweep effect

        bar_origin = RIGHT * 1 + UP * 0.8

        for i, (word, prob, color) in enumerate(zip(next_words, probabilities, colors)):
            bar = RoundedRectangle(
                width=prob * 6, height=0.4,
                corner_radius=0.05,
                fill_color=color, fill_opacity=0.7,
                stroke_color=color, stroke_width=1
            )
            bar.move_to(bar_origin + DOWN * (i * 0.55))
            bar.align_to(bar_origin, LEFT)

            # Fill lines for sweep effect
            fill_line = Line(
                bar.get_left() + LEFT * 0.1,
                bar.get_left() + LEFT * 0.1,
                stroke_width=bar.height * 20,
                color=WHITE,
                stroke_opacity=0.3
            )
            fill_lines.add(fill_line)

            word_label = Text(word, font_size=18)
            word_label.next_to(bar, LEFT, buff=0.2)

            prob_label = Text(f"{prob:.0%}", font_size=16, color=color)
            prob_label.next_to(bar, RIGHT, buff=0.15)

            bars.add(bar)
            labels.add(word_label)
            prob_labels.add(prob_label)

        # Thinking animation (pulsing dots with glow)
        thinking_dots = VGroup()
        for i in range(3):
            dot_glow = Dot(radius=0.1, color=GRAY).set_opacity(0.3)
            dot = Dot(radius=0.06, color=GRAY)
            thinking_dots.add(VGroup(dot_glow, dot))
        thinking_dots.arrange(RIGHT, buff=0.15)
        thinking_dots.next_to(cursor, RIGHT, buff=0.3)

        self.play(FadeIn(prob_title), run_time=0.5)

        # Show thinking dots with pulse
        self.play(FadeIn(thinking_dots), run_time=0.2)
        for _ in range(2):
            for dot_group in thinking_dots:
                self.play(
                    dot_group.animate.shift(UP * 0.1).scale(1.2),
                    run_time=0.1
                )
                self.play(
                    dot_group.animate.shift(DOWN * 0.1).scale(1/1.2),
                    run_time=0.1
                )
        self.play(FadeOut(thinking_dots), run_time=0.2)

        # Animate bars with fill sweep effect
        bar_anims = []
        for i, (bar, fill_line) in enumerate(zip(bars, fill_lines)):
            target_width = bar.width
            bar.stretch_to_fit_width(0.01)
            bar.align_to(bar_origin, LEFT)
            bar_anims.append(bar.animate.stretch_to_fit_width(target_width).align_to(bar_origin, LEFT))

        self.play(
            LaggedStart(*bar_anims, lag_ratio=0.12),
            LaggedStart(*[FadeIn(label) for label in labels], lag_ratio=0.12),
            LaggedStart(*[FadeIn(prob) for prob in prob_labels], lag_ratio=0.12),
            run_time=1.8
        )

        # Settling pause
        self.wait(0.25)

        # Flash and highlight selection with star indicator
        star = VGroup()
        for angle in range(0, 360, 72):
            ray = Line(ORIGIN, RIGHT * 0.12, stroke_width=2, color=YELLOW)
            ray.rotate(angle * DEGREES, about_point=ORIGIN)
            star.add(ray)
        star.next_to(bars[0], LEFT, buff=0.05)

        self.play(
            bars[0].animate.set_fill(opacity=1),
            GrowFromCenter(star),
            rate_func=there_and_back,
            run_time=0.4
        )

        selection_box = SurroundingRectangle(VGroup(bars[0], labels[0]), color=WHITE, buff=0.08, stroke_width=2)
        self.play(Create(selection_box), run_time=0.4)

        # Show generated word
        self.play(FadeOut(cursor), run_time=0.1)

        generated = Text(" sunny", font_size=26, color=YELLOW)
        generated.next_to(prompt_text, RIGHT, buff=0.05)

        # Curved arrow from bar to generated text
        selection_arrow = CurvedArrow(
            bars[0].get_left() + LEFT * 0.3,
            generated.get_right() + RIGHT * 0.1,
            angle=-PI/3,
            color=YELLOW,
            stroke_width=2
        )

        self.play(
            Create(selection_arrow),
            TransformFromCopy(labels[0], generated),
            run_time=0.8
        )

        # Highlight flash traveling across generated word
        word_flash = Rectangle(width=0.15, height=0.5, fill_color=WHITE, fill_opacity=0.5, stroke_width=0)
        word_flash.move_to(generated.get_left())
        self.play(
            word_flash.animate.move_to(generated.get_right()),
            run_time=0.3,
            rate_func=linear
        )
        self.remove(word_flash)

        # Fade out probability bars
        self.play(
            FadeOut(VGroup(bars, labels, prob_labels, selection_box, prob_title, selection_arrow, star)),
            run_time=0.5
        )

        # Continue generation with processing indicator
        current_group = VGroup(prompt_text, generated)

        more_words = [" and", " perfect", " for", " a", " walk"]
        cursor.next_to(generated, RIGHT, buff=0.05)

        for word in more_words:
            # Processing indicator (spinning dots)
            processing = VGroup()
            for i in range(3):
                proc_dot = Dot(radius=0.04, color=GREEN).set_opacity(0.5 + i * 0.15)
                processing.add(proc_dot)
            processing.arrange(RIGHT, buff=0.1)
            processing.next_to(current_group, RIGHT, buff=0.15)

            # Brief cursor blink
            self.play(FadeIn(cursor), run_time=0.1)
            self.play(FadeIn(processing), run_time=0.1)

            # Pulse processing dots
            self.play(
                *[dot.animate.scale(1.3) for dot in processing],
                rate_func=there_and_back,
                run_time=0.2
            )

            self.play(FadeOut(cursor), FadeOut(processing), run_time=0.1)

            new_word = Text(word, font_size=26, color=GREEN)
            new_word.next_to(current_group, RIGHT, buff=0)

            self.play(
                FadeIn(new_word, shift=LEFT * 0.15),
                new_word.animate.scale(1.05).scale(1/1.05),
                run_time=0.35
            )

            # Quick highlight flash on new word
            flash = Rectangle(width=0.1, height=0.5, fill_color=WHITE, fill_opacity=0.4, stroke_width=0)
            flash.move_to(new_word.get_left())
            self.add(flash)
            self.play(
                flash.animate.move_to(new_word.get_right()),
                run_time=0.15,
                rate_func=linear
            )
            self.remove(flash)

            current_group.add(new_word)
            cursor.next_to(new_word, RIGHT, buff=0.05)

        # Final result emphasis
        final_box = SurroundingRectangle(current_group, color=GREEN, buff=0.15, corner_radius=0.1)
        self.play(Create(final_box), run_time=0.5)

        self.wait(2)
        all_elements = VGroup(title, title_glow, subtitle, prompt_label, current_group,
                             final_box, corner_lines)
        self.play(FadeOut(all_elements), run_time=1)
        self.wait(0.3)


class ScaleScene(Scene):
    def construct(self):
        # Dark blue background
        bg = Rectangle(width=16, height=10, fill_color="#0a0a1a", fill_opacity=1, stroke_width=0)
        bg.set_z_index(-100)
        self.add(bg)

        # Corner decorations
        corner_lines = VGroup()
        for corner, angle in [(UL, 0), (UR, -PI/2), (DL, PI/2), (DR, PI)]:
            line1 = Line(ORIGIN, RIGHT * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            line2 = Line(ORIGIN, DOWN * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            corner_group = VGroup(line1, line2)
            corner_group.rotate(angle, about_point=ORIGIN)
            corner_group.move_to(corner * np.array([6.5, 3.5, 0]))
            corner_lines.add(corner_group)

        self.play(FadeIn(corner_lines), run_time=0.3)

        # Title
        title = Text("The Power of Scale", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        title_glow = title.copy().set_opacity(0.3).set_stroke(BLUE, width=6, opacity=0.2)
        self.play(Write(title), FadeIn(title_glow), run_time=1)

        # Bar chart on LEFT half - centered
        models = ["GPT-2", "GPT-3", "GPT-4"]
        years = ["2019", "2020", "2023"]
        parameters = [1.5, 175, 1760]  # in billions
        bar_colors = [BLUE, PURPLE, RED]

        # Use logarithmic scale for visual representation
        log_params = [np.log10(p) for p in parameters]
        max_log = max(log_params)

        chart_center = LEFT * 3
        max_height = 2.8
        bar_width = 1.0
        bar_base_y = -1.8

        # Reference lines - INCREASED OPACITY
        ref_lines = VGroup()
        ref_labels = VGroup()

        # Add reference line at 100B
        ref_y_100b = bar_base_y + (np.log10(100) / max_log) * max_height
        ref_line_100b = DashedLine(
            chart_center + LEFT * 1.5 + UP * (ref_y_100b - bar_base_y),
            chart_center + RIGHT * 1.5 + UP * (ref_y_100b - bar_base_y),
            dash_length=0.1,
            stroke_width=1.5,
            color=GRAY,
            stroke_opacity=0.6  # Increased from 0.4
        )
        ref_label_100b = Text("100B", font_size=14, color=GRAY).set_opacity(0.85)  # Increased
        ref_label_100b.next_to(ref_line_100b, LEFT, buff=0.1)
        ref_lines.add(ref_line_100b)
        ref_labels.add(ref_label_100b)

        # Add reference line at 1T
        ref_y_1t = bar_base_y + (np.log10(1000) / max_log) * max_height
        ref_line_1t = DashedLine(
            chart_center + LEFT * 1.5 + UP * (ref_y_1t - bar_base_y),
            chart_center + RIGHT * 1.5 + UP * (ref_y_1t - bar_base_y),
            dash_length=0.1,
            stroke_width=1.5,
            color=GRAY,
            stroke_opacity=0.6  # Increased from 0.4
        )
        ref_label_1t = Text("1T", font_size=14, color=GRAY).set_opacity(0.85)  # Increased
        ref_label_1t.next_to(ref_line_1t, LEFT, buff=0.1)
        ref_lines.add(ref_line_1t)
        ref_labels.add(ref_label_1t)

        bars = VGroup()
        model_labels = VGroup()
        year_labels = VGroup()
        param_labels = VGroup()
        chevrons_group = VGroup()
        bar_positions = []  # Store for particle effects

        for i, (model, year, param, log_p, color) in enumerate(zip(models, years, parameters, log_params, bar_colors)):
            height = (log_p / max_log) * max_height

            bar = RoundedRectangle(
                width=bar_width, height=height,
                corner_radius=0.08,
                fill_color=color, fill_opacity=0.7,
                stroke_color=color, stroke_width=2
            )

            x_pos = chart_center[0] + (i - 1) * 1.6
            bar.move_to(np.array([x_pos, bar_base_y + height/2, 0]))
            bar_positions.append((x_pos, bar_base_y + height, color))

            # Upward chevrons inside bar
            chevrons = VGroup()
            num_chevrons = min(3, int(height / 0.5) + 1)
            for j in range(num_chevrons):
                chevron = VGroup(
                    Line(LEFT * 0.15 + DOWN * 0.08, ORIGIN, stroke_width=1.5, color=WHITE).set_opacity(0.4),
                    Line(ORIGIN, RIGHT * 0.15 + DOWN * 0.08, stroke_width=1.5, color=WHITE).set_opacity(0.4)
                )
                chevron.move_to(bar.get_center() + DOWN * (height/2 - 0.3) + UP * (j * 0.4))
                chevrons.add(chevron)
            chevrons_group.add(chevrons)

            model_label = Text(model, font_size=20, color=WHITE)
            model_label.next_to(bar, DOWN, buff=0.15)

            year_label = Text(year, font_size=14, color=GRAY)
            year_label.next_to(model_label, DOWN, buff=0.08)

            param_text = f"{param}B" if param < 1000 else f"{param/1000:.1f}T"
            param_label = Text(param_text, font_size=16, color=color)
            param_label.next_to(bar, UP, buff=0.1)

            bars.add(bar)
            model_labels.add(model_label)
            year_labels.add(year_label)
            param_labels.add(param_label)

        y_label = Text("Parameters (log scale)", font_size=18, color=GRAY)
        y_label.rotate(PI/2)
        y_label.next_to(bars, LEFT, buff=0.8)

        # Timeline connecting year labels
        timeline = Line(
            year_labels[0].get_center() + DOWN * 0.2,
            year_labels[2].get_center() + DOWN * 0.2,
            stroke_width=1.5,
            color=GRAY,
            stroke_opacity=0.5
        )
        timeline_dots = VGroup()
        for year_label in year_labels:
            dot = Dot(radius=0.04, color=GRAY).move_to(year_label.get_center() + DOWN * 0.2)
            timeline_dots.add(dot)

        # Show reference lines first
        self.play(
            FadeIn(ref_lines),
            FadeIn(ref_labels),
            Write(y_label),
            run_time=0.8
        )

        # Animate bars with particle effects
        for i, (bar, model_label, year_label, param_label, chevrons, bar_pos) in enumerate(
            zip(bars, model_labels, year_labels, param_labels, chevrons_group, bar_positions)):

            target_height = bar.height
            bar.stretch_to_fit_height(0.1)
            bar.align_to(np.array([bar.get_center()[0], bar_base_y, 0]), DOWN)

            self.play(
                bar.animate.stretch_to_fit_height(target_height).align_to(
                    np.array([bar.get_center()[0], bar_base_y, 0]), DOWN
                ),
                Write(model_label),
                Write(year_label),
                run_time=0.6
            )

            # Reposition chevrons after bar animation
            for j, chevron in enumerate(chevrons):
                chevron.move_to(bar.get_center() + DOWN * (target_height/2 - 0.3) + UP * (j * 0.4))

            # Rising particle dots from bar top
            particles = VGroup()
            x_pos, top_y, color = bar_pos
            for _ in range(3):
                particle = Dot(radius=0.03, color=color)
                offset_x = np.random.uniform(-0.3, 0.3)
                particle.move_to(np.array([x_pos + offset_x, top_y, 0]))
                particles.add(particle)

            self.add(particles)

            self.play(
                FadeIn(param_label, shift=DOWN),
                FadeIn(chevrons),
                *[particle.animate.shift(UP * 0.5).set_opacity(0) for particle in particles],
                run_time=0.4
            )
            self.remove(particles)

        # Settling pause
        self.wait(0.25)

        # Animate timeline
        self.play(Create(timeline), run_time=0.5)
        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dot in timeline_dots], lag_ratio=0.2),
            run_time=0.5
        )

        # RIGHT SIDE: Key insight box with animated checkmarks
        insight_box = RoundedRectangle(
            width=4.8, height=2.8, corner_radius=0.2,
            fill_color="#1a1a3a", fill_opacity=0.9, stroke_color=BLUE, stroke_width=2
        )
        insight_box.move_to(RIGHT * 3 + DOWN * 0.2)

        insight_title = Text("Key Insight", font_size=22, color=BLUE)
        insight_title.move_to(insight_box.get_top() + DOWN * 0.35)

        insight_items = [
            ("More parameters", WHITE),
            ("Better understanding", GREEN),
            ("More capabilities", YELLOW),
            ("Emergent behaviors", PURPLE),
        ]

        insight_texts = VGroup()
        checkmarks = VGroup()

        for i, (text, color) in enumerate(insight_items):
            item_text = Text(f"â€¢ {text}", font_size=20, color=color)
            # Create checkmark as lines for draw animation
            check = VGroup(
                Line(ORIGIN, RIGHT * 0.08 + DOWN * 0.08, stroke_width=2, color=GREEN),
                Line(RIGHT * 0.08 + DOWN * 0.08, RIGHT * 0.2 + UP * 0.1, stroke_width=2, color=GREEN)
            )
            insight_texts.add(item_text)
            checkmarks.add(check)

        insight_texts.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        insight_texts.move_to(insight_box.get_center() + DOWN * 0.1)

        # Position checkmarks
        for text, check in zip(insight_texts, checkmarks):
            check.next_to(text, RIGHT, buff=0.15)

        self.play(Create(insight_box), run_time=0.5)
        self.play(Write(insight_title), run_time=0.5)

        # Animate items with draw animation for checkmarks
        for text, check in zip(insight_texts, checkmarks):
            self.play(FadeIn(text, shift=RIGHT * 0.3), run_time=0.3)
            self.play(Create(check), run_time=0.25)

        # Highlight exponential growth
        growth_arrow = CurvedArrow(
            bars[0].get_top() + UP * 0.3,
            bars[2].get_top() + UP * 0.3,
            angle=-PI/4,
            color=YELLOW,
            stroke_width=2
        )
        growth_label = Text("1000x growth!", font_size=18, color=YELLOW)
        growth_label.next_to(growth_arrow, UP, buff=0.1)

        self.play(Create(growth_arrow), Write(growth_label), run_time=1)

        self.wait(2)
        all_elements = VGroup(title, title_glow, bars, model_labels, year_labels, param_labels,
                             y_label, insight_box, insight_title, insight_texts, checkmarks,
                             growth_arrow, growth_label, corner_lines, ref_lines, ref_labels,
                             chevrons_group, timeline, timeline_dots)
        self.play(FadeOut(all_elements), run_time=1)
        self.wait(0.3)


class ConclusionScene(Scene):
    def construct(self):
        # Dark blue background
        bg = Rectangle(width=16, height=10, fill_color="#0a0a1a", fill_opacity=1, stroke_width=0)
        bg.set_z_index(-100)
        self.add(bg)

        # Background neural network with slow parallax drift
        bg_nodes = VGroup()
        bg_connections = VGroup()
        np.random.seed(123)

        positions = [
            [-5, 2, 0], [-4, -1, 0], [-3, 1.5, 0],
            [4, 2, 0], [5, -0.5, 0], [3, -2, 0],
            [-4.5, -2.5, 0], [4.5, 1, 0]
        ]

        # Different drift speeds for parallax
        drift_speeds = [0.02, 0.015, 0.025, 0.018, 0.022, 0.012, 0.02, 0.016]

        for i, pos in enumerate(positions):
            node = Dot(point=pos, radius=0.08, color=BLUE).set_opacity(0.15)
            bg_nodes.add(node)

        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                if np.random.random() > 0.6:
                    line = Line(positions[i], positions[j], stroke_width=0.5, color=BLUE).set_opacity(0.08)
                    bg_connections.add(line)

        bg_network = VGroup(bg_connections, bg_nodes)
        self.add(bg_network)

        # Corner decorations
        corner_lines = VGroup()
        for corner, angle in [(UL, 0), (UR, -PI/2), (DL, PI/2), (DR, PI)]:
            line1 = Line(ORIGIN, RIGHT * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            line2 = Line(ORIGIN, DOWN * 0.8, stroke_width=1, color=BLUE_E, stroke_opacity=0.3)
            corner_group = VGroup(line1, line2)
            corner_group.rotate(angle, about_point=ORIGIN)
            corner_group.move_to(corner * np.array([6.5, 3.5, 0]))
            corner_lines.add(corner_group)

        self.play(FadeIn(corner_lines), run_time=0.3)

        # Title
        title = Text("Large Language Models", font_size=52, color=BLUE)
        title.to_edge(UP, buff=0.7)
        title_glow = title.copy().set_opacity(0.3).set_stroke(BLUE, width=8, opacity=0.2)
        self.play(Write(title), FadeIn(title_glow), run_time=1)

        # Summary points with LARGER icons
        points = [
            ("1", "Tokenization", "Breaking text into pieces", RED, Circle(radius=0.18)),
            ("2", "Embeddings", "Words as vectors", ORANGE, Square(side_length=0.3)),
            ("3", "Attention", "Understanding context", YELLOW, Triangle().scale(0.18)),
            ("4", "Transformers", "Processing in parallel", GREEN, Star(n=5, outer_radius=0.2, inner_radius=0.1)),
            ("5", "Generation", "Predicting next tokens", BLUE, RegularPolygon(n=6, radius=0.18)),
        ]

        point_groups = VGroup()
        decorative_lines = VGroup()
        connection_lines = VGroup()
        icons = VGroup()

        for i, (num, title_text, desc, color, icon) in enumerate(points):
            # Larger icon
            icon.set_fill(color, opacity=0.4)
            icon.set_stroke(color, width=2)
            icon.scale(1.3)  # 30% larger
            icons.add(icon)

            # Number
            num_text = Text(num, font_size=28, color=color)

            # Title
            title_t = Text(title_text, font_size=28, color=WHITE)

            # Description
            desc_t = Text(f"â€” {desc}", font_size=20, color=GRAY)

            # Arrange
            icon.next_to(num_text, LEFT, buff=0.35)
            title_t.next_to(num_text, RIGHT, buff=0.25)
            desc_t.next_to(title_t, RIGHT, buff=0.25)

            group = VGroup(icon, num_text, title_t, desc_t)

            # Decorative line
            dec_line = Line(LEFT * 0.5, RIGHT * 0.5, stroke_width=1, color=color, stroke_opacity=0.3)
            decorative_lines.add(dec_line)

            point_groups.add(group)

        point_groups.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        point_groups.move_to(ORIGIN + UP * 0.1)

        # Position decorative lines
        for line, group in zip(decorative_lines, point_groups):
            line.next_to(group, LEFT, buff=0.35)

        # Create connection lines between points - MORE VISIBLE
        for i in range(len(point_groups) - 1):
            conn_line = Line(
                point_groups[i].get_bottom() + DOWN * 0.05,
                point_groups[i + 1].get_top() + UP * 0.05,
                stroke_width=1.5,  # Increased from 1
                color=WHITE,
                stroke_opacity=0.4  # Increased from 0.2
            )
            connection_lines.add(conn_line)

        # Animate points with icon glow pulse before text
        for i, (group, dec_line, icon) in enumerate(zip(point_groups, decorative_lines, icons)):
            # Icon glow pulse before text appears
            icon_glow = icon.copy().set_stroke(width=6, opacity=0.5)
            self.add(icon_glow)
            self.play(
                icon_glow.animate.scale(1.3).set_opacity(0),
                run_time=0.25
            )
            self.remove(icon_glow)

            self.play(
                FadeIn(dec_line),
                FadeIn(group, shift=RIGHT * 0.4),
                run_time=0.45
            )
            if i < len(connection_lines):
                self.play(Create(connection_lines[i]), run_time=0.15)

        # Settling pause
        self.wait(0.3)

        # Parallax drift animation for background
        drift_anims = []
        for node, speed in zip(bg_nodes, drift_speeds):
            direction = np.array([np.random.uniform(-1, 1), np.random.uniform(-1, 1), 0])
            direction = direction / np.linalg.norm(direction) * speed
            drift_anims.append(node.animate.shift(direction))

        # Pulse background network with parallax
        self.play(
            bg_network.animate.set_opacity(0.25),
            *drift_anims,
            rate_func=there_and_back,
            run_time=1.5
        )

        # Final message
        final_message = Text(
            "The foundation of modern AI assistants",
            font_size=28, color=PURPLE
        )
        final_message.to_edge(DOWN, buff=0.8)

        final_glow = final_message.copy().set_opacity(0.3).set_stroke(PURPLE, width=4, opacity=0.2)

        self.play(Write(final_message), FadeIn(final_glow), run_time=1.2)

        # Pulse summary points before fade - snappier (1.05 instead of larger)
        pulse_anims = []
        for i, group in enumerate(point_groups):
            pulse_anims.append(
                Succession(
                    Wait(i * 0.12),
                    group.animate.scale(1.05),
                    group.animate.scale(1/1.05)
                )
            )

        self.play(*pulse_anims, run_time=1.8)

        # Glow effect on title
        self.play(
            title.animate.set_color(YELLOW),
            title_glow.animate.set_color(YELLOW).set_opacity(0.5),
            rate_func=there_and_back,
            run_time=1
        )

        self.wait(1.5)

        # Fade out everything
        all_content = VGroup(title, title_glow, point_groups, decorative_lines, connection_lines,
                            final_message, final_glow, corner_lines, bg_network)
        self.play(FadeOut(all_content), run_time=1.2)

        # Thank you with color shift
        thanks = Text("Thank You!", font_size=64, color=BLUE)
        thanks_glow = thanks.copy().set_opacity(0.3).set_stroke(BLUE, width=8, opacity=0.2)

        # Expanding circles effect
        circles = VGroup()
        for i in range(4):
            circle = Circle(radius=0.5 + i * 0.5, stroke_width=2, color=BLUE)
            circle.set_stroke(opacity=0.4 - i * 0.1)
            circles.add(circle)

        self.play(Write(thanks), FadeIn(thanks_glow), run_time=1)

        # Color shift animation
        self.play(
            thanks.animate.set_color(WHITE),
            thanks_glow.animate.set_color(WHITE),
            run_time=0.4
        )
        self.play(
            thanks.animate.set_color(BLUE),
            thanks_glow.animate.set_color(BLUE),
            run_time=0.4
        )

        # Starburst effect with sparkle dots at ray tips
        rays = VGroup()
        ray_tips = VGroup()
        for angle in range(0, 360, 30):
            ray = Line(ORIGIN, RIGHT * 2, stroke_width=1, color=YELLOW, stroke_opacity=0.3)
            ray.rotate(angle * DEGREES, about_point=ORIGIN)
            rays.add(ray)

            # Sparkle dot at tip
            tip_dot = Dot(radius=0.04, color=YELLOW).move_to(ray.get_end())
            ray_tips.add(tip_dot)

        self.play(
            *[Create(circle) for circle in circles],
            *[Create(ray) for ray in rays],
            *[GrowFromCenter(dot) for dot in ray_tips],
            run_time=0.8
        )

        self.play(
            thanks.animate.scale(1.2),
            *[circle.animate.scale(1.5).set_opacity(0) for circle in circles],
            *[ray.animate.scale(1.5).set_opacity(0) for ray in rays],
            *[dot.animate.scale(1.5).set_opacity(0) for dot in ray_tips],
            rate_func=smooth,
            run_time=1.2
        )

        self.play(
            thanks.animate.scale(1/1.2),
            run_time=0.5
        )

        self.wait(1.5)
        self.play(FadeOut(thanks), FadeOut(thanks_glow), run_time=1)
