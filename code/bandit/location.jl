using CSV, Distributions, DataFrames

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

weekday_good_weather=[709269, 449256, 76108, 449052, 175735, 276017, 796877, 835159, 823073, 696163, 843941, 132388, 496077, 32441, 399686]
weekday_bad_weather=[709269, 449256, 76108, 449052]
weekend_good_weather=[692404, 10939, 709269, 157691, 175735, 276017, 702595, 449256, 76108, 793915, 796877, 835159, 823073, 696163, 531828, 781627, 843941, 132388, 496077, 371851, 32441, 399686, 449052]
weekend_bad_weather=[709269, 449256, 76108, 449052, 702595, 531828]

locations=CSV.File("/home/niplav/admn/daygame/locations") |> DataFrame

bandit=innerjoin(bandit, locations, on=:location=>:id)

println(sort(bandit, :sample))
