# Over- and underprecision of probabilistic forecasts, via isotonic
# recalibration (PAV). Companion to algorithms.py, which rounds/noises
# in log-odds space.
#
# Overprecision is not a property of the forecasts alone, but the gap
# between two scales, measured in the same coordinate:
#	δ	the scale at which the forecaster *reports* distinctions
#	σ*	the scale at which those distinctions still carry information
# Overprecise iff δ ≪ σ*.

using Random, Statistics, Printf

brierscore(o, p)=mean((p.-o).^2)

logit(p)=log(p/(1-p))

# Fisher-Rao coordinate on the Bernoulli family, φ=2·asin(√p) ∈ [0,π].
#
# The Fisher information of a Bernoulli is 1/(p(1-p)), so the line
# element is ds²=dp²/(p(1-p))=dφ². Confusing p with a neighbour at
# distance Δφ therefore costs ~Δφ²/2 nats of expected log-score
# (=KL to second order), *the same everywhere on [0,1]*.
#
# Log-odds lacks this property: there the same confusion costs
# ~p(1-p)·Δx²/2, maximal at p=1/2 and vanishing in the tails, so a
# log-odds noise sweep under-penalises sloppy extreme forecasts.
# Log-odds is the right coordinate for *updating* (Bayes=addition),
# not for *perturbing*.
fisher(p)=2*asin(sqrt(clamp(p, 0, 1)))
unfisher(φ)=sin(clamp(φ, 0, π)/2)^2

const COORD=Dict(:prob=>identity, :logodds=>logit, :fisher=>fisher)

to_coord(f, space)=COORD[space].(clamp.(f, 1e-9, 1-1e-9))

# ---------------------------------------------------------------- PAV

# Pool-adjacent-violators on y, already sorted by the covariate, with
# weights w. Returns (vals, wts) of the pooled blocks, in order. Blocks
# with equal values are merged too, so vals is strictly increasing.
#
# Geometry: vals are the slopes of the greatest convex minorant of the
# cumulative-sum diagram (Σw, Σw·y). Least-squares projection onto the
# monotone cone {g: g₁≤…≤gₙ}; a cone, not a subspace, so the projection
# is only piecewise linear (linear within each pooling pattern).
function pav(y, w=ones(length(y)))
	vals=Float64[]
	wts=Float64[]
	for (yi, wi) in zip(y, w)
		push!(vals, yi)
		push!(wts, wi)
		while length(vals)>1 && vals[end-1]>=vals[end]
			ω=wts[end-1]+wts[end]
			v=(vals[end-1]*wts[end-1]+vals[end]*wts[end])/ω
			pop!(vals); pop!(wts)
			vals[end]=v; wts[end]=ω
		end
	end
	return vals, wts
end

# Isotonic recalibration map fitted on (f,y). Returns (g, vals, wts)
# where g is the fitted step function.
#
# PAV only sees the rank order of f, so the fit is identical under any
# strictly monotone reparametrisation of f (p, log-odds, φ, …). The bin
# edges sit wherever the outcome rate stops being monotone: a property
# of the data, not a choice of the analyst.
#
# Ties in f are pooled *before* PAV. Otherwise PAV may cut a block
# boundary through a group of identical forecasts (whenever their y's
# happen to arrive sorted), mapping the same input to different
# outputs. Real forecasters on a coarse grid are almost all ties, so
# this is not an edge case.
function iso_map(f, y)
	ord=sortperm(f)
	fs, ys=f[ord], Float64.(y[ord])
	uf=unique(fs)
	grp=[searchsorted(fs, x) for x in uf]
	vals, wts=pav([mean(ys[r]) for r in grp], length.(grp))
	# upper edge of each block = largest forecast in it
	cw=cumsum(length.(grp))
	edges=[uf[searchsortedfirst(cw, c)] for c in cumsum(wts)]
	g(x)=vals[min(searchsortedfirst(edges, x), length(vals))]
	return g, vals, wts
end

iso_levels(f, y)=length(iso_map(f, y)[2])

# ------------------------------------------------- honest evaluation

# In-sample isotonic Brier ≤ raw Brier by construction (the fit is a
# least-squares projection of y), so an in-sample "isotonic gap" is
# always positive and measures nothing. Everything below is
# cross-fitted: fit on k-1 folds, score on the held-out one.
function folds(n, k, rng)
	idx=shuffle(rng, 1:n)
	[idx[i:k:end] for i in 1:k]
end

function xval_bs(f, y; k=5, rng=Random.default_rng())
	tot=0.0
	for te in folds(length(f), k, rng)
		tr=setdiff(1:length(f), te)
		g=iso_map(f[tr], y[tr])[1]
		tot+=sum((g.(f[te]).-y[te]).^2)
	end
	return tot/length(f)
end

# Number of PAV blocks when the forecasts carry NO information, by
# permuting y against f. A permutation null rather than a formula,
# because the count depends on the forecaster's own tie structure.
#
# This is far from zero: the convex minorant of an n-step random walk
# has H_n≈ln n faces in expectation, so a useless forecaster with n
# distinct values gets ~ln n "supported levels" for free. Counting
# levels without this baseline is the easiest way to fool yourself.
function null_levels(f, y; reps=200, rng=Random.default_rng())
	ls=[iso_levels(f, shuffle(rng, y)) for _ in 1:reps]
	return mean(ls), std(ls)
end

# --------------------------------------------------- noise injection

