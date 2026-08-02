import csv
import statistics
import numpy as np
import scipy.stats as sps
import scipy.optimize as spo
from sklearn.linear_model import LogisticRegression

daysec=24*60*60

def brier(x, y):
	return np.mean((x-y)**2)

def getpreds(s):
	pfile=open(s)
	predreader=csv.reader(pfile)
	preds=[]
	for entry in predreader:
		if entry[0][0]=="#":
			continue
		else:
			preds.append([int(entry[0]), float(entry[1])/daysec, float(entry[2]), float(entry[3]), float(entry[4])/daysec])
	preds=list(filter(lambda x: x[4]>0, preds))
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

# Why not do a linear regression on the transformed data? Because that ends up below 0
# Transformation is np.log((1/metbriers)-1)

def shrunk_logistic(x, slope, intercept):
	return 0.25*1/(1+np.exp(slope*x+intercept))

# Intercept not limited to positive range (point for 0.125 can be negative)
pblogifit=spo.curve_fit(shrunk_logistic, pbrngs, pbbriers, bounds=([-np.inf, -np.inf], [0, np.inf]))
metlogifit=spo.curve_fit(shrunk_logistic, metrngs, metbriers, bounds=([-np.inf, -np.inf], [0, np.inf]))

# Intercept limited to positive range

pblogifit=spo.curve_fit(shrunk_logistic, pbrngs, pbbriers, bounds=([-np.inf, 0], [0, np.inf]))
metlogifit=spo.curve_fit(shrunk_logistic, metrngs, metbriers, bounds=([-np.inf, 0], [0, np.inf]))

def shift_exp(x, b):
	return ((b**x)-1)/(-4)

pbexpfit=spo.curve_fit(shift_exp, pbrngs, pbbriers, bounds=([0], [1]))
metexpfit=spo.curve_fit(shift_exp, metrngs, metbriers, bounds=([0], [1]))

### Between Questions

def group(d):
	a=[]
	for e in np.unique(d[0]):
		indices=np.where(d[0]==e)
		a.append([e, d[1][indices[0][0]], d[2][indices], d[3][indices], d[4][indices]])
	return a

metquestions=group(met)
pbquestions=group(pb)

metqbrier=np.array([[i[1], brier(i[3], i[2])] for i in metquestions])
pbqbrier=np.array([[i[1], brier(i[3], i[2])] for i in pbquestions])

mqslope, mqintercept, _, _, _=sps.linregress(metqbrier.T[0], metqbrier.T[1])
pbqslope, pbqintercept, _, _, _=sps.linregress(pbqbrier.T[0], pbqbrier.T[1])

wmetqbrier=[[i[4], (i[3]-i[2])**2] for i in metquestions]
wpbqbrier=[[i[4], (i[3]-i[2])**2] for i in pbquestions]

wmetqbrier=list(filter(lambda x: len(x[0])>1, wmetqbrier))
wpbqbrier=list(filter(lambda x: len(x[0])>1, wpbqbrier))

wpbqbrier=list(filter(lambda x: not (x[0][0]==x[0][1] and len(x[0]==2) and x[1][0]==x[1][1] and len(x[1])==2), wpbqbrier))

wmetqregs=list(map(lambda x: sps.linregress(x[0], x[1]), wmetqbrier))
wpbqregs=list(map(lambda x: sps.linregress(x[0], x[1]), wpbqbrier))

pblogifit_betweenq=spo.curve_fit(shrunk_logistic, pbqbrier.T[0], pbqbrier.T[1], bounds=([-np.inf, 0], [0, np.inf]))
metlogifit_betweenq=spo.curve_fit(shrunk_logistic, metqbrier.T[0], metqbrier.T[1], bounds=([-np.inf, 0], [0, np.inf]))

pbexpfit_betweenq=spo.curve_fit(shift_exp, pbqbrier.T[0], pbqbrier.T[1], bounds=([0], [1]))
metexpfit_betweenq=spo.curve_fit(shift_exp, metqbrier.T[0], metqbrier.T[1], bounds=([0], [1]))

clean_metforecasts=np.sum([len(wmetqbrier[i][0]) for i in range(0, len(wmetqbrier))])
awmetqslope=np.sum([len(wmetqbrier[i][0])*wmetqregs[i][0] for i in range(0, len(wmetqregs))])/clean_metforecasts
awmetqintercept=np.sum([len(wmetqbrier[i][0])*wmetqregs[i][1] for i in range(0, len(wmetqregs))])/clean_metforecasts

clean_pbforecasts=np.sum([len(wpbqbrier[i][0]) for i in range(0, len(wpbqbrier))])
awpbqslope=np.sum([len(wpbqbrier[i][0])*wpbqregs[i][0] for i in range(0, len(wpbqregs))])/clean_pbforecasts
awpbqintercept=np.sum([len(wpbqbrier[i][0])*wpbqregs[i][1] for i in range(0, len(wpbqregs))])/clean_pbforecasts

fwpbqbrier=list(filter(lambda x: len(x[0])>=10, wpbqbrier))
fwpbqregs=list(map(lambda x: sps.linregress(x[0], x[1]), fwpbqbrier))
clean_fpbforecasts=np.sum([len(fwpbqbrier[i][0]) for i in range(0, len(fwpbqbrier))])
fawpbqslope=np.sum([len(fwpbqbrier[i][0])*fwpbqregs[i][0] for i in range(0, len(fwpbqregs))])/clean_fpbforecasts
fawpbqintercept=np.sum([len(fwpbqbrier[i][0])*fwpbqregs[i][1] for i in range(0, len(fwpbqregs))])/clean_fpbforecasts

within_logi_fits_met=[]

for e in wmetqbrier:
	try:
		within_logi_fits_met.append(spo.curve_fit(shrunk_logistic, e[0], e[1], bounds=([-np.inf, 0], [0, np.inf])))
	except RuntimeError:
		within_logi_fits_met.append([])
		continue

within_logi_fits_pb=[]

for e in fwpbqbrier:
	try:
		within_logi_fits_pb.append(spo.curve_fit(shrunk_logistic, e[0], e[1], bounds=([-np.inf, 0], [0, np.inf])))
	except RuntimeError:
		within_logi_fits_pb.append([])
		continue

within_logi_fits_met_filt=list(filter(lambda x: len(x)>0, within_logi_fits_met))
within_logi_fits_pb_filt=list(filter(lambda x: len(x)>0, within_logi_fits_pb))

met_logi_horizons=[(np.log((1/0.96)-1)-f[0][1])/f[0][0] for f in within_logi_fits_met_filt]
pb_logi_horizons=[(np.log((1/0.96)-1)-f[0][1])/f[0][0] for f in within_logi_fits_pb_filt]

within_exp_fits_met=[spo.curve_fit(shift_exp, e[0], e[1], bounds=([0], [1])) for e in wmetqbrier]
within_exp_fits_pb=[spo.curve_fit(shift_exp, e[0], e[1], bounds=([0], [1])) for e in fwpbqbrier]

met_exp_horizons=[np.log(0.04)/np.log(f[0][0]) for f in within_exp_fits_met]
pb_exp_horizons=[np.log(0.04)/np.log(f[0][0]) for f in within_exp_fits_pb]
