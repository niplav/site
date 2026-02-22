import pymc as pm
import numpy as np
import arviz as az
import matplotlib.pyplot as plt
from scipy import stats

def mcmc_market_analysis(distances, null_sigmas=[0.7]):
	"""
	PyMC analysis of market performance using half-normal model.

	Model: distances ~ HalfNormal(σ)
	Prior: σ ~ HalfNormal(0.5)

	Calculate Bayes factors by comparing likelihoods.
	"""
	distances = np.array(distances)

	with pm.Model() as adaptive_model:
		σ = pm.HalfNormal('sigma', sigma=0.5)
		obs = pm.HalfNormal('distances', sigma=σ, observed=distances)
		trace = pm.sample(2000, tune=1000, chains=4, target_accept=0.95,
						 return_inferencedata=True)

	print("Posterior summary:")
	print(az.summary(trace, var_names=['sigma']))
	print()

	σ_samples = trace.posterior.sigma.values.flatten()
	σ_mean = np.mean(σ_samples)

	print(f"Posterior mean σ: {σ_mean:.3f}")
	print()

	# Calculate Bayes factors against null hypotheses
	results = {}
	null_σ = null_sigmas[0]
	# Likelihood under adaptive model (at posterior mean)
	ll_adaptive = np.sum(stats.halfnorm.logpdf(distances, scale=σ_mean))

	# Likelihood under null model (fixed σ)
	ll_null = np.sum(stats.halfnorm.logpdf(distances, scale=null_σ))

	# Bayes factor and evidence
	log_bf = ll_adaptive - ll_null
	bits = log_bf / np.log(2)
	bf = np.exp(log_bf)

	results = {
		'σ_mean': σ_mean,
		'll_adaptive': ll_adaptive,
		'll_null': ll_null,
		'log_bf': log_bf,
		'bits': bits,
		'bf': bf
	}

	print(f"vs Null σ = {null_σ}:")
	print(f"  Log likelihood (adaptive): {ll_adaptive:.3f}")
	print(f"  Log likelihood (null): {ll_null:.3f}")
	print(f"  Evidence: {bits:.2f} bits")
	print(f"  Bayes factor: {bf:.1f}:1 in favor of adaptive")

	return trace, results

def plot_analysis(trace, distances):
	"""Plot posterior and model diagnostics"""
	fig, axes = plt.subplots(1, 2, figsize=(9, 4))

	# Posterior of σ
	az.plot_posterior(trace, var_names=['sigma'], ax=axes[0])
	axes[0].set_title('Posterior of σ')

	# Prior vs posterior
	σ_samples = trace.posterior.sigma.values.flatten()
	axes[1].hist(σ_samples, bins=50, alpha=0.7, density=True, label='Posterior')

	# Plot prior HalfNormal(0.5)
	σ_range = np.linspace(0, 1.5, 1000)
	prior_density = stats.halfnorm.pdf(σ_range, scale=0.5)
	axes[1].plot(σ_range, prior_density, 'r-', label='Prior HN(0.5)')

	axes[1].set_xlabel('σ')
	axes[1].set_ylabel('Density')
	axes[1].set_title('Prior vs Posterior')
	axes[1].legend()

	plt.tight_layout()
	plt.savefig('update.png')

if __name__ == "__main__":
	# Market data: distances from perfect performance
	# pomodoro: 0.326, vitamin D: 0.333, lumenator: 0.429
	distances = [0.326, 0.333, 0.429]

	trace, results = mcmc_market_analysis(distances)

	σ_hdi = az.hdi(trace.posterior.sigma, hdi_prob=0.95)

	print(f"Posterior mean σ: {results['σ_mean']:.3f}")
	print(f"95% credible interval: [{σ_hdi.sigma.values[0]:.3f}, {σ_hdi.sigma.values[1]:.3f}]")

	bits = results['bits']

	print(f"\nEvidence: {bits:.3f} bits")
	print(f"(vs null hypothesis σ = 0.7)")

	plot_analysis(trace, distances)
