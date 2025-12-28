#!/usr/bin/env python3
"""
Ultra-greedy: Try to minimize total disk movements by finding
better triplet orderings and keeping as many disks stationary as possible.
"""

import numpy as np
from itertools import permutations
import sys
sys.path.insert(0, '/home/niplav/proj/site/code/champagne')
from explore_n5 import Choreography


def simulate_choreography_with_memory(triplet_sequence, verbose=False):
    """
    Simulate a choreography where disks stay in place if they're
    reused in consecutive triplets.

    Returns: (configs, path_length, detailed_movements)
    """
    ch = Choreography(n=5)
    triplet_r = ch.triplet_radius()
    angles = [90, 210, 330]

    # Track current position of each disk
    current_positions = ch.initial_positions.copy()
    configs = []
    movements = {i: [] for i in range(5)}

    for t_idx, triplet in enumerate(triplet_sequence):
        config = current_positions.copy()

        # Figure out triplet positions
        triplet_positions = {}
        for idx, disk_id in enumerate(triplet):
            angle_rad = np.radians(angles[idx])
            pos = np.array([
                triplet_r * np.cos(angle_rad),
                triplet_r * np.sin(angle_rad)
            ])
            triplet_positions[disk_id] = pos

        # Move disks in this triplet to their positions
        for disk_id in triplet:
            old_pos = current_positions[disk_id]
            new_pos = triplet_positions[disk_id]
            dist = np.linalg.norm(new_pos - old_pos)

            if dist > 0.01:
                movements[disk_id].append((t_idx, 'move', dist))

            config[disk_id] = new_pos
            current_positions[disk_id] = new_pos

        # Disks NOT in this triplet: check if they should return home
        # Strategy: only send home if not in next triplet
        for disk_id in range(5):
            if disk_id in triplet:
                continue

            # Check if this disk is in the next triplet
            will_be_used_next = (t_idx + 1 < len(triplet_sequence) and
                                disk_id in triplet_sequence[t_idx + 1])

            if not will_be_used_next:
                # Send home
                old_pos = current_positions[disk_id]
                home_pos = ch.initial_positions[disk_id]
                dist = np.linalg.norm(home_pos - old_pos)

                if dist > 0.01:
                    movements[disk_id].append((t_idx, 'home', dist))
                    config[disk_id] = home_pos
                    current_positions[disk_id] = home_pos

        configs.append(config)

    # Final: send everyone home
    for disk_id in range(5):
        dist = np.linalg.norm(ch.initial_positions[disk_id] - current_positions[disk_id])
        if dist > 0.01:
            movements[disk_id].append((len(triplet_sequence), 'home', dist))

    path_length = ch.total_path_length(configs)

    return configs, path_length, movements
