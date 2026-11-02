"""V6-B directional second-order interval AD primitive; NOT a quadrature certificate.

Underlying I uses S=2**128 outward-rounded arithmetic (v3_fixed_128.py).
A separate pass is required for each of y,p,t,u; no mixed derivatives.
"""
from v3_fixed_128 import I, iv, S
from fractions import Fraction as Q

class D2:
    __slots__=('v','d1','d2')
    def __init__(self,v,d1=0,d2=0):
        self.v,self.d1,self.d2=iv(v),iv(d1),iv(d2)
    @staticmethod
    def variable(interval):return D2(interval,1,0)
    def __add__(a,b):
        b=ad(b);return D2(a.v+b.v,a.d1+b.d1,a.d2+b.d2)
    __radd__=__add__
    def __neg__(a):return D2(-a.v,-a.d1,-a.d2)
    def __sub__(a,b):return a+-ad(b)
    def __rsub__(a,b):return ad(b)-a
    def __mul__(a,b):
        b=ad(b)
        return D2(a.v*b.v,a.d1*b.v+a.v*b.d1,a.d2*b.v+2*a.d1*b.d1+a.v*b.d2)
    __rmul__=__mul__
    def sq(a):return D2(a.v.sq(),2*a.v*a.d1,2*(a.d1.sq()+a.v*a.d2))
    def inv(a):
        if a.v.lo<=0<=a.v.hi: raise ZeroDivisionError('reciprocal domain failure')
        r=iv(1)/a.v
        return D2(r,-a.d1*r.sq(),2*a.d1.sq()*r.sq()*r-a.d2*r.sq())
    def __truediv__(a,b):return a*ad(b).inv()
    def __rtruediv__(a,b):return ad(b)/a
    def sqrt(a):
        if a.v.lo<=0: raise ValueError('C2 sqrt requires strictly positive argument')
        r=a.v.sqrt()
        return D2(r,a.d1/(2*r),a.d2/(2*r)-a.d1.sq()/(4*a.v*r))

def ad(x):return x if isinstance(x,D2) else D2(x)

def intersect_value(a,lower=None,upper=None):
    """Value-only intersection with an EXTERNALLY PROVED bound.
    Caller must supply provenance; derivatives are deliberately untouched.
    """
    a=ad(a);lo=a.v.lo if lower is None else max(a.v.lo,iv(lower).lo)
    hi=a.v.hi if upper is None else min(a.v.hi,iv(upper).hi)
    if lo>hi:raise ValueError('inconsistent proven bound')
    return D2(I.raw(lo,hi),a.d1,a.d2)

if __name__=='__main__':
    # Regression: square crossing zero must have nonnegative value lower bound.
    x=D2.variable(I(-1,2));s=x.sq()
    if not (s.v.lo==0 and s.v.hi>=4*S): raise AssertionError("regression check failed")
    if not (s.d1.lo<=-2*S and s.d1.hi>=4*S): raise AssertionError("regression check failed")
    if not (s.d2.lo<=2*S<=s.d2.hi): raise AssertionError("regression check failed")
    # Rational-point identity tests (enclosure, not equality due to rounding).
    x=D2.variable(I(Q(3,2)));f=(x.sq()+1).inv()
    if not (f.v.lo<=Q(4,13)*S<=f.v.hi): raise AssertionError("regression check failed")
    # Derivative -2x/(x²+1)² = -48/169 at x=3/2.
    if not (f.d1.lo<=Q(-48,169)*S<=f.d1.hi): raise AssertionError("regression check failed")
    # Second derivative (6x²-2)/(x²+1)³ = 736/2197 at x=3/2.
    if not (f.d2.lo<=Q(736,2197)*S<=f.d2.hi): raise AssertionError("regression check failed")
    print('D2 regression PASS: crossing-zero square; inverse value/first/second derivative')
