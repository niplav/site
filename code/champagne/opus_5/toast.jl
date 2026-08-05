#!/usr/bin/env julia

# Champagne toasting problem: n disks of radius r sit on the corners of a
# regular n-gon with edge length `edge`. Find piecewise-linear closed tours
# (all disks stepping through waypoint index k simultaneously) minimizing
# total path length, such that every pair of disks is tangent at some point
# in time and no two disks ever overlap.
#
# Everything is evaluated in continuous time: for a pair (i,j) and a time
# step k the difference vector is affine in t, so min_{t∈[0,1]} ‖Δ(t)‖ is
# closed form. Let m_ij = min over the whole tour. Then
#
#	m_ij < 2r  ⟺  overlap,   m_ij > 2r  ⟺  never touched,
#
# i.e. feasibility is the equality m_ij = 2r for all pairs. Optimized with a
# two-sided quadratic penalty + L-BFGS + penalty continuation, wrapped in
# multi-start / basin hopping.

using LinearAlgebra, Random, Printf, JSON, Optim

const TOL_TOUCH = 1e-6		# m_ij - 2r allowed before "did not touch"
const TOL_OVER = 1e-9		# 2r - m_ij allowed before "overlap"

struct Prob
	n::Int
	w::Int			# free waypoints per disk
	r::Float64
	edge::Float64
	circ::Float64
	h::Matrix{Float64}	# 2×n home positions
end

function mkprob(n, w; r=0.3, edge=3.0)
	circ = n < 2 ? 0.0 : edge/(2*sin(pi/n))
	h = Matrix{Float64}(undef, 2, n)
	for i in 1:n
		a = pi/2 + 2*pi*(i-1)/n
		h[1,i] = circ*cos(a)
		h[2,i] = circ*sin(a)
	end
	Prob(n, w, r, edge, circ, h)
end

npair(pr) = pr.n*(pr.n-1)÷2

# path array: 2 × n × (w+2), home ... waypoints ... home
function mkpath(pr)
	Array{Float64}(undef, 2, pr.n, pr.w+2)
end

function build!(p, x, pr)
	@inbounds for i in 1:pr.n
		p[1,i,1] = pr.h[1,i]
		p[2,i,1] = pr.h[2,i]
		for k in 1:pr.w
			p[1,i,k+1] = x[1,i,k]
			p[2,i,k+1] = x[2,i,k]
		end
		p[1,i,pr.w+2] = pr.h[1,i]
		p[2,i,pr.w+2] = pr.h[2,i]
	end
	p
end

@inline function spread!(g, i, j, k, t, ex, ey, c)
	a = c*(1-t)
	b = c*t
	@inbounds begin
		g[1,i,k] += a*ex
		g[2,i,k] += a*ey
		g[1,i,k+1] += b*ex
		g[2,i,k+1] += b*ey
		g[1,j,k] -= a*ex
		g[2,j,k] -= a*ey
		g[1,j,k+1] -= b*ex
		g[2,j,k+1] -= b*ey
	end
end

# closest approach of disks i,j during step k: (dist, t)
@inline function seg_min(p, i, j, k)
	@inbounds begin
		d0x = p[1,i,k]-p[1,j,k]
		d0y = p[2,i,k]-p[2,j,k]
		ux = (p[1,i,k+1]-p[1,j,k+1])-d0x
		uy = (p[2,i,k+1]-p[2,j,k+1])-d0y
	end
	uu = ux*ux+uy*uy
	t = uu > 1e-18 ? clamp(-(d0x*ux+d0y*uy)/uu, 0.0, 1.0) : 0.0
	ax = d0x+t*ux
	ay = d0y+t*uy
	sqrt(ax*ax+ay*ay), t
end

