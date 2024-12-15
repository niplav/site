from manim import *
import numpy as np

class LongDiamondAnimation(ThreeDScene):
    def construct(self):
        # Configuration
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)

        # Create the basic cube frame with 3x3x3 grid - now scaled
        cube = VGroup()
        grid_size = 3
        for i in range(grid_size):
            for j in range(grid_size):
                for k in range(grid_size):
                    # Scale grid points from -2 to 2
                    x = (i - 1) * 2
                    y = (j - 1) * 2
                    z = (k - 1) * 2
                    point = Dot3D(point=[x, y, z], radius=0.05, color=BLUE)
                    cube.add(point)

        # Make cube translucent
        cube_surface = Cube(side_length=4)
        cube_surface.set_fill(BLUE, opacity=0.1)
        cube_surface.set_stroke(BLUE_E, opacity=0.3)

        # Add basic elements to scene
        self.play(Create(cube), Create(cube_surface))
        self.wait(1)

        # Generate corner coordinates
        corners = np.array([
            [-2, -2, -2], [-2, -2, 2], [-2, 2, -2], [-2, 2, 2],
            [2, -2, -2], [2, -2, 2], [2, 2, -2], [2, 2, 2]
        ])

        # Generate random colors for corners
        corner_colors = [
            color_gradient([BLUE, RED, GREEN, YELLOW], 8)[i]
            for i in range(8)
        ]

        # Light up corners
        corner_dots = VGroup()
        for corner, color in zip(corners, corner_colors):
            dot = Dot3D(point=corner, radius=0.1, color=color)  # Increased radius
            corner_dots.add(dot)
            self.play(Create(dot), run_time=0.3)

        self.wait(1)

        # Define edges and their midpoints
        edges = [
            ([1, 3], [-2, 0, 2]),
            ([1, 5], [0, -2, 2]),
            ([3, 7], [0, 2, 2]),
            ([5, 7], [2, 0, 2]),

            ([0, 1], [-2, -2, 0]),
            ([2, 3], [-2, 2, 0]),
            ([4, 5], [2, -2, 0]),
            ([6, 7], [2, 2, 0]),

            ([0, 2], [-2, 0, -2]),
            ([4, 0], [0, -2, -2]),
            ([6, 2], [0, 2, -2]),
            ([4, 6], [2, 0, -2])
        ]

        # Process each edge
        for (corner1_idx, corner2_idx), edge_center in edges:
            # Calculate mean color for edge center
            edge_colors = [corner_colors[corner1_idx], corner_colors[corner2_idx]]
            edge_center_color = average_color(*edge_colors)
            edge_center_dot = Dot3D(point=edge_center, radius=0.08, color=edge_center_color)

            # Create arrows from corners to edge center
            edge_arrows = VGroup()
            for corner_idx in [corner1_idx, corner2_idx]:
                start_point = corners[corner_idx]
                direction = np.array(edge_center) - start_point
                # Normalize and scale to make arrow shorter
                direction = direction / np.linalg.norm(direction) * (np.linalg.norm(direction) - 0.3)
                end_point = start_point + direction

                arrow = Arrow3D(
                    start=start_point,
                    end=end_point,
                    color=BLUE_E,
                    thickness=0.005,
                )
                edge_arrows.add(arrow)

            self.play(
                Create(edge_center_dot),
                *[Create(arrow) for arrow in edge_arrows],
                run_time=0.5
            )

        # Define faces and their centers
        faces = [
            # Front, Back, Left, Right, Top, Bottom
            ([1, 3, 5, 7], [0, 0, 2]),
            ([0, 2, 4, 6], [0, 0, -2]),
            ([4, 5, 6, 7], [2, 0, 0]),
            ([0, 1, 2, 3], [-2, 0, 0]),
            ([2, 3, 6, 7], [0, 2, 0]),
            ([0, 1, 4, 5], [0, -2, 0])
        ]

        # Process each face
        #for face_edgecenter_idx, face_center in faces:
            # Calculate mean color for face center

        face_centers = []

        # Continue rotation for a few more seconds
        self.wait(3)

