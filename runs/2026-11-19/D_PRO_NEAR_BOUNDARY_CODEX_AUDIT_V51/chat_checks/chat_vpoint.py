import sys; sys.path.insert(0,'.')
import mpmath as mp
mp.mp.dps = 20
from chat_nb_B import lowerV2
def Ez(lam, rho, z):
    lam = mp.mpf(lam); e2 = 1/lam**2
    def f(mu, ph):
        s = mp.sqrt(max(1-mu*mu, 0)); c = mp.cos(ph); D = mp.sqrt((s-rho)**2 + 2*rho*s*(1-c) + lam**2*(mu-z)**2)
        B = e2 + (1-e2)*(1-mu*mu); rB = mp.sqrt(B); k = 1 - z*mu - rho*s*c; g = min(max(k/(D*rB), 0), 1)
        a = mp.acos(g); P = 2*a/mp.sin(a) if a > 0 else mp.mpf(2); J = g*P - a*a; K = g*g*P; uz = lam*(mu-z)/D
        return mu*J - lam*rB*uz*K
    z = mp.mpf(z); bp = [-1, z-0.05, z-0.005, z, z+0.005, z+0.05, 1]
    return mp.quad(f, bp, [0, 0.005, 0.05, 0.5, mp.pi])/(2*mp.pi)
for lam, rho, z in [(1.0039, 0.95459, 0.25494), (1.07, 0.9670, 0.2507), (1.02, 0.9560, 0.2930), (1.0, 0.0, 0.25), (1.0, 0.95, 0.25)]:
    v = Ez(lam, rho, z); n = 2**20
    pb = tuple(int(round(x*n)) for x in (lam, lam, rho, rho, z, z))
    print(lam, rho, z, 'Ez_ref', mp.nstr(v, 8), 'Ez/z', mp.nstr(v/z, 6), 'lowerV2(point)', lowerV2(pb), flush=True)
