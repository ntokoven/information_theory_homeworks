import math
import string
from collections import defaultdict, OrderedDict
import re
import operator
import numpy as np
import pandas as pd

def count_freq(f):
    data = f.read().lower()
    data = re.sub(r'[^a-zA-Z]', '', data)

    counter = defaultdict(int)

    for c in data:
        counter[c] += 1
    
    counter = OrderedDict(sorted(counter.items(), key=lambda t: t[0]))
    #counter = sorted(counter.items(), key=operator.itemgetter(1))
    return counter

def build_dist(P):

    def sanity_check(P):
        norm = 0 
        eps = 1e-7
        for key, value in P.items():
            norm += value
        assert norm > 1 - eps and norm < 1 + eps

    norm = 0
    for key, value in P.items():
        norm += value
    for key, value in P.items():
        P[key] /= norm
    sanity_check(P)
    return P

def calc_variation_dist(P, Q):
    dist = []
    for key in P.keys():
        dist.append(np.abs(P[key] - Q[key]))
    return 0.5 * np.sum(dist)

langs = ['eng', 'esp', 'fin','ger', 'ita']
P = dict()
for lang in langs:
    with open('Alice_%s.txt' % lang) as f:
        P[lang] = count_freq(f)
    P[lang] = build_dist(P[lang])
var_distance = pd.DataFrame(index=langs, columns=langs)
for lang1 in langs:
    for lang2 in langs:
        var_distance.loc[lang1, lang2] = calc_variation_dist(P[lang1], P[lang2])

print(var_distance[0:-1])
