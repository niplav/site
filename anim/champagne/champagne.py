from manim import *
import numpy as np

class ChampagneToastN2(Scene):
    """Two glasses moving in a straight line to meet."""
    def construct(self):
        # Configuration
        radius = 0.3
        distance = 4.0

        # Create two circles at opposite sides
        glass_a = Circle(radius=radius, color=BLUE, fill_opacity=0.3)
        glass_b = Circle(radius=radius, color=RED, fill_opacity=0.3)

        glass_a.shift(LEFT * distance / 2)
        glass_b.shift(RIGHT * distance / 2)

        # Labels
        label_a = Text("A", font_size=24).move_to(glass_a.get_center())
        label_b = Text("B", font_size=24).move_to(glass_b.get_center())

        # Show initial setup
        self.play(Create(glass_a), Create(glass_b), Write(label_a), Write(label_b))

        # Add corner position markers
        dot_a = Dot(glass_a.get_center(), color=BLUE, radius=0.08)
        dot_a.set_opacity(0.3)
        dot_b = Dot(glass_b.get_center(), color=RED, radius=0.08)
        dot_b.set_opacity(0.3)
        self.play(FadeIn(dot_a), FadeIn(dot_b))
        self.wait(0.5)

        # Calculate meeting point (midpoint)
        meeting_point = ORIGIN

        # Move glasses together
        self.play(
            glass_a.animate.move_to(meeting_point + LEFT * radius),
            glass_b.animate.move_to(meeting_point + RIGHT * radius),
            label_a.animate.move_to(meeting_point + LEFT * radius),
            label_b.animate.move_to(meeting_point + RIGHT * radius),
            run_time=1.5
        )
        self.wait(0.5)

        # Highlight the touching point
        touch_dot = Dot(meeting_point, color=YELLOW)
        self.play(FadeIn(touch_dot))
        self.wait(0.5)
        self.play(FadeOut(touch_dot))

        # Return to original positions
        self.play(
            glass_a.animate.shift(LEFT * distance / 2),
            glass_b.animate.shift(RIGHT * distance / 2),
            label_a.animate.move_to(glass_a.get_center() + LEFT * distance / 2),
            label_b.animate.move_to(glass_b.get_center() + RIGHT * distance / 2),
            run_time=1.5
        )
        self.wait(1)


class ChampagneToastN3(Scene):
    """Three glasses forming an equilateral triangle, meeting at center."""
    def construct(self):
        # Configuration
        radius = 0.3
        triangle_radius = 3.0  # Distance from center to each corner

        # Calculate positions for equilateral triangle
        angles = [90, 210, 330]  # Degrees
        positions = [
            triangle_radius * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
            for a in angles
        ]

        # Create three circles
        colors = [BLUE, RED, GREEN]
        glasses = []
        labels = []

        for i, (pos, color) in enumerate(zip(positions, colors)):
            glass = Circle(radius=radius, color=color, fill_opacity=0.3)
            glass.move_to(pos)
            label = Text(chr(65 + i), font_size=24).move_to(pos)
            glasses.append(glass)
            labels.append(label)

        # Show initial setup
        self.play(
            *[Create(g) for g in glasses],
            *[Write(l) for l in labels]
        )

        # Add corner position markers
        corner_dots = []
        for i, (pos, color) in enumerate(zip(positions, colors)):
            dot = Dot(pos, color=color, radius=0.08)
            dot.set_opacity(0.3)
            corner_dots.append(dot)

        self.play(*[FadeIn(dot) for dot in corner_dots])
        self.wait(0.5)

        # Calculate center position where they meet
        center = ORIGIN
        # Arrange in a triplet: three circles all touching each other
        # For three circles of radius r to all touch each other:
        # - Centers form equilateral triangle with side length 2r
        # - Distance from center to each vertex is 2r/sqrt(3)
        triplet_radius = (2 * radius) / np.sqrt(3)
        triplet_positions = [
            center + triplet_radius * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
            for a in [90, 210, 330]
        ]

        # Move glasses to center to form triplet
        self.play(
            *[glasses[i].animate.move_to(triplet_positions[i]) for i in range(3)],
            *[labels[i].animate.move_to(triplet_positions[i]) for i in range(3)],
            run_time=2
        )
        self.wait(1)

        # Return to original positions
        self.play(
            *[glasses[i].animate.move_to(positions[i]) for i in range(3)],
            *[labels[i].animate.move_to(positions[i]) for i in range(3)],
            run_time=2
        )
        self.wait(1)


