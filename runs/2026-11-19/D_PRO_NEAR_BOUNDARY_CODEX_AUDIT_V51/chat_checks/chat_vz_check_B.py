import sys, gzip, glob, json, random, time, multiprocessing as mp
from math import factorial
from flint import arb, fmpq, ctx
ctx.prec = 128
NS = 24
a = [fmpq(4**n*factorial(n)**2, factorial(2*n+1)) for n in range(NS+2)]
q = [a[n]*fmpq(2*n*n+10*n+10, 2*n+3) for n in range(NS+1)]
U01 = arb(0).union(arb(1)); PI = arb.pi()
def clip(x, lo, hi):
    l = x.lower(); u = x.upper(); lo = arb(lo); hi = arb(hi)
    l = l if l > lo else lo; u = u if u < hi else hi
    return l.union(u)
def sqrtp(x):
    l = x.lower(); u = x.upper(); l = l if l > 0 else arb(0); return l.sqrt().union(u.sqrt())
def sq(x):
    lo = x.lower(); hi = x.upper(); zero = arb(0)
    if lo >= zero: return (lo*lo).union(hi*hi)
    if hi <= zero: return (hi*hi).union(lo*lo)
    m = hi if hi > -lo else -lo
    return zero.union(m*m)
def acos_safe(g):
    lo = g.lower(); hi = g.upper(); one = arb(1); zero = arb(0)
    lo = lo if lo > zero else zero; hi = hi if hi < one else one
    lo = lo if lo < one else one; hi = hi if hi > zero else zero
    return hi.acos().union(lo.acos())
def P_enc(g):
    h = (1-g)/2; S = 2*sum((arb(a[n])*h**n for n in range(NS+1)), arb(0)); return S + arb(0).union(4*arb(a[NS+1])*h**(NS+1))
def Q_enc(g):   # Q = sum q_n h^n, q_n <= a_M (n+4) tail (NP14): 0 <= Q - Q_N <= (2N+12) a_M h^M
    h = (1-g)/2; S = sum((arb(q[n])*h**n for n in range(NS+1)), arb(0)); return S + arb(0).union(arb(2*NS+12)*arb(a[NS+1])*h**(NS+1))
def cellsV(z0, z1):
    out = []
    for i in range(256):
        m0 = -1 + fmpq(2*i, 256); m1 = -1 + fmpq(2*(i+1), 256)
        sub = 16 if (m1 > z0 - fmpq(1, 8) and m0 < z1 + fmpq(1, 8)) else 1
        for j in range(sub):
            mu = arb(m0 + (m1-m0)*fmpq(j, sub)).union(arb(m0 + (m1-m0)*fmpq(j+1, sub)))
            for k in range(48): out.append((mu, PI*(arb(k)+U01)/48, (m1-m0)/sub))
    return out
CZ = [((arb(i)+U01)/512, PI*(arb(k)+U01)/64) for i in range(512) for k in range(64)]
def lowerV(box):
    l0, l1, r0, r1, z0, z1 = [fmpq(x, 2**20) for x in box]
    lam = arb(l0).union(arb(l1)); rho = arb(r0).union(arb(r1)); z = arb(z0).union(arb(z1)); e2 = 1/(lam*lam)
    tot = arb(0)
    for mu, ph, wm in cellsV(z0, z1):
        s = sqrtp(clip(1-mu*mu, 0, 1)); c = ph.cos(); A = sq(s-rho) + 2*rho*s*clip(1-c, 0, 2)
        D2 = A + lam*lam*sq(mu-z)
        if not D2.lower() > 0: return None
        D = D2.sqrt(); B = clip(clip(1-(1-e2)*mu*mu, 0, 1), e2.lower(), 1); rB = B.sqrt()
        k = 1 - z*mu - rho*s*c; g = clip(k/(D*rB), 0, 1); uz = clip(lam*(mu-z)/D, -1, 1)
        P = P_enc(g); J = g*P - acos_safe(g)**2; K = g*g*P
        tot += arb((mu*J - lam*rB*uz*K).lower())*arb(wm)
    return (tot*(PI/48)/(2*PI)).lower()
