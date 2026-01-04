#!/usr/bin/env python3
"""
Adaptive Penalty Solver for Champagne Toasting Problem

This file serves two purposes:
1. LIBRARY: Exports compute_adaptive_penalty_jit for use in cma_optimize.py
2. STANDALONE: Provides AdaptivePenaltySolver class for direct optimization

Uses trajectory-aware adaptive penalties:
- Pairs that haven't touched: quadratic distance penalty + exponential intersection penalty
- Pairs that have touched: only exponential intersection penalty
- Touch state determined by smooth sigmoid function (differentiable!)
"""

import numpy as np
import json
from scipy.optimize import minimize
from numba import jit
from vectorized_fitness import (
    build_full_trajectory,
    compute_all_path_lengths_vectorized
)

# ============================================================================
# USER-ADJUSTABLE PARAMETERS (for standalone mode)
# ============================================================================

N_DISKS = 8
DISK_RADIUS = 0.3
POLYGON_RADIUS = 3.0
N_WAYPOINTS = 12
MAX_ITER = 1000000  # Increased for longer optimization runs
VERBOSE = True
SAVE_AS_BEST = True

# Convergence tolerance (smaller = tighter convergence, approaching machine precision)
FTOL = 1e-15  # Function tolerance (default: 1e-6, machine epsilon ~2e-16)
GTOL = 1e-12  # Gradient tolerance (default: 1e-5)

# Penalty weights
TOUCH_SHARPNESS = 10.0  # Controls sigmoid transition smoothness
STATIONARY_PENALTY_SCALE = 10.0  # Collisions AT waypoints (harsh - easy to fix)
PATH_PENALTY_SCALE = 10.0  # Collisions BETWEEN waypoints (gentler - harder to avoid)
DISTANCE_PENALTY_SCALE = 1.0  # Quadratic distance penalty - higher = stronger attraction

# Initialization strategy: 'center_convergence', 'non_moving', or 'from_best'
INIT_STRATEGY = 'center_convergence'

# Optimizer parameters
INITIAL_TRUST_RADIUS = 10.0  # Initial trust region radius for exploration
VERBOSE_FREQ = 100  # Print progress every N evaluations

# Validation thresholds (shared with cma_optimize.py)
COLLISION_VALIDITY_THRESHOLD = 0.01  # Solution is valid if penalties < this value

# Initialization parameters
MEETING_RADIUS_MULTIPLIER = 2.0  # Meeting circle radius = this × disk_radius
CENTER_CONVERGENCE_MIDPOINT = 0.5  # t-value where disks reach center in initialization

# ============================================================================
# LIBRARY FUNCTIONS (exported to cma_optimize.py)
# ============================================================================
# These functions are imported and used by cma_optimize.py:
#   - compute_adaptive_penalty_jit: Core penalty computation
#   - compute_segment_min_distance: Helper for segment-wise distance (called by above)
#   - compute_trajectory_min_distance: Helper for trajectory-wise distance (called by above)


@jit(nopython=True, cache=True)
def compute_segment_min_distance(p1, p2, q1, q2):
    """
    Compute minimum distance between two disks moving linearly.

    p1, q1: start and end positions of disk 1
    p2, q2: start and end positions of disk 2

    Uses quadratic formula approach from vectorized_fitness.py
    """
    # Relative motion
    r0_x = p1[0] - p2[0]
    r0_y = p1[1] - p2[1]
    v_x = (q1[0] - p1[0]) - (q2[0] - p2[0])
    v_y = (q1[1] - p1[1]) - (q2[1] - p2[1])

    # Quadratic coefficients for distance² = a*t² + b*t + c
    a = v_x*v_x + v_y*v_y
    b = 2.0 * (r0_x*v_x + r0_y*v_y)
    c = r0_x*r0_x + r0_y*r0_y

    # Find minimum
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

    return np.sqrt(max(0.0, min_dist_sq))


