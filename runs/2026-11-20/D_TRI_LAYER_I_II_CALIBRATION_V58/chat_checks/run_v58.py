"""V58 calibration runner. usage: run_v58.py READER_DIR stage part nparts out.jsonl"""
import sys, json, time
sys.path.insert(0, sys.argv[1])
from fractions import Fraction as F
from geoenclosereader import tri3
stage, part, nparts, out = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), open(sys.argv[5], 'a')
R = F(1, 1024)
PATCH = [('oct', 'W3', (F(1,4), F(1,4), F(1,2))), ('face13', 'W3', (F(1,4), 0, F(1,2))), ('face23', 'W3', (0, F(1,4), F(1,2))),
         ('rim13', 'W3', (F(3,5), 0, F(4,5))), ('plane', 'H33', (F(1,4), F(1,4), 0)), ('disk', 'C12', (F(1,2), F(1,2), 0)),
         ('rim12', 'C12', (F(3,5), F(4,5), 0)), ('disk2', 'C12', (F(1,4), F(1,2), 0))]
def qbox(name, kind, c, r):
    b = []
    for k, x in enumerate(c):
        x = F(x)
        if kind == 'H33' and k == 2: b.append((F(0), r)); continue
        if x == 0: b.append((F(0), F(0))); continue
        lo, hi = max(F(0), x - r), x + r
        if name.startswith('rim'): hi = x          # box ∩ ball is covered by the box; for stage D keep the box inside the ball
        b.append((lo, hi))
    return b
def qbox_cal(name, kind, c):
    b = []
    for k, x in enumerate(c):
        x = F(x)
        if kind == 'H33' and k == 2: b.append((F(0), R)); continue
        if x == 0: b.append((F(0), F(0))); continue
        b.append((max(F(0), x - R), x + R))
    return b
def ev(kind, box, N):
    return {'W3': tri3.W3, 'H33': tri3.H33, 'C12': tri3.C12}[kind](box, N)
def tile(i, j): return (1 + F(11, 20)*i, 1 + F(11, 20)*(i+1)), (1 + F(5, 8)*j, 1 + F(5, 8)*(j+1))
def emit(rec): out.write(json.dumps(rec, default=str) + "\n"); out.flush(); print(json.dumps(rec, default=str), flush=True)
jobs = []
if stage in 'AB':
    jobs = [(i, j, p) for i in range(4) for j in range(8) for p in range(8)]
elif stage == 'C':
    jobs = [(i, j, p) for (i, j) in ((0, 0), (1, 3), (2, 5), (3, 7)) for p in range(8)]
elif stage == 'D':
    jobs = [(i, j, p) for (i, j) in ((0, 0), (1, 3), (2, 5), (3, 7)) for p in range(8)]
for idx, (i, j, p) in enumerate(jobs):
    if idx % nparts != part: continue
    name, kind, c = PATCH[p]; (s0, s1), (t0, t1) = tile(i, j); T0 = time.time()
    if stage == 'A':
        e = ev(kind, [(s0, s1), (t0, t1)] + qbox_cal(name, kind, c), 64)
        emit(dict(stage='A', tile=[i, j], patch=name, kind=kind, N=64, lo=float(e.lo), hi=float(e.hi), ok=bool(e.lo > 0), sec=round(time.time()-T0, 2)))
    elif stage == 'B':
        sm, tm = (s0 + s1)/2, (t0 + t1)/2; hs, ht = (s1 - s0)/128, (t1 - t0)/128
        for N in (64, 128, 256):
            e = ev(kind, [(sm - hs, sm + hs), (tm - ht, tm + ht)] + qbox_cal(name, kind, c), N)
            if e.lo > 0: break
        emit(dict(stage='B', tile=[i, j], patch=name, kind=kind, N=N, lo=float(e.lo), hi=float(e.hi), ok=bool(e.lo > 0), sec=round(time.time()-T0, 2)))
    elif stage == 'C':
        q = qbox_cal(name, kind, c); queue = [((s0, s1, t0, t1), 0, 64)]; leaves = evals = maxd = 0; status = 'COVERED'; maxN = 0
        while queue:
            if time.time() - T0 > 300: status = 'BUDGET'; break
            (a, b, cc, d), dep, N = queue.pop(); e = ev(kind, [(a, b), (cc, d)] + q, N); evals += 1
            if e.lo > 0: leaves += 1; maxd = max(maxd, dep); maxN = max(maxN, N); continue
            if e.hi < 0: status = 'NEGATIVE'; break
            w = tri3.enclose.last
            # split rule: compare the shape contribution with the angular one via a centre-point evaluation width
            sm, tm = (a + b)/2, (cc + d)/2
            pc = ev(kind, [(sm, sm), (tm, tm)] + q, N); angw = float(pc.hi - pc.lo); boxw = float(e.hi - e.lo)
            if boxw - angw > angw and dep < 10:
                queue += [((a, sm, cc, tm), dep+1, N), ((sm, b, cc, tm), dep+1, N), ((a, sm, tm, d), dep+1, N), ((sm, b, tm, d), dep+1, N)]
            elif N < 256: queue.append(((a, b, cc, d), dep, 2*N))
            else: status = 'UNRESOLVED'; break
        emit(dict(stage='C', tile=[i, j], patch=name, kind=kind, status=status, leaves=leaves, evals=evals, maxdepth=maxd, maxN=maxN,
                  remaining=len(queue), sec=round(time.time()-T0, 1)))
    elif stage == 'D':
        sm, tm = (s0 + s1)/2, (t0 + t1)/2; hs, ht = (s1 - s0)/128, (t1 - t0)/128; best = None
        for k in range(3, 10):
            r = F(1, 2**(k+1)); q = qbox(name, kind, c, r); okk = False
            for N in (64, 128, 256):
                e = ev(kind, [(sm - hs, sm + hs), (tm - ht, tm + ht)] + q, N)
                if e.lo > 0: okk = True; break
            if okk: best = (k, N); break
        emit(dict(stage='D', tile=[i, j], patch=name, kind=kind, largest_width_log2=None if best is None else -best[0], N=None if best is None else best[1], sec=round(time.time()-T0, 1)))
