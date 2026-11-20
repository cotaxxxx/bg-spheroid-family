import sys, csv, time, random, json; sys.path.insert(0, sys.argv[1])
from fractions import Fraction as Fr
from geoenclosereader import tri2
OUT = sys.argv[2]; U = 5242880; R = random.Random(57)
c = [r for r in csv.DictReader(open(f"{OUT}/central.csv")) if r['result'] == 'down_t' and r['surface'] == 'R']
a2 = sorted([r for r in c if r['axis'] == '2'], key=lambda r: -float(r['dthi'])); a1 = [r for r in c if r['axis'] == '1']
S = a2[:2] + R.sample(a2[2:], 2) + R.sample(a1, 2)
for r in S:
    T0 = time.time(); i = int(r['axis']); b0 = [Fr(int(r[k]), U) for k in ('s0', 's1', 't0', 't1')]
    queue = [(b0, 0)]; status = 'CONFIRMED'; leaves = 0; worst = None
    while queue:
        if time.time() - T0 > 1200: status = 'NOT_REPRODUCED'; break
        b, dep = queue.pop(); done = False
        for N in ((128, 256, 512) if dep == 0 else (512,)):
            gs, gt = tri2.param_grad("centre", i, (b[0], b[2]), (b[1], b[3]), N=N)
            if gt.hi < 0: done = True; leaves += 1; worst = max(worst or -9, float(gt.hi)); break
            if gt.lo > 0: status = 'CONTRADICTED'; break
        if status == 'CONTRADICTED': break
        if not done:
            if dep >= 4: status = 'NOT_REPRODUCED'; break
            sm, tm = (b[0] + b[1])/2, (b[2] + b[3])/2
            queue += [([b[0], sm, b[2], tm], dep+1), ([sm, b[1], b[2], tm], dep+1), ([b[0], sm, tm, b[3]], dep+1), ([sm, b[1], tm, b[3]], dep+1)]
    print(json.dumps(dict(axis=i, box=[float(x) for x in b0], codex_dt=[r['dtlo'], r['dthi']], status=status, leaves=leaves, chat_worst_upper=worst, seconds=round(time.time()-T0))), flush=True)
