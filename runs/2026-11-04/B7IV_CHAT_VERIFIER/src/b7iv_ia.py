"""Vectorised rigorous interval arithmetic (float64 endpoints, outward rounding)
and second-order directional jets.  Chat independent B7 verifier.

Every elementary result (+,-,*,/,sqrt) of IEEE-754 binary64 is correctly
rounded to nearest, so moving each computed endpoint one ulp outward with
nextafter gives a rigorous enclosure.  No producer code is used.
"""
import numpy as np
from fractions import Fraction as Fr

NINF, PINF = -np.inf, np.inf
dn = lambda x: np.nextafter(x, NINF)
up = lambda x: np.nextafter(x, PINF)

def enclose_fracs(fracs):
    """Exact-or-outward float enclosure of a sequence of rationals."""
    lo = np.empty(len(fracs)); hi = np.empty(len(fracs))
    for i, q in enumerate(fracs):
        f = float(q)
        if Fr(f) == q:
            lo[i] = hi[i] = f
        else:
            lo[i] = dn(f); hi[i] = up(f)
    return lo, hi


# ---- error-free transformations: exact directed rounding of +,*,1/x,sqrt
_SPLIT = 134217729.0          # 2^27 + 1 (Veltkamp)
_TINY = 1e-280                # below this, Dekker products may underflow: always nudge

def _two_sum_err(a, b, s):
    bb = s - a
    return (a - (s - bb)) + (b - bb)

def _split(a):
    c = _SPLIT * a
    hi = c - (c - a)
    return hi, a - hi

def _two_prod_err(a, b, p):
    ah, al = _split(a); bh, bl = _split(b)
    return ((ah * bh - p) + ah * bl + al * bh) + al * bl

def _round_dn(r, e, exact_ok):
    """r approximates r+e exactly; return a double <= r+e."""
    return np.where(exact_ok & (e >= 0), r, dn(r))

def _round_up(r, e, exact_ok):
    return np.where(exact_ok & (e <= 0), r, up(r))

def _sum_dn(a, b):
    with np.errstate(invalid='ignore', over='ignore'):
        s = a + b; e = _two_sum_err(a, b, s)
    ok = np.isfinite(e)
    return _round_dn(s, np.where(ok, e, 1.0), ok)

def _sum_up(a, b):
    with np.errstate(invalid='ignore', over='ignore'):
        s = a + b; e = _two_sum_err(a, b, s)
    ok = np.isfinite(e)
    return _round_up(s, np.where(ok, e, -1.0), ok)

def _prod(a, b):
    """product and a mask/err usable for directed rounding."""
    with np.errstate(invalid='ignore', over='ignore', under='ignore'):
        p = a * b
        e = _two_prod_err(a, b, p)
    zero_exact = (a == 0) | (b == 0)
    ok = (np.isfinite(e) & (np.abs(p) >= _TINY) & (np.abs(a) < 1e290) & (np.abs(b) < 1e290)) | zero_exact
    e = np.where(zero_exact, 0.0, np.where(np.isfinite(e), e, 0.0))
    return p, e, ok


