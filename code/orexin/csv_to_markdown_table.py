#!/usr/bin/env python3
"""
Convert analysis_results.csv to formatted markdown table.
"""

import pandas as pd
import numpy as np

# Variable name mapping with Wikipedia links
VARIABLE_NAMES = {
    'PVT_mean_rt': ('**[PVT](https://en.wikipedia.org/wiki/Psychomotor_vigilance_task) Mean RT (ms)**', 1),
    'PVT_median_rt': ('**[PVT](https://en.wikipedia.org/wiki/Psychomotor_vigilance_task) Median RT (ms)**', 1),
    'PVT_slowest_10pct': ('**[PVT](https://en.wikipedia.org/wiki/Psychomotor_vigilance_task) Slowest 10% (ms)**', 1),
    'PVT_false_starts': ('**[PVT](https://en.wikipedia.org/wiki/Psychomotor_vigilance_task) False Starts**', 2),
    'DSST_correct_count': ('**[DSST](https://en.wikipedia.org/wiki/Wechsler_Adult_Intelligence_Scale#Coding_and_Symbol_Search) Correct**', 1),
    'DSST_accuracy': ('**[DSST](https://en.wikipedia.org/wiki/Wechsler_Adult_Intelligence_Scale#Coding_and_Symbol_Search) Accuracy**', 3),
    'DigitSpan_forward_span': ('**[Digit Span](https://en.wikipedia.org/wiki/Memory_span#Digit-span) Forward**', 2),
    'DigitSpan_backward_span': ('**[Digit Span](https://en.wikipedia.org/wiki/Memory_span#Digit-span) Backward**', 2),
    'DigitSpan_total_span': ('**[Digit Span](https://en.wikipedia.org/wiki/Memory_span#Digit-span) Total**', 1),
    'SSS_rating': ('**[SSS](https://en.wikipedia.org/wiki/Stanford_Sleepiness_Scale) Rating**', 2),
    'Sleep_duration_hours': ('**Sleep Duration (hrs)**', 2),
    'Sleep_minutes_asleep': ('**Sleep Time Asleep (min)**', 0),
    'Sleep_efficiency': ('**Sleep Efficiency (%)**', 1),
    'Sleep_deep_minutes': ('**Sleep Deep (min)**', 1),
    'Sleep_light_minutes': ('**Sleep Light (min)**', 0),
    'Sleep_rem_minutes': ('**Sleep [REM](https://en.wikipedia.org/wiki/Rapid_eye_movement_sleep) (min)**', 1),
    'Sleep_wake_minutes': ('**Sleep Wake (min)**', 1),
}

def format_value(value, decimals):
    """Format a value to the specified number of decimal places."""
    if pd.isna(value):
        return 'N/A'
    if decimals == 0:
        return f'{value:.0f}'
    return f'{value:.{decimals}f}'

def format_difference(diff, decimals):
    """Format difference with + or - prefix."""
    if pd.isna(diff):
        return 'N/A'
    sign = '+' if diff >= 0 else ''
    if decimals == 0:
        return f'{sign}{diff:.0f}'
    return f'{sign}{diff:.{decimals}f}'

def main():
    # Read the CSV
    df = pd.read_csv('analysis_results.csv')

    # Build markdown table
    header = '| Variable | [Cohen\'s d](https://en.wikipedia.org/wiki/Effect_size#Cohen\'s_d) | p-value | Orexin | Placebo | Difference |'
    separator = '|----------|-----------|---------|---------|---------|------------|'

    rows = [header, separator]

    for _, row in df.iterrows():
        metric = row['metric']

        # Get formatted name and decimal places
        if metric not in VARIABLE_NAMES:
            continue

        var_name, decimals = VARIABLE_NAMES[metric]

        # Calculate difference
        diff = row['orexin_mean'] - row['placebo_mean']

        # Format orexin and placebo columns
        orexin_str = f"{format_value(row['orexin_mean'], decimals)} ± {format_value(row['orexin_std'], decimals)} (n={int(row['orexin_n'])})"
        placebo_str = f"{format_value(row['placebo_mean'], decimals)} ± {format_value(row['placebo_std'], decimals)} (n={int(row['placebo_n'])})"

        # Build row
        table_row = (
            f"| {var_name} | "
            f"{format_value(row['cohens_d'], 3)} | "
            f"{format_value(row['p_value'], 3)} | "
            f"{orexin_str} | "
            f"{placebo_str} | "
            f"{format_difference(diff, decimals)} |"
        )

        rows.append(table_row)

    # Write to file
    output = '\n'.join(rows) + '\n'
    with open('analysis_results.md', 'w') as f:
        f.write(output)

if __name__ == '__main__':
    main()
