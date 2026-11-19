"""chat V53: non-interval checks of Codex's new formulas (DIAGNOSTIC_ONLY). Independent of Codex code."""
import sys; sys.path.insert(0, 'GER2')
import mpmath as mp
from geoenclosereader.reference import ez_axis_ref
mp.mp.dps = 20
def PJK(g):
    g = min(max(g, mp.mpf(0)), mp.mpf(1)); a = mp.acos(g); P = 2*a/mp.sin(a) if a > 0 else mp.mpf(2)
    return P, g*P - a*a, g*g*P
def Qf(g):  # Q = 2P + g P'
    h = mp.mpf('1e-8'); P = lambda x: PJK(x)[0]
    return 2*P(g) + g*mp.diff(P, g) if g < 1 - 1e-6 else mp.mpf(10)/3
# §2 axis formula E_zz/lambda = <2 lam k s^2/D^4 + 4 s^3 a R / D^4>, <.> = dmu/2
def ezz_axis_codex(lam, z):
    lam = mp.mpf(lam); z = mp.mpf(z)
    def f(mu):
        s = mp.sqrt(1 - mu*mu); D2 = s*s + lam**2*(mu - z)**2; k = 1 - mu*z
        a = mp.atan(lam*(mu - z)/s) - mp.atan(mu/(lam*s)); R = (1 - lam**2)*mu + lam**2*z
        return 2*lam*k*s*s/D2**2 + 4*s**3*a*R/D2**2
    return lam*mp.quad(f, [-1, -0.5, z - 0.01, z, z + 0.01, 0.5, 1] if abs(z) < 0.49 else [-1, 0, z, 1])/2
def ezz_fd(lam, z, h=mp.mpf('1e-4')):
    return (ez_axis_ref(lam, z + h) - ez_axis_ref(lam, z - h))/(2*h)
print("§2 axis E_zz: Codex formula vs FD of E_z (2)")
for lam, z in [(0.5, 0.3), (1/32, 0.0), (1/32, 0.5), (1/32, 0.9)]:
    c = ezz_axis_codex(lam, z); d = ezz_fd(lam, z); print(' ', lam, z, mp.nstr(c, 10), mp.nstr(d, 10), ' <= -lam/2 ?', c <= -mp.mpf(lam)/2)
# §3 centre H(0,0)
def H0_codex(lam):
    lam = mp.mpf(lam)
    def f(mu):
        C = 1 - (1 - lam**2)*mu*mu; B = 1 + (1/lam**2 - 1)*mu*mu; g = 1/mp.sqrt(B*C); Y = (1 - mu*mu)/2
        P = PJK(g)[0]; Q = Qf(g)
        return (Y*g/C)*((1 - lam**2)*mu*mu*Q + (3 - 1/B)*P - (1 - 1/B)*Q)
    return mp.quad(f, [0, 0.5, 1])
print("§3 centre H(0,0) (Reader chord v50 at lambda=0.5: [?]; sphere 4/3)")
for lam in (1, 0.5, 0.3, 1/32): print(' ', lam, mp.nstr(H0_codex(lam), 10))
# §5 pole trace E_z(0,1) = int_0^1 2x [mu J + M K] dx
def pole_codex(lam):
    lam = mp.mpf(lam)
    def f(x):
        mu = 1 - 2*x*x; Cp = 1 - x*x + lam**2*x*x; B = 1/lam**2 + (1 - 1/lam**2)*(1 - mu*mu)
        g = x/mp.sqrt(Cp*B); M = lam**2*x*mp.sqrt(B/Cp); P, J, K = PJK(g)
        return 2*x*(mu*J + M*K)
    return mp.quad(f, [0, 0.25, 0.5, 0.75, 1])
print("§5 pole trace: Codex formula vs E_z(0, z -> 1) by (2)")
for lam in (0.62, 0.6435456, 0.66, 0.9):
    print(' ', lam, mp.nstr(pole_codex(lam), 10), [mp.nstr(ez_axis_ref(lam, z), 8) for z in ('0.999', '0.9999')])
# §7 boundary-equator trace H_b = <(aP/D) mu^2 (1 - lam^2 k / D^2)>, q = (1,0,0)
def hb_codex(lam):
    lam = mp.mpf(lam)
    def f(mu, ph):
        s = mp.sqrt(1 - mu*mu); x = s*mp.cos(ph); y = s*mp.sin(ph); k = 1 - x; D2 = (1 - x)**2 + y*y + lam**2*mu*mu
        B = x*x + y*y + mu*mu/lam**2; a = 1/mp.sqrt(B); D = mp.sqrt(D2); g = k/(D*mp.sqrt(B)); P = PJK(g)[0]
        return (a*P/D)*mu*mu*(1 - lam**2*k/D2)
    return mp.quad(f, [-1, -0.2, 0, 0.2, 1], [0, 0.05, 0.5, mp.pi])/(2*mp.pi)
print("§7 H_b: Codex formula, lambda/6, and H_b/lambda")
for lam in (0.5, 0.1, 0.01): v = hb_codex(lam); print(' ', lam, mp.nstr(v, 10), '>= lam/6', v >= mp.mpf(lam)/6, 'H_b/lam', mp.nstr(v/lam, 6))
