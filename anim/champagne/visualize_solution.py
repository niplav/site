#!/usr/bin/env python3
"""
Manim animation to visualize champagne toasting solutions from JSON.
"""

from manim import *
import json
import numpy as np


class ChampagneSolutionVisualization(Scene):
    def construct(self):
        # Load solution data
        with open('/home/niplav/proj/site/code/champagne/best_1.json', 'r') as f:
            data = json.load(f)

        metadata = data['metadata']
        initial_positions = np.array(data['initial_positions'])
        trajectories = data['disk_trajectories']

        # Scale factor for visualization (reduced to fit in frame)
        scale = 1.0
        vertical_offset = -0.5  # Shift everything down to avoid title overlap

        # Disk properties (actual problem radius is 0.3, scaled)
        actual_radius = 0.3
        radius = actual_radius * scale
        colors = [BLUE, RED, GREEN, YELLOW, PURPLE]

        # Create title (smaller and positioned higher)
        title = Text(f"Champagne Toasting: n=5", font_size=28)
        subtitle = Text(f"Path Length: {metadata['path_length']:.2f}", font_size=20)
        title.to_edge(UP, buff=0.2)
        subtitle.next_to(title, DOWN, buff=0.1)

        self.play(Write(title), Write(subtitle))
        self.wait(0.5)

        # Create corner position markers (semi-transparent)
        corner_markers = VGroup()
        for i, pos in enumerate(initial_positions):
            marker = Dot(point=[pos[0] * scale, pos[1] * scale + vertical_offset, 0],
                        radius=0.1,
                        color=colors[i],
                        fill_opacity=0.3)
            corner_markers.add(marker)

        self.play(FadeIn(corner_markers))

        # Create glasses (disks) and labels
        glasses = VGroup()
        labels = VGroup()

        for i, pos in enumerate(initial_positions):
            glass = Circle(radius=radius, color=colors[i], fill_opacity=0.5)
            glass.move_to([pos[0] * scale, pos[1] * scale + vertical_offset, 0])
            glasses.add(glass)

            label = Text(str(i), font_size=20, color=WHITE)
            label.move_to(glass.get_center())
            labels.add(label)

        self.play(
            *[FadeIn(glass) for glass in glasses],
            *[FadeIn(label) for label in labels]
        )
        self.wait(0.5)

        # Create path tracers (will show where disks have been)
        tracers = VGroup()
        for i in range(5):
            path = trajectories[str(i)]['path']
            start_point = [path[0][0] * scale, path[0][1] * scale, 0]
            tracer = TracedPath(glasses[i].get_center, stroke_color=colors[i],
                               stroke_width=2, stroke_opacity=0.5)
            tracers.add(tracer)
            self.add(tracer)

        # Animate through waypoints
        n_waypoints = len(trajectories['0']['path']) - 2  # Exclude initial and final return

        for wp_idx in range(1, n_waypoints + 1):
            # Get target positions for this waypoint
            targets = []
            for disk_id in range(5):
                pos = trajectories[str(disk_id)]['path'][wp_idx]
                targets.append([pos[0] * scale, pos[1] * scale + vertical_offset, 0])

            # Animate movement to waypoint
            animations = []
            for i in range(5):
                animations.append(glasses[i].animate.move_to(targets[i]))
                animations.append(labels[i].animate.move_to(targets[i]))

            self.play(*animations, run_time=1.5)
            self.wait(0.3)

        # Return home
        animations = []
        for i in range(5):
            home_pos = [initial_positions[i][0] * scale, initial_positions[i][1] * scale + vertical_offset, 0]
            animations.append(glasses[i].animate.move_to(home_pos))
            animations.append(labels[i].animate.move_to(home_pos))

        self.play(*animations, run_time=1.5)
        self.wait(1)


if __name__ == "__main__":
    # Render with: manim -pql visualize_solution.py ChampagneSolutionVisualization
    pass
