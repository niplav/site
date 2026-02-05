#!/usr/local/etc/uv/venvs/main/bin/python
"""
Supplement Stack Optimizer — GP + Thompson Sampling

Fits a Gaussian Process over the binary space {0,1}^n of supplement stacks
and recommends stacks via Thompson Sampling. The GP captures arbitrary
non-linear interactions between supplements.

Usage:
    python supplement_optimizer.py --init -m happy
    python supplement_optimizer.py --recommend -m happy
    python supplement_optimizer.py --stats -m happy
    python supplement_optimizer.py --update 2026-02-04 67.5 -m happy
"""

import json
import sys
import warnings
from datetime import date, datetime
from itertools import product
from pathlib import Path

import numpy as np
import joblib
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR / ".." / ".." / "data"
STATE_DIR = SCRIPT_DIR / "state"

SUBSTANCES_FILE = DATA_DIR / "substances.csv"
MOOD_FILE = DATA_DIR / "mood.csv"
MENTAL_FILE = DATA_DIR / "mental.csv"

STATE_DIR.mkdir(parents=True, exist_ok=True)

MOOD_VARIABLES = ["happy", "content", "relaxed", "horny"]
MENTAL_VARIABLES = ["productivity", "creativity", "sublen", "meaning"]
ALL_VARIABLES = MOOD_VARIABLES + MENTAL_VARIABLES
MIN_SUPPLEMENT_COUNT = 20

MORNING_SUBSTANCES = ["caffeine", "creatine", "l-theanine", "nicotine", "omega3", "sugar", "vitaminb12", "vitamind3"]
EVENING_SUBSTANCES = ["creatine", "magnesium", "melatonin"]

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


EVENING_CUTOFF_HOUR = 18  # substances taken at or after this hour count for the next day


def load_substances():
    df = pd.read_csv(SUBSTANCES_FILE)
    df["datetime"] = pd.to_datetime(df["datetime"], format="mixed", utc=True, errors="coerce")
    # Evening substances (>= 18:00) are shifted to the next calendar date so they
    # align with the next day's mood readings rather than today's (already taken).
    df["date"] = (
        df["datetime"] + pd.to_timedelta((df["datetime"].dt.hour >= EVENING_CUTOFF_HOUR).astype(int), unit="D")
    ).dt.date
    return df


def load_mood():
    df = pd.read_csv(MOOD_FILE)
    df["datetime"] = pd.to_datetime(df["alarm"])
    df["date"] = df["datetime"].dt.date
    for col in MOOD_VARIABLES:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def load_mental():
    df = pd.read_csv(MENTAL_FILE)
    df["datetime"] = pd.to_datetime(df["datetime"], format="mixed", utc=True, errors="coerce")
    df["date"] = df["datetime"].dt.date
    for col in MENTAL_VARIABLES:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def load_outcome_df(variable):
    """Return the right DataFrame for the given variable."""
    if variable in MOOD_VARIABLES:
        return load_mood()
    return load_mental()

def get_regular_supplements(substances_df):
    counts = substances_df["substance"].value_counts()
    return sorted(counts[counts >= MIN_SUPPLEMENT_COUNT].index.tolist())

def build_training_data(substances_df, mood_df, supplements, mood_variable):
    """Binary intake matrix X, daily-mean mood y, and reading counts, left-joined on mood dates."""
    daily_intake = (
        substances_df[substances_df["substance"].isin(supplements)]
        .groupby(["date", "substance"])
        .size()
        .unstack(fill_value=0)
        .clip(upper=1)
    )
    for s in supplements:
        if s not in daily_intake.columns:
            daily_intake[s] = 0
    daily_intake = daily_intake[supplements]

    daily_mood = mood_df.groupby("date")[mood_variable].mean()
    daily_counts = mood_df.groupby("date")[mood_variable].count()

    # Reindex onto all mood-dates so zero-supplement days are included
    daily_intake = daily_intake.reindex(daily_mood.index, fill_value=0)

    common_dates = sorted(daily_mood.index)
    if not common_dates:
        return None, None, None, []

    X = daily_intake.loc[common_dates].values.astype(np.float64)
    y = daily_mood.loc[common_dates].values.astype(np.float64)
    counts = daily_counts.loc[common_dates].values.astype(np.float64)

    # Drop rows where y is NaN (sparse columns like sublen, meaning)
    valid = ~np.isnan(y)
    return X[valid], y[valid], counts[valid], [d for d, v in zip(common_dates, valid) if v]

# ---------------------------------------------------------------------------
# GP model
# ---------------------------------------------------------------------------

def make_kernel(n_supplements):
    """Matérn 5/2 with per-dimension lengthscales (ARD)."""
    return ConstantKernel(
        constant_value=1.0, constant_value_bounds=(1e-2, 1e2)
    ) * Matern(
        nu=2.5,
        length_scale=np.ones(n_supplements),
        length_scale_bounds=(1e-2, 100.0),
    )