class IA:
    __slots__ = ('lo', 'hi')
    def __init__(s, lo, hi=None):
        s.lo = np.asarray(lo, dtype=float)
        s.hi = s.lo if hi is None else np.asarray(hi, dtype=float)
    @staticmethod
    def c(x):
        if isinstance(x, IA):
            return x
        if isinstance(x, (int, float)) and float(x) == x and abs(x) < 2**52:
            return IA(float(x))
        q = Fr(x); lo, hi = enclose_fracs([q]); return IA(lo[0], hi[0])
    @staticmethod
    def from_pairs(pairs):
        lo, _ = enclose_fracs([Fr(a) for a, b in pairs])
        _, hi = enclose_fracs([Fr(b) for a, b in pairs])
        return IA(lo, hi)
    def __add__(s, o):
        o = IA.c(o); return IA(_sum_dn(s.lo, o.lo), _sum_up(s.hi, o.hi))
    __radd__ = __add__
    def __neg__(s):
        return IA(-s.hi, -s.lo)
    def __sub__(s, o):
        o = IA.c(o); return IA(_sum_dn(s.lo, -o.hi), _sum_up(s.hi, -o.lo))
    def __rsub__(s, o):
        return IA.c(o) - s
    def __mul__(s, o):
        o = IA.c(o)
        los = []; his = []
        for a in (s.lo, s.hi):
            for b in (o.lo, o.hi):
                p, e, ok = _prod(a, b)
                los.append(_round_dn(p, e, ok)); his.append(_round_up(p, e, ok))
        lo = np.minimum(np.minimum(los[0], los[1]), np.minimum(los[2], los[3]))
        hi = np.maximum(np.maximum(his[0], his[1]), np.maximum(his[2], his[3]))
        return IA(lo, hi)
    __rmul__ = __mul__
    def sq(s):
        pa, ea, oka = _prod(s.lo, s.lo); pb, eb, okb = _prod(s.hi, s.hi)
        la, ua = _round_dn(pa, ea, oka), _round_up(pa, ea, oka)
        lb, ub = _round_dn(pb, eb, okb), _round_up(pb, eb, okb)
        lo = np.where(s.lo >= 0, la, np.where(s.hi <= 0, lb, 0.0))
        lo = np.maximum(lo, 0.0)
        return IA(lo, np.maximum(ua, ub))
    @staticmethod
    def _recip(x):
        """(lower, upper) of 1/x for nonzero x (elementwise)."""
        with np.errstate(divide='ignore', invalid='ignore', over='ignore', under='ignore'):
            r = 1.0 / x
            p, e, ok = _prod(r, x)
            d = (p - 1.0) + e          # sign(d)*sign(x) = sign(r - 1/x)
        ok = ok & np.isfinite(r) & (np.abs(r) >= _TINY)
        sgn = np.sign(d) * np.sign(x)
        lo = np.where(ok & (sgn <= 0), r, dn(r))
        hi = np.where(ok & (sgn >= 0), r, up(r))
        return lo, hi
    def inv(s):
        bad = (s.lo <= 0) & (s.hi >= 0)
        l1, _ = IA._recip(s.hi); _, h1 = IA._recip(s.lo)
        return IA(np.where(bad, NINF, l1), np.where(bad, PINF, h1))
    def __truediv__(s, o):
        return s * IA.c(o).inv()
    def __rtruediv__(s, o):
        return IA.c(o) * s.inv()
    @staticmethod
    def _sqrt(x):
        with np.errstate(invalid='ignore', under='ignore'):
            r = np.sqrt(x)
            p, e, ok = _prod(r, r)
            d = (p - x) + e            # sign(r - sqrt(x))
        ok = ok & np.isfinite(r) & ((x == 0) | (x >= _TINY))
        lo = np.where(ok & (d <= 0), r, dn(r)); hi = np.where(ok & (d >= 0), r, up(r))
        return np.maximum(lo, 0.0), hi
    def sqrt(s):
        bad = s.lo < 0
        lo, _ = IA._sqrt(np.maximum(s.lo, 0.0)); _, hi = IA._sqrt(np.maximum(s.hi, 0.0))
        return IA(np.where(bad, np.nan, lo), np.where(bad, np.nan, hi))
    def clamp(s, lo=None, hi=None):
        """Intersect with an externally PROVED range."""
        L = s.lo if lo is None else np.maximum(s.lo, lo)
        H = s.hi if hi is None else np.minimum(s.hi, hi)
        return IA(L, H)
    def meet(s, o):
        # both operands enclose the same quantity; fmax/fmin skip a NaN side
        return IA(np.fmax(s.lo, o.lo), np.fmin(s.hi, o.hi))


class JT:
    """Directional 2-jet with interval components."""
    __slots__ = ('v', 'a', 'b')
    def __init__(s, v, a=None, b=None):
        s.v = v; s.a = IA(0.0) if a is None else a; s.b = IA(0.0) if b is None else b
    @staticmethod
    def c(x):
        return x if isinstance(x, JT) else JT(IA.c(x))
    def __add__(s, o):
        o = JT.c(o); return JT(s.v + o.v, s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s):
        return JT(-s.v, -s.a, -s.b)
    def __sub__(s, o):
        o = JT.c(o); return JT(s.v - o.v, s.a - o.a, s.b - o.b)
    def __rsub__(s, o):
        return JT.c(o) - s
    def __mul__(s, o):
        o = JT.c(o)
        return JT(s.v * o.v, s.a * o.v + s.v * o.a, s.b * o.v + 2 * (s.a * o.a) + s.v * o.b)
    __rmul__ = __mul__
    def sq(s):
        return JT(s.v.sq(), 2 * (s.v * s.a), 2 * (s.a.sq() + s.v * s.b))
    def inv(s):
        r = s.v.inv(); r2 = r.sq()
        return JT(r, -(s.a * r2), 2 * (s.a.sq() * r2 * r) - s.b * r2)
    def __truediv__(s, o):
        return s * JT.c(o).inv()
    def __rtruediv__(s, o):
        return JT.c(o) * s.inv()
    def sqrt(s):
        r = s.v.sqrt()
        return JT(r, s.a / (2 * r), s.b / (2 * r) - s.a.sq() / (4 * (s.v * r)))
    def withv(s, v):
        return JT(v, s.a, s.b)
    def meet(s, o):
        return JT(s.v.meet(o.v), s.a.meet(o.a), s.b.meet(o.b))
