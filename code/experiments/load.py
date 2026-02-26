import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from load import get_meditations
from stats import log_likelihood, control_likelihood_ratio_statistic, llrt_pval

import os
import math
import numpy as np
import seaborn as sns
import pandas as pd
import scipy.stats as scistat
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_moods():
	mood=pd.read_csv('../../data/mood.csv')
	alarms=pd.to_datetime(pd.Series(mood['alarm']))
	dates=pd.to_datetime(pd.Series(mood['date']))
	mood=mood.assign(
		alarm=pd.DatetimeIndex(alarms.dt.tz_localize('CET', ambiguous='infer')).tz_convert(tz='UTC'),
		date=pd.DatetimeIndex(dates.dt.tz_localize('CET', ambiguous='infer')).tz_convert(tz='UTC')
	)

	return mood

def get_mental():
	mental=pd.read_csv('../../data/mental.csv')
	mental=mental.assign(
		datetime=pd.to_datetime(mental['datetime'], utc=True)
	)

	return mental

def get_ispom():
	ispomodoro=pd.read_csv('../../data/ispomodoro.csv')
	ispomodoro=ispomodoro.assign(
		date=pd.to_datetime(ispomodoro['date'], utc=True)
	)

	return ispomodoro

def get_islight():
	islight=pd.read_csv('../../data/islight.csv')
	islight=islight.assign(
		date=pd.to_datetime(islight['date'], utc=True)
	)

	return islight

def get_flashcards():
	flashcards=pd.read_csv('../../data/anki_reviews.csv')
	flashcards=flashcards.assign(
		id=pd.to_datetime(flashcards['id'], unit='ms', utc=True),
		cid=pd.to_datetime(flashcards['cid'], unit='ms', utc=True)
	)

	return flashcards

def get_masturbations():
	masturbations=pd.read_csv('../../data/masturbations.csv')
	masturbations.loc[masturbations['methods'].isna(),'methods']='n'
	masturbations=masturbations.assign(
		datetime=pd.to_datetime(masturbations['datetime'], utc=True, format='mixed', dayfirst=False)
	)

	return masturbations

def get_datasets_fn(experiment_fn, control_fn, intervention_fn):
	"""Return datasets.
	* `experiment_fn` receives a dataframe and returns the rows that
	were in that experiment.
	* `control_fn` receives a dataframe and returns the rows that
	were in the control group
	* `intervention_fn` receives a dataframe and returns the rows
	that were in the intervention group (usually this is just
	`not control_fn`)"""
	# Initialize the result dictionary
	result = {}

	# Get all the datasets
	meditations = get_meditations()
	mood = get_moods()
	mental = get_mental()
	flashcards = get_flashcards()

	# Process each dataset
	datasets = {
		'meditations': meditations,
		'mood': mood,
		'mental': mental,
		'flashcards': flashcards
	}

	for dataset_name, dataset in datasets.items():
		# Apply the experiment function to get the relevant rows
		experiment_data = experiment_fn(dataset)

		# Apply the control and intervention functions
		control_data = control_fn(experiment_data)
		intervention_data = intervention_fn(experiment_data)

		# Store the results in the dictionary
		result[dataset_name] = {
			'all': experiment_data,
			'control': control_data,
			'intervention': intervention_data
		}

	return result

