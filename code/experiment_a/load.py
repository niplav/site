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

def analyze(experiment, substance, placebo):
	substances=pd.read_csv('../..//data/substances.csv')

	expa=substances.loc[substances['experiment']==experiment].copy()
	expa['datetime']=pd.to_datetime(expa['datetime'], utc=True)

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

	flashcards=pd.read_csv('../../data/anki_reviews.csv')
	flashcards['id']=pd.to_datetime(flashcards['id'], unit='ms', utc=True)
	flashcards['cid']=pd.to_datetime(flashcards['cid'], unit='ms', utc=True)

	meditations.sort_values("meditation_start", inplace=True)
	meditations_a=pd.merge_asof(expa, meditations, left_on='datetime', right_on='meditation_start', direction='forward')
	caffeine_mindfulness=meditations_a.loc[meditations_a['substance']==substance]['mindfulness_rating']
	placebo_mindfulness=meditations_a.loc[meditations_a['substance']==placebo]['mindfulness_rating']
	caffeine_concentration=meditations_a.loc[meditations_a['substance']==substance]['concentration_rating']
	placebo_concentration=meditations_a.loc[meditations_a['substance']==placebo]['concentration_rating']

	prod_a=pd.merge_asof(expa, productivity, left_on='datetime', right_on='datetime', direction='forward')
	creat_a=pd.merge_asof(expa, creativity, left_on='datetime', right_on='datetime', direction='forward')
	caffeine_productivity=prod_a.loc[meditations_a['substance']==substance]['productivity']
	placebo_productivity=prod_a.loc[meditations_a['substance']==placebo]['productivity']
	caffeine_creativity=creat_a.loc[meditations_a['substance']==substance]['creativity']
	placebo_creativity=creat_a.loc[meditations_a['substance']==placebo]['creativity']

	mood=expa.join(mood, how='cross')
	mood=mood.loc[(mood['alarm']-mood['datetime']<pd.Timedelta('10h'))&(mood['alarm']-mood['datetime']>pd.Timedelta('0h'))]
	mood=mood.loc[mood['relaxed'].notna()]

	flashcards_a=flashcards.loc[(flashcards['id']>expa['datetime'].min()) & (flashcards['id']<expa['datetime'].max()+pd.Timedelta('10h'))]
	flashcards_a=expa.join(flashcards_a, how='cross', rsuffix='r')
	flashcards_a=flashcards_a.loc[(flashcards_a['idr']-flashcards_a['datetime']<pd.Timedelta('10h'))&(flashcards_a['idr']-flashcards_a['datetime']>pd.Timedelta('0h'))]

	placebo_mood=mood.loc[mood['substance']==placebo]
	caffeine_mood=mood.loc[mood['substance']==substance]

	result=pd.DataFrame()
	result=result.reindex(columns=['absorption', 'mindfulness', 'productivity', 'creativity', 'happy', 'content', 'relaxed', 'horny'], index=['d', 'λ', 'p', 'dσ'])

	result.loc['d','absorption']=(caffeine_concentration.mean()-placebo_concentration.mean())/meditations['concentration_rating'].std()
	result.loc['d','mindfulness']=(caffeine_mindfulness.mean()-placebo_mindfulness.mean())/meditations['mindfulness_rating'].std()
	result.loc['dσ', 'absorption']=caffeine_concentration.std()-placebo_concentration.std()
	result.loc['dσ', 'mindfulness']=caffeine_mindfulness.std()-placebo_mindfulness.std()

	result.loc['d','productivity']=(caffeine_productivity.mean()-placebo_productivity.mean())/prod_a['productivity'].std()
	result.loc['d','creativity']=(caffeine_creativity.mean()-placebo_creativity.mean())/creat_a['creativity'].std()
	result.loc['dσ', 'productivity']=caffeine_productivity.std()-placebo_productivity.std()
	result.loc['dσ', 'creativity']=caffeine_creativity.std()-placebo_creativity.std()

	mood_ds=(caffeine_mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['mean',:]-placebo_mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['mean',:])/mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['std',:]
	result.loc['d',['happy', 'content', 'relaxed', 'horny']]=mood_ds

	mood_d_sigmas=caffeine_mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['std',:]-placebo_mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['std',:]
	result.loc['dσ',['happy', 'content', 'relaxed', 'horny']]=mood_d_sigmas

	result.loc['λ', 'absorption']=likelihood_ratio_test(placebo_likelihood_ratio(caffeine_concentration, placebo_concentration))
	result.loc['λ', 'mindfulness']=likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mindfulness, placebo_mindfulness))
	result.loc['λ', 'productivity']=likelihood_ratio_test(placebo_likelihood_ratio(caffeine_productivity, placebo_productivity))
	result.loc['λ', 'creativity']=likelihood_ratio_test(placebo_likelihood_ratio(caffeine_creativity, placebo_creativity))

	result.loc['λ', 'happy']=likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mood['happy'], placebo_mood['happy']))
	result.loc['λ', 'content']=likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mood['content'], placebo_mood['content']))
	result.loc['λ', 'relaxed']=likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mood['relaxed'], placebo_mood['relaxed']))
	result.loc['λ', 'horny']=likelihood_ratio_test(placebo_likelihood_ratio(caffeine_mood['horny'], placebo_mood['horny']))

	result.loc['p',:]=llrt_pval(result.loc['λ',:])

	return result
