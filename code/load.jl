using CSV, DataFrames, JSON3, Dates, TimeZones

const _LOAD_DATA_DIR = joinpath(@__DIR__, "..", "data")
const _FITBIT_DIR = "/usr/local/backup/fitbit"

const _DT_FORMAT_MS  = dateformat"yyyy-mm-ddTHH:MM:SS.ssszzzz"
const _DT_FORMAT_SEC = dateformat"yyyy-mm-ddTHH:MM:SSzzzz"

function parse_zdt(s::AbstractString)
	str = String(s)
	try return parse(ZonedDateTime, str, _DT_FORMAT_MS) catch end
	try return parse(ZonedDateTime, str, _DT_FORMAT_SEC) catch end
	throw(ArgumentError("Unable to parse ZonedDateTime from: \"$s\""))
end

function get_meditations()
	df = CSV.read(joinpath(_LOAD_DATA_DIR, "meditations.csv"), DataFrame)
	df = transform(df,
		:meditation_start => ByRow(parse_zdt) => :meditation_start,
		:meditation_end   => ByRow(parse_zdt) => :meditation_end,
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
