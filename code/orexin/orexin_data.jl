# orexin_data.jl — shared constants, data loaders, and session pairer
# include()'d by analyze_orexin.jl and bayesian_orexin.jl

const BASE_DIR = expanduser("/usr/local/etc/Orexin")
const PARTICIPANTS = ["Niplav", "Sam", "Nomagicpill"]
const MAX_PAIR_GAP_DAYS = 14

function load_json_safe(path)
	isfile(path) || return []
	content = read(path, String)
	# Fix trailing commas (Ethan's digit_span.json)
	content = replace(content, r",\s*\]" => "]")
	content = replace(content, r",\s*\}" => "}")
	JSON.parse(content)
end

function load_niplav_tracking()
	rows = []
	path = joinpath(BASE_DIR, "Niplav", "tracking.csv")
	isfile(path) || return rows
	for line in eachline(path)
		parts = split(line, ',')
		length(parts) < 2 && continue
		ts, substance = parts[1], parts[2]
		date_str = split(ts, 'T')[1]
		cond = if substance == "water"
			"placebo"
		elseif substance == "orexin-a"
			"orexin"
		else
			continue
		end
		push!(rows, (participant="Niplav", date=Date(date_str), condition=cond))
	end
	rows
end

function load_xlsx_tracking(participant, xlsx_path, cond_col, cond_map)
	rows = []
	isfile(xlsx_path) || return rows
	xf = XLSX.readxlsx(xlsx_path)
	sn = XLSX.sheetnames(xf)[1]
	data = XLSX.readtable(xlsx_path, sn)

	dates = data.data[1]
	conds = data.data[cond_col]

	for i in eachindex(dates)
		d = dates[i]
		c = conds[i]
		ismissing(d) && continue
		ismissing(c) && continue

		dt = if d isa DateTime
			Date(d)
		elseif d isa Date
			d
		else
			continue
		end

		cond_str = string(c)
		mapped = get(cond_map, cond_str, nothing)
		isnothing(mapped) && continue
		push!(rows, (participant=participant, date=dt, condition=mapped))
	end
	rows
end

function load_sam_tracking()
	load_xlsx_tracking(
		"Sam",
		joinpath(BASE_DIR, "Sam", "sh ox notes.xlsx"),
		3,
		Dict("real" => "orexin", "placebo" => "placebo", "BASELINE DAY" => "baseline")
	)
end

function load_nomagicpill_tracking()
	load_xlsx_tracking(
		"Nomagicpill",
		joinpath(BASE_DIR, "Nomagicpill", "Orexin Tracking.xlsx"),
		6,
		Dict("Orexin" => "orexin", "Placebo" => "placebo", "Baseline day" => "baseline")
	)
end

function load_all_tracking()
	tracking = vcat(load_niplav_tracking(), load_sam_tracking(), load_nomagicpill_tracking())
	filter(r -> r.condition in ("orexin", "placebo"), tracking)
end

function match_to_condition(entries, tracking, participant; window_h=24)
	matched = []
	p_tracking = filter(r -> r.participant == participant, tracking)
	for entry in entries
		ts_str = get(entry, "timestamp", get(entry, "date", nothing))
		isnothing(ts_str) && continue
		entry_date = Date(split(ts_str, 'T')[1])
		entry_dt = DateTime(split(ts_str, '.')[1], dateformat"yyyy-mm-ddTHH:MM:SS")

		for t in p_tracking
			dose_dt = DateTime(t.date)
			if entry_date == t.date || (entry_dt >= dose_dt && entry_dt <= dose_dt + Hour(window_h))
				push!(matched, (entry=entry, condition=t.condition, participant=participant, date=t.date, datetime=entry_dt))
				break
			end
		end
	end
	matched
end

function load_sleep_data(participant)
	sleep_dir = joinpath(BASE_DIR, participant, "fitbit", "sleep")
	isdir(sleep_dir) || return Dict{String, Any}()

	by_date = Dict{String, Any}()
	for f in readdir(sleep_dir, join=true)
		endswith(f, ".json") || continue
		records = load_json_safe(f)
		for r in records
			get(r, "isMainSleep", false) || continue
			dos = get(r, "dateOfSleep", nothing)
			isnothing(dos) && continue
			by_date[dos] = r
		end
	end
	by_date
end

function load_fitbit_daily(participant, subdir)
	dir = joinpath(BASE_DIR, participant, "fitbit", subdir)
	isdir(dir) || return Dict{String, Any}()
	by_date = Dict{String, Any}()
	for f in readdir(dir, join=true)
		endswith(f, ".json") || continue
		records = load_json_safe(f)
		for r in records
			dt = get(r, "dateTime", nothing)
			isnothing(dt) && continue
			by_date[dt] = r
		end
	end
	by_date
end

# Greedy nearest-neighbor session pairing for crossover analysis.
# For each participant, matches orexin ↔ placebo sessions within MAX_PAIR_GAP_DAYS.
# Matches from the smaller group to the larger; unmatched sessions are silently excluded.
# Returns Vector of (participant, orexin_date, placebo_date) NamedTuples.
function match_sessions(tracking)
	pairs = NamedTuple[]
	for p in PARTICIPANTS
		p_track = filter(r -> r.participant == p, tracking)
		orx_dates = sort([r.date for r in p_track if r.condition == "orexin"])
		plc_dates = sort([r.date for r in p_track if r.condition == "placebo"])
		(isempty(orx_dates) || isempty(plc_dates)) && continue

		if length(orx_dates) <= length(plc_dates)
			small, large, small_is_orexin = orx_dates, plc_dates, true
		else
			small, large, small_is_orexin = plc_dates, orx_dates, false
		end

		used = falses(length(large))
		for sd in small
			best_i = 0
			best_gap = typemax(Int)
			for (i, ld) in enumerate(large)
				used[i] && continue
				gap = abs(Dates.value(sd - ld))
				if gap < best_gap
					best_gap = gap
					best_i = i
				end
			end
			best_i == 0 && continue
			best_gap > MAX_PAIR_GAP_DAYS && continue
			used[best_i] = true
			od = small_is_orexin ? sd : large[best_i]
			pd = small_is_orexin ? large[best_i] : sd
			push!(pairs, (participant=p, orexin_date=od, placebo_date=pd))
		end
	end
	pairs
end
