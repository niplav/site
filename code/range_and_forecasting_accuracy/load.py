import csv
import numpy as np
import scipy as sp

def getpreds(s):
	pfile=open(s)
	predreader=csv.reader(pfile)
	preds=[]
	for entry in predreader:
		if entry[0][0]=="#":
			continue
		else:
			preds.append([int(entry[0]), float(entry[1]), float(entry[2]), float(entry[3]), float(entry[4])])
	preds=list(filter(lambda x: x[4]>=0, preds))
	return np.array(preds)

pb=getpreds("../../data/pb.csv")
met=getpreds("../../data/met.csv")

pbress=pb[2]
pbfcs=pb[3]
pbrngs=pb[4]

metress=met[2]
metfcs=met[3]
metrngs=met[4]

pbbriers=(pbfcs-pbress)**2
metbriers=(metfcs-metress)**2
