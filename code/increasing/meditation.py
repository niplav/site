import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from load import get_sleep, get_meditations

import numpy as np
import pandas as pd
import scipy.stats as sps
import matplotlib.pyplot as plt

backwards_horizon='4d'
relevant_sleep_cols=['duration', 'minutes_asleep', 'minutes_to_sleep', 'minutes_after_wakeup', 'time_in_bed', 'deep_count', 'deep_minutes', 'light_count', 'light_minutes', 'rem_count', 'rem_minutes', 'wake_count', 'wake_minutes']

sleep=get_sleep()
first_sleep=sleep['date'].min()
last_sleep=sleep['date'].max()

meditations=get_meditations()
meditations.sort_values(by=['meditation_start'], inplace=True)
meditations=meditations.loc[meditations['meditation_start']>(first_sleep-pd.Timedelta(backwards_horizon))]
sleep.sort_values(by=['start_time'], inplace=True)

checkpoints=pd.DataFrame()
checkpoints['checkpoint']=pd.date_range(start=first_sleep, end=last_sleep, freq='1d')+pd.Timedelta('18h')

aggregated=pd.merge_asof(sleep, checkpoints, left_on='start_time', right_on='checkpoint', direction='backward')
aggregated=aggregated[relevant_sleep_cols+['checkpoint']].groupby('checkpoint').sum()
aggregated.reset_index(inplace=True)

daily_meditation = pd.DataFrame()
daily_meditation['checkpoint'] = pd.date_range(start=first_sleep - pd.Timedelta(backwards_horizon), end=last_sleep, freq='1d') + pd.Timedelta('18h')

# Initialize with zero meditation time
daily_meditation['meditation_duration'] = 0

# For each meditation session, calculate which checkpoint it belongs to
for _, meditation in meditations.iterrows():
	# Find checkpoints that this meditation might affect (within backwards_horizon)
	relevant_checkpoints = daily_meditation.loc[
		(daily_meditation['checkpoint'] - meditation['meditation_end'] < pd.Timedelta(backwards_horizon)) &
		(daily_meditation['checkpoint'] - meditation['meditation_end'] > pd.Timedelta('0d'))
	]

	# Add this meditation's duration to those checkpoints
	if not relevant_checkpoints.empty:
		daily_meditation.loc[relevant_checkpoints.index, 'meditation_duration'] += meditation['meditation_duration']

# Per-day meditation (1d window) — used to identify retreat days
daily_meditation_same_day = pd.DataFrame()
daily_meditation_same_day['checkpoint'] = pd.date_range(start=first_sleep - pd.Timedelta(backwards_horizon), end=last_sleep, freq='1d') + pd.Timedelta('18h')
daily_meditation_same_day['meditation_same_day'] = 0

for _, meditation in meditations.iterrows():
	relevant_checkpoints = daily_meditation_same_day.loc[
		(daily_meditation_same_day['checkpoint'] - meditation['meditation_end'] < pd.Timedelta('1d')) &
		(daily_meditation_same_day['checkpoint'] - meditation['meditation_end'] > pd.Timedelta('0d'))
	]
	if not relevant_checkpoints.empty:
		daily_meditation_same_day.loc[relevant_checkpoints.index, 'meditation_same_day'] += meditation['meditation_duration']

# Merge sleep data with meditation data (left join to keep all sleep data)
aggregated = pd.merge(aggregated, daily_meditation, on='checkpoint', how='left')
aggregated = pd.merge(aggregated, daily_meditation_same_day, on='checkpoint', how='left').copy()

# Fill any NaN meditation durations with 0 (for days with no meditation in range)
aggregated = aggregated.fillna({'meditation_duration': 0, 'meditation_same_day': 0})

# Exclude only days that were themselves retreat days (>6h meditation that day),
# not the days following retreats (which had no imposed sleep schedule)
retreat_days = aggregated['meditation_same_day'] >= 6*3600
no_outliers = aggregated.loc[~retreat_days]

def plot_with_regression(x, y, field, filename):
	slope, intercept, r, p, stderr = sps.linregress(x, y)
	fig, ax = plt.subplots()
	ax.scatter(x, y, s=10)
	over = np.linspace(0, x.max())
	ax.plot(over, intercept + slope * over, color='red')
	ax.set_xlabel('meditation (hours)')
	ax.set_ylabel(field)
	label = f'slope={slope:.2f} min/hr\nintercept={intercept:.1f}\nr={r:.3f}, p={p:.3f}\nstderr={stderr:.3f}'
	ax.text(0.98, 0.98, label, transform=ax.transAxes,
		fontsize=9, verticalalignment='top', horizontalalignment='right',
		bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
	fig.savefig(filename)
	plt.close(fig)

field='minutes_asleep'
agg_h = aggregated['meditation_duration'] / 3600
plot_with_regression(agg_h, aggregated[field], field, 'aggregated_scatter_total.png')

no_h = no_outliers['meditation_duration'] / 3600
plot_with_regression(no_h, no_outliers[field], field, 'no_outliers_scatter_total.png')
