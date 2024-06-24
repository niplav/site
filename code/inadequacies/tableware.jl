using Turing, Plots

@model function ceramic_glass()
        people ~ Normal(8*10^9, 0.05)
        meals_per_day ~ truncated(Normal(2.5, 1), lower=0)
        proportion_tableware_users ~ Beta(5, 2.5) # Mean ⅔
        breakage_per_meal ~ Beta(1.5, 1000) # Mean ~0.0015
        cost_per_tableware ~ truncated(Normal(2, 0.5), lower=0) # In dollars
end

chains = sample(ceramic_glass(), IS(), 9999)
sampled=get(chains, [:people, :meals_per_day, :proportion_tableware_users, :breakage_per_meal, :cost_per_tableware])
total_cost_per_day=sampled[:people] .* sampled[:meals_per_day] .* sampled[:proportion_tableware_users] .* sampled[:breakage_per_meal] .* sampled[:cost_per_tableware]
mean(total_cost_per_day)
fig=histogram(total_cost_per_day, label="samples", xlabel="cost", ylabel="number of samples")

savefig(fig, "tableware_jl.png")
