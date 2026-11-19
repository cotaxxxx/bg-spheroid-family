"""Endpoint-based interval helpers on python-flint arb (midpoint-radius balls).

Arb ball arithmetic can push a squared or intersected wide ball below 0 or to NaN; every helper here
works from explicit endpoints instead (lessons of V49/V50).
"""
from flint import arb, fmpq, ctx
ctx.prec = 128
U01 = arb(0).union(arb(1))
PI = arb.pi()
UNIT = 2**20          # box coordinates are integers in units of 2^-20
VUNIT = 2**36         # ledger values are integers in units of 2^-36


def clip(x, lo, hi):
    """[x] intersected with [lo, hi], using endpoints. Valid only where the true value lies in [lo, hi]."""
    l = x.lower(); u = x.upper(); lo = arb(lo); hi = arb(hi)
    l = l if l > lo else lo; u = u if u < hi else hi
    return l.union(u)


def sqrtp(x):
    """sqrt of the non-negative part of x."""
    l = x.lower(); u = x.upper(); l = l if l > 0 else arb(0)
    return l.sqrt().union(u.sqrt())


def sq(x):
    """x^2 from endpoints (never below 0)."""
    lo = x.lower(); hi = x.upper(); zero = arb(0)
    if lo >= zero: return (lo*lo).union(hi*hi)
    if hi <= zero: return (hi*hi).union(lo*lo)
    m = hi if hi > -lo else -lo
    return zero.union(m*m)


def acos_safe(g):
    """arccos of g clipped to [0, 1] (gamma is a cosine of an angle in [0, pi/2])."""
    lo = g.lower(); hi = g.upper(); one = arb(1); zero = arb(0)
    lo = lo if lo > zero else zero; hi = hi if hi < one else one
    lo = lo if lo < one else one; hi = hi if hi > zero else zero
    return hi.acos().union(lo.acos())


def box_arbs(box):
    """Integer box (l0, l1, r0, r1, z0, z1) in units 2^-20 -> rational endpoints and arb hulls."""
    l0, l1, r0, r1, z0, z1 = [fmpq(int(x), UNIT) for x in box]
    hull = lambda a, b: arb(a).union(arb(b))
    return (l0, l1, r0, r1, z0, z1), hull(l0, l1), hull(r0, r1), hull(z0, z1)
