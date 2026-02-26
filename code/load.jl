using CSV, DataFrames, JSON3, Dates, TimeZones

const _LOAD_DATA_DIR = joinpath(@__DIR__, "..", "data")
const _FITBIT_DIR = "/usr/local/backup/fitbit"

function get_meditations()
	df = CSV.read(joinpath(_LOAD_DATA_DIR, "meditations.csv"), DataFrame)
	df = transform(df,
		:meditation_start => ByRow(s -> ZonedDateTime(s, dateformat"yyyy-mm-ddTHH:MM:SSzzz")) => :meditation_start,
		:meditation_end   => ByRow(s -> ZonedDateTime(s, dateformat"yyyy-mm-ddTHH:MM:SSzzz")) => :meditation_end,
	)
	return df
end

function get_sleep()
	sleep_dir = joinpath(_FITBIT_DIR, "sleep")
	records = []
	for f in sort(readdir(sleep_dir, join=true))
		endswith(f, ".json") || continue
		append!(records, JSON3.read(read(f, String)))
	end
	return records  # raw vector of NamedTuples; caller converts to DataFrame as needed
end
