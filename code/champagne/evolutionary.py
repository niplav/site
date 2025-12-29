#!/usr/bin/env python3
"""
ULTRA-OPTIMIZED evolutionary algorithm using vectorized_fitness.

This actually uses the 388x faster fitness evaluation!
"""

import numpy as np
import sys
from multiprocessing import Pool, cpu_count
from functools import partial

sys.path.insert(0, '/home/niplav/proj/site/code/champagne')
from choreography import Choreography
from vectorized_fitness import evaluate_fitness_vectorized
from common import Solution, load_and_expand_best_solution, save_solution, load_best_known_fitness

# =============================================================================
# CONFIGURATION
# =============================================================================

# Reproducibility
RANDOM_SEED = None

# Evolutionary algorithm parameters
POPULATION_SIZE = 1000
N_WAYPOINTS = 5
N_GENERATIONS = 100000

# Evolutionary operators
MUTATION_RATE = 0.15
MUTATION_STRENGTH = 0.25
SURVIVAL_RATE = 0.4

# Fitness parameters
PENALTY_ALPHA = 1.0

# Smart initialization parameters
# Using ONLY greedy heuristic seed
N_BEST_1_PERTURBATIONS = 0   # Disabled - avoid local maximum trap
N_ULTRA_GREEDY_PERTURBATIONS = 1  # Just the base greedy solution, no perturbations
N_TRIPLET_ORDERINGS = 0      # Disabled - use only greedy

# Local refinement parameters
LOCAL_REFINEMENT_FREQUENCY = 150  # Apply every N generations
LOCAL_REFINEMENT_ELITE_FRACTION = 0.05  # Refine top 5% of population (50 solutions)
LOCAL_REFINEMENT_MAX_ITER = 150  # Max iterations per refinement (deep polish when we do it!)

# Parallelization
N_PROCESSES = max(1, cpu_count() - 1)
USE_PARALLEL = True

# =============================================================================

if RANDOM_SEED is not None:
    np.random.seed(RANDOM_SEED)
    print(f"Random seed set to {RANDOM_SEED}")
else:
    print("Using random seed")

print(f"Using {N_PROCESSES} processes" if USE_PARALLEL else "Single-threaded")


def evaluate_solution_worker(waypoints, params):
    """Worker for parallel evaluation using VECTORIZED fitness."""
    initial_positions, radius = params
    return evaluate_fitness_vectorized(
        waypoints, initial_positions, radius,
        penalty_alpha=PENALTY_ALPHA,
        early_terminate_threshold=1000.0
    )


def evaluate_population_parallel(population, ch, pool):
    """Evaluate entire population in parallel."""
    params = (ch.initial_positions, ch.radius)
    waypoints_list = [sol.waypoints for sol in population]

    fitnesses = pool.map(
        partial(evaluate_solution_worker, params=params),
        waypoints_list
    )

    for sol, fitness in zip(population, fitnesses):
        sol.fitness = fitness


def evaluate_population_serial(population, ch):
    """Evaluate population serially."""
    for sol in population:
        sol.fitness = evaluate_fitness_vectorized(
            sol.waypoints, ch.initial_positions, ch.radius,
            penalty_alpha=PENALTY_ALPHA,
            early_terminate_threshold=1000.0
        )


def initialize_population(pop_size, n_waypoints, ch):
    """Initialize population with random solutions."""
    population = []

    for _ in range(pop_size):
        waypoints = np.zeros((n_waypoints, 5, 2))
        for w in range(n_waypoints):
            for disk in range(5):
                angle = np.random.uniform(0, 2 * np.pi)
                radius = np.random.uniform(0, 2.0)
                waypoints[w, disk] = np.array([
                    radius * np.cos(angle),
                    radius * np.sin(angle)
                ])

        population.append(Solution(waypoints=waypoints))

    return population


