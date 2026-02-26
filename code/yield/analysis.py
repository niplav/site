import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from load import get_meditations

import bisect
import glob
import json
import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from tigramite import data_processing as pp
from tigramite import plotting as tp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.parcorr import ParCorr

# Global configuration
INTERVAL = '900s'
TAU_MIN = 1
TAU_MAX = 96
FITBIT_PATH = '/usr/local/src/myfitbit/BS7PZZ'
TIMELINE_PATH = '/usr/local/backup/google/Timeline.json'
AIR_PATH = '/usr/local/etc/data/air.csv'
CONSULTING_PATH = os.path.expanduser('~/admn/consulting')
SUBSTANCES = [
	'melatonin', 'creatine', 'vitamind3', 'caffeine', 'sugar',
	'vitaminb12', 'l-theanine', 'omega3', 'magnesium', 'nicotine', 'l-glycine',
]

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
	time_index = pd.date_range(start=df['datetime'].min().floor(interval),
	                           end=df['datetime'].max().ceil(interval),
	                           freq=interval)

	substance_series = {}

	for substance in SUBSTANCES:
		substance_df = df[df['substance'] == substance].sort_values('datetime')
		if len(substance_df) == 0:
			continue

		events_sorted = substance_df['datetime'].values
		idx = np.searchsorted(events_sorted, time_index.values, side='left') - 1
		valid = idx >= 0
		last_times = np.where(valid, events_sorted[np.maximum(idx, 0)], np.datetime64('NaT'))
		hours = np.where(
			valid,
			(time_index.values - last_times) / np.timedelta64(1, 'h'),
			np.nan
		)
		substance_series[substance] = pd.Series(hours, index=time_index)

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

def load_timezone_lookup(path=TIMELINE_PATH):
	with open(path) as f:
		data = json.load(f)
	records = []
	for seg in data.get('semanticSegments', []):
		for key in ('startTime', 'endTime'):
			ts = seg.get(key)
			if not ts:
				continue
			dt = pd.to_datetime(ts)
			offset_min = int(dt.utcoffset().total_seconds() / 60)
			records.append((dt.replace(tzinfo=None), offset_min))
	records.sort()
	return records

def _offset_at(local_dt, lookup):
	times = [r[0] for r in lookup]
	idx = bisect.bisect_right(times, local_dt) - 1
	return lookup[idx][1] if idx >= 0 else 60  # default UTC+1

# Load all monthly Fitbit JSON files for a given data type
def load_fitbit_files(data_type, base_path=FITBIT_PATH):
	records = []
	for f in sorted(glob.glob(f'{base_path}/{data_type}/{data_type}.*.json')):
		with open(f) as fh:
			records.extend(json.load(fh))
	return records

# Process Fitbit sleep data into time series.
# Anchored to wakeup time (endTime); forward-fill 30h like other end-of-period metrics.
def process_fitbit_sleep_data(records, interval=INTERVAL, tz_lookup=None):
	interval_hours = pd.Timedelta(interval).total_seconds() / 3600
	ffill_limit = max(1, int(30 / interval_hours))

	rows = []
	for r in records:
		if not r.get('isMainSleep'):
			continue
		end_naive = pd.to_datetime(r['endTime'])
		offset_min = _offset_at(end_naive, tz_lookup) if tz_lookup else 60
		end = (end_naive - pd.Timedelta(minutes=offset_min)).tz_localize('UTC')
		lvl = r.get('levels', {}).get('summary', {})
		rows.append({
			'date': end.floor(interval),
			'sleep_minutes': r['minutesAsleep'],
			'sleep_efficiency': r['efficiency'],
			'sleep_latency': r['minutesToFallAsleep'],
			'sleep_deep': lvl.get('deep', {}).get('minutes', np.nan),
			'sleep_rem': lvl.get('rem', {}).get('minutes', np.nan),
		})

	df = pd.DataFrame(rows).set_index('date')
	df = df[~df.index.duplicated(keep='last')]
	full_idx = pd.date_range(df.index.min(), df.index.max(), freq=interval, tz='UTC')
	df = df.reindex(full_idx).ffill(limit=ffill_limit)
	return df.reset_index().rename(columns={'index': 'date'})

