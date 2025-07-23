import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from tigramite import data_processing as pp
from tigramite import plotting as tp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.parcorr import ParCorr

# Global configuration
INTERVAL = '1h'

# Read raw meditation data
async def load_meditation_data():
    meditation_data = pd.read_csv('../../data/meditations.csv')
    # Use ISO format for parsing timestamps
    meditation_data['meditation_start'] = pd.to_datetime(meditation_data['meditation_start'], format='ISO8601', utc=True)
    meditation_data['meditation_end'] = pd.to_datetime(meditation_data['meditation_end'], format='ISO8601', utc=True)
    return meditation_data

# Process meditation data into time series
async def process_meditation_data(meditation_data, interval=INTERVAL):
    # Create time index for the interval
    start_time = meditation_data['meditation_start'].min().floor(interval)
    end_time = meditation_data['meditation_end'].max().ceil(interval)
    time_index = pd.date_range(start=start_time, end=end_time, freq=interval)

    # Calculate interval duration in minutes
    interval_duration = pd.Timedelta(interval).total_seconds() / 60

    # Initialize result dataframe
    result = pd.DataFrame(index=time_index)
    result['date'] = result.index
    result['meditation_proportion'] = 0.0
    result['num_sessions'] = 0
    result['mindfulness'] = np.nan
    result['concentration'] = np.nan

    # For each time interval, calculate all metrics
    for i in range(len(time_index) - 1):
        interval_start = time_index[i]
        interval_end = time_index[i + 1]

        # Find sessions that overlap with this interval (for proportion)
        overlapping = meditation_data[
            (meditation_data['meditation_start'] < interval_end) &
            (meditation_data['meditation_end'] > interval_start)
        ]

        # Find sessions that START in this interval (for ratings)
        starting_in_interval = meditation_data[
            (meditation_data['meditation_start'] >= interval_start) &
            (meditation_data['meditation_start'] < interval_end)
        ]

        # Calculate meditation proportion
        if len(overlapping) > 0:
            total_meditation_minutes = 0
            for _, session in overlapping.iterrows():
                overlap_start = max(session['meditation_start'], interval_start)
                overlap_end = min(session['meditation_end'], interval_end)
                overlap_duration = (overlap_end - overlap_start).total_seconds() / 60
                if overlap_duration > 0:
                    total_meditation_minutes += overlap_duration

            result.loc[interval_start, 'meditation_proportion'] = total_meditation_minutes / interval_duration
            result.loc[interval_start, 'num_sessions'] = len(overlapping)

        # Calculate average ratings for sessions starting in this interval
        if len(starting_in_interval) > 0:
            valid_mindfulness = starting_in_interval[
                pd.notna(starting_in_interval['mindfulness_rating']) &
                (starting_in_interval['mindfulness_rating'] > 0)
            ]
            valid_concentration = starting_in_interval[
                pd.notna(starting_in_interval['concentration_rating']) &
                (starting_in_interval['concentration_rating'] > 0)
            ]

            if len(valid_mindfulness) > 0:
                result.loc[interval_start, 'mindfulness'] = valid_mindfulness['mindfulness_rating'].mean()
            if len(valid_concentration) > 0:
                result.loc[interval_start, 'concentration'] = valid_concentration['concentration_rating'].mean()

    # Interpolate ratings between non-null periods
    result['mindfulness'] = result['mindfulness'].interpolate(method='linear')
    result['concentration'] = result['concentration'].interpolate(method='linear')

    return result.reset_index(drop=True)

# Read raw mood data
async def load_mood_data():
    mood_data = pd.read_csv('../../data/mood.csv')
    mood_data['date'] = pd.to_datetime(mood_data['date'])
    return mood_data

