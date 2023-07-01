import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# No! Wrong! TODO!
# Don't just pad. You need to do something more elaborate.

def plot_confusions(df, multiplier):
	values=np.zeros(len(labels))
	for i in range(0, len(labels)):
		try:
			values[i]=df.loc[df[1]==labels[i]][2].iloc[0]
		except:
			continue
	offset=width*multiplier
	rects=ax.bar(x+offset, values, width, log=True)

confusions=pd.read_csv('../../data/compressed.csv', header=None)
labels=np.sort(confusions[1].unique())
x=np.arange(len(labels))
width=1/6
multiplier=0

fig, ax=plt.subplots(constrained_layout=True)

for c in list(confusions.groupby(0)):
	plot_confusions(c[1], c[0])

ax.set_ylabel('Number of graphs with confusion')
ax.set_xticks(x+width, labels)

plt.savefig('nconfusions.png')
