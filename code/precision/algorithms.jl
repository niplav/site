# Isotonic/PAV-based over- and underprecision metrics for probabilistic
# forecasts. Companion to algorithms.py, which does the rounding/noising
# in log-odds space.
#
# Central claim: "overprecision" is *not* a property of the forecasts
# alone. It is the gap between two scales:
#	δ	the scale at which the forecaster *reports* distinctions
#	σ*	the scale at which their distinctions still carry information
# Overprecise iff δ ≪ σ*, underprecise iff δ ≫ σ*.
#
# Both scales have to be measured in the same coordinate on [0,1], and
# the coordinate is not arbitrary: see fisher() below.

using Random, Statistics, Printf

brierscore(o, p)=mean((p.-o).^2)
logscore(o, p)=mean(@. o*log(p)+(1-o)*log(1-p))

logit(p)=log(p/(1-p))
logistic(x)=1/(1+exp(-x))

# Fisher-Rao arclength on the Bernoulli 1-simplex, φ=2·asin(√p) ∈ [0,π].
# The Fisher information of a Bernoulli in the parameter p is 1/(p(1-p)),
# so the natural line element is ds²=dp²/(p(1-p)); substituting
# p=sin²(φ/2) gives ds²=dφ². I.e. this is the *unique* (up to affine
# maps) coordinate in which a perturbation of fixed size costs the same
# expected log-score no matter where on [0,1] it is applied, ~σ²/2.
#
# Log-odds does NOT have this property: a logit-perturbation of size σ
# costs ~p(1-p)σ²/2·(something), maximal at p=1/2 and vanishing in the
# tails, so a log-odds noise sweep systematically under-penalises sloppy
# extreme forecasts. Log-odds is the natural coordinate for *updating*
# (Bayes = addition), not for *perturbing*.
fisher(p)=2*asin(sqrt(clamp(p, 0, 1)))
unfisher(φ)=sin(clamp(φ, 0, π)/2)^2

const COORD=Dict(
	:prob=>(identity, identity),
	:logodds=>(logit, logistic),
	:fisher=>(fisher, unfisher))

# ---------------------------------------------------------------- PAV

# Pool-adjacent-violators. Input must already be sorted by the covariate.
# Returns (vals, counts) for the pooled blocks, in order.
#
# Geometry: the fitted values are the slopes of the greatest convex
# minorant of the cumulative sum k ↦ Σ_{i≤k} y_(i). Slopes of a convex
# function are non-decreasing, which is exactly the isotonicity
# constraint; the GCM is the highest convex function below the
# cumulative staircase, and least-squares projection onto the monotone
# cone M={g: g_1≤…≤g_n} is what that GCM computes. M is a polyhedral
# cone, not a subspace, so there is no projection *matrix*: the map is
# piecewise linear, linear only within each face (= each pooling
# pattern).
function pav(y, w=ones(length(y)))
	vals=Float64[]
	wts=Float64[]
	for (yi, wi) in zip(y, w)
		push!(vals, yi)
		push!(wts, wi)
		while length(vals)>1 && vals[end-1]>vals[end]
			v=(vals[end-1]*wts[end-1]+vals[end]*wts[end])/(wts[end-1]+wts[end])
			ω=wts[end-1]+wts[end]
			pop!(vals); pop!(wts); pop!(vals); pop!(wts)
			push!(vals, v); push!(wts, ω)
		end
	end
	return vals, wts
end

