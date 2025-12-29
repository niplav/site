#!/usr/bin/env python3
"""
Initialization strategies for n disks.

Creates a triplet sequence that covers all pairs, then simulates
collision-free choreography to produce initial waypoints for CMA-ES.
"""

import numpy as np
from itertools import combinations
import sys
sys.path.insert(0, '/home/niplav/proj/site/code/champagne')
from choreography import Choreography


def find_triplet_cover(n_disks):
    """
    Find a sequence of triplets that covers all pairs.

    Uses greedy set cover: repeatedly pick triplet that covers most uncovered pairs.
    """
    # All pairs that need to be covered
    all_pairs = set(combinations(range(n_disks), 2))
    covered_pairs = set()
    triplet_sequence = []

    while covered_pairs != all_pairs:
        best_triplet = None
        best_new_pairs = 0

        # Try all possible triplets
        for triplet in combinations(range(n_disks), 3):
            # Pairs covered by this triplet
            triplet_pairs = set(combinations(triplet, 2))
            new_pairs = triplet_pairs - covered_pairs

            if len(new_pairs) > best_new_pairs:
                best_new_pairs = len(new_pairs)
                best_triplet = triplet

        if best_triplet is None:
            break

        triplet_sequence.append(best_triplet)
        covered_pairs.update(combinations(best_triplet, 2))

    return triplet_sequence


def simulate_choreography(n_disks, radius=0.3, initial_distance=3.0, triplet_sequence=None):
    """
    Outer pair first strategy: minimize simultaneous movement.

    Strategy for each triplet (a, b, c):
    1. Find the two disks that are farthest apart (the "outer pair")
    2. Move them to meet at their midpoint, forming a pair
    3. Move the third disk to complete the triplet
    4. Move all three back home sequentially

    This reduces collisions by having fewer disks move simultaneously.

    Returns: (waypoints, path_length)
    """
    ch = Choreography(n=n_disks, radius=radius, initial_distance=initial_distance)

    if triplet_sequence is None:
        triplet_sequence = find_triplet_cover(n_disks)

    triplet_r = ch.triplet_radius()

    configs = []
    current_state = ch.initial_positions.copy()

    for triplet in triplet_sequence:
        # Find the two disks that are farthest apart
        triplet_list = list(triplet)
        max_dist = 0
        outer_pair = None
        middle_disk = None

        for i in range(3):
            for j in range(i + 1, 3):
                dist = np.linalg.norm(
                    ch.initial_positions[triplet_list[i]] -
                    ch.initial_positions[triplet_list[j]]
                )
                if dist > max_dist:
                    max_dist = dist
                    outer_pair = (triplet_list[i], triplet_list[j])
                    middle_disk = triplet_list[3 - i - j]  # The remaining one

        # KEY INSIGHT: Meeting point on radial line through middle disk's home
        # This allows middle disk to move straight inward without crossing
        middle_home = ch.initial_positions[middle_disk]
        meeting_angle = np.arctan2(middle_home[1], middle_home[0])

        # Place pair meeting point on this radial line at triplet_radius from origin
        pair_center = np.array([
            triplet_r * np.cos(meeting_angle),
            triplet_r * np.sin(meeting_angle)
        ])

        # Position the pair: 2 disks separated by 2*radius, perpendicular to radial line
        pair_separation = 2 * radius
        # Perpendicular direction (rotate 90 degrees counterclockwise)
        perp_angle = meeting_angle + np.pi / 2
        left_position = pair_center + (pair_separation / 2) * np.array([np.cos(perp_angle), np.sin(perp_angle)])
        right_position = pair_center - (pair_separation / 2) * np.array([np.cos(perp_angle), np.sin(perp_angle)])

        # Determine which disk is on which side of the middle disk's radial line
        # Use cross product to determine left/right
        def is_left_of_radial_line(disk_pos, radial_angle):
            """Check if disk is on the left (counterclockwise) side of radial line."""
            disk_angle = np.arctan2(disk_pos[1], disk_pos[0])
            # Normalize angle difference to [-pi, pi]
            angle_diff = (disk_angle - radial_angle + np.pi) % (2 * np.pi) - np.pi
            return angle_diff > 0

        disk0_is_left = is_left_of_radial_line(ch.initial_positions[outer_pair[0]], meeting_angle)

        # Assign positions so disks don't cross the radial line
        if disk0_is_left:
            pos0, pos1 = left_position, right_position
        else:
            pos0, pos1 = right_position, left_position

        # Compute middle disk's final position to complete triplet
        middle_pos = pair_center + (pair_separation * np.sqrt(3) / 2) * np.array([
            np.cos(meeting_angle), np.sin(meeting_angle)
        ])

        # Step 1: ALL THREE disks move to meet simultaneously (no crossing!)
        config = current_state.copy()
        config[outer_pair[0]] = pos0
        config[outer_pair[1]] = pos1
        config[middle_disk] = middle_pos
        configs.append(config.copy())

        # Step 2: ALL THREE disks move back home simultaneously
        config = ch.initial_positions.copy()
        configs.append(config.copy())

        current_state = ch.initial_positions.copy()

    # Convert to numpy array
    waypoints = np.array(configs)
    path_length = ch.total_path_length(waypoints)

    return waypoints, path_length
