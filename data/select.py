#!/usr/bin/python

import sys
import random
import itertools as it

def powerset(iterable):
        s = list(iterable)
        allcomb=[]
        for r in range(len(s)+1):
                allcomb+=list(it.combinations(s,r))
        return allcomb

if sys.argv[1].startswith('n'):
	choices=powerset(['melatonin', 'magnesium'])
else:
	choices=powerset(['caffeine', 'l-theanine', 'l-glycine', 'vitamind3', 'vitaminb12', 'omega3', 'creatine'])

print(random.sample(choices, 1))
