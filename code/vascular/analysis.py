import numpy as np
import pandas as pd
import scipy.stats as sps
import matplotlib.pyplot as plt

def get_meditations():
        meditations=pd.read_csv('../../data/meditations.csv')
        meditations['meditation_start']=pd.to_datetime(meditations['meditation_start'], utc=True, format='mixed')
        meditations['meditation_end']=pd.to_datetime(meditations['meditation_end'], utc=True, format='mixed')

        return meditations

hourseconds=60*60
rounder=hourseconds
timeframe=7 #days

approaches=pd.read_csv('../../data/daygame_approaches.csv')
approaches['Datetime']=pd.to_datetime(approaches['Datetime'], utc=True).dt.tz_convert('CET')

meditations=get_meditations()

# I feel like this should be doable with merge_asof, but it doesn't look like it?
merged=pd.merge(meditations, approaches, how='cross')
merged['diff']=merged['Datetime']-merged['meditation_end']
merged=merged.loc[(merged['diff']<=pd.Timedelta(timeframe, 'd')) & (merged['diff']>=pd.Timedelta(0, 's'))]

summed=merged[['Approach', 'meditation_duration']].groupby('Approach').sum()

both=pd.merge(approaches, summed, on='Approach')
both['Rounded']=(both['meditation_duration']/(rounder)).round()
both['Contactind']=both['Contact'].notna()

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
