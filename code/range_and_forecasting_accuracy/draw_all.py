import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import random

exec(open("load.py").read())

fig=plt.figure(figsize=(8,8))

plt.title("Scatterplot with linear regression for Metaculus & PredictionBook forecasts by range")
plt.xlabel("Range (days)")
plt.ylabel("Accuracy (Brier score)")

plt.plot(metrngs, metbriers, '.', color='red', markersize=1)
plt.plot(pbrngs, mintercept+mslope*pbrngs, 'red', label='Metaculus linear regression', linewidth=1)
plt.plot(pbrngs, pbbriers, '.', color='blue', markersize=1)
plt.plot(pbrngs, pintercept+pslope*pbrngs, 'blue', label='PredictionBook linear regression', linewidth=1)

plt.legend()

plt.savefig("allscatter.png")

fig=plt.figure(figsize=(8,8))

plt.title("Scatterplot with logistic-ish regression for Metaculus & PredictionBook forecasts by range")
plt.xlabel("Range (days)")
plt.ylabel("Accuracy (Brier score)")

fullrng_pb=np.array(range(0, round(max(pbrngs))+1))
fullrng_met=np.array(range(0, round(max(metrngs))+1))

plt.plot(pbrngs, pbbriers, '.', color='blue', markersize=1)
plt.plot(metrngs, metbriers, '.', color='red', markersize=1)
plt.plot(fullrng_pb, shrunk_logistic(fullrng_pb, metlogifit[0][0], metlogifit[0][1]), 'red', label='Metaculus shrunk logistic-ish regression', linewidth=2)
plt.plot(fullrng_pb, shrunk_logistic(fullrng_pb, pblogifit[0][0], pblogifit[0][1]), 'blue', label='PredictionBook shrunk logistic-ish regression', linewidth=2)

plt.legend()

plt.savefig("allscatter_logi.png")

fig=plt.figure(figsize=(8,8))

plt.title("Scatterplot with exponential-ish regression for Metaculus & PredictionBook forecasts by range")
plt.xlabel("Range (days)")
plt.ylabel("Accuracy (Brier score)")

fullrng_pb=np.array(range(0, round(max(pbrngs))+1))

plt.plot(pbrngs, pbbriers, '.', color='blue', markersize=1)
plt.plot(metrngs, metbriers, '.', color='red', markersize=1)
plt.plot(fullrng_pb, shift_exp(fullrng_pb, metexpfit[0][0]), 'red', label='Metaculus shrunk exponential-ish regression', linewidth=2)
plt.plot(fullrng_pb, shift_exp(fullrng_pb, pbexpfit[0][0]), 'blue', label='PredictionBook shrunk exponential-ish regression', linewidth=2)

plt.legend()

plt.savefig("allscatter_exp.png")

fig=plt.figure(figsize=(8,8), clear=True)

plt.title("Sample sizes for predictions with a range (in months), sorted and graphed")
plt.xlabel("Range (months)")
plt.ylabel("Number of datapoints")

plt.plot(metss, '-', color='red')
plt.plot(pbss, '-', color='blue')

plt.savefig("ss_plot.png")

#TODO: there is something fishy going on with this plot: it's not output at the right size, and the labels are truncated

fig=plt.figure(figsize=(10,10), clear=True)

plt.title("Truncated p-values and correlations for both datasets")

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

plt.title("Truncated p-values and correlations for the PredictionBook dataset")

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

fig=plt.figure(figsize=(8,8))

plt.title("Scatterplot with linear regression for Metaculus & PredictionBook question accuracy by range")
plt.xlabel("Range (days)")
plt.ylabel("Accuracy (Brier score)")

plt.plot(pbqbrier.T[0], pbqbrier.T[1], '.', color='blue', markersize=1)
plt.plot(pbqbrier.T[0], pbqintercept+pbqslope*pbqbrier.T[0], 'blue', label='PredictionBook linear regression', linewidth=1)
plt.plot(metqbrier.T[0], metqbrier.T[1], '.', color='red', markersize=2)
plt.plot(pbqbrier.T[0], mqintercept+mqslope*pbqbrier.T[0], 'red', label='Metaculus linear regression', linewidth=1)

plt.legend()

plt.savefig("allq.png")

fig=plt.figure(figsize=(8,8))

plt.title("Scatterplot with logistic-ish regression for Metaculus & PredictionBook forecasts by range")
plt.xlabel("Range (days)")
plt.ylabel("Accuracy (Brier score)")

fullrng_pb=np.array(range(0, round(max(pbrngs))+1))

plt.plot(pbqbrier.T[0], pbqbrier.T[1], '.', color='blue', markersize=1)
plt.plot(metqbrier.T[0], metqbrier.T[1], '.', color='red', markersize=1)
plt.plot(fullrng_pb, shrunk_logistic(fullrng_pb, metlogifit_betweenq[0][0], metlogifit_betweenq[0][1]), 'red', label='Metaculus shrunk logistic-ish regression', linewidth=2)
plt.plot(fullrng_pb, shrunk_logistic(fullrng_pb, pblogifit_betweenq[0][0], pblogifit_betweenq[0][1]), 'blue', label='PredictionBook shrunk logistic-ish regression', linewidth=2)

