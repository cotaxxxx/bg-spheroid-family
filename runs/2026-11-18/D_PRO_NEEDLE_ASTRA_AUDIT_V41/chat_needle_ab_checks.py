"""chat V41: independent checks of Astra's needle report (my own code; only the report's formulas are used as claims).
(1) N9 J(l,d) closed form vs quadrature; (2) N11 integrals; (3) N13 b(q) vs chat's brute-force lambda*Delta - a log lambda
(V-needle probe logs, lambda = 1e3, 1e4, 1e5); N14 on the axis; (4) centre Hessian E_rhorho(0) at lambda=5,10 by FD of primitive E;
(5) oblate a_ob (N27) at rho=1/2 from primitive E at small lambda."""
import sys, mpmath as mp
sys.path.insert(0, sys.argv[1])
from chat_r1_reference_check_lib import E_ref
mp.mp.dps = 30
res = []
def ck(n, ok, d=""):
    res.append(bool(ok)); print(("PASS " if ok else "FAIL ")+n+(" :: "+d if d else ""), flush=True)
F = lambda y: mp.pi**2/4 - mp.acos(y)**2
# (1) J(l,d)
for l, d in ((mp.mpf('0.3'), mp.mpf('0.7')), (mp.mpf('0.6'), mp.mpf('0.6')), (mp.mpf(1), mp.mpf(1))):
    T = mp.mpf(10)**8
    num = mp.quad(lambda x: F(l/mp.sqrt(x*x+d*d)), [0, 1, 10, 100, 1e3, 1e4, 1e5, 1e6, 1e7, T]) - mp.pi*l*mp.log(T)
    cf = mp.pi*(l*(1+mp.log(2)) + d*mp.log(d) - (d+l)*mp.log(d+l))
    ck(f"N9 J(l={mp.nstr(l,2)}, d={mp.nstr(d,2)})", abs(num-cf) < mp.mpf('1e-6'), f"num {mp.nstr(num,12)} closed {mp.nstr(cf,12)}")
# (2) N11
for z in (mp.mpf('0.3'), mp.mpf('0.8')):
    S = mp.sqrt(1-z*z); chi = S*S
    i1 = mp.quad(lambda m: (mp.sqrt(1-m*m)-S)/abs(m-z), [-1, z, 1]); c1 = S*mp.log(4*chi) - 2*S + 2*z*mp.asin(z)
    th = lambda f: mp.quad(lambda t: f(mp.sin(t)), [-mp.pi/2, mp.asin(z), mp.pi/2])   # mu = sin t, dmu/sqrt(1-mu^2) = dt
    i2 = th(lambda m: abs(m-z)); c2 = 2*(S + z*mp.asin(z))
    ck(f"N11 at z={mp.nstr(z,2)}", abs(i1-c1) < mp.mpf('1e-15') and abs(i2-c2) < mp.mpf('1e-15'), f"{mp.nstr(i1-c1,3)}, {mp.nstr(i2-c2,3)}")
# (3) b(q) via N13
def a_of(r, z): S = mp.sqrt(1-z*z); return mp.pi*S*(S*S + r*r/2)
def b_of(r, z):
    S = mp.sqrt(1-z*z); chi = S*S; c = chi + r*r/2; u = r/S
    def g(ph):
        L = 1-u*mp.cos(ph); D = mp.sqrt(1+u*u-2*u*mp.cos(ph))
        return L*(D*mp.log(D) - (D+L)*mp.log(D+L)) if D > 0 else mp.mpf(0)
    avg = mp.quad(g, [0, mp.pi/2, mp.pi])/mp.pi
    return mp.pi*(S + (c+1)*z*mp.asin(z) + S*c*mp.log(4*S) + S**3*avg)
ck("N13 b(0,0) = pi", abs(b_of(0, 0) - mp.pi) < mp.mpf('1e-25'))
for z in (mp.mpf('0.5'), mp.mpf('0.8')):
    S = mp.sqrt(1-z*z); n14 = mp.pi*(S + (2-z*z)*z*mp.asin(z) + S**3*mp.log(S))
    ck(f"N14 axis formula equals N13 at z={mp.nstr(z,2)}", abs(n14 - b_of(0, z)) < mp.mpf('1e-20'))
# chat brute-force lambda*Delta values (from V-needle probe logs; probe2 ran lambda=1e3,1e4,1e5 with labels one decade low)
data = {(0.5, 0): {1e3: 26.8389, 1e4: 34.98473}, (0.8, 0): {1e3: 30.03967, 1e4: 39.59555}, (0, 0.5): {1e3: 17.95216, 1e4: 22.65922},
        (0.5, 0.5): {1e3: 19.74774, 1e4: 25.23763, 1e5: 30.72023}, (0.3, 0.7): {1e3: 12.88384, 1e4: 15.75979, 1e5: 18.62799},
        (0, 0.8): {1e3: 9.385056, 1e4: 10.95659, 1e5: 12.5202}}
for (r, z), vals in data.items():
    a = a_of(mp.mpf(r), mp.mpf(z)); b = b_of(mp.mpf(r), mp.mpf(z))
    meas = {L: mp.mpf(v) - a*mp.log(L) for L, v in vals.items()}
    Ls = sorted(meas); gaps = [abs(meas[L]-b) for L in Ls]
    shrinking = all(gaps[i+1] < gaps[i] for i in range(len(gaps)-1)) and gaps[-1] < mp.mpf('0.02')
    ck(f"N13 b at q=({r},{z}) vs brute force", shrinking, f"b={mp.nstr(b,10)}  measured " + ", ".join(f"{int(L):.0e}:{mp.nstr(meas[L],8)}" for L in Ls))
# (4) centre Hessian E_rhorho(0) at lambda = 5, 10 (primitive E, FD)
for lam, claim in ((5, mp.mpf('-0.0243031238')), (10, mp.mpf('-0.1829940379'))):
    hh = mp.mpf('0.01'); e = {k: E_ref(mp.mpf(lam), k*hh, 0) for k in (0, 1, 2)}
    d2 = (-e[2] + 16*e[1] - 30*e[0] + 16*e[1] - e[2])/(12*hh*hh)      # even function: E(-x) = E(x)
    ck(f"centre E_rhorho(0) at lambda={lam}", abs(d2-claim) < mp.mpf('1e-5'), f"chat FD {mp.nstr(d2,10)}  Astra {mp.nstr(claim,10)}")
print(f"SUMMARY {sum(res)}/{len(res)} PASS")
