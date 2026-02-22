import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from tigramite import data_processing as pp
from tigramite import plotting as tp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.parcorr import ParCorr

# Global configuration
INTERVAL = '4h'

# Read raw meditation data
def load_meditation_data():
	meditation_data = pd.read_csv('../../data/meditations.csv')
	meditation_data['meditation_start'] = pd.to_datetime(meditation_data['meditation_start'], format='ISO8601', utc=True)
	meditation_data['meditation_end'] = pd.to_datetime(meditation_data['meditation_end'], format='ISO8601', utc=True)
	return meditation_data

# Process meditation data into time series
def process_meditation_data(meditation_data, interval=INTERVAL):
	start_time = meditation_data['meditation_start'].min().floor(interval)
	end_time = meditation_data['meditation_end'].max().ceil(interval)
	time_index = pd.date_range(start=start_time, end=end_time, freq=interval)

	interval_duration = pd.Timedelta(interval).total_seconds() / 60

	result = pd.DataFrame(index=time_index)
	result['date'] = result.index
	result['meditation_proportion'] = 0.0
	result['num_sessions'] = 0
	result['mindfulness'] = np.nan
	result['concentration'] = np.nan

	for i in range(len(time_index) - 1):
		interval_start = time_index[i]
		interval_end = time_index[i + 1]

		overlapping = meditation_data[
			(meditation_data['meditation_start'] < interval_end) &
			(meditation_data['meditation_end'] > interval_start)
		]

		starting_in_interval = meditation_data[
			(meditation_data['meditation_start'] >= interval_start) &
			(meditation_data['meditation_start'] < interval_end)
		]

		if len(overlapping) > 0:
			ov_start = overlapping['meditation_start'].clip(lower=interval_start)
			ov_end = overlapping['meditation_end'].clip(upper=interval_end)
			total_meditation_minutes = (ov_end - ov_start).dt.total_seconds().clip(lower=0).sum() / 60
			result.loc[interval_start, 'meditation_proportion'] = total_meditation_minutes / interval_duration
			result.loc[interval_start, 'num_sessions'] = len(overlapping)

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

	# mindfulness/concentration are per-session ratings: leave NaN between sessions,
	# to be masked rather than interpolated
	return result.reset_index(drop=True)

# Read raw mood data
def load_mood_data():
	mood_data = pd.read_csv('../../data/mood.csv')
	mood_data['date'] = pd.to_datetime(mood_data['date'])
	return mood_data

# Process mood data into time series.
# Mood is a sampled snapshot of current state: forward-fill up to ~8h, then leave as NaN.
def process_mood_data(mood_data, interval='2h'):
	interval_hours = pd.Timedelta(interval).total_seconds() / 3600
	ffill_limit = max(1, int(8 / interval_hours))

	mood_data = mood_data.set_index('date')
	resampled = mood_data[['happy', 'content', 'relaxed', 'horny']].resample(interval).mean()
	filled = resampled.ffill(limit=ffill_limit)

	result = filled.reset_index()
	result['date'] = pd.to_datetime(result['date'], utc=True)
	return result.reset_index(drop=True)

# Read raw mental data
def load_mental_data():
	mental_data = pd.read_csv('../../data/mental.csv')
	mental_data['datetime'] = pd.to_datetime(mental_data['datetime'], utc=True)
	return mental_data

# Process mental data into time series.
# These are end-of-day summaries: replication across the day is handled in
# prepare_tigramite_data after the merge.
def process_mental_data(mental_data, interval='2h'):
	daily_mental = mental_data.groupby(mental_data['datetime'].dt.round(interval)).agg({
		'productivity': 'mean',
		'creativity': 'mean',
		'sublen': 'mean'
	}).reset_index()

	daily_mental = daily_mental.rename(columns={'datetime': 'date'})
	daily_mental['date'] = pd.to_datetime(daily_mental['date'])
	return daily_mental

# Read raw masturbation data
def load_masturbation_data():
	df = pd.read_csv('../../data/masturbations.csv')
	df['datetime'] = pd.to_datetime(df['datetime'], format='ISO8601', utc=True)
	df = df.sort_values('datetime')
	return df

# Process masturbation data into time series.
# abstinence_hours is a continuous deterministic function, no upsampling needed.
# enjoyment is a per-event rating: leave NaN between events, to be masked.
def process_masturbation_data(df, interval='2h'):
	time_index = pd.date_range(start=df['datetime'].min(),
	                           end=df['datetime'].max(),
	                           freq=interval)

	events_sorted = df['datetime'].values
	idx = np.searchsorted(events_sorted, time_index.values, side='left') - 1
	valid = idx >= 0
	last_times = np.where(valid, events_sorted[np.maximum(idx, 0)], np.datetime64('NaT'))
	hours = np.where(
		valid,
		(time_index.values - last_times) / np.timedelta64(1, 'h'),
		np.nan
	)
	abstinence_duration = pd.Series(hours, index=time_index)

	enjoyment_series = pd.Series(df['enjoyment'].values, index=df['datetime'])
	# resample bins any multiple events in the same interval; gaps stay NaN
	enjoyment_hourly = enjoyment_series.resample(interval).mean()

	return abstinence_duration, enjoyment_hourly

