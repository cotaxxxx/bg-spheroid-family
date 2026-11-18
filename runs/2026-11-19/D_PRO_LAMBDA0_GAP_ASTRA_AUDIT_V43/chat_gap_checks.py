"""chat V43: independent checks of Astra's Lambda0-gap report, from chat's own primitive kernel.
(1) G1 at lambda=5,20 in the thin pole layer chi <= lambda^-2: lambda*E_z (FD of primitive E, 2D) >= 1/4.
(2) G12-G15 band lemma: -T f >= 0 (T = d_z + d_mu, f = k F(gamma)) at random points of (G11), lambda = 2^15.
(3) G8: the lower envelope L <= I s/eps at random points (exact kernel I from FD of f in z)."""
import mpmath as mp, random
random.seed(43)
res = []
def ck(n, ok, d=""):
    res.append(bool(ok)); print(("PASS " if ok else "FAIL ")+n+(" :: "+d if d else ""), flush=True)
Fn = lambda y: mp.pi**2/4 - mp.acos(y)**2
def f_kernel(lam, r, z, mu, ph):   # k F(gamma), reference coords, eps = 1/lam (G3)
    eps = 1/mp.mpf(lam); s = mp.sqrt(1-mu*mu); k = 1 - z*mu - r*s*mp.cos(ph); A = s*s + r*r - 2*r*s*mp.cos(ph)
    d = mp.sqrt((mu-z)**2 + eps**2*A); B = s*s + eps**2*mu*mu; g = eps*k/(d*mp.sqrt(B))
    return k*Fn(min(mp.mpf(1), g))
def E_2d(lam, r, z):
    def f(mu, ph): return f_kernel(lam, r, z, mu, ph)
    mus = sorted(set([-1, 1] + [min(1, max(-1, z + sg*mp.mpf(10)**(-j))) for sg in (-1, 1) for j in range(1, 9)] + [z]))
    return mp.pi**2/4 - 2*mp.quad(f, mus, [0, mp.pi/16, mp.pi/4, mp.pi/2, mp.pi])/(4*mp.pi)
# (1)
mp.mp.dps = 20
for lam in (5, 20):
    for w, u in ((1, 0), (1, mp.mpf('0.999')), (mp.mpf('0.5'), mp.mpf('0.5'))):
        eps = 1/mp.mpf(lam); z = mp.sqrt(1 - (eps*w)**2); r = eps*w*u; h = mp.mpf(10)**-8
        Ez = (E_2d(lam, r, z+h) - E_2d(lam, r, z-h))/(2*h)
        ck(f"G1 lambda={lam} w={mp.nstr(w,3)} u={mp.nstr(u,3)}: lambda*E_z >= 1/4", lam*Ez >= mp.mpf(1)/4, f"lambda*E_z = {mp.nstr(lam*Ez,8)}")
# (2)
mp.mp.dps = 50
lam = 2**15; eps = mp.mpf(1)/lam; worst = mp.inf
for _ in range(300):
    S = mp.mpf(2)**-12*(mp.mpf(1)/2 + mp.mpf(random.random())/2)       # S in [2^-13, 2^-12], S >= 4 eps holds
    z = mp.sqrt(1-S*S); r = S*mp.mpf(random.random()); hb = S*S/4
    mu = z + hb*(2*mp.mpf(random.random())-1); ph = mp.pi*mp.mpf(random.random())
    dd = mp.mpf(10)**-30
    Tf = (f_kernel(lam, r, z+dd, mu+dd, ph) - f_kernel(lam, r, z-dd, mu-dd, ph))/(2*dd)
    worst = min(worst, -Tf)
ck("G12-G15: -T f >= 0 in the band (300 random points, lambda = 2^15)", worst >= 0, f"min(-Tf) = {mp.nstr(worst,6)}")
# (3) G8 envelope
mp.mp.dps = 40
bad = 0
for _ in range(200):
    lam = random.choice([5, 20, 200]); eps = 1/mp.mpf(lam); w = mp.mpf(random.random()); u = mp.mpf(random.random())
    z = mp.sqrt(1-(eps*w)**2); r = eps*w*u; c = mp.mpf(3)/4
    th = mp.acos(c) + (mp.pi - mp.mpf(1)/64 - mp.acos(c))*mp.mpf(random.random()); mu = mp.cos(th); ph = mp.pi*mp.mpf(random.random())
    s = mp.sqrt(1-mu*mu); k = 1 - z*mu - r*s*mp.cos(ph); A = s*s + r*r - 2*r*s*mp.cos(ph)
    d = mp.sqrt((mu-z)**2 + eps**2*A); B = s*s + eps**2*mu*mu; g = eps*k/(d*mp.sqrt(B))
    dd = mp.mpf(10)**-20
    I = -(f_kernel(lam, r, z+dd, mu, ph) - f_kernel(lam, r, z-dd, mu, ph))/(2*dd)        # I = -d_z f  (E_z = (1/4pi) int I)
    T0 = s/mp.sqrt(B); f1 = mu*k; f2 = mu*k + k*k*(z-mu)/d**2
    Lw = T0/d*(mp.pi*(f1+f2) - g*(max(f1, 0) + 2*max(f2, 0)))
    if Lw > I*s/eps + mp.mpf(10)**-15: bad += 1
ck("G8: lower envelope <= I s/eps (200 random points in the kept region)", bad == 0, f"violations {bad}")
print(f"SUMMARY {sum(res)}/{len(res)} PASS")
