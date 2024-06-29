import numpy as np
import squigglepy as sq
import matplotlib.pyplot as plt

extinction_val=0
magic=1

timeline_us_race=sq.mixture([sq.norm(mean=2035, sd=5, lclip=2024), sq.norm(mean=2060, sd=20, lclip=2024)], [0.7, 0.3])
timeline_us_race_sample=timeline_us_race@10000

timeline_prc_race=sq.mixture([sq.norm(mean=2036, sd=5, lclip=2024), sq.norm(mean=2061, sd=20, lclip=2024)], [0.7, 0.3])
timeline_prc_nonrace=sq.mixture([sq.norm(mean=2040, sd=5, lclip=2024), sq.norm(mean=2065, sd=20, lclip=2024)], [0.7, 0.3])

pdoom_us_race=sq.beta(a=2, b=18)
pdoom_prc_race=sq.beta(a=1.5, b=6)
pdoom_prc_nonrace=sq.beta(a=1.06, b=6)

goodness_us_race=sq.norm(mean=0.95, sd=0.1)
goodness_prc_race=sq.norm(mean=0.8, sd=0.5)
goodness_prc_nonrace=sq.norm(mean=0.85, sd=0.45)

us_timelines_race=timeline_us_race@100000
prc_timelines_race=timeline_prc_race@100000

us_wins_race=1*(us_timelines_race<prc_timelines_race)
ev_us_wins_race=(1-pdoom_us_race@100000)*(goodness_us_race@100000)

prc_wins_race=1*(us_timelines_race>prc_timelines_race)
ev_prc_wins_race=(1-pdoom_prc_race@100000)*(goodness_prc_race@100000)

goodness_race=us_wins_race*ev_us_wins_race+prc_wins_race*ev_prc_wins_race

goodness_non_race=(goodness_prc_nonrace@100000)*(1-pdoom_prc_nonrace@100000)

curyear=time.localtime().tm_year
years_left_nonrace=(timeline_prc_nonrace-curyear)@100000
years_left_race=np.hstack((us_timelines_race[us_timelines_race<prc_timelines_race], prc_timelines_race[us_timelines_race>prc_timelines_race]))-curyear
