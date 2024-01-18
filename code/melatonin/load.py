import math
import json
import numpy as np
import pandas as pd
import scipy.stats as scistat

sleep_file_name='../../data/sleep.json'
sleep_file=open(sleep_file_name, 'r')
sleep_data = json.load(sleep_file)

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

for session in sleep_data['sleep']:
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

substances=pd.read_csv('../../data/substances.csv')
substances['datetime']=pd.to_datetime(substances['datetime'], utc=True)
melatonin_consumption=substances.loc[substances['substance']=='melatonin']
melatonin_consumption=melatonin_consumption.loc[melatonin_consumption['datetime']>first_sleep]

melatonin_consumption.sort_values(by=['datetime'], inplace=True)
sleep.sort_values(by=['start_time'], inplace=True)

melatonin_sleep=pd.merge_asof(melatonin_consumption, sleep, left_on='datetime', right_on='start_time', direction='forward')

non_melatonin_dates=list(set(sleep['date'])-set(melatonin_sleep['date']))
non_melatonin=pd.DataFrame(non_melatonin_dates, columns=['date'])
non_melatonin_sleep=pd.merge(sleep, non_melatonin, on='date')

non_nap_melatonin_sleep=melatonin_sleep.loc[(melatonin_sleep['start_time'].dt.hour<6) & (melatonin_sleep['start_time'].dt.hour<18)]
non_nap_non_melatonin_sleep=non_melatonin_sleep.loc[(non_melatonin_sleep['start_time'].dt.hour<6) & (non_melatonin_sleep['start_time'].dt.hour<18)]

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
	meditations['meditation_start']=pd.to_datetime(meditations['meditation_start'], unit='ms', utc=True)
	meditations['meditation_end']=pd.to_datetime(meditations['meditation_end'], unit='ms', utc=True)

	return meditations

def get_moods():
	mood=pd.read_csv('../../data/mood.csv')
	alarms=pd.to_datetime(pd.Series(mood['alarm']))
	mood['alarm']=pd.DatetimeIndex(alarms.dt.tz_localize('CET', ambiguous='infer')).tz_convert(tz='UTC')
	dates=pd.to_datetime(pd.Series(mood['date']))
	mood['date']=pd.DatetimeIndex(dates.dt.tz_localize('CET', ambiguous='infer')).tz_convert(tz='UTC')

	return mood

def get_mental():
	mental=pd.read_csv('../../data/mental.csv')
	mental['datetime']=pd.to_datetime(mental['datetime'], utc=True)

	return mental

def get_flashcards():
	flashcards=pd.read_csv('../../data/anki_reviews.csv')
	flashcards['id']=pd.to_datetime(flashcards['id'], unit='ms', utc=True)
	flashcards['cid']=pd.to_datetime(flashcards['cid'], unit='ms', utc=True)

	return flashcards

def get_masturbations():
	masturbations=pd.read_csv('../../data/masturbations.csv')
	masturbations.loc[masturbations['methods'].isna(),'methods']='n'
	masturbations['datetime']=pd.to_datetime(masturbations['datetime'], utc=True, format='mixed', dayfirst=False)

	return masturbations
