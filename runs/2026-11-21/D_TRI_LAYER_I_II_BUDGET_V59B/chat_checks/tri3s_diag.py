"""General-point triaxial enclosures (GeoEncloseReader 0.3.0, V58, chat). L = diag(1, s, st), q in the closed ball.
Integrands (full sphere chart (th, ph) in [0, pi] x [0, 2 pi], weight sin th / (4 pi)):
  E3  = xi3 (g P - F) - L3 S u3 g^2 P                      (gradient trace, bounded)
  H33 = [ P g^2 S^2 (L3^2 - b3^2) - Q z3^2 ] / (D S),  b3 = L3 u3,  z3 = xi3 - g S b3   (chord Hessian, interior only)
  T12 = k g P (u1 u2 - n1 n2)                              (shear tensor, bounded)
Parameters p = (s, t, q1, q2, q3) with a box; mean-value form in the angles (second order) and in the parameters.
Contact: a cell whose D^2 lower bound over (cell x parameter box) is <= DELTA uses an a-priori bound times its measure:
  |E3| <= pi^2/4 + pi L3   (|xi3 (gP - F)| <= pi^2/4;  |L3 S u3 g| = L3^2 |v3| k / D^2 <= L3 since D >= |v|, D >= L3 |v3|, k <= |v|)
  |T12| <= 2 pi            (k g <= 2,  P <= pi,  |u1 u2|, |n1 n2| <= 1/2)
Validity on box ∩ ball: g is clipped to [0, 1] (true for |q| <= 1); mean-value segments from a centre in the ball stay in it."""
import numpy as np
from fractions import Fraction
from mpmath import mpf, pi as mpi
from .fiv import I, iv_frac
from .dual import D
from .tri2 import _grid2, _PQ_d

DELTA = None          # contact mask threshold on D^2; None -> (4/N)^2 (tuned on the rim point, V58 selftest)
PI_HI = float(np.nextafter(np.pi, np.inf))


def _common(s1, c1, s2, c2, s, t, q1, q2, q3):
    xi = [s1*c2, s1*s2, c1]; L = [None, s, s*t]
    v = [xi[0] - q1, xi[1] - q2, xi[2] - q3]; k = 1 - (q1*xi[0] + q2*xi[1] + q3*xi[2])
    Lv = [v[0], s*v[1], L[2]*v[2]]; D2 = Lv[0].sq() + Lv[1].sq() + Lv[2].sq()
    S = (xi[0].sq() + (xi[1]/s).sq() + (xi[2]/L[2]).sq()).sqrt()
    return xi, L, v, k, Lv, D2, S


def _make(kind, safe_mask=None):
    def f(s1, c1, s2, c2, s, t, q1, q2, q3):
        xi, L, v, k, Lv, D2, S = _common(s1, c1, s2, c2, s, t, q1, q2, q3)
        if safe_mask is not None:               # keep contact cells away from 0 so the arithmetic is defined there
            if isinstance(D2, D): D2 = D(I(np.where(safe_mask, D2.v.lo, 1.0), np.where(safe_mask, D2.v.hi, 1.0)), D2.g)
            else: D2 = I(np.where(safe_mask, D2.lo, 1.0), np.where(safe_mask, D2.hi, 1.0))
        Dn = D2.sqrt(); g = (k/(Dn*S)).clip(0.0, 1.0); P, Q, F = _PQ_d(g); u = [x/Dn for x in Lv]
        if kind == "E3":
            return xi[2]*(g*P - F) - L[2]*S*u[2]*g.sq()*P
        if kind == "T12":
            n1 = xi[0]/S; n2 = (xi[1]/s)/S
            return k*g*P*(u[0]*u[1] - n1*n2)
        if kind == "H33":
            b3 = L[2]*u[2]; z3 = xi[2] - g*S*b3
            return (P*(g*S).sq()*(L[2].sq() - b3.sq()) - Q*z3.sq())/(Dn*S)
    return f


def _fallback(kind, s, t, shape):
    if kind == "E3":
        L3hi = (s*t).hi; b = float(np.nextafter(PI_HI**2/4 + PI_HI*L3hi*(1 + 1e-15), np.inf))
    elif kind == "T12":
        b = float(np.nextafter(2*PI_HI, np.inf))
    else:
        raise ValueError("contact cell in an interior-only kernel")
    return I(np.full(shape, -b), np.full(shape, b))


