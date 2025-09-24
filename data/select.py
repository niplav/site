#!/usr/bin/python

import random
import itertools as it

def powerset(iterable):
        s = list(iterable)
        allcomb=[]
        for r in range(len(s)+1):
                allcomb+=list(it.combinations(s,r))
        return allcomb

choices=powerset(['caffeine', 'theanine', 'glycine', 'vitamind', 'vitaminb12', 'omega3', 'creatine'])

print(random.sample(choices, 1))
