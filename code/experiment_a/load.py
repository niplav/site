import math
import numpy as np
import pandas as pd
import scipy.stats as scistat

def normal_likelihood(data, mu, std):
	return np.product(scistat.norm.pdf(data, loc=mu, scale=std))

def placebo_likelihood_ratio(active, placebo):
	placebo_mle_lh=normal_likelihood(active, placebo.mean(), placebo.std())
	active_mle_lh=normal_likelihood(active, active.mean(), active.std())
	return active_mle_lh/placebo_mle_lh

def likelihood_ratio_test(lr):
	return 2*np.log(lr)

def llrt_pval(lmbda, df=2):
	return scistat.chi2.cdf(df, lmbda)

substances=pd.read_csv('../..//data/substances.csv')

meditations=pd.read_csv('../../data/meditations.csv')
meditations['meditation_start']=pd.to_datetime(meditations['meditation_start'], unit='ms', utc=True)
meditations['meditation_end']=pd.to_datetime(meditations['meditation_end'], unit='ms', utc=True)

mood=pd.read_csv('../../data/mood.csv')
alarms=pd.to_datetime(pd.Series(mood['alarm']), format='mixed')
mood['alarm']=pd.DatetimeIndex(alarms.dt.tz_localize('CET', ambiguous='infer')).tz_convert(tz='UTC')
dates=pd.to_datetime(pd.Series(mood['date']), format='mixed')
mood['date']=pd.DatetimeIndex(dates.dt.tz_localize('CET', ambiguous='infer')).tz_convert(tz='UTC')

creativity=pd.read_csv('../../data/creativity.csv')
creativity['datetime']=pd.to_datetime(creativity['datetime'], utc=True)

productivity=pd.read_csv('../../data/productivity.csv')
productivity['datetime']=pd.to_datetime(productivity['datetime'], utc=True)

expa=substances.loc[substances['experiment']=='A'].copy()
expa['datetime']=pd.to_datetime(expa['datetime'], utc=True)

meditations.sort_values("meditation_start", inplace=True)
meditations_a=pd.merge_asof(expa, meditations, left_on='datetime', right_on='meditation_start', direction='forward')
caffeine_mindfulness=meditations_a.loc[meditations_a['substance']=='caffeine']['mindfulness_rating']
placebo_mindfulness=meditations_a.loc[meditations_a['substance']=='sugar']['mindfulness_rating']
caffeine_concentration=meditations_a.loc[meditations_a['substance']=='caffeine']['concentration_rating']
placebo_concentration=meditations_a.loc[meditations_a['substance']=='sugar']['concentration_rating']

prod_a=pd.merge_asof(expa, productivity, left_on='datetime', right_on='datetime', direction='forward')
creat_a=pd.merge_asof(expa, creativity, left_on='datetime', right_on='datetime', direction='forward')
caffeine_productivity=prod_a.loc[meditations_a['substance']=='caffeine']['productivity']
placebo_productivity=prod_a.loc[meditations_a['substance']=='sugar']['productivity']
caffeine_creativity=creat_a.loc[meditations_a['substance']=='caffeine']['creativity']
placebo_creativity=creat_a.loc[meditations_a['substance']=='sugar']['creativity']

mood=expa.join(mood, how='cross')
mood=mood.loc[(mood['alarm']-mood['datetime']<pd.Timedelta('10h'))&(mood['alarm']-mood['datetime']>pd.Timedelta('0h'))]
mood=mood.loc[mood['relaxed'].notna()]

placebo_mood=mood.loc[mood['substance']=='sugar']
caffeine_mood=mood.loc[mood['substance']=='caffeine']