def _graded(N, a, th0=None):
    """theta endpoints clustered at th0 (default the equator) with sinh grading of strength a on each side (0.4.0).
    The steep set of the integrand for an elongated shape is xi3 ~ q3, i.e. theta ~ arccos(q3)."""
    from mpmath import sinh, acos
    if a == 0: return None
    th0 = mpi/2 if th0 is None else mpf(th0)
    n1 = max(2, min(N - 2, int(round(N*float(th0/mpi))))); n2 = N - n1
    left = [th0 - th0*sinh(a*mpf(j)/n1)/sinh(a) for j in range(n1, -1, -1)]
    right = [th0 + (mpi - th0)*sinh(a*mpf(j)/n2)/sinh(a) for j in range(1, n2+1)]
    e = left + right; e[0] = mpf(0); e[-1] = mpi
    return e


def _th0(box):
    """centre of the steep set: arccos of the centre of the q3 range, rounded to a dyadic so grids can be cached."""
    from mpmath import acos
    q3 = (box[4][0] + box[4][1])/2; x = float(acos(mpf(q3.numerator)/q3.denominator))
    return mpf(round(x*256))/256


def enclose(kind, box, N=32, grade=0):
    """box: 5 pairs of Fractions (s, t, q1, q2, q3). Returns an interval enclosing the sphere mean over box ∩ ball.
    grade: equator clustering of the theta cells (0 = uniform)."""
    th0 = _th0(box) if grade else None
    G = _grid2(("sph", N, grade, None if th0 is None else float(th0)), N, 0, mpi, "sin", 2*N, 0, 2*mpi, "one", 1/(4*mpi),
               ends1=_graded(N, grade, th0))
    p0 = [Fraction(a) for a, b in box]; p1 = [Fraction(b) for a, b in box]
    pc = [(a + b)/2 for a, b in zip(p0, p1)]; prad = [(b - a)/2 for a, b in zip(p0, p1)]
    shp = G["C1"].lo.shape
    full = [iv_frac(a, b) for a, b in zip(p0, p1)]
    _, _, _, _, _, D2box, _ = _common(G["S1"], G["C1"], G["S2"], G["C2"], *full)
    thr = DELTA if DELTA is not None else (4.0/N)**2; safe = D2box.lo > thr; ncontact = int((~safe).sum())
    f = _make(kind, safe_mask=safe if ncontact else None)
    m0 = G["m0"]
    # (i) centre parameters: mean value in the two angles
    cen = [iv_frac(x) for x in pc]
    vc = f(G["s1"], G["c1"], G["s2"], G["c2"], *cen)
    z = I(np.zeros(shp)); n = 2
    sa = D(G["S1"], [G["C1"], z]); ca = D(G["C1"], [-G["S1"], z]); sb = D(G["S2"], [z, G["C2"]]); cb = D(G["C2"], [z, -G["S2"]])
    fd = f(sa, ca, sb, cb, *[D.const(x, n) for x in cen])
    cell = vc*m0
    for kk in range(2):
        gk = fd.g[kk]; gm = (gk.lo + gk.hi)*0.5; gr = np.maximum(gk.hi - gm, gm - gk.lo)
        cell = cell + I(gm)*G["m1"][kk] + I(-1.0, 1.0)*I(np.nextafter(gr, np.inf))*G["M1"][kk]
    aw = cell.fsum() if not ncontact else I.where(safe, cell, I(np.zeros(shp))).fsum()
    angular_width = float(aw.hi - aw.lo)
    terms = {}
    # (ii) parameter box: gradient over the box, per parameter with nonzero radius
    act = [j for j in range(5) if prad[j] != 0]
    if act:
        one = I(np.ones(shp)); m = len(act); sumterms = []
        pars = []
        for j in range(5):
            if j in act:
                gl = [z]*m; gl[act.index(j)] = one; pars.append(D(I(np.full(shp, full[j].lo), np.full(shp, full[j].hi)), gl))
            else:
                pars.append(D.const(I(np.full(shp, full[j].lo), np.full(shp, full[j].hi)), m))
        fp = f(D.const(G["S1"], m), D.const(G["C1"], m), D.const(G["S2"], m), D.const(G["C2"], m), *pars)
        for idx, j in enumerate(act):
            Gj = (fp.g[idx]*m0).fsum(); tw = Gj*iv_frac(-prad[j], prad[j]); sumterms.append(tw)
            terms[j] = float(tw.hi - tw.lo)
    if ncontact:
        raise ValueError('tri3s diagnostic: contact cells not handled')
    out = cell.fsum()
    for tw in (sumterms if act else []): out = out + tw
    enclose.last = {"contact_cells": ncontact, "terms": terms, "angular_width": angular_width, "total_width": float(out.hi - out.lo)}
    return out


def W3(box, N=32, grade=0):
    e = enclose("E3", box, N, grade); return e/iv_frac(box[4][0], box[4][1])


def C12(box, N=32, grade=0):
    e = enclose("T12", box, N, grade); return e/(iv_frac(box[2][0], box[2][1])*iv_frac(box[3][0], box[3][1]))


def H33(box, N=32, grade=0):
    return enclose("H33", box, N, grade)
