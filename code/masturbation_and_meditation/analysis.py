import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_meditations():
        meditations=pd.read_csv('../../data/meditations.csv')
        meditations['meditation_start']=pd.to_datetime(meditations['meditation_start'], unit='ms', utc=True)
        meditations['meditation_end']=pd.to_datetime(meditations['meditation_end'], unit='ms', utc=True)

        return meditations

def get_masturbations():
        masturbations=pd.read_csv('../../data/masturbations.csv')
        masturbations.loc[masturbations['methods'].isna(),'methods']='n'
        masturbations['datetime']=pd.to_datetime(masturbations['datetime'], utc=True, format='mixed', dayfirst=False)

        return masturbations

meditations=get_meditations()
masturbations=get_masturbations()

tohu=masturbations['datetime'].min()
meditations=meditations.loc[meditations['meditation_start']>tohu]

meditations=meditations.sort_values('meditation_start')
masturbations=masturbations.sort_values('datetime')
combined=pd.merge_asof(meditations, masturbations, left_on='meditation_start', right_on='datetime', direction='backward')
combined['diff']=combined['meditation_start']-combined['datetime']

mindfulness_correlations=[]
concentration_correlations=[]
sample_sizes=[]
for i in range(0,30):
        combined_long=combined.loc[combined['diff']>pd.Timedelta(str(i)+'d')]
        sample_sizes.append(len(combined_long))
        mindfulness_correlations.append(combined_long[['mindfulness_rating', 'concentration_rating', 'diff']].corr(numeric_only=False)['mindfulness_rating']['diff'])
        concentration_correlations.append(combined_long[['mindfulness_rating', 'concentration_rating', 'diff']].corr(numeric_only=False)['concentration_rating']['diff'])

fig=plt.figure(figsize=(8,8))
_, ax1 = plt.subplots()
ax2=ax1.twinx()
ax2.set_ylabel('Sample size')
ax1.plot(mindfulness_correlations, color='red', label='Mindfulness quality correlations')
ax1.plot(concentration_correlations, color='blue', label='Concentration quality correlations')
ax1.set_xlabel('Time since last masturbation (days)')
ax1.set_ylabel('Correlation (Pearson)')
ax2.plot(sample_sizes, color='green', label='Sample size')
ax1.legend()
ax2.legend()
plt.savefig('time_correlations.png')