@jit(nopython=True, cache=True)
def compute_trajectory_min_distance(full_traj, i, j):
    """
    Find minimum distance between disks i and j across entire trajectory.
    """
    n_segments = len(full_traj) - 1
    min_dist = float('inf')

    for seg in range(n_segments):
        p1 = full_traj[seg, i]
        q1 = full_traj[seg+1, i]
        p2 = full_traj[seg, j]
        q2 = full_traj[seg+1, j]

        seg_min = compute_segment_min_distance(p1, p2, q1, q2)
        if seg_min < min_dist:
            min_dist = seg_min

    return min_dist


@jit(nopython=True, cache=True)
def compute_adaptive_penalty_jit(full_traj, disk_radius, touch_sharpness,
                                  stationary_scale, path_scale, distance_scale):
    """
    Compute adaptive penalty with smooth touch indicator.

    Separates two types of collisions:
    1. STATIONARY: overlaps at waypoint positions (easy to fix, harsh penalty)
    2. PATH: overlaps between waypoints during motion (harder to avoid, gentler penalty)

    For each pair:
    1. Find minimum distance over trajectory
    2. Compute smooth touch_weight using sigmoid
    3. Apply penalties:
       - Stationary collision penalty at waypoints (quartic - very harsh)
       - Path collision penalty along segments (exponential - strong)
       - Distance penalty for pairs that haven't touched (quadratic)

    Returns: (total_penalty, stationary_penalty, path_penalty, distance_penalty)
    """
    n_disks = full_traj.shape[1]
    n_waypoints = len(full_traj)
    n_segments = n_waypoints - 1
    touch_dist = 2.0 * disk_radius

    stationary_penalty = 0.0
    path_penalty = 0.0
    distance_penalty = 0.0

    for i in range(n_disks):
        for j in range(i+1, n_disks):
            # 1. Find minimum distance over entire trajectory
            min_dist = compute_trajectory_min_distance(full_traj, i, j)

            # 2. Smooth "has touched" indicator (sigmoid)
            # touch_weight ≈ 0 if never touched, ≈ 1 if has touched
            touch_weight = 1.0 / (1.0 + np.exp(-touch_sharpness * (touch_dist - min_dist)))

            # 3A. STATIONARY collisions - check at each waypoint position
            for wp in range(n_waypoints):
                dx = full_traj[wp, i, 0] - full_traj[wp, j, 0]
                dy = full_traj[wp, i, 1] - full_traj[wp, j, 1]
                dist = np.sqrt(dx*dx + dy*dy)

                if dist < touch_dist:
                    overlap = touch_dist - dist
                    # Quartic penalty - VERY harsh for stationary overlaps
                    stationary_penalty += stationary_scale * (overlap / disk_radius)**4

            # 3B. PATH collisions - check along each segment between waypoints
            for seg in range(n_segments):
                p1 = full_traj[seg, i]
                q1 = full_traj[seg+1, i]
                p2 = full_traj[seg, j]
                q2 = full_traj[seg+1, j]

                # Find minimum distance along this segment
                dist = compute_segment_min_distance(p1, p2, q1, q2)

                # Exponential penalty for path collisions (excluding endpoints already counted)
                if dist < touch_dist:
                    # Check if this is NOT at an endpoint (already counted in stationary)
                    # We'll apply the penalty anyway and accept double-counting at endpoints
                    # (endpoints are more important to keep collision-free)
                    overlap = touch_dist - dist
                    path_penalty += path_scale * np.exp(overlap / disk_radius)

                # Quadratic distance penalty (scaled by touch_weight)
                if dist > touch_dist:
                    gap = dist - touch_dist
                    distance_penalty += distance_scale * (1.0 - touch_weight) * gap * gap

    total_penalty = stationary_penalty + path_penalty + distance_penalty
    return total_penalty, stationary_penalty, path_penalty, distance_penalty


# ============================================================================
# STANDALONE SOLVER CLASS & UTILITIES (NOT used when imported as library)
# ============================================================================
# The following code is ONLY executed when running `python adaptive_solver.py`
# NOT imported by cma_optimize.py - provides standalone optimization capability
#
# Standalone-only components:
#   - AdaptivePenaltySolver class (and all its methods)
#   - verify_solution()
#   - save_solution()
#   - main()

