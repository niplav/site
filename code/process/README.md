# Supplement Stack Optimizer

Two Gaussian Processes (morning + evening) with Thompson Sampling over
the binary space {0,1}^n of supplement stacks. The GPs capture arbitrary
non-linear interactions between supplements — no additivity assumption
needed.

Substances are split into two intake windows because the single-GP model
produces nonsensical stacks like "caffeine + melatonin":

- **Morning** (taken before 18:00, effects same day): caffeine, creatine, l-theanine, nicotine, omega3, sugar, vitaminb12, vitamind3
- **Evening** (taken ≥ 18:00, effects next day): creatine, magnesium, melatonin

## Usage

```bash
./supplement_optimizer.py                            # recommend morning + evening stacks (default: productivity)
./supplement_optimizer.py happy                      # recommend for a different variable
./supplement_optimizer.py --cached happy             # skip rebuild, use last saved models (faster)
./supplement_optimizer.py --exclude nicotine happy   # exclude substance from recommendations
./supplement_optimizer.py --exclude nicotine,sugar   # exclude multiple (comma-separated, no spaces)
./supplement_optimizer.py stats                      # show effects & top stacks (productivity)
./supplement_optimizer.py stats happy                # stats for a different variable
./supplement_optimizer.py update 0.4                 # log today's productivity score
./supplement_optimizer.py update 67 happy            # log today's happy score
./supplement_optimizer.py init happy                 # explicit rebuild of both GPs (not usually needed)
```

Optimizeable variables: `happy`, `content`, `relaxed`, `horny` (from
`mood.csv`), `productivity`, `creativity`, `sublen`, `meaning` (from
`mental.csv`).

Each recommend/stats/update call rebuilds from the CSVs automatically
— no separate init step needed.

## Setup

```bash
uv pip install scikit-learn pandas numpy joblib
```

## Reading the kernel

Each GP learns a lengthscale per supplement. This is the most reliable output:

- **lengthscale → 0** (e.g. 0.01): detectable effect.
- **lengthscale → ∞** (e.g. 100): no signal in the data.

```
Morning:
length_scale=[0.01, 100, 100, 0.01, 0.01, 100, 100, 0.01]
             caff   crea  thea  nic   om3   sug   b12   d3
             ^^^^         ^^^^  ^^^^              ^^^^
             detectable   detectable              detectable

Evening:
length_scale=[0.01, 0.01, 0.01]
             crea  mag   mel
             ^^^^  ^^^^  ^^^^
             all detectable
```

## How it works

1. **Morning/evening split**: substances are assigned to one or both periods based on explicit lists in `MORNING_SUBSTANCES` / `EVENING_SUBSTANCES`. Evening intakes (≥ 18:00) are date-shifted to the *next* day so they align with the mood reading they actually affect.
2. **Training data**: each day becomes one row per GP — a binary vector of which supplements (from that period's list) were taken, and the mean outcome for that day.
3. **GP surrogate**: a Matérn 5/2 GP with per-supplement lengthscales (ARD) is fit for each period. It learns a smooth function over {0,1}^n, capturing interactions automatically.
4. **Thompson Sampling**: all 2^n candidate stacks are enumerated. One sample is drawn from the *joint* GP posterior (correlations between similar stacks are respected). The stack with the highest sampled value is recommended.
5. **Exploration**: stacks the GP is uncertain about occasionally get recommended. This is intentional — it's how the system learns about stacks you haven't tried. Run it again for a different recommendation.

## Notes

- The substance lists are hardcoded constants — edit `MORNING_SUBSTANCES` / `EVENING_SUBSTANCES` in the config section to change them.
- **Exclusions**: Use `--exclude sub1,sub2` to prevent specific substances from being recommended. The GP is still trained on the full data (so it learns their effects), but they won't appear in recommendations. For permanent exclusions, add them to `EXCLUDED_SUBSTANCES` in the config.
- Mood variables are aggregated to daily means. Mental variables use one reading per day.
- State files are per-period: `gp_data_{variable}_{morning,evening}.json`, `gp_model_{variable}_{morning,evening}.pkl`.
