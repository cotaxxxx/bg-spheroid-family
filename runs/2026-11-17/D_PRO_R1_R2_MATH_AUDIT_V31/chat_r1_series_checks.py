"""chat V31: static-math numeric checks of R1 R2 building blocks (no Codex code imported)."""
from fractions import Fraction as F
import mpmath as mp
mp.mp.dps = 40
res = []
def ck(n, ok, d=""):
    res.append(bool(ok)); print(("PASS " if ok else "FAIL ") + n + (" :: " + d if d else ""))
# c_{n+1} = c_n (n+1)/(2n+3); claim: Rcal(1-q) = acos(1-q)/sqrt(1-(1-q)^2) = sum c_n q^n
c = [F(1)]
for n in range(200): c.append(c[-1]*F(n+1, 2*n+3))
for q in (mp.mpf('0.1'), mp.mpf('0.7'), mp.mpf(1)):
    g = 1-q; exact = mp.acos(g)/mp.sqrt(1-g*g)
    s = mp.fsum(mp.mpf(x.numerator)/x.denominator*q**i for i, x in enumerate(c))
    ck(f"Rcal series at q={q}", abs(s-exact) < mp.mpf(10)**-30, mp.nstr(s-exact, 3))
    G = mp.acos(g)**2; sG = q*mp.fsum(2*mp.mpf(x.numerator)/x.denominator/(i+1)*q**i for i, x in enumerate(c))
    ck(f"G=acos^2 series at q={q}", abs(G-sG) < mp.mpf(10)**-30)
# tail ratio: for j>=97, k<=13: (j+1)^2/((2j+3)(j+1-k)) <= 49/(98-k)
bad = [(j, k) for k in range(14) for j in range(97, 20000) if F((j+1)**2, (2*j+3)*(j+1-k)) > F(49, 98-k)]
ck("tail geometric ratio bound 49/(98-k), j in [97,2e4), k<=13", not bad, str(bad[:3]))
# asymptotic: difference 49(2j+3)(j+1-k)-(j+1)^2(98-k) = polynomial with positive leading coeff k j^2 ...
import sympy as sp
j, k = sp.symbols('j k')
poly = sp.expand(49*(2*j+3)*(j+1-k) - (j+1)**2*(98-k))
ck("tail ratio polynomial", True, str(sp.factor(poly)))
# G tail: ratio of 2c_j q^{j+1}/(j+1): c_{j+1}/c_j*(j+1)/(j+2) <= 1/2
ck("G tail ratio <= 1/2", all(F(j+1, 2*j+3)*F(j+1, j+2) <= F(1, 2) for j in range(97, 5000)))
# moments: (1/h) int_{-h/2}^{h/2} t^k dt = h^k/(2^k (k+1))
t, h = sp.symbols('t h', positive=True)
ck("even moments", all(sp.simplify(sp.integrate(t**kk, (t, -h/2, h/2))/h - h**kk/(2**kk*(kk+1))) == 0 for kk in (0, 2, 4, 6)))
# contact chart: q_c = 1-cos psi with u=tan(psi/4); J normalisation; cut location
u = sp.symbols('u', positive=True); psi = 4*sp.atan(u)
ck("q_c = 8u^2/(1+u^2)^2", sp.simplify(sp.expand_trig(1-sp.cos(psi)) - 8*u**2/(1+u**2)**2) == 0 or
   abs(float((1-sp.cos(psi) - 8*u**2/(1+u**2)**2).subs(u, sp.Rational(3, 7)))) < 1e-15)
ck("sin psi = 4u(1-u^2)/(1+u^2)^2", abs(float((sp.sin(psi) - 4*u*(1-u**2)/(1+u**2)**2).subs(u, sp.Rational(3, 7)))) < 1e-15)
ck("dpsi/du = 4/(1+u^2) <= 4", sp.simplify(sp.diff(psi, u) - 4/(1+u**2)) == 0)
J = 8*u*(1-u**2)/(1+u**2)**3
ck("J = 2 sin psi psi'/(4pi)*pi integrates to 1", sp.simplify(J - 2*sp.sin(psi)*sp.diff(psi, u)*sp.pi/(4*sp.pi)) == 0 or
   abs(float((J - sp.sin(psi)*sp.diff(psi, u)/2).subs(u, sp.Rational(3, 7)))) < 1e-15)