# Isotonic recalibration map fitted on (f,y). Returns a callable step
# function. Because pav() only sees the *rank order* of f, the fitted
# blocks are invariant under any strictly monotone reparameterisation of
# f (probabilities, log-odds, φ, logit³ — all identical). This is the
# answer to "why bins here and not there": the bin edges are wherever
# the empirical outcome rate stops being monotone, which is a property
# of the data, not of the analyst.
#
# Ties in f must be pooled *before* PAV, not left to it: PAV run on the
# raw sorted sequence will happily place a block boundary in the middle
# of a group of identical forecasts (whenever their y's happen to arrive
# in sorted order), producing a "recalibration map" that returns
# different values for the same input. Forecasters on a coarse grid —
# i.e. every real Metaculus/Manifold user — are almost all ties, so this
# is not an edge case.
function iso_map(f, y)
	ord=sortperm(f)
	fs, ys=f[ord], Float64.(y[ord])
	uf=Float64[]; um=Float64[]; uw=Float64[]
	i=1
	while i<=length(fs)
		j=i
		while j<length(fs) && fs[j+1]==fs[i]; j+=1 end
		push!(uf, fs[i]); push!(um, mean(ys[i:j])); push!(uw, j-i+1)
		i=j+1
	end
	vals, wts=pav(um, uw)
	edges=Float64[]
	k=0
	for ω in wts
		c=0.0
		while k<length(uw) && c<ω-1e-9; k+=1; c+=uw[k] end
		push!(edges, uf[k])
	end
	return x->vals[min(searchsortedfirst(edges, x), length(vals))], vals, wts
end

iso_fit(f, y)=(g=iso_map(f, y)[1]; [g(x) for x in f])
iso_levels(f, y)=length(unique(round.(iso_map(f, y)[2], digits=9)))

# ------------------------------------------------- honest evaluation

# In-sample isotonic Brier is always ≤ raw Brier, by construction (the
# fit is the least-squares projection of y). So an in-sample "isotonic
# gap" is guaranteed positive and measures nothing. Everything below is
# cross-fitted: the map is estimated on k-1 folds and scored on the
# held-out one.
function folds(n, k, rng)
	idx=shuffle(rng, 1:n)
	[idx[i:k:end] for i in 1:k]
end

function xval_bs(f, y; k=5, rng=Random.default_rng())
	fs=folds(length(f), k, rng)
	tot=0.0
	for te in fs
		tr=setdiff(1:length(f), te)
		g=iso_map(f[tr], y[tr])[1]
		tot+=sum((g.(f[te]).-y[te]).^2)
	end
	return tot/length(f)
end

# Number of PAV blocks expected when the forecasts carry NO information,
# obtained by permuting y against f. This has to be a permutation null
# rather than a formula, because the count depends on the forecaster's
# own tie structure.
#
# It is emphatically not zero: the greatest convex minorant of a random
# walk of length n has ~H_n ≈ ln n vertices, so an entirely uninformative
# forecaster reporting n distinct values still gets ~log(n) "supported
# levels" for free. Counting isotonic levels without this baseline is
# the main way to fool yourself with this method — a naive count of
# "levels PAV kept" reads as evidence of resolution when it is just the
# arithmetic of random walks.
function null_levels(f, y; reps=200, rng=Random.default_rng())
	ls=[iso_levels(f, shuffle(rng, y)) for _ in 1:reps]
	return mean(ls), std(ls)
end

# --------------------------------------------------- noise injection

# Naive noise injection has two failure modes, both fixed here.
#
# (1) In probability space, zero-mean noise raises the Brier score by
#	exactly σ², always: E[(p+ε-y)²]=(p-y)²+σ². So the sweep is a
#	constant, and tells you nothing. The information content only
#	shows up because noise in a *curved* coordinate is not mean-
#	preserving in p.
# (2) That non-mean-preservation is itself a confound: logit-noise pulls
#	forecasts toward 1/2 (logistic is convex below 1/2, concave
#	above), so it *helps* an overconfident forecaster. A naive sweep
#	therefore measures a mixture of overprecision and overextremity.
#
# Fix: recalibrate after noising. Then the shift is absorbed by the
# monotone map and only the *destroyed information* is left, which is
# what we wanted to measure all along.
function noised_xval_bs(f, y, σ; space=:fisher, reps=20, k=5, rng=Random.default_rng())
	fwd, bwd=COORD[space]
	u=fwd.(clamp.(f, 1e-9, 1-1e-9))
	mean(1:reps) do _
		fn=bwd.(u.+σ.*randn(rng, length(u)))
		xval_bs(clamp.(fn, 1e-9, 1-1e-9), y; k=k, rng=rng)
	end
end

