import numpy as np
import nashpy

N=1000

def player_payoffs(a, b, astrat, bstrat):
	apayoff=np.sum(astrat[:,None]*a*bstrat)
	bpayoff=np.sum(astrat[:,None]*b*bstrat)
	return apayoff, bpayoff

all_ameans=[]
all_bmeans=[]
all_taken_ameans=[]
all_taken_bmeans=[]

for i in range(0, N):
	a=np.random.rand(4, 3)
	b=np.random.rand(4, 3)

	game=nashpy.Game(a, b)
	equilibria=game.vertex_enumeration()

	apayoffs=[]
	bpayoffs=[]

	for equilibrium in equilibria:
		astrat=equilibrium[0]
		bstrat=equilibrium[1]
		apayoff, bpayoff=player_payoffs(a, b, astrat, bstrat)
		apayoffs+=[apayoff]
		bpayoffs+=[bpayoff]
		print("normal: ", apayoff, bpayoff)

	all_ameans+=[np.mean(apayoffs)]
	all_bmeans+=[np.mean(bpayoffs)]

	print("mean payoffs: ", np.mean(apayoffs), np.mean(bpayoffs))

	# Taking option away from a/row player
	taken_a=a[1:,]
	taken_b=b[1:,]
	taken_game=nashpy.Game(taken_a, taken_b)
	equilibria=taken_game.vertex_enumeration()

	taken_apayoffs=[]
	taken_bpayoffs=[]

	for equilibrium in equilibria:
		taken_astrat=equilibrium[0]
		taken_bstrat=equilibrium[1]
		taken_apayoff, taken_bpayoff=player_payoffs(taken_a, taken_b, taken_astrat, taken_bstrat)
		taken_apayoffs+=[taken_apayoff]
		taken_bpayoffs+=[taken_bpayoff]
		print("taken: ", taken_apayoff, taken_bpayoff)

	all_taken_ameans+=[np.mean(taken_apayoffs)]
	all_taken_bmeans+=[np.mean(taken_bpayoffs)]

	print("mean taken_payoffs: ", np.mean(taken_apayoffs), np.mean(taken_bpayoffs))

	print("-----------------")

all_ameans=np.array(all_ameans)
all_bmeans=np.array(all_bmeans)

all_taken_ameans=np.array(all_taken_ameans)
all_taken_bmeans=np.array(all_taken_bmeans)
