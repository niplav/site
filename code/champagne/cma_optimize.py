#!/usr/bin/env python3
"""
CMA-ES optimization for champagne toasting problem.

Uses Covariance Matrix Adaptation Evolution Strategy for sophisticated
black-box optimization.
"""

import numpy as np
import sys

sys.path.insert(0, '/home/niplav/proj/site/code/champagne')
from choreography import Choreography
from vectorized_fitness import evaluate_fitness_vectorized
from common import load_and_expand_best_solution, save_solution, load_best_known_fitness
from init import simulate_choreography, find_triplet_cover
from repair_operator import gentle_repair_population, compute_touching_positions

# =============================================================================
# CONFIGURATION
# =============================================================================

# Problem parameters
N_DISKS = 8             # Number of champagne glasses
N_WAYPOINTS = 10        # Number of intermediate waypoints
DISK_RADIUS = 0.3       # Radius of each disk
INITIAL_DISTANCE = 3.0  # Distance from origin to each disk's starting position

# Fitness parameters
PENALTY_ALPHA = 1.0
OVERLAP_PENALTY_WEIGHT = 50    # Penalty multiplier for waypoint overlaps (default: 50)
COLLISION_PENALTY_WEIGHT = 100  # Penalty multiplier for path collisions (default: 100)
MISSING_PENALTY_WEIGHT = 100

# CMA-ES parameters
SIGMA0 = 0.05  # Initial step size (small for local refinement from good starting point)
POPSIZE = 2  # Population size (CMA-ES typically uses smaller populations)
MAX_ITER = 8  # Maximum iterations
MIN_ITER = 4

# Termination tolerances (set very small to disable early stopping)
TOLFUN = 1e-11  # Tolerance on function value changes (smaller = run longer)
TOLX = 1e-11    # Tolerance on parameter changes (smaller = run longer)

# Sparse mutations (preserve coordinates to maintain structure)
SPARSE_MUTATION_RATE = 1.0  # Fraction of coordinates to preserve unchanged (0.0 = dense/disabled, 0.8 = very sparse)

# Repair operator (gentle waypoint modification)
REPAIR_RATE = 1.0 # Fraction of population to attempt repair (0.0 = disabled, 0.5 = 50%)

# Starting point options
WARM_START_MODE = 'nop'  # 'greedy' (collision-free), 'best', 'nop' (stationary), or 'random'

# Output filename (auto-generated from parameters)
OUTPUT_PATH = f'/home/niplav/proj/site/code/champagne/best_n{N_DISKS}_w{N_WAYPOINTS}.json'
BEST_PATH = OUTPUT_PATH

