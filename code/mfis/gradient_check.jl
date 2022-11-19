using Random, LinearAlgebra

function gradient_check(x, f, df)
	n=length(x)
	d=length(f(x))
	ε=10^-6
	J=zero(Matrix{Float64}(undef, d, n))
	for i in 1:n
		unit=zero(rand(n))
		unit[i]=1
		J[:,i].=(f(x+ε*unit)-f(x-ε*unit))/(2*ε)
	end
	if norm(J-df(x), Inf)<10^-4
		return true
	else
		return false
	end
end
