using CSV
using Distributions
using DataFrames

function select_location(dg_locations, successes, failures)
    num_locations = length(dg_locations)
    theta = [Beta(successes[i] + 1, failures[i] + 1) for i in 1:num_locations]
    samples = [rand(theta[i]) for i in 1:num_locations]
    return dg_locations[argmax(samples)]
end

function update_location(dg_locations, selected_location, success)
    location_index = findfirst(x -> x == selected_location, dg_locations)
    if success
        successes[location_index] += 1
    else
        failures[location_index] += 1
    end
end

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

# Perform the bandit algorithm
for i in 1:length(locations)
    selected_location = select_location(dg_locations, successes, failures)

    # Simulate success or failure based on "Enjoyment" column
    success = contacts[i] == 1

    # Update success/failure counts
    update_location(dg_locations, selected_location, success)
end

# Print the estimated success probabilities
for i in 1:length(dg_locations)
    success_prob = successes[i] / (successes[i] + failures[i])
    println("Shop: $(dg_locations[i]), Success Probability: $success_prob")
end

# Choose the best location based on the estimated success probabilities
best_location = dg_locations[argmax(successes + failures)]
println("Best Shop: $best_location")