def local_refine(solution, ch, max_iter=50):
    """
    Apply local refinement to a solution using scipy.optimize.

    This is gradient-free optimization (Nelder-Mead) to fine-tune the solution.
    """
    from scipy.optimize import minimize

    # Flatten waypoints for scipy
    x0 = solution.waypoints.flatten()
    original_shape = solution.waypoints.shape

    # Define objective function
    def objective(x):
        waypoints = x.reshape(original_shape)
        fitness = evaluate_fitness_vectorized(
            waypoints, ch.initial_positions, ch.radius,
            penalty_alpha=PENALTY_ALPHA,
            early_terminate_threshold=float('inf')  # No early termination in local search
        )
        return fitness

    # Run optimization (Nelder-Mead is gradient-free and robust)
    result = minimize(
        objective,
        x0,
        method='Nelder-Mead',
        options={'maxiter': max_iter, 'xatol': 1e-4, 'fatol': 1e-4}
    )

    # Create refined solution
    refined_waypoints = result.x.reshape(original_shape)
    refined_solution = Solution(waypoints=refined_waypoints, fitness=result.fun)

    return refined_solution

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
    """Run CMA-ES optimization with smart domain-specific mutations."""
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

    def objective(x):
        """Fitness function for CMA-ES."""
        waypoints = x.reshape((n_waypoints, N_DISKS, 2))
        fitness = evaluate_fitness_vectorized(
            waypoints, ch.initial_positions, ch.radius,
            penalty_alpha=PENALTY_ALPHA,
            early_terminate_threshold=float('inf'),
            overlap_penalty_weight=OVERLAP_PENALTY_WEIGHT,
            collision_penalty_weight=COLLISION_PENALTY_WEIGHT,
            missing_meet_penalty_weight=MISSING_PENALTY_WEIGHT
        )
        return fitness

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

    iteration = 0
    while not es.stop() or iteration<MIN_ITER:
        solutions = es.ask()

        if SPARSE_MUTATION_RATE > 0:
            for i in range(1, len(solutions)):
                mask = np.random.random(len(solutions[i])) < SPARSE_MUTATION_RATE
                solutions[i][mask] = x0[mask]

        # Inject exact collision-free solution as first individual in first iteration
        if iteration == 0:
            solutions[0] = x0.copy()

        if REPAIR_RATE > 0:
            solutions = gentle_repair_population(solutions, n_waypoints, N_DISKS, ch, repair_rate=REPAIR_RATE, fitness_fn=None)

        fitnesses = [objective(s) for s in solutions]
        es.tell(solutions, fitnesses)

        # Log progress
        if iteration % 1 == 0:
            best_fitness = min(fitnesses)
            best_idx = np.argmin(fitnesses)
            best_waypoints = solutions[best_idx].reshape((n_waypoints, N_DISKS, 2))

            print(f"Iter {iteration:5d}: Best={best_fitness:.4f}, "
                  f"Sigma={es.sigma:.4f}")

            # Check if new solution has collisions/overlaps
            from vectorized_fitness import check_waypoint_overlaps_vectorized, check_path_collisions_vectorized, build_full_trajectory
            full_traj = build_full_trajectory(best_waypoints, ch.initial_positions)
            new_has_overlaps = check_waypoint_overlaps_vectorized(best_waypoints, 2 * ch.radius) > 0.01
            new_has_collisions = check_path_collisions_vectorized(full_traj, 2 * ch.radius) > 0.01
            new_is_valid = not (new_has_overlaps or new_has_collisions)

            # Save if better and valid (using consolidated function)
            saved, original_file_fitness = save_if_better(
                best_waypoints, ch, n_waypoints, PENALTY_ALPHA, output_path,
                best_fitness, new_is_valid, original_file_fitness,
                current_best_fitness=best_known_fitness,
                verbose=True, context="iteration"
            )
            if saved:
                best_known_fitness = best_fitness

            # Track best valid solution from this generation
            if new_is_valid and best_fitness < best_valid_fitness:
                best_valid_solution = best_waypoints.copy()
                best_valid_fitness = best_fitness

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

    # Validate solution
    configs = [best_waypoints[i] for i in range(n_waypoints)]
    all_touching = ch.get_all_touching_pairs(configs)
    path_length = ch.total_path_length(best_waypoints)

    from vectorized_fitness import check_path_collisions_vectorized, check_waypoint_overlaps_vectorized, build_full_trajectory
    full_traj = build_full_trajectory(best_waypoints, ch.initial_positions)
    path_penalty = check_path_collisions_vectorized(full_traj, 2 * ch.radius)
    overlap_penalty = check_waypoint_overlaps_vectorized(best_waypoints, 2 * ch.radius)

    n_pairs = N_DISKS * (N_DISKS - 1) // 2
    if len(all_touching) != n_pairs:
        missing = set([(i, j) for i in range(N_DISKS) for j in range(i + 1, N_DISKS)]) - all_touching

    # Final save - use consolidated function
    final_is_valid = (path_penalty < 0.01 and overlap_penalty < 0.01)
    save_if_better(
        best_waypoints, ch, n_waypoints, PENALTY_ALPHA, output_path,
        best_fitness, final_is_valid, original_file_fitness,
        verbose=True, context="final"
    )

    return best_waypoints, best_fitness


if __name__ == '__main__':
    optimize_cma()