# objective + gradient in path space.
#
# The tangency requirement is the equality e_ij = m_ij - 2r = 0, handled by an
# augmented Lagrangian (multipliers mu, penalty lt). On top of that every
# *segment* gets a one-sided overlap penalty lc, so a pair that is intersecting
# during several time steps is pushed apart everywhere, not just at its worst
# moment.
function fg!(g, p, pr, mu, lt, lc)
	n = pr.n
	ns = pr.w+1
	dd = 2*pr.r
	fill!(g, 0.0)
	len = 0.0
	@inbounds for i in 1:n, k in 1:ns
		dx = p[1,i,k+1]-p[1,i,k]
		dy = p[2,i,k+1]-p[2,i,k]
		nd = sqrt(dx*dx+dy*dy)
		len += nd
		if nd > 1e-12
			ux = dx/nd
			uy = dy/nd
			g[1,i,k] -= ux
			g[2,i,k] -= uy
			g[1,i,k+1] += ux
			g[2,i,k+1] += uy
		end
	end
	pen = 0.0
	@inbounds for i in 1:n-1, j in i+1:n
		bm = Inf
		bk = 1
		bt = 0.0
		for k in 1:ns
			m, t = seg_min(p, i, j, k)
			if m < bm
				bm = m
				bk = k
				bt = t
			end
			if m < dd && m > 1e-9
				pen += 0.5*lc*(dd-m)^2
				d0x = p[1,i,k]-p[1,j,k]
				d0y = p[2,i,k]-p[2,j,k]
				ax = d0x+t*((p[1,i,k+1]-p[1,j,k+1])-d0x)
				ay = d0y+t*((p[2,i,k+1]-p[2,j,k+1])-d0y)
				spread!(g, i, j, k, t, ax/m, ay/m, -lc*(dd-m))
			end
		end
		if bm > 1e-9
			e = bm-dd
			pen += mu[i,j]*e+0.5*lt*e*e
			d0x = p[1,i,bk]-p[1,j,bk]
			d0y = p[2,i,bk]-p[2,j,bk]
			ax = d0x+bt*((p[1,i,bk+1]-p[1,j,bk+1])-d0x)
			ay = d0y+bt*((p[2,i,bk+1]-p[2,j,bk+1])-d0y)
			spread!(g, i, j, bk, bt, ax/bm, ay/bm, mu[i,j]+lt*e)
		end
	end
	len+pen
end

function tourlen(x, pr, p=mkpath(pr))
	build!(p, x, pr)
	len = 0.0
	@inbounds for i in 1:pr.n, k in 1:pr.w+1
		len += hypot(p[1,i,k+1]-p[1,i,k], p[2,i,k+1]-p[2,i,k])
	end
	len
end

struct Check
	len::Float64
	ntouch::Int
	maxover::Float64	# largest 2r - m_ij
	worstgap::Float64	# largest m_ij - 2r among untouched pairs
	ok::Bool
end

function check(x, pr; p=mkpath(pr))
	build!(p, x, pr)
	dd = 2*pr.r
	nt = 0
	over = 0.0
	gap = 0.0
	for i in 1:pr.n-1, j in i+1:pr.n
		bm = Inf
		for k in 1:pr.w+1
			m, _ = seg_min(p, i, j, k)
			bm = min(bm, m)
		end
		over = max(over, dd-bm)
		if bm <= dd+TOL_TOUCH
			nt += 1
		else
			gap = max(gap, bm-dd)
		end
	end
	l = tourlen(x, pr, p)
	Check(l, nt, over, gap, nt == npair(pr) && over <= TOL_OVER)
end

# A rigorous lower bound on the total path length.
#
# If disks i and j are tangent at some time, their displacements from home
# satisfy |a_i|+|a_j| >= d_ij-2r, and any closed path through home+a_i is at
# least 2|a_i| long, so T_i+T_j >= 2(d_ij-2r). For any fractional matching y
# (y_ij >= 0, sum_j y_ij <= 1),
#
#	sum_i T_i >= sum_ij y_ij (T_i+T_j) >= sum_ij y_ij 2(d_ij-2r).
#
# The longest chords of a regular n-gon form a perfect matching for even n
# (take y=1 on its n/2 edges) and a single n-cycle for odd n (take y=1/2 on its
# n edges); both give the same closed form.
function lowbound(pr)
	pr.n < 2 && return 0.0
	pr.n*(2*pr.circ*sin(pi*(pr.n÷2)/pr.n)-2*pr.r)