# Process mood data into time series
async def process_mood_data(mood_data, interval='2h'):
    # Create time series for each mood dimension
    mood_data = mood_data.set_index('date')

    # Resample to the desired interval and interpolate
    happy_resampled = mood_data['happy'].resample(interval).mean()
    content_resampled = mood_data['content'].resample(interval).mean()
    relaxed_resampled = mood_data['relaxed'].resample(interval).mean()
    horny_resampled = mood_data['horny'].resample(interval).mean()

    # Interpolate missing values
    happy_interpolated = happy_resampled.interpolate(method='linear')
    content_interpolated = content_resampled.interpolate(method='linear')
    relaxed_interpolated = relaxed_resampled.interpolate(method='linear')
    horny_interpolated = horny_resampled.interpolate(method='linear')

    # Create result dataframe
    result = pd.DataFrame({
        'date': happy_interpolated.index,
        'happy': happy_interpolated.values,
        'content': content_interpolated.values,
        'relaxed': relaxed_interpolated.values,
        'horny': horny_interpolated.values
    })

    result['date'] = pd.to_datetime(result['date'], utc=True)
    return result.reset_index(drop=True)

# Read raw mental data
async def load_mental_data():
    mental_data = pd.read_csv('../../data/mental.csv')
    mental_data['datetime'] = pd.to_datetime(mental_data['datetime'], utc=True)
    return mental_data

# Process mental data into time series
async def process_mental_data(mental_data, interval='2h'):
    # Create daily mental averages using datetime column
    daily_mental = mental_data.groupby(mental_data['datetime'].dt.round(interval)).agg({
        'productivity': 'mean',
        'creativity': 'mean',
        'sublen': 'mean'
    }).reset_index()

    # Rename the index column to 'date' to match other dataframes
    daily_mental = daily_mental.rename(columns={'index': 'date'})
    # Convert date to datetime
    daily_mental['date'] = pd.to_datetime(daily_mental.iloc[:, 0])

    return daily_mental

# Read raw masturbation data
async def load_masturbation_data():
    df = pd.read_csv('../../data/masturbations.csv')
    # Convert datetime to UTC
    df['datetime'] = pd.to_datetime(df['datetime'], format='ISO8601', utc=True)
    # Sort by datetime to ensure correct calculations
    df = df.sort_values('datetime')
    return df

# Process masturbation data into time series
async def process_masturbation_data(df, interval='2h'):
    # Create hourly time index from min to max date
    time_index = pd.date_range(start=df['datetime'].min(),
                              end=df['datetime'].max(),
                              freq=interval)

    # Initialize series for hours since last event
    abstinence_duration = pd.Series(index=time_index, dtype=float)

    # For each hour, calculate hours since the most recent event before that time
    for t in time_index:
        last_event = df[df['datetime'] < t]['datetime'].max()
        if pd.isnull(last_event):
            # If no previous event, set to NaN
            abstinence_duration[t] = np.nan
        else:
            # Calculate hours since last event
            duration = (t - last_event).total_seconds() / 3600  # Convert to hours
            abstinence_duration[t] = duration

    # Handle enjoyment data
    enjoyment_series = pd.Series(df['enjoyment'].values, index=df['datetime'])
    enjoyment_hourly = enjoyment_series.resample(interval).mean()

    # Interpolate enjoyment between events
    enjoyment_hourly = enjoyment_hourly.interpolate(method='linear', limit_direction='both')

    return abstinence_duration, enjoyment_hourly

# Read raw substances data
async def load_substances_data():
    df = pd.read_csv('../../data/substances.csv')
    df['datetime'] = pd.to_datetime(df['datetime'], format='ISO8601', utc=True)
    return df

