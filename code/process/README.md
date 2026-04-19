# Supplement Stack Optimizer

Two Gaussian Processes (morning + evening) with Thompson Sampling over
the binary space {0,1}^n of supplement stacks. The GPs capture arbitrary
non-linear interactions between supplements — no additivity assumption
needed.

Substances are split into two intake windows because the single-GP model
produces nonsensical stacks like "caffeine + melatonin":

- **Morning** (taken before 18:00, effects same day): caffeine, creatine, l-theanine, nicotine, omega3, sugar, vitaminb12, vitamind3, l-glycine, magnesium
- **Evening** (taken ≥ 18:00, effects next day): creatine, magnesium, melatonin, l-glycine, zinc

Interventions (non-substance tracked practices) are included per period:

- **Morning**: meditation, lumenator, masturbation
- **Evening**: meditation, masturbation

## Usage

```bash
./optimizer.jl                            # recommend morning + evening stacks (default: productivity)
./optimizer.jl happy                      # recommend for a different variable
./optimizer.jl --cached happy             # skip rebuild, use last saved models (faster)
./optimizer.jl --exclude nicotine happy   # exclude substance from recommendations
./optimizer.jl --exclude nicotine,sugar   # exclude multiple (comma-separated, no spaces)
./optimizer.jl stats                      # show effects & top stacks (productivity)
./optimizer.jl stats happy                # stats for a different variable
./optimizer.jl update 0.4                 # log today's productivity score
./optimizer.jl update 67 happy            # log today's happy score
./optimizer.jl init happy                 # explicit rebuild of both GPs (not usually needed)
```

Optimizeable variables: `happy`, `content`, `relaxed`, `horny` (from
`mood.csv`), `productivity`, `creativity`, `sublen`, `meaning` (from
`mental.csv`).

Each recommend/stats/update call rebuilds from the CSVs automatically
— no separate init step needed.

## Reading the stats output

The `stats` command shows marginal effects per feature: the difference in
posterior mean between stacks containing that feature vs. stacks without
it, averaged over all other feature combinations. This is the most useful
signal for deciding what to keep or cut.

Notable findings as of 2026-04:

- **productivity**: caffeine (+0.067) and nicotine (+0.015) have the
  strongest positive effects. Sugar (−0.012) and l-theanine (−0.008)
  are slightly negative.
- **meaning**: everything makes the day less meaningful — except
  masturbation (+0.18). Caffeine (−0.35), meditation (−0.31), and
  vitamind3 (−0.29) have the largest negative associations, though
  these are likely confounds rather than causal effects (caffeine →
  work/grind days; meditation days may correlate with already-low meaning).

## How it works

1. **Morning/evening split**: substances are assigned to one or both periods based on explicit lists in `MORNING_SUBSTANCES` / `EVENING_SUBSTANCES`. Evening intakes (≥ 18:00) are date-shifted to the *next* day so they align with the mood reading they actually affect.
2. **Training data**: each day becomes one row per GP — a binary vector of which supplements and interventions (from that period's list) were taken, and the mean outcome for that day.
3. **GP surrogate**: a Matérn 5/2 GP with uniform lengthscales is fit for each period. It learns a smooth function over {0,1}^n, capturing interactions automatically.
4. **Thompson Sampling**: all 2^n candidate stacks are enumerated. One sample is drawn from the *joint* GP posterior (correlations between similar stacks are respected). The stack with the highest sampled value is recommended.
5. **Exploration**: stacks the GP is uncertain about occasionally get recommended. This is intentional — it's how the system learns about stacks you haven't tried. Run it again for a different recommendation.

## Notes

- The substance lists are hardcoded constants — edit `MORNING_SUBSTANCES` / `EVENING_SUBSTANCES` in the config section to change them.
- **Exclusions**: Use `--exclude sub1,sub2` to prevent specific substances from being recommended. The GP is still trained on the full data (so it learns their effects), but they won't appear in recommendations. For permanent exclusions, add them to `EXCLUDED_SUBSTANCES` in the config.
- Mood variables are aggregated to daily means. Mental variables use one reading per day.
- State files are per-period: `gp_data_{variable}_{morning,evening}.json`, `gp_model_{variable}_{morning,evening}.jld2`.
