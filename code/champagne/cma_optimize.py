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

# =============================================================================
# CONFIGURATION
# =============================================================================

N_WAYPOINTS = 5
PENALTY_ALPHA = 1.0

# CMA-ES parameters
SIGMA0 = 0.01  # Initial step size (small for local refinement from good starting point)
POPSIZE = 1000  # Population size (CMA-ES typically uses smaller populations)
MAX_ITER = 10000  # Maximum iterations

# Termination tolerances (set very small to disable early stopping)
TOLFUN = 1e-11  # Tolerance on function value changes (smaller = run longer)
TOLX = 1e-11    # Tolerance on parameter changes (smaller = run longer)

# Starting point
WARM_START = True  # Start from best_1.json
BEST_1_PATH = '/home/niplav/proj/site/code/champagne/best_1.json'
OUTPUT_PATH = '/home/niplav/proj/site/code/champagne/best_solution.json'

# =============================================================================


def optimize_cma():
    """Run CMA-ES optimization."""
    import cma

    ch = Choreography(n=5)

    print("=" * 60)
    print("CMA-ES Optimization for Champagne Toasting Problem")
    print("=" * 60)
    print(f"Waypoints: {N_WAYPOINTS}")
    print(f"Dimensions: {N_WAYPOINTS * 5 * 2} (waypoints × disks × coords)")
    print(f"Population: {POPSIZE}")
    print(f"Max iterations: {MAX_ITER}")
    print(f"Initial sigma: {SIGMA0}")
    print(f"Tolerances: tolfun={TOLFUN}, tolx={TOLX}")

    # Load best known fitness
    best_known_fitness = load_best_known_fitness(BEST_1_PATH)
    print(f"Best known fitness: {best_known_fitness:.4f}")

    # Define objective function
    def objective(x):
        """Fitness function for CMA-ES."""
        waypoints = x.reshape((N_WAYPOINTS, 5, 2))
        fitness = evaluate_fitness_vectorized(
            waypoints, ch.initial_positions, ch.radius,
            penalty_alpha=PENALTY_ALPHA,
            early_terminate_threshold=float('inf')
        )
        return fitness

    # Initialize starting point
    if WARM_START:
        x0 = load_and_expand_best_solution(BEST_1_PATH, N_WAYPOINTS)
        if x0 is not None:
            x0_flat = x0.flatten()
            # Evaluate the starting point to verify it's good
            initial_fitness = objective(x0_flat)
            print(f"Warm-starting from best_1.json")
            print(f"Initial solution fitness: {initial_fitness:.4f}")
            x0 = x0_flat
        else:
            print("Warning: Could not load best_1.json, using random start")
            x0 = np.random.randn(N_WAYPOINTS * 5 * 2) * 0.5
    else:
        x0 = np.random.randn(N_WAYPOINTS * 5 * 2) * 0.5
        print("Starting from random initialization")

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
                best_waypoints = solutions[np.argmin(fitnesses)].reshape((N_WAYPOINTS, 5, 2))
                save_solution(best_waypoints, ch, N_WAYPOINTS, PENALTY_ALPHA, OUTPUT_PATH)
                print(f"  → New best! Saved to {OUTPUT_PATH}")
                best_known_fitness = best_fitness

        iteration += 1

    # Final results
    print("\n" + "=" * 60)
    print("OPTIMIZATION COMPLETE")
    print("=" * 60)

    best_solution = es.result.xbest
    best_fitness = es.result.fbest
    best_waypoints = best_solution.reshape((N_WAYPOINTS, 5, 2))

    print(f"Best fitness: {best_fitness:.4f}")
    print(f"Iterations: {es.result.iterations}")
    print(f"Function evaluations: {es.result.evaluations}")

    # Validate solution
    configs = [best_waypoints[i] for i in range(N_WAYPOINTS)]
    all_touching = ch.get_all_touching_pairs(configs)
    path_length = ch.total_path_length(best_waypoints)

    print(f"Path length: {path_length:.4f}")
    print(f"Pairs touching: {len(all_touching)}/10")

    from vectorized_fitness import check_path_collisions_vectorized, build_full_trajectory
    full_traj = build_full_trajectory(best_waypoints, ch.initial_positions)
    path_penalty = check_path_collisions_vectorized(full_traj, 2 * ch.radius)

    if len(all_touching) == 10:
        print("✓ All pairs touch!")
    else:
        missing = set([(i, j) for i in range(5) for j in range(i + 1, 5)]) - all_touching
        print(f"✗ Missing pairs: {missing}")

    if path_penalty < 0.01:
        print("✓ No collisions!")
    else:
        print(f"✗ Collision penalty: {path_penalty:.4f}")

    # Final save
    save_solution(best_waypoints, ch, N_WAYPOINTS, PENALTY_ALPHA, OUTPUT_PATH)
    print(f"\nFinal solution saved to {OUTPUT_PATH}")

    return best_waypoints, best_fitness


if __name__ == '__main__':
    optimize_cma()
