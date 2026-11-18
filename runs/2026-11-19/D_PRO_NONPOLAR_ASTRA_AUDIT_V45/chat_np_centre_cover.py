"""chat V45: independent re-implementation (own code, not Astra's) of the centre lemma (NP17)+(NP13), N=4:
H(0;lambda) <= U_4 = int_0^1 sqrt(B)/D [P4+ Abar - Q4- Cbar] dmu, rigorous range x area over theta cells.
eps in [1/64, 1/5] split in 128, theta in [0, pi/2] split in 2048. Arb 128 bit."""
import sys, json, time, multiprocessing as mp
from flint import arb, fmpq, ctx
ctx.prec = 128
from math import factorial
N = 4; M = N + 1
a = [fmpq(4**n * factorial(n)**2, factorial(2*n+1)) for n in range(M+1)]
q = [a[n] * fmpq(2*n*n + 10*n + 10, 2*n + 3) for n in range(N+1)]
NT = 2048
def box(i):
    e = arb(fmpq(1,64)) + (arb(fmpq(1,5)) - arb(fmpq(1,64))) * (arb(i) + arb(0).union(arb(1))) / 128
    lam2 = 1 / (e*e)
    tot = arb(0)
    half_pi = arb.pi() / 2
    for j in range(NT):
        th = half_pi * (arb(j) + arb(0).union(arb(1))) / NT
        mu = th.sin(); c = th.cos()
        mu2 = mu*mu; s2 = c*c
        D2 = 1 + (lam2 - 1) * mu2
        B = 1 - (1 - e*e) * mu2
        D = D2.sqrt(); rB = B.sqrt()
        g = 1 / (D * rB)
        g = g.intersection(arb(0).union(arb(1)))
        h = (1 - g) / 2
        P = 2 * sum((arb(a[n]) * h**n for n in range(N+1)), arb(0)) + 4 * arb(a[M]) * h**M
        Qm = sum((arb(q[n]) * h**n for n in range(N+1)), arb(0))
        Abar = g*g * (1 - s2 / (2*D2))
        Cbar = s2 / (2*B) * (1 - 1/D2)**2
        f = rB / D * (P * Abar - Qm * Cbar) * c      # dmu = cos(theta) dtheta
        tot += f
    U = tot * half_pi / NT
    return i, U.upper().fmpq()
if __name__ == '__main__':
    t = time.monotonic()
    with mp.Pool(4) as p: rows = p.map(box, range(128))
    mx = max(rows, key=lambda r: r[1])
    print(json.dumps({'boxes': len(rows), 'all_upper_negative': all(r[1] < 0 for r in rows),
                      'max_upper': int(mx[1].p)/int(mx[1].q), 'max_upper_exact': str(mx[1]), 'argmax': mx[0],
                      'seconds': round(time.monotonic()-t, 1)}))
