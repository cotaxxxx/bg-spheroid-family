"""chat V49: own rigorous (Arb) lower Darboux sums of N_c, N_e, N_p (Codex chord report §3) at lambda = 8 and 5.
Q(y) >= sum_{n<=N} q_n h^n, h=(1-y)/2 (all q_n > 0, NP12). Range x width over m-cells, m in [0,1]."""
from flint import arb, fmpq, ctx
from math import factorial
ctx.prec = 128
NQ = 14
a = [fmpq(4**n*factorial(n)**2, factorial(2*n+1)) for n in range(NQ+1)]
q = [a[n]*fmpq(2*n*n+10*n+10, 2*n+3) for n in range(NQ+1)]
def Qlo(y):
    h = (1-y)/2
    return sum((arb(q[n])*h**n for n in range(NQ+1)), arb(0))
def N_lower(lam, cells):
    l = arb(lam*lam-1).sqrt(); tot = [arb(0), arb(0), arb(0)]
    for i in range(cells):
        m = (arb(i) + arb(0).union(arb(1)))/cells
        x = l*m; C = 1 + x*x; U = 1 - 1/C; Y = (1-m*m)/2; J = (1-m*m)**2/8
        qC = Qlo(1/C.sqrt()); base = qC/C.sqrt()*l/cells        # dx = l dm
        for k, f in enumerate((U*U*Y, (1+U)**2*J, (1+U)**2*m*m*Y)):
            tot[k] += arb((base*f).lower())
    return tot
res = []
def ck(n, ok, d=""):
    res.append(bool(ok)); print(("PASS " if ok else "FAIL ")+n+(" :: "+d if d else ""), flush=True)
pi = arb.pi()
for lam, bounds in [(8, (fmpq(-1,20), fmpq(-2,5), fmpq(-3,5))), (5, (fmpq(1), fmpq(1), fmpq(-3,16)))]:
    Nc, Ne, Np = N_lower(lam, 4096)
    ub = [3*pi/4 - Nc, 3*pi/4 - Ne, pi/2 - Np]
    ok = all(u < arb(b) for u, b in zip(ub, bounds))
    ck(f"chord §3 lambda={lam}: uniform P bound minus rigorous lower N < claimed (c,e,p)", ok, ", ".join(f"{float(u.upper()):.5f} < {int(b.p)/int(b.q):.4f}" for u, b in zip(ub, bounds)))
print(f"SUMMARY {sum(res)}/{len(res)} PASS")
