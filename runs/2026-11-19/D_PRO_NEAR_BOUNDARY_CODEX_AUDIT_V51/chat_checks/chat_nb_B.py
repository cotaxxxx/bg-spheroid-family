import sys, json, time
sys.path.insert(0,'.')
import chat_vz_check_B as V
import chat_nb_check as N
from chat_vz_check_B import *
from flint import arb, fmpq
def cellsV2(z0, z1):
    out = []
    for i in range(256):
        m0 = -1 + fmpq(2*i, 256); m1 = -1 + fmpq(2*(i+1), 256)
        band = (m1 > z0 - fmpq(1, 8) and m0 < z1 + fmpq(1, 8)); sub = 16 if band else 1
        for j in range(sub):
            mu = arb(m0 + (m1-m0)*fmpq(j, sub)).union(arb(m0 + (m1-m0)*fmpq(j+1, sub))); w = (m1-m0)/sub
            for k in range(48):
                if band and k == 0:
                    for r in range(32): out.append((mu, PI*(arb(r)+U01)/(48*32), w/32))
                else: out.append((mu, PI*(arb(k)+U01)/48, w))
    return out
def lowerV2(box):
    l0, l1, r0, r1, z0, z1 = [fmpq(x, 2**20) for x in box]
    lam = arb(l0).union(arb(l1)); rho = arb(r0).union(arb(r1)); z = arb(z0).union(arb(z1)); e2 = 1/(lam*lam); tot = arb(0)
    for mu, ph, wm in cellsV2(z0, z1):
        s = sqrtp(clip(1-mu*mu, 0, 1)); c = ph.cos(); A = sq(s-rho) + 2*rho*s*clip(1-c, 0, 2); D2 = A + lam*lam*sq(mu-z)
        B = clip(clip(1-(1-e2)*mu*mu, 0, 1), e2.lower(), 1); rB = B.sqrt()
        if D2.lower() > 0:
            D = D2.sqrt(); k = 1 - z*mu - rho*s*c; g = clip(k/(D*rB), 0, 1); uz = clip(lam*(mu-z)/D, -1, 1)
        else: g = U01; uz = 2*U01 - 1
        P = P_enc(g); J = g*P - acos_safe(g)**2; K = g*g*P
        tot += arb((mu*J - lam*rB*uz*K).lower())*arb(wm)
    return (tot*(PI/48)/(2*PI)).lower()
CY2 = [((arb(i)+U01)/1024, PI*(arb(k)+U01)/128) for i in range(1024) for k in range(128)]
def lowerZ2(box):
    V.CZ[:] = CY2; return V.lowerZ(box)
def test(kind, b):
    if kind == 'V': v = lowerV2(b); return v > 0, v
    if kind == 'Z': v = lowerZ2(b); return v > 0, v
    N.CY[:] = CY2; v = N.chord_bound(b, 'y', 'lower'); return v > 0, v
def run(item):
    nm, kind, box = item; t0 = time.monotonic(); todo = [(tuple(box), 0)]; vals = []; ok = True
    while todo:
        b, d = todo.pop()
        if b[2]*b[2] + b[4]*b[4] >= 2**40: continue
        good, v = test(kind, b)
        if good: vals.append(float(v))
        elif d < 8: todo += [(c, d+1) for c in N.bisect(b)]
        else: ok = False; vals.append(float(v)); todo = []
    return {'name': nm, 'kind': kind, 'confirmed': ok, 'children': len(vals), 'min': min(vals) if vals else None, 'seconds': round(time.monotonic()-t0, 1)}
if __name__ == '__main__':
    items = [(r['name'], r['kind'], r['box']) for r in map(json.loads, open('nb_check.jsonl')) if r['kind'] in ('V','Z','H') and not r['confirmed']]
    for it in sorted(items, key=lambda x: x[1] != 'V'): print(json.dumps(run(it)), flush=True)
