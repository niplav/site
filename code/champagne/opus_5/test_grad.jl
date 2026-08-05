include("toast.jl")
# finite-difference check of the analytic gradient in fg!
using Random
pr=mkprob(4,5)
rng=Xoshiro(7)
x=init_cluster(pr,rng)
p=mkpath(pr); g=mkpath(pr)
lt,lc=1.3,7.7
mu=[0.3*(i+j) for i in 1:pr.n, j in 1:pr.n]
build!(p,x,pr); f0=fg!(g,p,pr,mu,lt,lc)
err=0.0
h=1e-6
for i in 1:pr.n, k in 1:pr.w, d in 1:2
	y=copy(x); y[d,i,k]+=h; build!(p,y,pr); fp=fg!(mkpath(pr),p,pr,mu,lt,lc)
	y=copy(x); y[d,i,k]-=h; build!(p,y,pr); fm=fg!(mkpath(pr),p,pr,mu,lt,lc)
	num=(fp-fm)/(2h)
	global err=max(err,abs(num-g[d,i,k+1]))
end
println("f0=",f0," max grad err=",err)
