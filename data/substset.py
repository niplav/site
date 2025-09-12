#!/usr/bin/python

import random

substances=['caffeine', 'theanine', 'glycine', 'vitamind', 'vitaminb12', 'omega3', 'creatine']

print(random.sample(substances, random.randint(0, len(substances))))
