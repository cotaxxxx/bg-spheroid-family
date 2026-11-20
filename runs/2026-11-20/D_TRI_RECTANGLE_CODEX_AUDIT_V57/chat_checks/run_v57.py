"""Run the V57 sample checks (plan PLAN_V57.md). usage: run_v57.py READER_DIR samples.json part nparts out.jsonl"""
import sys, json, time
sys.path.insert(0, sys.argv[1])
from fractions import Fraction as Fr
from geoenclosereader import tri2
UNIT = 5242880
S = json.load(open(sys.argv[2])); part, nparts = int(sys.argv[3]), int(sys.argv[4]); out = open(sys.argv[5], 'a')
def ev(kind, axis, b, N):
    if kind == 'centre': return tri2.centre_h(axis, *b, N=N)
    if kind == 'pole': return tri2.pole_b(axis, *b, N=N)
    if kind == 'tau': return tri2.disk_tau(*b, N=N)
    if kind == 'tau2': return tri2.disk_tau2(*b, N=N)
for idx, smp in enumerate(S):
    if idx % nparts != part: continue
    T0 = time.time(); b0 = [Fr(int(x), UNIT) for x in smp['box']]; want = smp['sign']
    cs = [(b0[0] + b0[1])/2, (b0[0] + b0[1])/2, (b0[2] + b0[3])/2, (b0[2] + b0[3])/2]
    pc = ev(smp['kind'], smp['axis'], cs, 256)
    lo, hi = float(smp['lower']), float(smp['upper'])
    consistent = not (pc.hi < lo or pc.lo > hi)
    queue = [(b0, 0, 128)]; leaves = 0; maxN = 0; maxd = 0; status = 'CONFIRMED'; evals = 0
    while queue:
        if time.time() - T0 > 1800: status = 'NOT_REPRODUCED'; break
        b, depth, N = queue.pop(); e = ev(smp['kind'], smp['axis'], b, N); evals += 1; w = dict(tri2._enclose.last)
        ok = (e.lo > 0) if want == 'positive' else (e.hi < 0)
        bad = (e.hi < 0) if want == 'positive' else (e.lo > 0)
        if ok: leaves += 1; maxN = max(maxN, N); maxd = max(maxd, depth); continue
        if bad: status = 'CONTRADICTED'; break
        if w['shape_width'] > w['centre_width'] and depth < 8:
            sm, tm = (b[0] + b[1])/2, (b[2] + b[3])/2
            for q in ([b[0], sm, b[2], tm], [sm, b[1], b[2], tm], [b[0], sm, tm, b[3]], [sm, b[1], tm, b[3]]): queue.append((q, depth + 1, N))
        elif N < 512: queue.append((b, depth, 2*N))
        else: status = 'NOT_REPRODUCED'; break
    rec = dict(smp, centre_chat=[float(pc.lo), float(pc.hi)], consistent=consistent, status=status, leaves=leaves, evals=evals,
               maxN=maxN, maxdepth=maxd, seconds=round(time.time() - T0, 1))
    out.write(json.dumps(rec) + "\n"); out.flush(); print(rec['set'], rec['kind'], rec['axis'], rec['sign'], status, consistent, leaves, evals, rec['seconds'], flush=True)
