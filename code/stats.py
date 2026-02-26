import numpy as np
import scipy.stats as scistat

def log_likelihood(data, mu, std):
	data_probs=scistat.norm.pdf(data, loc=mu, scale=std)
	cleaned_data=data_probs[np.nonzero(~np.isnan(data_probs))]
	return np.sum(np.log(cleaned_data))

def control_likelihood_ratio_statistic(active, placebo):
	placebo_log_lh=log_likelihood(active, placebo.mean(), placebo.std())
	active_log_lh=log_likelihood(active, active.mean(), active.std())
	return 2 * (active_log_lh - placebo_log_lh)

def llrt_pval(lmbda, df=2):
	return scistat.chi2.cdf(df, lmbda)
