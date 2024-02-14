import math
import numpy as np
import pandas as pd
import scipy.stats as scistat
import matplotlib.pyplot as plt

def normal_likelihood(data, mu, std):
	data_probs=scistat.norm.pdf(data, loc=mu, scale=std)
	return np.multiply.reduce(data_probs, where=~np.isnan(data_probs))

def placebo_likelihood_ratio(active, placebo):
	placebo_mle_lh=normal_likelihood(active, placebo.mean(), placebo.std())
	active_mle_lh=normal_likelihood(active, active.mean(), active.std())
	if active_mle_lh==0:
		return 0
	return active_mle_lh/placebo_mle_lh

def likelihood_ratio_test(lr):
	if lr==0:
		return math.inf
	return 2*np.log(lr)

def llrt_pval(lmbda, df=2):
	return scistat.chi2.cdf(df, lmbda)

def get_meditations():
	meditations=pd.read_csv('../../data/meditations.csv')
	meditations['meditation_start']=pd.to_datetime(meditations['meditation_start'], unit='ms', utc=True)
	meditations['meditation_end']=pd.to_datetime(meditations['meditation_end'], unit='ms', utc=True)

	return meditations

def get_moods():
	mood=pd.read_csv('../../data/mood.csv')
	alarms=pd.to_datetime(pd.Series(mood['alarm']))
	mood['alarm']=pd.DatetimeIndex(alarms.dt.tz_localize('CET', ambiguous='infer')).tz_convert(tz='UTC')
	dates=pd.to_datetime(pd.Series(mood['date']))
	mood['date']=pd.DatetimeIndex(dates.dt.tz_localize('CET', ambiguous='infer')).tz_convert(tz='UTC')

	return mood

def get_mental():
	mental=pd.read_csv('../../data/mental.csv')
	mental['datetime']=pd.to_datetime(mental['datetime'], utc=True)

	return mental

def get_flashcards():
	flashcards=pd.read_csv('../../data/anki_reviews.csv')
	flashcards['id']=pd.to_datetime(flashcards['id'], unit='ms', utc=True)
	flashcards['cid']=pd.to_datetime(flashcards['cid'], unit='ms', utc=True)

	return flashcards

def get_masturbations():
	masturbations=pd.read_csv('../../data/masturbations.csv')
	masturbations.loc[masturbations['methods'].isna(),'methods']='n'
	masturbations['datetime']=pd.to_datetime(masturbations['datetime'], utc=True, format='mixed', dayfirst=False)

	return masturbations

def get_datasets(experiment, substance, placebo):
	substances=pd.read_csv('../../data/substances.csv')

	expa=substances.loc[substances['experiment']==experiment].copy()
	expa['datetime']=pd.to_datetime(expa['datetime'], utc=True)

	meditations=get_meditations()
	mood=get_moods()
	mental=get_mental()
	flashcards=get_flashcards()

	creativity=mental[['datetime', 'creativity']]
	productivity=mental[['datetime', 'productivity']]
	sublen=mental[['datetime', 'sublen']]

	meditations.sort_values("meditation_start", inplace=True)
	meditations=pd.merge_asof(expa, meditations, left_on='datetime', right_on='meditation_start', direction='forward')
	meditations=meditations.rename(columns={'mindfulness_rating': 'mindfulness', 'concentration_rating': 'absorption'})
	placebo_meditations=meditations.loc[meditations['substance']==placebo]
	substance_meditations=meditations.loc[meditations['substance']==substance]

	mental=pd.merge_asof(expa, mental, left_on='datetime', right_on='datetime', direction='forward')
	placebo_mental=mental.loc[mental['substance']==placebo]
	substance_mental=mental.loc[mental['substance']==substance]

	mood=expa.join(mood, how='cross')
	mood=mood.loc[(mood['alarm']-mood['datetime']<pd.Timedelta('10h'))&(mood['alarm']-mood['datetime']>pd.Timedelta('0h'))]
	mood=mood.loc[mood['relaxed'].notna()]

	flashcards_a=flashcards.loc[(flashcards['id']>expa['datetime'].min()) & (flashcards['id']<expa['datetime'].max()+pd.Timedelta('10h'))]
	flashcards_a=expa.join(flashcards_a, how='cross', rsuffix='r')
	flashcards_a=flashcards_a.loc[(flashcards_a['idr']-flashcards_a['datetime']<pd.Timedelta('10h'))&(flashcards_a['idr']-flashcards_a['datetime']>pd.Timedelta('0h'))]
	flashcards_a.loc[flashcards_a['ivl']>0,'ivl']=-flashcards_a.loc[flashcards_a['ivl']>0,'ivl']/86400

	placebo_mood=mood.loc[mood['substance']==placebo]
	substance_mood=mood.loc[mood['substance']==substance]

	placebo_flashcards=flashcards_a.loc[flashcards_a['substance']==placebo]
	substance_flashcards=flashcards_a.loc[flashcards_a['substance']==substance]

	return meditations, substance_meditations, placebo_meditations, mental, substance_mental, placebo_mental, mood, placebo_mood, substance_mood, flashcards, placebo_flashcards, substance_flashcards

def plot_experiment(experiment, substance, placebo):
	meditation, substance_meditations, placebo_meditations, mental, substance_mental, placebo_mental, mood, placebo_mood, substance_mood, flashcards, placebo_flashcards, substance_flashcards=get_datasets(experiment, substance, placebo)

	fig=plt.figure(figsize=(8,8))
	plt.bar(placebo_meditations.index, placebo_meditations['absorption'], color='red')
	plt.bar(substance_meditations.index, substance_meditations['absorption'], color='blue')
	return