def plot_datasets(datasets, title):
	# Set the overall layout
	sns.set(style="whitegrid")

	data_pairs = [
		('meditations', 'mindfulness', 'mindfulness', 'datetime'),
		('meditations', 'absorption', 'absorption', 'datetime'),
		('mental', 'productivity', 'productivity', 'datetime'),
		('mental', 'creativity', 'creativity', 'datetime'),
		('mental', 'subjective length', 'sublen', 'datetime'),
		('mental', 'meaning', 'meaning', 'datetime'),
		('mood', 'happiness', 'happy', 'datetime'),
		('mood', 'contentment', 'content', 'datetime'),
		('mood', 'relaxation', 'relaxed', 'datetime'),
		('mood', 'horniness', 'horny', 'datetime'),
		('flashcards', 'factor', 'factor', 'datetime'),
		('flashcards', 'interval', 'ivl', 'datetime'),
		('flashcards', 'ease', 'ease', 'datetime'),
		('flashcards', 'duration', 'time', 'datetime'),
	]

	n_data_pairs = 0
	n_plots_per_pair = 3

	for i, (dataset_name, label, y_variable, x_variable) in enumerate(data_pairs):
		if dataset_name not in datasets or \
		   datasets[dataset_name]['all'].size == 0 or \
		   datasets[dataset_name]['intervention'].size == 0 or \
		   datasets[dataset_name]['control'].size == 0:
			continue
		n_data_pairs+=1

	# Create a figure with a grid of subplots
	fig, axs = plt.subplots(n_data_pairs, n_plots_per_pair, figsize=(15, 4 * n_data_pairs))

	j=0

	for dataset_name, label, y_variable, x_variable in data_pairs:
		if dataset_name not in datasets or \
		   datasets[dataset_name]['all'].size == 0 or \
		   datasets[dataset_name]['intervention'].size == 0 or \
		   datasets[dataset_name]['control'].size == 0:
			continue

		substance_data = datasets[dataset_name]['intervention']
		placebo_data = datasets[dataset_name]['control']

		print(dataset_name, label)

		for subplot_index in range(0, 2):
			axs[j, subplot_index].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # Change format to Month-Day

		# Scatter plot
		sns.scatterplot(ax=axs[j, 0], x=x_variable, y=y_variable, data=substance_data, color='blue', label='Intervention')
		sns.scatterplot(ax=axs[j, 0], x=x_variable, y=y_variable, data=placebo_data, color='red', label='Placebo')
		axs[j, 0].set_title(f'Scatter Plot of {label}')
		axs[j, 0].set_xlabel(x_variable)
		axs[j, 0].set_ylabel(y_variable)

		# Line plot
		sns.lineplot(ax=axs[j, 1], x=x_variable, y=y_variable, data=substance_data, color='blue', label='Intervention')
		sns.lineplot(ax=axs[j, 1], x=x_variable, y=y_variable, data=placebo_data, color='red', label='Placebo')
		axs[j, 1].set_title(f'Line Plot of {label}')
		axs[j, 1].set_xlabel(x_variable)
		axs[j, 1].set_ylabel(y_variable)

		# Histogram
		sns.histplot(ax=axs[j, 2], data=substance_data, x=y_variable, color='blue', label='Intervention', kde=True, alpha=0.6)
		sns.histplot(ax=axs[j, 2], data=placebo_data, x=y_variable, color='red', label='Placebo', kde=True, alpha=0.6)
		axs[j, 2].set_title(f'Histogram of {label}')
		axs[j, 2].set_xlabel(y_variable)
		axs[j, 2].set_ylabel('Frequency')
		j+=1

	plt.tight_layout()

	plt.savefig(f'{title}_results.png')

