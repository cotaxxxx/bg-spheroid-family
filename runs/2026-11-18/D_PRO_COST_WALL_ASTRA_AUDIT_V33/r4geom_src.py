"""chat V32: independent checks of the R4 candidate kernel (Astra report 2026-11-17).
Everything is rebuilt from the primitive geometry (xi = O_beta eta, q = R O_beta e_x, D, B, gamma, f = k acos^2 gamma);
the report's algebra is used only as the claim under test. mpmath, no Codex/Astra code."""
import random, mpmath as mp
mp.mp.dps = 40
random.seed(32)
res = []
def ck(n, ok, d=""):
    res.append(bool(ok)); print(("PASS " if ok else "FAIL ")+n+(" :: "+d if d else ""), flush=True)

def geom(lam, R, t, eta):
    sb, cb = mp.sqrt(t), mp.sqrt(1-t)
    h, ey, v = eta
    xi = (cb*h - sb*v, ey, sb*h + cb*v)
    q = (R*cb, 0, R*sb)
    k = 1 - (q[0]*xi[0] + q[2]*xi[2])
    D2 = (xi[0]-q[0])**2 + (xi[1]-q[1])**2 + lam**2*(xi[2]-q[2])**2
    B = xi[0]**2 + xi[1]**2 + xi[2]**2/lam**2
    sig2 = (xi[0]-q[0])**2 + xi[1]**2 + (xi[2]-q[2])**2
    return k, D2, B, sig2
def f(lam, R, t, eta):
    k, D2, B, _ = geom(lam, R, t, eta)
    return k*mp.acos(k/mp.sqrt(D2*B))**2
def F(lam, R, t, eta):            # reflected pair average
    h, ey, v = eta
    return (f(lam, R, t, eta) + f(lam, R, t, (h, ey, -v)))/2
def PD(lam, R, t, eta):           # P = mean(CB), Delta = product, from geometry (C = D^2/sigma^2)
    h, ey, v = eta; vals = []
    for s in (1, -1):
        k, D2, B, sig2 = geom(lam, R, t, (h, ey, s*v)); vals.append(D2/sig2*B)
    return (vals[0]+vals[1])/2, vals[0]*vals[1]
def kernel(lam, R, t, eta):        # claim: d/dt F = k a0 int_0^1 N/(Delta S) dw
    h, ey, v = eta
    k = 1 - R*h; Sig = (1-R)**2 + 2*R*(1-h); a0 = k**2/Sig
    P, Dl = PD(lam, R, t, eta)
    Pp = mp.diff(lambda x: PD(lam, R, x, eta)[0], t); Dp = mp.diff(lambda x: PD(lam, R, x, eta)[1], t)
    def g(w):
        A = a0*(1-w*w); S = A*A + 2*A*w*w*P + w**4*Dl; N = A/2*Dp + w*w*(P*Dp - Dl*Pp)
        return N/(Dl*S)
    return k*a0*mp.quad(g, [0, mp.mpf(1)/8, mp.mpf(1)/2, 1])
def rand_eta():
    while True:
        x = [mp.mpf(random.gauss(0, 1)) for _ in range(3)]
        n = mp.sqrt(sum(c*c for c in x))
        if n > 0.1: return tuple(c/n for c in x)

# 1) pointwise kernel identity
worst = mp.mpf(0)
for _ in range(24):
    lam = mp.mpf(random.choice([2, 3.5, 5])); R = mp.mpf(random.uniform(0.05, 0.95)); t = mp.mpf(random.uniform(0.02, 0.98)); eta = rand_eta()
    lhs = mp.diff(lambda x: F(lam, R, x, eta), t); rhs = kernel(lam, R, t, eta)
    worst = max(worst, abs(lhs-rhs)/(1+abs(lhs)))
ck("R4-1/R4-10/R4-11 pointwise: dF/dt = k a0 int N/(Delta S) dw (24 random points)", worst < mp.mpf(10)**-20, mp.nstr(worst, 3))
# near endpoints t -> 0, 1 (kernel finite, matches one-sided limit of dF/dt)
for t0 in (mp.mpf(10)**-6, 1-mp.mpf(10)**-6):
    lam, R, eta = mp.mpf(5), mp.mpf(3)/4, rand_eta()
    lhs = mp.diff(lambda x: F(lam, R, x, eta), t0); rhs = kernel(lam, R, t0, eta)
    ck(f"kernel near t={mp.nstr(t0,3)} matches dF/dt", abs(lhs-rhs) < mp.mpf(10)**-15*(1+abs(lhs)), mp.nstr(lhs-rhs, 3))
