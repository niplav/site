import numpy as np
import pandas as pd
import scipy.stats as sps
import matplotlib.pyplot as plt

def get_masturbations():
	masturbations=pd.read_csv('../../data/masturbations.csv')
	masturbations.loc[masturbations['methods'].isna(),'methods']='n'
	masturbations['datetime']=pd.to_datetime(masturbations['datetime'], utc=True, format='mixed', dayfirst=False)
	masturbations['datetime']=masturbations['datetime'].dt.tz_convert('CET')
	masturbations=masturbations.sort_values(by='datetime')

	return masturbations

def get_sessions():
	sessions=pd.read_csv('../../data/daygame_sessions.csv')
	sessions['Depart']=pd.to_datetime(sessions['Depart'], utc=True).dt.tz_convert('CET')
	sessions['Start']=pd.to_datetime(sessions['Start'], utc=True).dt.tz_convert('CET')
	sessions['End']=pd.to_datetime(sessions['End'], utc=True).dt.tz_convert('CET')
	sessions['Return']=pd.to_datetime(sessions['Return'], utc=True).dt.tz_convert('CET')

	return sessions

def merged_masturbations_sessions():
	masturbations=get_masturbations()
	sessions=get_sessions()

	merged=pd.merge_asof(sessions, masturbations, left_on='Depart', right_on='datetime', direction='backward')
	merged['diff']=merged['Depart']-merged['datetime']
	merged['daydiff']=merged['diff'].dt.total_seconds()/dayseconds
	merged=merged.dropna()

	return merged

dayseconds=60*60*24
rounder=dayseconds
timeframe=120 #days

merged=merged_masturbations_sessions()

slope, intercept, r, p, stderr=sps.linregress(merged['daydiff'], merged['Amount'])

fig=plt.figure(figsize=(8,8))
plt.xlabel('Days since last masturbation')
plt.ylabel('Number of approaches in session')

plt.plot(merged['daydiff'], merged['Amount'], '.', color='blue', markersize=4)
plt.plot(merged['daydiff'], merged['daydiff']*slope+intercept, 'red')

plt.savefig('volume.png')
