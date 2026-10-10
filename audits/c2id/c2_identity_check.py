"""chat symbolic check of the C2 identity G_t = T1+T2+T3 (predeclare c0999ff4...b1a8). Exact SymPy only."""
import sympy as sp

s, t, lam = sp.symbols('s t lambda', positive=True)
R, Rg = sp.symbols('R R_gamma')          # independent symbols for R(gamma), R'(gamma)
mu = 1 - s**2
delta = 1 - t
d = s**2 - delta
A = 1 - t*mu
q = 1 - mu**2 + lam**2*(mu - t)**2
w = sp.sqrt(lam**2*(1 - mu**2) + mu**2)   # independent of t
x = s**2
H = (1 - x)*(2 - x) + lam**2*(2 - x)*(x - delta)
N = -s**2*H
gamma = lam*A/(w*sp.sqrt(q))

def zero(e):
    return sp.simplify(sp.expand(e)) == 0

res = {}
# 1
res['1a q = s^2(2-s^2)+lam^2 d^2'] = zero(q - (s**2*(2 - s**2) + lam**2*d**2))
res['1b 1-mu^2 = s^2(2-s^2)'] = zero((1 - mu**2) - s**2*(2 - s**2))
# 3
gt = sp.diff(gamma, t)
res['3a gamma_t = lam*Nsrc/(w q^{3/2}), Nsrc=-mu q - lam^2 A d'] = zero(sp.simplify(gt - lam*(-mu*q - lam**2*A*d)/(w*q**sp.Rational(3, 2))))
res['3b Nsrc = -s^2 H (Lemma 1(i))'] = zero((-mu*q - lam**2*A*d) - N)
# 2: F_t with alpha_t = -gamma_t/sin(alpha), 2 alpha alpha_t = -2 R gamma_t  (R = alpha/sin alpha)
#    d/dt (A alpha^2) = A_t alpha^2 + A*(2 alpha alpha_t) = -mu alpha^2 - 2 A R gamma_t
res['2 A_t = -mu'] = zero(sp.diff(A, t) + mu)
# 4: G_t = d/dt [ s(-mu alpha^2 - 2 A R gamma_t) ] with d(alpha^2)/dt = -2 R gamma_t, dR/dt = Rg*gamma_t
gtt = sp.diff(gt, t)
G = s*(-mu*(-2*R*gt) - 2*(sp.diff(A, t)*R*gt + A*Rg*gt**2 + A*R*gtt))
G_expected_form = s*(4*mu*R*gt - 2*A*Rg*gt**2 - 2*A*R*gtt)
res['4 G_t form'] = zero(G - G_expected_form)
# 5: T1+T2+T3
rho = s/sp.sqrt(q); phi = d/sp.sqrt(q); Ahat = A/sp.sqrt(q)
T1 = -4*(1 - s**2)*R*lam*rho**3*H/w
T2 = -2*Rg*lam**2*H**2*Ahat*rho**5/w**2
T3 = -2*R*lam**3*Ahat*rho**3*(3*phi*H - (2 - s**2)*sp.sqrt(q))/w
diff = sp.expand(G - (T1 + T2 + T3))
cR = sp.simplify(diff.coeff(R)); cRg = sp.simplify(diff.coeff(Rg)); c0 = sp.simplify(diff.subs({R: 0, Rg: 0}))
res['5 coeff of R  in G_t-(T1+T2+T3)'] = sp.simplify(cR) == 0
res['5 coeff of Rg in G_t-(T1+T2+T3)'] = sp.simplify(cRg) == 0
res['5 R,Rg-free part'] = sp.simplify(c0) == 0
res['5b rho^2(2-s^2)+lam^2 phi^2 = 1'] = zero(sp.simplify(rho**2*(2 - s**2) + lam**2*phi**2 - 1))
res['5c Ahat = (2-s^2) s rho - (1-s^2) phi'] = zero(sp.simplify(Ahat - ((2 - s**2)*s*rho - (1 - s**2)*phi)))
# 6
g = sp.symbols('g', positive=True)
Rf = sp.acos(g)/sp.sqrt(1 - g**2)
res['6 R_gamma = (gamma R - 1)/(1-gamma^2)'] = zero(sp.simplify(sp.diff(Rf, g) - (g*Rf - 1)/(1 - g**2)))

for k, v in res.items():
    print(('PASS ' if v else 'FAIL ') + k)
if not all(res.values()):
    print('residues:', 'cR=', cR, 'cRg=', cRg, 'c0=', c0)
print('OVERALL', 'PASS' if all(res.values()) else 'FAIL')
