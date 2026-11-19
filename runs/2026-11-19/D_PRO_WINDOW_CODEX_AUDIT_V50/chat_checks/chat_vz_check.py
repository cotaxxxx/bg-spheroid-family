import sys, gzip, glob, json, random, time, multiprocessing as mp
from math import factorial
from flint import arb, fmpq, ctx
ctx.prec = 128
NS = 24
a = [fmpq(4**n*factorial(n)**2, factorial(2*n+1)) for n in range(NS+2)]
U01 = arb(0).union(arb(1)); PI = arb.pi(); NMU, NPH = 256, 48
def clip(x, lo, hi):
    l = x.lower(); u = x.upper(); lo = arb(lo); hi = arb(hi)
    l = l if l > lo else lo; u = u if u < hi else hi
    return l.union(u)
def sqrtp(x):
    l = x.lower(); u = x.upper(); l = l if l > 0 else arb(0); return l.sqrt().union(u.sqrt())
def Fp(g):
    h = (1-g)/2; S = 2*sum((arb(a[n])*h**n for n in range(NS+1)), arb(0))
    return S + arb(0).union(4*arb(a[NS+1])*h**(NS+1))
def Fpp(g):
    h = (1-g)/2; S = -sum((arb(n*a[n])*h**(n-1) for n in range(1, NS+1)), arb(0))
    M = NS+1; return S - arb(0).union(arb(a[M])*h**(M-1)*(2*M+2))
def F(g):
    return PI*PI/4 - g.acos()**2
def build_cells(zlo, zhi):
    cells = []
    for i in range(NMU):
        m0 = -1 + fmpq(2*i, NMU); m1 = -1 + fmpq(2*(i+1), NMU)
        near = (m1 > zlo - fmpq(1, 8)) and (m0 < zhi + fmpq(1, 8))
        sub = 16 if near else 1
        for j in range(sub):
            mu = arb(m0 + (m1-m0)*fmpq(j, sub)).union(arb(m0 + (m1-m0)*fmpq(j+1, sub)))
            wmu = (m1-m0)/sub
            for k in range(NPH):
                cells.append((mu, PI*(arb(k) + U01)/NPH, wmu))
    return cells
def lower(mode, box):
    l0, l1, r0, r1, z0, z1 = [fmpq(x, 2**20) for x in box]
    lam = arb(l0).union(arb(l1)); rho = arb(r0).union(arb(r1)); z = arb(z0).union(arb(z1)); e = 1/lam; e2 = e*e
    tot = arb(0)
    for mu, ph, wmu in build_cells(z0, z1):
        s = sqrtp(clip(1-mu*mu, 0, 1)); c = ph.cos()
        A = (s - rho)**2 + 2*rho*s*clip(1 - c, 0, 2); w = mu - z; d2 = w*w + e2*A
        if not (d2.lower() > 0): return None
        d = d2.sqrt(); B = clip(1 - (1-e2)*mu*mu, 0, 1); B = clip(B, e2.lower(), 1); rB = B.sqrt()
        k = 1 - z*mu - rho*s*c; g = clip(e*k/(d*rB), 0, 1)
        P = Fp(g)
        if mode == 'V':
            val = mu*(F(g) + g*P) - k*g*P*w/d2
        else:
            Pp = Fpp(g); Q = 2*P + g*Pp; V = k*w/d2
            val = (mu*Q - V*(P + g*Pp))*e*(-mu + V)/(rB*d) - g*P*(-mu*w/d2 - k/d2 + 2*k*w*w/(d2*d2))
        tot += arb(val.lower())*arb(wmu)
    return (tot*(PI/NPH)/(2*PI)).lower()
def bisect(b):
    l0, l1, r0, r1, z0, z1 = b; sc = [l1-l0, 4*(r1-r0), 4*(z1-z0)]; i = sc.index(max(sc))
    lo, hi = [(0, 1), (2, 3), (4, 5)][i]; m = (b[lo]+b[hi])//2; c1 = list(b); c2 = list(b); c1[hi] = m; c2[lo] = m
    return [tuple(c1), tuple(c2)]
def check(item):
    name, mode, box = item; t = time.monotonic(); todo = [(box, 0)]; res = []; ok = True
    while todo:
        b, dep = todo.pop(); v = lower(mode, b)
        if v is not None and v > 0: res.append(float(v))
        elif dep < 4: todo += [(c, dep+1) for c in bisect(b)]
        else: ok = False; res.append(float('nan') if v is None else float(v))
    return {'name': name, 'mode': mode, 'box': box, 'confirmed': ok, 'children': len(res), 'min_lower': min(res), 'seconds': round(time.monotonic()-t, 1)}
if __name__ == '__main__':
    root = sys.argv[1]; L = {'V': [], 'Z': []}
    for k in 'VZ':
        for f in sorted(glob.glob(f'{root}/ledgers/N3/{k}*.tsv.gz')):
            for ln in gzip.open(f, 'rt'):
                if ln.startswith('path'): continue
                p = ln.rstrip('\n').split('\t')
                if p[14] == 'positive': L[k].append((fmpq(int(p[10]), 2**36), f.split('/')[-1]+':'+p[0], tuple(int(x) for x in p[1:7])))
    items = []
    random.seed(50)
    for k, nrand in (('V', 10), ('Z', 6)):
        srt = sorted(L[k], key=lambda r: r[0])
        items += [(f"weak_{r[1]}", k, r[2]) for r in srt[:3]] + [(f"rand_{r[1]}", k, r[2]) for r in random.sample(L[k], nrand)]
    with mp.Pool(2) as pool:
        for out in pool.imap(check, items): print(json.dumps(out), flush=True)
