"""V59 runner: 5-D adaptive cover (shape tile x position box) for layer I (W3/H33) and layer II (C12).
usage: run_v59.py READER_DIR samples.json part nparts out.jsonl"""
import sys, json, time
sys.path.insert(0, sys.argv[1])
from fractions import Fraction as F
from geoenclosereader import tri3
S = json.load(open(sys.argv[2])); part, nparts, out = int(sys.argv[3]), int(sys.argv[4]), open(sys.argv[5], 'a')
import math
BUDGET = 240; MAXDEPTH = 14
def grade(kind, box):
    L3 = float(box[0][1]*box[1][1])          # largest third axis on the box
    if kind == 'H33': return max(0, min(4, round(math.log2(L3))))
    if kind == 'W3': return max(0, min(2, round(math.log2(L3)/2)))
    return 0
def ev(kind, box, N):
    return {'W3': tri3.W3, 'H33': tri3.H33, 'C12': tri3.C12}[kind](box, N, grade(kind, box))
def outside(box):
    return sum(b[0]**2 for b in box[2:]) > 1
for idx, smp in enumerate(S):
    if idx % nparts != part: continue
    kind = smp['kind']; box0 = [tuple(F(x) for x in pr) for pr in smp['box']]; T0 = time.time()
    queue = [(box0, 0, 64)]; leaves = evals = skipped = maxd = 0; status = 'COVERED'
    while queue:
        if time.time() - T0 > BUDGET: status = 'BUDGET'; break
        box, dep, N = queue.pop()
        if outside(box): skipped += 1; continue
        try:
            e = ev(kind, box, N); evals += 1
        except ValueError as ex:
            status = 'KERNEL_LIMIT: ' + str(ex); break
        if e.lo > 0: leaves += 1; maxd = max(maxd, dep); continue
        if e.hi < 0 and tri3.enclose.last['contact_cells'] == 0: status = 'NEGATIVE'; break
        L = tri3.enclose.last; terms = L['terms']; aw = L['angular_width']
        jbest = max(terms, key=lambda j: terms[j]) if terms else None
        if jbest is not None and terms[jbest] >= aw and dep < MAXDEPTH:
            lo, hi = box[jbest]; m = (lo + hi)/2
            for half in ((lo, m), (m, hi)):
                nb = list(box); nb[jbest] = half; queue.append((nb, dep + 1, N))
        elif N < 256: queue.append((box, dep, 2*N))
        elif jbest is not None and dep < MAXDEPTH:
            lo, hi = box[jbest]; m = (lo + hi)/2
            for half in ((lo, m), (m, hi)):
                nb = list(box); nb[jbest] = half; queue.append((nb, dep + 1, N))
        else: status = 'UNRESOLVED'; break
    rec = dict(smp, status=status, leaves=leaves, evals=evals, skipped=skipped, maxdepth=maxd, remaining=len(queue), sec=round(time.time() - T0, 1))
    out.write(json.dumps(rec, default=str) + "\n"); out.flush(); print(json.dumps(rec, default=str), flush=True)