# Process substances data into time series
async def process_substances_data(df, interval='2h'):
    # Get unique substances and filter by minimum datapoints
    substance_counts = df['substance'].value_counts()
    substances = substance_counts[substance_counts >= 10].index.tolist()

    # Create time index matching other data
    time_index = pd.date_range(start=df['datetime'].min().floor(interval),
                              end=df['datetime'].max().ceil(interval),
                              freq=interval)

    # Initialize dict to store time series for each substance
    substance_series = {}

    for substance in substances:
        # Filter for this substance
        substance_df = df[df['substance'] == substance]

        # Create indicator series (1 when substance was taken)
        events = pd.Series(1.0, index=substance_df['datetime'])
        resampled = events.resample(interval).sum().reindex(time_index).fillna(0)

        # Calculate hours since last intake
        hours_since = pd.Series(index=time_index, dtype=float)
        for t in time_index:
            last_intake = substance_df[substance_df['datetime'] < t]['datetime'].max()
            if pd.isnull(last_intake):
                hours_since[t] = np.nan
            else:
                hours_since[t] = (t - last_intake).total_seconds() / 3600

        substance_series[f"{substance}_hours"] = hours_since

    return substance_series

# Read raw Anki data
async def load_anki_data():
    anki_data = pd.read_csv('../../data/anki_reviews.csv')
    # Convert timestamp from milliseconds to datetime
    anki_data['datetime'] = pd.to_datetime(anki_data['id'], unit='ms', utc=True)
    return anki_data

# Process Anki data into time series
async def process_anki_data(anki_data, interval='2h'):
    # Create time index from min to max date
    start_time = anki_data['datetime'].min().floor(interval)
    end_time = anki_data['datetime'].max().ceil(interval)
    time_index = pd.date_range(start=start_time, end=end_time, freq=interval)

    # Initialize result series with zeros (no reviews = 0)
    reviews_count = pd.Series(index=time_index, data=0, dtype=int)
    avg_review_time = pd.Series(index=time_index, data=0.0, dtype=float)
    success_rate = pd.Series(index=time_index, data=0.0, dtype=float)
    total_anki_time = pd.Series(index=time_index, data=0.0, dtype=float)

    # Group by interval and calculate metrics
    anki_data['interval'] = anki_data['datetime'].dt.floor(interval)
    grouped = anki_data.groupby('interval')

    for interval_time, group in grouped:
        if interval_time in time_index:
            # Number of reviews
            reviews_count[interval_time] = len(group)

            # Average review time in seconds
            avg_review_time[interval_time] = group['time'].mean() / 1000.0

            # Success rate (ease >= 2, i.e., not "Again")
            success_rate[interval_time] = (group['ease'] >= 2).mean()

            # Total time spent on Anki in minutes
            total_anki_time[interval_time] = group['time'].sum() / (1000.0 * 60.0)

    # Create result dataframe
    result = pd.DataFrame({
        'date': time_index,
        'reviews_count': reviews_count.values,
        'avg_review_time': avg_review_time.values,
        'success_rate': success_rate.values,
        'total_anki_time': total_anki_time.values
    })

    result['date'] = pd.to_datetime(result['date'], utc=True)
    return result.reset_index(drop=True)

# Read raw weight data
async def load_weight_data():
    weight_data = pd.read_csv('../../data/weights.csv')
    weight_data['datetime'] = pd.to_datetime(weight_data['datetime'], utc=True)
    return weight_data

# Process weight data into time series
async def process_weight_data(weight_data, interval='2h'):
    # Create time series from weight measurements
    weight_data = weight_data.set_index('datetime')
    weight_series = weight_data['weight']

    # Resample to the desired interval and interpolate
    weight_resampled = weight_series.resample(interval).mean()

    # Interpolate missing values
    weight_interpolated = weight_resampled.interpolate(method='linear')

    # Create result dataframe
    result = pd.DataFrame({
        'date': weight_interpolated.index,
        'weight': weight_interpolated.values
    })

    result['date'] = pd.to_datetime(result['date'], utc=True)
    return result.reset_index(drop=True)

