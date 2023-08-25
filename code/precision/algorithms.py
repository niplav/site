import csv
import time
import statistics
import numpy as np

def brierscore(o,p):
	return np.mean(np.abs(o-p)**2)

def logscore(o,p):
	return o*np.log(p)+(1-o)*np.log(1-p)

def logit(p):
	return np.log(p/(1-p))

def logistic(p):
	return 1/(1+np.exp(-p))

def perturbed_score(forecasts, perturbation=1, samples=100):
	o=forecasts[0]
	p=forecasts[1]
	pert_scores=[]
	for i in range(0,samples):
		perturbed=logistic(logit(p)+np.random.default_rng(seed=time.monotonic_ns()).uniform(-perturbation/2,perturbation/2,len(p)))
		pert_scores.append(logscore(o,perturbed))
	return np.mean(pert_scores)

def logodds_rounded_score(forecasts, precision=1):
	p=forecasts[1]
	lo=logit(p)
	rounded_lo=precision*np.round(lo/precision)
	rounded_probs=logistic(rounded_lo)
	return np.mean(logscore(forecasts[0], rounded_probs))

def lo_precision_scores(forecasts, samples=100, low=10e-4, high=10, change=2, mode='round', stepmode='exp'):
	p=low
	deg_scores=[]
	while p<high:
		if mode=='round':
			deg_scores=deg_scores+[[p, logodds_rounded_score(forecasts, precision=p)]]
		elif mode=='pert':
			deg_scores=deg_scores+[[p, perturbed_score(forecasts, perturbation=p, samples=samples)]]
		if stepmode=='exp':
			p=p*change
		elif stepmode=='lin':
			p=p+change
	return np.array(deg_scores).T

def prob_rounded_score(forecasts, precision=0.1):
	p=forecasts[1]
	rounded_probs=precision*np.round(p/precision)
	rounded_probs[np.where(rounded_probs>=1)]=1-precision
	rounded_probs[np.where(rounded_probs<=0)]=precision
	return np.mean(logscore(forecasts[0], rounded_probs))

def prob_precision_scores(forecasts, samples=100, low=10e-4, high=0.5, change=0.01, stepmode='lin'):
	p=low
	deg_scores=[]
	while p<high:
		deg_scores=deg_scores+[[p, prob_rounded_score(forecasts, precision=p)]]

		if stepmode=='exp':
			p=p*change
		elif stepmode=='lin':
			p=p+change
	return np.array(deg_scores).T

d1=np.array([[1,0.8],[0,0.4],[0,0.65],[1,0.99]]).T
oc=d1[0]
pr=d1[1]

d2=np.array([[1,0.8],[0,0.4],[0,0.65],[1,0.9]]).T
oc2=d1[0]
pr2=d1[1]

d3=np.array([[0,0.8],[1,0.4],[1,0.65],[0,0.9]]).T
oc3=d1[0]
pr3=d1[1]

def syndata(buckets=10, bucket_samples=10):
	probs=np.repeat(np.arange(0.001, 1, 1/buckets)[:,None], bucket_samples)
	outcomes=np.int32(np.random.default_rng(seed=time.monotonic_ns()).uniform(size=buckets*bucket_samples)<probs)
	return np.vstack((outcomes, probs))

d4=syndata(buckets=10, bucket_samples=10)
d5=syndata(buckets=2, bucket_samples=50)
d6=syndata(buckets=20, bucket_samples=100)

lo_round_scores_1=lo_precision_scores(d1, change=1.1, high=10)
lo_round_scores_2=lo_precision_scores(d2, change=1.1, high=10)
lo_round_scores_3=lo_precision_scores(d3, change=1.1, high=10)
lo_round_scores_4=lo_precision_scores(d4, change=1.1, high=10)
lo_round_scores_5=lo_precision_scores(d5, change=1.1, high=10)
lo_round_scores_6=lo_precision_scores(d6, change=1.1, high=10)

lo_pert_scores_1=lo_precision_scores(d1, change=1.2, mode='pert', samples=500, high=10)
lo_pert_scores_2=lo_precision_scores(d2, change=1.2, mode='pert', samples=500, high=10)
lo_pert_scores_3=lo_precision_scores(d3, change=1.2, mode='pert', samples=500, high=10)
lo_pert_scores_4=lo_precision_scores(d4, change=1.2, mode='pert', samples=500, high=10)
lo_pert_scores_5=lo_precision_scores(d5, change=1.2, mode='pert', samples=500, high=10)
lo_pert_scores_6=lo_precision_scores(d6, change=1.2, mode='pert', samples=500, high=10)

p_round_scores_1=prob_precision_scores(d1)
p_round_scores_2=prob_precision_scores(d2)
p_round_scores_3=prob_precision_scores(d3)
p_round_scores_4=prob_precision_scores(d4)
p_round_scores_5=prob_precision_scores(d5)
p_round_scores_6=prob_precision_scores(d6)