def fit_gp(X, y, counts):
    gp = GaussianProcessRegressor(
        kernel=make_kernel(X.shape[1]),
        alpha=1.0 / counts,
        n_restarts_optimizer=5,
        normalize_y=True,
    )
    # Lengthscale bounds hitting 0 or inf is expected: it means
    # "this supplement has a strong effect" or "no effect". Not a problem.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        gp.fit(X, y)
    return gp

# ---------------------------------------------------------------------------
# Candidate enumeration & Thompson Sampling
# ---------------------------------------------------------------------------

def all_stacks(n):
    """All 2^n binary vectors."""
    return np.array(list(product([0, 1], repeat=n)), dtype=np.float64)

def thompson_sample(gp, candidates):
    """
    Draw one sample from the joint GP posterior over all candidates.
    Returns (best_index, full_sample_vector).

    Joint sampling (not independent marginals) so the GP's correlation
    structure between similar stacks is respected.
    """
    mean, cov = gp.predict(candidates, return_cov=True)
    cov += np.eye(len(mean)) * 1e-6  # numerical jitter
    sample = np.random.multivariate_normal(mean, cov)
    return int(sample.argmax()), sample

# ---------------------------------------------------------------------------
# State persistence  (training data only — GP is refit each call, fast)
# ---------------------------------------------------------------------------

def state_path(mood_variable, period):
    return STATE_DIR / f"gp_data_{mood_variable}_{period}.json"

def save_state(X, y, counts, dates, supplements, mood_variable, period):
    with open(state_path(mood_variable, period), "w") as f:
        json.dump(
            {
                "supplements": supplements,
                "X": X.tolist(),
                "y": y.tolist(),
                "counts": counts.tolist(),
                "dates": [str(d) for d in dates],
            },
            f,
            indent=2,
        )

def load_state(mood_variable, period):
    path = state_path(mood_variable, period)
    if not path.exists():
        return None
    with open(path) as f:
        s = json.load(f)
    return (
        np.array(s["X"]),
        np.array(s["y"]),
        np.array(s["counts"]),
        [datetime.strptime(d, "%Y-%m-%d").date() for d in s["dates"]],
        s["supplements"],
    )

def model_path(mood_variable, period):
    return STATE_DIR / f"gp_model_{mood_variable}_{period}.pkl"

def save_model(gp, mood_variable, period):
    joblib.dump(gp, model_path(mood_variable, period))

def load_model(mood_variable, period):
    path = model_path(mood_variable, period)
    if not path.exists():
        return None
    return joblib.load(path)

# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def stack_label(supplements, vector):
    selected = [supplements[i] for i, v in enumerate(vector) if v == 1]
    return ", ".join(selected) if selected else "(nothing)"

# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def rebuild_state(mood_variable, period, substances_df):
    """Build training data for one period, save state, return (X, y, counts, dates, supplements)."""
    supplements = MORNING_SUBSTANCES if period == "morning" else EVENING_SUBSTANCES

    outcome_df = load_outcome_df(mood_variable)
    X, y, counts, dates = build_training_data(
        substances_df, outcome_df, supplements, mood_variable
    )
    if X is None or len(X) == 0:
        print(f"ERROR: No training data for {mood_variable} ({period}).")
        sys.exit(1)

    save_state(X, y, counts, dates, supplements, mood_variable, period)
    return X, y, counts, dates, supplements

def cmd_init(mood_variable):
    print("Loading data...")
    substances_df = load_substances()

    for period in ["morning", "evening"]:
        print(f"\n--- {period.capitalize()} ---")
        X, y, counts, dates, supplements = rebuild_state(mood_variable, period, substances_df)
        print(f"Tracking {len(supplements)} supplements: {', '.join(supplements)}")
        print(f"Built {len(X)} training observations ({min(dates)} to {max(dates)})")

        print("Fitting GP...")
        gp = fit_gp(X, y, counts)
        save_model(gp, mood_variable, period)

        candidates = all_stacks(len(supplements))
        mean, std = gp.predict(candidates, return_std=True)
        best = int(mean.argmax())

        print(f"\nBest predicted stack: {stack_label(supplements, candidates[best])}")
        print(f"  Predicted: {mean[best]:.1f} ± {std[best]:.1f}")
        print(f"  Kernel: {gp.kernel_}")
        print(f"  State saved to {state_path(mood_variable, period)}")

def cmd_recommend(mood_variable, cached=False):
    substances_df = None if cached else load_substances()
    results = {}

    for period in ["morning", "evening"]:
        if cached:
            gp = load_model(mood_variable, period)
            state = load_state(mood_variable, period)
            if gp is None or state is None:
                print(f"ERROR: No cached {period} model. Run without --cached first.")
                sys.exit(1)
            X, y, counts, dates, supplements = state
        else:
            X, y, counts, dates, supplements = rebuild_state(mood_variable, period, substances_df)
            gp = fit_gp(X, y, counts)
            save_model(gp, mood_variable, period)

        candidates = all_stacks(len(supplements))
        best_idx, _ = thompson_sample(gp, candidates)
        results[period] = stack_label(supplements, candidates[best_idx])

    print(f"morning: {results['morning']}")
    print(f"evening: {results['evening']}")

