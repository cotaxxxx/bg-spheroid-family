#!/usr/bin/env python3
"""chat I2 check of clean-room derivation R1 (SHA 1e53f74e...) against the first lineage.
Auditor-side only. (1) symbolic: c1, c2, G2, F_e/F_a geometry; (2) numeric: R1's algorithms
implemented as written, evaluated at lambda = 47/10, compared with first-lineage records and
chat's brute-force primitive-definition values."""
import sympy as sp, mpmath as mp
res = []
def ck(n, ok, d=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + n + (" :: " + d if d else ""))

# ---- symbolic -----------------------------------------------------------------
t, beta, gam, S, n, lam, w, u, v = sp.symbols('t beta gamma S n lambda w u v', positive=True)
Afun = sp.Function('A')
B = 1 - beta*t; D = sp.sqrt(S - 2*gam*t + t**2); c = B/(n*D)
c0 = c.subs(t, 0); c1 = sp.diff(c, t).subs(t, 0); c2 = sp.diff(c, t, 2).subs(t, 0)
ck("c0 = 1/(n sqrt S)", sp.simplify(c0 - 1/(n*sp.sqrt(S))) == 0)
ck("c1 = (gamma/S - beta)/(n sqrt S)", sp.simplify(c1 - (gam/S - beta)/(n*sp.sqrt(S))) == 0)
ck("c2 = (-1/S + 3gamma^2/S^2 - 2 beta gamma/S)/(n sqrt S)",
   sp.simplify(c2 - (-1/S + 3*gam**2/S**2 - 2*beta*gam/S)/(n*sp.sqrt(S))) == 0)
A1, A2 = sp.symbols('A1 A2')
x = sp.symbols('x')
G2_direct = sp.diff(B*Afun(c), t, 2).subs(t, 0)
G2_direct = G2_direct.subs(sp.Subs(sp.Derivative(Afun(x), x, 2), x, c0), A2) if False else G2_direct
# evaluate with a concrete analytic A to compare: A = acos^2
Aex = lambda y: sp.acos(y)**2
G2_true = sp.diff(B*Aex(c), t, 2).subs(t, 0)
A1v = sp.diff(Aex(x), x).subs(x, c0); A2v = sp.diff(Aex(x), x, 2).subs(x, c0)
G2_R1 = A2v*c1**2 + A1v*c2 - 2*beta*A1v*c1
worst = 0
for bb, gg, SS, nn in [(sp.Rational(3,10), sp.Rational(1,5), 2, sp.Rational(7,10)), (sp.Rational(-1,2), sp.Rational(9,10), 5, sp.Rational(2,5)), (sp.Rational(1,10), sp.Rational(-3,10), sp.Rational(3,2), sp.Rational(9,10))]:
    val = (G2_true - G2_R1).subs({beta: bb, gam: gg, S: SS, n: nn})
    worst = max(worst, abs(sp.N(val, 60)))
ck("G2 = A2 c1^2 + A1 c2 - 2 beta A1 c1 (vs direct d2/dt2 of B*acos^2(c)), exact rationals, 60 digits", worst < 1e-50, str(sp.N(worst,3)))
# geometry: X = (u, v, lam w) on sphere, N = (u, v, w/lam); p = (t,0,0) and (0,0,t)
X = sp.Matrix([u, v, lam*w]); N = sp.Matrix([u, v, w/lam]); sph = {v**2: 1 - u**2 - w**2}
Se = 1 + (lam**2 - 1)*w**2
for name, P, bexp, gexp in [("equatorial", sp.Matrix([t, 0, 0]), u, u), ("axial", sp.Matrix([0, 0, t]), w/lam, lam*w)]:
    Bp = sp.expand((X - P).dot(N)); D2 = sp.expand((X - P).dot(X - P))
    okB = sp.simplify(sp.expand(Bp.subs(sph)) - (1 - bexp*t)) == 0
    okD = sp.simplify(sp.expand(D2.subs(sph)) - (Se - 2*gexp*t + t**2)) == 0
    ck(f"{name}: B = 1 - beta t and D^2 = S - 2 gamma t + t^2", okB and okD)
ck("n^2 = 1 - w^2 + w^2/lam^2 = |N|^2 on sphere", sp.simplify(sp.expand(N.dot(N)).subs(sph) - (1 - w**2 + w**2/lam**2)) == 0)
ck("arccos c = 2 arcsin sqrt((1-c)/2)", abs(mp.acos(mp.mpf('0.37')) - 2*mp.asin(mp.sqrt((1-mp.mpf('0.37'))/2))) < mp.mpf('1e-35'))

