import math
import numpy as np
import pandas as pd
import scipy.stats as scistat

def normal_likelihood(data, mu, std):
	return np.product(scistat.norm.pdf(data, loc=mu, scale=std))

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

def analyze(experiment, substance, placebo):
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
	meditations_a=pd.merge_asof(expa, meditations, left_on='datetime', right_on='meditation_start', direction='forward')
	substance_mindfulness=meditations_a.loc[meditations_a['substance']==substance]['mindfulness_rating']
	placebo_mindfulness=meditations_a.loc[meditations_a['substance']==placebo]['mindfulness_rating']
	substance_concentration=meditations_a.loc[meditations_a['substance']==substance]['concentration_rating']
	placebo_concentration=meditations_a.loc[meditations_a['substance']==placebo]['concentration_rating']

	prod_a=pd.merge_asof(expa, productivity, left_on='datetime', right_on='datetime', direction='forward')
	creat_a=pd.merge_asof(expa, creativity, left_on='datetime', right_on='datetime', direction='forward')
	sublen_a=pd.merge_asof(expa, sublen, left_on='datetime', right_on='datetime', direction='forward')
	substance_productivity=prod_a.loc[prod_a['substance']==substance]['productivity']
	placebo_productivity=prod_a.loc[prod_a['substance']==placebo]['productivity']
	substance_creativity=creat_a.loc[creat_a['substance']==substance]['creativity']
	placebo_creativity=creat_a.loc[creat_a['substance']==placebo]['creativity']
	substance_sublen=sublen_a.loc[sublen_a['substance']==substance]['sublen']
	placebo_sublen=sublen_a.loc[sublen_a['substance']==placebo]['sublen']

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

	result=pd.DataFrame()
	result=result.reindex(columns=['absorption', 'mindfulness', 'productivity', 'creativity', 'sublen', 'happy', 'content', 'relaxed', 'horny', 'ease', 'factor', 'ivl', 'time'], index=['d', 'λ', 'p', 'dσ'])

	result.loc['d','absorption']=(substance_concentration.mean()-placebo_concentration.mean())/meditations['concentration_rating'].std()
	result.loc['d','mindfulness']=(substance_mindfulness.mean()-placebo_mindfulness.mean())/meditations['mindfulness_rating'].std()
	result.loc['dσ', 'absorption']=substance_concentration.std()-placebo_concentration.std()
	result.loc['dσ', 'mindfulness']=substance_mindfulness.std()-placebo_mindfulness.std()

	result.loc['d','productivity']=(substance_productivity.mean()-placebo_productivity.mean())/prod_a['productivity'].std()
	result.loc['d','creativity']=(substance_creativity.mean()-placebo_creativity.mean())/creat_a['creativity'].std()
	result.loc['d','sublen']=(substance_sublen.mean()-placebo_sublen.mean())/sublen_a['sublen'].std()

	result.loc['dσ', 'productivity']=substance_productivity.std()-placebo_productivity.std()
	result.loc['dσ', 'creativity']=substance_creativity.std()-placebo_creativity.std()
	result.loc['dσ', 'sublen']=substance_sublen.std()-placebo_sublen.std()

	mood_ds=(substance_mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['mean',:]-placebo_mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['mean',:])/mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['std',:]
	result.loc['d',['happy', 'content', 'relaxed', 'horny']]=mood_ds

	mood_d_sigmas=substance_mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['std',:]-placebo_mood[['happy', 'content', 'relaxed', 'horny']].describe().loc['std',:]
	result.loc['dσ',['happy', 'content', 'relaxed', 'horny']]=mood_d_sigmas

	flashcards_ds=(substance_flashcards[['ease', 'factor', 'ivl', 'time']].describe().loc['mean',:]-placebo_flashcards[['ease', 'factor', 'ivl', 'time']].describe().loc['mean',:])/flashcards[['ease', 'factor', 'ivl', 'time']].describe().loc['std',:]
	result.loc['d',['ease', 'factor', 'ivl', 'time']]=flashcards_ds

	flashcards_d_sigmas=substance_flashcards[['ease', 'factor', 'ivl', 'time']].describe().loc['std',:]-placebo_flashcards[['ease', 'factor', 'ivl', 'time']].describe().loc['std',:]
	result.loc['dσ',['ease', 'factor', 'ivl', 'time']]=flashcards_d_sigmas

	result.loc['λ', 'absorption']=likelihood_ratio_test(placebo_likelihood_ratio(substance_concentration, placebo_concentration))
	result.loc['λ', 'mindfulness']=likelihood_ratio_test(placebo_likelihood_ratio(substance_mindfulness, placebo_mindfulness))
	result.loc['λ', 'productivity']=likelihood_ratio_test(placebo_likelihood_ratio(substance_productivity, placebo_productivity))
	result.loc['λ', 'creativity']=likelihood_ratio_test(placebo_likelihood_ratio(substance_creativity, placebo_creativity))
	result.loc['λ', 'sublen']=likelihood_ratio_test(placebo_likelihood_ratio(substance_sublen, placebo_sublen))

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