# Process Fitbit HRV data into time series.
# Daily metric: assign to midnight UTC, forward-fill 30h.
def process_fitbit_hrv_data(records, interval=INTERVAL):
	interval_hours = pd.Timedelta(interval).total_seconds() / 3600
	ffill_limit = max(1, int(30 / interval_hours))

	rows = [{'date': pd.to_datetime(r['dateTime'], utc=True),
	         'hrv_rmssd': r['value']['dailyRmssd']}
	        for r in records]
	df = pd.DataFrame(rows).set_index('date')
	full_idx = pd.date_range(df.index.min(), df.index.max(), freq=interval, tz='UTC')
	df = df.reindex(full_idx).ffill(limit=ffill_limit)
	return df.reset_index().rename(columns={'index': 'date'})

# Process Fitbit resting heart rate into time series.
# Daily metric: assign to midnight UTC, forward-fill 30h.
def process_fitbit_hr_data(records, interval=INTERVAL):
	interval_hours = pd.Timedelta(interval).total_seconds() / 3600
	ffill_limit = max(1, int(30 / interval_hours))

	rows = [{'date': pd.to_datetime(r['dateTime'], utc=True),
	         'resting_hr': r['value']['restingHeartRate']}
	        for r in records
	        if r['value'].get('restingHeartRate') is not None]
	df = pd.DataFrame(rows).set_index('date')
	full_idx = pd.date_range(df.index.min(), df.index.max(), freq=interval, tz='UTC')
	df = df.reindex(full_idx).ffill(limit=ffill_limit)
	return df.reset_index().rename(columns={'index': 'date'})

# Process Fitbit skin temperature deviation into time series.
# Daily metric: assign to midnight UTC, forward-fill 30h.
def process_fitbit_temp_data(records, interval=INTERVAL):
	interval_hours = pd.Timedelta(interval).total_seconds() / 3600
	ffill_limit = max(1, int(30 / interval_hours))

	rows = [{'date': pd.to_datetime(r['dateTime'], utc=True),
	         'skin_temp': r['value']['nightlyRelative']}
	        for r in records]
	df = pd.DataFrame(rows).set_index('date')
	full_idx = pd.date_range(df.index.min(), df.index.max(), freq=interval, tz='UTC')
	df = df.reindex(full_idx).ffill(limit=ffill_limit)
	return df.reset_index().rename(columns={'index': 'date'})

# Generic helper for simple Fitbit daily scalar metrics (date-keyed, ffill 30h).
def _fitbit_daily(records, col_name, extract_fn, interval=INTERVAL):
	interval_hours = pd.Timedelta(interval).total_seconds() / 3600
	ffill_limit = max(1, int(30 / interval_hours))
	rows = []
	for r in records:
		val = extract_fn(r['value'])
		if val is not None:
			rows.append({'date': pd.to_datetime(r['dateTime'], utc=True), col_name: float(val)})
	df = pd.DataFrame(rows).set_index('date')
	full_idx = pd.date_range(df.index.min(), df.index.max(), freq=interval, tz='UTC')
	df = df.reindex(full_idx).ffill(limit=ffill_limit)
	return df.reset_index().rename(columns={'index': 'date'})

# Read raw air quality data
def load_air_data(path=AIR_PATH):
	df = pd.read_csv(path, low_memory=False)
	df['timestamp'] = pd.to_datetime(df['timestamp'], format='ISO8601', utc=True, errors='coerce')
	for col in ['pm2_5', 'co2_ppm', 'temperature', 'humidity']:
		df[col] = pd.to_numeric(df[col], errors='coerce')
	return df.dropna(subset=['timestamp'])

# Process air quality into time series.
# High-frequency sensor data: resample to interval mean, interpolate short gaps.
def process_air_data(df, interval=INTERVAL):
	df = df.set_index('timestamp')
	agg = df[['pm2_5', 'co2_ppm', 'temperature', 'humidity']].resample(interval).mean()
	agg = agg.interpolate(method='linear', limit=3)
	result = agg.reset_index().rename(columns={'timestamp': 'date'})
	result['date'] = pd.to_datetime(result['date'], utc=True)
	return result

# Read consulting worktime CSVs
def load_worktime_data(base=CONSULTING_PATH):
	files = sorted(glob.glob(f'{base}/*.csv'))
	frames = []
	for f in files:
		df = pd.read_csv(f, usecols=[0, 1], header=None, names=['start', 'end'])
		frames.append(df)
	df = pd.concat(frames, ignore_index=True)
	df['start'] = pd.to_datetime(df['start'], format='mixed', utc=True, errors='coerce')
	df['end'] = pd.to_datetime(df['end'], format='mixed', utc=True, errors='coerce')
	return df.dropna(subset=['start', 'end'])

