"""chat probe (numerical, not proof): needle limit of E at the centre, E(0) vs pi^2/4 as lambda grows."""
import mpmath as mp
mp.mp.dps = 20
def E0(lam):
    lam = mp.mpf(lam)
    def f(mu):   # p = 0: azimuthally symmetric; h = lam*k with k = 1, D^2 = (1-mu^2) + lam^2 mu^2
        w = mp.sqrt(lam**2*(1-mu*mu)+mu*mu); D = mp.sqrt((1-mu*mu)+lam**2*mu*mu)
        return mp.acos(min(mp.mpf(1), lam/(w*D)))**2
    pts = sorted(set([-1, 1, 0] + [s*mp.mpf(10)**(-k) for s in (-1, 1) for k in range(1, 7)]))
    return mp.quad(f, pts)/2      # (1/4pi) * 2pi * int dmu
for lam in (1, 2, 5, 20, 100, 1000, 10000):
    e = E0(lam); print(f"lam={lam:>6}  E(0)={mp.nstr(e,10)}  pi^2/4-E={mp.nstr(mp.pi**2/4-e,8)}  lam*(pi^2/4-E)={mp.nstr(lam*(mp.pi**2/4-e),8)}")