# Read raw substances data
def load_substances_data():
	df = pd.read_csv('../../data/substances.csv')
	df['datetime'] = pd.to_datetime(df['datetime'], format='ISO8601', utc=True)
	return df

# Process substances data into time series.
# hours_since is a continuous deterministic function, no upsampling needed.
def process_substances_data(df, interval='2h'):
	substance_counts = df['substance'].value_counts()
	substances = substance_counts[substance_counts >= 10].index.tolist()

	time_index = pd.date_range(start=df['datetime'].min().floor(interval),
	                           end=df['datetime'].max().ceil(interval),
	                           freq=interval)

	substance_series = {}

	for substance in substances:
		substance_df = df[df['substance'] == substance].sort_values('datetime')

		events_sorted = substance_df['datetime'].values
		idx = np.searchsorted(events_sorted, time_index.values, side='left') - 1
		valid = idx >= 0
		last_times = np.where(valid, events_sorted[np.maximum(idx, 0)], np.datetime64('NaT'))
		hours = np.where(
			valid,
			(time_index.values - last_times) / np.timedelta64(1, 'h'),
			np.nan
		)
		substance_series[f"{substance}_hours"] = pd.Series(hours, index=time_index)

	return substance_series

# Read raw Anki data
def load_anki_data():
	anki_data = pd.read_csv('../../data/anki_reviews.csv')
	anki_data['datetime'] = pd.to_datetime(anki_data['id'], unit='ms', utc=True)
	return anki_data

# Process Anki data into time series.
# reviews_count and total_anki_time are naturally 0 on empty intervals.
# avg_review_time and success_rate are undefined when there are no reviews: leave as NaN.
def process_anki_data(anki_data, interval='2h'):
	start_time = anki_data['datetime'].min().floor(interval)
	end_time = anki_data['datetime'].max().ceil(interval)
	time_index = pd.date_range(start=start_time, end=end_time, freq=interval)

	reviews_count = pd.Series(index=time_index, data=0, dtype=int)
	avg_review_time = pd.Series(index=time_index, data=np.nan, dtype=float)
	success_rate = pd.Series(index=time_index, data=np.nan, dtype=float)
	total_anki_time = pd.Series(index=time_index, data=0.0, dtype=float)

	anki_data['interval'] = anki_data['datetime'].dt.floor(interval)
	grouped = anki_data.groupby('interval')

	for interval_time, group in grouped:
		if interval_time in time_index:
			reviews_count[interval_time] = len(group)
			avg_review_time[interval_time] = group['time'].mean() / 1000.0
			success_rate[interval_time] = (group['ease'] >= 2).mean()
			total_anki_time[interval_time] = group['time'].sum() / (1000.0 * 60.0)

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
def load_weight_data():
	weight_data = pd.read_csv('../../data/weights.csv')
	weight_data['datetime'] = pd.to_datetime(weight_data['datetime'], utc=True)
	return weight_data

# Process weight data into time series.
# Weight changes slowly and continuously: linear interpolation is appropriate,
# capped at 5 days to avoid bridging long measurement gaps.
def process_weight_data(weight_data, interval='2h'):
	interval_hours = pd.Timedelta(interval).total_seconds() / 3600
	interp_limit = max(1, int(5 * 24 / interval_hours))

	weight_data = weight_data.set_index('datetime')
	weight_resampled = weight_data['weight'].resample(interval).mean()
	weight_interpolated = weight_resampled.interpolate(method='linear', limit=interp_limit)

	result = pd.DataFrame({
		'date': weight_interpolated.index,
		'weight': weight_interpolated.values
	})

	result['date'] = pd.to_datetime(result['date'], utc=True)
	return result.reset_index(drop=True)

