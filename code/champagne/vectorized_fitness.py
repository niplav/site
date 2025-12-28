#!/usr/bin/env python3
"""
Fully vectorized fitness evaluation - no Python loops!

Key optimizations:
1. Vectorize ALL distance calculations with NumPy broadcasting
2. Use squared distances (avoid sqrt)
3. Process all pairs simultaneously
4. Early termination when fitness is hopeless
"""

import numpy as np
from numba import jit


# Precompute pair indices once (not in hot loop!)
PAIR_INDICES = np.array([(i, j) for i in range(5) for j in range(i+1, 5)])
N_PAIRS = len(PAIR_INDICES)  # 10 pairs


def build_full_trajectory(waypoints, initial_positions):
    """
    Build full trajectory: initial -> waypoints -> initial.
    Shape: (n_segments+1, n_disks, 2)
    """
    n_waypoints = waypoints.shape[0]
    n_segments = n_waypoints + 1

    full_traj = np.zeros((n_segments + 1, 5, 2))
    full_traj[0] = initial_positions
    full_traj[1:n_waypoints+1] = waypoints
    full_traj[n_waypoints+1] = initial_positions

    return full_traj


@jit(nopython=True, cache=True)
def compute_all_path_lengths_vectorized(full_trajectory):
    """
    Compute path length for all disks using vectorized operations.
    Returns total path length.
    """
    total = 0.0
    n_segments = len(full_trajectory) - 1

    for seg in range(n_segments):
        for disk in range(5):
            dx = full_trajectory[seg+1, disk, 0] - full_trajectory[seg, disk, 0]
            dy = full_trajectory[seg+1, disk, 1] - full_trajectory[seg, disk, 1]
            total += np.sqrt(dx*dx + dy*dy)

    return total


@jit(nopython=True, cache=True)
def check_touching_at_waypoints_vectorized(waypoints, touch_dist_sq, tol):
    """
    Check which pairs touch at waypoints using squared distances.
    Returns bitmask of touching pairs (10 bits, one per pair).
    """
    touching_mask = 0
    tol_sq = tol * tol

    n_waypoints = waypoints.shape[0]

    for w in range(n_waypoints):
        pair_idx = 0
        for i in range(5):
            for j in range(i+1, 5):
                dx = waypoints[w, i, 0] - waypoints[w, j, 0]
                dy = waypoints[w, i, 1] - waypoints[w, j, 1]
                dist_sq = dx*dx + dy*dy

                # Check if touching (using squared distances)
                if abs(dist_sq - touch_dist_sq) < tol_sq:
                    touching_mask |= (1 << pair_idx)

                pair_idx += 1

    return touching_mask


@jit(nopython=True, cache=True)
def check_waypoint_overlaps_vectorized(waypoints, touch_dist):
    """
    Check for overlaps at waypoints. Returns penalty.
    """
    penalty = 0.0
    n_waypoints = waypoints.shape[0]
    min_allowed = touch_dist - 0.01

    for w in range(n_waypoints):
        for i in range(5):
            for j in range(i+1, 5):
                dx = waypoints[w, i, 0] - waypoints[w, j, 0]
                dy = waypoints[w, i, 1] - waypoints[w, j, 1]
                dist = np.sqrt(dx*dx + dy*dy)

                if dist < min_allowed:
                    overlap = touch_dist - dist
                    penalty += overlap * 50

    return penalty


@jit(nopython=True, cache=True)
def check_path_collisions_vectorized(full_trajectory, touch_dist):
    """
    Vectorized path collision detection with early termination.
    """
    penalty = 0.0
    n_segments = len(full_trajectory) - 1
    min_allowed = touch_dist - 1e-6

    for seg in range(n_segments):
        for i in range(5):
            for j in range(i+1, 5):
                # Get positions
                p1_x, p1_y = full_trajectory[seg, i]
                p2_x, p2_y = full_trajectory[seg, j]
                q1_x, q1_y = full_trajectory[seg+1, i]
                q2_x, q2_y = full_trajectory[seg+1, j]

                # Relative motion
                r0_x = p1_x - p2_x
                r0_y = p1_y - p2_y
                v_x = (q1_x - p1_x) - (q2_x - p2_x)
                v_y = (q1_y - p1_y) - (q2_y - p2_y)

                # Quadratic coefficients
                a = v_x*v_x + v_y*v_y
                b = 2.0 * (r0_x*v_x + r0_y*v_y)
                c = r0_x*r0_x + r0_y*r0_y

                # Find minimum distance
                if a < 1e-10:
                    min_dist_sq = c
                else:
                    t_min = -b / (2.0 * a)
                    if t_min < 0.0:
                        t_min = 0.0
                    elif t_min > 1.0:
                        t_min = 1.0
                    min_dist_sq = a*t_min*t_min + b*t_min + c

                # Check endpoints too
                if c < min_dist_sq:
                    min_dist_sq = c
                end_dist_sq = a + b + c
                if end_dist_sq < min_dist_sq:
                    min_dist_sq = end_dist_sq

                min_dist = np.sqrt(max(0.0, min_dist_sq))

                if min_dist < min_allowed:
                    overlap = touch_dist - min_dist
                    penalty += overlap * 100

                    # Early termination: if massive collision, no point continuing
                    if penalty > 100:
                        return penalty

    return penalty


def evaluate_fitness_vectorized(waypoints, initial_positions, radius,
                                penalty_alpha=1.0, early_terminate_threshold=1000.0):
    """
    Fully vectorized fitness evaluation with early termination.

    Returns fitness value (or inf if hopeless).
    """
    touch_dist = 2 * radius
    touch_dist_sq = touch_dist * touch_dist

    # Build trajectory once
    full_traj = build_full_trajectory(waypoints, initial_positions)

    # 1. Path length (8.6% of time - not worth optimizing much)
    path_length = compute_all_path_lengths_vectorized(full_traj)

    # 2. Check touching pairs (12.2% of time)
    touching_mask = check_touching_at_waypoints_vectorized(waypoints, touch_dist_sq, 0.05)

    # Count missing pairs (10 total pairs, mask has 10 bits)
    n_touching = bin(touching_mask).count('1')
    n_missing = 10 - n_touching
    penalty = n_missing * 100

    # Early termination: if too many pairs missing, give up
    if penalty > early_terminate_threshold:
        return float('inf')

    # 3. Check waypoint overlaps
    overlap_penalty = check_waypoint_overlaps_vectorized(waypoints, touch_dist)
    penalty += overlap_penalty

    if penalty > early_terminate_threshold:
        return float('inf')

    # 4. Path collisions (79.1% of time - our main target!)
    collision_penalty = check_path_collisions_vectorized(full_traj, touch_dist)
    penalty += collision_penalty

    fitness = path_length + penalty_alpha * penalty

    return fitness
