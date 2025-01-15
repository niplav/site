using DataFrames, CSV, Distributions

approaches = CSV.File("../../data/daygame_approaches.csv") |> DataFrame
sessions = CSV.File("../../data/daygame_sessions.csv") |> DataFrame
