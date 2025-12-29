#!/usr/bin/env python3
"""
Repair operator for modifying waypoints to cover missing pairs.

This module provides gentle repair operations that modify existing waypoints
to make missing disk pairs touch, without adding new waypoints or increasing
dimensionality.
"""

import numpy as np
import sys

sys.path.insert(0, '/home/niplav/proj/site/code/champagne')
from vectorized_fitness import (
    check_touching_at_waypoints_vectorized,
    build_full_trajectory,
    check_path_collisions_vectorized,
    check_waypoint_overlaps_vectorized
)

# =============================================================================
# GEOMETRY FUNCTIONS
# =============================================================================

def compute_touching_positions(pos_i, pos_j, touch_distance):
    """
    Compute new positions for disks i and j to make them touch.

    Strategy: Move both disks toward their midpoint by equal amounts
    until they're exactly touch_distance apart.

    Args:
        pos_i: Current position of disk i (shape: (2,))
        pos_j: Current position of disk j (shape: (2,))
        touch_distance: Target distance (2 * radius)

    Returns:
        (new_pos_i, new_pos_j): New positions that are exactly touch_distance apart
    """
    direction = pos_j - pos_i
    current_dist = np.linalg.norm(direction)

    # Edge case: disks at same position
    if current_dist < 1e-9:
        # Place them at random direction, touching distance apart
        angle = np.random.uniform(0, 2*np.pi)
        direction_normalized = np.array([np.cos(angle), np.sin(angle)])
    else:
        direction_normalized = direction / current_dist

    # Midpoint between current positions
    midpoint = (pos_i + pos_j) / 2.0

    # Place disks at touch_distance/2 on either side of midpoint
    half_touch = touch_distance / 2.0
    new_pos_i = midpoint - half_touch * direction_normalized
    new_pos_j = midpoint + half_touch * direction_normalized

    return new_pos_i, new_pos_j


def pair_idx_to_disks(pair_idx, n_disks):
    """
    Convert lexicographic pair index to (i, j).

    Pairs are indexed: (0,1), (0,2), ..., (0,n-1), (1,2), ..., (n-2,n-1)

    Args:
        pair_idx: Pair index in lexicographic order
        n_disks: Number of disks

    Returns:
        (i, j): Disk indices
    """
    count = 0
    for i in range(n_disks):
        for j in range(i+1, n_disks):
            if count == pair_idx:
                return i, j
            count += 1
    raise ValueError(f"Invalid pair_idx {pair_idx} for n_disks {n_disks}")

# =============================================================================
# VERIFICATION FUNCTIONS
# =============================================================================

def verify_creates_meet(waypoints, w, pair_i, pair_j, touch_distance, tolerance=0.05):
    """
    Verify that pair (i,j) touches at waypoint w.

    Args:
        waypoints: Modified waypoints array (n_waypoints, n_disks, 2)
        w: Waypoint index
        pair_i, pair_j: Disk indices
        touch_distance: 2 * radius
        tolerance: Acceptable distance error

    Returns:
        bool: True if pair touches at waypoint w
    """
    pos_i = waypoints[w, pair_i]
    pos_j = waypoints[w, pair_j]
    dist = np.linalg.norm(pos_i - pos_j)

    return abs(dist - touch_distance) < tolerance

def verify_no_new_collisions(waypoints_original, waypoints_modified,
                             w, initial_positions, touch_distance):
    """
    Verify modification doesn't create new collisions.

    Uses existing optimized collision detection from vectorized_fitness.py.
    Checks entire trajectory (simpler than checking only affected segments).

    Args:
        waypoints_original: Original waypoints before modification
        waypoints_modified: Modified waypoints
        w: Modified waypoint index (unused, kept for API compatibility)
        initial_positions: Starting positions
        touch_distance: 2 * radius

    Returns:
        bool: True if no new collisions introduced
    """
    # Build full trajectories
    full_traj_orig = build_full_trajectory(waypoints_original, initial_positions)
    full_traj_mod = build_full_trajectory(waypoints_modified, initial_positions)

    # Check collisions on full trajectories using existing optimized code
    collision_orig = check_path_collisions_vectorized(full_traj_orig, touch_distance)
    collision_mod = check_path_collisions_vectorized(full_traj_mod, touch_distance)

    # Check waypoint overlaps using existing optimized code
    overlap_orig = check_waypoint_overlaps_vectorized(waypoints_original, touch_distance)
    overlap_mod = check_waypoint_overlaps_vectorized(waypoints_modified, touch_distance)

    # Accept if no new collisions or overlaps
    tolerance = 1e-6
    return (collision_mod <= collision_orig + tolerance and
            overlap_mod <= overlap_orig + tolerance)

def verify_no_removed_meets(waypoints_original, waypoints_modified,
                            touch_distance, tolerance=0.05):
    """
    Verify that no previously touching pairs have been broken.

    Args:
        waypoints_original: Original waypoints
        waypoints_modified: Modified waypoints
        touch_distance: 2 * radius
        tolerance: Touching tolerance

    Returns:
        bool: True if all original touching pairs still touch
    """
    touch_dist_sq = touch_distance * touch_distance

    # Get touching pairs in original
    touching_mask_orig = check_touching_at_waypoints_vectorized(
        waypoints_original, touch_dist_sq, tolerance
    )

    # Get touching pairs in modified
    touching_mask_mod = check_touching_at_waypoints_vectorized(
        waypoints_modified, touch_dist_sq, tolerance
    )

    # Verify: all bits set in original are still set in modified
    return (touching_mask_orig & touching_mask_mod) == touching_mask_orig

