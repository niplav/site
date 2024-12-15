import time
import math
import numpy as np
import squigglepy as sq
import matplotlib.pyplot as plt

from squigglepy import bayes

SAMPLE_SIZE=1000000
CURYEAR=time.localtime().tm_year+1

extinction_val=0
magic_val=sq.norm(mean=1, sd=0.1)

timeline_us_race=sq.mixture([sq.norm(mean=2032, sd=5, lclip=CURYEAR), sq.norm(mean=2060, sd=20, lclip=CURYEAR)], [0.7, 0.3])

def timeline_prc_race_fn(us_year):
	timeline_stddev=0.1*((us_year-CURYEAR)+1)
	timeline=sq.norm(mean=us_year+1, sd=timeline_stddev, lclip=CURYEAR)
	return sq.sample(timeline)

def define_event_race():
	us_tai_year=sq.sample(timeline_us_race, lclip=CURYEAR)
	return({'prc': timeline_prc_race_fn(us_tai_year), 'us': us_tai_year})

timeline_race_samples=np.array(bayes.bayesnet(define_event_race, find=lambda e: [e['us'], e['prc']], reduce_fn=lambda d: d, n=SAMPLE_SIZE))
timeline_race_samples=timeline_race_samples[(timeline_race_samples>CURYEAR).all(axis=1)].T # Filter for years after this one

FILTERED_SIZE=timeline_race_samples.shape[1]

timeline_prc_nonrace=sq.mixture([sq.norm(mean=2040, sd=5, lclip=CURYEAR), sq.norm(mean=2065, sd=20, lclip=CURYEAR)], [0.7, 0.3])

timeline_magic=sq.mixture([sq.norm(mean=2055, sd=5, lclip=CURYEAR), sq.norm(mean=2080, sd=20, lclip=CURYEAR)], [0.7, 0.3])

pdoom_us_race=sq.beta(a=2, b=18)
pdoom_prc_race=sq.beta(a=1.5, b=6)
pdoom_prc_nonrace=sq.beta(a=1.06, b=6)
pdoom_magic=sq.beta(a=2, b=96)

us_race_val=sq.norm(mean=0.95, sd=0.25)
prc_race_val=sq.norm(mean=0.8, sd=0.5)
prc_nonrace_val=sq.norm(mean=0.85, sd=0.45)

timeline_us_race_samples=timeline_race_samples[0]
timeline_prc_race_samples=timeline_race_samples[1]
timeline_prc_nonrace_samples=timeline_prc_nonrace@SAMPLE_SIZE
timeline_magic_samples=timeline_magic@SAMPLE_SIZE

timeline_prc_nonrace_samples=timeline_prc_nonrace_samples[timeline_prc_nonrace_samples>CURYEAR]
timeline_magic_samples=timeline_magic_samples[timeline_magic_samples>CURYEAR]

us_wins_race=1*(timeline_us_race_samples<timeline_prc_race_samples)
ev_us_wins_race=(1-pdoom_us_race@FILTERED_SIZE)*(us_race_val@FILTERED_SIZE)

prc_wins_race=1*(timeline_us_race_samples>timeline_prc_race_samples)
ev_prc_wins_race=(1-pdoom_prc_race@FILTERED_SIZE)*(prc_race_val@FILTERED_SIZE)

race_val=us_wins_race*ev_us_wins_race+prc_wins_race*ev_prc_wins_race

non_race_val=(prc_nonrace_val@SAMPLE_SIZE)*(1-pdoom_prc_nonrace@SAMPLE_SIZE)

little_magic_val=sq.mixture([(prc_nonrace_val*(1-pdoom_prc_nonrace)), (magic_val*(1-pdoom_magic))], [0.9, 0.1])
more_magic_val=sq.mixture([(prc_nonrace_val*(1-pdoom_prc_nonrace)), (magic_val*(1-pdoom_magic))], [0.8, 0.2])

little_magic_samples=little_magic_val@SAMPLE_SIZE
more_magic_samples=more_magic_val@SAMPLE_SIZE