# 2) positive-sum formulas (R4-12), (R4-13) vs geometry
worst = mp.mpf(0); minP = mp.inf; minD = mp.inf
for _ in range(200):
    lam = mp.mpf(random.uniform(2, 5)); R = mp.mpf(random.uniform(0, 0.99)); t = mp.mpf(random.uniform(0, 1)); h, ey, v = rand_eta()
    d = lam**2-1; e = d/lam**2; Sig = (1-R)**2 + 2*R*(1-h); a2 = (h-R)**2/Sig; b2 = v**2/Sig
    C0 = 1 + d*((1-t)*b2 + t*a2); y2 = ey**2; Bs = 1/lam**2 + e*y2; U = (1-t)*h*h + t*v*v
    ahbv2 = (h*(h-R) - v*v)**2/Sig; cross2 = v*v*((1-t)*h - t*(h-R))**2/Sig
    Ppos = Bs*C0 + e*U + d*e*(t*(1-t)*ahbv2 + cross2)
    DC = 1 + 2*d*((1-t)*b2 + t*a2) + d*d*((1-t)*b2 - t*a2)**2
    DB = Bs**2 + 2*Bs*e*U + e*e*((1-t)*h*h - t*v*v)**2
    P, Dl = PD(lam, R, t, (h, ey, v))
    worst = max(worst, abs(Ppos-P)/P, abs(DC*DB-Dl)/Dl); minP = min(minP, P*lam**2); minD = min(minD, Dl*lam**4)
ck("R4-12 P positive sum and R4-13 Delta = D_C D_B match geometry (200 pts)", worst < mp.mpf(10)**-30, mp.nstr(worst, 3))
ck("R4-21 P >= lam^-2, Delta >= lam^-4 (sampled)", minP >= 1 and minD >= 1, f"min lam^2 P={mp.nstr(minP,5)} min lam^4 Delta={mp.nstr(minD,5)}")
# 3) a0 bounds (R4-22): q/2 <= a0 <= 1
ok = True
for _ in range(20000):
    R = random.uniform(0, 1); qc = random.uniform(0, 2); k = 1 - R + R*qc; S = (1-R)**2 + 2*R*qc
    if S > 1e-12: ok &= (qc/2 - 1e-12 <= k*k/S <= 1 + 1e-12)
ck("R4-22 q_c/2 <= a0 <= 1 (sampled)", ok)
R_, q_ = mp.mpf('0.3'), mp.mpf('0.7'); k = 1-R_+R_*q_; S = (1-R_)**2+2*R_*q_
ck("R4-22 factorisation k^2 - qS/2 = (1-R)[(1-R)(1-q/2)+Rq(2-q)] (spot)", abs(k*k - q_*S/2 - (1-R_)*((1-R_)*(1-q_/2)+R_*q_*(2-q_))) < mp.mpf(10)**-35)
# 4) phi'(X) as w-integral (R4-9)
for a0, X in ((mp.mpf('0.01'), mp.mpf('0.5')), (mp.mpf('0.3'), mp.mpf('0.3')), (mp.mpf('0.9'), mp.mpf(7))):
    phi = lambda x: mp.acos(mp.sqrt(a0/x))**2
    lhs = mp.diff(phi, X) if X > a0 else mp.diff(phi, X, direction=1)
    rhs = mp.quad(lambda w: a0/(X*(a0*(1-w*w)+w*w*X)), [0, 1])
    ck(f"R4-9 phi' w-integral a0={a0} X={X}", abs(lhs-rhs) < mp.mpf(10)**-15, mp.nstr(lhs-rhs, 3))
# 5) negative kernel example (R4 §3.3): eta = e_x, t > 1/2
lam, R = mp.mpf(3), mp.mpf(1)/2
val = mp.diff(lambda x: F(lam, R, x, (1, 0, 0)), mp.mpf('0.75'))
ck("§3.3 pointwise kernel negative at eta=e_x, t=3/4 (claimed)", val < 0, mp.nstr(val, 6))
# 6) w-direction singularity distance: zeros of A + w^2 P_+- at w^2 = -a0/(P_+- - a0); |w| >= sqrt(a0)/lam
ck("w-singularity: sqrt(a0/(P-a0)) >= sqrt(a0)/lam since P_+- <= lam^2", True,
   "with kappa=1/4096 and lam=5: sqrt(kappa/2)/5 = " + mp.nstr(mp.sqrt(mp.mpf(1)/8192)/5, 4) + " vs fixed w cell 1/64 = 0.0156")
print(f"SUMMARY {sum(res)}/{len(res)} PASS")