def get_datasets(experiment, substance, placebo):
	# Load substances data
	substances = pd.read_csv('../../data/substances.csv').copy()
	expa = substances.loc[substances['experiment'] == experiment].copy()
	expa['datetime'] = pd.to_datetime(expa['datetime'], utc=True)
	expa = expa.sort_values('datetime')

	def experiment_fn(df):
		if 'meditation_start' in df.columns:
			df = df.sort_values('meditation_start')
			df = pd.merge_asof(expa, df, left_on='datetime', right_on='meditation_start', direction='forward')
			df = df.rename(columns={'mindfulness_rating': 'mindfulness', 'concentration_rating': 'absorption'})
		elif 'alarm' in df.columns:
			df = expa.join(df, how='cross')
			df = df.loc[(df['alarm'] - df['datetime'] < pd.Timedelta('14h')) & (df['alarm'] - df['datetime'] > pd.Timedelta('0h'))]
			df = df.loc[df['relaxed'].notna()]
		elif 'productivity' in df.columns:
			df = df.sort_values('datetime')
			df = pd.merge_asof(expa, df, left_on='datetime', right_on='datetime', direction='forward')
		elif 'id' in df.columns:
			df = df.loc[(df['id'] > expa['datetime'].min()) & (df['id'] < expa['datetime'].max() + pd.Timedelta('14h'))]
			df = expa.join(df, how='cross', rsuffix='r')
			df = df.loc[(df['idr'] - df['datetime'] < pd.Timedelta('14h')) & (df['idr'] - df['datetime'] > pd.Timedelta('0h'))]
			mask = df['ivl'] > 0
			df = df.assign(ivl=df['ivl'].where(~mask, -df['ivl'] / 86400))
		return df

	def control_fn(df):
		return df[df['substance'] == placebo]

	def intervention_fn(df):
		return df[df['substance'] == substance]

	return get_datasets_fn(experiment_fn, control_fn, intervention_fn)

def get_datasets_pom():
	# Load substances data
	ispom=get_ispom()

	def experiment_fn(df):
		if 'meditation_start' in df.columns:
			df = df.sort_values('meditation_start')
			df = pd.merge_asof(ispom, df, left_on='date', right_on='meditation_start', direction='forward', tolerance=pd.Timedelta('14h'))
			df = df.rename(columns={'mindfulness_rating': 'mindfulness', 'concentration_rating': 'absorption', 'date': 'datetime'})
			df=df[df['_id'].notna()]
		elif 'alarm' in df.columns:
			df = ispom.join(df, how='cross', rsuffix='_r')
			df = df.loc[(df['alarm'] - df['date'] < pd.Timedelta('20h')) & (df['alarm'] - df['date'] > pd.Timedelta('0h'))]
			df = df.loc[df['relaxed'].notna()]
			df = df.rename(columns={'date': 'datetime'})
		elif 'productivity' in df.columns:
			df = df.sort_values('datetime')
			df = pd.merge_asof(ispom, df, left_on='date', right_on='datetime', direction='forward', tolerance=pd.Timedelta('24h'))
		elif 'id' in df.columns:
			df = df.loc[(df['id'] > ispom['date'].min()) & (df['id'] < ispom['date'].max() + pd.Timedelta('14h'))]
			df = ispom.join(df, how='cross')
			df = df.loc[(df['id'] - df['date'] < pd.Timedelta('14h')) & (df['id'] - df['date'] > pd.Timedelta('0h'))]
			mask = df['ivl'] > 0
			df = df.assign(ivl=df['ivl'].where(~mask, -df['ivl'] / 86400))
			df = df.rename(columns={'date': 'datetime'})
		return df

	def control_fn(df):
		return df[df['ispomodoro'] == 0]

	def intervention_fn(df):
		return df[df['ispomodoro'] == 1]

	return get_datasets_fn(experiment_fn, control_fn, intervention_fn)

