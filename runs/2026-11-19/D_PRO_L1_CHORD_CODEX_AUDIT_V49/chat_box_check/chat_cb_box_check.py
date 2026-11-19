"""chat V49 (2): independent Arb upper enclosure of H over Codex cover leaves, chord formula (3) directly. Plan: CHAT_PLAN_V49_BOX_CHECK.md"""
import sys, gzip, json, random, time, multiprocessing as mp
from math import factorial
from flint import arb, fmpq, ctx
ctx.prec = 128
NQ = 16
a = [fmpq(4**n*factorial(n)**2, factorial(2*n+1)) for n in range(NQ+2)]
q = [a[n]*fmpq(2*n*n+10*n+10, 2*n+3) for n in range(NQ+1)]
NM, NP = 256, 32
U01 = arb(0).union(arb(1))
def Fp_hi(g):
    h = (1-g)/2; return 2*sum((arb(a[n])*h**n for n in range(NQ+1)), arb(0)) + 4*arb(a[NQ+1])*h**(NQ+1)
def Q_lo(g):
    h = (1-g)/2; return sum((arb(q[n])*h**n for n in range(NQ+1)), arb(0))
def sqrtp(x):
    lo = x.lower(); hi = x.upper()
    lo = lo if lo > 0 else arb(0)
    return lo.sqrt().union(hi.sqrt())
def clip(x, lo, hi):
    return x.intersection(arb(lo).union(arb(hi)))
PI = arb.pi()
CELLS = []
for i in range(NM):
    m = (arb(i) + U01)/NM
    for k in range(NP):
        psi = PI*(arb(k) + U01)/NP
        CELLS.append((m, psi))
def H_upper(box):
    l0, l1, r0, r1, z0, z1 = [fmpq(x, 4096) for x in box]
    lam = arb(l0).union(arb(l1)); rho = arb(r0).union(arb(r1)); z = arb(z0).union(arb(z1))
    e2 = 1/(lam*lam); L2 = lam*lam
    dl = 1 - rho*rho - z*z
    dl = dl.intersection(arb(0).union(arb(1)))      # leaves lie in the closed unit disc
    tot = arb(0)
    for m, psi in CELLS:
        s = sqrtp(clip(1 - m*m, 0, 1)); ex = s*psi.cos(); ey = s*psi.sin(); j = ey*ey
        v = rho*ex + z*m; d = sqrtp(clip(dl + v*v, 0, 4)); C = 1 + (L2-1)*m*m; U = 1 - 1/C
        val = arb(0)
        for sg in (1, -1):
            l = d - sg*v; xz = z + sg*l*m
            B = clip(1 - (1-e2)*xz*xz, 0, 1); B = B.intersection(e2.union(arb(1)))
            g = clip(d/(C*B).sqrt(), 0, 1)
            w = clip((1 - sg*v/d)/2, 0, 1) if not (d.lower() <= 0) else U01
            pos = d*d*(1 - j/C)/C**fmpq(3,2)*Fp_hi(g)/B.sqrt()
            neg = j*(d*U - sg*v)**2/C.sqrt()*Q_lo(g)/B.sqrt()
            val += w*(pos - neg)
        tot += arb(val.upper())
    return tot.upper()/(NM*NP)      # cell measure: (1/NM)(pi/NP)/pi
def score(b):
    l0, l1, r0, r1, z0, z1 = b; return [8*(r1-r0), 8*(z1-z0), l1-l0]
def bisect(b):
    sc = score(b); i = sc.index(max(sc)); b = list(b)
    lo, hi = {0: (2, 3), 1: (4, 5), 2: (0, 1)}[i]
    mid = (b[lo]+b[hi])//2; c1 = list(b); c2 = list(b); c1[hi] = mid; c2[lo] = mid
    return [tuple(c1), tuple(c2)]
def check(item):
    name, box = item; t = time.monotonic(); todo = [(box, 0)]; leaves = []; ok = True
    while todo:
        b, dep = todo.pop()
        u = H_upper(b)
        if u < 0: leaves.append((b, float(u)))
        elif dep < 4: todo += [(c, dep+1) for c in bisect(b)]
        else: ok = False; leaves.append((b, float(u)))
    return {'name': name, 'box': box, 'confirmed': ok and all(x[1] < 0 for x in leaves), 'children': len(leaves),
            'max_upper': max(x[1] for x in leaves), 'seconds': round(time.monotonic()-t, 1)}
if __name__ == '__main__':
    root = sys.argv[1]; rows = []
    for k in (5, 6, 7):
        with gzip.open(f"{root}/cover_{k}.tsv.gz", 'rt') as f:
            for ln in f:
                if ln.startswith('#') or ln.startswith('path'): continue
                p = ln.rstrip('\n').split('\t')
                if p[9] == 'negative': rows.append((f"c{k}:{p[0]}", tuple(int(x) for x in p[1:7]), fmpq(int(p[10]), int(p[11]))))
    worst = [max((r for r in rows if r[0].startswith(f"c{k}:")), key=lambda r: r[2]) for k in (5, 6, 7)]
    random.seed(49); sample = random.sample(rows, 20)
    items = [("worst_"+r[0], r[1]) for r in worst] + [("rand_"+r[0], r[1]) for r in sample]
    with mp.Pool(4) as pool:
        for out in pool.imap(check, items):
            print(json.dumps(out), flush=True)