# =============================================================================
# CORE REPAIR FUNCTIONS
# =============================================================================

def try_modify_waypoint(waypoints, w, pair_idx, ch):
    """
    Try modifying waypoint w to make pair_idx touch.

    Args:
        waypoints: Current waypoints (n_waypoints, n_disks, 2)
        w: Waypoint index to modify
        pair_idx: Pair index in lexicographic order
        ch: Choreography instance

    Returns:
        (success, modified_waypoints) tuple
        - success: bool indicating if modification was valid
        - modified_waypoints: Modified waypoints if success, else original
    """
    n_disks = ch.n
    touch_distance = 2 * ch.radius

    # Convert pair_idx to (i, j)
    pair_i, pair_j = pair_idx_to_disks(pair_idx, n_disks)

    # Create modified copy
    waypoints_modified = waypoints.copy()

    # Get current positions
    pos_i = waypoints[w, pair_i]
    pos_j = waypoints[w, pair_j]

    # Compute touching positions
    new_pos_i, new_pos_j = compute_touching_positions(pos_i, pos_j, touch_distance)

    # Apply modification
    waypoints_modified[w, pair_i] = new_pos_i
    waypoints_modified[w, pair_j] = new_pos_j

    # Verification checks
    # Check A: Creates new meet
    if not verify_creates_meet(waypoints_modified, w, pair_i, pair_j,
                               touch_distance):
        return False, waypoints

    # Check B: No new collisions
    if not verify_no_new_collisions(waypoints, waypoints_modified, w,
                                     ch.initial_positions, touch_distance):
        return False, waypoints

    # Check C: No removed meets
    if not verify_no_removed_meets(waypoints, waypoints_modified,
                                    touch_distance):
        return False, waypoints

    return True, waypoints_modified

def repair_single_pair(waypoints, missing_pair_idx, ch):
    """
    Try to repair a single missing pair by modifying waypoints.

    Strategy: Try each waypoint in random order until one succeeds.

    Args:
        waypoints: Current waypoints (n_waypoints, n_disks, 2)
        missing_pair_idx: Index of missing pair
        ch: Choreography instance

    Returns:
        (success, modified_waypoints) tuple
    """
    n_waypoints = waypoints.shape[0]

    # Try each waypoint in random order (to avoid bias)
    waypoint_order = np.random.permutation(n_waypoints)

    for w in waypoint_order:
        success, modified = try_modify_waypoint(waypoints, w, missing_pair_idx, ch)
        if success:
            return True, modified

    # No waypoint modification succeeded
    return False, waypoints

def gentle_repair_population(solutions, n_waypoints, n_disks, ch, repair_rate=0.5, verbose=False):
    """
    Apply gentle repair to a population of solutions.

    For each solution (with probability repair_rate):
    1. Identify missing pairs
    2. Try to fix ONE random missing pair
    3. Accept modification if successful

    Args:
        solutions: List of flattened solution vectors
        n_waypoints: Number of waypoints
        n_disks: Number of disks
        ch: Choreography instance
        repair_rate: Fraction of population to attempt repair on
        verbose: Print diagnostic information

    Returns:
        List of solutions (some potentially repaired)
    """
    n_solutions = len(solutions)
    n_to_repair = int(n_solutions * repair_rate)

    if n_to_repair == 0:
        return solutions

    # Randomly select solutions to repair (skip first - it's our best)
    indices_to_repair = np.random.choice(
        range(1, n_solutions),
        size=min(n_to_repair, n_solutions - 1),
        replace=False
    )

    touch_distance = 2 * ch.radius
    touch_dist_sq = touch_distance * touch_distance
    n_pairs = n_disks * (n_disks - 1) // 2

    repaired_count = 0
    total_missing = 0
    attempt_count = 0

    for idx in indices_to_repair:
        solution = solutions[idx].copy()
        waypoints = solution.reshape((n_waypoints, n_disks, 2))

        # Get touching pairs bitmask
        touching_mask = check_touching_at_waypoints_vectorized(
            waypoints, touch_dist_sq, 0.05
        )

        # Extract missing pairs
        missing_pairs = []
        for pair_idx in range(n_pairs):
            if not (touching_mask & (1 << pair_idx)):
                missing_pairs.append(pair_idx)

        # If no missing pairs, skip
        if len(missing_pairs) == 0:
            continue

        total_missing += len(missing_pairs)
        attempt_count += 1

        # Try to fix ONE random missing pair (gentle repair)
        target_pair = np.random.choice(missing_pairs)

        success, repaired_waypoints = repair_single_pair(waypoints, target_pair, ch)

        if success:
            solutions[idx] = repaired_waypoints.flatten()
            repaired_count += 1

    if verbose and attempt_count > 0:
        avg_missing = total_missing / attempt_count
        success_rate = repaired_count / attempt_count * 100
        print(f"  → Repair: {repaired_count}/{attempt_count} succeeded ({success_rate:.1f}%), avg {avg_missing:.1f} missing pairs")

    return solutions
