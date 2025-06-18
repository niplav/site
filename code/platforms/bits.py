import pymc as pm
import numpy as np
import arviz as az
import matplotlib.pyplot as plt

def mcmc_market_analysis(distances, null_sigma=1.0):
    """
    PyMC analysis of market performance using half-normal model.

    Model: distances ~ HalfNormal(σ)
    Prior: σ ~ HalfNormal(1.0)  # Weakly informative

    Compare against null hypotheses with fixed σ values.
    """
    distances = np.array(distances)

    # Adaptive model with uncertain σ
    with pm.Model() as adaptive_model:
        σ = pm.HalfNormal('sigma', sigma=null_sigma)
        pm.HalfNormal('distances', sigma=σ, observed=distances)

        # Sample posterior
        trace = pm.sample(2000, tune=1000, chains=4, target_accept=0.98, return_inferencedata=True)

    # Print results
    print("Posterior summary:")
    print(az.summary(trace, var_names=['sigma']))
    print()

    # Calculate marginal likelihood via importance sampling
    # (PyMC doesn't give you marginal likelihood directly)
    with adaptive_model:
        # Use SMC sampler for marginal likelihood estimate
        smc_trace = pm.sample_smc(2000, chains=4, return_inferencedata=True)
        adaptive_log_ml = smc_trace.log_marginal_likelihood

    print(f"Adaptive model log marginal likelihood: {adaptive_log_ml:.3f}")
    print()

    # Compare against null models with fixed σ
    results = {}

    # Calculate likelihood under null hypothesis
    log_likelihood_null = np.sum(pm.HalfNormal.logp(distances, sigma=null_sigma).eval())

    # Bayes factor and evidence
    log_bf = adaptive_log_ml - log_likelihood_null
    bits = log_bf / np.log(2)

    results = {
        'log_likelihood': log_likelihood_null,
        'log_bayes_factor': log_bf,
        'bits_evidence': bits,
        'bayes_factor': np.exp(log_bf)
    }

    print(f"Null hypothesis σ = {null_sigma}:")
    print(f"  Log likelihood: {log_likelihood_null:.3f}")
    print(f"  Evidence: {bits:.2f} bits")
    print(f"  Bayes factor: {np.exp(log_bf):.1f}:1 in favor of adaptive")
    print()

    return trace, results

def plot_dists():
    # Plot posterior
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Posterior of σ
    az.plot_posterior(trace, var_names=['sigma'], ax=axes[0])
    axes[0].set_title('Posterior of σ (Half-Normal scale)')

    # Prior vs posterior comparison
    σ_samples = trace.posterior.sigma.values.flatten()
    axes[1].hist(σ_samples, bins=50, alpha=0.7, density=True, label='Posterior')

    # Plot prior
    σ_range = np.linspace(0, 2, 1000)
    prior_density = 2 * (1/0.5) * (1/np.sqrt(2*np.pi)) * np.exp(-σ_range**2 / (2*0.5**2))
    axes[1].plot(σ_range, prior_density, 'r-', label='Prior')

    axes[1].set_xlabel('σ')
    axes[1].set_ylabel('Density')
    axes[1].set_title('Prior vs Posterior')
    axes[1].legend()

    plt.tight_layout()
    plt.show()

    return trace, results

# Run the analysis
if __name__ == "__main__":
    # Your market data: distances from perfect performance
    distances = [0.326, 0.333]

    print("Half-Normal Model for Market Performance")
    print("=" * 50)
    print("Interpretation:")
    print("- Small σ → consistently excellent markets (close to perfect)")
    print("- Large σ → inconsistent/poor markets (far from perfect)")
    print("- Evidence > 0 → support for adaptive model over fixed σ")
    print()

    trace, results = mcmc_market_analysis(distances)

    print("\n=== Summary ===")
    σ_mean = trace.posterior.sigma.mean().item()
    σ_hdi = az.hdi(trace.posterior.sigma, hdi_prob=0.95)

    print(f"Posterior mean σ: {σ_mean:.3f}")
    print(f"95% HDI: [{σ_hdi[0]:.3f}, {σ_hdi[1]:.3f}]")
    print(f"Interpretation: Markets have consistent performance")
    print(f"with typical distance from perfect ≈ {σ_mean:.2f}")

    # Best evidence estimate
    best_bits = max(r['bits_evidence'] for r in results.values())
    print(f"\nBest evidence estimate: {best_bits:.1f} bits")
    print("(for your meme title!)")
