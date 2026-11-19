"""chat V48: independent checks of Codex L1/L2 tail report (commit 8fd265f), chat's own code."""
import sys, random
sys.path.insert(0, sys.argv[1])
import mpmath as mp
from chat_r1_reference_check_lib import E_ref
random.seed(48); res = []
def ck(n, ok, d=""):
    res.append(bool(ok)); print(("PASS " if ok else "FAIL ")+n+(" :: "+d if d else ""), flush=True)
def Fp(g):
    if 1-g < mp.mpf(10)**-8: h=(1-g)/2; return 2*(1+mp.mpf(2)/3*h+mp.mpf(8)/15*h*h)
    return 2*mp.acos(g)/mp.sqrt(1-g*g)
def Fpp(g):
    if 1-g < mp.mpf(10)**-8: h=(1-g)/2; return -(mp.mpf(2)/3+mp.mpf(16)/15*h)
    return (g*Fp(g)-2)/(1-g*g)
Q = lambda g: 2*Fp(g)+g*Fpp(g)
# ---------- L2 ----------
mp.mp.dps = 30
def a_ang(mu, z, e):
    s = mp.sqrt(1-mu*mu); return mp.atan((mu-z)/(e*s)) - mp.atan(e*mu/s)
def Eax(z, e):   # (13)
    return mp.quad(lambda m: (1-z*m)*a_ang(m, z, e)**2, [-1, -0.5, 0, z, 0.5, 1])/2
def Ez_over_z_16(z, e):
    def f(m):
        s = mp.sqrt(1-m*m)
        if s == 0: return mp.mpf(0)
        B = s*s+e*e*m*m; b = mp.atan(e*m/s)
        tp = mp.atan((m+z)/(e*s)); tm = mp.atan((m-z)/(e*s)); Sig = tp+tm-2*b
        Daz = mp.quad(lambda u: e*s/((m+u*z)**2+e*e*s*s), [-1, 0, 1]) if z != 0 else 2*e*s/(m*m+e*e*s*s)
        return Daz*(3*m*Sig + 2*e*s/B)
    return mp.quad(f, [0, abs(z)/2, abs(z), (1+abs(z))/2, 1])/2
lam = 5; e = mp.mpf(1)/lam
ck("L2 (13): axis E(0,z) = (1/2) int k a^2 equals chat E_ref (lambda=5, z=0.3)", abs(Eax(mp.mpf('0.3'), e) - E_ref(lam, 0, lam*mp.mpf('0.3'))) < 1e-9)
def Iax(mu, z, e):   # independent G4 kernel on the axis (V46/V47)
    s2 = 1-mu*mu; w = mu-z; D2 = w*w + e*e*s2; B = 1-(1-e*e)*mu*mu; k = 1-z*mu
    g = min(mp.mpf(1), e*k/(mp.sqrt(D2)*mp.sqrt(B))); F = mp.pi**2/4 - mp.acos(g)**2
    return mu*(F + g*Fp(g)) - k*g*Fp(g)*w/D2
vals = []
for z in [mp.mpf('0.5'), mp.mpf('0.9'), mp.sqrt(24)/5]:
    v16 = Ez_over_z_16(z, e)
    vg4 = mp.quad(lambda m: Iax(m, z, e), [-1, -z, 0, z, 1])/2/z
    vals.append((z, v16, vg4))
ck("L2 (16): paired angle formula vs independent G4-kernel E_z/z (lambda=5; z=0.5, 0.9, focus sqrt24/5)", all(abs(a-b) < 1e-12 for _, a, b in vals), "; ".join(f"z={mp.nstr(z,4)}: {mp.nstr(a,12)} vs {mp.nstr(b,12)}" for z, a, b in vals))
hz = mp.mpf('0.0005'); z = mp.mpf('0.5'); fd = (E_ref(lam, 0, lam*(z+hz)) - E_ref(lam, 0, lam*(z-hz)))/(2*hz)/z
ck("L2 (16) vs chat E_ref central difference (z=0.5, h=5e-4; FD truncation ~h^2)", abs(fd - vals[0][1]) < 1e-6, f"{mp.nstr(fd,10)} vs {mp.nstr(vals[0][1],10)}")
mp.mp.dps = 40; worst = 0
for _ in range(300):
    e = mp.mpf(random.random())/2; z = mp.mpf(random.random()); m = mp.mpf(random.random())
    s = mp.sqrt(1-m*m); B = s*s+e*e*m*m; S2 = 1-z*z
    Sig = mp.atan((m+z)/(e*s)) + mp.atan((m-z)/(e*s)) - 2*mp.atan(e*m/s)
    Lp = (m+z)**2+e*e*s*s; Lm = (m-z)**2+e*e*s*s
    worst = max(worst, abs(mp.sin(Sig) - 2*e*m*s*(S2-e*e)/(B*mp.sqrt(Lp*Lm))))
