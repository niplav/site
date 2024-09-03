using DataFrames, CSV, HypothesisTests, Distributions

data=CSV.read("../../data/masturbation_attractiveness_dummy_even.csv", DataFrame)

before=filter(row->row["after"]==0, data)
after=filter(row->row["after"]==1, data)

result=MannWhitneyUTest(before[!, "progress"], after[!, "progress"])
cliff_d=(2*result.U)/(result.nx*result.ny)-1
