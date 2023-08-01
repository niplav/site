import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fig=plt.figure(figsize=(8,8))

df=pd.read_csv('./hodge_preservations.csv', header=None)
summ=df.groupby(0).describe()
preserves=df.loc[df[1]==1.0].groupby(0).count()[1]

#plt.plot(summ[2]['mean'], color="green", label="Mean |imcs(G)|")

plt.plot(summ[1]['mean'], color="red", label="Mean amsp(G) (hodgeresolve)")
plt.plot(preserves/summ[1]['count'], color="pink", label="Graphs with amsp(G)=1 (hodgeresolve)")
plt.plot(summ[1]['min'], color="crimson", label="Min amsp(G) (hodgeresolve)")

df=pd.read_csv('./eged_preservations.csv', header=None)
summ=df.groupby(0).describe()
preserves=df.loc[df[1]==1.0].groupby(0).count()[1]

plt.plot(summ[1]['mean'], color="blue", label="Mean amsp(G) (eged)")
plt.plot(preserves/summ[1]['count'], color="cyan", label="Graphs with amsp(G)=1 (eged)")
plt.plot(summ[1]['min'], color="darkblue", label="Min amsp(G) (eged)")

plt.legend()

plt.set_xlabel('Number of nodes in graph')
plt.set_ylabel('Percentage')
plt.set_xticks()

plt.savefig("preservations.png")

exit(0)

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