ck("L2 (17): sin Sigma identity (300 random eps<1/2, z, mu)", worst < mp.mpf(10)**-35, f"max diff {mp.nstr(worst,3)}")
mp.mp.dps = 25; ok = True; mn = mp.inf
for lam in [5, 10, 50]:
    e = mp.mpf(1)/lam
    for z in [mp.mpf('0.01'), mp.mpf('0.5'), mp.mpf('0.9'), mp.sqrt(1-e*e), mp.sqrt(1-e*e/4)]:
        v = Ez_over_z_16(z, e); mn = min(mn, v/(mp.mpf(3)/10*e*e)); ok &= v >= mp.mpf(3)/10*e*e
ck("L2 (18)/G1: E_z/z >= 3 eps^2/10 at 15 axis points (lambda=5,10,50; incl. focus and S<eps)", ok, f"min ratio to bound {mp.nstr(mn,4)}")
ck("L2 window remark: (18) denominator bound (mu+uz)^2+eps^2 s^2 <= 9/4+1/4 = 5/2 also for eps <= 1/2 (lambda >= 2)", mp.mpf(9)/4 + mp.mpf(1)/4 <= mp.mpf(5)/2)
# ---------- L1 key inequality (8)-(9): pointwise in t after phi-average, lambda = 4096 ----------
mp.mp.dps = 25
def rbar(t, e, r, z):
    S = mp.sqrt(1-z*z)
    def K(ph):
        mu = min(mp.mpf(1), max(mp.mpf(-1), z + e*t)); s2 = 1-mu*mu; s = mp.sqrt(s2); x = s*mp.cos(ph); y = s*mp.sin(ph)
        A = (x-r)**2 + y*y; k = 1 - z*mu - r*x; B = s2 + e*e*mu*mu; D2 = t*t + A; D = mp.sqrt(D2)
        g = min(mp.mpf(1), mp.re(k/(D*mp.sqrt(B)))); m = s2/mp.sqrt(B)
        Kv = mp.sqrt(B)/D*Fp(g)*g*g*(1-y*y/D2) - m/D*mp.sin(ph)**2*Q(g)*(1-k/D2)**2
        k0 = S*S - r*S*mp.cos(ph); c = -2*mp.pi*S*mp.sin(ph)**2; d = 6*k0*mp.sin(ph)**2
        return Kv - c/mp.sqrt(1+t*t) - d/(1+t*t)
    return mp.quad(K, [0, mp.pi/2, mp.pi])/mp.pi, S
lam = 4096; e = mp.mpf(1)/lam; bad = 0; n = 0; tight = mp.inf
for _ in range(40):
    S = mp.mpf(2)**(-random.uniform(0, 9)); z = mp.sqrt(1-S*S); r = S*mp.mpf(random.random())
    h = e/S
    if h > mp.mpf(1)/8: continue
    T = S*mp.mpf(3)*mp.mpf(10)**random.uniform(0, 2.5); sg = random.choice([-1, 1]); t = sg*T
    mu = z + e*t
    if not (-1 < mu < 1): continue
    rb, _ = rbar(t, e, r, z); s = mp.sqrt(1-mu*mu); B = s*s+e*e*mu*mu; m = s*s/mp.sqrt(B)
    rhs9 = mp.pi*max(S-s, 0)/T + mp.pi*(s-m)/T + (mp.pi+3)*(S*S/T**2 + e*e/2) + 3*mp.pi*m*(S*S+e*T)/T**3
    n += 1; tight = min(tight, rhs9 - rb)
    if rb > rhs9: bad += 1
ck("L1 (9): phi-averaged residual kernel <= RHS(9) at random T >= 3S, h <= 1/8, lambda = 4096", bad == 0 and n >= 20, f"{n} points, violations {bad}, min slack {mp.nstr(tight,4)}")
# ---------- L1 sample: R_H^(2)/S at lambda = 4096 (independent of Codex grid) ----------
def RH2_over_S(lam, S, u):
    e = mp.mpf(1)/lam; z = mp.sqrt(1-S*S); r = u*S
    tm, tp = (-1-z)/e, (1-z)/e
    pts = [tm] + sorted(set([sg*S*mp.mpf(10)**j for j in range(-3, 7) for sg in (-1, 1) if tm < sg*S*mp.mpf(10)**j < tp] + [mp.mpf(0)])) + [tp]
    I = mp.quad(lambda t: rbar(t, e, r, z)[0], pts)
    return I/2/S
mp.mp.dps = 20
v1 = RH2_over_S(4096, mp.mpf(3)/4, mp.mpf(1)/2)
ck("L1 sample lambda=4096, S=3/4, rho/S=1/2: R_H^(2)/S (Codex 2.16229532) and <= 29/2", abs(v1-mp.mpf('2.16229532')) < 1e-4 and v1 <= 14.5, mp.nstr(v1, 9))
v2 = RH2_over_S(4096, mp.mpf(1)/32, mp.mpf('0.999'))
ck("L1 sample lambda=4096, S=1/32 (h=1/128), rho/S=0.999 (near contact): R_H^(2)/S <= 29/2", v2 <= 14.5, mp.nstr(v2, 9))
print(f"SUMMARY {sum(res)}/{len(res)} PASS")
