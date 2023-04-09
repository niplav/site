using CSV, DataFrames, Distributions
using Distributions, Statistics, ConjugatePriors

struct BetaBernoulli
	pθ::Array{Beta{Float64}}
end

BetaBernoulli(K) =
	BetaBernoulli([Beta(1, 1) for _ in 1:K])

Base.length(b::BetaBernoulli) = length(b.pθ)
Base.iterate(b::BetaBernoulli) = b.pθ[1], 1
Base.iterate(b::BetaBernoulli, i) =
	i < length(b) ? (b.pθ[i+1], i+1) : nothing

(b::BetaBernoulli)(act) = begin
	θ = rand.(b.pθ)
	a = argmax(θ)
	r = act(a)
	b.pθ[a] = posterior(b.pθ[a], Bernoulli, [r])
	a
end

struct PalmerEnv
	locations::DataFrame
	success_probs::Matrix{Bernoulli{Float64}}
end

PalmerEnv(locations, success_probs) =
	PalmerEnv(locations,
			  Bernoulli.(success_probs))

(env::PalmerEnv)(location) =
	rand(env.success_probs[location])

Base.size(env::PalmerEnv, kwargs...) = size(env.locations, kwargs...)
Base.getindex(env::PalmerEnv, i) = env.locations[i,:]
Base.rand(env::PalmerEnv, n::Integer = 1) = env[rand(1:size(env, 1), n)]

approaches=CSV.read("../../data/daygame_approaches.csv", DataFrame)
successes=approaches[!,["Location", "Contact info"]]
rename!(successes, Symbol("Contact info")=>:Contact)
replace!(successes[!, :Contact], ["number" => "1", "insta" => "1", "insta given" => "1", "number given" => "1", "facebook" => "1", "email" => "1"]...)
successes=coalesce.(successes, "0")
successes[!, :Contact]=map(string->parse(Int, string), successes[!, :Contact])
success_freq=combine(groupby(successes, :Location), :Contact => mean)[!, :Contact_mean]

agent=BetaBernoulli(length(success_freq))
expected_reward(location)=success_freq[location]
θ_max=expected_reward(argmax(success_freq))

#run(env, agent, θmax, expected_reward; rounds) = begin
#    map(1:rounds) do _
#        penguin = first(rand(env))
#        a = agent(fish -> env(fish, penguin))
#        θ = expected_reward(a)
#        ρ = θmax - θ
#    end
#end
#
#expected_reward(fish) = fish_eat_probs.eaten_mean[fish]
#θ_max = expected_reward(argmax(fish_eat_probs.eaten_mean))
#regrets = run(env, agent, θ_max, expected_reward; rounds = 1000);