plt.legend()

plt.savefig("allq_logi.png")

fig=plt.figure(figsize=(8,8))

plt.title("Scatterplot with exponential-ish regression for Metaculus & PredictionBook forecasts by range")
plt.xlabel("Range (days)")
plt.ylabel("Accuracy (Brier score)")

fullrng_pb=np.array(range(0, round(max(pbrngs))+1))

plt.plot(pbqbrier.T[0], pbqbrier.T[1], '.', color='blue', markersize=1)
plt.plot(metqbrier.T[0], metqbrier.T[1], '.', color='red', markersize=1)
plt.plot(fullrng_pb, shift_exp(fullrng_pb, metexpfit_betweenq[0][0]), 'red', label='Metaculus shrunk exponential-ish regression', linewidth=2)
plt.plot(fullrng_pb, shift_exp(fullrng_pb, pbexpfit_betweenq[0][0]), 'blue', label='PredictionBook shrunk exponential-ish regression', linewidth=2)

plt.legend()

plt.savefig("allq_exp.png")

fig=plt.figure(figsize=(8,8))

plt.title("Linear regressions for the accuracy of questions by range (only Metaculus data)")
plt.xlabel("Age (days)")
plt.ylabel("Linear regression")

for i in range(0, len(wmetqregs)):
	r=wmetqregs[i]
	rngs=wmetqbrier[i][0]
	slope, intercept, _, _, _=r
	cl=hex(random.sample(range(0, 256*256*256), 1)[0]) #random rgb code
	#left padding with zeros, can't be bothered to read the formatting docs right now
	cl='#'+('0'*(6-len(cl[2:])))+cl[2:]
	plt.plot(rngs, intercept+slope*rngs, color=cl, linewidth=1)

plt.savefig("permetquestion.png")

fig=plt.figure(figsize=(8,8))

plt.title("Linear regressions for the accuracy of questions by range (only PredictionBook data)")
plt.xlabel("Age (days)")
plt.ylabel("Linear regression")

for i in range(0, len(wpbqregs)):
	r=wpbqregs[i]
	rngs=wpbqbrier[i][0]
	slope, intercept, _, _, _=r
	cl=hex(random.sample(range(0, 256*256*256), 1)[0]) #random rgb code
	#left padding with zeros, can't be bothered to read the formatting docs right now
	cl='#'+('0'*(6-len(cl[2:])))+cl[2:]
	plt.plot(rngs, intercept+slope*rngs, color=cl, linewidth=1)

plt.savefig("perpbquestion.png")

fig=plt.figure(figsize=(8,8))

plt.title("Mean of linear regressions on accuracy within questions")
plt.xlabel("Range (days)")
plt.ylabel("Accuracy (Brier score)")

plt.plot(pbrngs, awmetqintercept+awmetqslope*pbrngs, 'red', label='Metaculus aggregate linear regression', linewidth=1)
plt.plot(pbrngs, fawpbqintercept+fawpbqslope*pbrngs, 'blue', label='PredictionBook aggregate linear regression', linewidth=1)

plt.legend()

plt.savefig("withintotal.png")

fig=plt.figure(figsize=(8,8))

plt.title("Logistic curve-fits for the accuracy of questions by range (only Metaculus data)")
plt.xlabel("Age (days)")
plt.ylabel("Logistic curve-fit")

for i in range(0, len(within_logi_fits_met)):
	r=within_logi_fits_met[i]
	if len(r)==0:
		continue
	rngs=wmetqbrier[i][0]
	slope, intercept=r[0][0], r[0][1]
	cl=hex(random.sample(range(0, 256*256*256), 1)[0]) #random rgb code
	#left padding with zeros, can't be bothered to read the formatting docs right now
	cl='#'+('0'*(6-len(cl[2:])))+cl[2:]
	plt.plot(fullrng_met, shrunk_logistic(fullrng_met, slope, intercept))

plt.savefig("permetquestion_logi.png")

fig=plt.figure(figsize=(8,8))

plt.title("Logistic curve-fits for the accuracy of questions by range (only PredictionBook data)")
plt.xlabel("Age (days)")
plt.ylabel("Logistic curve-fit")

for i in range(0, len(within_logi_fits_pb)):
	r=within_logi_fits_pb[i]
	if len(r)==0:
		continue
	rngs=wpbqbrier[i][0]
	slope, intercept=r[0][0], r[0][1]
	cl=hex(random.sample(range(0, 256*256*256), 1)[0]) #random rgb code
	#left padding with zeros, can't be bothered to read the formatting docs right now
	cl='#'+('0'*(6-len(cl[2:])))+cl[2:]
	plt.plot(fullrng_pb, shrunk_logistic(fullrng_pb, slope, intercept))

plt.savefig("perpbquestion_logi.png")
