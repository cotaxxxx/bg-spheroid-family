"""chat independent cross-check of Codex prolate_p3 kernel (auditor side).
Independent reference: brute-force 2D mpmath quadrature of the PRIMITIVE E (no derived kernel),
derivatives by Richardson central differences. Compares with Codex Ez_ball / Ezz_ball / V_box_lower."""
import sys, random, mpmath as mp
from flint import fmpq, arb
sys.path.insert(0, sys.argv[1])
from prolate_p3 import kernel as K

mp.mp.dps = 25
def E_ref(lam, px, pz):
    lam = mp.mpf(lam)
    def f(mu, phi):
        s = mp.sqrt(1-mu*mu); xi = s*mp.cos(phi); eta = s*mp.sin(phi)
        w = mp.sqrt(lam**2*(1-mu*mu)+mu*mu); h = lam*(1-px*xi)-pz*mu
        D = mp.sqrt((xi-px)**2+eta**2+(lam*mu-pz)**2)
        return h*mp.acos(h/(w*D))**2
    return 2*mp.quad(f, [-1, 0, 1], [0, mp.pi/2, mp.pi])/(4*mp.pi*lam)
def derivs(lam, px, pz, d=mp.mpf('0.004')):
    e = {k: E_ref(lam, px, pz+k*d) for k in (-2, -1, 0, 1, 2)}
    Ez = (8*(e[1]-e[-1]) - (e[2]-e[-2]))/(12*d)
    Ezz = (16*(e[1]+e[-1]) - (e[2]+e[-2]) - 30*e[0])/(12*d*d)
    return Ez, Ezz
def contains(ball, x, slack):
    lo = mp.mpf(ball.lower().str(30, radius=False)); hi = mp.mpf(ball.upper().str(30, radius=False))
    return lo - slack <= x <= hi + slack, lo, hi
ok_all = True
pts = [(fmpq(3), fmpq(1, 2), fmpq(1, 2)), (fmpq(47, 10), fmpq(1, 4), fmpq(3, 2)), (fmpq(2), fmpq(3, 5), fmpq(1, 5))]
for lam, rho, z in pts:
    Ez, Ezz = derivs(mp.mpf(int(lam.p))/int(lam.q), mp.mpf(int(rho.p))/int(rho.q), mp.mpf(int(z.p))/int(z.q))
    bz = K.Ez_ball(rho, z, lam, 128); bzz = K.Ezz_ball(rho, z, lam, 128)
    c1 = contains(bz, Ez, mp.mpf('1e-7')); c2 = contains(bzz, Ezz, mp.mpf('1e-5'))
    print(f"lam={lam} rho={rho} z={z}: Ez_ref={mp.nstr(Ez,10)} in [{mp.nstr(c1[1],8)},{mp.nstr(c1[2],8)}] {c1[0]} ; "
          f"Ezz_ref={mp.nstr(Ezz,10)} in [{mp.nstr(c2[1],8)},{mp.nstr(c2[2],8)}] {c2[0]}")
    ok_all &= c1[0] and c2[0]
# box soundness against independent V = Ez/z at random interior points
random.seed(11)
Riv, tiv, liv = (fmpq(63, 128), fmpq(65, 128)), (fmpq(63, 128), fmpq(65, 128)), (fmpq(895, 256), fmpq(897, 256))
lowb = K.V_box_lower(Riv, tiv, liv, 128)
lb = mp.mpf(lowb.mid().str(30, radius=False))
print("V_box_lower =", mp.nstr(lb, 10))
for _ in range(4):
    Rr = mp.mpf(63)/128 + mp.mpf(random.random())/64; tt = mp.mpf(63)/128 + mp.mpf(random.random())/64
    ll = mp.mpf(895)/256 + mp.mpf(random.random())/128
    a = (1-tt*tt)/(1+tt*tt); b = 2*tt/(1+tt*tt); rho = Rr*a; z = ll*Rr*b
    Ez, _ = derivs(ll, rho, z); V = Ez/z
    print(f"  point V_ref={mp.nstr(V,10)} >= lower {mp.nstr(lb,8)}: {V >= lb}")
    ok_all &= V >= lb
print("SUMMARY", "ALL_PASS" if ok_all else "FAIL")
