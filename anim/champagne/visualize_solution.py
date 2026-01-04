#!/usr/bin/env python3
"""
Manim animation to visualize champagne toasting solutions from JSON.

Usage:
  manim -pql visualize_solution.py ChampagneSolutionVisualization

To visualize a specific solution file, modify JSON_PATH below.
"""

from manim import *
import json
import numpy as np

# Configuration: path to solution JSON file
JSON_PATH = '/home/niplav/proj/site/code/champagne/best_n8_w22_pathonly.json'

class ChampagneSolutionVisualization(Scene):
    def construct(self):
        # Load solution data
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)

        metadata = data['metadata']
        initial_positions = np.array(data['initial_positions'])
        trajectories = data['disk_trajectories']

        # Get number of disks from data
        n_disks = metadata['n_disks']

        # Scale factor for visualization (reduced to fit in frame)
        scale = 1.0
        vertical_offset = -0.5  # Shift everything down to avoid title overlap

        # Disk properties (actual problem radius is 0.3, scaled)
        actual_radius = 0.3
        radius = actual_radius * scale

        # Generate colors for any number of disks
        base_colors = [BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE, PINK, TEAL, GOLD, MAROON]
        colors = (base_colors * ((n_disks // len(base_colors)) + 1))[:n_disks]

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
        for i in range(n_disks):
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
            for disk_id in range(n_disks):
                pos = trajectories[str(disk_id)]['path'][wp_idx]
                targets.append([pos[0] * scale, pos[1] * scale + vertical_offset, 0])

            # Animate movement to waypoint
            animations = []
            for i in range(n_disks):
                animations.append(glasses[i].animate.move_to(targets[i]))
                animations.append(labels[i].animate.move_to(targets[i]))

            self.play(*animations, run_time=1.5)
            self.wait(0.3)

        # Return home
        animations = []
        for i in range(n_disks):
            home_pos = [initial_positions[i][0] * scale, initial_positions[i][1] * scale + vertical_offset, 0]
            animations.append(glasses[i].animate.move_to(home_pos))
            animations.append(labels[i].animate.move_to(home_pos))

        self.play(*animations, run_time=1.5)
        self.wait(1)


if __name__ == "__main__":
    # Render with: manim -pql visualize_solution.py ChampagneSolutionVisualization
    pass
