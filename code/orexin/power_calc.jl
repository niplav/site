#!/usr/bin/env julia
#=
Power calculation for the orexin-A v2 trial (2 mg dose).
Paired crossover, m participants, k pairs (orexin/control sessions) each.

The honest constraint: difference scores are correlated within a participant,
so collecting more sessions per person yields diminishing returns. With m
participants and intraclass correlation ρ of the difference scores,

    n_eff = m*k / (1 + (k-1)*ρ)        (design effect)

and as k -> ∞, n_eff -> m/ρ. More sessions can't buy you past that floor;
only more participants can.

Three power estimates, from optimistic to conservative:
  power_indep  -- treat all m*k pairs as independent (ignores clustering). Upper bound.
  power_deff   -- design-effect-adjusted via n_eff, df = n_eff - 1. The realistic number.
  power_pmean  -- collapse to per-participant mean differences, t-test on m points,
                  df = m-1. Bulletproof but brutal (df=2 when m=3).
sim_power Monte-Carlos the per-participant-mean test to validate power_pmean.
=#

using Distributions, Printf, Random

Random.seed!(42)

# --- analytical power ---

function crit(df, α, sided)
	quantile(TDist(df), sided == 2 ? 1 - α/2 : 1 - α)
end

function pow_from_nct(df, λ, tc, sided)
	nct = NoncentralT(df, λ)
	sided == 2 ? (1 - cdf(nct, tc)) + cdf(nct, -tc) : 1 - cdf(nct, tc)
end

# all m*k pairs treated as independent -- anticonservative upper bound
function power_indep(d_z, k, m; α=0.05, sided=2)
	n = m * k
	df = n - 1
	λ = sqrt(n) * d_z
	pow_from_nct(df, λ, crit(df, α, sided), sided)
end

# design-effect adjusted: realistic
function power_deff(d_z, k, m, ρ; α=0.05, sided=2)
	n_eff = m * k / (1 + (k - 1) * ρ)
	df = max(n_eff - 1, 1.0)
	λ = sqrt(n_eff) * d_z
	pow_from_nct(df, λ, crit(df, α, sided), sided)
end

# per-participant means, t-test on m points (df = m-1): conservative
function power_pmean(d_z, k, m, ρ; α=0.05, sided=2)
	df = m - 1
	λ = sqrt(m) * d_z / sqrt(ρ + (1 - ρ) / k)
	pow_from_nct(df, λ, crit(df, α, sided), sided)
end

# Monte-Carlo check of power_pmean (total difference-score SD fixed to 1)
function sim_power(d_z, k, m, ρ; α=0.05, sided=2, nsim=20000)
	τ = sqrt(ρ); σ = sqrt(1 - ρ); β = d_z
	tc = crit(m - 1, α, sided)
	rej = 0
	for _ in 1:nsim
		means = [β + τ * randn() + (σ / sqrt(k)) * randn() for _ in 1:m]
		t = mean(means) / (std(means) / sqrt(m))
		hit = sided == 2 ? abs(t) > tc : t > tc
		rej += hit
	end
	rej / nsim
end

# smallest k reaching target power (per-participant-mean test); 0 if unreachable
function required_k(d_z, m, ρ, target; α=0.05, sided=2, kmax=200)
	for k in 1:kmax
		power_pmean(d_z, k, m, ρ; α, sided) >= target && return k
	end
	0
end

function ceiling_power(d_z, m, ρ; α=0.05, sided=2)
	# k -> ∞ limit of power_pmean: λ -> sqrt(m/ρ)*d_z, df = m-1
	df = m - 1
	λ = ρ > 0 ? sqrt(m / ρ) * d_z : Inf
	isinf(λ) ? 1.0 : pow_from_nct(df, λ, crit(df, α, sided), sided)
end

# --- report ---

function main()
	m = 3
	α = 0.05
	sided = 2
	ks = [4, 6, 8, 10, 12, 16, 20, 30]
	dzs = [0.15, 0.3, 0.5, 0.8]   # 0.15 ≈ old sleep-duration effect; rest are hopes
	ρs = [0.0, 0.1, 0.3, 0.5]

	println("Orexin-A v2 power: m=$m participants, two-sided α=$α")
	println("d_z = standardized within-pair effect (mean diff / SD of diffs)")
	println("="^72)

	# sanity: analytic vs simulation for power_pmean
	println("\nValidation (power_pmean analytic vs Monte-Carlo), ρ=0.3:")
	@printf("  %-6s %-4s %10s %10s\n", "d_z", "k", "analytic", "sim")
	for d_z in (0.3, 0.5, 0.8), k in (6, 12)
		a = power_pmean(d_z, k, m, 0.3; α, sided)
		s = sim_power(d_z, k, m, 0.3; α, sided)
		@printf("  %-6.2f %-4d %10.3f %10.3f\n", d_z, k, a, s)
	end

	# the diminishing-returns ceiling
	println("\nPower ceiling as k -> ∞ (per-participant-mean test, m=$m):")
	@printf("  %-8s", "ρ \\ d_z")
	for d_z in dzs; @printf("%9.2f", d_z); end
	println()
	for ρ in ρs
		@printf("  %-8.2f", ρ)
		for d_z in dzs
			@printf("%9.3f", ρ == 0 ? 1.0 : ceiling_power(d_z, m, ρ; α, sided))
		end
		println()
	end
	println("  (ρ=0 is the no-clustering fantasy; real ρ for diff-scores is usually 0.1-0.4)")

	# main grid: realistic (design-effect) power
	for ρ in [0.1, 0.3]
		println("\n" * "-"^72)
		println("REALISTIC power_deff, ρ=$ρ   (rows=d_z, cols=k pairs/participant)")
		@printf("  %-8s", "d_z \\ k")
		for k in ks; @printf("%7d", k); end
		println()
		for d_z in dzs
			@printf("  %-8.2f", d_z)
			for k in ks
				@printf("%7.2f", power_deff(d_z, k, m, ρ; α, sided))
			end
			println()
		end
	end

	# optimistic upper bound for contrast
	println("\n" * "-"^72)
	println("OPTIMISTIC power_indep (clustering ignored -- upper bound only)")
	@printf("  %-8s", "d_z \\ k")
	for k in ks; @printf("%7d", k); end
	println()
	for d_z in dzs
		@printf("  %-8.2f", d_z)
		for k in ks
			@printf("%7.2f", power_indep(d_z, k, m; α, sided))
		end
		println()
	end

	# required k for 80% power, conservative test
	println("\n" * "-"^72)
	println("Sessions/participant for 80% power (power_pmean, conservative):")
	@printf("  %-8s %8s %8s %8s\n", "d_z", "ρ=0.1", "ρ=0.3", "ρ=0.5")
	for d_z in dzs
		@printf("  %-8.2f", d_z)
		for ρ in [0.1, 0.3, 0.5]
			k = required_k(d_z, m, ρ, 0.80; α, sided)
			@printf("%8s", k == 0 ? "∞" : string(k))
		end
		println()
	end
	println("\n('∞' = unreachable at this m no matter how many sessions -- add participants.)")
end

main()