# What a noise sweep measures, and why it has to be recalibrated:
#
# ① Without recalibration, zero-mean noise in p raises Brier by exactly
#	σ², for every forecaster: E[(p+ε-y)²]=(p-y)²+σ². In a curved
#	coordinate the rise depends on *where* the forecasts sit, which
#	is still not their information content.
# ② Noise in a curved coordinate also shifts the mean (logit-noise pulls
#	toward 1/2, by Jensen), which *helps* an overconfident forecaster
#	and confounds overprecision with overextremity.
#
# Recalibrating after noising fixes both, and has a clean reading:
# since iso_map only sees ranks, noising u=coord(f) is the same as
# randomly swapping forecasts that lie within ~σ of each other in that
# coordinate. The back-transform to [0,1] is irrelevant, so we skip it
# (which also avoids clamping noised values into artificial ties at
# the boundary). The coordinate's only job is to say which forecasts
# count as "close".
function noised_xval_bs(f, y, σ; space=:fisher, reps=20, k=5, rng=Random.default_rng())
	u=to_coord(f, space)
	mean(1:reps) do _
		xval_bs(u.+σ.*randn(rng, length(u)), y; k=k, rng=rng)
	end
end

# σ*: the largest noise the forecaster absorbs before the cross-fitted
# recalibrated Brier rises by more than tol. Distinctions finer than σ*
# are not recoverable from the track record. Censored to the range of
# σs: σ*=0 means "<σs[1]", σ*=σs[end] means "≥σs[end]".
#
# Default tol: an upper bound on 1 SE of the Brier score (per-item
# squared errors lie in [0,1], so by Bhatia–Davis Var≤b(1-b)).
function sigma_star(f, y; space=:fisher, tol=nothing, σs=exp10.(-2.5:0.125:0.5),
		reps=20, k=5, rng=Random.default_rng())
	base=xval_bs(f, y; k=k, rng=rng)
	tol===nothing && (tol=sqrt(base*(1-base)/length(f)))
	best=0.0
	curve=Tuple{Float64,Float64}[]
	for σ in σs
		s=noised_xval_bs(f, y, σ; space=space, reps=reps, k=k, rng=rng)
		push!(curve, (σ, s))
		# Stop at the FIRST failure, not the last pass: the curve is
		# monotone only in expectation, and one lucky draw at a huge σ
		# would otherwise certify a forecaster as maximally coarse.
		s>base+tol && break
		best=σ
	end
	return best, base, curve
end

# δ: median gap between adjacent distinct reported values, in the same
# coordinate as σ*. Median rather than minimum, for robustness.
function report_scale(f; space=:fisher)
	u=sort(unique(round.(to_coord(f, space), digits=9)))
	length(u)<2 && return Inf
	return median(diff(u))
end

# ------------------------------------------------------ the verdict

# bits=log2(σ*/δ), floored at 0: how many binary digits of reported
# granularity the track record fails to support.
#
# This tests for overprecision only; underprecision is *not
# identifiable* from (f,y) alone.
#	Overprecision: destroy their distinctions, observe nothing lost.
#		A manipulation you can actually perform on the track record.
#	Underprecision: you'd have to split a reported level into finer
#		ones and observe a gain, but within a level all forecasts are
#		identical, so there is nothing to split on.
# Detecting underprecision needs an outside signal: a covariate, a
# second forecaster, a later revision. A negative log2(σ*/δ) just means
# "reports coarsely, tolerates lots of noise", which is what a
# calibrated low-resolution forecaster looks like.
function overprecision(f, y; space=:fisher, k=5, reps=20, rng=Random.default_rng())
	σ, base, curve=sigma_star(f, y; space=space, k=k, reps=reps, rng=rng)
	δ=report_scale(f; space=space)
	lv=iso_levels(f, y)
	nl, ns=null_levels(f, y; rng=rng)
	ratio=log2(σ/δ)
	return (n=length(f),
		reported=length(unique(round.(f, digits=9))),
		levels=lv, null_levels=nl, levels_z=(lv-nl)/max(ns, 1e-9),
		bs_raw=brierscore(y, f), bs_xval_iso=base,
		δ=δ, σ_star=σ, ratio=ratio, bits=max(0.0, ratio),
		curve=curve)
end

# ---------------------------------------------------------- demo

function demo(; n=8000, seed=1)
	rng=MersenneTwister(seed)

	# ① a forecaster with genuinely 8 levels of signal, reporting them
	grid=range(0.1, 0.9, length=8)
	truep=[grid[1+(i%8)] for i in 1:n]
	y=Float64.(rand(rng, n).<truep)
	earned=copy(truep)

	# ② same signal, but reported with meaningless fine-grained jitter
	over=clamp.(unfisher.(fisher.(truep).+0.20.*randn(rng, n)), 1e-4, 1-1e-4)

	# ③ same signal, thrown away: two levels only
	coarse=[p<0.5 ? 0.3 : 0.7 for p in truep]

	# ④ no signal at all, but reported to four decimal places
	noise=clamp.(0.5.+0.2.*randn(rng, n), 1e-4, 1-1e-4)
	ynoise=Float64.(rand(rng, n).<0.5)

	println("case          reported  levels  null   bs      δ       σ*     over(bits)")
	for (nm, ff, yy) in (("earned-fine", earned, y), ("overprecise", over, y),
			("coarse", coarse, y), ("pure-noise", noise, ynoise))
		r=overprecision(ff, yy; rng=MersenneTwister(seed))
		@printf("%-13s %7d  %5d  %5.1f  %.4f  %.4f  %.4f  %5.2f\n",
			nm, r.reported, r.levels, r.null_levels, r.bs_raw, r.δ, r.σ_star, r.bits)
	end
end

(abspath(PROGRAM_FILE)==@__FILE__) && demo()
