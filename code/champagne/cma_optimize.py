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

# =============================================================================
# CONFIGURATION
# =============================================================================

# Problem parameters
N_DISKS = 6             # Number of champagne glasses
N_WAYPOINTS = 6         # Number of intermediate waypoints
DISK_RADIUS = 0.3       # Radius of each disk
INITIAL_DISTANCE = 3.0  # Distance from origin to each disk's starting position

# Fitness parameters
PENALTY_ALPHA = 1.0

# CMA-ES parameters
SIGMA0 = 0.01  # Initial step size (small for local refinement from good starting point)
POPSIZE = 1000  # Population size (CMA-ES typically uses smaller populations)
MAX_ITER = 10000  # Maximum iterations

# Termination tolerances (set very small to disable early stopping)
TOLFUN = 1e-11  # Tolerance on function value changes (smaller = run longer)
TOLX = 1e-11    # Tolerance on parameter changes (smaller = run longer)

# Starting point options
WARM_START_MODE = 'greedy'  # 'greedy' (collision-free), 'best', or 'random'

# Output filename (auto-generated from parameters)
OUTPUT_PATH = f'/home/niplav/proj/site/code/champagne/best_n{N_DISKS}_w{N_WAYPOINTS}_p{POPSIZE}.json'
BEST_PATH = OUTPUT_PATH

# =============================================================================


def optimize_cma():
    """Run CMA-ES optimization."""
    import cma

    ch = Choreography(n=N_DISKS, radius=DISK_RADIUS, initial_distance=INITIAL_DISTANCE)

    print("CMA-ES Optimization for Champagne Toasting Problem")
    print("=" * 60)
    print(f"Disks: {N_DISKS}")
    print(f"Disk radius: {DISK_RADIUS}")
    print(f"Initial distance: {INITIAL_DISTANCE}")
    print(f"Population: {POPSIZE}")
    print(f"Max iterations: {MAX_ITER}")
    print(f"Initial sigma: {SIGMA0}")
    print(f"Tolerances: tolfun={TOLFUN}, tolx={TOLX}")

    # Determine N_WAYPOINTS based on initialization mode
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
            early_terminate_threshold=float('inf')
        )
        return fitness

    # Update output path with actual waypoint count
    output_path = f'/home/niplav/proj/site/code/champagne/best_n{N_DISKS}_w{n_waypoints}_p{POPSIZE}.json'
    best_known_fitness = load_best_known_fitness(output_path)
    if best_known_fitness < float('inf'):
        print(f"Found existing solution: {output_path}, fitness {best_known_fitness:.4f}")

    # Evaluate initial fitness
    initial_fitness = objective(x0)
    print(f"Initial fitness: {initial_fitness:.4f}")

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

    iteration = 0
    while not es.stop():
        solutions = es.ask()
        fitnesses = [objective(s) for s in solutions]
        es.tell(solutions, fitnesses)

        # Log progress
        if iteration % 100 == 0:
            best_fitness = min(fitnesses)
            print(f"Iter {iteration:5d}: Best={best_fitness:.4f}, "
                  f"Sigma={es.sigma:.4f}")

            # Save if better than best known
            if best_fitness < best_known_fitness:
                best_waypoints = solutions[np.argmin(fitnesses)].reshape((n_waypoints, N_DISKS, 2))
                save_solution(best_waypoints, ch, n_waypoints, PENALTY_ALPHA, output_path)
                print(f"  → New best! Saved to {output_path}")
                best_known_fitness = best_fitness

        iteration += 1

    # Final results
    print("\n" + "=" * 60)
    print("OPTIMIZATION COMPLETE")
    print("=" * 60)

    best_solution = es.result.xbest
    best_fitness = es.result.fbest
    best_waypoints = best_solution.reshape((n_waypoints, N_DISKS, 2))

    print(f"Best fitness: {best_fitness:.4f}")
    print(f"Iterations: {es.result.iterations}")
    print(f"Function evaluations: {es.result.evaluations}")

    # Validate solution
    configs = [best_waypoints[i] for i in range(n_waypoints)]
    all_touching = ch.get_all_touching_pairs(configs)
    path_length = ch.total_path_length(best_waypoints)

    n_pairs = N_DISKS * (N_DISKS - 1) // 2

    print(f"Path length: {path_length:.4f}")
    print(f"Pairs touching: {len(all_touching)}/{n_pairs}")

    from vectorized_fitness import check_path_collisions_vectorized, build_full_trajectory
    full_traj = build_full_trajectory(best_waypoints, ch.initial_positions)
    path_penalty = check_path_collisions_vectorized(full_traj, 2 * ch.radius)

    if len(all_touching) == n_pairs:
        print("✓ All pairs touch!")
    else:
        missing = set([(i, j) for i in range(N_DISKS) for j in range(i + 1, N_DISKS)]) - all_touching
        print(f"✗ Missing pairs: {missing}")

    if path_penalty < 0.01:
        print("✓ No collisions!")
    else:
        print(f"✗ Collision penalty: {path_penalty:.4f}")

    # Final save
    save_solution(best_waypoints, ch, n_waypoints, PENALTY_ALPHA, output_path)
    print(f"\nFinal solution saved to {output_path}")

    return best_waypoints, best_fitness


if __name__ == '__main__':
    optimize_cma()
