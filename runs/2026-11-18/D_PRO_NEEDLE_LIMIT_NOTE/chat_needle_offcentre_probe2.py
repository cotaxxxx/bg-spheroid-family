"""chat probe (numerical, not proof): needle limit off the centre. Delta(q) = pi^2/4 - E(q) at reference point q
(physical p = (q_rho, lambda q_z)); is lambda*Delta ~ a(q) log(lambda) + b(q), and does a(q) depend on q?"""
import mpmath as mp
mp.mp.dps = 18
def E(lam, qr, qz):
    lam = mp.mpf(lam); px, pz = mp.mpf(qr), lam*mp.mpf(qz)
    def f(mu, phi):
        s = mp.sqrt(1-mu*mu); xi = s*mp.cos(phi); eta = s*mp.sin(phi)
        w = mp.sqrt(lam**2*(1-mu*mu)+mu*mu); h = lam*(1-px*xi)-pz*mu
        D = mp.sqrt((xi-px)**2+eta**2+(lam*mu-pz)**2)
        return h*mp.acos(min(mp.mpf(1), h/(w*D)))**2
    c = mp.mpf(qz)
    mus = sorted(set([-1, 1] + [min(1, max(-1, c + sg*mp.mpf(10)**(-k))) for sg in (-1, 1) for k in range(0, 6)] + [c]))
    return 2*mp.quad(f, mus, [0, mp.pi/4, mp.pi/2, 3*mp.pi/4, mp.pi])/(4*mp.pi*lam)
for (qr, qz) in ((0.5, 0.5), (0.3, 0.7), (0, 0.8)):
    vals = []
    for lam in (1000, 10000, 100000):
        d = mp.pi**2/4 - E(lam, qr, qz); vals.append((lam, lam*d))
    slope = (vals[2][1]-vals[1][1])/mp.log(10)
    print(f"q=({qr},{qz}): lambda*Delta at 1e2,1e3,1e4 = {[mp.nstr(v,7) for _, v in vals]}  slope per ln(lambda) (1e3->1e4) = {mp.nstr(slope,6)}  (centre pi = {mp.nstr(mp.pi,6)})", flush=True)
for (qr, qz) in ((0, 0), (0.5, 0), (0.8, 0), (0, 0.5), (0.5, 0.5), (0.3, 0.7), (0, 0.8)):
    print(f"candidate a(q) = pi sqrt(1-z^2)(1 - z^2 + rho^2/2) at ({qr},{qz}) = {mp.nstr(mp.pi*mp.sqrt(1-qz**2)*(1-qz**2+qr**2/2),6)}")
