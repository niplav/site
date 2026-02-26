import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from load import get_meditations

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
combined['rounded']=combined['diff'].dt.round('2d')

result = (combined[['rounded', 'mindfulness_rating', 'concentration_rating']]
          .groupby('rounded')
          .agg(['mean', 'size', 'std'])
          .dropna())

result['mindfulness_rating', 'sem'] = (
    result['mindfulness_rating']['std'] /
    np.sqrt(result['mindfulness_rating']['size'])
)
result['concentration_rating', 'sem'] = (
    result['concentration_rating']['std'] /
    np.sqrt(result['concentration_rating']['size'])
)

fig, ax1 = plt.subplots(figsize=(8,8))
ax2 = ax1.twinx()

x_pos = np.arange(len(result.index))
x_labels = [str(td.days) for td in result.index]

ax1.errorbar(x_pos - 0.2, result['mindfulness_rating']['mean'],
            yerr=result['mindfulness_rating']['sem'],
            color='red',
            label='Mindfulness quality',
            capsize=5,
            marker='o')

ax1.errorbar(x_pos + 0.2, result['concentration_rating']['mean'],
            yerr=result['concentration_rating']['sem'],
            color='blue',
            label='Concentration quality',
            capsize=5,
            marker='o')

ax1.set_xticks(x_pos, labels=x_labels)
ax2.plot(x_pos, result['mindfulness_rating']['size'],
         color='green',
         label='Sample size',
         linestyle='--')

ax1.set_xlabel('Time since last masturbation (days)')
ax1.set_ylabel('Meditation Rating')
ax2.set_ylabel('Sample size')

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig('time_correlations.png')
