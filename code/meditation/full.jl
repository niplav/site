# Should I go to Lumbini for three months? Command-line frontend to retreat.jl.
#
#	julia full.jl			fit and price
#	julia full.jl --prior		price off the prior, skipping the likelihood
#	julia full.jl --quick		400 draws, for checking the plumbing
#	julia full.jl --synthetic	parameter-recovery check on the fit

include(joinpath(@__DIR__, "retreat.jl"))
using .Retreat, Gekrakel, Statistics, MCMCChains

const PRIOR = "--prior" in ARGS
const SYNTHETIC = "--synthetic" in ARGS
const DRAWS = "--quick" in ARGS ? 400 : 1500

table(df) = (show(stdout, df; summary = false, eltypes = false,
	show_row_number = false, allrows = true, truncate = 0); println())

function main()
	D = SYNTHETIC ? synthetic() : load_data()
	SYNTHETIC || println(length(D.span), " people, ", length(D.days), " periods, ",
		count(D.web), " from the web, ", count(!, D.known), " outcome-unknown\n",
		D.n_miss, "/", length(D.days), " intensities latent across ",
		length(D.types), " practice types")

	# MCMCChains for summarystats; Turing >= 0.45 defaults to FlexiChains
	chain = fit_se(D; draws = DRAWS, prior = PRIOR, chain_type = MCMCChains.Chains)
	PRIOR && println("\n!! PRIOR MODE: the likelihood was not evaluated. ",
		"Everything below is a\n!! prior predictive check.")
	show(stdout, MIME("text/plain"), summarystats(chain[SYNTHETIC ? PARS[PARS .!= :b_src] : PARS]))
	println()
	SYNTHETIC && return chain

	P = posterior(chain, D)
	W = World()		# after posterior(), which fixes the particle count

	println("\npractice history: ", round(Int, P.acc0), " formal hours before the decision point")
	w = dose_warning(P)
	w === nothing || show(stdout, MIME("text/plain"), w)
	println("\ndose-response, p(cessation)")
	table(dose_table(P))

	println("\naccrual window (years)\n  ", spark(W.window), "  median ",
		round(median(W.window), digits = 1), "   90% ",
		round(quantile(W.window, 0.05), digits = 1), " – ",
		round(quantile(W.window, 0.95), digits = 1))

	println("\nscenarios")
	table(scenario_table(W, P))
	println("\nsensitivity of Lumbini standard to the cost schedule")
	table(sensitivity_table(W, P))

	v = value(W, P, 12.0, 90)
	println("\nLumbini, 3 months, 12 hr/day — net value\n  ", spark(v.net),
		"\n  90% ", ci(v.net), "   median ", money(median(v.net)),
		"   mean ", money(mean(v.net)),
		"\n  supramundane ", money(mean(v.supramundane)),
		"   mundane ", money(mean(v.mundane)), "   cost ", money(mean(v.cost)))
	println("\nPrefer the median and P(net>0): E[net] is driven by the 5% tail ",
		"of value_se_per_year.")
	return chain
end

main()
