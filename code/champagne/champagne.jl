#!/usr/bin/env julia
#=
Champagne Toasting Problem Solver

Find minimum total path length for n disks on a regular n-gon
such that every pair touches (center distance = 2r) and no pair
intersects (center distance ≥ 2r at all times).

APPROACH TRADE-OFFS:
────────────────────
• Gradient-based (L-BFGS): Fast local convergence. Works well for
  n ≤ ~15 with finite differences. Needs good initialization.
• Brute-force / evolutionary (DE, CMA-ES): Better global search,
  but slower. Good for n ≤ ~10 with reasonable compute.
• Mathematical / structural: Round-robin scheduling determines
  meeting order optimally. For large n, this combinatorial structure
  is essential—pure optimization chokes on the exponential landscape.

This solver uses multi-restart L-BFGS with progressive penalty
weighting and tournament-aware initialization. Constraint checking
is ANALYTICAL: exact quadratic minimization over each linear segment,
not sampling.

Usage:
  julia champagne.jl -n 6
  julia champagne.jl -n 6 -w 14 -d 3.0 -r 0.1 --restarts 100
  julia champagne.jl -n 10 --method multi
=#

using LinearAlgebra
using Optim
using JSON
using Random
using Printf
using Dates

# ── Geometry ──────────────────────────────────────────────────

"""Regular n-gon vertices with given edge length. Returns n×2 matrix."""
function polygon_positions(n::Int, edge_len::Float64)
	R = edge_len / (2 * sin(π / n))  # circumradius
	pos = Matrix{Float64}(undef, n, 2)
	for k in 0:n-1
		θ = π/2 + 2π*k/n
		pos[k+1, 1] = R * cos(θ)
		pos[k+1, 2] = R * sin(θ)
	end
	pos
end

"""
Exact minimum distance between two linearly-moving points over t ∈ [0,1].

P₁(t) = p1a + t·(p1b - p1a),  P₂(t) = p2a + t·(p2b - p2a)
|P₁(t) - P₂(t)|² = at² + bt + c  (quadratic in t)
Minimized at t* = -b/(2a), clamped to [0,1].
"""
function seg_min_dist(p1ax, p1ay, p1bx, p1by, p2ax, p2ay, p2bx, p2by)
	ux = p1ax - p2ax
	uy = p1ay - p2ay
	vx = (p1bx - p1ax) - (p2bx - p2ax)
	vy = (p1by - p1ay) - (p2by - p2ay)
	a = vx*vx + vy*vy
	b = 2(ux*vx + uy*vy)
	c = ux*ux + uy*uy
	if a < 1e-15
		return sqrt(max(c, 0.0))
	end
	t = clamp(-b / (2a), 0.0, 1.0)
	sqrt(max(a*t*t + b*t + c, 0.0))
end

# ── Trajectory encoding ──────────────────────────────────────
# Internal layout: traj[dim, point, disk]
# dim ∈ {1,2}, point ∈ 1:nw+2, disk ∈ 1:n
# point 1 = initial, points 2:nw+1 = waypoints, point nw+2 = return

function decode!(traj, x, n, nw, pos0)
	idx = 0
	@inbounds for i in 1:n
		traj[1, 1, i] = pos0[i, 1]
		traj[2, 1, i] = pos0[i, 2]
		for k in 1:nw
			traj[1, k+1, i] = x[idx + 1]
			traj[2, k+1, i] = x[idx + 2]
			idx += 2
		end
		traj[1, nw+2, i] = pos0[i, 1]
		traj[2, nw+2, i] = pos0[i, 2]
	end
	traj
end

function path_length(traj, n, n_seg)
	pl = 0.0
	@inbounds for i in 1:n, s in 1:n_seg
		dx = traj[1, s+1, i] - traj[1, s, i]
		dy = traj[2, s+1, i] - traj[2, s, i]
		pl += sqrt(dx*dx + dy*dy)
	end
	pl
end

# ── Analytical verification ──────────────────────────────────

struct VerifyResult
	path_length::Float64
	n_touched::Int
	total_pairs::Int
	all_touched::Bool
	violations::Vector{Tuple{Int,Int,Int,Float64}}
	valid::Bool
end