# σ* — the largest perturbation the forecaster can absorb before the
# cross-fitted, re-calibrated score degrades by more than tol (in Brier
# units). This is the *resolution scale* of the forecaster: distinctions
# finer than σ* are not recoverable from their track record.
function sigma_star(f, y; space=:fisher, tol=nothing, σs=exp10.(-2.5:0.125:0.5),
		reps=20, k=5, rng=Random.default_rng())
	base=xval_bs(f, y; k=k, rng=rng)
	tol===nothing && (tol=sqrt(base*(1-base)/length(f)))	# ~1 SE
	best=0.0
	curve=Tuple{Float64,Float64}[]
	for σ in σs
		s=noised_xval_bs(f, y, σ; space=space, reps=reps, k=k, rng=rng)
		push!(curve, (σ, s))
		# stop at the FIRST failure rather than keeping the last pass:
		# the degradation curve is monotone in expectation but noisy in
		# any finite sample, and taking the last pass lets one lucky
		# draw at a huge σ certify a forecaster as maximally coarse.
		s>base+tol && break
		best=σ
	end
	return best, base, curve
end

# δ — the scale at which the forecaster actually reports distinctions,
# in the same coordinate. Median gap between adjacent distinct reported
# values; robust to a few outliers, unlike the minimum.
function report_scale(f; space=:fisher)
	fwd, _=COORD[space]
	u=sort(unique(round.(fwd.(clamp.(f, 1e-9, 1-1e-9)), digits=9)))
	length(u)<2 && return Inf
	return median(diff(u))
end

# ------------------------------------------------------ the verdict

# bits = log2(σ*/δ), floored at 0: how many binary digits of reported
# granularity the track record fails to support.
#
# THE ASYMMETRY, which is the main conceptual result here: this is a
# test for overprecision only. Underprecision is *not identifiable*
# from (f,y) alone. To show someone is overprecise you destroy their
# distinctions and observe that nothing was lost — a manipulation you
# can actually perform on their track record. To show someone is
# underprecise you would have to split one of their reported levels
# into finer ones and observe a gain, but within a reported level every
# forecast is by definition identical, so there is no variable to split
# on. Underprecision only becomes visible with an outside source of
# signal: a covariate, a second forecaster, a later revision by the
# same forecaster. A negative log2(σ*/δ) means "reports coarsely and
# has a wide noise tolerance", which is what a well-calibrated
# low-resolution forecaster looks like, not evidence of withheld
# information.
function overprecision(f, y; space=:fisher, k=5, reps=20, rng=Random.default_rng())
	σ, base, curve=sigma_star(f, y; space=space, k=k, reps=reps, rng=rng)
	δ=report_scale(f; space=space)
	lv=iso_levels(f, y)
	nl, ns=null_levels(f, y; rng=rng)
	ratio=δ>0 ? log2(σ/δ) : Inf
	return (n=length(f),
		reported=length(unique(round.(f, digits=9))),
		levels=lv, null_levels=nl, excess_levels=(lv-nl)/max(ns, 1e-9),
		bs_raw=brierscore(y, f), bs_xval_iso=base,
		δ=δ, σ_star=σ, ratio=ratio, bits=max(0.0, ratio),
		curve=curve)
end

# ------------------------------------------------- decomposition aid

# H(F) bounds resolution: I(F;Y) ≤ H(F). "Precision" in the purely
# descriptive sense is H(F), a property of the forecasts alone and
# morally neutral. The part of it that is wasted is H(F|Y)=H(F)-I(F;Y).
function shannon(f; bins=20)
	h=zeros(bins)
	for x in f
		h[clamp(1+floor(Int, x*bins), 1, bins)]+=1
	end
	p=h./sum(h)
	-sum(pi>0 ? pi*log2(pi) : 0.0 for pi in p)
end

# ---------------------------------------------------------- demo

function demo(; n=8000, seed=1)
	rng=MersenneTwister(seed)

	# ① a forecaster with genuinely 8 levels of signal, reporting them
	grid=range(0.1, 0.9, length=8)
	truep=[grid[1+(i%8)] for i in 1:n]
	y=Float64.(rand(rng, n).<truep)
	earned=copy(truep)

	# ② same signal, but reported on a 1e-4 grid with meaningless jitter
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