# Prepare data for tigramite analysis
def prepare_tigramite_data(interval='2h', start_date=None):
	meditation_data = load_meditation_data()
	mood_data = load_mood_data()
	mental_data = load_mental_data()
	masturbation_data = load_masturbation_data()
	substances_data = load_substances_data()
	weight_data = load_weight_data()
	anki_data = load_anki_data()

	daily_med = process_meditation_data(meditation_data, interval)
	daily_mood = process_mood_data(mood_data, interval)
	daily_mental = process_mental_data(mental_data, interval)
	abstinence_duration, enjoyment_hourly = process_masturbation_data(masturbation_data, interval)
	substance_series = process_substances_data(substances_data, interval)
	daily_weight = process_weight_data(weight_data, interval)
	daily_anki = process_anki_data(anki_data, interval)

	# Merge all sources
	merged_data = pd.merge(daily_med, daily_mood, on='date', how='outer')
	merged_data = pd.merge(merged_data, daily_mental, on='date', how='outer')
	merged_data = pd.merge(merged_data, daily_weight, on='date', how='outer')
	merged_data = pd.merge(merged_data, daily_anki, on='date', how='outer')

	abstinence_duration.index.name = 'date'
	enjoyment_hourly.index.name = 'date'
	merged_data = pd.merge(merged_data,
	                       abstinence_duration.to_frame('abstinence_hours'),
	                       left_on='date', right_index=True, how='outer')
	merged_data = pd.merge(merged_data,
	                       enjoyment_hourly.to_frame('masturbation_enjoyment'),
	                       left_on='date', right_index=True, how='outer')

	for name, series in substance_series.items():
		series.index.name = 'date'
		merged_data = pd.merge(merged_data,
		                       series.to_frame(name),
		                       left_on='date', right_index=True, how='outer')

	merged_data = merged_data.sort_values('date').reset_index(drop=True)

	# Per-variable upsampling:
	# - Mood: snapshot of current state, forward-fill up to 8h (already done in
	#   process_mood_data, but gaps introduced by the outer merge need another pass)
	# - Mental: end-of-day summary, replicate across ~30h (slightly > 1 day)
	# - Everything else: genuinely undefined between measurements → stays NaN → masked
	interval_hours = pd.Timedelta(interval).total_seconds() / 3600
	mood_cols = ['happy', 'content', 'relaxed', 'horny']
	mental_cols = ['productivity', 'creativity', 'sublen']
	merged_data[mood_cols] = merged_data[mood_cols].ffill(limit=max(1, int(8 / interval_hours)))
	merged_data[mental_cols] = merged_data[mental_cols].ffill(limit=max(1, int(30 / interval_hours)))

	if start_date is not None:
		start_date = pd.to_datetime(start_date, utc=True)
		original_len = len(merged_data)
		merged_data = merged_data[merged_data['date'] >= start_date]
		filtered_len = len(merged_data)
		print(f"Filtered data from {start_date.strftime('%Y-%m-%d')}: {original_len} -> {filtered_len} rows ({filtered_len/original_len:.1%} kept)")

	# Log transform hours-since columns
	for col in merged_data.columns:
		if col.endswith('_hours'):
			merged_data[col] = np.log1p(merged_data[col])

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
	data = merged_data[variables].values

	means = np.nanmean(data, axis=0)
	stds = np.nanstd(data, axis=0)
	stds[stds == 0] = 1
	data = (data - means) / stds

	# Build mask from remaining NaN (True = exclude from analysis).
	# These are genuinely missing observations, not legitimate zeros.
	mask = np.isnan(data)

	# tigramite requires no NaN in the data array; fill with 0 (masked values
	# are ignored by ParCorr, so the fill value doesn't matter)
	data = np.nan_to_num(data, nan=0.0)

	dataframe = pp.DataFrame(data,
	                         mask=mask,
	                         var_names=variables,
	                         datatime=merged_data.date)

	return dataframe, merged_data, None

def run_causal_analysis():
	dataframe, merged_data, link_assumptions = prepare_tigramite_data(interval=INTERVAL, start_date='2022-10-01')
	print(merged_data.describe())

	# mask_type='y': exclude time points where the TARGET variable is masked.
	# Switch to 'xyz' for stricter exclusion (also masks when predictors are missing),
	# at the cost of a smaller effective sample.
	parcorr = ParCorr(significance='analytic', mask_type='y')
	pcmci = PCMCI(dataframe=dataframe, cond_ind_test=parcorr, verbosity=1)

	if link_assumptions is not None:
		results = pcmci.run_pcmciplus(tau_min=1, tau_max=24, pc_alpha=0.05, link_assumptions=link_assumptions)
	else:
		results = pcmci.run_pcmciplus(tau_min=1, tau_max=24, pc_alpha=0.05)

	print("\nSignificant causal links at alpha = 0.05:")
	pcmci.print_significant_links(
		p_matrix=results['p_matrix'],
		val_matrix=results['val_matrix'],
		alpha_level=0.05
	)

	n_vars = len(dataframe.var_names)
	radius = 0.8
	angles = np.linspace(0, 2*np.pi, n_vars, endpoint=False)
	node_pos = {
		'x': list(radius * np.cos(angles)),
		'y': list(radius * np.sin(angles))
	}

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
	results, dataframe = run_causal_analysis()