"""
Rigorous analytical verification.

For each pair and each linear segment, computes the EXACT minimum
distance via closed-form quadratic minimization—no sampling.

With do_sample_check=true, also cross-validates by sampling 1000
points per segment.
"""
function verify(traj, r; tol=1e-3, do_sample_check=false)
	n = size(traj, 3)
	n_seg = size(traj, 2) - 1
	two_r = 2r
	pl = path_length(traj, n, n_seg)

	n_touched = 0
	violations = Tuple{Int,Int,Int,Float64}[]

	for i in 1:n, j in (i+1):n
		pair_min = Inf
		for s in 1:n_seg
			d = seg_min_dist(
				traj[1,s,i], traj[2,s,i], traj[1,s+1,i], traj[2,s+1,i],
				traj[1,s,j], traj[2,s,j], traj[1,s+1,j], traj[2,s+1,j])
			pair_min = min(pair_min, d)
			if d < two_r - tol
				push!(violations, (i, j, s, d))
			end
			if do_sample_check
				for k in 0:1000
					t = k / 1000.0
					x1 = traj[1,s,i] + t*(traj[1,s+1,i] - traj[1,s,i])
					y1 = traj[2,s,i] + t*(traj[2,s+1,i] - traj[2,s,i])
					x2 = traj[1,s,j] + t*(traj[1,s+1,j] - traj[1,s,j])
					y2 = traj[2,s,j] + t*(traj[2,s+1,j] - traj[2,s,j])
					ds = sqrt((x1-x2)^2 + (y1-y2)^2)
					if ds < d - 1e-8
						@warn "Analytical ≠ sampled" i j s t d ds
					end
				end
			end
		end
		if pair_min <= two_r + tol
			n_touched += 1
		end
	end

	total_pairs = n*(n-1) ÷ 2
	all_t = n_touched == total_pairs
	valid = all_t && isempty(violations)
	VerifyResult(pl, n_touched, total_pairs, all_t, violations, valid)
end

# ── Objective function ────────────────────────────────────────

function make_objective(n, nw, pos0, r)
	two_r = 2r
	n_seg = nw + 1
	traj = Array{Float64}(undef, 2, nw + 2, n)

	function obj(x, w_t, w_c)
		decode!(traj, x, n, nw, pos0)
		pl = path_length(traj, n, n_seg)
		tp = 0.0
		cp = 0.0
		# Use softmin over segments via log-sum-exp for smooth gradients
		@inbounds for i in 1:n, j in (i+1):n
			md = Inf
			for s in 1:n_seg
				d = seg_min_dist(
					traj[1,s,i], traj[2,s,i], traj[1,s+1,i], traj[2,s+1,i],
					traj[1,s,j], traj[2,s,j], traj[1,s+1,j], traj[2,s+1,j])
				md = min(md, d)
				if d < two_r
					cp += (two_r - d)^2
				end
			end
			if md > two_r
				gap = md - two_r
				tp += gap^2 + 0.1 * gap
			end
		end
		pl + w_t * tp + w_c * cp
	end
end

# ── Initialization strategies ─────────────────────────────────

function init_converge(n, nw, pos0, r)
	x = Vector{Float64}(undef, 2*n*nw)
	# Move disks to a TINY polygon near center so all pairs are within
	# touching distance. The optimizer will sort out the exact arrangement.
	small_R = 2r  # circumradius of target: ensures adjacent dist ≈ 2r·2sin(π/n)
	R_orig = sqrt(pos0[1,1]^2 + pos0[1,2]^2)
	scale = small_R / max(R_orig, 1e-10)
	idx = 0
	for i in 1:n, k in 1:nw
		t = 1.0 - abs(2k/(nw+1) - 1.0)
		noise = r * (0.3 + rand())
		x[idx+1] = pos0[i,1]*(1-t) + pos0[i,1]*scale*t + randn()*noise
		x[idx+2] = pos0[i,2]*(1-t) + pos0[i,2]*scale*t + randn()*noise
		idx += 2
	end
	x
end

function round_robin_schedule(n)
	n <= 1 && return Vector{Vector{Tuple{Int,Int}}}()
	if isodd(n)
		schedule = round_robin_schedule(n + 1)
		return [filter(p -> p[1] <= n && p[2] <= n, rd) for rd in schedule]
	end
	players = collect(2:n)
	rounds = Vector{Vector{Tuple{Int,Int}}}()
	for _ in 1:n-1
		rd = Tuple{Int,Int}[(1, players[1])]
		for k in 1:(n÷2-1)
			push!(rd, (players[1+k], players[n-k]))
		end
		push!(rounds, rd)
		players = vcat(players[2:end], players[1:1])
	end
	rounds
end

function init_random(n, nw, pos0, r)
	"""Completely random waypoints within the polygon bounds."""
	R = sqrt(pos0[1,1]^2 + pos0[1,2]^2)
	x = Vector{Float64}(undef, 2*n*nw)
	idx = 0
	for i in 1:n, k in 1:nw
		# Random point within circle of radius R
		θ = 2π * rand()
		r_sample = R * sqrt(rand())
		x[idx+1] = r_sample * cos(θ)
		x[idx+2] = r_sample * sin(θ)
		idx += 2
	end
	x
end

