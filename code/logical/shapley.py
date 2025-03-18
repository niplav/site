import math
import numpy as np
import itertools as it

def v(vals):
	#For 0
	#return (not vals[0] and vals[1]) or (vals[1] and not vals[2])
	#For 1
	#return (vals[0] and vals[1]) or (not vals[1] and not vals[2])
	return (not vals[0] and vals[1]) or (not vals[1] and not vals[2])

def powerset(iterable):
	s = list(iterable)
	return it.chain.from_iterable(it.combinations(s, r) for r in range(len(s)+1))

def shapley(defaults_nonplay, defaults_play, player, v):
	n=len(defaults_play)

	defaults_play=np.array(defaults_play)
	defaults_nonplay=np.array(defaults_nonplay)

	playerset=set([player])
	without_player=set(range(n))-playerset

	sum=0
	for s in powerset(without_player):
		s_list=list(s)

		action=defaults_nonplay.copy()
		action[s_list]=defaults_play[s_list]

		action_withplayer=action.copy()
		action_withplayer[player]=defaults_play[player]

		ssize=len(s)
		mult=math.factorial(ssize)*math.factorial(n-ssize-1)/math.factorial(n)

		sum+=mult*(v(action_withplayer)-v(action))

	return sum
