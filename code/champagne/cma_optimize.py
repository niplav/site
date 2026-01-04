#!/usr/bin/env python3
"""
Hybrid CMA-ES + trust-constr Optimizer for Champagne Toasting Problem

OPTIMIZATION STRATEGY:
This file implements a hybrid optimization approach combining:
1. CMA-ES (Covariance Matrix Adaptation Evolution Strategy) - global exploration
2. trust-constr (Trust Region Constrained Optimizer) - local exploitation

HYBRID ARCHITECTURE:
┌─────────────────────────────────────────────────────────────────┐
│ CMA-ES Population Evolution (Global Search)                     │
│  - Maintains population of candidate solutions                  │
│  - Adapts covariance matrix to learn promising search directions│
│  - Population size: POPSIZE (typically 10k)                      │
│  - Step size: SIGMA0 (adaptive)                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ every LOCAL_REFINEMENT_FREQUENCY iterations
┌─────────────────────────────────────────────────────────────────┐
│ trust-constr Local Refinement (Local Search)                    │
│  - Applied to best solution in current population               │
│  - Uses adaptive penalty objective (same as population)         │
│  - Max iterations: LOCAL_REFINEMENT_MAX_ITER                    │
│  - Only replaces if improved (monotonic!)                       │
└─────────────────────────────────────────────────────────────────┘

OBJECTIVE FUNCTION:
Uses adaptive penalty from adaptive_solver.py:
  fitness = path_length + stationary_penalty + path_penalty + distance_penalty

Where:
  - stationary_penalty: Quartic penalty for overlaps at waypoints
  - path_penalty: Exponential penalty for overlaps between waypoints
  - distance_penalty: Quadratic penalty for pairs that haven't touched

MONOTONICITY GUARANTEE:
The optimizer ensures monotonic progress through:
  1. Local refinement only updates if refined_fitness < current_fitness
  2. Best valid solution tracking only updates if better AND valid
  3. Sparse mutation anchors to current best (not initial solution)

WHY THIS WORKS:
- CMA-ES provides robust global search with adaptive step sizing
- trust-constr provides tight local convergence with gradient info
- Adaptive penalty creates smooth optimization landscape
- Hybrid approach gets best of both: exploration + exploitation
"""

import numpy as np
import sys

sys.path.insert(0, '/home/niplav/proj/site/code/champagne')
from choreography import Choreography
from vectorized_fitness import build_full_trajectory, compute_all_path_lengths_vectorized
from common import load_and_expand_best_solution, save_solution, load_best_known_fitness
from init import simulate_choreography, find_triplet_cover
from repair_operator import gentle_repair_population, compute_touching_positions

# Import adaptive penalty functions and constants from adaptive_solver
from adaptive_solver import compute_adaptive_penalty_jit, COLLISION_VALIDITY_THRESHOLD

# =============================================================================
# CONFIGURATION
# =============================================================================

# Problem parameters
N_DISKS = 8             # Number of champagne glasses
N_WAYPOINTS = 14        # Number of intermediate waypoints
DISK_RADIUS = 0.3       # Radius of each disk
INITIAL_DISTANCE = 3.0  # Distance from origin to each disk's starting position

# Adaptive penalty parameters (from adaptive_solver.py)
TOUCH_SHARPNESS = 10.0  # Controls sigmoid transition smoothness
STATIONARY_PENALTY_SCALE = 1.0  # Collisions AT waypoints (harsh - easy to fix)
PATH_PENALTY_SCALE = 1.0  # Collisions BETWEEN waypoints (gentler - harder to avoid)
DISTANCE_PENALTY_SCALE = 1.0  # Quadratic distance penalty - higher = stronger attraction

# Legacy parameter for save functions
PENALTY_ALPHA = 1.0

# Optimizer parameters
LOCAL_REFINE_INITIAL_TR_RADIUS = 1.0  # Initial trust region radius for local refinement

