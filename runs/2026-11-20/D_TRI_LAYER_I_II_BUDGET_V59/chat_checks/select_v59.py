import json, random
from fractions import Fraction as F
R = random.Random(59); w = F(1, 32); n = 32
tiles = [(0, 0), (1, 3), (2, 5), (3, 7)]
def tile(i, j): return [(1 + F(11, 20)*i, 1 + F(11, 20)*(i+1)), (1 + F(5, 8)*j, 1 + F(5, 8)*(j+1))]
cells = [(a, b, c) for a in range(n) for b in range(n) for c in range(n) if (a*w)**2 + (b*w)**2 + (c*w)**2 <= 1]
def stratum(a, b, c):
    if ((a+1)*w)**2 + ((b+1)*w)**2 + ((c+1)*w)**2 > 1: return 'rim'
    if c == 0: return 'equator'
    if a == 0 or b == 0: return 'axis-face'
    return 'interior'
groups = {}
for x in cells: groups.setdefault(stratum(*x), []).append(x)
counts = {k: len(v) for k, v in groups.items()}
disk = [(a, b) for a in range(1, n) for b in range(1, n) if (a*w)**2 + (b*w)**2 <= 1]
dgroups = {}
for (a, b) in disk: dgroups.setdefault('rim' if ((a+1)*w)**2 + ((b+1)*w)**2 > 1 else 'interior', []).append((a, b))
S = []
for k, v in sorted(groups.items()):
    for (a, b, c) in R.sample(v, 4):
        for (i, j) in tiles:
            q = [(a*w, (a+1)*w), (b*w, (b+1)*w), (c*w, (c+1)*w)]
            S.append(dict(layer='I', stratum=k, kind='H33' if c == 0 else 'W3', tile=[i, j], cell=[a, b, c], box=[[str(x) for x in p] for p in tile(i, j) + q]))
for k, v in sorted(dgroups.items()):
    for (a, b) in R.sample(v, 4):
        for (i, j) in tiles:
            q = [(a*w, (a+1)*w), (b*w, (b+1)*w), (F(0), F(0))]
            S.append(dict(layer='II', stratum=k, kind='C12', tile=[i, j], cell=[a, b], box=[[str(x) for x in p] for p in tile(i, j) + q]))
json.dump(dict(counts_I=counts, counts_II={k: len(v) for k, v in dgroups.items()}, axis_strip_II=2*n - 1), open('strata_v59.json', 'w'))
json.dump(S, open('samples_v59.json', 'w')); print(len(S), counts, {k: len(v) for k, v in dgroups.items()})