function init_tournament(n, nw, pos0, r)
	schedule = round_robin_schedule(n)
	n_rounds = length(schedule)
	wp = zeros(n, nw, 2)
	assigned = falses(n, nw)

	for (ri, pairs) in enumerate(schedule)
		k = clamp(round(Int, ri/(n_rounds+1) * nw), 1, nw)
		for (a, b) in pairs
			mx = (pos0[a,1] + pos0[b,1]) * 0.15
			my = (pos0[a,2] + pos0[b,2]) * 0.15
			wp[a, k, 1] = mx + randn()*r
			wp[a, k, 2] = my + randn()*r
			wp[b, k, 1] = mx + randn()*r
			wp[b, k, 2] = my + randn()*r
			assigned[a, k] = true
			assigned[b, k] = true
		end
	end

	# Fill gaps by interpolation
	for i in 1:n
		ts = Float64[0.0]
		xs = Float64[pos0[i,1]]
		ys = Float64[pos0[i,2]]
		for k in 1:nw
			if assigned[i, k]
				push!(ts, k/(nw+1))
				push!(xs, wp[i, k, 1])
				push!(ys, wp[i, k, 2])
			end
		end
		push!(ts, 1.0)
		push!(xs, pos0[i,1])
		push!(ys, pos0[i,2])

		for k in 1:nw
			if !assigned[i, k]
				t = k / (nw+1)
				si = searchsortedlast(ts, t)
				si = clamp(si, 1, length(ts)-1)
				α = (t - ts[si]) / (ts[si+1] - ts[si])
				wp[i, k, 1] = xs[si]*(1-α) + xs[si+1]*α
				wp[i, k, 2] = ys[si]*(1-α) + ys[si+1]*α
			end
		end
	end

	wp .+= randn(size(wp)) .* r .* 0.5

	x = Vector{Float64}(undef, 2*n*nw)
	idx = 0
	for i in 1:n, k in 1:nw
		x[idx+1] = wp[i, k, 1]
		x[idx+2] = wp[i, k, 2]
		idx += 2
	end
	x
end

# ── Solver ────────────────────────────────────────────────────

function solve(n, nw; r=0.3, edge_len=3.0, restarts=50,
               verbose=true, outdir=".")
	pos0 = polygon_positions(n, edge_len)
	obj = make_objective(n, nw, pos0, r)
	traj_buf = Array{Float64}(undef, 2, nw+2, n)

	best_x = nothing
	best_cost = Inf
	best_attempt_x = nothing
	best_attempt_pl = Inf
	attempt_num = 0
	t0 = time()

	# Phase 1: Force touching (high touch penalty, lower collision)
	# Phase 2: Fix collisions while maintaining touches
	# Phase 3: Polish with balanced high penalties
	stages = [
		(50000.0,  100.0,    500),
		(50000.0,  5000.0,   500),
		(50000.0,  50000.0,  500),
		(100000.0, 100000.0, 300),
	]

	for trial in 1:restarts
		x0 = if trial % 3 == 1
			init_converge(n, nw, pos0, r)
		else
			init_tournament(n, nw, pos0, r)
		end

		for (w_t, w_c, maxiter) in stages
			f(x) = obj(x, w_t, w_c)
			try
				result = optimize(f, x0, LBFGS(),
					Optim.Options(iterations=maxiter, f_tol=1e-12, g_tol=1e-8);
					autodiff=:finite)
				x0 = Optim.minimizer(result)
			catch e
				verbose && println("  trial $trial: optimizer error: $e")
				break
			end
		end

		decode!(traj_buf, x0, n, nw, pos0)
		vr = verify(traj_buf, r)
		elapsed = time() - t0

		if vr.valid
			if vr.path_length < best_cost
				best_cost = vr.path_length
				best_x = copy(x0)
				save_json(x0, n, nw, pos0, r, edge_len, vr,
				          joinpath(outdir, "best_n$(n)_w$(nw).json"))
				verbose && @printf("[%6.1fs] trial %3d/%d: pl=%.4f BEST\n",
					elapsed, trial, restarts, vr.path_length)
			else
				verbose && @printf("[%6.1fs] trial %3d/%d: pl=%.4f valid\n",
					elapsed, trial, restarts, vr.path_length)
			end
		else
			attempt_num += 1
			if vr.path_length < best_attempt_pl
				best_attempt_pl = vr.path_length
				best_attempt_x = copy(x0)
				# Save best invalid attempt (overwrites previous best attempt)
				save_json(x0, n, nw, pos0, r, edge_len, vr,
				          joinpath(outdir, "attempt_n$(n)_w$(nw).json"))
			end
			verbose && @printf("[%6.1fs] trial %3d/%d: pl=%.4f (t=%d/%d v=%d)\n",
				elapsed, trial, restarts, vr.path_length,
				vr.n_touched, vr.total_pairs, length(vr.violations))
		end
	end

	best_x, best_cost
end

# ── Multi-resolution solver ──────────────────────────────────

function refine_waypoints(x, n, nw_old, nw_new, pos0)
	traj_old = Array{Float64}(undef, 2, nw_old+2, n)
	decode!(traj_old, x, n, nw_old, pos0)

	t_old = range(0, 1, length=nw_old+2)
	t_new = range(0, 1, length=nw_new+2)
	t_old_vec = collect(t_old)

	x_new = Vector{Float64}(undef, 2*n*nw_new)
	idx = 0
	for i in 1:n, k in 1:nw_new
		t = t_new[k+1]
		s = searchsortedlast(t_old_vec, t)
		s = clamp(s, 1, nw_old+1)
		α = (t - t_old[s]) / (t_old[s+1] - t_old[s])
		x_new[idx+1] = traj_old[1, s, i]*(1-α) + traj_old[1, s+1, i]*α
		x_new[idx+2] = traj_old[2, s, i]*(1-α) + traj_old[2, s+1, i]*α
		idx += 2
	end
	x_new