# CMA-ES parameters
SIGMA0 = 0.05  # Initial step size (small for local refinement from good starting point)
POPSIZE = 10000  # Population size (CMA-ES typically uses smaller populations)
MAX_ITER = 100000  # Maximum iterations
MIN_ITER = 0

# Termination tolerances (set very small to disable early stopping)
TOLFUN = 1e-11  # Tolerance on function value changes (smaller = run longer)
TOLX = 1e-11    # Tolerance on parameter changes (smaller = run longer)

# Sparse mutations (preserve coordinates to maintain structure)
SPARSE_MUTATION_RATE = 0.0  # Fraction of coordinates to preserve unchanged (0.0 = dense/disabled, 0.8 = very sparse)

# Repair operator (gentle waypoint modification)
REPAIR_RATE = 0.0 # Fraction of population to attempt repair (0.0 = disabled, 0.5 = 50%)
REPAIR_FREQUENCY = 10  # Apply repair every N iterations (1 = every iteration, 50 = every 50 iterations)
REPAIR_DEBUG = False # Enable detailed debugging output for repair operator

# Local refinement (trust-constr optimization - same as adaptive_solver.py)
LOCAL_REFINEMENT_ENABLED = True  # Enable/disable trust-constr refinement
LOCAL_REFINEMENT_FREQUENCY = 1   # Apply every N iterations (1 = every iteration)
LOCAL_REFINEMENT_MAX_ITER = 10000   # Max iterations for trust-constr

# Starting point options
WARM_START_MODE = 'greedy'  # 'greedy' (collision-free), 'best', 'nop' (stationary), or 'random'

# Output filename (auto-generated from parameters)
OUTPUT_PATH = f'/home/niplav/proj/site/code/champagne/best_n{N_DISKS}_w{N_WAYPOINTS}.json'
BEST_PATH = OUTPUT_PATH

def local_refine(x_flat, n_waypoints, n_disks, ch, max_iter=50):
    """
    Apply local refinement using trust-constr optimizer (hybrid architecture component).

    This function implements the LOCAL EXPLOITATION phase of the hybrid optimizer.
    It takes the best solution from the CMA-ES population and refines it using
    gradient-based trust-constr optimization for tight local convergence.

    Uses the same adaptive penalty objective as the CMA-ES population, ensuring
    consistency across global and local search phases.

    Args:
        x_flat: Flattened waypoints array (best from CMA-ES population)
        n_waypoints: Number of waypoints
        n_disks: Number of disks
        ch: Choreography instance
        max_iter: Maximum iterations for trust-constr

    Returns:
        (refined_flat, refined_fitness): Tuple of refined solution and its fitness
    """
    from scipy.optimize import minimize
    from vectorized_fitness import build_full_trajectory, compute_all_path_lengths_vectorized
    from adaptive_solver import compute_adaptive_penalty_jit

    original_shape = (n_waypoints, n_disks, 2)

    # Define objective function using adaptive penalty
    def objective(x):
        waypoints = x.reshape(original_shape)
        full_traj = build_full_trajectory(waypoints, ch.initial_positions)

        # Path length
        path_length = compute_all_path_lengths_vectorized(full_traj)

        # Adaptive penalty with separated stationary/path collisions
        total_penalty, _, _, _ = compute_adaptive_penalty_jit(
            full_traj,
            ch.radius,
            TOUCH_SHARPNESS,
            STATIONARY_PENALTY_SCALE,
            PATH_PENALTY_SCALE,
            DISTANCE_PENALTY_SCALE
        )

        return path_length + total_penalty

    # Run trust-constr optimization (robust, modern optimizer)
    result = minimize(
        objective,
        x_flat,
        method='trust-constr',
        options={
            'maxiter': max_iter,
            'gtol': 1e-6,
            'xtol': 1e-9,
            'verbose': 0,
            'initial_tr_radius': LOCAL_REFINE_INITIAL_TR_RADIUS
        }
    )

    return result.x, result.fun