end

# ---------- optimization ----------

# signed tangency errors e_ij = m_ij - 2r
function errs(x, pr, p=mkpath(pr))
	build!(p, x, pr)
	e = zeros(pr.n, pr.n)
	for i in 1:pr.n-1, j in i+1:pr.n
		bm = Inf
		for k in 1:pr.w+1
			m, _ = seg_min(p, i, j, k)
			bm = min(bm, m)
		end
		e[i,j] = bm-2*pr.r
	end
	e
end

function polish(x0, pr; lt=2.0, lc=100.0, stages=18, iters=1200, growth=6.0)
	p = mkpath(pr)
	g = mkpath(pr)
	mu = zeros(pr.n, pr.n)
	function obj(f, gv, v)
		xx = reshape(v, 2, pr.n, pr.w)
		build!(p, xx, pr)
		val = fg!(g, p, pr, mu, lt, lc)
		if gv !== nothing
			gg = reshape(gv, 2, pr.n, pr.w)
			@inbounds for i in 1:pr.n, k in 1:pr.w
				gg[1,i,k] = g[1,i,k+1]
				gg[2,i,k] = g[2,i,k+1]
			end
		end
		val
	end
	v = vec(copy(x0))
	prev = Inf
	for s in 1:stages
		res = optimize(Optim.only_fg!(obj), v, LBFGS(),
			Optim.Options(iterations=iters, g_abstol=1e-14, f_abstol=1e-16))
		v = Optim.minimizer(res)
		e = errs(reshape(v, 2, pr.n, pr.w), pr, p)
		vio = maximum(abs, e)
		for i in 1:pr.n-1, j in i+1:pr.n
			mu[i,j] += lt*e[i,j]
		end
		lt *= growth
		lc *= growth
		prev = vio
		vio < 1e-12 && break
	end
	reshape(v, 2, pr.n, pr.w)
end

# ---------- radial mode ----------
#
# The exact optima for n=3 and n=4 both move every disk in and out along its
# own home ray, so it is worth searching that subfamily separately: the state
# is one radius per disk per time step (n*w instead of 2*n*w unknowns) and the
# tour length is just the total variation of each radius profile.

function dirs(pr)
	d = Matrix{Float64}(undef, 2, pr.n)
	for i in 1:pr.n
		d[1,i] = pr.h[1,i]/pr.circ
		d[2,i] = pr.h[2,i]/pr.circ
	end
	d
end

function rad2xy(rho, pr, u=dirs(pr))
	x = Array{Float64}(undef, 2, pr.n, pr.w)
	for i in 1:pr.n, k in 1:pr.w
		x[1,i,k] = rho[i,k]*u[1,i]
		x[2,i,k] = rho[i,k]*u[2,i]
	end
	x
end

function polish_rad(rho0, pr; lt=2.0, lc=100.0, stages=18, iters=1200, growth=6.0)
	u = dirs(pr)
	p = mkpath(pr)
	g = mkpath(pr)
	mu = zeros(pr.n, pr.n)
	function obj(f, gv, v)
		rho = reshape(v, pr.n, pr.w)
		build!(p, rad2xy(rho, pr, u), pr)
		val = fg!(g, p, pr, mu, lt, lc)
		if gv !== nothing
			gg = reshape(gv, pr.n, pr.w)
			@inbounds for i in 1:pr.n, k in 1:pr.w
				gg[i,k] = g[1,i,k+1]*u[1,i]+g[2,i,k+1]*u[2,i]
			end
		end
		val
	end
	v = vec(copy(rho0))
	for s in 1:stages
		res = optimize(Optim.only_fg!(obj), v, LBFGS(),
			Optim.Options(iterations=iters, g_abstol=1e-14, f_abstol=1e-16))
		v = Optim.minimizer(res)
		e = errs(rad2xy(reshape(v, pr.n, pr.w), pr, u), pr, p)
		vio = maximum(abs, e)
		for i in 1:pr.n-1, j in i+1:pr.n
			mu[i,j] += lt*e[i,j]
		end
		lt *= growth
		lc *= growth
		vio < 1e-12 && break
	end
	reshape(v, pr.n, pr.w)