end

function solve_multi(n, nw_target; r=0.3, edge_len=3.0,
                     restarts=50, verbose=true, outdir=".")
	nw_coarse = max(6, nw_target ÷ 2)
	verbose && println("Phase 1: coarse (nw=$nw_coarse)")
	x_c, cost_c = solve(n, nw_coarse; r, edge_len, restarts, verbose, outdir)

	if x_c === nothing
		verbose && println("Coarse failed, direct solve")
		return solve(n, nw_target; r, edge_len, restarts, verbose, outdir)
	end

	verbose && println("\nPhase 2: refine → nw=$nw_target")
	pos0 = polygon_positions(n, edge_len)
	x_f = refine_waypoints(x_c, n, nw_coarse, nw_target, pos0)
	obj = make_objective(n, nw_target, pos0, r)

	for (w_t, w_c, mi) in [(2000., 2000., 300),
	                        (20000., 20000., 500),
	                        (200000., 200000., 500)]
		f(x) = obj(x, w_t, w_c)
		res = optimize(f, x_f, LBFGS(),
			Optim.Options(iterations=mi, f_tol=1e-12); autodiff=:finite)
		x_f = Optim.minimizer(res)
	end

	traj_buf = Array{Float64}(undef, 2, nw_target+2, n)
	decode!(traj_buf, x_f, n, nw_target, pos0)
	vr = verify(traj_buf, r)

	if vr.valid
		save_json(x_f, n, nw_target, pos0, r, edge_len, vr,
		          joinpath(outdir, "best_n$(n)_w$(nw_target).json"))
		verbose && @printf("Refined: pl=%.4f ✓\n", vr.path_length)
	else
		save_json(x_f, n, nw_target, pos0, r, edge_len, vr,
		          joinpath(outdir, "attempt_n$(n)_w$(nw_target)_refined.json"))
		verbose && @printf("Refined: pl=%.4f (t=%d/%d v=%d)\n",
			vr.path_length, vr.n_touched, vr.total_pairs, length(vr.violations))
	end

	verbose && println("\nPhase 3: direct restarts at nw=$nw_target")
	x_d, cost_d = solve(n, nw_target; r, edge_len,
		restarts=max(10, restarts÷3), verbose, outdir)

	cost_f = vr.valid ? vr.path_length : Inf
	if cost_d < cost_f
		return x_d, cost_d
	end
	vr.valid ? (x_f, cost_f) : (x_d, cost_d)
end

# ── JSON I/O ──────────────────────────────────────────────────

function save_json(x, n, nw, pos0, r, edge_len, vr, filepath)
	traj = Array{Float64}(undef, 2, nw+2, n)
	decode!(traj, x, n, nw, pos0)
	R = edge_len / (2 * sin(π / n))

	disk_dists = zeros(n)
	for i in 1:n, s in 1:(nw+1)
		dx = traj[1, s+1, i] - traj[1, s, i]
		dy = traj[2, s+1, i] - traj[2, s, i]
		disk_dists[i] += sqrt(dx*dx + dy*dy)
	end

	result = Dict(
		"metadata" => Dict(
			"n_disks" => n,
			"n_waypoints" => nw,
			"disk_radius" => r,
			"edge_length" => edge_len,
			"polygon_circumradius" => R,
			"path_length" => vr.path_length,
			"fitness" => vr.path_length,
			"all_pairs_touch" => vr.all_touched,
			"has_path_collisions" => !isempty(vr.violations),
			"path_collision_penalty" => 0.0,
			"n_touched" => vr.n_touched,
			"total_pairs" => vr.total_pairs,
			"n_violations" => length(vr.violations),
			"valid" => vr.valid,
		),
		"initial_positions" => [[pos0[i,1], pos0[i,2]] for i in 1:n],
		"waypoints" => [
			[[traj[1, k+1, i], traj[2, k+1, i]] for i in 1:n]
			for k in 1:nw
		],
		"disk_trajectories" => Dict(
			string(i-1) => Dict(
				"path" => [[traj[1, s, i], traj[2, s, i]] for s in 1:(nw+2)],
				"distance" => disk_dists[i],
			)
			for i in 1:n
		),
	)

	open(filepath, "w") do f
		JSON.print(f, result)
	end
end

# ── Differential Evolution solver ────────────────────────────

