import numpy as np
import pandas as pd

sessions=pd.read_csv('../../data/daygame_sessions.csv')
approaches=pd.read_csv('../../data/daygame_approaches.csv')

sessions['Depart']=pd.to_datetime(sessions['Depart'])
sessions['Start']=pd.to_datetime(sessions['Start'])
sessions['End']=pd.to_datetime(sessions['End'])
sessions['Return']=pd.to_datetime(sessions['Return'])

approaches['Datetime']=pd.to_datetime(approaches['Datetime'])

def create_timestamps(row):
	times=pd.date_range(row['Start'], row['End'], periods=row['Amount']+1, unit='s')[1:]
	return pd.DataFrame({
		'Last': row['Last'],
		'Estimated': times
	})

# Create all timestamps
new_times=pd.concat([create_timestamps(row) for _, row in sessions.iterrows()])
new_times['Index']=range(1, len(new_times)+1)

timed=pd.merge(new_times, approaches, left_on='Index', right_on='Approach')
timed['Datetime']=timed['Datetime'].fillna(timed['Estimated'])
timed['Datetime']=timed['Datetime'].dt.tz_localize('CET')
timed=timed.sort_values(by='Datetime')

timed=timed.drop(['Last', 'Index', 'Estimated'], axis=1)

def get_masturbations():
	masturbations=pd.read_csv('../../data/masturbations.csv')
	masturbations.loc[masturbations['methods'].isna(),'methods']='n'
	masturbations['datetime']=pd.to_datetime(masturbations['datetime'], utc=True, format='mixed', dayfirst=False)

	return masturbations

masturbations=get_masturbations()
masturbations['datetime']=masturbations['datetime'].dt.tz_convert('CET')
masturbations=masturbations.sort_values(by='datetime')

both=pd.merge_asof(timed, masturbations, left_on='Datetime', right_on='datetime', direction='backward')
both['Abstinence']=both['Datetime']-both['datetime']