class ChampagneToastN4(Scene):
    """Four glasses at square corners: A,B,C form triplet, then D joins."""
    def construct(self):
        # Configuration
        radius = 0.3
        square_radius = 3.0  # Distance from center to each corner

        # Calculate positions for square (4 corners)
        angles = [45, 135, 225, 315]  # Degrees
        positions = [
            square_radius * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
            for a in angles
        ]

        # Create four circles
        colors = [BLUE, RED, GREEN, YELLOW]
        labels_text = ['A', 'B', 'C', 'D']
        glasses = []
        labels = []

        for i, (pos, color, label_text) in enumerate(zip(positions, colors, labels_text)):
            glass = Circle(radius=radius, color=color, fill_opacity=0.3)
            glass.move_to(pos)
            label = Text(label_text, font_size=24).move_to(pos)
            glasses.append(glass)
            labels.append(label)

        # Show initial setup
        self.play(
            *[Create(g) for g in glasses],
            *[Write(l) for l in labels]
        )
        self.wait(0.5)

        # Step 1: A, B, C move to form a triplet slightly offset from center
        # We'll offset the triplet slightly up-left so D can come from the bottom-right
        triplet_center = UP * 0.5 + LEFT * 0.5
        triplet_angles = [90, 210, 330]
        triplet_radius = (2 * radius) / np.sqrt(3)
        triplet_positions = [
            triplet_center + triplet_radius * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
            for a in triplet_angles
        ]

        self.play(
            *[glasses[i].animate.move_to(triplet_positions[i]) for i in range(3)],
            *[labels[i].animate.move_to(triplet_positions[i]) for i in range(3)],
            run_time=2
        )
        self.wait(0.5)

        # Highlight that A, B, C are touching
        dot_abc = Dot(triplet_center, color=WHITE, radius=0.08)
        self.play(FadeIn(dot_abc))
        self.wait(0.5)

        # Step 2: D moves in to touch B & C
        # Position D to be tangent to both B and C
        # B is at triplet_positions[1], C is at triplet_positions[2]
        # We need D to touch both B and C

        # For simplicity, position D at a point where it's tangent to B and C
        # This is a bit tricky geometrically, so let's position D between B and C
        # at a distance of 2*radius from each

        b_pos = triplet_positions[1]
        c_pos = triplet_positions[2]
        bc_midpoint = (b_pos + c_pos) / 2

        # Move D toward B and C
        # Calculate a position where D touches both B and C
        # For circles of equal radius, this forms an equilateral triangle
        bc_vector = c_pos - b_pos
        bc_distance = np.linalg.norm(bc_vector)
        perpendicular = np.array([-bc_vector[1], bc_vector[0], 0])
        perpendicular = perpendicular / np.linalg.norm(perpendicular)

        # Position D below the BC edge
        d_touch_bc = bc_midpoint - perpendicular * radius * np.sqrt(3)

        self.play(FadeOut(dot_abc))
        self.play(
            glasses[3].animate.move_to(d_touch_bc),
            labels[3].animate.move_to(d_touch_bc),
            run_time=1.5
        )
        self.wait(0.5)

        # Highlight that D is touching B and C
        bc_center = (b_pos + c_pos + d_touch_bc) / 3
        dot_bcd = Dot(bc_center, color=WHITE, radius=0.08)
        self.play(FadeIn(dot_bcd))
        self.wait(0.5)

        # Step 3: D "pushes" to briefly touch A
        # Move B, C, and D together so D can reach A
        a_pos = triplet_positions[0]

        # Calculate where D needs to be to touch A
        # D should be at distance 2*radius from A
        direction_to_a = a_pos - d_touch_bc
        direction_to_a = direction_to_a / np.linalg.norm(direction_to_a)
        d_touch_a = a_pos - direction_to_a * 2 * radius

        # Move D toward A (and slightly adjust B, C to maintain contact if desired)
        # For simplicity, just move D
        self.play(FadeOut(dot_bcd))
        self.play(
            glasses[3].animate.move_to(d_touch_a),
            labels[3].animate.move_to(d_touch_a),
            run_time=1.5
        )
        self.wait(0.5)

        # Highlight that D is now touching A
        ad_midpoint = (a_pos + d_touch_a) / 2
        dot_ad = Dot(ad_midpoint, color=WHITE, radius=0.08)
        self.play(FadeIn(dot_ad))
        self.wait(0.5)
        self.play(FadeOut(dot_ad))

        # Step 4: All return to original positions
        self.play(
            *[glasses[i].animate.move_to(positions[i]) for i in range(4)],
            *[labels[i].animate.move_to(positions[i]) for i in range(4)],
            run_time=2
        )
        self.wait(1)


