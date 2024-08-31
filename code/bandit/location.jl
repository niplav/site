using CSV
using Distributions
using DataFrames

# Load data from CSV
data = CSV.File("../../data/daygame_approaches.csv") |> DataFrame

locations = data.Location
contacts = ismissing.(data."Contact info")

dg_locations = unique(locations)

# Initialize success and failure counts
successes = zeros(Int, length(dg_locations))
failures = zeros(Int, length(dg_locations))
success_prob = zeros(Int, length(dg_locations))

bandit=DataFrame([dg_locations, successes, failures, success_prob], [:location, :successes, :failures, :success_prob])

for i in 1:length(dg_locations)
	failures[i]=sum(ismissing.(filter(x->x[:Location]==bandit[!,1][i], data)[!,"Contact info"]))
	successes[i]=sum(.!ismissing.(filter(x->x[:Location]==bandit[!,1][i], data)[!,"Contact info"]))
end

success_prob=successes ./ (successes .+ failures)

bandit[!, :successes]=successes
bandit[!, :failures]=failures
bandit[!, :success_prob]=success_prob
bandit[!, :dist]=[Beta(bandit[!,2][i] + 1, bandit[!,3][i] + 1) for i in 1:length(bandit[!,1])]
bandit[!, :sample]=rand.(bandit[!, :dist])

weekday_good_weather=[702595, 76108, 843941, 823073, 696163, 276017, 835159, 496077, 709269, 132388, 449256, 449052, 175735]
weekday_bad_weather=[709269, 449052, 76108, 449256, 817198]
weekend=[175735, 157691, 449052, 692404, 449256, 132388, 32441, 10939, 793915, 781627, 709269, 371851, 496077, 835159, 276017, 531828, 696163, 823073, 796877, 843941, 399686, 76108, 702595]


locations=CSV.File("/home/niplav/admn/daygame/locations") |> DataFrame

bandit=innerjoin(bandit, locations, on=:location=>:id)

println(sort(bandit, :success_prob))
