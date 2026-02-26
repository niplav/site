import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from load import get_sleep
from stats import control_likelihood_ratio_statistic, llrt_pval

import numpy as np
import pandas as pd
import scipy.stats as sps
import matplotlib.pyplot as plt

sleep=get_sleep()
first_sleep=sleep['date'].min()

substances=pd.read_csv('../../data/substances.csv')
substances=substances.assign(datetime=pd.to_datetime(substances['datetime'], utc=True))
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

metrics=[
	('minutes_asleep', 'Minutes asleep'),
	('efficiency', 'Sleep efficiency (%)'),
	('deep_minutes', 'Deep sleep (min)'),
	('rem_minutes', 'REM sleep (min)'),
	('time_in_bed', 'Time in bed (min)'),
]

mel=non_nap_melatonin_sleep
non=non_nap_non_melatonin_sleep

fig, axes=plt.subplots(2, 3, figsize=(14, 8))
fig.suptitle('Melatonin vs no melatonin — sleep metrics', fontsize=13)

for ax, (col, label) in zip(axes.flat, metrics):
	m=mel[col].dropna()
	n=non[col].dropna()

	lam=control_likelihood_ratio_statistic(m, n)
	p=llrt_pval(lam)
	cohen_d=(m.mean()-n.mean())/pd.concat([m,n]).std()

	ax.hist(n, bins=25, alpha=0.5, color='steelblue', label=f'no mel (n={len(n)})', density=True)
	ax.hist(m, bins=25, alpha=0.5, color='tomato', label=f'mel (n={len(m)})', density=True)
	ax.axvline(n.mean(), color='steelblue', linestyle='--', linewidth=1)
	ax.axvline(m.mean(), color='tomato', linestyle='--', linewidth=1)
	ax.set_title(label)
	ax.set_xlabel(f'd={cohen_d:.2f}, p={p:.3f}')
	ax.legend(fontsize=7)

plt.tight_layout()
plt.savefig('melatonin_sleep.png', dpi=150)
plt.close()