end

# V-shaped radius profiles: disk i dives to depth dep[i] at time tau[i]
function init_rad(pr, rng)
	n = pr.n
	rho = Array{Float64}(undef, n, pr.w)
	dep = [pr.r*(0.5+2.5*rand(rng)) for _ in 1:n]
	tau = [1+(pr.w-1)*rand(rng) for _ in 1:n]
	for i in 1:n, k in 1:pr.w
		f = abs(k-tau[i])/max(1.0, pr.w/2)
		rho[i,k] = dep[i]+f*(pr.circ-dep[i])
	end
	rho
end

function search_rad(n, w; r=0.3, edge=3.0, budget=60.0, seed=1, verbose=true)
	pr = mkprob(n, w; r=r, edge=edge)
	rng = Xoshiro(seed)
	best = nothing
	bl = Inf
	t0 = time()
	tries = 0
	while time()-t0 < budget
		tries += 1
		rho = best !== nothing && rand(rng) < 0.5 ?
			best.+(0.05+0.5*rand(rng)).*randn(rng, n, pr.w) : init_rad(pr, rng)
		rho = polish_rad(rho, pr)
		c = check(rad2xy(rho, pr), pr)
		if c.ok && c.len < bl
			bl = c.len
			best = copy(rho)
			verbose && @printf("  [%5.1fs try %4d] len=%.5f\n", time()-t0, tries, bl)
		end
	end
	pr, best === nothing ? nothing : rad2xy(best, pr), bl, tries
end

# ---------- initializations ----------

# random cluster of `n` points near the origin with pairwise distance >= 2r
function cluster(n, r, rng; spread=1.0)
	c = zeros(2, n)
	for i in 1:n
		for _ in 1:400
			q = (2*rand(rng, 2).-1).*(spread*2*r*sqrt(n))
			ok = true
			for j in 1:i-1
				if hypot(q[1]-c[1,j], q[2]-c[2,j]) < 2.05*r
					ok = false
					break
				end
			end
			if ok
				c[:,i] .= q
				break
			end
		end
	end
	c
end

function init_rand(pr, rng)
	x = Array{Float64}(undef, 2, pr.n, pr.w)
	for k in 1:pr.w
		x[:,:,k] .= cluster(pr.n, pr.r, rng; spread=1.0+2*rand(rng))
	end
	x
end

# disks travel to a sequence of tight clusters and back; disk->slot
# assignment reshuffled between clusters
function init_cluster(pr, rng)
	x = Array{Float64}(undef, 2, pr.n, pr.w)
	nc = max(1, min(pr.w, rand(rng, 1:max(1, pr.w÷2))))
	cs = [cluster(pr.n, pr.r, rng; spread=1.0+0.6*rand(rng)) for _ in 1:nc]
	ps = [randperm(rng, pr.n) for _ in 1:nc]
	for k in 1:pr.w
		c = cs[min(nc, 1+((k-1)*nc)÷pr.w)]
		q = ps[min(nc, 1+((k-1)*nc)÷pr.w)]
		for i in 1:pr.n
			x[:,i,k] .= c[:,q[i]] .+ 0.02*pr.r.*randn(rng, 2)
		end
	end
	x
end

