import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

exec(open("load.py").read())

fig=plt.figure(figsize=(8,8))
plt.xlabel("Range (days)")
plt.ylabel("Accuracy (Brier score)")

plt.plot(metrngs, metbriers, '.', color='red', markersize=1)
plt.plot(pbrngs, mintercept+mslope*pbrngs, 'red', label='Metaculus linear regression', linewidth=1)
plt.plot(pbrngs, pbbriers, '.', color='blue', markersize=1)
plt.plot(pbrngs, pintercept+pslope*pbrngs, 'blue', label='PredictionBook linear regression', linewidth=1)

plt.savefig("allscatter.png")

fig=plt.figure(figsize=(8,8), clear=True)

plt.xlabel("Range (months)")
plt.ylabel("Number of datapoints")

plt.plot(metss, '-', color='red')
plt.plot(pbss, '-', color='blue')

plt.savefig("ss_plot.png")

_, ax1 = plt.subplots()

ax2=ax1.twinx()

ax2.set_ylabel("p value")
ax2.semilogy(metpvals[1], metpvals[0], '.', color='orange', markersize=1)
ax2.semilogy(pbpvals[1], pbpvals[0], '.', color='purple', markersize=1)

plt.savefig("pvals_ss_plot.png")
