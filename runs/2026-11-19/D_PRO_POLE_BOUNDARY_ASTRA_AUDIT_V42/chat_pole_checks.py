"""chat V42: independent checks of Astra's pole report.
(1) P8 pole lemma: lambda*E_z >= 1/4 at lambda = 256 in the layer 1-z^2 <= lambda^-2, from chat's own primitive E
    (reference coords; E = (1/4pi) int k acos^2(k/(D sqrt B)) dOmega), finite differences in z; axis (1D) and off-axis (2D).
(2) P19 transport identity vs direct E_z (P3-free: FD of primitive E) on the axis at lambda=5, z=0.9.
(3) P13: max |G''(u)| on [0,1).  (4) P18 cap integral formula (closed form vs quadrature)."""
import mpmath as mp
res = []
def ck(n, ok, d=""):
    res.append(bool(ok)); print(("PASS " if ok else "FAIL ")+n+(" :: "+d if d else ""), flush=True)
def E_axis(lam, z):
    lam = mp.mpf(lam); e = 1-1/lam**2
    def f(mu):
        k = 1-z*mu; D = mp.sqrt(1-2*z*mu+z*z + (lam**2-1)*(mu-z)**2); B = 1-e*mu*mu
        return k*mp.acos(min(mp.mpf(1), k/(D*mp.sqrt(B))))**2
    pts = sorted(set([-1, 1] + [min(1, max(-1, z + sg*mp.mpf(10)**(-j))) for sg in (-1, 1) for j in range(1, 14)] + [z]))
    return mp.quad(f, pts)/2
def E_2d(lam, r, z):
    lam = mp.mpf(lam); e = 1-1/lam**2
    def f(mu, ph):
        s = mp.sqrt(1-mu*mu); x = s*mp.cos(ph); y = s*mp.sin(ph)
        k = 1-r*x-z*mu; D = mp.sqrt((x-r)**2+y*y+(mu-z)**2 + (lam**2-1)*(mu-z)**2); B = 1-e*mu*mu
        return k*mp.acos(min(mp.mpf(1), k/(D*mp.sqrt(B))))**2
    mus = sorted(set([-1, 1] + [min(1, max(-1, z + sg*mp.mpf(10)**(-j))) for sg in (-1, 1) for j in range(1, 9)] + [z]))
    return 2*mp.quad(f, mus, [0, mp.pi/8, mp.pi/4, mp.pi/2, mp.pi])/(4*mp.pi)
mp.mp.dps = 40
lam = 256
for X in (1, mp.mpf(1)/4, mp.mpf(1)/100):
    z = mp.sqrt(1 - mp.mpf(X)/lam**2); h = mp.mpf(10)**-12
    Ez = (E_axis(lam, z+h) - E_axis(lam, z-h))/(2*h)
    ck(f"P8 axis lambda=256, 1-z^2={mp.nstr(mp.mpf(X),3)}/lambda^2: lambda*E_z >= 1/4", lam*Ez >= mp.mpf(1)/4, f"lambda*E_z = {mp.nstr(lam*Ez,10)}")
mp.mp.dps = 20
z = mp.sqrt(1 - mp.mpf(1)/lam**2); r = mp.sqrt(1-z*z)/2; h = mp.mpf(10)**-7
Ez = (E_2d(lam, r, z+h) - E_2d(lam, r, z-h))/(2*h)
ck("P8 off-axis lambda=256, chi=lambda^-2, rho=sqrt(chi)/2: lambda*E_z >= 1/4", lam*Ez >= mp.mpf(1)/4, f"lambda*E_z = {mp.nstr(lam*Ez,8)}")
# (2) P19 on the axis (rho = 0): chi E_z = (1/4pi) int [(3mu+z)k F - k gamma F' J_T]; eps = 1/lambda, A = s^2, d^2 = (mu-z)^2 + eps^2 s^2
mp.mp.dps = 30
lam = mp.mpf(5); z = mp.mpf('0.9'); eps = 1/lam
Fn = lambda y: mp.pi**2/4 - mp.acos(y)**2
Fp = lambda y: 2*mp.acos(y)/mp.sqrt(1-y*y) if y < 1 else mp.mpf(2)
def p19(mu):
    s2 = 1-mu*mu; k = 1-z*mu; A = s2; d2 = (mu-z)**2 + eps**2*A; B = s2 + eps**2*mu*mu
    g = eps*k/(mp.sqrt(d2)*mp.sqrt(B))
    JT = eps**2*(-z*A)/d2 + (1-eps**2)*mu*s2/B
    return (3*mu+z)*k*Fn(g) - k*g*Fp(g)*JT
pts = sorted(set([-1, 1, z] + [z + sg*mp.mpf(10)**(-j) for sg in (-1, 1) for j in range(1, 10)]))
lhs_p19 = mp.quad(p19, pts)/2/(1-z*z)               # (1/4pi) * 2pi * int dmu, divided by chi
h = mp.mpf(10)**-10
Ez_fd = (E_axis(lam, z+h) - E_axis(lam, z-h))/(2*h)
ck("P19 transport identity on the axis (lambda=5, z=0.9) vs FD of primitive E", abs(lhs_p19 - Ez_fd) < mp.mpf(10)**-8, f"P19 {mp.nstr(lhs_p19,14)}  FD {mp.nstr(Ez_fd,14)}")
# (3) P13
mp.mp.dps = 20
def G(u):
    def g(ph):
        L = 1-u*mp.cos(ph); D = mp.sqrt(1+u*u-2*u*mp.cos(ph))
        return L*(D*mp.log(D) - (D+L)*mp.log(D+L)) if D > 0 else mp.mpf(0)
    return mp.quad(g, [0, mp.mpf(1)/100, mp.pi/8, mp.pi/2, mp.pi])/mp.pi
mx = max(abs(mp.diff(G, u, 2)) for u in [mp.mpf(i)/20 for i in range(0, 20)] + [mp.mpf('0.99'), mp.mpf('0.999')])
ck("P13 |G''(u)| < 11 on sampled u in [0, 0.999]", mx < 11, f"max sampled |G''| = {mp.nstr(mx,6)}")
# (4) P18 cap
for R, kap in ((mp.mpf('0.6'), mp.mpf(1)/4096), (mp.mpf('0.999'), mp.mpf(1)/4096)):
    quad = mp.quad(lambda q: 12/mp.sqrt((1-R)**2 + 2*R*q), [0, kap])*2*mp.pi/(4*mp.pi)
    cf = 6/R*(mp.sqrt((1-R)**2 + 2*R*kap) - (1-R))
    ck(f"P18 cap integral at R={mp.nstr(R,4)}", abs(quad-cf) < mp.mpf(10)**-15 and cf <= 12*mp.sqrt(kap), f"{mp.nstr(cf,8)} <= 12 sqrt(kappa) = {mp.nstr(12*mp.sqrt(kap),8)}")
print(f"SUMMARY {sum(res)}/{len(res)} PASS")
