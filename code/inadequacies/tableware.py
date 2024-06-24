import numpy as np
import matplotlib.pyplot as plt
import squigglepy as sq

people=sq.norm(mean=8*10**9, sd=0.05)
meals_per_day=sq.norm(mean=2.5, sd=1, lclip=0)
proportion_tableware_users=sq.beta(a=5, b=2.5)
breakage_per_meal=sq.beta(a=1.5, b=1000)
cost_per_tableware=sq.norm(mean=2, sd=0.5, lclip=0)
total_cost_per_day=(people*meals_per_day*proportion_tableware_users*breakage_per_meal*cost_per_tableware)@100000

fig=plt.figure(figsize=(10,10))
plt.xlabel('cost')
plt.ylabel('number of samples')
plt.hist(total_cost_per_day, label="samples", bins=500)
plt.legend()
plt.savefig('tableware_sq.png')
