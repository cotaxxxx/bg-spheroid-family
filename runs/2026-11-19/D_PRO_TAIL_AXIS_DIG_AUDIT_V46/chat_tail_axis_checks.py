"""chat V46: independent checks of Dig's tail-axis M1 (commit b5f4353), chat's own code."""
import sys
sys.path.insert(0, sys.argv[1])
import mpmath as mp
from chat_r1_reference_check_lib import E_ref
res = []
def ck(n, ok, d=""):
    res.append(bool(ok)); print(("PASS " if ok else "FAIL ")+n+(" :: "+d if d else ""), flush=True)
Fp = lambda g: 2*mp.acos(g)/mp.sqrt(1-g*g) if g < 1-mp.mpf(10)**-12 else mp.mpf(2)
def Q(g): return 2*Fp(g) + g*(g*Fp(g)-2)/(1-g*g) if g < 1-mp.mpf(10)**-12 else mp.mpf(10)/3
def KH(t, ph, eps, r, z):          # NP7 integrand in t = (mu - z)/eps, reference coords
    mu = min(mp.mpf(1), max(mp.mpf(-1), z + eps*t)); s2 = 1-mu*mu; s = mp.sqrt(max(s2, 0)); x = s*mp.cos(ph); y = s*mp.sin(ph)
    A = s2 + r*r - 2*r*x; k = 1 - r*x - z*mu; B = s2 + eps**2*mu*mu; D2 = t*t + A; D = mp.sqrt(D2)
    g = min(mp.mpf(1), mp.re(k/(D*mp.sqrt(B))))
    return mp.sqrt(B)/D*(Fp(g)*g*g*(1-y*y/D2) - Q(g)*y*y*(1-k/D2)**2/B)
mp.mp.dps = 25
# (1) inner kernel at eps=0, phi-average, vs -pi S/|t| + 3 S^2/t^2 ; t^3 * error bounded
for r, z in [(mp.mpf('0.5'), mp.mpf(0)), (mp.mpf('0.3'), mp.mpf('0.6'))]:
    S = mp.sqrt(1-z*z); errs = []
    for t in [16, 64, 256]:
        Kbar = mp.quad(lambda ph: KH(mp.mpf(t), ph, mp.mpf(0), r, z), [0, mp.pi/2, mp.pi, 3*mp.pi/2, 2*mp.pi])/(2*mp.pi)
        errs.append(abs(Kbar - (-mp.pi*S/t + 3*S*S/t**2))*t**3)
    ck(f"inner kernel 2-term expansion q=({r},{z}): t^3*err bounded (t=16,64,256)", errs[2] < 2*errs[0] + 1, ", ".join(mp.nstr(e,4) for e in errs))
# (2) exact identity at finite eps: H = eps[-(pi S/2)(asinh+asinh) + R_H], R_H integrated independently in t; compare H with NP7 value / FD of E_ref
lam, r, z = 5, mp.mpf('0.3'), mp.mpf('0.4'); eps = mp.mpf(1)/lam; S = mp.sqrt(1-z*z)
tm, tp = (-1-z)/eps, (1-z)/eps
cH = lambda ph: -2*mp.pi*S*mp.sin(ph)**2
br = sorted(set([tm, tp] + [b for b in (0, -1, 1, -5, 5) if tm < b < tp]))
RH = mp.quad(lambda t, ph: KH(t, ph, eps, r, z) - cH(ph)/mp.sqrt(1+t*t), br, [0, mp.pi/2, mp.pi, 3*mp.pi/2, 2*mp.pi])/(4*mp.pi)
Hid = eps*(-(mp.pi*S/2)*(mp.asinh((1-z)/eps)+mp.asinh((1+z)/eps)) + RH)
hd = mp.mpf('0.002'); Hfd = (E_ref(lam, r+hd, lam*z) - E_ref(lam, r-hd, lam*z))/(2*hd)/r
ck("exact log-subtraction identity at lambda=5, q=(0.3,0.4) vs E_rho/rho from chat E_ref", abs(Hid-Hfd) < 1e-5, f"identity {mp.nstr(Hid,10)} FD {mp.nstr(Hfd,10)}; R_H = {mp.nstr(RH,8)}, main = {mp.nstr(-(mp.pi*S/2)*(mp.asinh((1-z)/eps)+mp.asinh((1+z)/eps)),8)}")
# (3) centre cancellation numbers at lambda = 5
ck("centre lambda=5: main term -pi asinh 5 = -7.2647393", abs(-mp.pi*mp.asinh(5)+mp.mpf('7.2647393')) < 1e-7)
# (4) axis: E_z(0,z) = (1/2) int I = -z pi^2/4 - (1/2) int T f  vs FD of chat E_ref (reference z derivative)
lam, z = 5, mp.mpf('0.5'); eps = mp.mpf(1)/lam
def fax(mu, zz):
    k = 1 - zz*mu; d = mp.sqrt((mu-zz)**2 + eps**2*(1-mu*mu)); B = 1-(1-eps**2)*mu*mu
    g = min(mp.mpf(1), eps*k/(d*mp.sqrt(B))); return k*(mp.pi**2/4 - mp.acos(g)**2)
def Iax(mu, zz):
    k = 1 - zz*mu; d2 = (mu-zz)**2 + eps**2*(1-mu*mu); d = mp.sqrt(d2); B = 1-(1-eps**2)*mu*mu
    g = min(mp.mpf(1), eps*k/(d*mp.sqrt(B))); F = mp.pi**2/4 - mp.acos(g)**2
    return mu*(F + g*Fp(g)) - k*g*Fp(g)*(mu-zz)/d2
pts = [-1, -0.5, 0, z-0.01, z, z+0.01, 1]
Ez1 = mp.quad(lambda m: Iax(m, z), pts)/2
dd = mp.mpf(10)**-12
Tf = lambda m: (fax(m+dd, z+dd) - fax(m-dd, z-dd))/(2*dd)
Ez2 = -z*mp.pi**2/4 - mp.quad(Tf, [-1+1e-9, -0.5, 0, z-0.01, z, z+0.01, 1-1e-9])/2
Ez3 = mp.quad(lambda m: (Iax(m, z) - Iax(m, -z)), [0, z-0.01, z, z+0.01, 1])/2
hz = mp.mpf('0.002'); Ezfd = (E_ref(lam, 0, lam*(z+hz)) - E_ref(lam, 0, lam*(z-hz)))/(2*hz)
ck("axis: (1/2)int I = -z pi^2/4 - (1/2)int Tf = (1/2)int_0^1 [I(mu,z)-I(mu,-z)] = FD of E_ref", max(abs(Ez1-Ezfd), abs(Ez2-Ezfd), abs(Ez3-Ezfd)) < 1e-5,
   f"{mp.nstr(Ez1,10)}, {mp.nstr(Ez2,10)}, {mp.nstr(Ez3,10)}, FD {mp.nstr(Ezfd,10)}")
ck("axis endpoint values: gamma(+-1)=1, f(+-1,z) = (1 -+ z) pi^2/4", abs(fax(mp.mpf(1)-mp.mpf(10)**-15, z)-(1-z)*mp.pi**2/4) < 1e-6 and abs(fax(-mp.mpf(1)+mp.mpf(10)**-15, z)-(1+z)*mp.pi**2/4) < 1e-6)
print(f"SUMMARY {sum(res)}/{len(res)} PASS")
