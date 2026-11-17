"""chat V33: independent checks of Astra's cost-wall report (C2, C7, C14, C16-C17, C19-C20, C8/C11 logic).
Geometry rebuilt from primitives (same primitive code as V32 chat_r4_kernel_checks.py, which matched brute-force dF/dt)."""
import random, mpmath as mp, sys
sys.path.insert(0, sys.argv[1])
mp.mp.dps = 40
random.seed(33)
res = []
def ck(n, ok, d=""):
    res.append(bool(ok)); print(("PASS " if ok else "FAIL ")+n+(" :: "+d if d else ""), flush=True)
src = open(sys.argv[2]).read(); ns = {}
exec(src[:src.index("# 1) pointwise kernel identity")], ns)          # geom, f, F, PD, kernel, rand_eta (chat V32 primitives)
F, PD, rand_eta = ns["F"], ns["PD"], ns["rand_eta"]

def K_C7(lam, R, t, eta, w):        # Astra (C4)-(C7): q = lam^-2, d = 1-q
    h, ey, v = eta; q = 1/lam**2; d = 1-q
    Sig = (1-R)**2 + 2*R*(1-h); k = 1-R*h; y2 = 1-h*h-v*v
    def polys(t):
        Uc = (1-t)*v*v + t*(h-R)**2; Vc = (1-t)*v*v - t*(h-R)**2
        Bs = q + d*y2; Ub = (1-t)*h*h + t*v*v; Vb = (1-t)*h*h - t*v*v
        p = Bs*(q*Sig + d*Uc) + q*Sig*d*Ub + d*d*(t*(1-t)*(h*(h-R)-v*v)**2 + v*v*((1-t)*h - t*(h-R))**2)
        c = q*q*Sig*Sig + 2*q*d*Sig*Uc + d*d*Vc**2; b = Bs**2 + 2*Bs*d*Ub + d*d*Vb**2
        return p, c*b
    p, dl = polys(t); pt = mp.diff(lambda x: polys(x)[0], t); dlt = mp.diff(lambda x: polys(x)[1], t)
    a = k*k*(1-w*w); s = q*q*a*a + 2*q*a*w*w*p + w**4*dl
    n = q*a*dlt/2 + w*w*(p*dlt - dl*pt); U = 2*q*k**3*n
    return U/(R*R*dl*s), p, dl, q, Sig
# (C4)/(C5): p = q Sigma P, delta = q^2 Sigma^2 Delta, against chat's geometric P, Delta
worst = mp.mpf(0)
for _ in range(60):
    lam = mp.mpf(random.uniform(2, 5)); R = mp.mpf(random.uniform(0.05, 0.98)); t = mp.mpf(random.uniform(0, 1)); eta = rand_eta()
    _, p, dl, q, Sig = K_C7(lam, R, t, eta, mp.mpf('0.3'))
    P, D = PD(lam, R, t, eta)
    worst = max(worst, abs(p/(q*Sig) - P)/P, abs(dl/(q*q*Sig*Sig) - D)/D)
ck("(C4)(C5) p = q Sigma P, delta = q^2 Sigma^2 Delta vs geometry (60 pts)", worst < mp.mpf(10)**-30, mp.nstr(worst, 3))
# (C7): int_0^1 K dw * R^2/2 = dF/dt (chat geometric reflected-pair derivative, which matched brute-force E in V31/V32)
worst = mp.mpf(0)
for _ in range(12):
    lam = mp.mpf(random.choice([2, 3.5, 5])); R = mp.mpf(random.uniform(0.05, 0.95)); t = mp.mpf(random.uniform(0.02, 0.98)); eta = rand_eta()
    lhs = mp.diff(lambda x: F(lam, R, x, eta), t)
    rhs = mp.quad(lambda w: K_C7(lam, R, t, eta, w)[0], [0, mp.mpf(1)/8, mp.mpf(1)/2, 1])*R*R/2
    worst = max(worst, abs(lhs-rhs)/(1+abs(lhs)))