class AdaptivePenaltySolver:  # STANDALONE ONLY
    def __init__(self, n_disks, disk_radius, polygon_radius, n_waypoints):
        self.n_disks = n_disks
        self.disk_radius = disk_radius
        self.polygon_radius = polygon_radius
        self.n_waypoints = n_waypoints

        # Compute initial positions on regular polygon
        angles = np.linspace(0, 2*np.pi, n_disks, endpoint=False)
        self.initial_positions = polygon_radius * np.column_stack([
            np.cos(angles),
            np.sin(angles)
        ])

        # Compute all pairs
        self.all_pairs = [(i, j) for i in range(n_disks) for j in range(i+1, n_disks)]

        # Iteration counter for verbose output
        self.n_evals = 0

        # Store latest penalties for reporting
        self.last_stationary_penalty = 0.0
        self.last_path_penalty = 0.0
        self.last_distance_penalty = 0.0

    def decode_variables(self, x):
        """Convert flat array to waypoints array."""
        return x.reshape(self.n_waypoints, self.n_disks, 2)

    def encode_variables(self, waypoints):
        """Convert waypoints array to flat array."""
        return waypoints.flatten()

    def objective(self, x):
        """
        Total objective: path_length + adaptive_penalty
        """
        waypoints = self.decode_variables(x)
        full_traj = build_full_trajectory(waypoints, self.initial_positions)

        # Path length
        path_length = compute_all_path_lengths_vectorized(full_traj)

        # Adaptive penalty (returns total, stationary, path, distance components)
        total_penalty, stat_penalty, path_penalty, dist_penalty = compute_adaptive_penalty_jit(
            full_traj,
            self.disk_radius,
            TOUCH_SHARPNESS,
            STATIONARY_PENALTY_SCALE,
            PATH_PENALTY_SCALE,
            DISTANCE_PENALTY_SCALE
        )

        # Store penalties for later reporting
        self.last_stationary_penalty = stat_penalty
        self.last_path_penalty = path_penalty
        self.last_distance_penalty = dist_penalty

        total = path_length + total_penalty

        self.n_evals += 1
        if VERBOSE and self.n_evals % VERBOSE_FREQ == 0:
            print(f"Eval {self.n_evals}: path={path_length:.2f}, stat={stat_penalty:.2f}, "
                  f"path={path_penalty:.2f}, dist={dist_penalty:.2f}, total={total:.2f}")

        return total

    def initialize_center_convergence(self):
        """
        Disks converge toward small circle around center, then return.
        """
        waypoints = np.zeros((self.n_waypoints, self.n_disks, 2))

        # Angles for small circle
        angles = np.linspace(0, 2*np.pi, self.n_disks, endpoint=False)
        meeting_radius = MEETING_RADIUS_MULTIPLIER * self.disk_radius  # Small circle where disks can touch
        meeting_circle = meeting_radius * np.column_stack([
            np.cos(angles),
            np.sin(angles)
        ])

        # Interpolate: start -> meeting circle -> start
        for w in range(self.n_waypoints):
            t = (w + 1) / (self.n_waypoints + 1)
            if t <= CENTER_CONVERGENCE_MIDPOINT:
                # Going toward center
                alpha = 2 * t
                waypoints[w] = (1 - alpha) * self.initial_positions + alpha * meeting_circle
            else:
                # Returning from center
                alpha = 2 * (t - CENTER_CONVERGENCE_MIDPOINT)
                waypoints[w] = (1 - alpha) * meeting_circle + alpha * self.initial_positions

        return waypoints

    def initialize_non_moving(self):
        """
        All disks stay at initial positions (no movement).
        """
        waypoints = np.zeros((self.n_waypoints, self.n_disks, 2))
        for w in range(self.n_waypoints):
            waypoints[w] = self.initial_positions
        return waypoints

    def initialize_from_best(self, filename='best_n8_w10.json'):
        """
        Load waypoints from existing solution.
        """
        with open(filename, 'r') as f:
            data = json.load(f)

        # Extract waypoints - format is list[waypoint][disk][coordinate]
        waypoints_list = data['waypoints']

        # Convert to numpy array with shape (n_waypoints, n_disks, 2)
        waypoints = np.array(waypoints_list)

        return waypoints

    def solve(self, max_iter=MAX_ITER):
        """
        Run optimization with adaptive penalties.
        """
        # Initialize
        if INIT_STRATEGY == 'center_convergence':
            waypoints_init = self.initialize_center_convergence()
        elif INIT_STRATEGY == 'non_moving':
            waypoints_init = self.initialize_non_moving()
        elif INIT_STRATEGY == 'from_best':
            waypoints_init = self.initialize_from_best()
        else:
            raise ValueError(f"Unknown initialization strategy: {INIT_STRATEGY}")

        x0 = self.encode_variables(waypoints_init)

        if VERBOSE:
            print(f"Starting optimization with {INIT_STRATEGY} initialization")
            print(f"Initial objective: {self.objective(x0):.2f}")
            self.n_evals = 0  # Reset counter

        # Run trust-constr (most robust modern optimizer)
        result = minimize(
            self.objective,
            x0,
            method='trust-constr',
            options={
                'maxiter': max_iter,
                'gtol': GTOL,
                'xtol': FTOL,
                'verbose': 2 if VERBOSE else 0,
                'initial_tr_radius': INITIAL_TRUST_RADIUS  # Larger trust region for exploration
            }
        )

        # Decode result
        final_waypoints = self.decode_variables(result.x)
        final_traj = build_full_trajectory(final_waypoints, self.initial_positions)

        return {
            'waypoints': final_waypoints,
            'full_trajectory': final_traj,
            'path_length': compute_all_path_lengths_vectorized(final_traj),
            'success': result.success,
            'message': result.message,
            'n_iterations': result.nit
        }


