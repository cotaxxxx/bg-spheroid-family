"""Vectorised B7 kernel jets (chat independent verifier)."""
import numpy as np
from b7iv_ia import IA, JT
CL = float(np.nextafter(0.16, -np.inf))   # float(4/25) rounds UP; use the next lower double
assert __import__("fractions").Fraction(CL) < __import__("fractions").Fraction(4, 25)

def F_K(V, eps, var=None, form='both'):
    """V: list of 7 IA arrays (lam,tau,delta,y,p,t,u); eps=+1/-1; var: jet variable index."""
    if form == 'both':
        F1, K1 = F_K(V, eps, var, 'kappa'); F2, K2 = F_K(V, eps, var, 'eta')
        return F1.meet(F2), K1.meet(K2)
    z = IA(0.0); one = IA(1.0)
    xs = [JT(v, one if i == var else z, z) for i, v in enumerate(V)]
    lam, tau, delta, y, p, t, u = xs
    tt = tau.sq()
    Ac = (1 - tt) / (1 + tt); Bs = 2 * tau / (1 + tt)
    x = y * (2 - y)
    A2 = Ac.sq()
    N = 1 - A2 * x
    sN = N.sqrt()
    M = delta + (1 - delta) * A2 * x
    s = ((1 - delta) * N).sqrt()
    rs = s.sqrt()
    qx = (1 - y) * Ac / sN; qz = Bs / sN
    pp = p.sq()
    sig = 2 * p / (1 + pp); g = (1 - pp) / (1 + pp)
    tq = t.sq()
    cb = eps * ((1 - tq) / (1 + tq)); sb = 2 * t / (1 + tq)
    dv = M / (1 + s)
    if form == 'kappa':
        kap = 2 * rs * sig / dv
        root = (1 + kap.sq()).sqrt(); cp = 1 / root; sp = kap / root
        W = 4 * sig / (dv.sq() + 4 * s * sig.sq()).sqrt()
    else:
        eta = dv / (2 * rs * sig)
        root = (1 + eta.sq()).sqrt(); cp = eta / root; sp = 1 / root
        W = 2 / (rs * root)
    L = cp - sig * sp / rs
    Jt = g * sp / rs
    ox = L * qx - Jt * cb * qz
    oz = L * qz + Jt * cb * qx
    s2 = sig.sq()
    xx = (1 - 2 * s2) * qx - 2 * sig * g * cb * qz
    xy = 2 * sig * g * sb
    xz = (1 - 2 * s2) * qz + 2 * sig * g * cb * qx
    Hh = cp + rs * sig * sp
    l2 = lam.sq()
    V2 = 1 - (1 - l2) * oz.sq()
    V2 = V2.withv(V2.v.clamp(CL, 1.0))            # |omega|=1, lam>=2/5
    U2 = V2 - ox.sq()
    w2 = l2 * (xx.sq() + xy.sq()) + xz.sq()
    w2 = w2.withv(w2.v.clamp(CL, 1.0))
    w = w2.sqrt()
    T = w * V2.sqrt()
    G = lam * Hh
    E = -(s * qx * Jt.sq() * sb.sq()) - s * Jt * cb * oz + (1 - l2) * xx * oz.sq()
    P = Hh.sq() * U2
    R = E.sq()
    uu = u.sq()
    Bh = (1 + uu) * T + (1 - uu) * G
    Bh = Bh.withv(Bh.v.clamp(CL, None))
    num = (1 + uu) * T * (P - 2 * R) + (1 - uu) * G * (P - R)
    den = V2.sq() * Bh.sq()
    F = W * num / den
    jac = 2 * (1 - pp) / (1 + pp).sq() * 2 / (1 + tq)
    # two algebraically identical groupings; each encloses K, so their meet does too
    K = (F * jac).meet(W * jac * num / den)
    return F, K

def K2(V, var=None):
    return F_K(V, 1, var)[1] + F_K(V, -1, var)[1]
