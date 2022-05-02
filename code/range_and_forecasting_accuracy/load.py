import csv
import numpy as np
import scipy.stats as sps

daysec=24*60*60

def getpreds(s):
	pfile=open(s)
	predreader=csv.reader(pfile)
	preds=[]
	for entry in predreader:
		if entry[0][0]=="#":
			continue
		else:
			preds.append([int(entry[0]), float(entry[1])/daysec, float(entry[2]), float(entry[3]), float(entry[4])/daysec])
	preds=list(filter(lambda x: x[4]>=0, preds))
	return np.array(preds)

pb=getpreds("../../data/pb.csv").T
met=getpreds("../../data/met.csv").T

pbress=pb[2]
pbfcs=pb[3]
pbrngs=pb[4]

metress=met[2]
metfcs=met[3]
metrngs=met[4]

pbbriers=(pbfcs-pbress)**2
metbriers=(metfcs-metress)**2

mslope, mintercept, _, _, _=sps.linregress(metrngs, metbriers)
pslope, pintercept, _, _, _=sps.linregress(pbrngs, pbbriers)

metss=np.bincount(np.sort(np.floor(metrngs/30)).astype(int))
pbss=np.bincount(np.sort(np.floor(pbrngs/30)).astype(int))

def val_shrinking_dataset(briers, ranges):
	sortind=np.argsort(ranges)
	chronbriers=briers[sortind]
	chronranges=ranges[sortind]/30
	dropranges=[]
	pvalues=[]
	rvalues=[]
	for i in range(0, len(ranges)-2):
		_, _, rval, pval, _=sps.linregress(chronranges, chronbriers)
		pvalues.append(pval)
		rvalues.append(rval)
		dropranges.append(chronranges[0])
		chronranges=chronranges[1::]
		chronbriers=chronbriers[1::]
	return np.vstack([pvalues, rvalues, dropranges])

metpvals=val_shrinking_dataset(metbriers, metrngs)
pbpvals=val_shrinking_dataset(pbbriers, pbrngs)