# Process worktime into time series.
# Genuine 0 on non-work slots — no ffill in merge pass.
def process_worktime_data(df, interval=INTERVAL):
	iv = pd.Timedelta(interval)
	time_index = pd.date_range(df['start'].min().floor(interval),
	                           df['end'].max().ceil(interval),
	                           freq=interval, tz='UTC')
	work_minutes = pd.Series(0.0, index=time_index)

	for _, row in df.iterrows():
		slot = row['start'].floor(interval)
		while slot < row['end']:
			ov_start = max(row['start'], slot)
			ov_end = min(row['end'], slot + iv)
			mins = max(0, (ov_end - ov_start).total_seconds() / 60)
			if slot in work_minutes.index:
				work_minutes[slot] += mins
			slot += iv

	result = pd.DataFrame({'date': time_index, 'work_minutes': work_minutes.values})
	result['date'] = pd.to_datetime(result['date'], utc=True)
	return result

# Read raw light exposure data
def load_light_data():
	df = pd.read_csv('../../data/light.csv')
	df['start'] = pd.to_datetime(df['start'], utc=True)
	df['stop'] = pd.to_datetime(df['stop'], utc=True)
	return df

# Process light exposure into time series.
# lux-minutes per slot; forward-fill up to 8h (lumenator state persists).
def process_light_data(df, interval=INTERVAL):
	interval_hours = pd.Timedelta(interval).total_seconds() / 3600
	ffill_limit = max(1, int(8 / interval_hours))

	df['slot'] = df['start'].dt.floor(interval)
	df['lux_minutes'] = df['lumens'] * (df['stop'] - df['start']).dt.total_seconds() / 60
	grouped = df.groupby('slot')['lux_minutes'].sum()
	full_idx = pd.date_range(grouped.index.min(), grouped.index.max(),
	                         freq=interval, tz='UTC')
	grouped = grouped.reindex(full_idx).ffill(limit=ffill_limit)
	result = grouped.reset_index()
	result.columns = ['date', 'lux_minutes']
	result['date'] = pd.to_datetime(result['date'], utc=True)
	return result

# Read raw air filter (Cuboid) run intervals
def load_air_filter_data():
	df = pd.read_csv('../../data/cuboid.csv')
	df['start'] = pd.to_datetime(df['start'], utc=True)
	df['end'] = pd.to_datetime(df['end'], utc=True)
	return df

# Process air filter into time series.
# Minutes per interval the filter was running; genuine 0 when off — no ffill.
def process_air_filter_data(df, interval=INTERVAL):
	iv = pd.Timedelta(interval)
	time_index = pd.date_range(df['start'].min().floor(interval),
	                           df['end'].max().ceil(interval),
	                           freq=interval, tz='UTC')
	filter_minutes = pd.Series(0.0, index=time_index)

	for _, row in df.iterrows():
		slot = row['start'].floor(interval)
		while slot < row['end']:
			ov_start = max(row['start'], slot)
			ov_end = min(row['end'], slot + iv)
			mins = max(0, (ov_end - ov_start).total_seconds() / 60)
			if slot in filter_minutes.index:
				filter_minutes[slot] += mins
			slot += iv

	result = pd.DataFrame({'date': time_index, 'air_filter_minutes': filter_minutes.values})
	result['date'] = pd.to_datetime(result['date'], utc=True)
	return result

