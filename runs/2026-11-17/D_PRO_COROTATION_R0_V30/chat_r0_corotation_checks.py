#!/usr/bin/env python3
"""chat R0: independent derivation checks of Astra's co-rotation design (2026-11-17 report)."""
import sympy as sp
from fractions import Fraction as F
res = []
def ck(n, ok, d=""):
    res.append(bool(ok)); print(("PASS " if ok else "FAIL ") + n + (" :: " + d if d else ""))

lam, R, beta, rho, z, H, V = sp.symbols('lambda R beta rho z H V', positive=True)
# (9): E_beta = -R sin E_rho + lam R cos E_z with E_rho = rho H, E_z = z V
Eb = -R*sp.sin(beta)*(R*sp.cos(beta)*H) + lam*R*sp.cos(beta)*(lam*R*sp.sin(beta)*V)
ck("(9) E_beta = R^2 sin cos (lam^2 V - H)", sp.simplify(Eb - R**2*sp.sin(beta)*sp.cos(beta)*(lam**2*V - H)) == 0)

# co-rotation: m = O_beta m0, xi = O_beta eta ; d, e
b = sp.symbols('b'); m0x, m0z, ex, ez = sp.symbols('m0x m0z ex ez')
d = lam**2 - 1; e = d/lam**2
mx = sp.cos(b)*m0x - sp.sin(b)*m0z; mz = sp.sin(b)*m0x + sp.cos(b)*m0z
xx = sp.cos(b)*ex - sp.sin(b)*ez;   xz = sp.sin(b)*ex + sp.cos(b)*ez
ck("rotation: m_z' = m_x, m_x' = -m_z", sp.simplify(sp.diff(mz, b) - mx) == 0 and sp.simplify(sp.diff(mx, b) + mz) == 0)
C = 1 + d*mz**2; B = 1 - e*xz**2
k, sig = sp.symbols('k sigma', positive=True)
gam = k/(sig*sp.sqrt(C*B))
T = d*mx*mz/C - e*xx*xz/B
ck("(5) gamma_beta = -gamma T", sp.simplify(sp.diff(gam, b) + gam*T) == 0)
Tb_doc = d*(mx**2 - mz**2)/C - 2*(d*mx*mz/C)**2 - e*(xx**2 - xz**2)/B - 2*(e*xx*xz/B)**2
ck("(6) T_beta", sp.simplify(sp.diff(T, b) - Tb_doc) == 0)
# (7),(8) with G' = -2R(gamma), R' abstract
g = sp.symbols('g'); Rf = sp.Function('Rf')
G = sp.Function('G')
f = k*G(gam)
# do it by hand-chain: f_beta = k G'(gam) gam_b
Gp = lambda y: -2*Rf(y)
fb_chain = k*Gp(gam)*sp.diff(gam, b)
ck("(7) f_beta = 2 k gamma R T", sp.simplify(fb_chain - 2*k*gam*Rf(gam)*T) == 0)
# manual: d/db[2k gam R T] = 2k[gam_b R T + gam R' gam_b T + gam R T_b]
g_s, R_s, T_s, Tb_s, Rp_s = sp.symbols('g R T Tb Rp')
manual = 2*k*((-g_s*T_s)*R_s*T_s + g_s*Rp_s*(-g_s*T_s)*T_s + g_s*R_s*Tb_s)
doc = 2*k*g_s*(R_s*Tb_s - (R_s + g_s*Rp_s)*T_s**2)
ck("(8) f_bb = 2k gamma {R T_b - (R + gamma R') T^2}", sp.expand(manual - doc) == 0)

# (13) building blocks
t = sp.symbols('t', positive=True)
ck("square completion: (1+d t^2)^2 - 4 lam^2 t^2 (1-t^2) = (1-(lam^2+1)t^2)^2",
   sp.expand((1 + d*t**2)**2 - 4*lam**2*t**2*(1 - t**2) - (1 - (lam**2 + 1)*t**2)**2) == 0)