# disks form a tight row, then a random sequence of adjacent transpositions
# is applied (each swap makes that pair touch); the row axis is random
function init_row(pr, rng)
	n = pr.n
	x = Array{Float64}(undef, 2, n, pr.w)
	th = 2*pi*rand(rng)
	ax = [cos(th), sin(th)]
	pp = [-ax[2], ax[1]]
	ord = randperm(rng, n)
	slot(s) = ((s-1)-(n-1)/2)*2.02*pr.r
	pos = Vector{Int}(undef, n)		# disk -> slot
	for s in 1:n
		pos[ord[s]] = s
	end
	for k in 1:pr.w
		# swap a random adjacent pair every other waypoint
		if k > 1 && isodd(k)
			s = rand(rng, 1:n-1)
			a = findfirst(==(s), pos)
			b = findfirst(==(s+1), pos)
			pos[a], pos[b] = pos[b], pos[a]
		end
		for i in 1:n
			c = slot(pos[i]).*ax
			# nudge off-axis while swapping so paths stay collision free
			x[:,i,k] .= c .+ (0.6*pr.r*randn(rng)).*pp
		end
	end
	x
end

# "Comb": park all disks in a tight row (spacing exactly 2r, so neighbours are
# tangent), then let the leftmost remaining disk lift off by 2r and travel in a
# straight line at height 2r above the row: at the moment it passes over row
# disk j their distance is exactly 2r, so *one* segment makes it touch every
# remaining disk. It then flies home, and the next disk sweeps. Covers all
# C(n,2) pairs and is valid by construction (up to gather-phase crossings).
comb_w(n) = 1+3*(n-2)

function init_comb(pr, rng)
	n = pr.n
	r = pr.r
	th = 2*pi*rand(rng)
	u = [cos(th), sin(th)]
	v = [-u[2], u[1]]
	rand(rng, Bool) && (v = -v)
	cen = 0.5*pr.circ.*(2 .*rand(rng, 2).-1)
	ord = sortperm([dot(pr.h[:,d], u) for d in 1:n])
	rand(rng, Bool) && reverse!(ord)
	slot = [cen .+ ((m-(n+1)/2)*2*r).*u for m in 1:n]
	nw = comb_w(n)
	x = Array{Float64}(undef, 2, n, nw)
	at = Vector{Vector{Float64}}(undef, n)
	for m in 1:n
		at[ord[m]] = copy(slot[m])
	end
	for d in 1:n
		x[:,d,1] .= at[d]
	end
	c = 1
	for m in 1:n-2
		d = ord[m]
		for q in (slot[m].+2*r.*v, slot[n].+2*r.*v, pr.h[:,d])
			c += 1
			at[d] = q
			for e in 1:n
				x[:,e,c] .= at[e]
			end
		end
	end
	x
end

# pad a waypoint sequence to w steps by repeating its first entry (zero cost)
function padwp(x, w)
	nw = size(x, 3)
	nw >= w && return x[:,:,1:w]
	y = Array{Float64}(undef, 2, size(x, 2), w)
	rep = w-nw
	for k in 1:rep
		y[:,:,k] .= x[:,:,1]
	end
	y[:,:,rep+1:end] .= x
	y
end

function perturb(x, pr, rng; amp=0.35)
	y = copy(x)
	for k in 1:pr.w, i in 1:pr.n
		if rand(rng) < 0.5
			y[:,i,k] .+= amp.*randn(rng, 2)
		end
	end
	y
end

# ---------- waypoint surgery ----------

# split time step k (path index k -> k+1) of every disk at parameter t;
# geometry and total length are unchanged, one degree of freedom is gained
function insert_step(x, pr, k, t)
	p = mkpath(pr)
	build!(p, x, pr)
	q = Array{Float64}(undef, 2, pr.n, pr.w+3)
	for i in 1:pr.n
		for kk in 1:k
			q[:,i,kk] .= p[:,i,kk]
		end
		q[1,i,k+1] = p[1,i,k]+t*(p[1,i,k+1]-p[1,i,k])
		q[2,i,k+1] = p[2,i,k]+t*(p[2,i,k+1]-p[2,i,k])
		for kk in k+1:pr.w+2
			q[:,i,kk+1] .= p[:,i,kk]
		end
	end
	mkprob(pr.n, pr.w+1; r=pr.r, edge=pr.edge), q[:,:,2:pr.w+2]
end

