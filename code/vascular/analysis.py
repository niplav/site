import numpy as np
import pandas as pd
import scipy.stats as sps
import matplotlib.pyplot as plt

def get_meditations():
        meditations=pd.read_csv('../../data/meditations.csv')
        meditations['meditation_start']=pd.to_datetime(meditations['meditation_start'], utc=True, format='mixed')
        meditations['meditation_end']=pd.to_datetime(meditations['meditation_end'], utc=True, format='mixed')

        return meditations

def get_approaches():
	approaches=pd.read_csv('../../data/daygame_approaches.csv')
	approaches['Datetime']=pd.to_datetime(approaches['Datetime'], utc=True).dt.tz_convert('CET')

	return approaches

def get_sessions():
	sessions=pd.read_csv('../../data/daygame_sessions.csv')
	sessions['Depart']=pd.to_datetime(sessions['Depart'], utc=True).dt.tz_convert('CET')
	sessions['Start']=pd.to_datetime(sessions['Start'], utc=True).dt.tz_convert('CET')
	sessions['End']=pd.to_datetime(sessions['End'], utc=True).dt.tz_convert('CET')
	sessions['Return']=pd.to_datetime(sessions['Return'], utc=True).dt.tz_convert('CET')

	return sessions

def merged_approaches_meditations():
	approaches=get_approaches()
	meditations=get_meditations()

	# I feel like this should be doable with merge_asof, but it doesn't look like it?
	merged=pd.merge(meditations, approaches, how='cross')
	merged['diff']=merged['Datetime']-merged['meditation_end']
	merged=merged.loc[(merged['diff']<=pd.Timedelta(timeframe, 'd')) & (merged['diff']>=pd.Timedelta(0, 's'))]

	summed=merged[['Approach', 'meditation_duration']].groupby('Approach').sum()

	both=pd.merge(approaches, summed, on='Approach')
	both['Rounded']=(both['meditation_duration']/(rounder)).round()
	both['Contactind']=both['Contact'].notna()

	return both

def merged_sessions_meditations():
	meditations=get_meditations()
	sessions=get_sessions()

	merged=pd.merge(meditations, sessions, how='cross')
	merged['diff']=merged['Return']-merged['meditation_end']
	merged=merged.loc[(merged['diff']<=pd.Timedelta(timeframe, 'd')) & (merged['diff']>=pd.Timedelta(0, 's'))]

	summed=merged[['Return', 'meditation_duration']].groupby('Return').sum()
	both=pd.merge(sessions, summed, on='Return')

	return both

hourseconds=60*60
rounder=hourseconds
timeframe=7 #days

both=merged_approaches_meditations()

slope, intercept, r, p, stderr=sps.linregress(both['meditation_duration'], both['Contactind'])

result=both[['Rounded', 'Contactind']].groupby('Rounded').agg(['mean', 'size'])

def betavar(group):
	a=group.sum()
	b=(~group).sum()
	return np.sqrt((a*b)/((a+b)**2*(a+b+1)))

result['std']=both[['Rounded', 'Contactind']].groupby('Rounded').agg(betavar).rename(columns={'Contactind': 'std'})
result['Contactind']['mean'].plot.bar(yerr=result['std'], rot=90, figsize=(11, 9),
        xlabel='Hours of meditation in the last week', ylabel='Proportion contact exchanged', color='red')
plt.savefig('errorbars.png')

# Plotting volume

both=merged_sessions_meditations()
slope, intercept, r, p, stderr=sps.linregress(both['meditation_duration'], both['Amount'])

filtered=both.loc[both['meditation_duration']<60000]
f_slope, f_intercept, f_r, f_p, f_stderr=sps.linregress(filtered['meditation_duration'], filtered['Amount'])

fig=plt.figure(figsize=(8,8))
plt.xlabel('Amount of meditation in the last week')
plt.ylabel('Number of approaches in session')

plt.plot(both['meditation_duration'], both['Amount'], '.', color='blue', markersize=4)
plt.plot(both['meditation_duration'], both['meditation_duration']*slope+intercept, 'red', label='Linear regression, unfiltered data')
plt.plot(filtered['meditation_duration'], filtered['meditation_duration']*f_slope+f_intercept, 'green', label='Linear regression, filtered data')

plt.legend()

plt.savefig('volume.png')