def verify_solution(full_traj, disk_radius):  # STANDALONE ONLY
    """
    Verify that solution satisfies all constraints.
    (STANDALONE ONLY - not used when imported as library)
    """
    n_disks = full_traj.shape[1]
    touch_dist = 2 * disk_radius

    # Check all pairs touched
    pairs_touched = []
    min_distances = {}

    for i in range(n_disks):
        for j in range(i+1, n_disks):
            min_dist = compute_trajectory_min_distance(full_traj, i, j)
            min_distances[(i, j)] = min_dist
            pairs_touched.append(min_dist <= touch_dist)

    n_touching = sum(pairs_touched)
    n_pairs = len(pairs_touched)

    # Find minimum and colliding pairs
    overall_min = min(min_distances.values())
    colliding_pairs = [(pair, dist) for pair, dist in min_distances.items() if dist < touch_dist]

    print(f"\n{'='*60}")
    print(f"VERIFICATION")
    print(f"{'='*60}")
    print(f"Pairs touching: {n_touching}/{n_pairs}")
    print(f"Minimum distance: {overall_min:.4f} (threshold: {touch_dist:.4f})")

    if colliding_pairs:
        print(f"⚠️  {len(colliding_pairs)} COLLISION(S) DETECTED:")
        # Show worst 5 collisions
        colliding_pairs.sort(key=lambda x: x[1])
        for (i, j), dist in colliding_pairs[:5]:
            print(f"   Pair ({i},{j}): {dist:.4f} < {touch_dist:.4f} (overlap: {touch_dist - dist:.4f})")
        if len(colliding_pairs) > 5:
            print(f"   ... and {len(colliding_pairs) - 5} more")
    else:
        print(f"✓ No collisions")

    if n_touching == n_pairs:
        print(f"✓ All pairs touched!")
    else:
        print(f"✗ Missing {n_pairs - n_touching} pairs:")
        # Show which pairs didn't touch
        not_touching = [(pair, dist) for pair, dist in min_distances.items() if dist > touch_dist]
        for (i, j), dist in not_touching:
            print(f"   Pair ({i},{j}): {dist:.4f} > {touch_dist:.4f} (gap: {dist - touch_dist:.4f})")

    return n_touching == n_pairs and overall_min >= touch_dist