"""
Hybrid Differential Evolution + L-BFGS solver.

Maintains a population of solutions that evolve via DE mutation/crossover,
with each trial vector polished by gradient descent. Combines global
exploration (DE) with local refinement (L-BFGS).

Parameters:
- pop_size: population size (default: min(50, 10*sqrt(n)))
- F: mutation scale factor (default: 0.7)
- CR: crossover probability (default: 0.8)
- generations: max generations (default: 100)
- polish_freq: run L-BFGS every N generations (default: 5)
"""
function solve_de(n, nw; r=0.3, edge_len=3.0,
                  pop_size=0, F=0.7, CR=0.8, generations=100,
                  polish_freq=5, verbose=true, outdir=".")
	pos0 = polygon_positions(n, edge_len)
	obj = make_objective(n, nw, pos0, r)
	traj_buf = Array{Float64}(undef, 2, nw+2, n)

	# Adaptive population size
	if pop_size == 0
		pop_size = clamp(Int(round(10 * sqrt(n))), 20, 80)
	end

	verbose && println("DE parameters: pop=$pop_size, F=$F, CR=$CR, gens=$generations")
	verbose && println("Initializing population...")

	# Initialize population with diverse strategies
	nvars = 2 * n * nw
	population = Matrix{Float64}(undef, nvars, pop_size)
	fitness = fill(Inf, pop_size)

	for i in 1:pop_size
		# Mix of initialization strategies for maximum diversity
		if i % 4 == 0
			population[:, i] = init_random(n, nw, pos0, r)
		elseif i % 4 == 1
			population[:, i] = init_converge(n, nw, pos0, r)
		else
			population[:, i] = init_tournament(n, nw, pos0, r)
		end
		# LIGHT initial polish - just feasibility, not optimization
		# Keep diversity high for DE to explore
		x_init = population[:, i]
		f(z) = obj(z, 5e4, 5e4)
		try
			res = optimize(f, x_init, LBFGS(),
				Optim.Options(iterations=150, f_tol=1e-10); autodiff=:finite)
			x_init = Optim.minimizer(res)
		catch; end
		population[:, i] = x_init

		# Compute fitness
		decode!(traj_buf, x_init, n, nw, pos0)
		vr = verify(traj_buf, r)
		fitness[i] = vr.valid ? vr.path_length : Inf
	end

	best_idx = argmin(fitness)
	best_x = copy(population[:, best_idx])
	best_fit = fitness[best_idx]

	if isfinite(best_fit)
		decode!(traj_buf, best_x, n, nw, pos0)
		vr = verify(traj_buf, r)
		save_json(best_x, n, nw, pos0, r, edge_len, vr,
		          joinpath(outdir, "best_n$(n)_w$(nw).json"))
		verbose && @printf("Init: best pl=%.4f\n\n", best_fit)
	else
		verbose && println("Init: no valid solutions yet\n")
	end

	t0 = time()
	stagnant = 0
	last_improvement = best_fit

	for gen in 1:generations
		improved_this_gen = false

		for i in 1:pop_size
			# DE mutation: x_trial = x_a + F*(x_b - x_c)
			indices = randperm(pop_size)
			a, b, c = indices[1], indices[2], indices[3]
			if a == i; a = indices[4]; end
			if b == i; b = indices[4]; end
			if c == i; c = indices[4]; end

			donor = population[:, a] .+ F .* (population[:, b] .- population[:, c])

			# Crossover
			trial = copy(population[:, i])
			j_rand = rand(1:nvars)
			for j in 1:nvars
				if rand() < CR || j == j_rand
					trial[j] = donor[j]
				end
			end

			# Polish trial with L-BFGS (every polish_freq generations)
			# Early gens: explore more, polish less. Late gens: exploit.
			should_polish = (gen % polish_freq == 0) || (gen > generations ÷ 2 && gen % 3 == 0)
			if should_polish
				penalty = gen > generations ÷ 2 ? 1e6 : 1e5
				for (w_t, w_c, mi) in [(penalty, penalty, 150)]
					f(z) = obj(z, w_t, w_c)
					try
						res = optimize(f, trial, LBFGS(),
							Optim.Options(iterations=mi, f_tol=1e-12); autodiff=:finite)
						trial = Optim.minimizer(res)
					catch; end
				end
			end

			# Evaluate trial
			decode!(traj_buf, trial, n, nw, pos0)
			vr = verify(traj_buf, r)
			trial_fit = vr.valid ? vr.path_length : Inf

			# Selection: keep if better
			if trial_fit < fitness[i]
				population[:, i] = trial
				fitness[i] = trial_fit

				if trial_fit < best_fit
					best_fit = trial_fit
					best_x = copy(trial)
					improved_this_gen = true
					save_json(trial, n, nw, pos0, r, edge_len, vr,
					          joinpath(outdir, "best_n$(n)_w$(nw).json"))
				end
			end
		end

		elapsed = time() - t0

		if improved_this_gen
			stagnant = 0
			last_improvement = best_fit
			# Compute diversity: avg distance between population members
			div = 0.0
			for i in 1:min(10, pop_size), j in (i+1):min(10, pop_size)
				div += norm(population[:, i] - population[:, j])
			end
			div /= (min(10, pop_size) * (min(10, pop_size) - 1) / 2)

			verbose && @printf("[%6.1fs] gen %3d: pl=%.6f BEST (div=%.2f)\n",
				elapsed, gen, best_fit, div)
		else
			stagnant += 1
			if verbose && gen % 10 == 0
				n_valid = count(isfinite, fitness)
				@printf("[%6.1fs] gen %3d: best=%.6f (valid=%d/%d, stagnant=%d)\n",
					elapsed, gen, best_fit, n_valid, pop_size, stagnant)
			end
		end

		# Early stopping: if no improvement for 30 generations
		if stagnant >= 30
			verbose && println("\nConverged (no improvement for 30 gens)")
			break
		end

		# Diversity injection: if stagnant for 8 gens, replace worst 30%
		if stagnant >= 8 && gen % 4 == 0
			n_replace = max(2, pop_size * 3 ÷ 10)
			worst_indices = sortperm(fitness, rev=true)[1:n_replace]
			for idx in worst_indices
				# Mix of strategies: random, tournament, mutated best
				rnd = rand()
				if rnd < 0.4
					population[:, idx] = init_random(n, nw, pos0, r)
				elseif rnd < 0.7
					population[:, idx] = init_tournament(n, nw, pos0, r)
				else
					# Mutate best solution with large noise
					population[:, idx] = best_x .+ randn(nvars) .* r .* 1.0
				end
				decode!(traj_buf, population[:, idx], n, nw, pos0)
				vr = verify(traj_buf, r)
				fitness[idx] = vr.valid ? vr.path_length : Inf
			end
			verbose && println("  Diversity injection: replaced $n_replace worst")
		end
	end

	# Final polish of best solution with very high penalties
	verbose && println("\nFinal polish of best solution...")
	x_final = copy(best_x)
	for (w_t, w_c, mi) in [(1e6, 1e6, 500), (1e7, 1e7, 300)]
		f(z) = obj(z, w_t, w_c)
		try
			res = optimize(f, x_final, LBFGS(),
				Optim.Options(iterations=mi, f_tol=1e-14, g_tol=1e-10);
				autodiff=:finite)
			x_final = Optim.minimizer(res)
		catch; end
	end

	decode!(traj_buf, x_final, n, nw, pos0)
	vr = verify(traj_buf, r)
	if vr.valid && vr.path_length < best_fit
		best_fit = vr.path_length
		best_x = x_final
		save_json(x_final, n, nw, pos0, r, edge_len, vr,
		          joinpath(outdir, "best_n$(n)_w$(nw).json"))
		verbose && @printf("Final polish: %.6f\n", best_fit)
	else
		verbose && @printf("Final: %.6f\n", best_fit)
	end

	best_x, best_fit
