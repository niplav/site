# Regressional Goodhart vs. dimensionality.
#
# Thesis: regressional Goodhart only scales with dimension d through the
# proxy's noise-to-signal budget d*s^2 / ||beta||^2.  Whether high d is
# catastrophic is entirely about whether the true signal ||beta||^2 grows
# with d (dimension-proof) or stays O(1) (alignment decays as 1/sqrt(d)).
#
# Two models:
#   align_sphere : true=<b,x>, proxy=<b+eta,x>, optimize over ||x||<=1.
#                  Exact: realized value = ||b|| * cos<(b, b+eta).
#                  Closed form rho ~ 1 / sqrt(1 + d*s^2/||b||^2).
#   align_bestn  : finite optimization pressure (best of n candidates),
#                  lets heavy-tailed error + d compound a la Kwa & Thomas.

using LinearAlgebra, Statistics, Distributions, Random

iqr(D) = quantile(D, 0.75) - quantile(D, 0.25)

# build beta with chosen ||beta||^2 = sig2 (only ||beta|| matters on the sphere)
make_beta(d, sig2) = fill(sqrt(sig2 / d), d)

# IQR-match an arbitrary noise dist to N(0,s) so light/heavy tails are comparable
unit_scale(noise, s) = s / (iqr(noise) / iqr(Normal()))

"""
    align_sphere(d; s, sig2, noise, reps)

Mean alignment rho = cos<(beta, beta+eta) for per-coordinate error scale `s`.
rho=1 is no Goodhart, rho=0 is total. Compare against `rho_closed`.
"""
function align_sphere(d; s=0.3, sig2=1.0, noise=Normal(), reps=4000,
                      rng=MersenneTwister(1))
	beta = make_beta(d, sig2)
	bn2  = dot(beta, beta)
	sc   = unit_scale(noise, s)
	acc  = 0.0
	for _ in 1:reps
		bhat = beta .+ sc .* rand(rng, noise, d)
		acc += dot(beta, bhat) / (sqrt(bn2) * norm(bhat))
	end
	acc / reps
end

# closed-form Gaussian prediction (light tails, large d)
rho_closed(d; s=0.3, sig2=1.0) = 1 / sqrt(1 + d * s^2 / sig2)

"""
    align_bestn(d; n, s, sig2, noise, reps)

Best-of-n: draw n candidate options x~N(0,I), score by proxy U=<beta+eta,x>,
return E[V(argmax U)] / E[max V]  (oracle-normalized). n is optimization pressure.
"""
function align_bestn(d; n=1000, s=0.3, sig2=1.0, noise=Normal(), reps=400,
                     rng=MersenneTwister(1))
	beta = make_beta(d, sig2)
	sc   = unit_scale(noise, s)
	vprx = 0.0; vbst = 0.0
	for _ in 1:reps
		bhat = beta .+ sc .* rand(rng, noise, d)   # fixed misweighting this run
		X = randn(rng, d, n)
		V = X' * beta
		U = X' * bhat
		vprx += V[argmax(U)]
		vbst += maximum(V)
	end
	vprx / vbst
end

# ---- demos --------------------------------------------------------------
if abspath(PROGRAM_FILE) == @__FILE__
	println("== sphere model, fixed per-coord error s=0.3 ==")
	println("concentrated signal (||b||^2=1): alignment should fall ~1/sqrt(d)")
	for d in (1, 2, 4, 16, 64, 256, 1024)
		mc = align_sphere(d; s=0.3, sig2=1.0)
		th = rho_closed(d; s=0.3, sig2=1.0)
		println("  d=$(lpad(d,4))  rho_mc=$(round(mc,digits=3))  rho_closed=$(round(th,digits=3))")
	end
	println("extensive signal (||b||^2=d): alignment should stay flat")
	for d in (1, 16, 256, 1024)
		mc = align_sphere(d; s=0.3, sig2=Float64(d))
		println("  d=$(lpad(d,4))  rho_mc=$(round(mc,digits=3))")
	end
	println("== heavy vs light tails compound with d (||b||^2=1, s=0.3) ==")
	for d in (4, 64, 1024)
		lt = align_sphere(d; s=0.3, sig2=1.0, noise=Normal())
		ht = align_sphere(d; s=0.3, sig2=1.0, noise=TDist(1.5)) # heavy (var->inf-ish)
		println("  d=$(lpad(d,4))  normal=$(round(lt,digits=3))  student-t(1.5)=$(round(ht,digits=3))")
	end
	println("== best-of-n: optimization pressure x dimension (||b||^2=1) ==")
	for n in (10, 100, 10_000)
		row = [round(align_bestn(d; n=n, s=0.3, sig2=1.0), digits=3) for d in (4,64,1024)]
		println("  n=$(lpad(n,6))  d=4,64,1024 -> $row")
	end
end