# drop waypoint index k (one time step less); returns smaller problem+state
function drop_step(x, pr, k)
	y = Array{Float64}(undef, 2, pr.n, pr.w-1)
	c = 1
	for kk in 1:pr.w
		kk == k && continue
		y[:,:,c] .= x[:,:,kk]
		c += 1
	end
	mkprob(pr.n, pr.w-1; r=pr.r, edge=pr.edge), y
end

# make every touch event land exactly on a waypoint (nicer animation, and
# validators that only look at waypoints then see the tangencies)
function pin_touches(x, pr)
	dd = 2*pr.r
	while true
		p = mkpath(pr)
		build!(p, x, pr)
		ev = Tuple{Int,Float64}[]
		for i in 1:pr.n-1, j in i+1:pr.n
			bm = Inf
			bk = 1
			bt = 0.0
			for k in 1:pr.w+1
				m, t = seg_min(p, i, j, k)
				if m < bm
					bm = m
					bk = k
					bt = t
				end
			end
			if bm <= dd+TOL_TOUCH && 1e-4 < bt < 1-1e-4
				push!(ev, (bk, bt))
			end
		end
		isempty(ev) && return pr, x
		k, t = ev[1]
		pr, x = insert_step(x, pr, k, t)
	end
end

# ---------- search ----------

function search(n, w; r=0.3, edge=3.0, budget=60.0, seed=1, verbose=true,
		x0=nothing, pr0=nothing)
	pr = pr0 === nothing ? mkprob(n, w; r=r, edge=edge) : pr0
	rng = Xoshiro(seed)
	best = nothing
	bl = Inf
	t0 = time()
	tries = 0
	inits = pr.w >= comb_w(n) ? [init_comb, init_comb, init_cluster, init_row] :
		[init_cluster, init_row, init_rand]
	while time()-t0 < budget
		tries += 1
		x = if x0 !== nothing && tries == 1
			copy(x0)
		elseif best !== nothing && rand(rng) < 0.5
			perturb(best, pr, rng; amp=0.05+0.4*rand(rng))
		else
			padwp(inits[1+(tries%length(inits))](pr, rng), pr.w)
		end
		x = polish(x, pr)
		c = check(x, pr)
		if c.ok && c.len < bl
			bl = c.len
			best = copy(x)
			verbose && @printf("  [%5.1fs try %3d] len=%.4f\n", time()-t0, tries, bl)
		end
	end
	pr, best, bl, tries
end

# greedy removal of waypoints that are not needed
function prune(x, pr)
	improved = true
	while improved && pr.w > 1
		improved = false
		for k in 1:pr.w
			pr2, y = drop_step(x, pr, k)
			y = polish(y, pr2)
			c = check(y, pr2)
			if c.ok && c.len <= check(x, pr).len+1e-9
				pr, x = pr2, y
				improved = true
				break
			end
		end
	end
	pr, x
end

# ---------- output ----------

function to_json(x, pr, path)
	p = mkpath(pr)
	build!(p, x, pr)
	c = check(x, pr)
	traj = Dict{String,Any}()
	for i in 1:pr.n
		pts = [[p[1,i,k], p[2,i,k]] for k in 1:pr.w+2]
		d = sum(hypot(p[1,i,k+1]-p[1,i,k], p[2,i,k+1]-p[2,i,k]) for k in 1:pr.w+1)
		traj[string(i-1)] = Dict("path" => pts, "distance" => d)
	end
	wps = [[[x[1,i,k], x[2,i,k]] for i in 1:pr.n] for k in 1:pr.w]
	meta = Dict(
		"n_disks" => pr.n,
		"n_waypoints" => pr.w,
		"disk_radius" => pr.r,
		"edge_length" => pr.edge,
		"polygon_circumradius" => pr.circ,
		"path_length" => c.len,
		"fitness" => c.len,
		"n_touched" => c.ntouch,
		"total_pairs" => npair(pr),
		"all_pairs_touch" => c.ntouch == npair(pr),
		"n_violations" => c.maxover > TOL_OVER ? 1 : 0,
		"max_overlap" => c.maxover,
		"has_path_collisions" => c.maxover > TOL_OVER,
		"path_collision_penalty" => max(0.0, c.maxover),
		"valid" => c.ok,
		"solver" => "opus_5/toast.jl (continuous-time penalty + L-BFGS)")
	open(path, "w") do f
		JSON.print(f, Dict(
			"waypoints" => wps,
			"initial_positions" => [[pr.h[1,i], pr.h[2,i]] for i in 1:pr.n],
			"disk_trajectories" => traj,
			"metadata" => meta))
	end
	c