# Prepare data for tigramite analysis
async def prepare_tigramite_data(interval='2h', start_date=None):
    # Load all raw data
    meditation_data = await load_meditation_data()
    mood_data = await load_mood_data()
    mental_data = await load_mental_data()
    masturbation_data = await load_masturbation_data()
    substances_data = await load_substances_data()
    weight_data = await load_weight_data()
    anki_data = await load_anki_data()

    # Process all data with the same interval
    daily_med = await process_meditation_data(meditation_data, interval)
    daily_mood = await process_mood_data(mood_data, interval)
    daily_mental = await process_mental_data(mental_data, interval)
    abstinence_duration, enjoyment_hourly = await process_masturbation_data(masturbation_data, interval)
    substance_series = await process_substances_data(substances_data, interval)
    daily_weight = await process_weight_data(weight_data, interval)
    daily_anki = await process_anki_data(anki_data, interval)

    # Merge base data
    merged_data = pd.merge(daily_med, daily_mood, on='date', how='outer')
    merged_data = pd.merge(merged_data, daily_mental, on='date', how='outer')
    merged_data = pd.merge(merged_data, daily_weight, on='date', how='outer')
    merged_data = pd.merge(merged_data, daily_anki, on='date', how='outer')

    # Add masturbation data
    abstinence_duration.index.name = 'date'
    enjoyment_hourly.index.name = 'date'
    merged_data = pd.merge(merged_data,
                          abstinence_duration.to_frame('abstinence_hours'),
                          left_on='date',
                          right_index=True,
                          how='outer')
    merged_data = pd.merge(merged_data,
                          enjoyment_hourly.to_frame('masturbation_enjoyment'),
                          left_on='date',
                          right_index=True,
                          how='outer')

    # Add substance data
    for name, series in substance_series.items():
        series.index.name = 'date'
        merged_data = pd.merge(merged_data,
                             series.to_frame(name),
                             left_on='date',
                             right_index=True,
                             how='outer')

    # Sort and interpolate
    merged_data = merged_data.sort_values('date')
    merged_data = merged_data.interpolate(method='linear', limit_direction='both')

    # Filter data from start_date if provided
    if start_date is not None:
        start_date = pd.to_datetime(start_date, utc=True)
        original_len = len(merged_data)
        merged_data = merged_data[merged_data['date'] >= start_date]
        filtered_len = len(merged_data)
        print(f"Filtered data from {start_date.strftime('%Y-%m-%d')}: {original_len} -> {filtered_len} rows ({filtered_len/original_len:.1%} kept)")

    # Log transform abstinence hours and substance hours
    # TODO: belongs into the respective data producing functions.
    merged_data['abstinence_hours'] = np.log1p(merged_data['abstinence_hours'])
    for col in merged_data.columns:
        if col.endswith('_hours'):
            merged_data[col] = np.log1p(merged_data[col])

    # Get list of all variables for analysis
    base_variables = [
        'meditation_proportion', 'mindfulness', 'concentration', 'num_sessions',
        'happy', 'content', 'relaxed', 'horny',
        'productivity', 'creativity', 'sublen',
        'abstinence_hours', 'masturbation_enjoyment',
        'weight',
        'reviews_count', 'avg_review_time', 'success_rate', 'total_anki_time'
    ]
    substance_variables = [col for col in merged_data.columns
                         if col not in base_variables and col != 'date' and col != 'datetime']
    variables = base_variables + substance_variables

    merged_data = merged_data.reset_index(drop=True)

    # Create Tigramite dataframe
    data = merged_data[variables].values

    # Handle standardization with proper NaN and zero variance handling
    means = np.nanmean(data, axis=0)
    stds = np.nanstd(data, axis=0)

    # Replace zero standard deviations with 1 to avoid division by zero
    stds[stds == 0] = 1

    # Standardize the data
    data = (data - means) / stds

    # Fill any remaining NaNs with 0 (standardized mean)
    data = np.nan_to_num(data, nan=0.0)

    dataframe = pp.DataFrame(data,
                           var_names=variables,
                           datatime=merged_data.date)

    link_assumptions=None
    #link_assumptions=generate_link_assumptions(variables)

    return dataframe, merged_data, link_assumptions

