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

plt.legend()

plt.savefig("allscatter.png")

fig=plt.figure(figsize=(8,8), clear=True)

plt.xlabel("Range (months)")
plt.ylabel("Number of datapoints")

plt.plot(metss, '-', color='red')
plt.plot(pbss, '-', color='blue')

plt.savefig("ss_plot.png")

#TODO: there is something fishy going on with this plot: it's not output at the right size, and the labels are truncated

fig=plt.figure(figsize=(10,10), clear=True)

_, ax1 = plt.subplots()

ax1.set_xlabel("Range (months)")
ax1.set_ylabel("Correlation value")

ax1.plot(metpvals[2], metpvals[1], '-', linewidth=3, color='#ff4500', label="Metaculus truncated correlations")
ax1.plot(pbpvals[2], pbpvals[1], '-', linewidth=3, color='#00bfff', label="PredictionBook truncated correlations")

ax1.legend(loc='lower right')

ax2=ax1.twinx()

ax2.set_ylabel("p value")
ax2.semilogy(metpvals[2], metpvals[0], '-', color='#ffa500', basey=10, linewidth=1, label="Metaculus truncated p-values")
ax2.semilogy(pbpvals[2], pbpvals[0], '-', color='cyan', basey=10, linewidth=1, label="PredictionBook truncated p-values")

#urgh TODO fix this
ax2.legend(loc='upper right')

plt.savefig("pvals_plot.png")

fig=plt.figure(figsize=(10,10), clear=True)

_, ax1 = plt.subplots()

ax1.set_xlabel("Range (months)")
ax1.set_ylabel("Correlation value")

ax1.plot(pbpvals[2], pbpvals[1], '-', linewidth=3, color='#00bfff', label="PredictionBook truncated correlations")

ax1.legend(loc='lower right')

ax2=ax1.twinx()

ax2.set_ylabel("p value")
ax2.semilogy(pbpvals[2], pbpvals[0], '-', color='cyan', basey=10, linewidth=1, label="PredictionBook truncated p-values")

#urgh TODO fix this
ax2.legend(loc='upper right')

plt.savefig("pvals_pb_plot.png")