class LongSquareAnimation(ThreeDScene):
    def construct(self):
        # Configuration
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)

        # Create the basic cube frame with 3x3x3 grid - now scaled
        cube = VGroup()
        grid_size = 3
        for i in range(grid_size):
            for j in range(grid_size):
                for k in range(grid_size):
                    x = (i - 1) * 2
                    y = (j - 1) * 2
                    z = (k - 1) * 2
                    point = Dot3D(point=[x, y, z], radius=0.05, color=BLUE)
                    cube.add(point)

        # Make cube translucent
        cube_surface = Cube(side_length=4)
        cube_surface.set_fill(BLUE, opacity=0.1)
        cube_surface.set_stroke(BLUE_E, opacity=0.3)

        self.play(Create(cube), Create(cube_surface))
        self.wait(1)

        # Generate corner coordinates
        corners = np.array([
            [-2, -2, -2], [-2, -2, 2], [-2, 2, -2], [-2, 2, 2],
            [2, -2, -2], [2, -2, 2], [2, 2, -2], [2, 2, 2]
        ])

        # Hardcoded corner colors for better caching
        corner_colors = [
            "#FF0000",  # Red
            "#00FF00",  # Green
            "#0000FF",  # Blue
            "#FFFF00",  # Yellow
            "#FF00FF",  # Magenta
            "#00FFFF",  # Cyan
            "#FF8000",  # Orange
            "#8000FF",  # Purple
        ]

        # Light up corners
        corner_dots = VGroup()
        for corner, color in zip(corners, corner_colors):
            dot = Dot3D(point=corner, radius=0.1, color=color)
            corner_dots.add(dot)
            self.play(Create(dot), run_time=0.3)

        self.wait(1)

        # Calculate and show center point with mean color
        center_color = average_color(*corner_colors)
        center = Dot3D(point=[0, 0, 0], radius=0.15, color=center_color)

        # Draw arrows from corners to center with smaller tips
        arrows_to_center = VGroup()
        for corner in corners:
            direction = np.array([0, 0, 0]) - corner
            direction = direction / np.linalg.norm(direction) * (np.linalg.norm(direction) - 0.4)
            end_point = corner + direction

            arrow = Arrow3D(
                start=corner,
                end=end_point,
                color=WHITE,
                thickness=0.015
            )
            arrows_to_center.add(arrow)

        self.play(
            Create(center),
            *[Create(arrow) for arrow in arrows_to_center],
            run_time=2
        )
        self.wait(1)

        # Define edges and their midpoints
        edges = [
            ([1, 3], [-2, 0, 2]),
            ([1, 5], [0, -2, 2]),
            ([3, 7], [0, 2, 2]),
            ([5, 7], [2, 0, 2]),

            ([0, 1], [-2, -2, 0]),
            ([2, 3], [-2, 2, 0]),
            ([4, 5], [2, -2, 0]),
            ([6, 7], [2, 2, 0]),

            ([0, 2], [-2, 0, -2]),
            ([4, 0], [0, -2, -2]),
            ([6, 2], [0, 2, -2]),
            ([4, 6], [2, 0, -2]),
        ]

        # Process each edge
        for (corner1_idx, corner2_idx), edge_center in edges:
            colors_to_average = [
                corner_colors[corner1_idx],
                corner_colors[corner2_idx]
            ]

            edge_center_color = average_color(*colors_to_average)
            edge_center_dot = Dot3D(point=edge_center, radius=0.08, color=edge_center_color)

            edge_arrows = VGroup()

            # Arrows from corners to edge center
            for corner_idx in [corner1_idx, corner2_idx]:
                start_point = corners[corner_idx]
                direction = np.array(edge_center) - start_point
                direction = direction / np.linalg.norm(direction) * (np.linalg.norm(direction) - 0.3)
                end_point = start_point + direction

                arrow = Arrow3D(
                    start=start_point,
                    end=end_point,
                    color=WHITE,
                    thickness=0.005,
                )
                edge_arrows.add(arrow)

            self.play(
                Create(edge_center_dot),
                *[Create(arrow) for arrow in edge_arrows],
                run_time=1.25
            )

        self.wait(1)

#        # Define faces and their centers
#        faces = [
#            # Front, Back, Left, Right, Top, Bottom
#            ([1, 3, 5, 7], [0, 0, 2]),
#            ([0, 2, 4, 6], [0, 0, -2]),
#            ([4, 5, 6, 7], [2, 0, 0]),
#            ([0, 1, 2, 3], [-2, 0, 0]),
#            ([2, 3, 6, 7], [0, 2, 0]),
#            ([0, 1, 4, 5], [0, -2, 0])
#        ]
#
#        # Store face centers and their colors
#        face_center_colors = {}
#        face_center_points = {}  # Store actual face center points
#
#        # Process each face
#        for face_corners_idx, face_center in faces:
#            face_colors = [corner_colors[i] for i in face_corners_idx]
#            face_center_color = average_color(*face_colors)
#            face_center_dot = Dot3D(point=face_center, radius=0.1, color=face_center_color)
#
#            face_center_colors[tuple(face_center)] = face_center_color
#            face_center_points[tuple(face_center)] = np.array(face_center)  # Store the point
#
#            face_arrows = VGroup()
#            for corner_idx in face_corners_idx:
#                start_point = corners[corner_idx]
#                direction = np.array(face_center) - start_point
#                direction = direction / np.linalg.norm(direction) * (np.linalg.norm(direction) - 0.3)
#                end_point = start_point + direction
#
#                arrow = Arrow3D(
#                    start=start_point,
#                    end=end_point,
#                    color=WHITE,
#                    thickness=0.01,
#                )
#                face_arrows.add(arrow)
#
#            self.play(
#                Create(face_center_dot),
#                *[Create(arrow) for arrow in face_arrows],
#                run_time=1.33
#            )
#
#        self.wait(3)
