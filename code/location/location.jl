using CSV
using Distributions
using DataFrames

# Load data from CSV
data = CSV.File("../../data/daygame_approaches.csv") |> DataFrame

# Extract location and enjoyment information
locations = data.Location
contacts = ismissing.(data."Contact info")

# Define ice cream locations
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

weekday_bad_weather=[449052, 709269, 76108, 548236, 422985]
weekday_good_weather=[548236, 175735, 709269, 76108, 956569, 132388, 449256, 591664, 449052, 119752, 868084, 422985]
weekend_bad_weather=[449052, 709269, 76108, 548236, 422985, 10939, 702595, 531828]
weekend_good_weather=[692404,10939,548236,35322,175735,702595,709269,803955,76108,276017,52055,422985,956569,300211,132388,449256,531828,433507,591664,868084,371851,32441,119752,449052]

println(sort(bandit, :sample))
