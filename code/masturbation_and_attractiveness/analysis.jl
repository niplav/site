using DataFrames, CSV, HypothesisTests

data=CSV.read("./data/masturbation_attractiveness.csv", DataFrame)

before=filter(row->row["after"]==0, data)
after=filter(row->row["after"]==1, data)

MannWhitneyUTest(before[!, "progress"], after[!, "progress"])
