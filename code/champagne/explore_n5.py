#!/usr/bin/env python3
"""
Explore different choreographies for n=5 champagne toasting.

Try various heuristic approaches inspired by the n=3, n=4 solutions.
"""

import numpy as np
from typing import List, Tuple


class Choreography:
    """Represents a sequence of configurations for the champagne toasting problem."""

    def __init__(self, n: int = 5, radius: float = 0.3):
        self.n = n
        self.radius = radius

        # Initial positions: regular n-gon
        angles = np.linspace(0, 2*np.pi, n, endpoint=False) + np.pi/2
        self.initial_positions = np.column_stack([
            np.cos(angles),
            np.sin(angles)
        ]) * 3.0

    def distance(self, pos1, pos2):
        return np.linalg.norm(pos1 - pos2)

    def touching_distance(self):
        """Distance between centers when two disks touch."""
        return 2 * self.radius

    def triplet_radius(self):
        """Radius of circumcircle for three mutually touching disks."""
        return (2 * self.radius) / np.sqrt(3)

    def check_pairs_touching(self, config: np.ndarray) -> List[Tuple[int, int]]:
        """Return list of pairs that are touching in this configuration."""
        touching = []
        tol = 0.05
        target_dist = self.touching_distance()

        for i in range(self.n):
            for j in range(i+1, self.n):
                dist = self.distance(config[i], config[j])
                if abs(dist - target_dist) < tol:
                    touching.append((i, j))

        return touching

    def total_path_length(self, configs: List[np.ndarray]) -> float:
        """Calculate total path length through a sequence of configurations."""
        total = 0.0

        # From initial to first config
        for i in range(self.n):
            total += self.distance(self.initial_positions[i], configs[0][i])

        # Between configs
        for k in range(len(configs) - 1):
            for i in range(self.n):
                total += self.distance(configs[k][i], configs[k+1][i])

        # From last config back to initial
        for i in range(self.n):
            total += self.distance(configs[-1][i], self.initial_positions[i])

        return total

    def get_all_touching_pairs(self, configs: List[np.ndarray]) -> set:
        """Get set of all pairs that touch at some point."""
        all_touching = set()
        for config in configs:
            pairs = self.check_pairs_touching(config)
            all_touching.update(pairs)
        return all_touching


def choreography_1_all_to_center():
    """Strategy: All disks move to center in a tight cluster."""
    ch = Choreography(n=5)

    # Try to pack 5 disks as tightly as possible
    # One in center, four around it
    configs = []

    # Config 1: Pentagon contracted to touching distance
    scale = ch.touching_distance() / ch.distance(ch.initial_positions[0], ch.initial_positions[1])
    config1 = ch.initial_positions * scale
    configs.append(config1)

    path_length = ch.total_path_length(configs)
    all_touching = ch.get_all_touching_pairs(configs)

    return configs, path_length, all_touching


def choreography_2_triplets():
    """Strategy: Form overlapping triplets to cover all pairs."""
    ch = Choreography(n=5)

    configs = []

    # Triplet 1: disks 0, 1, 2
    config1 = ch.initial_positions.copy()
    # Move 0, 1, 2 to form a triplet at origin
    triplet_r = ch.triplet_radius()
    angles = [90, 210, 330]  # degrees
    for idx, (disk_id, angle) in enumerate(zip([0, 1, 2], angles)):
        angle_rad = np.radians(angle)
        config1[disk_id] = np.array([
            triplet_r * np.cos(angle_rad),
            triplet_r * np.sin(angle_rad)
        ])
    configs.append(config1)

    # Triplet 2: disks 0, 3, 4
    config2 = ch.initial_positions.copy()
    for idx, (disk_id, angle) in enumerate(zip([0, 3, 4], angles)):
        angle_rad = np.radians(angle)
        config2[disk_id] = np.array([
            triplet_r * np.cos(angle_rad),
            triplet_r * np.sin(angle_rad)
        ])
    configs.append(config2)

    triplet_configs = [
        [0, 1, 2],
        [0, 3, 4],
        [1, 2, 3],
        [2, 3, 4],
        [0, 1, 4]
    ]

    configs = []
    for triplet in triplet_configs:
        config = ch.initial_positions.copy()
        for idx, disk_id in enumerate(triplet):
            angle = angles[idx]
            angle_rad = np.radians(angle)
            config[disk_id] = np.array([
                triplet_r * np.cos(angle_rad),
                triplet_r * np.sin(angle_rad)
            ])
        configs.append(config)

    path_length = ch.total_path_length(configs)
    all_touching = ch.get_all_touching_pairs(configs)

    return configs, path_length, all_touching
