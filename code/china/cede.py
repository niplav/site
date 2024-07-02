import time
import numpy as np
import squigglepy as sq
import matplotlib.pyplot as plt

extinction_val=0
magic_val=sq.norm(mean=1, sd=0.1)

timeline_us_race=sq.mixture([sq.norm(mean=2035, sd=5, lclip=2024), sq.norm(mean=2060, sd=20, lclip=2024)], [0.7, 0.3])
timeline_us_race_sample=timeline_us_race@100000

timeline_prc_race=sq.mixture([sq.norm(mean=2036, sd=5, lclip=2024), sq.norm(mean=2061, sd=20, lclip=2024)], [0.7, 0.3])
timeline_prc_nonrace=sq.mixture([sq.norm(mean=2040, sd=5, lclip=2024), sq.norm(mean=2065, sd=20, lclip=2024)], [0.7, 0.3])

timeline_magic=sq.mixture([sq.norm(mean=2055, sd=5, lclip=2024), sq.norm(mean=2080, sd=20, lclip=2024)], [0.7, 0.3])

pdoom_us_race=sq.beta(a=2, b=18)
pdoom_prc_race=sq.beta(a=1.5, b=6)
pdoom_prc_nonrace=sq.beta(a=1.06, b=6)
pdoom_magic=sq.beta(a=2, b=96)

us_race_val=sq.norm(mean=0.95, sd=0.25)
prc_race_val=sq.norm(mean=0.8, sd=0.5)
prc_nonrace_val=sq.norm(mean=0.85, sd=0.45)

us_timelines_race=timeline_us_race@100000
prc_timelines_race=timeline_prc_race@100000

us_wins_race=1*(us_timelines_race<prc_timelines_race)
ev_us_wins_race=(1-pdoom_us_race@100000)*(us_race_val@100000)

prc_wins_race=1*(us_timelines_race>prc_timelines_race)
ev_prc_wins_race=(1-pdoom_prc_race@100000)*(prc_race_val@100000)

race_val=us_wins_race*ev_us_wins_race+prc_wins_race*ev_prc_wins_race

non_race_val=(prc_nonrace_val@100000)*(1-pdoom_prc_nonrace@100000)

curyear=time.localtime().tm_year
years_left_nonrace=(timeline_prc_nonrace-curyear)@100000
years_left_race=np.hstack((us_timelines_race[us_timelines_race<prc_timelines_race], prc_timelines_race[us_timelines_race>prc_timelines_race]))-curyear

fig=plt.figure(figsize=(8,4))

plt.hist(pdoom_us_race@100000, bins=200, histtype='step', stacked=True, fill=False, color="blue", label="US race p(doom)")
plt.hist(pdoom_prc_race@100000, bins=200, histtype='step', stacked=True, fill=False, color="red", label="PRC race p(doom)")
plt.hist(pdoom_prc_nonrace@100000, bins=200, histtype='step', stacked=True, fill=False, color="orange", label="PRC non-race p(doom)")
plt.hist(pdoom_magic@100000, bins=200, histtype='step', stacked=True, fill=False, color="green", label="MAGIC p(doom)")

plt.legend()

plt.savefig("pdooms.png")

fig=plt.figure(figsize=(8,4))

plt.hist(us_race_val@100000, bins=200, histtype='step', stacked=True, fill=False, color="blue", label="US race value")
plt.hist(prc_race_val@100000, bins=200, histtype='step', stacked=True, fill=False, color="red", label="PRC race value")
plt.hist(prc_nonrace_val@100000, bins=200, histtype='step', stacked=True, fill=False, color="orange", label="PRC non-race value")
plt.hist(magic_val@100000, bins=200, histtype='step', stacked=True, fill=False, color="green", label="MAGIC value")

plt.legend()

plt.savefig("values.png")

fig=plt.figure(figsize=(8,4))

timeline_us_race_samples=timeline_us_race@100000
timeline_prc_race_samples=timeline_prc_race@100000
timeline_prc_nonrace_samples=timeline_prc_nonrace@100000
timeline_magic_samples=timeline_magic@100000

timeline_us_race_samples=timeline_us_race_samples[timeline_us_race_samples>curyear]
timeline_prc_race_samples=timeline_prc_race_samples[timeline_prc_race_samples>curyear]
timeline_prc_nonrace_samples=timeline_prc_nonrace_samples[timeline_prc_nonrace_samples>curyear]
timeline_magic_samples=timeline_magic_samples[timeline_magic_samples>curyear]

plt.hist(timeline_us_race_samples, bins=200, histtype='step', stacked=True, fill=False, color="blue", label="US race timeline")
plt.hist(timeline_prc_race_samples, bins=200, histtype='step', stacked=True, fill=False, color="red", label="PRC race timeline")
plt.hist(timeline_prc_nonrace_samples, bins=200, histtype='step', stacked=True, fill=False, color="orange", label="PRC non-race timeline")
plt.hist(timeline_magic_samples, bins=200, histtype='step', stacked=True, fill=False, color="green", label="MAGIC timeline")

plt.legend()

plt.savefig("timelines.png")

fig=plt.figure(figsize=(8,8))

plt.hist(race_val, bins=200, histtype='step', stacked=True, fill=False, color="blue", label="Value of TAI race")
plt.hist(non_race_val, bins=200, histtype='step', stacked=True, fill=False, color="red", label="Value of ceding to PRC")

plt.legend()

plt.savefig("goodnesses.png")
#plt.hist(, bins=200, histtype='step', stacked=True, fill=False, color="orange", label="PRC non-race value")

plt.savefig("goodnesses_with_little_magic.png")
