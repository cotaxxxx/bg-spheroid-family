import sys, gzip, glob, json, random, time, multiprocessing as mp
sys.path.insert(0, '.')
from chat_vz_check_B import *
from flint import arb, fmpq
CY = [((arb(i)+U01)/512, PI*(arb(k)+U01)/64) for i in range(512) for k in range(64)]
def chord_bound(box, comp, want):
    l0, l1, r0, r1, z0, z1 = [fmpq(x, 2**20) for x in box]
    lam = arb(l0).union(arb(l1)); rho = arb(r0).union(arb(r1)); z = arb(z0).union(arb(z1)); e2 = 1/(lam*lam); L2 = lam*lam
    dl = clip(1 - sq(rho) - sq(z), 0, 1); tot = arb(0)
    for m, psi in CY:
        s = sqrtp(clip(1-m*m, 0, 1)); ex = s*psi.cos(); ey = s*psi.sin()
        v = rho*ex + z*m; d = sqrtp(clip(dl + sq(v), 0, 4)); C = 1 + (L2-1)*m*m
        bs = []; ws = []
        for sg in (1, -1):
            l = d - sg*v; xz = z + sg*l*m; xr2 = sq(rho + sg*l*ex) + sq(l*ey)
            B1 = e2 + (1-e2)*clip(1-sq(xz), 0, 1); B2 = e2 + (1-e2)*clip(xr2, 0, 1)
            B = clip(B1, B2.lower(), B2.upper()) if B1.overlaps(B2) else B1
            T = 1/(C*B).sqrt(); g = clip(d*T, 0, 1)
            w = clip((1 - sg*v/d)/2, 0, 1) if d.lower() > 0 else U01
            ei = ey if comp == 'y' else ex; qi = 0 if comp == 'y' else rho
            br = qi + sg*ei*(l - d/C)
            val = T*(P_enc(g)*d*d/C*(1 - sq(ei)/C) - Q_enc(g)*sq(br))
            bs.append(val); ws.append(w)
        if want == 'lower':
            a_, b_ = bs[0].lower(), bs[1].lower()
            val = (arb(b_) - arb(ws[0].upper())*(arb(b_) - arb(a_))) if a_ <= b_ else (arb(a_) - arb(ws[1].upper())*(arb(a_) - arb(b_)))
            tot += arb(val.lower())
        else:
            a_, b_ = bs[0].upper(), bs[1].upper()
            val = (arb(b_) + arb(ws[0].upper())*(arb(a_) - arb(b_))) if a_ >= b_ else (arb(a_) + arb(ws[1].upper())*(arb(b_) - arb(a_)))
            tot += arb(val.upper())
    r = tot/(512*64); return r.lower() if want == 'lower' else r.upper()
CB = [((arb(i)+U01)/512, PI*(arb(k)+U01)/64) for i in range(512) for k in range(64)]
def hb_lower(box):
    l0, l1 = fmpq(box[0], 2**20), fmpq(box[1], 2**20); lam = arb(l0).union(arb(l1)); e2 = 1/(lam*lam); L2 = lam*lam; tot = arb(0)
    for t, ph in CB:
        co = ph.cos(); si = ph.sin(); m2 = (1 - t*t)*sq(co); j = (1 - t*t)*sq(si); C = 1 + (L2-1)*m2; c = 1/C
        B = clip(1 - 4*(1-e2)*t*t*m2, e2.lower(), 1); T = (c/B).sqrt(); g = clip(t*T, 0, 1)
        tot += arb((T*t*t*(P_enc(g)*c*(1 - j*c) - Q_enc(g)*j*sq(2 - c))).lower())
    return (tot/(512*64)).lower()
def bisect(b, onlyl=False):
    l0, l1, r0, r1, z0, z1 = b; sc = [l1-l0, 0 if onlyl else 4*(r1-r0), 0 if onlyl else 4*(z1-z0)]; i = sc.index(max(sc))
    lo, hi = [(0, 1), (2, 3), (4, 5)][i]; mid = (b[lo]+b[hi])//2; c1 = list(b); c2 = list(b); c1[hi] = mid; c2[lo] = mid
    return [tuple(c1), tuple(c2)]
def test(kind, b):
    if kind == 'H': v = chord_bound(b, 'y', 'lower'); return v > 0, v
    if kind == 'Exx': v = chord_bound(b, 'x', 'upper'); return v < 0, v
    if kind == 'Hb': v = hb_lower(b); return v > 0, v
    if kind == 'V': v = lowerV(b); return (v is not None and v > 0), v
    v = lowerZ(b); return v > 0, v
def check(item):
    name, kind, box = item; t0 = time.monotonic(); todo = [(box, 0)]; vals = []; ok = True
    while todo:
        b, dep = todo.pop(); good, v = test(kind, b)
        if good: vals.append(float(v))
        elif dep < 4: todo += [(c, dep+1) for c in bisect(b, kind == 'Hb')]
        else: ok = False; vals.append(float('nan') if v is None else float(v))
    return {'name': name, 'kind': kind, 'box': box, 'confirmed': ok, 'children': len(vals), 'extreme': (min(vals) if kind != 'Exx' else max(vals)), 'seconds': round(time.monotonic()-t0, 1)}
if __name__ == '__main__':
    root = sys.argv[1]; items = []; VL = []; ZL = []
    for fn in sorted(glob.glob(f'{root}/final/*.tsv.gz')):
        for ln in gzip.open(fn, 'rt'):
            if ln.startswith('path'): continue
            p = ln.rstrip('\n').split('\t'); box = tuple(int(x) for x in p[1:7]); nm = fn.split('/')[-1]+':'+p[0]
            if p[7] == 'E' and p[14] == 'H_positive': items.append((nm, 'H', box))
            elif p[7] == 'E' and p[14] == 'radial_curvature_negative': items.append((nm, 'Exx', box))
            elif p[7] == 'B' and p[14] == 'H_positive': items.append((nm, 'Hb', box))
            elif p[7] == 'V' and p[14] == 'positive': VL.append((fmpq(int(p[10]), 2**36), nm, box))
            elif p[7] == 'Z' and p[14] == 'positive': ZL.append((fmpq(int(p[10]), 2**36), nm, box))
    random.seed(51)
    sv = sorted(VL, key=lambda r: r[0]); sz = sorted(ZL, key=lambda r: r[0])
    items += [("weak_"+r[1], 'V', r[2]) for r in sv[:3]] + [("rand_"+r[1], 'V', r[2]) for r in random.sample(VL, 5)] + [("weak_"+r[1], 'Z', r[2]) for r in sz[:3]]
    with mp.Pool(2) as pool:
        for out in pool.imap(check, items): print(json.dumps(out), flush=True)
