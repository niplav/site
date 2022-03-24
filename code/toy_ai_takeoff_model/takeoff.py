import random
import numpy as np

exec(open("ndim_diamond_square.py").read())

def climb(space, pos, size, dim):
	"""At position pos in space, do some kind of climbing."""
	return climb_dim(space, pos, size, dim)

def climb_dim(space, pos, size, dim):
	"""Look in direction of each dimension (not two dimensions at
	once), then choose maximum spot."""
	maxpos=np.array(pos)
	for i in range(0, dim):
		pos[i]+=1
		if 0<=pos[i]<size:
			if space[tuple(pos)]>space[tuple(maxpos)]:
					maxpos=np.array(pos)
		pos[i]-=2
		if 0<=pos[i]<size:
			if space[tuple(pos)]>space[tuple(maxpos)]:
				maxpos=np.array(pos)
		pos[i]+=1
	return maxpos

def climb_hypcub(space, pos):
	"""Look one unit-hypercube around, choose maximum."""
	return pos

def search_around(space, pos, size, dim, intelligence):
	"""At position pos in space, dependent on current optimization
	power, search around in the neighbouring space to find the
	minimum in the subspace searched. This subspace can be an n-ball
	or an n-cube."""
	step=round(intelligence**(2/dim))
	subpos=[slice(0,0)]*dim
	for i in range(0, dim):
		subpos[i]=slice(max(0,pos[i]-step), min(size-1, pos[i]+step))
	subsection=space[tuple(subpos)]
	mp=np.where(subsection == np.amax(subsection))
	pos=np.array([list(mp[i])[0]+subpos[i].start for i in range(0, dim)])
	return pos

def datagen(dim, size, minval, maxval, extrfact, rounds, growth):
	filename=str(dim) + "_" + str(size) + "_" + str(extrfact) + "_" + str(growth) + ".csv"

	f=open(filename, "w+")
	space=create_space(dim, size, minval, maxval, extrfact)
	factor=1

	pos=[random.randint(0, size-1) for i in range(0, dim)]

	for i in range(0, rounds):
		factor*=growth
		intelligence=max(1, space[tuple(pos)])*factor
		f.write(str(space[tuple(pos)]) + "," + str(intelligence) + "\n")

		pos=climb(space, pos, size, dim)
		pos=search_around(space, pos, size, dim, intelligence)

	f.close()

datagen(1, 8193, 0, 256, 0.5, 2048, 1.001)
datagen(1, 16385, 0, 256, 0.5, 2048, 1.001)
datagen(1, 32769, 0, 256, 0.5, 2048, 1.001)
datagen(1, 65537, 0, 256, 0.5, 2048, 1.001)
datagen(1, 1048577, 0, 256, 0.5, 2048, 1.001)
datagen(1, 16777217, 0, 256, 0.5, 2048, 1.001)
datagen(2, 4097, 0, 256, 0.5, 2048, 1.001)		# 16785409
datagen(3, 65, 0, 256, 0.5, 2048, 1.001)		# 274625
datagen(3, 129, 0, 256, 0.5, 2048, 1.001)		# 2146689
datagen(3, 257, 0, 256, 0.5, 2048, 1.001)		# 16974593
datagen(4, 65, 0, 256, 0.5, 2048, 1.001)		# 17850625
datagen(5, 33, 0, 256, 0.5, 2048, 1.001)		# 39135393
datagen(6, 17, 0, 256, 0.5, 2048, 1.001)		# 24137569
datagen(8, 9, 0, 256, 0.5, 2048, 1.001)			# 43046721
