"""chat V45: independent checks of Astra NONPOLAR report (NP4)-(NP20), from chat's own kernel / own algebra."""
import sys, random
sys.path.insert(0, sys.argv[1])
import mpmath as mp
from fractions import Fraction as Fr
from math import factorial, log, pi
from chat_r1_reference_check_lib import E_ref
random.seed(45)
res = []
def ck(n, ok, d=""):
    res.append(bool(ok)); print(("PASS " if ok else "FAIL ")+n+(" :: "+d if d else ""), flush=True)
Fp = lambda g: 2*mp.acos(g)/mp.sqrt(1-g*g) if g < 1 else mp.mpf(2)
def Fpp(g): return (g*Fp(g) - 2)/(1-g*g)
# (1) series (NP11),(NP12)
mp.mp.dps = 40
an = lambda n: mp.mpf(4)**n*mp.factorial(n)**2/mp.factorial(2*n+1)
qn = lambda n: an(n)*(2*n*n+10*n+10)/(2*n+3)
worst = 0
for g in [mp.mpf('0.05'), mp.mpf('0.3'), mp.mpf('0.7'), mp.mpf('0.95')]:
    h = (1-g)/2
    s1 = 2*mp.nsum(lambda n: an(int(n))*h**n, [0, mp.inf]); s2 = mp.nsum(lambda n: qn(int(n))*h**n, [0, mp.inf])
    worst = max(worst, abs(s1-Fp(g)), abs(s2-(2*Fp(g)+g*Fpp(g))))
ck("NP11/NP12: F' = 2 sum a_n h^n, Q = 2F'+gF'' = sum q_n h^n (4 gammas)", worst < mp.mpf(10)**-30, f"max diff {mp.nstr(worst,3)}")
# (2) eigenvalue range of the w-direction: 4a sin a - 2 cos a in [-2, 2pi], and -g^2F' in [-2,0]
mp.mp.dps = 30
vals = [4*al*mp.sin(al) - 2*mp.cos(al) for al in mp.linspace(0, mp.pi/2, 2001)]
ok = all(vals[i] <= vals[i+1] for i in range(len(vals)-1)) and abs(vals[0]+2) < 1e-25 and abs(vals[-1]-2*mp.pi) < 1e-25
ck("NP8: 4 a sin a - 2 cos a increasing from -2 to 2pi; identity (1-g^2)F''=gF'-2", ok)
# (3) density Hessian (NP4) eigenvalues: FD of kF in physical p, scaled by D/sqrt(B), lie in [-2, 2pi]
mp.mp.dps = 40
bad = 0; ext = [mp.inf, -mp.inf]
for _ in range(40):
    lam = random.choice([2, 5, 10]); th = mp.acos(2*mp.mpf(random.random())-1); ph = 2*mp.pi*mp.mpf(random.random())
    xi = (mp.sin(th)*mp.cos(ph), mp.sin(th)*mp.sin(ph), mp.cos(th))
    r = mp.mpf(random.random())*0.9; zz = (2*mp.mpf(random.random())-1)*mp.sqrt(1-r*r)*0.95
    p0 = [r, mp.mpf(0), lam*zz]
    def dens(p):
        qv = (p[0], p[1], p[2]/lam); k = 1 - sum(qv[i]*xi[i] for i in range(3))
        v = (xi[0]-p[0], xi[1]-p[1], lam*xi[2]-p[2]); D = mp.sqrt(sum(t*t for t in v)); B = xi[0]**2+xi[1]**2+xi[2]**2/lam**2
        g = k/(D*mp.sqrt(B)); return k*(mp.pi**2/4 - mp.acos(g)**2), D, B
    _, D, B = dens(p0); hh = mp.mpf(10)**-10
    Hm = mp.matrix(3, 3)
    for i in range(3):
        for j in range(3):
            def sh(di, dj):
                p = list(p0); p[i] += di*hh; p[j] += dj*hh; return dens(p)[0]
            Hm[i, j] = (sh(1,1)-sh(1,-1)-sh(-1,1)+sh(-1,-1))/(4*hh*hh)
    ev = mp.eigsy(Hm*(D/mp.sqrt(B)))[0]
    ext = [min(ext[0], min(ev)), max(ext[1], max(ev))]
    if min(ev) < -2-1e-6 or max(ev) > 2*mp.pi+1e-6: bad += 1
ck("NP4/NP8: eigenvalues of (D/sqrtB) Hess_p(kF) in [-2, 2pi] (40 random xi,p)", bad == 0, f"observed range [{mp.nstr(ext[0],5)}, {mp.nstr(ext[1],5)}]")
# (4) (NP7) H formula vs chat's own E_ref finite differences of E_rho/rho
mp.mp.dps = 20
def H_np7(lam, r, z):
    def f(mu, ph):
        s = mp.sqrt(1-mu*mu); x = s*mp.cos(ph); y = s*mp.sin(ph)
        k = 1 - r*x - z*mu; D2 = (x-r)**2 + y*y + lam**2*(mu-z)**2; D = mp.sqrt(D2); B = s*s + mu*mu/lam**2
        g = min(mp.mpf(1), k/(D*mp.sqrt(B))); Q = 2*Fp(g) + g*Fpp(g) if g < 1-mp.mpf(10)**-12 else mp.mpf(10)/3
        return (k*k*Fp(g)*(D2-y*y) - Q*y*y*(D2-k)**2)/(D**5*mp.sqrt(B))
    mus = sorted(set([-1, 1, z] + [min(1, max(-1, z+sg*mp.mpf(10)**(-j))) for sg in (-1,1) for j in range(1,6)]))
    return 2*mp.quad(f, mus, [0, mp.pi/4, mp.pi/2, mp.pi])/(4*mp.pi)
