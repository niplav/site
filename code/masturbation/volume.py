import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_masturbations():
	masturbations=pd.read_csv('../../data/masturbations.csv')
	masturbations.loc[masturbations['methods'].isna(),'methods']='n'
	masturbations['datetime']=pd.to_datetime(masturbations['datetime'], utc=True, format='mixed', dayfirst=False)

	return masturbations

masturbations=get_masturbations()
masturbations['datetime']=masturbations['datetime'].dt.tz_convert('CET')
masturbations=masturbations.sort_values(by='datetime')

hourseconds=60*60
rounder=hourseconds
timeframe=120 #days

sessions=pd.read_csv('../../data/daygame_sessions.csv')
sessions['Depart']=pd.to_datetime(sessions['Depart'], utc=True).dt.tz_convert('CET')
sessions['Start']=pd.to_datetime(sessions['Start'], utc=True).dt.tz_convert('CET')
sessions['End']=pd.to_datetime(sessions['End'], utc=True).dt.tz_convert('CET')
sessions['Return']=pd.to_datetime(sessions['Return'], utc=True).dt.tz_convert('CET')

merged=pd.merge_asof(sessions, masturbations, left_on='Depart', right_on='datetime', direction='backward')
merged['diff']=merged['Depart']-merged['datetime']
merged=merged.dropna()

#slope, intercept, r, p, stderr=sps.linregress(merged['diff'], both['Amount'])

merged.plot.scatter(x='diff', y='Amount')
plt.savefig('scatter.png')