def save_solution(full_traj, path_length, initial_positions, all_pairs_touch, has_collisions,
                 stationary_penalty, path_penalty, filename='solution_adaptive.json'):  # STANDALONE ONLY
    """
    Save solution in format compatible with visualization.
    (STANDALONE ONLY - not used when imported as library)
    """
    n_disks = full_traj.shape[1]
    n_waypoints = len(full_traj) - 2  # Exclude initial and final positions

    # Extract waypoints (exclude first and last positions)
    waypoints_array = full_traj[1:-1, :, :]  # Shape: (n_waypoints, n_disks, 2)
    waypoints = []
    for w in range(n_waypoints):
        waypoint = [waypoints_array[w, i, :].tolist() for i in range(n_disks)]
        waypoints.append(waypoint)

    # Convert to disk_trajectories format: dict with string keys and 'path' field
    disk_trajectories = {}
    for i in range(n_disks):
        trajectory = full_traj[:, i, :].tolist()
        disk_trajectories[str(i)] = {
            'path': trajectory
        }

    data = {
        'metadata': {
            'n_disks': int(n_disks),
            'n_waypoints': int(n_waypoints),
            'path_length': float(path_length),
            'fitness': float(path_length),  # For adaptive penalty, final fitness ≈ path_length
            'all_pairs_touch': bool(all_pairs_touch),
            'has_path_collisions': bool(has_collisions),
            'stationary_collision_penalty': float(stationary_penalty),
            'path_collision_penalty': float(path_penalty),
            'total_collision_penalty': float(stationary_penalty + path_penalty),
            'solver': 'adaptive_penalty',
            'disk_radius': float(DISK_RADIUS),
            'polygon_radius': float(POLYGON_RADIUS)
        },
        'initial_positions': initial_positions.tolist(),
        'waypoints': waypoints,
        'disk_trajectories': disk_trajectories
    }

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\nSolution saved to {filename}")


def main():  # STANDALONE ONLY
    """Entry point for standalone execution (not used when imported as library)."""
    print(f"{'='*60}")
    print(f"ADAPTIVE PENALTY SOLVER")
    print(f"{'='*60}")
    print(f"Problem: {N_DISKS} disks, radius {DISK_RADIUS}")
    print(f"Waypoints: {N_WAYPOINTS}")
    print(f"Initialization: {INIT_STRATEGY}")
    print(f"{'='*60}\n")

    solver = AdaptivePenaltySolver(N_DISKS, DISK_RADIUS, POLYGON_RADIUS, N_WAYPOINTS)
    result = solver.solve(max_iter=MAX_ITER)

    print(f"\n{'='*60}")
    print(f"OPTIMIZATION COMPLETE")
    print(f"{'='*60}")
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print(f"Iterations: {result['n_iterations']}")
    print(f"Path length: {result['path_length']:.4f}")

    # Verify solution
    is_valid = verify_solution(result['full_trajectory'], DISK_RADIUS)

    # Check collision status
    n_disks = result['full_trajectory'].shape[1]
    touch_dist = 2 * DISK_RADIUS
    has_collisions = False
    all_pairs_touch = True

    for i in range(n_disks):
        for j in range(i+1, n_disks):
            min_dist = compute_trajectory_min_distance(result['full_trajectory'], i, j)
            if min_dist < touch_dist:
                has_collisions = True
            if min_dist > touch_dist:
                all_pairs_touch = False

    # Save solution
    if SAVE_AS_BEST and is_valid:
        save_solution(result['full_trajectory'], result['path_length'], solver.initial_positions,
                     all_pairs_touch, has_collisions,
                     solver.last_stationary_penalty, solver.last_path_penalty,
                     'best_n8_w10_adaptive.json')
    else:
        save_solution(result['full_trajectory'], result['path_length'], solver.initial_positions,
                     all_pairs_touch, has_collisions,
                     solver.last_stationary_penalty, solver.last_path_penalty,
                     'solution_adaptive.json')


if __name__ == '__main__':
    main()