def crossover(parent1, parent2):
    """Create offspring by mixing parents."""
    n_wp = parent1.waypoints.shape[0]
    offspring_wp = np.zeros_like(parent1.waypoints)

    for w in range(n_wp):
        if np.random.random() < 0.5:
            offspring_wp[w] = parent1.waypoints[w].copy()
        else:
            offspring_wp[w] = parent2.waypoints[w].copy()

    return Solution(waypoints=offspring_wp)


def mutate(solution, generation=None):
    """
    Mutate solution by perturbing waypoints.

    Uses adaptive mutation strength that decreases over generations.
    """
    mutated = solution.waypoints.copy()

    # Adaptive mutation strength: decay from MUTATION_STRENGTH to 0.01
    if generation is not None:
        progress = generation / N_GENERATIONS
        mutation_strength = MUTATION_STRENGTH * (1 - progress * 0.95) + 0.01
    else:
        mutation_strength = MUTATION_STRENGTH

    for w in range(mutated.shape[0]):
        for disk in range(mutated.shape[1]):
            if np.random.random() < MUTATION_RATE:
                perturbation = np.random.normal(0, mutation_strength, size=2)
                mutated[w, disk] += perturbation

    return Solution(waypoints=mutated)


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


def save_solution_wrapper(solution, ch, filename='/home/niplav/proj/site/code/champagne/best_solution.json'):
    """Wrapper for save_solution that takes a Solution object."""
    save_solution(solution.waypoints, ch, N_WAYPOINTS, PENALTY_ALPHA, filename)