def generate_link_assumptions(variables):
    # Exclude specific variable links
    link_assumptions = {}

    # Get substance variable indices
    substance_indices = [i for i, var in enumerate(variables) if any(var.endswith(suffix) for suffix in ['_hours'])]

    # Get indices for specific variables to exclude
    num_sessions_idx = variables.index('num_sessions') if 'num_sessions' in variables else None
    meditation_proportion_idx = variables.index('meditation_proportion') if 'meditation_proportion' in variables else None
    mindfulness_idx = variables.index('mindfulness') if 'mindfulness' in variables else None
    concentration_idx = variables.index('concentration') if 'concentration' in variables else None
    happy_idx = variables.index('happy') if 'happy' in variables else None
    content_idx = variables.index('content') if 'content' in variables else None
    relaxed_idx = variables.index('relaxed') if 'relaxed' in variables else None
    horny_idx = variables.index('horny') if 'horny' in variables else None

    # Initialize empty dictionaries for all variables
    for var_idx in range(len(variables)):
        link_assumptions[var_idx] = {}

    print(f"Excluding all links between {len(substance_indices)} substance variables")
    print("Excluding definitional links: num_sessions ↔ meditation_proportion")

    # Add all potential links EXCEPT excluded ones
    for ii in range(len(variables)):
        for jj in range(len(variables)):
            if ii != jj:  # Don't add self-loops
                for tau in range(1, 5):  # tau_min=1, tau_max=4
                    # Skip ALL substance-to-substance links
                    if ii in substance_indices and jj in substance_indices:
                        continue

                    # Skip definitional links: num_sessions ↔ meditation_proportion
                    if (ii == num_sessions_idx and jj == meditation_proportion_idx) or \
                       (ii == meditation_proportion_idx and jj == num_sessions_idx):
                        continue

                    link_assumptions[jj][(ii, -tau)] = 'o-o'  # Use undirected link

    return link_assumptions

async def run_causal_analysis():
    dataframe, merged_data, link_assumptions = await prepare_tigramite_data(interval=INTERVAL, start_date='2022-10-01')
    print(merged_data.describe())

    parcorr = ParCorr(significance='analytic')
    pcmci = PCMCI(dataframe=dataframe, cond_ind_test=parcorr, verbosity=1)

    # Run PCMCI+ algorithm with single link exclusion test
    if link_assumptions is not None:
        results = pcmci.run_pcmciplus(tau_min=1, tau_max=24, pc_alpha=0.05, link_assumptions=link_assumptions)
    else:
        results = pcmci.run_pcmciplus(tau_min=1, tau_max=24, pc_alpha=0.05)

    # Print significant links
    print("\nSignificant causal links at alpha = 0.05:")
    pcmci.print_significant_links(
        p_matrix=results['p_matrix'],
        val_matrix=results['val_matrix'],
        alpha_level=0.05
    )

    # Calculate positions for all variables including substances
    n_vars = len(dataframe.var_names)
    radius = 0.8
    angles = np.linspace(0, 2*np.pi, n_vars, endpoint=False)

    node_pos = {
        'x': list(radius * np.cos(angles)),
        'y': list(radius * np.sin(angles))
    }

    # Plot
    tp.plot_graph(
        val_matrix=results['val_matrix'],
        graph=results['graph'],
        var_names=dataframe.var_names,
        link_colorbar_label='MCI',
        node_colorbar_label='Auto-MCI',
        node_pos=node_pos,
        figsize=(15, 15),
        node_size=0.15,
        arrow_linewidth=3.0
    )

    plt.savefig('graph.png', dpi=300, bbox_inches='tight')
    return results, dataframe

# Execute analysis
if __name__ == "__main__":
    import asyncio
    results, dataframe = asyncio.run(run_causal_analysis())
