import numpy as np
import squigglepy as sq
import matplotlib.pyplot as plt

extinction_val=0
patient_us_val=1

timeline_us_race=sq.mixture([sq.norm(mean=2035, sd=5, lclip=2024), sq.norm(mean=2060, sd=20, lclip=2024)], [0.7, 0.3])
timeline_us_race_sample=timeline_us_race@10000

timeline_prc_race=sq.mixture([sq.norm(mean=2036, sd=5, lclip=2024), sq.norm(mean=2061, sd=20, lclip=2024)], [0.7, 0.3])

pdoom_us_race=sq.beta(a=2, b=18)
pdoom_prc_race=sq.beta(a=1.5, b=6)

goodness_us_race=sq.norm(mean=0.95, sd=0.1)
goodness_prc_race=sq.norm(mean=0.8, sd=0.5)
goodness_prc_nonrace=sq.norm(mean=0.85, sd=0.45)