def cmd_stats(mood_variable):
    substances_df = load_substances()

    for period in ["morning", "evening"]:
        X, y, counts, dates, supplements = rebuild_state(mood_variable, period, substances_df)
        print(f"\nFitting {period} GP on {len(X)} observations...")
        gp = fit_gp(X, y, counts)

        candidates = all_stacks(len(supplements))
        mean, std = gp.predict(candidates, return_std=True)

        # Marginal effect: average predicted mood WITH vs WITHOUT each supplement
        print()
        print("=" * 60)
        print(f"  {period.capitalize()} — Marginal Supplement Effects")
        print("=" * 60)
        print(f"  {'Supplement':<20} {'With':>7} {'W/o':>7} {'Effect':>7}")
        print(f"  {'-'*20} {'-'*7} {'-'*7} {'-'*7}")
        for i, supp in enumerate(supplements):
            with_mean = mean[candidates[:, i] == 1].mean()
            without_mean = mean[candidates[:, i] == 0].mean()
            print(f"  {supp:<20} {with_mean:>7.1f} {without_mean:>7.1f} {with_mean - without_mean:>+7.1f}")

        # Top 10 stacks
        top10 = mean.argsort()[-10:][::-1]
        print()
        print(f"  {period.capitalize()} — Top 10 Stacks")
        print("=" * 60)
        print(f"  {'#':<3} {'Stack':<38} {'Mean':>6} {'Std':>6}")
        print(f"  {'-'*3} {'-'*38} {'-'*6} {'-'*6}")
        for rank, idx in enumerate(top10, 1):
            label = stack_label(supplements, candidates[idx])
            if len(label) > 36:
                label = label[:33] + "..."
            print(f"  {rank:<3} {label:<38} {mean[idx]:>6.1f} {std[idx]:>6.1f}")
        print("=" * 60)

        print(f"\n  Training: {len(X)} days ({min(dates)} to {max(dates)})")
        print(f"  Kernel: {gp.kernel_}")

def cmd_update(mood_variable, date_str, mood_value):
    substances_df = load_substances()
    obs_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    taken = set(
        substances_df[substances_df["date"] == obs_date]["substance"].unique()
    )

    for period, supplements in [("morning", MORNING_SUBSTANCES), ("evening", EVENING_SUBSTANCES)]:
        state = load_state(mood_variable, period)
        if state is None:
            print(f"ERROR: No {period} state file. Run init first.")
            sys.exit(1)
        X, y, counts, dates, _supplements = state

        vector = np.array([1.0 if s in taken else 0.0 for s in supplements])

        print(f"\n--- {period.capitalize()} ---")
        print(f"Date:  {obs_date}")
        print(f"Mood:  {mood_value}")
        print(f"Stack: {stack_label(supplements, vector)}")

        if obs_date in dates:
            idx = dates.index(obs_date)
            print(f"Updating existing entry for {obs_date}")
            X[idx] = vector
            y[idx] = mood_value
            counts[idx] = 1
        else:
            X = np.vstack([X, vector])
            y = np.append(y, mood_value)
            counts = np.append(counts, 1)
            dates.append(obs_date)

        save_state(X, y, counts, dates, supplements, mood_variable, period)
        print("Saved.")

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

USAGE = f"""Supplement Stack Optimizer (GP + Thompson Sampling)

Usage:
    supplement_optimizer.py [--cached] [variable]       recommend (default: productivity)
    supplement_optimizer.py stats [variable]            show effects & top stacks
    supplement_optimizer.py update <value> [variable]   log today's outcome
    supplement_optimizer.py init [variable]             explicit rebuild (not usually needed)

    --cached    skip rebuild, use last saved state (faster for repeated samples)

Variables: {', '.join(ALL_VARIABLES)}
"""

def main():
    args = sys.argv[1:]

    cached = "--cached" in args
    args = [a for a in args if a != "--cached"]

    if not args:
        cmd_recommend("productivity", cached=cached)

    elif args[0] in ALL_VARIABLES:
        cmd_recommend(args[0], cached=cached)

    elif args[0] == "stats":
        cmd_stats(args[1] if len(args) > 1 else "productivity")

    elif args[0] == "update":
        if len(args) < 2:
            print("Usage: supplement_optimizer.py update <value> [variable]")
            sys.exit(1)
        variable = args[2] if len(args) > 2 else "productivity"
        cmd_update(variable, str(date.today()), float(args[1]))

    elif args[0] == "init":
        cmd_init(args[1] if len(args) > 1 else "productivity")

    else:
        print(USAGE)
        sys.exit(1)

if __name__ == "__main__":
    main()
