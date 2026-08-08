# toy scaling laws for the fitness-value of casual sex
# (see daygame.md, Appendix D)
#
# deps: Plots
# run:  julia scaling.jl

using Plots

gr()

# ============================================================
# Age-fertility curve
#
# Stylized logistic decline in per-cycle conception probability
# with age, anchored loosely to reproductive-epidemiology figures
# (peak natural fecundability ~0.20-0.25/cycle in the early-to-mid
# 20s, half-max around late 30s, near-zero by mid-40s — see e.g.
# Dunson, Colombo & Baird 2002). Not a precise demographic fit,
# just illustrative of the shape.
# ============================================================

const FERT_MAX  = 0.25
const FERT_MID  = 38.0   # age of half-max decline
const FERT_SLOPE = 4.5   # smaller = sharper cliff

fertility(n) = FERT_MAX / (1 + exp((n - FERT_MID) / FERT_SLOPE))

# ============================================================
# Value of m "chances" (fertile-cycle exposures) with one partner
# of age n: saturating in m because each additional chance only
# covers the probability mass the previous ones missed. Evolution
# doesn't know about contraception, so m counts opportunities, not
# just literal acts.
# ============================================================

chance(n, m) = 1 - (1 - fertility(n))^m

# Paternal-investment discount: value of a raw conception, translated
# into offspring-survived-to-reproduce-equivalents. Fixed here as a
# stylized constant per the zero-investment idealization; in reality
# this is where most of the real-world casual-sex discount lives.
const W_SURV = 1.0

value(n, m) = W_SURV * chance(n, m)

# ============================================================
# Plots
# ============================================================

function plot_fertility()
	ns = 16:1:50
	p = plot(ns, fertility.(ns), linewidth=2, color=:black, legend=false,
	         xlabel="Partner age n", ylabel="Per-cycle conception probability",
	         title="Stylized age-fertility curve", size=(900,600), dpi=150)
	savefig(p, "scaling_fertility.png")
end

function plot_value_vs_m()
	ms = 1:1:20
	p = plot(xlabel="Chances m (fertile-cycle exposures)", ylabel="Value(n, m)",
	         title="Diminishing returns within a partner, by age",
	         legend=:outertopright, size=(900,600), dpi=150)
	for n in (20, 25, 30, 35, 40, 45)
		plot!(p, ms, value.(n, ms), linewidth=2, marker=:circle, markersize=3,
		      label="n=$n")
	end
	savefig(p, "scaling_value_m.png")
end

function plot_heatmap()
	ns = 18:50
	ms = 1:20
	zs = [value(n, m) for m in ms, n in ns]
	p = heatmap(ns, ms, zs, xlabel="Partner age n", ylabel="Chances m",
	            title="Value(n, m)", size=(900,600), dpi=150)
	savefig(p, "scaling_heatmap.png")
end

# ============================================================
# Speculative extension: perceived effective population size N_e
# as an input to the value function.
#
# This is NOT a rigorous derivation — Gillespie's variance-in-offspring-
# number effect is a population-level statement about allele-frequency
# drift over many generations, not a per-decision utility. But if we
# indulge the idea that organisms carry some density/N_e-sensing cue
# that tunes a risk-aversion knob, the natural toy is a mean-variance
# (mean minus variance-penalty) utility over a strategy of k independent
# partners at fixed (n, m):
#
#   mean       mu(n,m,k)     = k * chance(n,m)
#   variance   sigma2(n,m,k) = k * chance(n,m) * (1 - chance(n,m))
#   utility    U(n,m,k;Ne)   = mu - gamma(Ne) * sigma2
#
# with gamma(Ne) a risk-aversion coefficient, decreasing in Ne (large
# perceived population -> drift negligible -> ordinary EV-maximization;
# small perceived population -> drift matters -> discount variance).
# The marginal value of pursuing one more (n,m)-partner is then
#
#   dU/dk = chance(n,m) * (1 - gamma(Ne) * (1 - chance(n,m)))
#
# which can go negative for low-chance (low m, older n) partners once
# gamma(Ne) is large enough — i.e. a small enough perceived Ne should
# push the model away from spreading across many uncertain partners
# and toward concentrating on fewer, surer ones (raising m with an
# existing partner rather than raising k with new ones), since
# chance*(1-chance) is maximized at chance=0.5 and vanishes as
# chance->1.
#
# RISK_CONST is an arbitrary illustrative constant, not fit to
# anything — it just sets where the crossover becomes visible on a
# plausible range of Ne.
# ============================================================

const RISK_CONST = 1000.0

gamma_risk(Ne) = RISK_CONST / Ne

marginal_value(n, m, Ne) = let c = chance(n, m)
	c * (1 - gamma_risk(Ne) * (1 - c))
end

function plot_Ne_effect()
	ms = 1:1:20
	n = 25
	p = plot(xlabel="Chances m with one partner (age n=$n)",
	         ylabel="Marginal value of one more partner at (n,m)",
	         title="Perceived N_e reweighting the mean-variance tradeoff (toy)",
	         legend=:outertopright, size=(900,600), dpi=150)
	hline!(p, [0.0], color=:gray, linestyle=:dash, label="")
	for Ne in (10, 100, 1_000, 10_000, 1_000_000)
		plot!(p, ms, marginal_value.(n, ms, Ne), linewidth=2, marker=:circle,
		      markersize=3, label="N_e=$Ne")
	end
	savefig(p, "scaling_Ne.png")
end

plot_fertility()
plot_value_vs_m()
plot_heatmap()
plot_Ne_effect()
@info "scaling plots done"
