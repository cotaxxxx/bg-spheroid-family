"""chat V47: independent checks of Dig M2 notes (commit 91d486b)."""
import random, mpmath as mp
random.seed(47); res = []
def ck(n, ok, d=""):
    res.append(bool(ok)); print(("PASS " if ok else "FAIL ")+n+(" :: "+d if d else ""), flush=True)
mp.mp.dps = 40
F = lambda g: mp.pi**2/4 - mp.acos(g)**2
def Fp(g):
    if 1-g < mp.mpf(10)**-8: h=(1-g)/2; return 2*(1+mp.mpf(2)/3*h+mp.mpf(8)/15*h*h)
    return 2*mp.acos(g)/mp.sqrt(1-g*g)
def Fpp(g):
    if 1-g < mp.mpf(10)**-8: h=(1-g)/2; return -(mp.mpf(2)/3+mp.mpf(16)/15*h)
    return (g*Fp(g)-2)/(1-g*g)
def parts(mu, z, e):
    w = mu-z; D2 = w*w + e*e*(1-mu*mu); B = 1-(1-e*e)*mu*mu; k = 1-z*mu; g = e*k/(mp.sqrt(D2)*mp.sqrt(B))
    return w, D2, B, k, g
def I(mu, z, e):
    w, D2, B, k, g = parts(mu, z, e); return mu*(F(g)+g*Fp(g)) - k*g*Fp(g)*w/D2
def dzI(mu, z, e):
    w, D2, B, k, g = parts(mu, z, e); V = k*w/D2
    return (mu*(2*Fp(g)+g*Fpp(g)) - V*(Fp(g)+g*Fpp(g)))*e*(-mu+V)/(mp.sqrt(B)*mp.sqrt(D2)) - g*Fp(g)*(-mu*w/D2 - k/D2 + 2*k*w*w/D2**2)
worst = 0
for _ in range(200):
    e = mp.mpf(1)/random.choice([5, 10, 50, 500]); mu = mp.mpf(random.random()); z = (2*mp.mpf(random.random())-1)*mp.mpf('0.99')
    h = mp.mpf(10)**-15; fd = (I(mu, z+h, e)-I(mu, z-h, e))/(2*h)
    worst = max(worst, abs(fd-dzI(mu, z, e))/max(1, abs(fd)))
ck("M2-4: closed form of d_z I vs central FD (200 random points)", worst < mp.mpf(10)**-20, f"max rel diff {mp.nstr(worst,3)}")
# M2-3: E_z/z = 1/2 int_0^1 int_-1^1 dzI(mu,uz) du dmu  vs  1/2 int_-1^1 I dmu / z
mp.mp.dps = 20
e = mp.mpf(1)/5; z = mp.mpf('0.5')
lhs = mp.quad(lambda m: I(m, z, e), [-1, -z, 0, z, 1])/2/z
rhs = mp.quad(lambda m, u: dzI(m, u*z, e), [0, z/2, z, 1], [-1, 0, 1])/2
ck("M2-3: odd-quotient double integral = E_z/z (lambda=5, z=1/2); V46 value E_z = 0.90525177", abs(lhs-rhs) < 1e-8 and abs(lhs*z-mp.mpf('0.90525177')) < 1e-7, f"{mp.nstr(lhs,10)} vs {mp.nstr(rhs,10)}")
# M2-5/6 product identity, gamma0 min
mp.mp.dps = 30
ok = True
for _ in range(100):
    e = mp.mpf(random.random())/5; mu = mp.mpf(random.random()); a = 1-e*e
    D0 = e*e + a*mu*mu; B0 = 1 - a*mu*mu
    ok &= abs(D0*B0 - (e*e + a*a*mu*mu*(1-mu*mu))) < 1e-25 and abs(D0+B0-(1+e*e)) < 1e-25
ck("M2-6: D0 B0 = eps^2 + a^2 mu^2(1-mu^2), D0 + B0 = 1 + eps^2 (100 random)", ok)
e = mp.mpf(1)/5; a = 1-e*e
g0 = lambda mu: e/mp.sqrt((e*e+a*mu*mu)*(1-a*mu*mu))
gm = mp.findroot(lambda m: mp.diff(g0, m), 0.7)
ck("M2-6: gamma0 minimum at mu = 1/sqrt2 equals 2eps/(1+eps^2)", abs(gm-1/mp.sqrt(2)) < 1e-15 and abs(g0(gm)-2*e/(1+e*e)) < 1e-20)
# M2-2 elementary bound and its slack near the polar cutoff
for lam, S in [(10, mp.mpf(2)**-12), (10, mp.mpf('0.5')), (100, mp.mpf(2)**-12)]:
    z = mp.sqrt(1-S*S); A = mp.asinh(lam*(1-z)) + mp.asinh(lam*(1+z)); lb = 2*mp.log(lam) + mp.log(4*S*S)
    print(f"  lambda={lam} S={mp.nstr(S,4)}: exact (pi/2)A = {mp.nstr(mp.pi/2*A,6)}  vs  log-bound (pi/2)(2log lam + log 4S^2) = {mp.nstr(mp.pi/2*lb,6)}")
z = mp.sqrt(1-(mp.mpf(2)**-12)**2)
ck("M2-2: asinh(x) >= log(2x) holds but is far from tight at x = lambda(1-z) ~ lambda S^2/2 (S = 2^-12)", mp.asinh(10*(1-z)) >= mp.log(20*(1-z)) and mp.asinh(10*(1-z)) - mp.log(20*(1-z)) > 14, f"slack {mp.nstr(mp.asinh(10*(1-z)) - mp.log(20*(1-z)),5)}")
ck("M2-2: conditional threshold with C=0 is e^(3/2)/(2 S0) ~ 9180 (an artifact of the log bound near S0)", abs(mp.e**1.5/(2*mp.mpf(2)**-12) - 9178.6) < 1)
ck("M2-1: horizontal core reference for all |z| <= sqrt(1-S0^2) iff m <= 1-sqrt(1-S0^2) = S0^2/(1+sqrt(1-S0^2)) ~ 2^-25",
   abs((1-mp.sqrt(1-mp.mpf(2)**-24)) - mp.mpf(2)**-24/(1+mp.sqrt(1-mp.mpf(2)**-24))) < 1e-30 and abs((1-mp.sqrt(1-mp.mpf(2)**-24))/mp.mpf(2)**-25 - 1) < 1e-6)
print(f"SUMMARY {sum(res)}/{len(res)} PASS")
