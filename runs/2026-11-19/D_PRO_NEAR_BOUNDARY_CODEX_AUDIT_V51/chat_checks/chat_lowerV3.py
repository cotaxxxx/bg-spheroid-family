import sys; sys.path.insert(0,'.')
from chat_vz_check_B import *
from flint import arb, fmpq
def cellsV3(z0, z1, KR=8, SUBR=16, SUB0=64, SUBM=16, BAND=fmpq(1,8), NM=256, NP=48):
    out = []
    for i in range(NM):
        m0 = -1 + fmpq(2*i, NM); m1 = -1 + fmpq(2*(i+1), NM)
        band = (m1 > z0 - BAND and m0 < z1 + BAND); sub = SUBM if band else 1
        for j in range(sub):
            mu = arb(m0 + (m1-m0)*fmpq(j, sub)).union(arb(m0 + (m1-m0)*fmpq(j+1, sub))); w = (m1-m0)/sub
            for k in range(NP):
                ns = (SUB0 if k == 0 else SUBR if k < KR else 1) if band else 1
                for r in range(ns): out.append((mu, PI*(arb(k*ns + r)+U01)/(NP*ns), w/ns))
    return out
def lowerV3(box, **kw):
    l0, l1, r0, r1, z0, z1 = [fmpq(x, 2**20) for x in box]
    lam = arb(l0).union(arb(l1)); rho = arb(r0).union(arb(r1)); z = arb(z0).union(arb(z1)); e2 = 1/(lam*lam); tot = arb(0)
    for mu, ph, wm in cellsV3(z0, z1, **kw):
        s = sqrtp(clip(1-mu*mu, 0, 1)); c = ph.cos(); A = sq(s-rho) + 2*rho*s*clip(1-c, 0, 2); D2 = A + lam*lam*sq(mu-z)
        B = clip(clip(1-(1-e2)*mu*mu, 0, 1), e2.lower(), 1); rB = B.sqrt()
        if D2.lower() > 0:
            D = D2.sqrt(); k = 1 - z*mu - rho*s*c; g = clip(k/(D*rB), 0, 1); uz = clip(lam*(mu-z)/D, -1, 1)
        else: g = U01; uz = 2*U01 - 1
        P = P_enc(g); J = g*P - acos_safe(g)**2; K = g*g*P
        tot += arb((mu*J - lam*rB*uz*K).lower())*arb(wm)
    return (tot*(PI/kw.get('NP',48))/(2*PI)).lower()
if __name__ == '__main__':
    import time
    n = 2**20; pb = tuple(int(round(x*n)) for x in (1.0039, 1.0039, 0.95459, 0.95459, 0.25494, 0.25494))
    for kw in [dict(NM=512, NP=96, SUBM=8, KR=8, SUBR=8, SUB0=32, BAND=fmpq(1,4)), dict(NM=1024, NP=192, SUBM=4, KR=16, SUBR=4, SUB0=16, BAND=fmpq(1,4))]:
        t = time.time(); print(kw, lowerV3(pb, **kw), round(time.time()-t, 1), flush=True)
