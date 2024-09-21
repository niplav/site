import numpy as np
import nashpy
from itertools import product
import matplotlib.pyplot as plt
import seaborn as sns

NUM_SAMPLES = 2000  # Number of games to sample for each size combination
LIMIT_SUM=12

def player_payoffs(a, b, astrat, bstrat):
	apayoff = np.sum(astrat[:, None] * a * bstrat)
	bpayoff = np.sum(astrat[:, None] * b * bstrat)
	return apayoff, bpayoff

def calculate_equilibria_payoffs(game):
	equilibria = game.vertex_enumeration()
	payoffs = [player_payoffs(game.payoff_matrices[0], game.payoff_matrices[1], *eq) for eq in equilibria]
	return payoffs

def simulate_games():
	all_results = {}

	for a_actions, b_actions in product(range(3, 10), range(3, 10)):
		if a_actions + b_actions > LIMIT_SUM:
			continue

		print(f"\nSimulating games with {a_actions} × {b_actions} actions")

		game_results = []

		for _ in range(NUM_SAMPLES):
			a = np.random.rand(a_actions, b_actions)
			b = np.random.rand(a_actions, b_actions)

			# Normal game
			normal_game = nashpy.Game(a, b)
			normal_payoffs = calculate_equilibria_payoffs(normal_game)

			# Games with option taken away from a/row player
			taken_a = np.delete(a, 0, axis=0)
			taken_b = np.delete(b, 0, axis=0)

			taken_game = nashpy.Game(taken_a, taken_b)
			taken_payoffs = calculate_equilibria_payoffs(taken_game)

			game_results.append({
				'normal': normal_payoffs,
				'taken': taken_payoffs
			})

		all_results[(a_actions, b_actions)] = game_results

	return all_results

def analyze_payoff_changes(all_results):
	payoff_changes = {
		'A': {},
		'B': {}
	}

	for (a_actions, b_actions), game_results in all_results.items():
		payoff_changes['A'][(a_actions, b_actions)] = []
		payoff_changes['B'][(a_actions, b_actions)] = []

		for result in game_results:
			normal_payoffs = result['normal']
			taken_payoffs = result['taken']

			normal_mean = np.mean(normal_payoffs, axis=0) if normal_payoffs else (0, 0)
			taken_mean = np.mean(taken_payoffs, axis=0) if taken_payoffs else (0, 0)

			for player_idx, player in enumerate(['A', 'B']):
				change = taken_mean[player_idx] - normal_mean[player_idx]
				payoff_changes[player][(a_actions, b_actions)].append(change)

	return payoff_changes

def create_heatmap(payoff_changes, player, mode='i'):
	"""change: whether the change was an improvement ('i'), no change
	('n'), or worsening ('w')"""
	game_sizes = sorted(payoff_changes.keys())
	data = []

	for size in game_sizes:
		changes = payoff_changes[size]
		if mode=='i':
			improved = sum(1 for change in changes if change > 0)
		elif mode=='n':
			improved = sum(1 for change in changes if change == 0)
		elif mode=='w':
			improved = sum(1 for change in changes if change < 0)
		total = len(changes)

		if total > 0:
			improvement_ratio = improved / total
		else:
			improvement_ratio = 0

		data.append([size[0], size[1], improvement_ratio])

	data = np.array(data)

	plt.figure(figsize=(12, 10))
	heatmap = plt.scatter(data[:, 1], data[:, 0], c=data[:, 2], s=500, cmap='RdYlGn', vmin=0, vmax=1)
	plt.colorbar(heatmap)

	if mode=='i':
		plt.title(f'Ratio of Improved Games for Player {player} When Removing Options from A')
	elif mode=='n':
		plt.title(f'Ratio of Unchanged Games for Player {player} When Removing Options from A')
	elif mode=='w':
		plt.title(f'Ratio of Worsened Games for Player {player} When Removing Options from A')

	plt.xlabel('Player B Actions')
	plt.ylabel('Player A Actions')

	plt.xticks(range(3, 10))
	plt.yticks(range(3, 10))

	plt.grid(True)

	for i, txt in enumerate(data[:, 2]):
		plt.annotate(f'{txt:.2f}', (data[i, 1], data[i, 0]), ha='center', va='center')

	# Save the plot as a PNG file
	plt.savefig(f'./player_{player}_{mode}.png', dpi=300, bbox_inches='tight')
	plt.close()  # Close the figure to free up memory

# Run the simulation
all_results = simulate_games()

print("\nSimulation complete. Results stored in all_results dictionary.")

# Assuming all_results is available from the previous simulation
payoff_changes = analyze_payoff_changes(all_results)

# Create heatmaps for both players and save as PNG files
create_heatmap(payoff_changes['A'], 'A', mode='i')
create_heatmap(payoff_changes['B'], 'B', mode='i')

create_heatmap(payoff_changes['A'], 'A', mode='n')
create_heatmap(payoff_changes['B'], 'B', mode='n')

create_heatmap(payoff_changes['A'], 'A', mode='w')
create_heatmap(payoff_changes['B'], 'B', mode='w')

print("All plots have been saved in the 'plots' directory.")