def lowerZ(box):
    l0, l1, r0, r1, z0, z1 = [fmpq(x, 2**20) for x in box]
    lam = arb(l0).union(arb(l1)); rho = arb(r0).union(arb(r1)); z = arb(z0).union(arb(z1)); e2 = 1/(lam*lam); L2 = lam*lam
    dl = clip(1 - rho*rho - z*z, 0, 1); tot = arb(0)
    for m, psi in CZ:
        s = sqrtp(clip(1-m*m, 0, 1)); ex = s*psi.cos(); ey = s*psi.sin()
        v = rho*ex + z*m; d = sqrtp(clip(dl + v*v, 0, 4)); C = 1 + (L2-1)*m*m
        ls = []; ws = []
        for sg in (1, -1):
            l = d - sg*v; xz = z + sg*l*m; xr2 = (rho + sg*l*ex)**2 + (l*ey)**2
            B1 = e2 + (1-e2)*clip(1-xz*xz, 0, 1); B2 = e2 + (1-e2)*clip(xr2, 0, 1)
            B = clip(B1, B2.lower(), B2.upper()) if B1.overlaps(B2) else B1
            T = 1/(C*B).sqrt(); g = clip(d*T, 0, 1)
            w = clip((1 - sg*v/d)/2, 0, 1) if d.lower() > 0 else U01
            br = z*(1-m*m) - rho*ex*m - sg*m*d*(L2-1)*(1-m*m)/C
            val = T*(P_enc(g)*L2*d*d*(1-m*m)/(C*C) - Q_enc(g)*br*br)
            ls.append(val.lower()); ws.append(w)
        l0_, l1_ = ls
        # lower of w+ L+ + w- L- with w+ + w- = 1: = Lmax - w_min_side*(Lmax - Lmin); use sup of weight on the smaller side
        if l0_ <= l1_: val = arb(l1_) - arb(ws[0].upper())*(arb(l1_) - arb(l0_))
        else: val = arb(l0_) - arb(ws[1].upper())*(arb(l0_) - arb(l1_))
        tot += arb(val.lower())
    return (tot/(512*64)).lower()
def bisect(b):
    l0, l1, r0, r1, z0, z1 = b; sc = [l1-l0, 4*(r1-r0), 4*(z1-z0)]; i = sc.index(max(sc))
    lo, hi = [(0, 1), (2, 3), (4, 5)][i]; mid = (b[lo]+b[hi])//2; c1 = list(b); c2 = list(b); c1[hi] = mid; c2[lo] = mid
    return [tuple(c1), tuple(c2)]
def check(item):
    name, mode, box = item; t = time.monotonic(); todo = [(box, 0)]; res = []; ok = True
    f = lowerV if mode == 'V' else lowerZ
    while todo:
        b, dep = todo.pop(); v = f(b)
        if v is not None and v > 0: res.append(float(v))
        elif dep < 4: todo += [(c, dep+1) for c in bisect(b)]
        else: ok = False; res.append(float('nan') if v is None else float(v))
    return {'name': name, 'mode': mode, 'box': box, 'confirmed': ok, 'children': len(res), 'min_lower': min(res), 'seconds': round(time.monotonic()-t, 1)}
if __name__ == '__main__':
    root = sys.argv[1]; L = {'V': [], 'Z': []}
    for k in 'VZ':
        for fn in sorted(glob.glob(f'{root}/ledgers/N3/{k}*.tsv.gz')):
            for ln in gzip.open(fn, 'rt'):
                if ln.startswith('path'): continue
                p = ln.rstrip('\n').split('\t')
                if p[14] == 'positive': L[k].append((fmpq(int(p[10]), 2**36), fn.split('/')[-1]+':'+p[0], tuple(int(x) for x in p[1:7])))
    items = []; random.seed(50)
    for k, nr in (('V', 10), ('Z', 6)):
        srt = sorted(L[k], key=lambda r: r[0])
        items += [(f"weak_{r[1]}", k, r[2]) for r in srt[:3]] + [(f"rand_{r[1]}", k, r[2]) for r in random.sample(L[k], nr)]
    with mp.Pool(2) as pool:
        for out in pool.imap(check, items): print(json.dumps(out), flush=True)
