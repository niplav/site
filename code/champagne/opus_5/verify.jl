#!/usr/bin/env julia

# Independently re-check champagne solution JSONs (any of them, mine or not)
# against the continuous-time criteria: does every pair of disks become
# tangent at some point, does any pair ever overlap *between* waypoints, and
# does every disk actually return home?
#
#	julia verify.jl file.json [file.json ...]

include("toast.jl")

@printf("%-24s %2s %3s %10s %10s %7s %7s %9s %9s %9s\n",
	"file", "n", "w", "length", "bound", "gap", "touch", "maxover", "needtol",
	"homeerr")
for f in ARGS
	pr, x = load_json(f)
	c = check(x, pr)
	lb = lowbound(pr)
	d = JSON.parsefile(f)
	he = 0.0
	for i in 1:pr.n
		pth = d["disk_trajectories"][string(i-1)]["path"]
		for q in (pth[1], pth[end])
			he = max(he, hypot(q[1]-pr.h[1,i], q[2]-pr.h[2,i]))
		end
	end
	@printf("%-24s %2d %3d %10.4f %10.4f %+6.1f%% %3d/%-3d %9.2e %9.2e %9.2e%s\n",
		basename(f), pr.n, pr.w, c.len, lb, 100*(c.len/lb-1),
		c.ntouch, npair(pr), c.maxover, c.worstgap, he,
		c.ok ? "" : "  INVALID")
end
