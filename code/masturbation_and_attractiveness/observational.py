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

approaches=pd.read_csv('../../data/daygame_approaches.csv')
approaches['Datetime']=pd.to_datetime(approaches['Datetime'], utc=True).dt.tz_convert('CET')

both=pd.merge_asof(approaches, masturbations, left_on='Datetime', right_on='datetime', direction='backward')

both['Abstinence']=both['Datetime']-both['datetime']
both['Rounded']=both['Abstinence'].dt.round('2d')
both['Contactind']=both['Contact'].notna()

result=both[['Rounded', 'Contactind']].groupby('Rounded').agg(['mean', 'size'])

def betavar(group):
	a=group.sum()
	b=(~group).sum()
	return np.sqrt((a*b)/((a+b)**2*(a+b+1)))

result['std']=both[['Rounded', 'Contactind']].groupby('Rounded').agg(betavar).rename(columns={'Contactind': 'std'})

#TODO: add sample size, also x-axis is slightly artefacted
result['Contactind']['mean'].plot.bar(yerr=result['std'], rot=90, figsize=(16, 14),
	xlabel='Time since last masturbation', ylabel='Percentage contact exchanged', color='red')
plt.savefig('errorbars.png')
