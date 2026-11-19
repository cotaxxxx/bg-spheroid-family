"""chat V54: independent non-interval checks of Codex rim-layer formulas (DIAGNOSTIC_ONLY). Own code, mpmath."""
import mpmath as mp
mp.mp.dps = 25
def Pf(g):
    g = min(max(g, mp.mpf(0)), mp.mpf(1)); a = mp.acos(g); return 2*a/mp.sin(a) if a > 0 else mp.mpf(2)
def Qf(g):
    return 2*Pf(g) + g*mp.diff(Pf, g) if g < 1 - mp.mpf('1e-8') else mp.mpf(10)/3
def JK(g):
    g = min(max(g, mp.mpf(0)), mp.mpf(1)); a = mp.acos(g); P = Pf(g); return g*P - a*a, g*g*P
def sph(f, lam, rho, z):  # <f> over the sphere, mu in [-1,1], phi in [0, pi] (q in the x-z plane)
    z = mp.mpf(z); bp_mu = sorted(set([-1, 1, mp.mpf(0), z, max(-1, z - mp.mpf('0.02')), min(1, z + mp.mpf('0.02'))]))
    return mp.quad(lambda mu, ph: f(mu, ph), bp_mu, [0, mp.mpf('0.02'), mp.mpf('0.2'), mp.pi])/(2*mp.pi)
def geom(lam, rho, z, mu, ph):
    s = mp.sqrt(max(1 - mu*mu, 0)); x = s*mp.cos(ph); y = s*mp.sin(ph)
    k = 1 - rho*x - z*mu; D = mp.sqrt((x - rho)**2 + y*y + lam**2*(mu - z)**2); S = mp.sqrt(x*x + y*y + mu*mu/lam**2)
    return s, x, y, k, D, S
def E_rho(lam, rho, z):  # gradient trace formula E_i = <xi_i J - L_ii S u_i K>, i = x (L_xx = 1)
    def f(mu, ph):
        s, x, y, k, D, S = geom(lam, rho, z, mu, ph); g = k/(S*D); J, K = JK(g); return x*J - S*((x - rho)/D)*K
    return sph(f, lam, rho, z)
def E_z(lam, rho, z):
    def f(mu, ph):
        s, x, y, k, D, S = geom(lam, rho, z, mu, ph); g = k/(S*D); J, K = JK(g); return mu*J - lam*S*(lam*(mu - z)/D)*K
    return sph(f, lam, rho, z)
def H_codex(lam, rho):  # (1)
    beta = 1 - lam**2; delta = 1 - rho**2
    def f(mu, ph):
        s, x, y, k, D, S = geom(lam, rho, 0, mu, ph); g = k/(S*D)
        N = delta*y*y + mu*mu*(1 + beta*s*s - (rho + beta/rho)*x); return Pf(g)*N/(S*D**3)
    return sph(f, lam, rho, 0)
def I_mirror(lam, rho):  # (3)
    beta = 1 - lam**2; a = rho/beta
    def f(mu, ph):
        s, x, y, k, D, S = geom(lam, rho, 0, mu, ph); g = k/(S*D); return Pf(g)*mu*mu*(x - a)/(S*D**3)
    return sph(f, lam, rho, 0)
def Ezz_codex(lam, rho, z):  # (7)
    def f(mu, ph):
        s, x, y, k, D, S = geom(lam, rho, z, mu, ph); g = k/(S*D); R2 = (x - rho)**2 + y*y; v = mu - z
        h1 = lam**2*k*v/D**2; return Pf(g)*lam**2*k*k*R2/(S*D**5) - Qf(g)/(S*D)*(mu - h1)**2
    return sph(f, lam, rho, z)
out = []
print("(1) H at z=0: Codex formula vs E_rho/rho from the gradient trace")
for lam, rho in [(mp.mpf(1)/32, mp.mpf('0.5')), (mp.mpf(1)/32, mp.mpf('0.97')), (mp.mpf('0.3'), mp.mpf('0.6')), (mp.mpf(1)/100, mp.mpf('0.9'))]:
    a = H_codex(lam, rho); b = E_rho(lam, rho, 0)/rho
    print(' ', mp.nstr(lam, 4), mp.nstr(rho, 3), 'H(1)=', mp.nstr(a, 12), ' E_rho/rho=', mp.nstr(b, 12), ' H/lam=', mp.nstr(a/lam, 6), flush=True)
print("(3) mirror integral I <= 0 for rho <= beta; (5) H >= lam/12")
for lam, rho in [(mp.mpf(1)/32, mp.mpf('0.3')), (mp.mpf(1)/32, mp.mpf('0.9')), (mp.mpf('0.5'), mp.mpf('0.7')), (mp.mpf(1)/100, mp.mpf('0.99'))]:
    print(' ', mp.nstr(lam, 4), mp.nstr(rho, 3), 'I=', mp.nstr(I_mirror(lam, rho), 10), flush=True)
print("(7) E_zz: Codex decomposition vs central difference of the gradient trace E_z")
for lam, rho, z in [(mp.mpf(1)/32, mp.mpf('0.5'), mp.mpf('0.25')), (mp.mpf(1)/32, mp.mpf('0.9'), mp.mpf('0.3')), (mp.mpf(1)/50, mp.mpf('0.95'), mp.mpf('0.05'))]:
    c = Ezz_codex(lam, rho, z); h = mp.mpf('1e-5'); d = (E_z(lam, rho, z + h) - E_z(lam, rho, z - h))/(2*h)
    print(' ', mp.nstr(lam, 4), mp.nstr(rho, 3), mp.nstr(z, 3), '(7)=', mp.nstr(c, 10), ' FD=', mp.nstr(d, 10), ' /lam=', mp.nstr(c/lam, 6), ' <= -6/55?', c/lam <= -mp.mpf(6)/55, flush=True)
print("<1/R> = pi/2 on the projected disc (both faces, 1/(2 pi) normalisation) == <1/|xi_h - p|> over the sphere")
for rho in ('0', '0.5', '0.9', '0.99'):
    rho = mp.mpf(rho)
    v = mp.quad(lambda mu, ph: 1/mp.sqrt((mp.sqrt(1 - mu*mu)*mp.cos(ph) - rho)**2 + (1 - mu*mu)*mp.sin(ph)**2), [-1, 0, 1], [0, mp.mpf('0.05'), mp.pi])/(2*mp.pi)
    print(' ', mp.nstr(rho, 3), mp.nstr(v, 12), 'pi/2 =', mp.nstr(mp.pi/2, 12), flush=True)
