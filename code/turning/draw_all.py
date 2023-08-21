import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fig=plt.figure(figsize=(10,10))

df=pd.read_csv('./hodge_preservations.csv', header=None)
summ=df.groupby(0).describe()
preserves=df.loc[df[1]==1.0].groupby(0).count()[1]

#plt.plot(summ[2]['mean'], color="green", label="Mean |imcs(G)|")

plt.plot(summ[1]['mean'], color="red", label="Mean amsp(G) (hodgeresolve)", linewidth=3)
plt.plot(preserves/summ[1]['count'], color="pink", label="Graphs with amsp(G)=1 (hodgeresolve)", linewidth=3)
plt.plot(summ[1]['min'], color="brown", label="Min amsp(G) (hodgeresolve)", linewidth=3)

df=pd.read_csv('./eged_preservations.csv', header=None)
summ=df.groupby(0).describe()
preserves=df.loc[df[1]==1.0].groupby(0).count()[1]

plt.plot(summ[1]['mean'], color="blue", label="Mean amsp(G) (eged)", linewidth=3)
plt.plot(preserves/summ[1]['count'], color="cyan", label="Graphs with amsp(G)=1 (eged)", linewidth=3)
plt.plot(summ[1]['min'], color="darkblue", label="Min amsp(G) (eged)", linewidth=3)

plt.legend()

plt.xlabel('Number of nodes in graph')
plt.ylabel('Percentage')
plt.xticks()

plt.savefig("preservations.png")

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

fig, ax=plt.subplots(constrained_layout=True, figsize=(10,10))

for c in list(confusions.groupby(0)):
	plot_confusions(c[1], c[0])

ax.set_xlabel('Confusion')
ax.set_ylabel('Number of graphs with confusion')
ax.set_xticks(x+width, labels)

plt.legend(loc='lower right')

plt.savefig('nconfusions.png')