end

function load_json(path)
	d = JSON.parsefile(path)
	m = d["metadata"]
	n = Int(m["n_disks"])
	tr = d["disk_trajectories"]
	pth = [Float64.(reduce(vcat, [q' for q in tr[string(i-1)]["path"]])) for i in 1:n]
	w = size(pth[1], 1)-2
	r = Float64(get(m, "disk_radius", 0.3))
	ip = [Float64.(q) for q in d["initial_positions"]]
	edge = Float64(get(m, "edge_length", hypot(ip[1][1]-ip[2][1], ip[1][2]-ip[2][2])))
	pr = mkprob(n, w; r=r, edge=edge)
	for i in 1:n			# trust the file's own home positions
		pr.h[1,i] = ip[i][1]
		pr.h[2,i] = ip[i][2]
	end
	x = Array{Float64}(undef, 2, n, w)
	for i in 1:n, k in 1:w
		x[1,i,k] = pth[i][k+1,1]
		x[2,i,k] = pth[i][k+1,2]
	end
	pr, x
end

function main()
	n = 5
	w = 0
	budget = 60.0
	seed = 1
	out = ""
	initf = ""
	doprune = false
	radial = false
	a = ARGS
	i = 1
	while i <= length(a)
		if a[i] == "-n"
			n = parse(Int, a[i+1]); i += 2
		elseif a[i] == "-w"
			w = parse(Int, a[i+1]); i += 2
		elseif a[i] == "-t"
			budget = parse(Float64, a[i+1]); i += 2
		elseif a[i] == "-s"
			seed = parse(Int, a[i+1]); i += 2
		elseif a[i] == "-o"
			out = a[i+1]; i += 2
		elseif a[i] == "--init"
			initf = a[i+1]; i += 2
		elseif a[i] == "--prune"
			doprune = true; i += 1
		elseif a[i] == "--radial"
			radial = true; i += 1
		else
			error("unknown arg $(a[i])")
		end
	end
	x0 = nothing
	pr0 = nothing
	if initf != ""
		pr0, x0 = load_json(initf)
		n, w = pr0.n, pr0.w
	end
	w == 0 && (w = comb_w(n)+2)
	radial && initf == "" && w == comb_w(n)+2 && (w = 2*n)
	@printf("n=%d w=%d budget=%.0fs seed=%d%s\n", n, w, budget, seed, radial ? " radial" : "")
	pr, x, l, tries = radial ? search_rad(n, w; budget=budget, seed=seed) :
		search(n, w; budget=budget, seed=seed, x0=x0, pr0=pr0)
	if x === nothing
		println("no valid solution found in $tries tries")
		return
	end
	if doprune
		pr, x = prune(x, pr)
		@printf("pruned to w=%d len=%.4f\n", pr.w, check(x, pr).len)
	end
	pr, x = pin_touches(x, pr)
	c = check(x, pr)
	lb = lowbound(pr)
	@printf("final: w=%d len=%.6f touched=%d/%d maxover=%.2e valid=%s (%d tries)\n",
		pr.w, c.len, c.ntouch, npair(pr), c.maxover, c.ok, tries)
	@printf("       lower bound %.6f, gap %+.2f%%\n", lb, 100*(c.len/lb-1))
	if out != ""
		to_json(x, pr, out)
		println("wrote $out")
	end
end

if abspath(PROGRAM_FILE) == (@__FILE__)
	main()
end