# Prepare data for tigramite analysis
def prepare_tigramite_data(interval='2h', start_date=None):
	meditation_data = get_meditations()
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

	tz_lookup = load_timezone_lookup()
	fitbit_sleep = process_fitbit_sleep_data(load_fitbit_files('sleep'), interval, tz_lookup)
	fitbit_hrv = process_fitbit_hrv_data(load_fitbit_files('hrv'), interval)
	fitbit_hr = process_fitbit_hr_data(load_fitbit_files('heartrate'), interval)
	fitbit_temp = process_fitbit_temp_data(load_fitbit_files('temperature_skin'), interval)
	fitbit_steps = _fitbit_daily(load_fitbit_files('steps'), 'steps', lambda v: int(v), interval)
	fitbit_active = _fitbit_daily(load_fitbit_files('minutes_very_active'), 'minutes_very_active', lambda v: int(v), interval)
	fitbit_breath = _fitbit_daily(load_fitbit_files('breathing_rate'), 'breathing_rate', lambda v: v['breathingRate'], interval)
	fitbit_spo2 = _fitbit_daily(load_fitbit_files('spo2'), 'spo2_avg', lambda v: v['avg'], interval)

	air_quality = process_air_data(load_air_data())
	worktime = process_worktime_data(load_worktime_data())
	light = process_light_data(load_light_data())
	air_filter = process_air_filter_data(load_air_filter_data())

	# Merge all sources
	merged_data = pd.merge(daily_med, daily_mood, on='date', how='outer')
	merged_data = pd.merge(merged_data, daily_mental, on='date', how='outer')
	merged_data = pd.merge(merged_data, daily_weight, on='date', how='outer')
	merged_data = pd.merge(merged_data, daily_anki, on='date', how='outer')
	merged_data = pd.merge(merged_data, fitbit_sleep, on='date', how='outer')
	merged_data = pd.merge(merged_data, fitbit_hrv, on='date', how='outer')
	merged_data = pd.merge(merged_data, fitbit_hr, on='date', how='outer')
	merged_data = pd.merge(merged_data, fitbit_temp, on='date', how='outer')
	merged_data = pd.merge(merged_data, fitbit_steps, on='date', how='outer')
	merged_data = pd.merge(merged_data, fitbit_active, on='date', how='outer')
	merged_data = pd.merge(merged_data, fitbit_breath, on='date', how='outer')
	merged_data = pd.merge(merged_data, fitbit_spo2, on='date', how='outer')
	merged_data = pd.merge(merged_data, air_quality, on='date', how='outer')
	merged_data = pd.merge(merged_data, worktime, on='date', how='outer')
	merged_data = pd.merge(merged_data, light, on='date', how='outer')
	merged_data = pd.merge(merged_data, air_filter, on='date', how='outer')

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

	# Zero-fill count/duration columns that are genuinely 0 outside their data range
	for col in ['work_minutes', 'air_filter_minutes']:
		merged_data[col] = merged_data[col].fillna(0)

	# Per-variable upsampling:
	# - Mood: snapshot of current state, forward-fill up to 8h (already done in
	#   process_mood_data, but gaps introduced by the outer merge need another pass)
	# - Mental: end-of-day summary, replicate across ~30h (slightly > 1 day)
	# - Everything else: genuinely undefined between measurements → stays NaN → masked
	interval_hours = pd.Timedelta(interval).total_seconds() / 3600
	mood_cols = ['happy', 'content', 'relaxed', 'horny']
	mental_cols = ['productivity', 'creativity', 'sublen']
	fitbit_cols = ['sleep_minutes', 'sleep_efficiency', 'sleep_latency', 'sleep_deep', 'sleep_rem',
	               'hrv_rmssd', 'resting_hr', 'skin_temp',
	               'steps', 'minutes_very_active', 'breathing_rate', 'spo2_avg']
	env_cols = ['pm2_5', 'co2_ppm', 'temperature', 'humidity', 'lux_minutes']
	# work_minutes and air_filter_minutes are genuine zeros — no ffill
	merged_data[mood_cols] = merged_data[mood_cols].ffill(limit=max(1, int(8 / interval_hours)))
	merged_data[mental_cols] = merged_data[mental_cols].ffill(limit=max(1, int(30 / interval_hours)))
	merged_data[fitbit_cols] = merged_data[fitbit_cols].ffill(limit=max(1, int(30 / interval_hours)))
	merged_data[env_cols] = merged_data[env_cols].ffill(limit=max(1, int(3 / interval_hours)))

	if start_date is not None:
		start_date = pd.to_datetime(start_date, utc=True)
		original_len = len(merged_data)
		merged_data = merged_data[merged_data['date'] >= start_date]
		filtered_len = len(merged_data)
		print(f"Filtered data from {start_date.strftime('%Y-%m-%d')}: {original_len} -> {filtered_len} rows ({filtered_len/original_len:.1%} kept)")

	# Log transform duration columns and substances (clip to 0 first — negative values are data errors)
	for col in merged_data.columns:
		if col.endswith('_hours') or col.endswith('_minutes') or col in SUBSTANCES:
			merged_data[col] = np.log1p(merged_data[col].clip(lower=0))

	base_variables = [
		'meditation_proportion', 'num_sessions',
		'reviews_count', 'total_anki_time',
		'abstinence_hours', 'weight',
		'steps', 'minutes_very_active',
		'happy', 'content', 'relaxed', 'horny',
		'productivity', 'creativity', 'sublen',
		'mindfulness', 'concentration',
		'avg_review_time', 'success_rate', 'masturbation_enjoyment',
		'sleep_minutes', 'sleep_efficiency', 'sleep_latency', 'sleep_deep', 'sleep_rem',
		'hrv_rmssd', 'resting_hr', 'skin_temp', 'breathing_rate', 'spo2_avg',
		'pm2_5', 'co2_ppm', 'temperature', 'humidity',
		'work_minutes', 'lux_minutes', 'air_filter_minutes',
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
		results = pcmci.run_pcmciplus(tau_min=TAU_MIN, tau_max=TAU_MAX, pc_alpha=0.05, link_assumptions=link_assumptions)
	else:
		results = pcmci.run_pcmciplus(tau_min=TAU_MIN, tau_max=TAU_MAX, pc_alpha=0.05)

	print("\nSignificant causal links at alpha = 0.05:")
	pcmci.print_significant_links(
		p_matrix=results['p_matrix'],
		val_matrix=results['val_matrix'],
		alpha_level=0.05
	)

	# Bipartite layout: intervenables left, measurables right.
	measurable_vars = {
		'happy', 'content', 'relaxed', 'horny',
		'productivity', 'creativity', 'sublen',
		'mindfulness', 'concentration',
		'avg_review_time', 'success_rate', 'masturbation_enjoyment',
		'weight',
		'sleep_minutes', 'sleep_efficiency', 'sleep_latency', 'sleep_deep', 'sleep_rem',
		'hrv_rmssd', 'resting_hr', 'skin_temp', 'breathing_rate', 'spo2_avg',
	}
	var_names = dataframe.var_names
	left_idx = [i for i, v in enumerate(var_names) if v not in measurable_vars]
	right_idx = [i for i, v in enumerate(var_names) if v in measurable_vars]

	# Sort each side by total cross-side |val|, strongest at top.
	vm = results['val_matrix']
	def cross_strength(i, other):
		return sum(np.sum(np.abs(vm[i, j, :])) + np.sum(np.abs(vm[j, i, :])) for j in other)
	left_sorted  = sorted(left_idx,  key=lambda i: cross_strength(i, right_idx), reverse=True)
	right_sorted = sorted(right_idx, key=lambda j: cross_strength(j, left_idx),  reverse=True)

	# Strip same-side links from the plot (keep results intact).
	plot_val   = vm.copy()
	plot_graph = results['graph'].copy()
	for i in left_idx:
		for j in left_idx:
			plot_val[i, j, :]   = 0
			plot_graph[i, j, :] = ''
	for i in right_idx:
		for j in right_idx:
			plot_val[i, j, :]   = 0
			plot_graph[i, j, :] = ''

	# Assign positions.
	left_rank  = {v: k for k, v in enumerate(left_sorted)}
	right_rank = {v: k for k, v in enumerate(right_sorted)}
	x_pos, y_pos = [], []
	for i, v in enumerate(var_names):
		if v in measurable_vars:
			x_pos.append(1.0)
			y_pos.append(1.0 - 2.0 * right_rank[i] / max(len(right_idx) - 1, 1))
		else:
			x_pos.append(-1.0)
			y_pos.append(1.0 - 2.0 * left_rank[i] / max(len(left_idx) - 1, 1))
	node_pos = {'x': x_pos, 'y': y_pos}

	tp.plot_graph(
		val_matrix=plot_val,
		graph=plot_graph,
		var_names=dataframe.var_names,
		link_colorbar_label='MCI',
		node_colorbar_label='Auto-MCI',
		node_pos=node_pos,
		figsize=(24, 22),
		node_size=0.08,
		arrow_linewidth=2.0
	)

	plt.savefig('graph.png', dpi=300, bbox_inches='tight')
	return results, dataframe

# Execute analysis
if __name__ == "__main__":
	results, dataframe = run_causal_analysis()