def evolve():
    """Run evolutionary optimization with ULTRA-FAST fitness."""
    ch = Choreography(n=5)

    print(f"Population: {POPULATION_SIZE}, Waypoints: {N_WAYPOINTS}, Generations: {N_GENERATIONS}")

    # Load best known fitness
    best_known_fitness = load_best_known_fitness('/home/niplav/proj/site/code/champagne/best_1.json')
    if best_known_fitness < float('inf'):
        print(f"Loaded best_1.json: fitness = {best_known_fitness:.4f}")

    population = initialize_population(POPULATION_SIZE, N_WAYPOINTS, ch)

    # Smart seeding
    from ultra_greedy import simulate_choreography_with_memory
    from itertools import permutations

    smart_seeds = 0

    # Seed with best_1.json if enabled (N_BEST_1_PERTURBATIONS > 0)
    if N_BEST_1_PERTURBATIONS > 0:
        best_1_waypoints = load_and_expand_best_solution(
            '/home/niplav/proj/site/code/champagne/best_1.json', N_WAYPOINTS)

        if best_1_waypoints is not None:
            # Add the exact solution
            population[smart_seeds] = Solution(waypoints=best_1_waypoints.copy())
            smart_seeds += 1

            # Add perturbed versions (small perturbations for local exploration)
            n_perturbations = min(N_BEST_1_PERTURBATIONS - 1, POPULATION_SIZE - smart_seeds)
            for i in range(n_perturbations):
                perturbed = best_1_waypoints + np.random.normal(0, 0.05, size=best_1_waypoints.shape)
                population[smart_seeds] = Solution(waypoints=perturbed)
                smart_seeds += 1

    # Seed with greedy heuristic if enabled (N_ULTRA_GREEDY_PERTURBATIONS > 0)
    if N_ULTRA_GREEDY_PERTURBATIONS > 0:
        best_order = ((0, 1, 2), (0, 3, 4), (1, 2, 3), (1, 2, 4))
        greedy_configs, _, _ = simulate_choreography_with_memory(best_order)

        if len(greedy_configs) == N_WAYPOINTS:
            seed_wp = np.array(greedy_configs)
            population[smart_seeds] = Solution(waypoints=seed_wp)
            smart_seeds += 1

            for i in range(min(N_ULTRA_GREEDY_PERTURBATIONS - 1, POPULATION_SIZE - smart_seeds)):
                perturbed = seed_wp + np.random.normal(0, 0.1, size=seed_wp.shape)
                population[smart_seeds] = Solution(waypoints=perturbed)
                smart_seeds += 1

    # Seed with triplet orderings if enabled (N_TRIPLET_ORDERINGS > 0)
    if N_TRIPLET_ORDERINGS > 0:
        triplets = [(0, 1, 2), (0, 3, 4), (1, 2, 3), (1, 2, 4)]
        for order in list(permutations(triplets))[:min(N_TRIPLET_ORDERINGS, POPULATION_SIZE - smart_seeds)]:
            configs, _, _ = simulate_choreography_with_memory(order)
            if len(configs) == N_WAYPOINTS:
                population[smart_seeds] = Solution(waypoints=np.array(configs))
                smart_seeds += 1

    # Create process pool
    pool = Pool(processes=N_PROCESSES) if USE_PARALLEL else None

    try:
        best_ever = None

        for gen in range(N_GENERATIONS):
            if USE_PARALLEL:
                evaluate_population_parallel(population, ch, pool)
            else:
                evaluate_population_serial(population, ch)

            # Sort by fitness
            population.sort(key=lambda s: s.fitness)

            # Apply local refinement to elite solutions periodically
            if gen > 0 and gen % LOCAL_REFINEMENT_FREQUENCY == 0:
                n_elite = max(1, int(POPULATION_SIZE * LOCAL_REFINEMENT_ELITE_FRACTION))
                print(f"Gen {gen:4d}: Applying local refinement to top {n_elite} solutions...")

                for i in range(n_elite):
                    refined = local_refine(population[i], ch, max_iter=LOCAL_REFINEMENT_MAX_ITER)
                    if refined.fitness < population[i].fitness:
                        population[i] = refined

                # Re-sort after refinement
                population.sort(key=lambda s: s.fitness)
                print(f"Gen {gen:4d}: Local refinement complete. Best fitness: {population[0].fitness:.4f}")

            # Track best and save if better than best_1.json
            if best_ever is None or population[0].fitness < best_ever.fitness:
                best_ever = Solution(waypoints=population[0].waypoints.copy(),
                                   fitness=population[0].fitness)

                # Save if better than best known
                if best_ever.fitness < best_known_fitness:
                    save_solution_wrapper(best_ever, ch)
                    print(f"Gen {gen:4d}: 🎉 new best {best_ever.fitness:.4f} (saved to best_solution.json)")
                    best_known_fitness = best_ever.fitness

            if gen % 10 == 0:
                print(f"Gen {gen:4d}: Best={population[0].fitness:.4f}, "
                      f"Avg={np.mean([s.fitness for s in population]):.4f}")

            # Selection
            n_survivors = int(POPULATION_SIZE * SURVIVAL_RATE)
            survivors = population[:n_survivors]

            # Create offspring
            offspring = []
            while len(offspring) < POPULATION_SIZE - n_survivors:
                p1, p2 = np.random.choice(survivors, size=2, replace=False)
                child = crossover(p1, p2)
                child = mutate(child, generation=gen)
                offspring.append(child)

            population = survivors + offspring

    finally:
        if pool:
            pool.close()
            pool.join()

    print(f"Best fitness: {best_ever.fitness:.4f}")

    # Validate best solution
    configs = [best_ever.waypoints[i] for i in range(N_WAYPOINTS)]
    all_touching = ch.get_all_touching_pairs(configs)
    path_length = ch.total_path_length(best_ever.waypoints)

    print(f"Path length: {path_length:.4f}")

    from vectorized_fitness import check_path_collisions_vectorized, build_full_trajectory
    full_traj = build_full_trajectory(best_ever.waypoints, ch.initial_positions)
    path_penalty = check_path_collisions_vectorized(full_traj, 2 * ch.radius)
    has_collisions = path_penalty > 0.01

    if len(all_touching) != 10:
        missing = set([(i, j) for i in range(5) for j in range(i + 1, 5)]) - all_touching
        print(f"✗ Missing: {missing}")

    # Final save (ensure best is saved even if no improvement happened)
    save_solution_wrapper(best_ever, ch)
    print(f"Final solution saved to best_solution.json")

    return best_ever


if __name__ == '__main__':
    import time
    best = evolve()
