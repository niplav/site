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
N_DISKS = 8             # Number of champagne glasses
N_WAYPOINTS = None # Number of intermediate waypoints
DISK_RADIUS = 0.3       # Radius of each disk
INITIAL_DISTANCE = 3.0  # Distance from origin to each disk's starting position

# Fitness parameters
PENALTY_ALPHA = 1.0

# CMA-ES parameters
SIGMA0 = 0.01  # Initial step size (small for local refinement from good starting point)
POPSIZE = 200  # Population size (CMA-ES typically uses smaller populations)
MAX_ITER = 10000  # Maximum iterations

# Termination tolerances (set very small to disable early stopping)
TOLFUN = 1e-11  # Tolerance on function value changes (smaller = run longer)
TOLX = 1e-11    # Tolerance on parameter changes (smaller = run longer)

# Smart mutations (domain-specific)
SMART_MUTATION_RATE = 0  # Fraction of population to apply smart mutations (0.0 = disabled, 0.2 = 20%)

# Starting point options
WARM_START_MODE = 'greedy'  # 'greedy' (collision-free), 'best', or 'random'

# Output filename (auto-generated from parameters)
OUTPUT_PATH = f'/home/niplav/proj/site/code/champagne/best_n{N_DISKS}_w{N_WAYPOINTS}.json'
BEST_PATH = OUTPUT_PATH

# =============================================================================


def apply_smart_mutations(solutions, n_waypoints, n_disks, radius, mutation_rate=0.2):
    """
    Apply domain-specific mutations: move disks toward each other to create touching.

    For a subset of solutions, pick random disk pairs and move them closer together
    at random waypoints to maintain/create touching configurations.
    """
    touch_distance = 2 * radius
    n_solutions = len(solutions)
    n_mutated = int(n_solutions * mutation_rate)

    if n_mutated == 0:
        return solutions

    # Pick random solutions to mutate (skip first one - it's our exact solution)
    indices_to_mutate = np.random.choice(range(1, n_solutions), size=min(n_mutated, n_solutions-1), replace=False)

    for idx in indices_to_mutate:
        solution = solutions[idx].copy()
        waypoints = solution.reshape((n_waypoints, n_disks, 2))

        # Pick a random pair of disks
        disk_a, disk_b = np.random.choice(n_disks, size=2, replace=False)

        # Pick a random waypoint
        wp = np.random.randint(n_waypoints)

        # Move disk_a toward disk_b to be exactly touch_distance apart
        pos_a = waypoints[wp, disk_a].copy()
        pos_b = waypoints[wp, disk_b].copy()

        direction = pos_b - pos_a
        current_dist = np.linalg.norm(direction)

        if current_dist > 1e-6:  # Avoid division by zero
            # Both disks move toward their midpoint, ending up touch_distance apart
            direction_normalized = direction / current_dist
            midpoint = (pos_a + pos_b) / 2
            half_touch = touch_distance / 2

            new_pos_a = midpoint - half_touch * direction_normalized
            new_pos_b = midpoint + half_touch * direction_normalized

            waypoints[wp, disk_a] = new_pos_a
            waypoints[wp, disk_b] = new_pos_b

        solutions[idx] = waypoints.flatten()

    return solutions


def optimize_cma():
    """Run CMA-ES optimization with smart domain-specific mutations."""
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
    output_path = f'/home/niplav/proj/site/code/champagne/best_n{N_DISKS}_w{n_waypoints}.json'
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

        # Inject exact collision-free solution as first individual in first iteration
        if iteration == 0:
            solutions[0] = x0.copy()
            print(f"  → Injected exact solution as solutions[0]")
            if SMART_MUTATION_RATE > 0:
                print(f"  → Using smart mutations ({SMART_MUTATION_RATE*100:.0f}% of population)")
            else:
                print(f"  → Smart mutations disabled")

        # Apply smart domain-specific mutations to subset of population
        if SMART_MUTATION_RATE > 0:
            solutions = apply_smart_mutations(solutions, n_waypoints, N_DISKS, DISK_RADIUS, mutation_rate=SMART_MUTATION_RATE)

        fitnesses = [objective(s) for s in solutions]
        es.tell(solutions, fitnesses)

        # Log progress
        if iteration % 100 == 0:
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

            # Load current best to check if it has collisions
            current_best_is_valid = True
            if best_known_fitness < float('inf'):
                try:
                    import json
                    with open(output_path, 'r') as f:
                        data = json.load(f)
                    current_best_is_valid = not (data['metadata'].get('has_waypoint_overlaps', False) or
                                                 data['metadata'].get('has_path_collisions', False))
                except:
                    pass

            # Save if better AND valid, OR if current best is also invalid
            should_save = False
            if best_fitness < best_known_fitness:
                if new_is_valid:
                    should_save = True  # Always save valid improvements
                elif not current_best_is_valid:
                    should_save = True  # Save if both are invalid (allow improving invalid solutions)
                else:
                    print(f"  ✗ Skipping save: new solution has collisions/overlaps but current best is valid")

            if should_save:
                save_solution(best_waypoints, ch, n_waypoints, PENALTY_ALPHA, output_path)
                validity_msg = "valid" if new_is_valid else "invalid (has collisions/overlaps)"
                print(f"  → New best ({validity_msg})! Saved to {output_path}")
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