class ChampagneToastN4Better(Scene):
    """
    Improved N=4 solution: Move A,B,C to center forming triplet,
    then bring D in from the side to touch all three sequentially.
    """
    def construct(self):
        # Configuration
        radius = 0.3
        square_radius = 3.0

        # Square corners
        angles = [45, 135, 225, 315]
        positions = [
            square_radius * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
            for a in angles
        ]

        # Create glasses
        colors = [BLUE, RED, GREEN, YELLOW]
        labels_text = ['A', 'B', 'C', 'D']
        glasses = []
        labels = []

        for i, (pos, color, label_text) in enumerate(zip(positions, colors, labels_text)):
            glass = Circle(radius=radius, color=color, fill_opacity=0.3)
            glass.move_to(pos)
            label = Text(label_text, font_size=24).move_to(pos)
            glasses.append(glass)
            labels.append(label)

        # Show initial setup
        self.play(
            *[Create(g) for g in glasses],
            *[Write(l) for l in labels]
        )

        # Add corner position markers to show start/end points
        corner_dots = []
        for i, (pos, color) in enumerate(zip(positions, colors)):
            dot = Dot(pos, color=color, radius=0.08)
            dot.set_opacity(0.3)
            corner_dots.append(dot)

        self.play(*[FadeIn(dot) for dot in corner_dots])
        self.wait(0.5)

        # Add title
        title = Text("n=4: Proposed Solution", font_size=32).to_edge(UP)
        self.play(Write(title))

        # Calculate triplet positions first (oriented toward top-left)
        triplet_center = ORIGIN
        triplet_radius = (2 * radius) / np.sqrt(3)
        triplet_angles = [135, 255, 15]  # B at 135°, C at 255°, A at 15°
        abc_triplet = [
            triplet_center + triplet_radius * np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
            for a in triplet_angles
        ]

        # Step 1: A and C meet first (they're diagonal)
        step1 = Text("Step 1: A & C meet", font_size=24).to_edge(DOWN)
        self.play(Write(step1))

        # A and C move directly to their triplet positions (already on diagonal)
        # A goes to position 2 (15°), C to position 1 (255°)
        self.play(
            glasses[0].animate.move_to(abc_triplet[2]),  # A to 15°
            labels[0].animate.move_to(abc_triplet[2]),
            glasses[2].animate.move_to(abc_triplet[1]),  # C to 255°
            labels[2].animate.move_to(abc_triplet[1]),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(FadeOut(step1))

        # Step 2: B docks from top-left to form triplet oriented toward top-left
        step2 = Text("Step 2: B docks to form triplet", font_size=24).to_edge(DOWN)
        self.play(Write(step2))

        # Only B moves now (to position 0 at 135°)
        self.play(
            glasses[1].animate.move_to(abc_triplet[0]),
            labels[1].animate.move_to(abc_triplet[0]),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(FadeOut(step2))

        # Step 3: D approaches and touches A & C
        step3 = Text("Step 3: D touches A & C", font_size=24).to_edge(DOWN)
        self.play(Write(step3))

        # Get current positions after triplet formation
        a_pos = abc_triplet[2]  # A is at position 2
        c_pos = abc_triplet[1]  # C is at position 1

        # D approaches from bottom-right to touch A and C
        # Position D to be tangent to both A and C
        ac_midpoint = (a_pos + c_pos) / 2
        # D comes from the opposite side of the triplet center
        from_center = ac_midpoint - triplet_center
        from_center_norm = from_center / np.linalg.norm(from_center)
        d_pos_ac = ac_midpoint + from_center_norm * radius * np.sqrt(3)

        self.play(
            glasses[3].animate.move_to(d_pos_ac),
            labels[3].animate.move_to(d_pos_ac),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(FadeOut(step3))

        # Step 4: A & C move aside so D can pass through to touch B
        step4 = Text("Step 4: D passes through to touch B", font_size=24).to_edge(DOWN)
        self.play(Write(step4))

        b_pos = abc_triplet[0]  # B is at position 0 (135°)

        # Move A and C outward more to make room for D
        a_new = a_pos + (a_pos - triplet_center) * 1.2
        c_new = c_pos + (c_pos - triplet_center) * 1.2

        # First, A and C move out of the way (straight lines for optimal trajectory)
        self.play(
            glasses[0].animate(path_arc=0).move_to(a_new),
            labels[0].animate(path_arc=0).move_to(a_new),
            glasses[2].animate(path_arc=0).move_to(c_new),
            labels[2].animate(path_arc=0).move_to(c_new),
            run_time=1.0
        )
        self.wait(0.3)

        # Then D moves to touch B
        d_to_b = b_pos - d_pos_ac
        d_to_b_norm = d_to_b / np.linalg.norm(d_to_b)
        d_pos_b = b_pos - d_to_b_norm * 2 * radius

        self.play(
            glasses[3].animate.move_to(d_pos_b),
            labels[3].animate.move_to(d_pos_b),
            run_time=1.0
        )
        self.wait(0.5)
        self.play(FadeOut(step4))

        # Step 5: Return to original positions
        step5 = Text("Step 5: Return to corners", font_size=24).to_edge(DOWN)
        self.play(Write(step5))

        self.play(
            *[glasses[i].animate.move_to(positions[i]) for i in range(4)],
            *[labels[i].animate.move_to(positions[i]) for i in range(4)],
            run_time=2
        )
        self.wait(0.5)
        self.play(FadeOut(step5), FadeOut(title))
        self.wait(1)


class ChampagneToastOverview(Scene):
    """Shows all solutions side by side for comparison."""
    def construct(self):
        title = Text("The Champagne Toasting Problem", font_size=40)
        subtitle = Text("Minimize total path length for all glasses to touch", font_size=24)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), Write(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Show the solutions for n=2, 3, 4 in sequence
        for n in [2, 3, 4]:
            n_title = Text(f"n = {n}", font_size=36)
            self.play(Write(n_title))
            self.wait(1)
            self.play(FadeOut(n_title))
