import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from tigramite import data_processing as pp
from tigramite import plotting as tp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.parcorr import ParCorr

# Read and process meditation data
async def load_meditation_data():
    meditation_data = pd.read_csv('../../data/meditations.csv')
    # Use ISO format for parsing timestamps
    meditation_data['meditation_start'] = pd.to_datetime(meditation_data['meditation_start'], format='ISO8601', utc=True)
    meditation_data['meditation_end'] = pd.to_datetime(meditation_data['meditation_end'], format='ISO8601', utc=True)

    # Create daily meditation features
    daily_med = meditation_data.groupby(meditation_data['meditation_start'].dt.round('2h')).agg({
        'meditation_duration': ['count', 'sum', 'mean'],
        'mindfulness_rating': 'mean',
        'concentration_rating': 'mean'
    }).reset_index()

    daily_med.columns = ['date', 'num_sessions', 'total_duration', 'avg_duration',
                        'mindfulness', 'concentration']
    daily_med['date'] = pd.to_datetime(daily_med['date'])
    return daily_med

# Read and process mood data
async def load_mood_data():
    mood_data = pd.read_csv('../../data/mood.csv')
    mood_data['date'] = pd.to_datetime(mood_data['date'])

    # Create daily mood averages
    daily_mood = mood_data.groupby(mood_data['date'].dt.round('2h')).agg({
        'happy': 'mean',
        'content': 'mean',
        'relaxed': 'mean',
        'horny': 'mean'
    }).reset_index()

    daily_mood['date'] = pd.to_datetime(daily_mood['date'], utc=True)
    return daily_mood

async def load_mental_data():
    mental_data = pd.read_csv('../../data/mental.csv')
    mental_data['datetime'] = pd.to_datetime(mental_data['datetime'], utc=True)

    # Create daily mental averages using datetime column
    daily_mental = mental_data.groupby(mental_data['datetime'].dt.round('2h')).agg({
        'productivity': 'mean',
        'creativity': 'mean',
        'sublen': 'mean'
    }).reset_index()

    # Rename the index column to 'date' to match other dataframes
    daily_mental = daily_mental.rename(columns={'index': 'date'})
    # Convert date to datetime
    daily_mental['date'] = pd.to_datetime(daily_mental.iloc[:, 0])

    return daily_mental

async def prepare_masturbation_data():
    # Read masturbation data
    df = pd.read_csv('../../data/masturbations.csv')

    # Convert datetime to UTC
    df['datetime'] = pd.to_datetime(df['datetime'], format='ISO8601', utc=True)

    # Sort by datetime to ensure correct calculations
    df = df.sort_values('datetime')

    # Create hourly time index from min to max date
    time_index = pd.date_range(start=df['datetime'].min(),
                              end=df['datetime'].max(),
                              freq='2h')

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
    enjoyment_hourly = enjoyment_series.resample('2h').mean()

    # Interpolate enjoyment between events
    enjoyment_hourly = enjoyment_hourly.interpolate(method='linear', limit_direction='both')

    return abstinence_duration, enjoyment_hourly

async def prepare_substances_data():
    # Read data
    df = pd.read_csv('../../data/substances.csv')
    df['datetime'] = pd.to_datetime(df['datetime'], format='ISO8601', utc=True)

    # Get unique substances
    substances = df['substance'].unique()

    # Create time index matching other data
    time_index = pd.date_range(start=df['datetime'].min(),
                              end=df['datetime'].max(),
                              freq='2h')

    # Initialize dict to store time series for each substance
    substance_series = {}

    for substance in substances:
        # Filter for this substance
        substance_df = df[df['substance'] == substance]

        # Create indicator series (1 when substance was taken)
        events = pd.Series(1.0, index=substance_df['datetime'])
        resampled = events.resample('2h').sum().reindex(time_index).fillna(0)

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

