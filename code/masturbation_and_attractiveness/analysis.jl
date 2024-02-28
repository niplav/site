using DataFrames, CSV

approaches=CSV.read("../../data/daygame_approaches.csv", DataFrame)
sessions=CSV.read("../../data/daygame_sessions.csv", DataFrame)
