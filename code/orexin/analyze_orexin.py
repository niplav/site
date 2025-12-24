#!/usr/bin/env python3
"""
Orexin-A Analysis Script
Analyzes the impact of Orexin-A on cognitive performance and sleep metrics
compared to placebo (water) during sleep deprivation.
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats
from pathlib import Path
import os
import warnings
warnings.filterwarnings('ignore')

# TODO: Make possible to pool the data from multiple people

# Data paths
SUBSTANCES_PATH = Path(__file__).parent.parent.parent / 'data' / 'substances.csv'
COGNITIVE_DATA_DIR = Path.home() / 'orexin_data'
FITBIT_SLEEP_DIR = Path('/usr/local/src/myfitbit/BS7PZZ/sleep')

def load_substances():
    """Load and parse substances data to identify orexin vs placebo administration dates."""
    df = pd.read_csv(SUBSTANCES_PATH)

    # Filter for orexin experiment (marked with 'D' in experiment column)
    orexin_exp = df[df['experiment'] == 'D'].copy()

    # Parse datetime - handle timezone-aware strings
    orexin_exp['datetime'] = pd.to_datetime(orexin_exp['datetime'], utc=True)
    # Convert to timezone-naive for easier comparison
    orexin_exp['datetime'] = orexin_exp['datetime'].dt.tz_localize(None)
    orexin_exp['date'] = orexin_exp['datetime'].dt.date

    # Create treatment labels
    orexin_exp['treatment'] = orexin_exp['substance'].map({
        'orexin-a': 'Orexin',
        'water': 'Placebo'
    })

    return orexin_exp[['datetime', 'date', 'substance', 'treatment', 'id', 'prediction']]

def load_cognitive_tests():
    """Load all cognitive test data."""
    tests = {}

    # Load PVT (Psychomotor Vigilance Task)
    with open(COGNITIVE_DATA_DIR / 'pvt.json', 'r') as f:
        pvt_data = json.load(f)
    tests['pvt'] = pd.DataFrame(pvt_data)
    tests['pvt']['timestamp'] = pd.to_datetime(tests['pvt']['timestamp'])

    # Load DSST (Digit Symbol Substitution Test)
    with open(COGNITIVE_DATA_DIR / 'dsst.json', 'r') as f:
        dsst_data = json.load(f)
    tests['dsst'] = pd.DataFrame(dsst_data)
    tests['dsst']['timestamp'] = pd.to_datetime(tests['dsst']['timestamp'])

    # Load Digit Span
    with open(COGNITIVE_DATA_DIR / 'digit_span.json', 'r') as f:
        digit_span_data = json.load(f)
    tests['digit_span'] = pd.DataFrame(digit_span_data)
    tests['digit_span']['timestamp'] = pd.to_datetime(tests['digit_span']['timestamp'])

    # Load Stanford Sleepiness Scale
    with open(COGNITIVE_DATA_DIR / 'sss.json', 'r') as f:
        sss_data = json.load(f)
    tests['sss'] = pd.DataFrame(sss_data)
    tests['sss']['timestamp'] = pd.to_datetime(tests['sss']['timestamp'])

    return tests

def load_sleep_data():
    """Load Fitbit sleep data."""
    # TODO: Calculate this from the current date and the dates of the orexin data
    sleep_files = [
        'sleep.2025.09.json',
        'sleep.2025.10.json',
        'sleep.2025.11.json',
        'sleep.2025.12.partial.json'
    ]

    all_sleep = []
    for filename in sleep_files:
        filepath = FITBIT_SLEEP_DIR / filename
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                all_sleep.extend(data)
        except FileNotFoundError:
            print(f"Warning: {filepath} not found, skipping...")

    if not all_sleep:
        return pd.DataFrame()

    sleep_df = pd.DataFrame(all_sleep)
    if 'dateOfSleep' in sleep_df.columns:
        sleep_df['date'] = pd.to_datetime(sleep_df['dateOfSleep']).dt.date

    return sleep_df

def match_tests_to_treatment(substances, tests, window_hours=24):
    """
    Match cognitive test results to treatment administrations.
    Tests are matched if they occur within window_hours after dosing.
    """
    matched_data = {
        'pvt': [],
        'dsst': [],
        'digit_span': [],
        'sss': []
    }

    for _, dose in substances.iterrows():
        dose_time = dose['datetime']
        treatment = dose['treatment']
        dose_date = dose['date']

        # Define time window (same day as dosing)
        window_start = dose_time
        window_end = dose_time + timedelta(hours=window_hours)

        for test_name, test_df in tests.items():
            # Find tests within the window
            matching_tests = test_df[
                (test_df['timestamp'] >= window_start) &
                (test_df['timestamp'] <= window_end)
            ].copy()

            matching_tests['treatment'] = treatment
            matching_tests['dose_date'] = dose_date
            matching_tests['dose_time'] = dose_time

            if len(matching_tests) > 0:
                matched_data[test_name].append(matching_tests)

    # Concatenate all matched tests
    for test_name in matched_data:
        if matched_data[test_name]:
            matched_data[test_name] = pd.concat(matched_data[test_name], ignore_index=True)
        else:
            matched_data[test_name] = pd.DataFrame()

    return matched_data

def calculate_pvt_metrics(pvt_df):
    """Calculate aggregate metrics for PVT data."""
    results = []

    for _, row in pvt_df.iterrows():
        if 'reaction_times_ms' in row and row['reaction_times_ms']:
            rt_list = row['reaction_times_ms']
            results.append({
                'timestamp': row['timestamp'],
                'treatment': row['treatment'],
                'dose_date': row['dose_date'],
                'mean_rt': np.mean(rt_list),
                'median_rt': np.median(rt_list),
                'slowest_10pct': np.percentile(rt_list, 90),
                'fastest_10pct': np.percentile(rt_list, 10),
                'false_starts': row.get('false_starts', 0)
            })

    return pd.DataFrame(results)

# TODO: Can these three be refactored into a single function?

def calculate_dsst_metrics(dsst_df):
    """Extract DSST metrics."""
    if dsst_df.empty:
        return pd.DataFrame()

    return dsst_df[['timestamp', 'treatment', 'dose_date',
                    'correct_count', 'total_attempted', 'accuracy']].copy()

def calculate_digit_span_metrics(ds_df):
    """Extract digit span metrics."""
    if ds_df.empty:
        return pd.DataFrame()

    return ds_df[['timestamp', 'treatment', 'dose_date',
                  'forward_span', 'backward_span', 'total_span']].copy()

def calculate_sss_metrics(sss_df):
    """Extract Stanford Sleepiness Scale ratings."""
    if sss_df.empty:
        return pd.DataFrame()

    return sss_df[['timestamp', 'treatment', 'dose_date', 'rating']].copy()

def run_ttests(orexin_data, placebo_data, metric_name):
    """Run two-sample t-test and return results."""
    if len(orexin_data) < 2 or len(placebo_data) < 2:
        return None

    # Remove NaN values
    orexin_clean = orexin_data[~np.isnan(orexin_data)]
    placebo_clean = placebo_data[~np.isnan(placebo_data)]

    if len(orexin_clean) < 2 or len(placebo_clean) < 2:
        return None

    # Run t-test
    t_stat, p_value = stats.ttest_ind(orexin_clean, placebo_clean)

    # Calculate effect size (Cohen's d)
    pooled_std = np.sqrt((np.var(orexin_clean) + np.var(placebo_clean)) / 2)
    cohens_d = (np.mean(orexin_clean) - np.mean(placebo_clean)) / pooled_std if pooled_std > 0 else 0

    return {
        'metric': metric_name,
        'orexin_mean': np.mean(orexin_clean),
        'orexin_std': np.std(orexin_clean),
        'orexin_n': len(orexin_clean),
        'placebo_mean': np.mean(placebo_clean),
        'placebo_std': np.std(placebo_clean),
        'placebo_n': len(placebo_clean),
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d
    }

def analyze_sleep_data(substances, sleep_df):
    """Analyze sleep data matched to treatment days."""
    if sleep_df.empty:
        return []

    results = []

    for _, dose in substances.iterrows():
        dose_date = dose['date']
        treatment = dose['treatment']

        # Find sleep data for the night AFTER dosing (recovery night)
        # Fitbit's dateOfSleep is the date you wake up
        # So dose on Sept 8 → look for dateOfSleep Sept 9 (sleep on night of Sept 8-9)
        from datetime import timedelta
        next_day = dose_date + timedelta(days=1)
        matching_sleep = sleep_df[sleep_df['date'] == next_day]

        if not matching_sleep.empty:
            sleep_record = matching_sleep.iloc[0]

            result = {
                'date': dose_date,
                'treatment': treatment,
            }

            # Extract relevant metrics
            if 'duration' in sleep_record:
                result['duration_ms'] = sleep_record['duration']
                result['duration_hours'] = sleep_record['duration'] / (1000 * 60 * 60)

            if 'minutesAsleep' in sleep_record:
                result['minutes_asleep'] = sleep_record['minutesAsleep']

            if 'efficiency' in sleep_record:
                result['efficiency'] = sleep_record['efficiency']

            # Sleep stages
            if 'levels' in sleep_record and isinstance(sleep_record['levels'], dict):
                summary = sleep_record['levels'].get('summary', {})
                for stage in ['deep', 'light', 'rem', 'wake']:
                    if stage in summary:
                        result[f'{stage}_minutes'] = summary[stage].get('minutes', 0)

            results.append(result)

    return pd.DataFrame(results)

def main():
    substances = load_substances()
    tests = load_cognitive_tests()
    sleep_df = load_sleep_data()

    # Match tests to treatments
    matched = match_tests_to_treatment(substances, tests)
    for test_name, test_df in matched.items():
        if not test_df.empty:
            orexin_count = len(test_df[test_df['treatment'] == 'Orexin'])
            placebo_count = len(test_df[test_df['treatment'] == 'Placebo'])

    pvt_metrics = calculate_pvt_metrics(matched['pvt'])
    dsst_metrics = calculate_dsst_metrics(matched['dsst'])
    digit_span_metrics = calculate_digit_span_metrics(matched['digit_span'])
    sss_metrics = calculate_sss_metrics(matched['sss'])
    sleep_metrics = analyze_sleep_data(substances, sleep_df)

    test_results = []

    if not pvt_metrics.empty:
        for metric in ['mean_rt', 'median_rt', 'slowest_10pct', 'false_starts']:
            orexin_vals = pvt_metrics[pvt_metrics['treatment'] == 'Orexin'][metric].values
            placebo_vals = pvt_metrics[pvt_metrics['treatment'] == 'Placebo'][metric].values
            result = run_ttests(orexin_vals, placebo_vals, f'PVT_{metric}')
            if result:
                test_results.append(result)

    if not dsst_metrics.empty:
        for metric in ['correct_count', 'accuracy']:
            orexin_vals = dsst_metrics[dsst_metrics['treatment'] == 'Orexin'][metric].values
            placebo_vals = dsst_metrics[dsst_metrics['treatment'] == 'Placebo'][metric].values
            result = run_ttests(orexin_vals, placebo_vals, f'DSST_{metric}')
            if result:
                test_results.append(result)

    if not digit_span_metrics.empty:
        for metric in ['forward_span', 'backward_span', 'total_span']:
            orexin_vals = digit_span_metrics[digit_span_metrics['treatment'] == 'Orexin'][metric].values
            placebo_vals = digit_span_metrics[digit_span_metrics['treatment'] == 'Placebo'][metric].values
            result = run_ttests(orexin_vals, placebo_vals, f'DigitSpan_{metric}')
            if result:
                test_results.append(result)

    if not sss_metrics.empty:
        orexin_vals = sss_metrics[sss_metrics['treatment'] == 'Orexin']['rating'].values
        placebo_vals = sss_metrics[sss_metrics['treatment'] == 'Placebo']['rating'].values
        result = run_ttests(orexin_vals, placebo_vals, 'SSS_rating')
        if result:
            test_results.append(result)

    if not sleep_metrics.empty:
        for metric in ['duration_hours', 'minutes_asleep', 'efficiency',
                      'deep_minutes', 'light_minutes', 'rem_minutes', 'wake_minutes']:
            if metric in sleep_metrics.columns:
                orexin_vals = sleep_metrics[sleep_metrics['treatment'] == 'Orexin'][metric].values
                placebo_vals = sleep_metrics[sleep_metrics['treatment'] == 'Placebo'][metric].values
                result = run_ttests(orexin_vals, placebo_vals, f'Sleep_{metric}')
                if result:
                    test_results.append(result)

    results_df = pd.DataFrame(test_results)

    if not results_df.empty:
        results_df.to_csv('analysis_results.csv', index=False)
    else:
        print("\nNo results to display - insufficient data for analysis")

if __name__ == '__main__':
    main()
