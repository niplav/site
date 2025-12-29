#!/usr/bin/env python3
"""
Common utilities for champagne toasting optimization.
"""

import numpy as np
from dataclasses import dataclass
import json
import os


@dataclass
class Solution:
    """Represents a solution with waypoints for each disk."""
    waypoints: np.ndarray
    fitness: float = float('inf')


def load_and_expand_best_solution(filename, target_waypoints):
    """
    Load a solution from JSON and expand it to target number of waypoints.

    For expansion: duplicate the middle waypoint to create a 'no-op' action.
    E.g., 4 waypoints [0,1,2,3] -> 5 waypoints [0,1,2,2,3]
    """
    if not os.path.exists(filename):
        return None

    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        waypoints = np.array(data['waypoints'])
        current_waypoints = waypoints.shape[0]

        if current_waypoints == target_waypoints:
            return waypoints
        elif current_waypoints < target_waypoints:
            # Expand by duplicating middle waypoint(s)
            expanded = []
            mid_idx = current_waypoints // 2

            for i in range(current_waypoints):
                expanded.append(waypoints[i])
                # Duplicate middle waypoint
                if i == mid_idx:
                    for _ in range(target_waypoints - current_waypoints):
                        expanded.append(waypoints[i].copy())

            return np.array(expanded)
        else:
            # Shrink by removing middle waypoints
            indices = np.linspace(0, current_waypoints - 1, target_waypoints).astype(int)
            return waypoints[indices]

    except Exception as e:
        print(f"Warning: Could not load {filename}: {e}")
        return None


def save_solution(waypoints, ch, n_waypoints, penalty_alpha, filename):
    """Save a solution to JSON file."""
    from vectorized_fitness import (
        check_path_collisions_vectorized,
        build_full_trajectory,
        evaluate_fitness_vectorized
    )

    n_disks = ch.n
    configs = [waypoints[i] for i in range(n_waypoints)]
    all_touching = ch.get_all_touching_pairs(configs)
    path_length = ch.total_path_length(waypoints)

    full_traj = build_full_trajectory(waypoints, ch.initial_positions)
    path_penalty = check_path_collisions_vectorized(full_traj, 2 * ch.radius)

    fitness = evaluate_fitness_vectorized(
        waypoints, ch.initial_positions, ch.radius,
        penalty_alpha=penalty_alpha
    )

    n_pairs = n_disks * (n_disks - 1) // 2

    trajectories = {
        'metadata': {
            'n_disks': n_disks,
            'n_waypoints': n_waypoints,
            'path_length': float(path_length),
            'fitness': float(fitness),
            'all_pairs_touch': len(all_touching) == n_pairs,
            'has_path_collisions': path_penalty > 0.01,
            'path_collision_penalty': float(path_penalty),
        },
        'initial_positions': ch.initial_positions.tolist(),
        'waypoints': waypoints.tolist(),
        'disk_trajectories': {}
    }

    for disk_id in range(n_disks):
        trajectory = [ch.initial_positions[disk_id].tolist()]
        for w in range(n_waypoints):
            trajectory.append(waypoints[w, disk_id].tolist())
        trajectory.append(ch.initial_positions[disk_id].tolist())

        disk_dist = 0.0
        for i in range(len(trajectory) - 1):
            disk_dist += np.linalg.norm(np.array(trajectory[i + 1]) - np.array(trajectory[i]))

        trajectories['disk_trajectories'][str(disk_id)] = {
            'path': trajectory,
            'distance': float(disk_dist)
        }

    with open(filename, 'w') as f:
        json.dump(trajectories, f, indent=2)


def load_best_known_fitness(filename):
    """Load the fitness from best_1.json if it exists."""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                return data['metadata']['fitness']
        except:
            pass
    return float('inf')
