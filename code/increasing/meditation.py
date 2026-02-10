import math
import json
import numpy as np
import pandas as pd
import scipy.stats as sps
import matplotlib.pyplot as plt

# TODO: Check if retreat days are excluded, or even days not during retreats (that is, no externally imposed sleep schedule)
# but simply days with much meditation.

def normal_likelihood(data, mu, std):
	data_probs=scistat.norm.pdf(data, loc=mu, scale=std)
	return np.multiply.reduce(data_probs, where=~np.isnan(data_probs))

def placebo_likelihood_ratio(active, placebo):
	placebo_mle_lh=normal_likelihood(active, placebo.mean(), placebo.std())
	active_mle_lh=normal_likelihood(active, active.mean(), active.std())
	if active_mle_lh==0:
		return 0
	return active_mle_lh/placebo_mle_lh

def likelihood_ratio_test(lr):
	if lr==0:
		return math.inf
	return 2*np.log(lr)

def llrt_pval(lmbda, df=2):
	return scistat.chi2.cdf(df, lmbda)

def get_meditations():
	meditations=pd.read_csv('../../data/meditations.csv')
	meditations['meditation_start']=pd.to_datetime(meditations['meditation_start'], utc=True, format='mixed')
	meditations['meditation_end']=pd.to_datetime(meditations['meditation_end'], utc=True, format='mixed')

	return meditations

sleep_file_name='../../data/sleep.json'
sleep_file=open(sleep_file_name, 'r')
sleep_data = json.load(sleep_file)

backwards_horizon='4d'
relevant_sleep_cols=['duration', 'minutes_asleep', 'minutes_to_sleep', 'minutes_after_wakeup', 'time_in_bed', 'deep_count', 'deep_minutes', 'light_count', 'light_minutes', 'rem_count', 'rem_minutes', 'wake_count', 'wake_minutes']

sleep_values={
	'date': [],
	'duration': [],
	'efficiency': [],
	'start_time': [],
	'end_time': [],
	'minutes_asleep': [],
	'minutes_to_sleep': [],
	'minutes_after_wakeup': [],
	'time_in_bed': [],
	'deep_count': [],
	'deep_minutes': [],
	'light_count': [],
	'light_minutes': [],
	'rem_count': [],
	'rem_minutes': [],
	'wake_count': [],
	'wake_minutes': []
}

for session in sleep_data:
	sleep_values['date'].append(pd.to_datetime(session['dateOfSleep'], utc=True))
	sleep_values['duration'].append(session['duration'])
	sleep_values['efficiency'].append(session['efficiency'])
	sleep_values['start_time'].append(pd.to_datetime(session['startTime'], utc=True))
	sleep_values['end_time'].append(pd.to_datetime(session['endTime'], utc=True))
	sleep_values['minutes_asleep'].append(session['minutesAsleep'])
	sleep_values['minutes_to_sleep'].append(session['minutesToFallAsleep'])
	sleep_values['minutes_after_wakeup'].append(session['minutesAfterWakeup'])
	sleep_values['time_in_bed'].append(session['timeInBed'])
	if 'deep' in session['levels']['summary'].keys():
		sleep_values['deep_count'].append(session['levels']['summary']['deep']['count'])
		sleep_values['deep_minutes'].append(session['levels']['summary']['deep']['minutes'])
	else:
		sleep_values['deep_count'].append(np.nan)
		sleep_values['deep_minutes'].append(np.nan)
	if 'light' in session['levels']['summary'].keys():
		sleep_values['light_count'].append(session['levels']['summary']['light']['count'])
		sleep_values['light_minutes'].append(session['levels']['summary']['light']['minutes'])
	else:
		sleep_values['light_count'].append(np.nan)
		sleep_values['light_minutes'].append(np.nan)
	if 'rem' in session['levels']['summary'].keys():
		sleep_values['rem_count'].append(session['levels']['summary']['rem']['minutes'])
		sleep_values['rem_minutes'].append(session['levels']['summary']['rem']['minutes'])
	else:
		sleep_values['rem_count'].append(np.nan)
		sleep_values['rem_minutes'].append(np.nan)
	if 'wake' in session['levels']['summary'].keys():
		sleep_values['wake_count'].append(session['levels']['summary']['wake']['count'])
		sleep_values['wake_minutes'].append(session['levels']['summary']['wake']['minutes'])
	else:
		sleep_values['wake_count'].append(np.nan)
		sleep_values['wake_minutes'].append(np.nan)

sleep=pd.DataFrame(sleep_values)
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

# Merge sleep data with meditation data (left join to keep all sleep data)
aggregated = pd.merge(aggregated, daily_meditation, on='checkpoint', how='left')

# Fill any NaN meditation durations with 0 (for days with no meditation in range)
aggregated['meditation_duration'] = aggregated['meditation_duration'].fillna(0)
no_outliers=aggregated.loc[aggregated['meditation_duration']<8*3600]

field='minutes_asleep'
aggregated[['meditation_duration', field]].plot.scatter(x='meditation_duration', y=field)

slope, intercept, r, p, stderr=sps.linregress(aggregated['meditation_duration'], aggregated[field])
over=np.linspace(0, aggregated['meditation_duration'].max())
plt.plot(over, intercept+slope*over, color='red')

plt.savefig('aggregated_scatter_total.png')

no_outliers[['meditation_duration', field]].plot.scatter(x='meditation_duration', y=field)

slope, intercept, r, p, stderr=sps.linregress(no_outliers['meditation_duration'], no_outliers[field])
over=np.linspace(0, no_outliers['meditation_duration'].max())
plt.plot(over, intercept+slope*over, color='red')

plt.savefig('no_outliers_scatter_total.png')
