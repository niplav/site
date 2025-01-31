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
    daily_med = meditation_data.groupby(meditation_data['meditation_start'].dt.round('12h')).agg({
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
    daily_mood = mood_data.groupby(mood_data['date'].dt.round('12h')).agg({
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
    daily_mental = mental_data.groupby(mental_data['datetime'].dt.round('12h')).agg({
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
                              freq='12h')

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
    enjoyment_hourly = enjoyment_series.resample('12h').mean()

    # Interpolate enjoyment between events
    enjoyment_hourly = enjoyment_hourly.interpolate(method='linear', limit_direction='both')

    return abstinence_duration, enjoyment_hourly

async def prepare_substances_data():
    # Read data
    df = pd.read_csv('../../data/substances.csv')
    df['datetime'] = pd.to_datetime(df['datetime'], format='ISO8601')

    # Get unique substances
    substances = df['substance'].unique()

    # Create time index matching other data
    time_index = pd.date_range(start=df['datetime'].min(),
                              end=df['datetime'].max(),
                              freq='12h')

    # Initialize dict to store time series for each substance
    substance_series = {}

    for substance in substances:
        # Filter for this substance
        substance_df = df[df['substance'] == substance]

        # Create indicator series (1 when substance was taken)
        events = pd.Series(1.0, index=substance_df['datetime'])
        resampled = events.resample('12h').sum().reindex(time_index).fillna(0)

        # Calculate hours since last intake
        hours_since = pd.Series(index=time_index, dtype=float)
        for t in time_index:
            last_intake = substance_df[substance_df['datetime'] < t]['datetime'].max()
            if pd.isnull(last_intake):
                hours_since[t] = np.nan
            else:
                hours_since[t] = (t - last_intake).total_seconds() / 3600

        substance_series[f"{substance}_taken"] = resampled
        substance_series[f"{substance}_hours"] = hours_since

    return substance_series

async def prepare_tigramite_data():
    # Load all data
    daily_med = await load_meditation_data()
    daily_mood = await load_mood_data()
    daily_mental = await load_mental_data()
    abstinence_duration, enjoyment_hourly = await prepare_masturbation_data()

    # Merge meditation, mood, and mental data
    merged_data = pd.merge(daily_med, daily_mood, on='date', how='outer')
    merged_data = pd.merge(merged_data, daily_mental, on='date', how='outer')
    merged_data = merged_data.sort_values('date')

    # Add masturbation data
    # First convert the index of masturbation data to match the date column
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

    # Sort by date
    merged_data = merged_data.sort_values('date')

    # Use linear interpolation for all variables
    merged_data = merged_data.interpolate(method='linear', limit_direction='both')

    # Log transform abstinence hours to handle large values and make distribution more normal
    merged_data['abstinence_hours'] = np.log1p(merged_data['abstinence_hours'])

    # Select variables for analysis
    variables = [
        'total_duration', 'mindfulness', 'concentration', 'num_sessions',
        'happy', 'content', 'relaxed', 'horny',
        'productivity', 'creativity', 'sublen',
        'abstinence_hours', 'masturbation_enjoyment'
    ]

    # Create Tigramite dataframe
    data = merged_data[variables].values

    # Standardize all variables
    data = (data - data.mean(axis=0)) / data.std(axis=0)

    dataframe = pp.DataFrame(data,
                           var_names=variables,
                           datatime=merged_data.date)

    return dataframe, merged_data

async def run_causal_analysis():
    dataframe, merged_data = await prepare_tigramite_data()

    # Initialize PCMCI
    parcorr = ParCorr(significance='analytic')
    pcmci = PCMCI(
        dataframe=dataframe,
        cond_ind_test=parcorr,
        verbosity=1
    )

    # Run PCMCI+ algorithm
    # Increased tau_max to 4 to capture longer-term effects
    results = pcmci.run_pcmciplus(tau_min=0, tau_max=4, pc_alpha=0.05)

    # Print significant causal links
    print("\nSignificant causal links at alpha = 0.05:")
    pcmci.print_significant_links(
        p_matrix=results['p_matrix'],
        val_matrix=results['val_matrix'],
        alpha_level=0.05
    )

    # Define node positions for better visualization
    node_pos = {
        'x': [
            0.8,    # total_duration
            0.3,    # mindfulness
            -0.3,   # concentration
            -0.8,   # num_sessions
            0.8,    # happy
            0.3,    # content
            -0.3,   # relaxed
            -0.8,   # horny
            0.8,    # productivity
            0.3,    # creativity
            -0.3,   # sublen
            -0.8,   # abstinence_hours
            -0.8     # masturbation_enjoyment
        ],
        'y': [
            0.8,
            0.5,
            0.5,
            0.8,
            0.2,
            -0.1,
            -0.1,
            0.2,
            -0.6,
            -0.8,
            -0.8,
            -0.4,
            -0.8
        ]
    }

    # Plot the graph
    tp.plot_graph(
        val_matrix=results['val_matrix'],
        graph=results['graph'],
        var_names=dataframe.var_names,
        link_colorbar_label='MCI',
        node_colorbar_label='Auto-MCI',
        node_pos=node_pos,
        figsize=(12, 8),
        node_size=0.2,
        arrow_linewidth=6.0
    )

    plt.savefig('graph.png', dpi=300, bbox_inches='tight')

    return results, dataframe

# Execute analysis
if __name__ == "__main__":
    import asyncio
    results, dataframe = asyncio.run(run_causal_analysis())