def get_datasets_light():
	# Load lumenator data
	islight=get_islight()

	def experiment_fn(df):
		if 'meditation_start' in df.columns:
			df = df.sort_values('meditation_start')
			df = pd.merge_asof(islight, df, left_on='date', right_on='meditation_start', direction='forward', tolerance=pd.Timedelta('14h'))
			df = df.rename(columns={'mindfulness_rating': 'mindfulness', 'concentration_rating': 'absorption', 'date': 'datetime'})
			df=df[df['_id'].notna()]
		elif 'alarm' in df.columns:
			df = islight.join(df, how='cross', rsuffix='_r')
			df = df.loc[(df['alarm'] - df['date'] < pd.Timedelta('20h')) & (df['alarm'] - df['date'] > pd.Timedelta('0h'))]
			df = df.loc[df['relaxed'].notna()]
			df = df.rename(columns={'date': 'datetime'})
		elif 'productivity' in df.columns:
			df = df.sort_values('datetime')
			df = pd.merge_asof(islight, df, left_on='date', right_on='datetime', direction='forward', tolerance=pd.Timedelta('24h'))
		elif 'id' in df.columns:
			df = df.loc[(df['id'] > islight['date'].min()) & (df['id'] < islight['date'].max() + pd.Timedelta('14h'))]
			df = islight.join(df, how='cross')
			df = df.loc[(df['id'] - df['date'] < pd.Timedelta('14h')) & (df['id'] - df['date'] > pd.Timedelta('0h'))]
			mask = df['ivl'] > 0
			df = df.assign(ivl=df['ivl'].where(~mask, -df['ivl'] / 86400))
			df = df.rename(columns={'date': 'datetime'})
		return df

	def control_fn(df):
		return df[df['islight'] == 0]

	def intervention_fn(df):
		return df[df['islight'] == 1]

	return get_datasets_fn(experiment_fn, control_fn, intervention_fn)

def analyze(datasets):
	result = pd.DataFrame(index=['d', 'λ', 'p', 'dσ', 'k'])

	# Define the correct column order
	column_order = ['absorption', 'mindfulness',
			'productivity', 'creativity', 'sublen', 'meaning',
			'happy', 'content', 'relaxed', 'horny',
			'ease', 'factor', 'ivl', 'time']

	for dataset_name, data in datasets.items():
		all_data = data['all']
		intervention_data = data['intervention']
		control_data = data['control']

		if dataset_name == 'meditations':
			columns = ['absorption', 'mindfulness']
		elif dataset_name == 'mental':
			columns = ['productivity', 'creativity', 'sublen', 'meaning']
		elif dataset_name == 'mood':
			columns = ['happy', 'content', 'relaxed', 'horny']
		elif dataset_name == 'flashcards':
			columns = ['ease', 'factor', 'ivl', 'time']
		else:
			continue

		for col in columns:
			if col not in all_data.columns or intervention_data.empty or control_data.empty:
				result.loc['d', col] = np.nan
				result.loc['λ', col] = np.nan
				result.loc['p', col] = np.nan
				result.loc['dσ', col] = np.nan
				result.loc['k', col] = np.nan
				result.loc['control_k', col] = np.nan
				result.loc['intervention_k', col] = np.nan
				result.loc['m', col] = np.nan
				result.loc['control_m', col] = np.nan
				result.loc['intervention_m', col] = np.nan

				continue

			# Calculate d (Cohen's d)
			d = (intervention_data[col].mean() - control_data[col].mean()) / all_data[col].std()
			result.loc['d', col] = d

			# Calculate λ (likelihood ratio test statistic)
			lambda_value = control_likelihood_ratio_statistic(intervention_data[col], control_data[col])
			result.loc['λ', col] = lambda_value

			# Calculate p-value
			p_value = llrt_pval(lambda_value)
			result.loc['p', col] = p_value

			# Calculate dσ (difference in standard deviations)
			d_sigma = intervention_data[col].std() - control_data[col].std()
			result.loc['dσ', col] = d_sigma

			result.loc['k', col] = all_data[col].count()
			result.loc['control_k', col] = control_data[col].dropna().count()
			result.loc['intervention_k', col] = intervention_data[col].dropna().count()
			result.loc['m', col] = all_data[[col, 'datetime']].dropna()['datetime'].dt.date.unique().size
			result.loc['control_m', col] = control_data[[col, 'datetime']].dropna()['datetime'].dt.date.unique().size
			result.loc['intervention_m', col] = intervention_data[[col, 'datetime']].dropna()['datetime'].dt.date.unique().size

	result = result.reindex(columns=column_order)

	result.loc['k'] = result.loc['k'].astype('Int64')

	return result

def logscore(o,p):
        return np.mean(o*np.log(p)+(np.ones_like(o)-o)*np.log(np.ones_like(p)-p))