async def load_light_data():
    # Read light data
    light_df = pd.read_csv('../../data/light.csv')

    # Convert timestamps to datetime
    light_df['start'] = pd.to_datetime(light_df['start'], format='ISO8601', utc=True)
    light_df['stop'] = pd.to_datetime(light_df['stop'], format='ISO8601', utc=True)

    # Create time series with 2h frequency from min to max date
    time_index = pd.date_range(start=light_df['start'].min(),
                              end=light_df['stop'].max(),
                              freq='2h')

    # Initialize series for light exposure
    light_exposure = pd.Series(index=time_index, dtype=float)

    # Calculate average lumens for each 2h period
    for t in time_index:
        period_start = t
        period_end = t + pd.Timedelta(hours=2)

        # Find light sessions that overlap with this period
        relevant_sessions = light_df[
            ((light_df['start'] <= period_end) & (light_df['stop'] >= period_start))
        ]

        if len(relevant_sessions) > 0:
            # For each overlapping session, calculate the overlap duration and weighted lumens
            total_lumens = 0
            total_minutes = 0

            for _, session in relevant_sessions.iterrows():
                overlap_start = max(period_start, session['start'])
                overlap_end = min(period_end, session['stop'])
                overlap_minutes = (overlap_end - overlap_start).total_seconds() / 60

                total_lumens += session['lumens'] * overlap_minutes
                total_minutes += overlap_minutes

            # Calculate average lumens for this period
            if total_minutes > 0:
                light_exposure[t] = total_lumens / total_minutes
            else:
                light_exposure[t] = 0
        else:
            light_exposure[t] = 0

    # Add some derived metrics
    light_binary = (light_exposure > 0).astype(int)

    return pd.DataFrame({
        'light_lumens': light_exposure,
        'light_binary': light_binary,
        'light_log': light_log
    }, index=time_index)

async def prepare_tigramite_data():
    # Load all data
    daily_med = await load_meditation_data()
    daily_mood = await load_mood_data()
    daily_mental = await load_mental_data()
    abstinence_duration, enjoyment_hourly = await prepare_masturbation_data()
    substance_series = await prepare_substances_data()

    # Merge base data
    merged_data = pd.merge(daily_med, daily_mood, on='date', how='outer')
    merged_data = pd.merge(merged_data, daily_mental, on='date', how='outer')
    merged_data = merged_data.sort_values('date')

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

    # Log transform abstinence hours and substance hours
    merged_data['abstinence_hours'] = np.log1p(merged_data['abstinence_hours'])
    for col in merged_data.columns:
        if col.endswith('_hours'):
            merged_data[col] = np.log1p(merged_data[col])

    # Get list of all variables for analysis
    base_variables = [
        'total_duration', 'mindfulness', 'concentration', 'num_sessions',
        'happy', 'content', 'relaxed', 'horny',
        'productivity', 'creativity', 'sublen',
        'abstinence_hours', 'masturbation_enjoyment'
    ]
    substance_variables = [col for col in merged_data.columns
                         if col not in base_variables and col != 'date' and col != 'datetime']
    variables = base_variables + substance_variables

    merged_data = merged_data.reset_index(drop=True)
    merged_data.index = range(len(merged_data))

    # Create Tigramite dataframe
    data = merged_data[variables].values
    data = (data - data.mean(axis=0)) / data.std(axis=0)
    dataframe = pp.DataFrame(data,
                           var_names=variables,
                           datatime=merged_data.date)

    return dataframe, merged_data

async def run_causal_analysis():
    dataframe, merged_data = await prepare_tigramite_data()

    parcorr = ParCorr(significance='analytic')
    pcmci = PCMCI(dataframe=dataframe, cond_ind_test=parcorr, verbosity=1)

    # Run PCMCI+ algorithm
    results = pcmci.run_pcmciplus(tau_min=0, tau_max=4, pc_alpha=0.05)

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
#if __name__ == "__main__":
#    import asyncio
#    results, dataframe = asyncio.run(run_causal_analysis())
