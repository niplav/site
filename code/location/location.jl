using CSV, DataFrames

approaches=CSV.read("./daygame_approaches.csv", DataFrame)
successes=approaches[!,["Location", "Contact info"]]
rename!(successes, Symbol("Contact info")=>:Contact)
replace!(successes[!, :Contact], ["number" => "1", "insta" => "1", "insta given" => "1", "number given" => "1", "facebook" => "1", "email" => "1"]...)
successes=coalesce.(successes, "0")
successes[!, :Contact]=map(string->parse(Int, string), successes[!, :Contact])