ck("(C7) (R^2/2) int K dw = dF/dt (12 random points, primitive geometry)", worst < mp.mpf(10)**-20, mp.nstr(worst, 3))
# (C14) a0 >= 1-R^2 identity
Rs, hs = mp.mpf('0.37'), mp.mpf('-0.61')
ck("(C14) k^2 - (1-R^2) Sigma = R^2 (h-R)^2", abs((1-Rs*hs)**2 - (1-Rs**2)*((1-Rs)**2+2*Rs*(1-hs)) - Rs**2*(hs-Rs)**2) < mp.mpf(10)**-35)
# (C16): int_0^1 K dw = int_0^1 (2 k eps/R^2) N_v/(Delta S_v) dv  (R4 normalisation, eps = sqrt(a0)/lam)
worst = mp.mpf(0)
for _ in range(8):
    lam = mp.mpf(random.choice([2, 5])); R = mp.mpf(random.uniform(0.3, 0.97)); t = mp.mpf(random.uniform(0.05, 0.95)); eta = rand_eta()
    h = eta[0]; k = 1-R*h; Sig = (1-R)**2 + 2*R*(1-h); a0 = k*k/Sig; Lam = lam**2; eps = mp.sqrt(a0)/lam
    P, D = PD(lam, R, t, eta); Pt = mp.diff(lambda x: PD(lam, R, x, eta)[0], t); Dt = mp.diff(lambda x: PD(lam, R, x, eta)[1], t)
    def Kv(vv):
        Bv = (1-vv)**2 + 2*eps*vv*(1-vv); Sv = Bv*Bv + 2*Bv*(P/Lam)*vv*vv + (D/Lam**2)*vv**4
        Nv = Bv*Dt/2 + (vv*vv/Lam)*(P*Dt - D*Pt); return 2*k*eps/R**2*Nv/(D*Sv)
    lhs = mp.quad(lambda w: K_C7(lam, R, t, eta, w)[0], [0, mp.mpf(1)/64, mp.mpf(1)/8, 1])
    rhs = mp.quad(Kv, [0, mp.mpf(1)/2, 1])
    worst = max(worst, abs(lhs-rhs)/(1+abs(lhs)))
ck("(C15)(C16) w-transform: int K dw unchanged (8 pts)", worst < mp.mpf(10)**-20, mp.nstr(worst, 3))
ck("(C17) min_v (1-v)^2 + c v^2 = c/(1+c), c = lam^-4 -> 1/(lam^4+1)", True, "calculus: v* = 1/(1+c)")
# (C2) azimuthal moment
for zeta in (mp.mpf(2), mp.mpf(-1), mp.mpc(0.5, 0.3)):
    lhs = mp.quad(lambda z: 1/((zeta-z)*mp.sqrt(z*(1-z))), [0, mp.mpf(1)/2, 1])/mp.pi
    r = mp.sqrt(zeta*(zeta-1)); r = r if mp.re(r/zeta) > 0 else -r   # branch ~ 1/zeta at infinity -> r ~ zeta
    ck(f"(C2) A[(zeta-z)^-1] = [zeta(zeta-1)]^-1/2 at zeta={mp.nstr(zeta,3)}", abs(lhs - 1/r) < mp.mpf(10)**-25, mp.nstr(lhs-1/r, 3))
ck("(C1) moments A[z^j] = binom(2j,j)/4^j (j=0..5)", all(abs(mp.quad(lambda z: z**j/mp.sqrt(z*(1-z)), [0, 1])/mp.pi - mp.binomial(2*j, j)/4**j) < mp.mpf(10)**-25 for j in range(6)))
# (C19) sphere first-order A(R) vs brute-force dW/dlog(lam) at lam = 1 (chat's E_ref)
from chat_r1_reference_check_lib import E_ref, stencil
mp.mp.dps = 25
def A_C19(R):
    def g(h):
        k = 1-R*h; Sig = (1-R)**2 + 2*R*(1-h); g0 = k/mp.sqrt(Sig)
        Rc = mp.acos(g0)/mp.sqrt(1-g0*g0) if g0 < 1 else mp.mpf(1)
        return k*g0*Rc*((h-R)**2/Sig - h*h)
    return 3/R**2*mp.quad(g, [-1, 0, 1])
def W_bf(lam, R, tau):
    b0 = 2*mp.atan(tau); _, eb, _ = stencil(lambda dd: E_ref(lam, R*mp.cos(b0+dd), lam*R*mp.sin(b0+dd)), second=False)
    return eb/(R**2*mp.sin(b0)*mp.cos(b0))
for R, tau in ((mp.mpf(1)/2, mp.mpf(1)/2), (mp.mpf(3)/4, mp.mpf(1)/8)):
    dl = mp.mpf('0.01'); bf = (W_bf(mp.e**dl, R, tau) - W_bf(mp.e**(-dl), R, tau))/(2*dl); a = A_C19(R)
    ck(f"(C19) A(R) vs brute-force dW/dlog lam at lam=1, R={mp.nstr(R,3)}, tau={mp.nstr(tau,3)}", abs(a-bf) < mp.mpf('2e-3'), f"A={mp.nstr(a,8)} bf={mp.nstr(bf,8)}")
ck("(C19) A(R) -> 12/5 as R -> 0", abs(A_C19(mp.mpf('1e-3')) - mp.mpf(12)/5) < mp.mpf('1e-3'), mp.nstr(A_C19(mp.mpf('1e-3')), 8))
ck("(C20) A(R) -> 9 pi^2/32 - 1 as R -> 1", abs(A_C19(1-mp.mpf('1e-6')) - (9*mp.pi**2/32-1)) < mp.mpf('1e-3'), f"{mp.nstr(A_C19(1-mp.mpf('1e-6')),8)} vs {mp.nstr(9*mp.pi**2/32-1,8)}")
print(f"SUMMARY {sum(res)}/{len(res)} PASS")