def analyze(experiment, substance, placebo):
	meditation, substance_meditations, placebo_meditations, mental, substance_mental, placebo_mental, mood, placebo_mood, substance_mood, flashcards, placebo_flashcards, substance_flashcards=get_datasets(experiment, substance, placebo)

	result=pd.DataFrame()
	result=result.reindex(columns=['absorption', 'mindfulness', 'productivity', 'creativity', 'sublen', 'happy', 'content', 'relaxed', 'horny', 'ease', 'factor', 'ivl', 'time'], index=['d', 'λ', 'p', 'dσ'])

	meditation_ds=(substance_meditations[['mindfulness', 'absorption']].describe().loc['mean',:]-placebo_meditations[['mindfulness', 'absorption']].describe().loc['mean',:])/meditation[['mindfulness', 'absorption']].describe().loc['std',:]
	result.loc['d', ['mindfulness', 'absorption']]=meditation_ds

	meditation_d_sigmas=substance_meditations[['mindfulness', 'absorption']].describe().loc['std',:]-placebo_meditations[['mindfulness', 'absorption']].describe().loc['std',:]
	result.loc['dσ',['mindfulness', 'absorption']]=meditation_d_sigmas

	mental_ds=(substance_mental[['productivity', 'creativity', 'sublen']].describe().loc['mean',:]-placebo_mental[['productivity', 'creativity', 'sublen']].describe().loc['mean',:])/mental[['productivity', 'creativity', 'sublen']].describe().loc['std',:]
	result.loc['d', ['productivity', 'creativity', 'sublen']]=mental_ds

	mental_d_sigmas=substance_mental[['productivity', 'creativity', 'sublen']].describe().loc['std',:]-placebo_mental[['productivity', 'creativity', 'sublen']].describe().loc['std',:]
	result.loc['dσ',['productivity', 'creativity', 'sublen']]=mental_d_sigmas

	mood_ds=(substance_mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['mean',:]-placebo_mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['mean',:])/mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['std',:]
	result.loc['d',['happy', 'content', 'relaxed', 'horny']]=mood_ds

	mood_d_sigmas=substance_mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['std',:]-placebo_mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['std',:]
	result.loc['dσ',['happy', 'content', 'relaxed', 'horny']]=mood_d_sigmas

	flashcards_ds=(substance_flashcards[['ease', 'factor', 'ivl', 'time']].describe().loc['mean',:]-placebo_flashcards[['ease', 'factor', 'ivl', 'time']].describe().loc['mean',:])/flashcards[['ease', 'factor', 'ivl', 'time']].describe().loc['std',:]
	result.loc['d',['ease', 'factor', 'ivl', 'time']]=flashcards_ds

	flashcards_d_sigmas=substance_flashcards[['ease', 'factor', 'ivl', 'time']].describe().loc['std',:]-placebo_flashcards[['ease', 'factor', 'ivl', 'time']].describe().loc['std',:]
	result.loc['dσ',['ease', 'factor', 'ivl', 'time']]=flashcards_d_sigmas

	result.loc['λ', 'absorption']=likelihood_ratio_test(placebo_likelihood_ratio(substance_meditations['absorption'], placebo_meditations['absorption']))
	result.loc['λ', 'mindfulness']=likelihood_ratio_test(placebo_likelihood_ratio(substance_meditations['mindfulness'], placebo_meditations['mindfulness']))
	result.loc['λ', 'productivity']=likelihood_ratio_test(placebo_likelihood_ratio(substance_mental['productivity'], placebo_mental['productivity']))
	result.loc['λ', 'creativity']=likelihood_ratio_test(placebo_likelihood_ratio(substance_mental['creativity'], placebo_mental['creativity']))
	result.loc['λ', 'sublen']=likelihood_ratio_test(placebo_likelihood_ratio(substance_mental['sublen'], placebo_mental['sublen']))

	result.loc['λ', 'happy']=likelihood_ratio_test(placebo_likelihood_ratio(substance_mood['happy'], placebo_mood['happy']))
	result.loc['λ', 'content']=likelihood_ratio_test(placebo_likelihood_ratio(substance_mood['content'], placebo_mood['content']))
	result.loc['λ', 'relaxed']=likelihood_ratio_test(placebo_likelihood_ratio(substance_mood['relaxed'], placebo_mood['relaxed']))
	result.loc['λ', 'horny']=likelihood_ratio_test(placebo_likelihood_ratio(substance_mood['horny'], placebo_mood['horny']))

	result.loc['λ', 'ease']=likelihood_ratio_test(placebo_likelihood_ratio(substance_flashcards['ease'], placebo_flashcards['ease']))
	result.loc['λ', 'factor']=likelihood_ratio_test(placebo_likelihood_ratio(substance_flashcards['factor'], placebo_flashcards['factor']))
	result.loc['λ', 'ivl']=likelihood_ratio_test(placebo_likelihood_ratio(substance_flashcards['ivl'], placebo_flashcards['ivl']))
	result.loc['λ', 'time']=likelihood_ratio_test(placebo_likelihood_ratio(substance_flashcards['time'], placebo_flashcards['time']))

	result.loc['p',:]=llrt_pval(result.loc['λ',:])

	return result