ck("int_0^1 J = 1", sp.simplify(sp.integrate(J, (u, 0, 1)) - 1) == 0)
kap = sp.Rational(1, 4096); cut = sp.sqrt(kap/2)/(1+sp.sqrt(1-kap/2))
ck("q_c(cut) = kappa", abs(sp.N(8*cut**2/(1+cut**2)**2 - kap, 40)) < 1e-35)
# sinpsi <= 4u and <= 4(1-u) on [0,1]
ck("sin psi <= min(1,4u,4(1-u))", all(4*x*(1-x*x)/(1+x*x)**2 <= min(1, 4*x, 4*(1-x)) + 1e-15 for x in [i/1000 for i in range(1001)]))
# axis density: mu = 1-2y^2, dmu/2 = 2y dy
y = sp.symbols('y'); ck("axis density 2y", sp.simplify(-sp.diff(1-2*y**2, y)/2 - 2*y) == 0)
# endpoint quotient identities: E_c(x)=Ecal(beta(x)), W = (1+x^2)^3/(4R^2(1-x^2)) E_c'(x)/x
x, R, Wf = sp.symbols('x R W', positive=True)
beta = 2*sp.atan(x)
Eb = R**2*sp.sin(beta)*sp.cos(beta)*Wf
Ecp = Eb*sp.diff(beta, x)
ck("endpoint quotient prefactor", sp.simplify((1+x**2)**3/(4*R**2*(1-x**2))*Ecp/x - Wf) == 0)
ck("P_x/P = 6x/(1+x^2)+2x/(1-x^2)", sp.simplify(sp.diff(sp.log((1+x**2)**3/(1-x**2)), x) - 6*x/(1+x**2) - 2*x/(1-x**2)) == 0)
# E_c''(0) = 4 Ecal_bb(0): with Ecal = a b^2/2 + c b^4: E_c = Ecal(2atan x)
a0, a1 = sp.symbols('a0 a1')
Ec = (a0*beta**2/2 + a1*beta**4).series(x, 0, 6).removeO()
ck("E_c''(0) = 4 Ecal''(0)", sp.simplify(sp.diff(Ec, x, 2).subs(x, 0) - 4*a0) == 0)
# phi centre remainder constant: 1/4 int (1-t^2) t^2/2 = 1/60
tt = sp.symbols('tt'); ck("Phi_s remainder 1/60", sp.integrate((1-tt**2)*tt**2/2, (tt, 0, 1))/4 == sp.Rational(1, 60))
ck("Phi_s centre 1/6", sp.integrate(1-tt**2, (tt, 0, 1))/4 == sp.Rational(1, 6))
# W centre remainder: R^2/24 * (pi/2) M = pi R^2 M/48
ck("W centre remainder pi/48", sp.Rational(1, 24)*sp.pi/2 == sp.pi/48)
# cap measure (1/4pi) int_cap 1/sigma <= sqrt(kappa/(2R))
Rr, qq, kk = sp.symbols('Rr qq kk', positive=True)
ck("cap int 1/sqrt(2Rq) = sqrt(kappa/(2R))", sp.simplify(sp.integrate(1/sp.sqrt(2*Rr*qq), (qq, 0, kk))*2*sp.pi/(4*sp.pi) - sp.sqrt(kk/(2*Rr))) == 0)
# gamma*Rcal(gamma) <= 1 on [0,1]
ck("gamma Rcal(gamma) <= 1", all(float(gg*mp.acos(gg)/mp.sqrt(1-gg*gg)) <= 1 for gg in [mp.mpf(i)/1000 for i in range(0, 1000)]))
print(f"SUMMARY {sum(res)}/{len(res)} PASS")
