import glob
import json
import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'
FITBIT_DIR = Path('/usr/local/backup/fitbit')

def get_sleep():
	sleep_data = []
	for f in sorted(glob.glob(str(FITBIT_DIR / 'sleep' / 'sleep.*.json'))):
		sleep_data += json.load(open(f))

	sleep_values = {
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
		'wake_minutes': [],
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
			sleep_values['rem_count'].append(session['levels']['summary']['rem']['count'])
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

	return pd.DataFrame(sleep_values)

def get_meditations():
	meditations = pd.read_csv(DATA_DIR / 'meditations.csv')
	meditations = meditations.assign(
		meditation_start=pd.to_datetime(meditations['meditation_start'], utc=True, format='mixed'),
		meditation_end=pd.to_datetime(meditations['meditation_end'], utc=True, format='mixed'),
	)
	return meditations
