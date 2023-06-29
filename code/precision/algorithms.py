import csv
import statistics
import numpy as np

def mse(o,p):
	return np.mean(np.abs(o-p)**2)

def logit(p):
	return np.log(p/(1-p))

def logistic(p):
	return 1/(1+np.exp(-p))

def perturbed_score_difference(forecasts, perturbation=1, samples=100):
	o=forecasts[0]
	p=forecasts[1]
	score=mse(o,p)
	pert_scores=[]
	for i in range(0,samples):
		perturbed=logistic(logit(p)+np.random.default_rng().uniform(-perturbation/2,perturbation/2,len(p)))
		pert_scores.append(mse(o,perturbed))
	return np.mean(pert_scores)-score

def score_differences(forecasts, samples=100, low=0, high=100, div=100):
	return np.array([[s/div, perturbed_score_difference(d1, perturbation=s/div, samples=samples)] for s in range(low,high)]).T

def precision(forecasts, samples=100):
	differences_list=score_differences(forecasts, samples)

d1=np.array([[1,0.8],[0,0.4],[0,0.65],[1,0.99]]).T
oc=d1[0]
pr=d1[1]

d2=np.array([[1,0.8],[0,0.4],[0,0.65],[1,0.9]]).T
oc2=d1[0]
pr2=d1[1]

d3=np.array([[0,0.8],[1,0.4],[1,0.65],[0,0.9]]).T
oc3=d1[0]
pr3=d1[1]

differences1=score_differences(d1, samples=1000, low=0, high=25, div=50)
differences2=score_differences(d1, samples=1000, low=0, high=25, div=50)
differences3=score_differences(d1, samples=1000, low=0, high=25, div=50)