end

# ── Refine existing solution ──────────────────────────────────

function load_solution(filepath)
	data = JSON.parsefile(filepath)
	m = data["metadata"]
	n = m["n_disks"]
	nw = m["n_waypoints"]
	r = m["disk_radius"]
	edge_len = m["edge_length"]
	pos0 = polygon_positions(n, edge_len)

	# Reconstruct flat waypoint vector from trajectories
	x = Vector{Float64}(undef, 2*n*nw)
	idx = 0
	for i in 1:n
		path = data["disk_trajectories"][string(i-1)]["path"]
		for k in 1:nw
			x[idx+1] = path[k+1][1]  # skip initial pos (index 1)
			x[idx+2] = path[k+1][2]
			idx += 2
		end
	end
	(; x, n, nw, r, edge_len, pos0)
end

"""
Refine an existing solution. Three strategies applied in sequence:

1. **Polish**: Long L-BFGS runs with very high penalty weights.
   Squeezes path length while keeping constraints satisfied.

2. **Perturb + polish**: Small random perturbations followed by
   L-BFGS. Explores nearby basins that might be shorter.

3. **Upsample + polish**: Interpolate to more waypoints, then
   optimize. More degrees of freedom → smoother, shorter paths.
"""
function refine(filepath; rounds=5, perturb_trials=20,
                upsample=0, verbose=true, outdir=".")
	sol = load_solution(filepath)
	(; x, n, nw, r, edge_len, pos0) = sol
	obj = make_objective(n, nw, pos0, r)
	traj_buf = Array{Float64}(undef, 2, nw+2, n)

	decode!(traj_buf, x, n, nw, pos0)
	vr0 = verify(traj_buf, r)
	verbose && @printf("Loaded: pl=%.6f valid=%s\n\n", vr0.path_length, vr0.valid)

	best_x = copy(x)
	best_pl = vr0.valid ? vr0.path_length : Inf
	t0 = time()

	# ── Strategy 1: Polish with high penalties ────────────────
	verbose && println("Strategy 1: Polish ($(rounds) rounds of long L-BFGS)")
	x_cur = copy(x)
	for round in 1:rounds
		for (w_t, w_c, mi) in [
			(1e5,  1e5,  1000),
			(1e6,  1e6,  1000),
			(1e7,  1e7,  500),
		]
			f(z) = obj(z, w_t, w_c)
			try
				res = optimize(f, x_cur, LBFGS(),
					Optim.Options(iterations=mi, f_tol=1e-14, g_tol=1e-10);
					autodiff=:finite)
				x_cur = Optim.minimizer(res)
			catch; end
		end
		decode!(traj_buf, x_cur, n, nw, pos0)
		vr = verify(traj_buf, r)
		elapsed = time() - t0
		if vr.valid && vr.path_length < best_pl
			best_pl = vr.path_length
			best_x = copy(x_cur)
			save_json(x_cur, n, nw, pos0, r, edge_len, vr,
			          joinpath(outdir, "best_n$(n)_w$(nw).json"))
			verbose && @printf("  [%5.1fs] round %d: pl=%.6f BEST\n",
				elapsed, round, vr.path_length)
		else
			verbose && @printf("  [%5.1fs] round %d: pl=%.6f%s\n",
				elapsed, round, vr.path_length,
				vr.valid ? "" : " (invalid)")
		end
	end

	# ── Strategy 2: Perturb + polish ──────────────────────────
	verbose && println("\nStrategy 2: Perturb + polish ($(perturb_trials) trials)")
	for trial in 1:perturb_trials
		# Perturbation scale decays: explore broadly first, then fine-tune
		σ = r * 0.5 * (1.0 - 0.7 * trial / perturb_trials)
		x_p = best_x .+ randn(length(best_x)) .* σ

		for (w_t, w_c, mi) in [
			(1e5,  1e5,  500),
			(1e6,  1e6,  500),
			(1e7,  1e7,  300),
		]
			f(z) = obj(z, w_t, w_c)
			try
				res = optimize(f, x_p, LBFGS(),
					Optim.Options(iterations=mi, f_tol=1e-14, g_tol=1e-10);
					autodiff=:finite)
				x_p = Optim.minimizer(res)
			catch; end
		end
		decode!(traj_buf, x_p, n, nw, pos0)
		vr = verify(traj_buf, r)
		elapsed = time() - t0
		if vr.valid && vr.path_length < best_pl
			best_pl = vr.path_length
			best_x = copy(x_p)
			save_json(x_p, n, nw, pos0, r, edge_len, vr,
			          joinpath(outdir, "best_n$(n)_w$(nw).json"))
			verbose && @printf("  [%5.1fs] trial %2d/%d: pl=%.6f BEST\n",
				elapsed, trial, perturb_trials, vr.path_length)
		elseif verbose && trial % 5 == 0
			@printf("  [%5.1fs] trial %2d/%d: pl=%.6f%s\n",
				elapsed, trial, perturb_trials, vr.path_length,
				vr.valid ? "" : " (invalid)")
		end
	end

	# ── Strategy 3: Upsample + polish ─────────────────────────
	nw_new = upsample > 0 ? upsample : 0
	if nw_new > nw
		verbose && println("\nStrategy 3: Upsample $(nw) → $(nw_new) waypoints + polish")
		pos0_up = polygon_positions(n, edge_len)
		x_up = refine_waypoints(best_x, n, nw, nw_new, pos0_up)
		obj_up = make_objective(n, nw_new, pos0_up, r)
		traj_up = Array{Float64}(undef, 2, nw_new+2, n)

		for round in 1:3
			for (w_t, w_c, mi) in [
				(1e5,  1e5,  1000),
				(1e6,  1e6,  1000),
				(1e7,  1e7,  500),
			]
				f(z) = obj_up(z, w_t, w_c)
				try
					res = optimize(f, x_up, LBFGS(),
						Optim.Options(iterations=mi, f_tol=1e-14, g_tol=1e-10);
						autodiff=:finite)
					x_up = Optim.minimizer(res)
				catch; end
			end
			decode!(traj_up, x_up, n, nw_new, pos0_up)
			vr = verify(traj_up, r)
			elapsed = time() - t0
			if vr.valid
				save_json(x_up, n, nw_new, pos0_up, r, edge_len, vr,
				          joinpath(outdir, "best_n$(n)_w$(nw_new).json"))
				verbose && @printf("  [%5.1fs] round %d: pl=%.6f%s\n",
					elapsed, round, vr.path_length,
					vr.path_length < best_pl ? " BEST" : "")
				if vr.path_length < best_pl
					best_pl = vr.path_length
				end
			else
				verbose && @printf("  [%5.1fs] round %d: pl=%.6f (invalid)\n",
					elapsed, round, vr.path_length)
			end
		end
	end

	@printf("\nFinal best: %.6f\n", best_pl)
