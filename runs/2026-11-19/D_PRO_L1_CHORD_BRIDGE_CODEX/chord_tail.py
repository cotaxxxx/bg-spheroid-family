"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. One-dimensional lower Darboux sums for (C4)."""
import json
from time import perf_counter
from flint import arb, ctx, fmpq

ctx.prec = 96
N = 2048
targets = [fmpq(k,2) for k in (10,11,12,13,14,15,16,18,20)]
coeff = []
a = fmpq(1)
for n in range(13):
    nxt = a*fmpq(2*n+2,2*n+3)
    coeff.append(arb((4+2*n)*a-(n+1)*nxt))
    a = nxt


def lower_q(c):
    h = (1-1/c.sqrt())/2
    poly = coeff[-1]
    for coef in reversed(coeff[:-1]):
        poly = poly*h+coef
    return poly


def screen(lam):
    l2 = arb(lam**2-1)
    ell = l2.sqrt()
    neg = [arb(0) for _ in range(3)]
    for j in range(N):
        a2 = arb(fmpq(j*j,N*N))
        b2 = arb(fmpq((j+1)**2,N*N))
        ca,cb = 1+l2*a2,1+l2*b2
        weight = ell*lower_q(ca)/cb.sqrt()/N
        u = 1-1/ca
        hh = 1-b2
        neg[0] += weight*u*u*hh/2
        neg[1] += weight*(1+u)**2*hh**2/8
        neg[2] += weight*(1+u)**2*a2*hh/2
    pi=arb.pi()
    caps=[3*pi/4,3*pi/4,pi/2]
    upper=[(p-n).upper().fmpq() for p,n in zip(caps,neg)]
    return dict(lam=str(lam),upper_exact=[str(q) for q in upper],
                upper_approx=[float(q.p)/float(q.q) for q in upper],
                all_negative=all(q<0 for q in upper))


if __name__ == "__main__":
    start=perf_counter()
    print(json.dumps({"status":"DIAGNOSTIC_ONLY / NOT_EVIDENCE","n":N,"prec":ctx.prec}),flush=True)
    for lam in targets:
        print(json.dumps(screen(lam)),flush=True)
    print(json.dumps({"wall_seconds":round(perf_counter()-start,3)}))
