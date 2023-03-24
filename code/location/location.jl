using CSV, DataFrames, Distributions

approaches=CSV.read("./daygame_approaches.csv", DataFrame)
successes=approaches[!,["Location", "Contact info"]]
rename!(successes, Symbol("Contact info")=>:Contact)
replace!(successes[!, :Contact], ["number" => "1", "insta" => "1", "insta given" => "1", "number given" => "1", "facebook" => "1", "email" => "1"]...)
successes=coalesce.(successes, "0")
successes[!, :Contact]=map(string->parse(Int, string), successes[!, :Contact])

thompson_sampling = Bandits.ThompsonSampling()
sb = Bandits.staticbandit([Bernoulli(0.5), Bernoulli(0.6)])
beta_agent = Bandits.BetaBernoulliAgent([0.6, 0.5], thompson_sampling, sb)
stats = Bandits.simulate(sb, beta_agent, 100)
print(stats.regret)