def should_save_solution(new_fitness, new_is_valid, original_file_fitness, current_best_fitness=None):
    """
    Determine if a solution should be saved and generate appropriate message.

    Args:
        new_fitness: Fitness of new solution
        new_is_valid: Whether new solution is valid (no collisions/overlaps)
        original_file_fitness: Fitness from the loaded file
        current_best_fitness: Re-evaluated fitness (optional, for info messages)

    Returns:
        (should_save: bool, message: str or None)
    """
    if new_fitness < original_file_fitness and new_is_valid:
        return True, None  # Will print save success message elsewhere
    elif new_fitness < original_file_fitness and not new_is_valid:
        return False, f"✗ Skipping save: fitness {new_fitness:.4f} is better but has collisions/overlaps"
    elif current_best_fitness and new_fitness < current_best_fitness:
        return False, f"ℹ Found fitness {new_fitness:.4f}, but not better than original file fitness {original_file_fitness:.4f}"
    else:
        return False, None


def save_if_better(waypoints, ch, n_waypoints, penalty_alpha, output_path,
                   new_fitness, new_is_valid, original_file_fitness,
                   current_best_fitness=None, verbose=True, context=""):
    """
    Save solution only if it's valid and better than original file.

    Returns:
        (saved: bool, new_original_fitness: float) - updated threshold for future saves
    """
    should_save, msg = should_save_solution(new_fitness, new_is_valid,
                                           original_file_fitness, current_best_fitness)

    if msg and verbose:
        prefix = "  " if context == "iteration" else ""
        print(f"{prefix}{msg}")

    if should_save:
        save_solution(waypoints, ch, n_waypoints, penalty_alpha, output_path)
        if verbose:
            prefix = "  → " if context == "iteration" else "✓ "
            print(f"{prefix}New best (valid)! Saved to {output_path} (fitness: {new_fitness:.4f})")
        return True, new_fitness  # Update threshold

    return False, original_file_fitness  # Keep original threshold