# ---- numeric: R1 algorithms as written ----------------------------------------
mp.mp.dps = 20
def Aj(c0, j):  # derivatives of acos^2 at c0
    return mp.diff(lambda y: mp.acos(y)**2, c0, j)
def G2num(bt, gm, L, ww):
    SS = 1 + (L*L - 1)*ww*ww; nn = mp.sqrt(1 - ww*ww + ww*ww/(L*L))
    c0 = 1/(nn*mp.sqrt(SS)); c1 = (gm/SS - bt)/(nn*mp.sqrt(SS))
    c2 = (-1/SS + 3*gm*gm/SS**2 - 2*bt*gm/SS)/(nn*mp.sqrt(SS))
    a1, a2 = Aj(c0, 1), Aj(c0, 2)
    return a2*c1*c1 + a1*c2 - 2*bt*a1*c1
def Qint(L, axial=False):
    def f(ww, ph):
        uu = mp.sqrt(1 - ww*ww)*mp.cos(ph)
        return G2num(ww/L, L*ww, L, ww) if axial else G2num(uu, uu, L, ww)
    return 2*mp.quad(f, [-1, 0, 1], [0, mp.pi/2, mp.pi])/(4*mp.pi)
def H4int(L):
    def f(ww, ph):
        uu = mp.sqrt(1 - ww*ww)*mp.cos(ph)
        SS = 1 + (L*L - 1)*ww*ww; nn = mp.sqrt(1 - ww*ww + ww*ww/(L*L))
        # truncated series arithmetic mod t^5 (lists of 5 coeffs)
        def mul(a, b): return [sum(a[i]*b[k-i] for i in range(k+1)) for k in range(5)]
        xs = [mp.mpf(0), -2*uu/SS, 1/SS, 0, 0]
        P = [mp.mpf(0)]*5; xp = [mp.mpf(1), 0, 0, 0, 0]
        for k in range(5):
            P = [P[i] + mp.binomial(-0.5, k)*xp[i] for i in range(5)]; xp = mul(xp, xs)
        P = [p_/mp.sqrt(SS) for p_ in P]
        Bt = [mp.mpf(1), -uu, 0, 0, 0]
        C = [ci/nn for ci in mul(Bt, P)]; c0 = C[0]
        dC = [mp.mpf(0)] + C[1:]
        acc = [mp.mpf(0)]*5; pw = [mp.mpf(1), 0, 0, 0, 0]
        for j in range(5):
            aj = Aj(c0, j)/mp.factorial(j)
            acc = [acc[i] + aj*pw[i] for i in range(5)]; pw = mul(pw, dC)
        F = mul(Bt, acc)
        return F[4]
    return 2*24*mp.quad(f, [-1, 0, 1], [0, mp.pi/2, mp.pi])/(4*mp.pi)
L = mp.mpf(47)/10
Q = mp.re(Qint(L)); Qz = mp.re(Qint(L, axial=True))
ck("R1 Q(4.7) == first lineage 0.0023224244930128758(2)", abs(Q - mp.mpf('0.00232242449301287582')) < mp.mpf('1e-15'), mp.nstr(Q, 17))
ck("R1 Q_z(4.7) == chat brute force 0.09532685683", abs(Qz - mp.mpf('0.09532685683')) < mp.mpf('2e-9'), mp.nstr(Qz, 12))
ck("R1 Q_z(4.7) inside first-lineage enclosure on [4.7,4.71] [0.09025,0.09994]", mp.mpf('0.09025284') < Qz < mp.mpf('0.09993736'))
H4 = mp.re(H4int(L))
ck("R1 H4(4.7) inside first-lineage enclosure on [4.7,4.71] [-1.4967,-1.3925]", mp.mpf('-1.49669437') < H4 < mp.mpf('-1.39252716'), mp.nstr(H4, 12))
d = mp.mpf('1e-4')
Qp = mp.re((Qint(L + d) - Qint(L - d))/(2*d))
ck("R1 Q'(4.7) (= d/dlam of R1 Q) inside first-lineage enclosure [-0.10544,-0.08574]", mp.mpf('-0.10544393') < Qp < mp.mpf('-0.08573940'), mp.nstr(Qp, 10))
print(f"SUMMARY {sum(res)}/{len(res)} PASS")
