"""chat check of the needle-limit claim: (1) exact 1D representation vs chat's primitive E(0);
(2) lemma lim [int_0^T F - pi log T] = pi(1 - log 2), F = pi^2/4 - atan^2 x; (3) Delta vs pi(log t + 1)/t, t = lam - 1/lam."""
import mpmath as mp
mp.mp.dps = 30
def E0_primitive(lam):
    lam = mp.mpf(lam)
    f = lambda mu: mp.acos(min(mp.mpf(1), lam/(mp.sqrt(lam**2*(1-mu*mu)+mu*mu)*mp.sqrt((1-mu*mu)+lam**2*mu*mu))))**2
    pts = sorted(set([0, 1] + [mp.mpf(10)**(-k) for k in range(1, 9)] + [1-mp.mpf(10)**(-k) for k in range(1, 9)]))
    return mp.quad(f, pts)
def E0_1d(lam):
    t = mp.mpf(lam) - 1/mp.mpf(lam)
    pts = sorted(set([0, 1] + [mp.mpf(10)**(-k) for k in range(1, 9)] + [1-mp.mpf(10)**(-k) for k in range(1, 9)]))
    return mp.quad(lambda u: mp.atan(t*u*mp.sqrt(1-u*u))**2, pts)
for lam in (2, 5, 100):
    a, b = E0_primitive(lam), E0_1d(lam)
    print(f"(1) lam={lam}: primitive {mp.nstr(a,20)}  1D {mp.nstr(b,20)}  diff {mp.nstr(a-b,3)}")
F = lambda x: mp.pi**2/4 - mp.atan(x)**2
for T in (mp.mpf(10)**3, mp.mpf(10)**6, mp.mpf(10)**9):
    v = mp.quad(F, [0, 1, 10, 100, 1000, T]) - mp.pi*mp.log(T)
    print(f"(2) T={mp.nstr(T,3)}: int_0^T F - pi log T = {mp.nstr(v,15)}  target pi(1-log2) = {mp.nstr(mp.pi*(1-mp.log(2)),15)}")
for lam in (10, 100, 1000, 10**4, 10**5):
    t = mp.mpf(lam) - 1/mp.mpf(lam); D = mp.pi**2/4 - E0_1d(lam); A = mp.pi*(mp.log(t)+1)/t
    print(f"(3) lam={lam}: Delta={mp.nstr(D,12)}  pi(log t+1)/t={mp.nstr(A,12)}  t*(Delta-A)={mp.nstr(t*(D-A),6)}  t^2*(Delta-A)/log(t)^2={mp.nstr(t*t*(D-A)/mp.log(t)**2,6)}")
