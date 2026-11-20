import csv, json, random, sys
OUT = sys.argv[1]; R = random.Random(57)
load = lambda n: list(csv.DictReader(open(f"{OUT}/{n}")))
def pick(rows, sign, nweak, nrand):
    m = (lambda r: float(r['lower'])) if sign == 'positive' else (lambda r: -float(r['upper']))
    rows = sorted(rows, key=m); weak = rows[:nweak]; rest = rows[nweak:]
    return weak + R.sample(rest, min(nrand, len(rest)))
S = []
c = [r for r in load('central.csv') if r['surface'] == 'R']
for ax, sg in (('1', 'negative'), ('2', 'positive'), ('2', 'negative')):
    for r in pick([x for x in c if x['axis'] == ax and x['result'] == sg], sg, 2, 2):
        S.append(dict(set='S1', kind='centre', axis=int(ax), sign=sg, box=[r[k] for k in ('s0', 's1', 't0', 't1')], lower=r['lower'], upper=r['upper']))
a = [r for r in load('axis_cover.csv') if r['surface'] == 'R' and r['mode'] == '1']
b = [r for r in load('bfinish.csv') if r['surface'] == 'R' and r['mode'] == '1']
for ax, sg in (('2', 'negative'), ('2', 'positive'), ('1', 'negative'), ('1', 'positive')):
    src = a if ax == '2' else b
    for r in pick([x for x in src if x['axis'] == ax and x['result'] == sg], sg, 1, 2):
        S.append(dict(set='S2', kind='pole', axis=int(ax), sign=sg, box=[r[k] for k in ('s0', 's1', 't0', 't1')], lower=r['lower'], upper=r['upper']))
d = load('disk.csv')
for mode in ('tau', 'tau2'):
    for r in pick([x for x in d if x['mode'] == mode], 'positive', 2, 0):
        S.append(dict(set='S3', kind=mode, axis=0, sign='positive', box=[r[k] for k in ('t0', 't1', 'r0', 'r1')], lower=r['lower'], upper=r['upper']))
json.dump(S, open('samples_v57.json', 'w'), indent=1); print(len(S))