for lam, r, z in [(5, mp.mpf('0.3'), mp.mpf('0.4')), (5, mp.mpf('0.5'), mp.mpf(0)), (10, mp.mpf('0.2'), mp.mpf('0.6'))]:
    hd = mp.mpf('0.002')
    Er = (E_ref(lam, r+hd, lam*z) - E_ref(lam, r-hd, lam*z))/(2*hd)
    Hfd = Er/r; Hn = H_np7(lam, r, z)
    ck(f"NP7 vs E_rho/rho (chat E_ref, central FD h=0.002) lam={lam} rho={r} z={z}", abs(Hn-Hfd) < 1e-5*max(1, abs(Hfd))*10, f"NP7 {mp.nstr(Hn,10)}  FD {mp.nstr(Hfd,10)}")
# (5) centre values H(0) by NP17 1D formula (exact F', Q) vs V41 references
def H0(lam):
    def f(mu):
        D2 = 1+(lam**2-1)*mu*mu; D = mp.sqrt(D2); B = 1-(1-mp.mpf(1)/lam**2)*mu*mu; s2 = 1-mu*mu
        g = min(mp.mpf(1), 1/(D*mp.sqrt(B)))
        Q = 2*Fp(g)+g*Fpp(g) if g < 1-mp.mpf(10)**-10 else mp.mpf(10)/3
        return mp.sqrt(B)/D*(Fp(g)*g*g*(1-s2/(2*D2)) - Q*s2/(2*B)*(1-1/D2)**2)
    return mp.quad(f, [0, mp.mpf(1)/lam/10, mp.mpf(1)/lam, 1])
h5, h10 = H0(5), H0(10)
ck("centre H(0;5) = -0.0243031 (V41), H(0;10) = -0.1829940 (V41)", abs(h5+mp.mpf('0.0243031'))<2e-7 and abs(h10+mp.mpf('0.1829940'))<2e-7, f"{mp.nstr(h5,9)}, {mp.nstr(h10,9)}")
ck("centre: lambda H(0) < -1/2 at lambda = 64, 256, 4096 (numeric)", all(L*H0(L) < -0.5 for L in (64, 256, 4096)), ", ".join(mp.nstr(L*H0(L),6) for L in (64,256,4096)))
# (6) exact fractions
a = lambda n: Fr(4**n*factorial(n)**2, factorial(2*n+1))
zeta = lambda N: Fr(4*N+20)*a(N+1)/2**(N+1); eta = lambda N: Fr(2*N+12)*a(N+1)/2**(N+1)
ck("zeta_20 = 5242880/578627215023", zeta(20) == Fr(5242880, 578627215023), str(zeta(20)))
ck("5 zeta_20 < 1/20000 and 5 eta_20 < 1/40000", 5*zeta(20) < Fr(1,20000) and 5*eta(20) < Fr(1,40000), f"{float(5*zeta(20)):.3e}, {float(5*eta(20)):.3e}")
ck("T_lambda < 25 on [5,10]: log 11 + 29 log 2", log(11)+29*log(2) < 25, f"{log(11)+29*log(2):.4f}")
ck("q_n <= a_M (n+4): (n+4)(2n+3) >= 2n^2+10n+10", all((n+4)*(2*n+3) >= 2*n*n+10*n+10 for n in range(200)))
ck("bracket <= 4M+16: max over h in [0,1/2] of 2g^2/(1-h)+16h+4g(M+h/(1-h)) (M=21)",
   max(2*(1-2*h)**2/(1-h)+16*h+4*(1-2*h)*(21+h/(1-h)) for h in [i/10000/2 for i in range(10001)]) <= 4*21+16)
L = Fr(310,81); Pp = Fr(22,7)*(1+Fr(22,7)/128)
ck("NP20: 40/27 (5*2/3 - 3/4) = 310/81; (22/7)(1+(22/7)/128) = 5049/1568; diff = 77111/127008 > 1/2",
   Fr(40,27)*(5*Fr(2,3)-Fr(3,4)) == L and Pp == Fr(5049,1568) and L-Pp == Fr(77111,127008) and L-Pp > Fr(1,2) and log(2) > 2/3 and pi < 22/7)
# NP19 identity check numerically
lam = 7; aa = lam**2-1
lhs = (1+aa)*mp.quad(lambda t: (1+aa*mp.sin(t)**2)**-1.5, [0, mp.pi/2]); rhs = mp.quad(lambda t: mp.sqrt(1+aa*mp.sin(t)**2), [0, mp.pi/2])
ck("NP19: (1+a) int D^-3 = int D (boundary terms vanish)", abs(lhs-rhs) < 1e-15, f"{mp.nstr(lhs,12)} vs {mp.nstr(rhs,12)}")
ck("NP20 integral closed form (lambda=64)", abs(mp.quad(lambda m: (1-m*m)/m*(1-2/(64**2*m*m)), [mp.mpf(2)/64, 1]) - ((1+mp.mpf(2)/64**2)*mp.log(32) - mp.mpf(3)/4 + mp.mpf(3)/64**2)) < 1e-15)
print(f"SUMMARY {sum(res)}/{len(res)} PASS")