years_left_nonrace=(timeline_prc_nonrace-CURYEAR)@SAMPLE_SIZE
years_left_race=np.hstack((timeline_us_race_samples[timeline_us_race_samples<timeline_prc_race_samples], timeline_prc_race_samples[timeline_us_race_samples>timeline_prc_race_samples]))-CURYEAR

years_left_race=years_left_race[years_left_race>0]
years_left_nonrace=years_left_nonrace[years_left_nonrace>0]

### Plotting!

fig=plt.figure(figsize=(8,4))

plt.hist(years_left_race, bins=200, histtype='step', stacked=True, fill=False, color="blue", label="Years left, race")
plt.hist(years_left_nonrace, bins=200, histtype='step', stacked=True, fill=False, color="red", label="Years left, no race")

plt.legend()

plt.savefig("yearsleft.png")

fig=plt.figure(figsize=(8,4))

plt.hist(pdoom_us_race@SAMPLE_SIZE, bins=200, histtype='step', stacked=True, fill=False, color="blue", label="US race p(doom)")
plt.hist(pdoom_prc_race@SAMPLE_SIZE, bins=200, histtype='step', stacked=True, fill=False, color="red", label="PRC race p(doom)")
plt.hist(pdoom_prc_nonrace@SAMPLE_SIZE, bins=200, histtype='step', stacked=True, fill=False, color="orange", label="PRC non-race p(doom)")
plt.hist(pdoom_magic@SAMPLE_SIZE, bins=200, histtype='step', stacked=True, fill=False, color="green", label="MAGIC p(doom)")

plt.legend()

plt.savefig("pdooms.png")

fig=plt.figure(figsize=(8,4))

plt.hist(us_race_val@SAMPLE_SIZE, bins=200, histtype='step', stacked=True, fill=False, color="blue", label="US race value")
plt.hist(prc_race_val@SAMPLE_SIZE, bins=200, histtype='step', stacked=True, fill=False, color="red", label="PRC race value")
plt.hist(prc_nonrace_val@SAMPLE_SIZE, bins=200, histtype='step', stacked=True, fill=False, color="orange", label="PRC non-race value")
plt.hist(magic_val@SAMPLE_SIZE, bins=200, histtype='step', stacked=True, fill=False, color="green", label="MAGIC value")

plt.legend()

plt.savefig("values.png")

fig=plt.figure(figsize=(8,4))

plt.hist(timeline_us_race_samples, bins=200, histtype='step', stacked=True, fill=False, color="blue", label="US race timeline")
plt.hist(timeline_prc_race_samples, bins=200, histtype='step', stacked=True, fill=False, color="red", label="PRC race timeline")
plt.hist(timeline_prc_nonrace_samples, bins=200, histtype='step', stacked=True, fill=False, color="orange", label="PRC non-race timeline")
plt.hist(timeline_magic_samples, bins=200, histtype='step', stacked=True, fill=False, color="green", label="MAGIC timeline")

plt.legend()

plt.savefig("timelines.png")

fig=plt.figure(figsize=(8,8))

plt.hist(race_val, bins=200, histtype='step', stacked=True, fill=False, color="blue", label="TAI race")

plt.legend()

plt.savefig("goodness_race.png")

plt.hist(non_race_val, bins=200, histtype='step', stacked=True, fill=False, color="red", label="Ceding to PRC")

plt.legend()

plt.savefig("goodnesses.png")

plt.hist(little_magic_val@SAMPLE_SIZE, bins=200, histtype='step', stacked=True, fill=False, color="green", label="Advocating for MAGIC (10% success)")

plt.legend()

plt.savefig("goodnesses_with_a_little_magic.png")

plt.hist(more_magic_val@SAMPLE_SIZE, bins=200, histtype='step', stacked=True, fill=False, color="purple", label="Advocating for MAGIC (20% success)")

plt.legend()

plt.savefig("goodnesses_with_more_magic.png")
