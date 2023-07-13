import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_confusions(df, multiplier):
	values=np.zeros(len(labels))
	for i in range(0, len(labels)):
		try:
			values[i]=df.loc[df[1]==labels[i]][2].iloc[0]
		except:
			continue
	offset=width*multiplier-4*width
	rects=ax.bar(x+offset, values, width, log=True, label="size of graph: "+str(multiplier))

confusions=pd.read_csv('../../data/compressed.csv', header=None)
labels=np.sort(confusions[1].unique())
x=np.arange(len(labels))

width=1/5
multiplier=0

fig, ax=plt.subplots(constrained_layout=True)

for c in list(confusions.groupby(0)):
	plot_confusions(c[1], c[0])

ax.set_xlabel('Confusion')
ax.set_ylabel('Number of graphs with confusion')
ax.set_xticks(x+width, labels)

plt.legend(loc='lower right')

plt.savefig('nconfusions.png')