def optimize_cma():
    """
    Run CMA-ES optimization with smart domain-specific mutations.

    DUAL-SAVE SYSTEM:
    This optimizer tracks and saves TWO separate solutions:
    1. Best VALID solution   → saved to best_n{N}_w{W}.json
       - Constraint: penalties < COLLISION_VALIDITY_THRESHOLD (0.01)
       - Only saves if fitness improves AND constraints satisfied

    2. Best PATH-LENGTH solution → saved to best_n{N}_w{W}_pathonly.json
       - No constraint on collision penalties
       - Tracks pure optimization progress, even if slightly invalid
       - Useful for understanding theoretical lower bounds
    """
    import cma

    ch = Choreography(n=N_DISKS, radius=DISK_RADIUS, initial_distance=INITIAL_DISTANCE)

    n_waypoints = N_WAYPOINTS  # local variable

    # Initialize starting point
    if WARM_START_MODE == 'greedy':
        # Use collision-free initialization (generates variable # of waypoints)
        print(f"Generating collision-free initialization for {N_DISKS} disks...")
        triplet_sequence = find_triplet_cover(N_DISKS)
        print(f"  Triplet sequence ({len(triplet_sequence)} triplets): {triplet_sequence}")

        init_waypoints, init_path_length = simulate_choreography(
            N_DISKS, DISK_RADIUS, INITIAL_DISTANCE, triplet_sequence
        )

        # Use ALL waypoints from initialization (don't resample!)
        n_waypoints = init_waypoints.shape[0]
        print(f"  Generated {n_waypoints} waypoints (collision-free)")
        print(f"  Initial path length: {init_path_length:.4f}")

        x0 = init_waypoints.flatten()

    elif WARM_START_MODE == 'best':
        # Load from best.json
        if n_waypoints is None:
            print("Error: N_WAYPOINTS must be specified for 'best' mode")
            return None
        x0 = load_and_expand_best_solution(BEST_PATH, n_waypoints)
        if x0 is None:
            print("Warning: Could not load best.json, falling back to greedy")
            init_waypoints, _ = simulate_choreography(N_DISKS, DISK_RADIUS, INITIAL_DISTANCE)
            n_waypoints = init_waypoints.shape[0]
            x0 = init_waypoints.flatten()
        else:
            x0 = x0.flatten()
            print(f"Warm-starting from {BEST_PATH} with {n_waypoints} waypoints")

    elif WARM_START_MODE == 'nop':
        # Stationary: all disks stay at initial positions (zero movement, guaranteed collision-free)
        if n_waypoints is None:
            print("Error: N_WAYPOINTS must be specified for 'nop' mode")
            return None
        init_waypoints = np.tile(ch.initial_positions, (n_waypoints, 1, 1))
        x0 = init_waypoints.flatten()
        print(f"Starting from stationary initialization with {n_waypoints} waypoints (all disks at initial positions)")

    else:  # random
        if n_waypoints is None:
            print("Error: N_WAYPOINTS must be specified for 'random' mode")
            return None
        x0 = np.random.randn(n_waypoints * N_DISKS * 2) * 0.5
        print(f"Starting from random initialization with {n_waypoints} waypoints")

    # Define objective function (now that we know n_waypoints)
    print(f"\nProblem dimensions: {n_waypoints} waypoints × {N_DISKS} disks × 2 coords = {n_waypoints * N_DISKS * 2} parameters")
    print(f"Using adaptive penalty: stationary={STATIONARY_PENALTY_SCALE}, path={PATH_PENALTY_SCALE}, distance={DISTANCE_PENALTY_SCALE}")

    def objective(x):
        """Fitness function for CMA-ES with adaptive penalties."""
        from vectorized_fitness import build_full_trajectory, compute_all_path_lengths_vectorized
        from adaptive_solver import compute_adaptive_penalty_jit

        waypoints = x.reshape((n_waypoints, N_DISKS, 2))
        full_traj = build_full_trajectory(waypoints, ch.initial_positions)

        # Path length
        path_length = compute_all_path_lengths_vectorized(full_traj)

        # Adaptive penalty with separated stationary/path collisions
        total_penalty, stat_pen, path_pen, dist_pen = compute_adaptive_penalty_jit(
            full_traj,
            ch.radius,
            TOUCH_SHARPNESS,
            STATIONARY_PENALTY_SCALE,
            PATH_PENALTY_SCALE,
            DISTANCE_PENALTY_SCALE
        )

        # Store penalties for debugging (accessible via objective.last_penalties)
        objective.last_stat = stat_pen
        objective.last_path = path_pen
        objective.last_dist = dist_pen

        return path_length + total_penalty

    # Update output path with actual waypoint count
    output_path = f'/home/niplav/proj/site/code/champagne/best_n{N_DISKS}_w{n_waypoints}.json'
    best_known_fitness = load_best_known_fitness(output_path)
    original_file_fitness = best_known_fitness  # Keep original for comparison
    if best_known_fitness < float('inf'):
        print(f"Found existing solution: {output_path}, fitness {best_known_fitness:.4f}")

    # Evaluate initial fitness
    initial_fitness = objective(x0)
    print(f"Initial fitness: {initial_fitness:.4f}")
    if abs(initial_fitness - best_known_fitness) > 0.01 and best_known_fitness < float('inf'):
        print(f"  ⚠ Warning: Re-evaluated fitness ({initial_fitness:.4f}) differs from saved ({best_known_fitness:.4f})")

    # CMA-ES options
    opts = {
        'popsize': POPSIZE,
        'maxiter': MAX_ITER,
        'tolfun': TOLFUN,  # Terminate if fitness improvement < tolfun
        'tolx': TOLX,      # Terminate if step size < tolx
        'verbose': 1,      # Print progress
    }

    print("\nStarting CMA-ES optimization...")
    print("-" * 60)

    # Run CMA-ES
    es = cma.CMAEvolutionStrategy(x0, SIGMA0, opts)

    # Track best valid solution from repaired population
    best_valid_solution = None
    best_valid_fitness = float('inf')

    # Track best path-length solution (regardless of validity)
    best_pathlen_solution = None
    best_pathlen_fitness = float('inf')
    best_pathlen_file_fitness = load_best_known_fitness(output_path.replace('.json', '_pathonly.json'))

    iteration = 0
    current_best = x0.copy()  # Track current best solution for sparse mutation

    while not es.stop() or iteration<MIN_ITER:
        solutions = es.ask()

        # Sparse mutation: preserve coordinates from current best (not initial!)
        if SPARSE_MUTATION_RATE > 0:
            for i in range(1, len(solutions)):
                mask = np.random.random(len(solutions[i])) < SPARSE_MUTATION_RATE
                solutions[i][mask] = current_best[mask]

        # Inject exact collision-free solution as first individual in first iteration
        if iteration == 0:
            solutions[0] = x0.copy()

        if REPAIR_RATE > 0 and iteration % REPAIR_FREQUENCY == 0:
            # Only debug on first few repair calls to avoid spam
            debug_repair = REPAIR_DEBUG and iteration <= REPAIR_FREQUENCY * 2
            solutions = gentle_repair_population(solutions, n_waypoints, N_DISKS, ch, repair_rate=REPAIR_RATE, fitness_fn=None, debug=debug_repair)

        # Evaluate all solutions once
        fitnesses = [objective(s) for s in solutions]

        # Apply local refinement to best solution(s)
        if LOCAL_REFINEMENT_ENABLED and iteration % LOCAL_REFINEMENT_FREQUENCY == 0:
            best_idx = np.argmin(fitnesses)

            # Refine best solution
            refined_solution, refined_fitness = local_refine(
                solutions[best_idx], n_waypoints, N_DISKS, ch,
                max_iter=LOCAL_REFINEMENT_MAX_ITER
            )

            # Replace if improved (MONOTONICITY: only update if strictly better)
            if refined_fitness < fitnesses[best_idx]:
                solutions[best_idx] = refined_solution
                fitnesses[best_idx] = refined_fitness

        es.tell(solutions, fitnesses)

        # Update current best for sparse mutation (MONOTONICITY: always best from current population)
        best_idx_current = np.argmin(fitnesses)
        current_best = solutions[best_idx_current].copy()

        # Log progress
        if iteration % 1 == 0:
            best_fitness = min(fitnesses)
            best_idx = np.argmin(fitnesses)
            best_waypoints = solutions[best_idx].reshape((n_waypoints, N_DISKS, 2))

            # Show separated penalties for best solution
            print(f"Iter {iteration:5d}: Best={best_fitness:.4f}, "
                  f"Stat={objective.last_stat:.2f}, Path={objective.last_path:.2f}, "
                  f"Dist={objective.last_dist:.2f}, Sigma={es.sigma:.4f}")

            # Check if new solution has collisions using adaptive penalty (consistent with objective!)
            from vectorized_fitness import build_full_trajectory
            full_traj = build_full_trajectory(best_waypoints, ch.initial_positions)

            # Use the same adaptive penalty we optimize
            _, stat_penalty, path_penalty, _ = compute_adaptive_penalty_jit(
                full_traj, ch.radius, TOUCH_SHARPNESS,
                STATIONARY_PENALTY_SCALE, PATH_PENALTY_SCALE, DISTANCE_PENALTY_SCALE
            )

            # Solution is valid if collision penalties are near zero
            new_is_valid = (stat_penalty < COLLISION_VALIDITY_THRESHOLD and
                           path_penalty < COLLISION_VALIDITY_THRESHOLD)

            # Save if better and valid (using consolidated function)
            saved, original_file_fitness = save_if_better(
                best_waypoints, ch, n_waypoints, PENALTY_ALPHA, output_path,
                best_fitness, new_is_valid, original_file_fitness,
                current_best_fitness=best_known_fitness,
                verbose=True, context="iteration"
            )
            if saved:
                best_known_fitness = best_fitness

            # Track best valid solution (MONOTONICITY: only update if valid AND better)
            if new_is_valid and best_fitness < best_valid_fitness:
                best_valid_solution = best_waypoints.copy()
                best_valid_fitness = best_fitness

            # Track best path-length solution (REGARDLESS of validity)
            # This tracks pure optimization progress, even if constraints are violated
            if best_fitness < best_pathlen_fitness:
                best_pathlen_solution = best_waypoints.copy()
                best_pathlen_fitness = best_fitness

                # Save if better than previous best path-only solution
                if best_fitness < best_pathlen_file_fitness:
                    pathonly_path = output_path.replace('.json', '_pathonly.json')
                    save_solution(best_waypoints, ch, n_waypoints, PENALTY_ALPHA, pathonly_path)
                    print(f"  → New best path-length! Saved to {pathonly_path} (fitness: {best_fitness:.4f}, valid: {new_is_valid})")
                    best_pathlen_file_fitness = best_fitness

        iteration += 1

    # Final results
    print("\n" + "=" * 60)
    print("OPTIMIZATION COMPLETE")
    print("=" * 60)

    # Use tracked best valid solution instead of es.result.xbest
    if best_valid_solution is not None:
        print(f"Using tracked best valid solution (fitness={best_valid_fitness:.4f})")
        best_waypoints = best_valid_solution
        best_fitness = best_valid_fitness
    else:
        print(f"No valid solution found, using CMA-ES xbest")
        best_solution = es.result.xbest
        best_fitness = es.result.fbest
        best_waypoints = best_solution.reshape((n_waypoints, N_DISKS, 2))

    print(f"Best fitness: {best_fitness:.4f}")

    # Validate solution using adaptive penalty (consistent!)
    from vectorized_fitness import build_full_trajectory
    full_traj = build_full_trajectory(best_waypoints, ch.initial_positions)

    _, stat_penalty, path_penalty, dist_penalty = compute_adaptive_penalty_jit(
        full_traj, ch.radius, TOUCH_SHARPNESS,
        STATIONARY_PENALTY_SCALE, PATH_PENALTY_SCALE, DISTANCE_PENALTY_SCALE
    )

    print(f"\nFinal solution penalties: Stat={stat_penalty:.4f}, Path={path_penalty:.4f}, Dist={dist_penalty:.4f}")

    # Print summary of both tracked solutions
    print("\n" + "-" * 60)
    print("SOLUTION TRACKING SUMMARY:")
    print(f"  Best valid solution:      {best_valid_fitness:.4f} (penalties < {COLLISION_VALIDITY_THRESHOLD})")
    print(f"  Best path-length solution: {best_pathlen_fitness:.4f} (regardless of validity)")
    print("-" * 60)

    # Final save - use consolidated function
    final_is_valid = (stat_penalty < COLLISION_VALIDITY_THRESHOLD and
                     path_penalty < COLLISION_VALIDITY_THRESHOLD)
    save_if_better(
        best_waypoints, ch, n_waypoints, PENALTY_ALPHA, output_path,
        best_fitness, final_is_valid, original_file_fitness,
        verbose=True, context="final"
    )

    # Also save final best path-length solution (regardless of validity)
    if best_pathlen_solution is not None and best_pathlen_fitness < best_pathlen_file_fitness:
        pathonly_path = output_path.replace('.json', '_pathonly.json')
        save_solution(best_pathlen_solution, ch, n_waypoints, PENALTY_ALPHA, pathonly_path)
        print(f"✓ Final best path-length saved to {pathonly_path} (fitness: {best_pathlen_fitness:.4f})")

    return best_waypoints, best_fitness


if __name__ == '__main__':
    optimize_cma()