end

# ── CLI ───────────────────────────────────────────────────────

function main()
	args = Dict{String,Any}()
	i = 1
	while i <= length(ARGS)
		a = ARGS[i]
		if a == "-n"
			args["n"] = parse(Int, ARGS[i+1]); i += 2
		elseif a in ["-w", "--waypoints"]
			args["w"] = parse(Int, ARGS[i+1]); i += 2
		elseif a in ["-r", "--radius"]
			args["r"] = parse(Float64, ARGS[i+1]); i += 2
		elseif a in ["-d", "--edge-length"]
			args["d"] = parse(Float64, ARGS[i+1]); i += 2
		elseif a == "--restarts"
			args["restarts"] = parse(Int, ARGS[i+1]); i += 2
		elseif a == "--method"
			args["method"] = ARGS[i+1]; i += 2
		elseif a == "--pop-size"
			args["pop_size"] = parse(Int, ARGS[i+1]); i += 2
		elseif a == "--generations"
			args["generations"] = parse(Int, ARGS[i+1]); i += 2
		elseif a == "--mutation"
			args["F"] = parse(Float64, ARGS[i+1]); i += 2
		elseif a == "--crossover"
			args["CR"] = parse(Float64, ARGS[i+1]); i += 2
		elseif a in ["-o", "--output-dir"]
			args["outdir"] = ARGS[i+1]; i += 2
		elseif a in ["-q", "--quiet"]
			args["quiet"] = true; i += 1
		elseif a == "--seed"
			args["seed"] = parse(Int, ARGS[i+1]); i += 2
		elseif a == "--verify"
			args["verify"] = true; i += 1
		elseif a == "--refine"
			args["refine"] = ARGS[i+1]; i += 2
		elseif a == "--rounds"
			args["rounds"] = parse(Int, ARGS[i+1]); i += 2
		elseif a == "--perturb"
			args["perturb"] = parse(Int, ARGS[i+1]); i += 2
		elseif a == "--upsample"
			args["upsample"] = parse(Int, ARGS[i+1]); i += 2
		elseif a in ["-h", "--help"]
			println("""Champagne Toasting Problem Solver

Usage: julia champagne.jl -n <disks> [options]
       julia champagne.jl --refine <file.json> [refine options]

Solve mode:
  -n INT             Number of disks (required)
  -w INT             Waypoints (default: 2n+2)
  -r FLOAT           Disk radius (default: 0.3)
  -d FLOAT           Polygon edge length (default: 3.0)
  --restarts INT     Random restarts (default: 50, for lbfgs/multi)
  --method STR       lbfgs | multi | de (default: auto)

DE-specific (for --method de):
  --pop-size INT     Population size (default: auto)
  --generations INT  Max generations (default: 100)
  --mutation FLOAT   DE mutation factor F (default: 0.7)
  --crossover FLOAT  DE crossover rate CR (default: 0.8)

Refine mode (crank compute on existing solution):
  --refine FILE      JSON solution to refine
  --rounds INT       Polish rounds (default: 5)
  --perturb INT      Perturb+polish trials (default: 20)
  --upsample INT     Upsample to N waypoints, then polish

Common:
  -o DIR             Output directory (default: .)
  -q                 Quiet
  --seed INT         Random seed
  --verify           Cross-check analytical formula with sampling""")
			return
		else
			println("Unknown: $a"); return
		end
	end

	# ── Refine mode ──────────────────────────────────────────
	if haskey(args, "refine")
		outdir = get(args, "outdir", ".")
		quiet = get(args, "quiet", false)
		haskey(args, "seed") && Random.seed!(args["seed"])
		mkpath(outdir)
		refine(args["refine"];
			rounds=get(args, "rounds", 5),
			perturb_trials=get(args, "perturb", 20),
			upsample=get(args, "upsample", 0),
			verbose=!quiet, outdir)
		return
	end

	# ── Solve mode ───────────────────────────────────────────
	n = get(args, "n", nothing)
	if n === nothing
		println("Error: -n required (or use --refine)"); return
	end

	nw = get(args, "w", 2n + 2)
	r = get(args, "r", 0.3)
	edge_len = get(args, "d", 3.0)
	restarts = get(args, "restarts", 50)
	method = get(args, "method", "auto")
	outdir = get(args, "outdir", ".")
	quiet = get(args, "quiet", false)
	do_verify = get(args, "verify", false)

	haskey(args, "seed") && Random.seed!(args["seed"])

	if edge_len <= 2r
		println("Error: edge length ($edge_len) must be > 2r ($(2r))")
		return
	end

	if n <= 1
		println("n=$n: trivial."); return
	end

	R = edge_len / (2 * sin(π / n))
	println("Champagne Toasting Problem")
	@printf("  n=%d, waypoints=%d, r=%.3f, edge=%.3f (R=%.3f)\n", n, nw, r, edge_len, R)
	println("  Pairs: $(n*(n-1)÷2), Variables: $(2*n*nw)")
	do_verify && println("  Sampling cross-check: enabled")
	println()

	if method == "auto"
		method = nw >= 12 ? "multi" : "lbfgs"
	end

	mkpath(outdir)

	x, cost = if method == "de"
		solve_de(n, nw; r, edge_len,
			pop_size=get(args, "pop_size", 0),
			F=get(args, "F", 0.7),
			CR=get(args, "CR", 0.8),
			generations=get(args, "generations", 100),
			verbose=!quiet, outdir)
	elseif method == "multi"
		solve_multi(n, nw; r, edge_len, restarts, verbose=!quiet, outdir)
	else
		solve(n, nw; r, edge_len, restarts, verbose=!quiet, outdir)
	end

	if x === nothing || isinf(cost)
		println("\nNo valid solution found. Try more --restarts or -w.")
	else
		@printf("\nBest valid path length: %.6f\n", cost)
		if do_verify
			pos0 = polygon_positions(n, edge_len)
			traj = Array{Float64}(undef, 2, nw+2, n)
			decode!(traj, x, n, nw, pos0)
			vr = verify(traj, r; do_sample_check=true)
			println("Sampling cross-check: $(vr.valid ? "PASS" : "FAIL")")
		end
	end
end

if abspath(PROGRAM_FILE) == @__FILE__
	main()
end