L5 = F(5); d5 = L5**2 - 1; l5 = L5 - 1/L5
ck("C_lambda(5) = 2d + 2 l^2 = 2352/25", 2*d5 + 2*l5**2 == F(2352, 25))
ck("l = d/lam", sp.simplify((lam - 1/lam) - d/lam) == 0)
ck("pi^2 C/4 <= 1176/5 at C = 2352/25 (pi^2 < 10)", F(10)*F(2352, 25)/4 == F(1176, 5))
lhs = F(1176, 5)*F(256, 225)*(F(1, 16)*F(1, 4096) + F(1, 2)*F(1, 4096)**2)
ck("(15) bound < 1/240", lhs < F(1, 240) and F(1176, 5)*F(256, 225) == F(301056, 1125), f"{float(lhs):.6g} vs {1/240:.6g}")
import math
ck("min(b, pi/2-b)/(sin b cos b) <= pi/2 (grid)", max(min(x, math.pi/2 - x)/(math.sin(x)*math.cos(x)) for x in [i*math.pi/2/2000 for i in range(1, 2000)]) <= math.pi/2 + 1e-12)
# cap integral: (1/4pi) int_A k dOmega, dOmega = 2 pi dq, k = 1-R+R q, q in [0,kappa]
q, kap = sp.symbols('q kappa', positive=True)
ck("(1/4pi) int_cap k = (1/2)((1-R)kappa + R kappa^2/2)",
   sp.simplify(sp.integrate((1 - R + R*q)*2*sp.pi, (q, 0, kap))/(4*sp.pi) - sp.Rational(1, 2)*((1 - R)*kap + R*kap**2/2)) == 0)

# (7.1) counterexample
l2 = F(2); dd = l2**2 - 1; ee = dd/l2**2
cb, sb = F(3, 5), F(4, 5)
m = (-cb, -sb); xi = (-cb, -sb)
Cv = 1 + dd*m[1]**2; Bv = 1 - ee*xi[1]**2; Tv = dd*m[0]*m[1]/Cv - ee*xi[0]*xi[1]/Bv
ck("(7.1) C=73/25, B=13/25, T=-189/949", (Cv, Bv, Tv) == (F(73, 25), F(13, 25), F(-189, 949)))

# (17)-(19) equatorial
r, s = sp.symbols('r s', positive=True); Q, H4, c6 = sp.symbols('Q H4 c6')
E = Q*r**2/2 + H4*r**4/24 + c6*r**6
Fr = sp.diff(E, r); Phi = sp.expand((Fr/r).subs(r, sp.sqrt(s)))
ck("(17) Phi_s = (r E_rr - E_r)/(2 r^3)", sp.simplify(sp.diff(Phi, s).subs(s, r**2) - (r*sp.diff(E, r, 2) - Fr)/(2*r**3)) == 0)
ck("(18) Phi(0)=Q, Phi_s(0)=H4/6", sp.simplify(Phi.subs(s, 0) - Q) == 0 and sp.simplify(sp.diff(Phi, s).subs(s, 0) - H4/6) == 0)
tt = sp.symbols('tt', positive=True)
rhs19 = sp.Rational(1, 4)*sp.integrate((1 - tt**2)*sp.diff(E, r, 4).subs(r, tt*r), (tt, 0, 1))
ck("(19) Phi_s(r^2) = 1/4 int (1-t^2) E''''(tr) dt", sp.simplify(sp.diff(Phi, s).subs(s, r**2) - rhs19) == 0)

# (20) axis kernel
mu, tz = sp.symbols('mu t', real=True)
A = 1 - tz*mu; D = sp.sqrt(1 - mu**2 + lam**2*(mu - tz)**2); w = sp.sqrt(lam**2*(1 - mu**2) + mu**2)
gm = lam*A/(w*D)
lhs20 = sp.diff(A, tz)*sp.Symbol('G') + A*(-2*sp.Symbol('R'))*sp.diff(gm, tz)
rhs20 = -mu*sp.Symbol('G') - 2*lam*A*sp.Symbol('R')*(1 - mu**2)*((lam**2 - 1)*mu - lam**2*tz)/(w*D**3)
ck("(20) axis kernel d/dt[A G(gamma)]", sp.simplify(lhs20 - rhs20) == 0)
# pull-back: (Lxi - Lq).L^{-1}xi = 1 - q.xi ; cos alpha = k/(D sqrt(B))
x1, x2, x3, q1, q3 = sp.symbols('x1 x2 x3 q1 q3')
Lm = sp.diag(1, 1, lam); X = Lm*sp.Matrix([x1, x2, x3]); P = Lm*sp.Matrix([q1, 0, q3]); N = Lm.inv()*sp.Matrix([x1, x2, x3])
ck("pull-back (x-p).N = 1 - q.xi on sphere", sp.simplify(((X - P).T*N)[0] - (x1**2 + x2**2 + x3**2 - q1*x1 - q3*x3)) == 0)
print(f"SUMMARY {sum(res)}/{len(res)} PASS")
