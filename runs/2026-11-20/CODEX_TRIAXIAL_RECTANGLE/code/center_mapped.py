"""DIAGNOSTIC_ONLY / NOT_EVIDENCE.
Outward binary64 enclosures of the three center Hessian eigenvalues.
Assumptions: IEEE 754 nearest primitive operations, correctly rounded sqrt,
gradual underflow. No floating transcendental function is used.
"""
from functools import lru_cache
from fractions import Fraction
import numpy as np

def down(x): return np.nextafter(x, -np.inf)
def up(x): return np.nextafter(x, np.inf)

class I:
    __array_priority__ = 1000
    def __init__(self, lo, hi=None):
        self.lo=np.asarray(lo,dtype=np.float64)
        self.hi=self.lo if hi is None else np.asarray(hi,dtype=np.float64)
    def __add__(self, other):
        o=iv(other); return I(down(self.lo+o.lo),up(self.hi+o.hi))
    __radd__=__add__
    def __neg__(self): return I(-self.hi,-self.lo)
    def __sub__(self,o): return self+-iv(o)
    def __rsub__(self,o): return iv(o)+-self
    def __mul__(self,other):
        o=iv(other)
        vals=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi]
        return I(down(np.minimum.reduce(np.broadcast_arrays(*vals))),up(np.maximum.reduce(np.broadcast_arrays(*vals))))
    __rmul__=__mul__
    def __truediv__(self,other):
        o=iv(other)
        if not np.all(o.lo>0): raise ArithmeticError('Nonpositive divisor lower bound')
        return self*I(down(1/o.hi),up(1/o.lo))
    def square(self):
        a,b=self.lo*self.lo,self.hi*self.hi
        return I(np.where((self.lo<=0)&(self.hi>=0),0,down(np.minimum(a,b))),up(np.maximum(a,b)))
    def sqrt(self):
        if np.any(self.hi<0): raise ArithmeticError('Negative square root')
        return I(np.maximum(0,down(np.sqrt(np.maximum(0,self.lo)))),up(np.sqrt(np.maximum(0,self.hi))))
    def intersect(self,a,b):
        lo=np.maximum(self.lo,a);hi=np.minimum(self.hi,b)
        if np.any(lo>hi): raise ArithmeticError('Empty enclosure intersection')
        return I(lo,hi)

def iv(x): return x if isinstance(x,I) else I(x)
def rat(a,b=1):
    x=float(Fraction(a,b));return I(down(x),up(x))
def rational_box(a,b,scale):
    return I(down(float(Fraction(a,scale))),up(float(Fraction(b,scale))))

@lru_cache(None)
def pi_interval():
    def atan_recip(n):
        m=40
        q=sum((Fraction((-1)**j,(2*j+1)*n**(2*j+1)) for j in range(m)),Fraction(0))
        remainder=Fraction(1,(2*m+1)*n**(2*m+1))
        return q,q+remainder # m even, next term positive
    a,b=atan_recip(5);c,d=atan_recip(239)
    return I(down(float(16*a-4*d)),up(float(16*b-4*c)))

def sum_out(a, upper=False):
    v=np.ravel(a)
    if len(v)==0 or len(v)&(len(v)-1): raise ValueError('Power of two summation required')
    f=up if upper else down
    while len(v)>1: v=f(v[::2]+v[1::2])
    return float(v[0])

ANGLE_N=65536
@lru_cache(None)
def angle_table():
    # P=2 sum p_j z^j, Q=sum q_j z^j, z=(1-gamma)/2.
    # All coefficients are positive, so both are decreasing in gamma.
    z=I((1-np.arange(ANGLE_N+1)/ANGLE_N)/2)
    coeff=[];p=Fraction(1)
    for j in range(65):
        coeff.append((2*p,Fraction(2*(j*j+5*j+5),2*j+3)*p))
        p*=Fraction(2*(j+1),2*j+3)
    P=I(0);Q=I(0)
    for a,b in reversed(coeff):
        P=rat(a.numerator,a.denominator)+z*P
        Q=rat(b.numerator,b.denominator)+z*Q
    # First omitted m=65; coefficient bounds 2 and 2j+4.
    P=P+I(0.,2.**-63)
    Q=Q+I(0.,136*2.**-64)
    return P,Q

def angles(g):
    a=np.floor(g.lo*ANGLE_N).astype(np.int64)
    b=np.ceil(g.hi*ANGLE_N).astype(np.int64)
    a=np.clip(a,0,ANGLE_N);b=np.clip(b,0,ANGLE_N)
    return tuple(I(v.lo[b],v.hi[a]) for v in angle_table())

def center(slo,shi,tlo,thi,scale=1280,nmu=128,nw=None,components=(0,1,2), mapping=4):
    """Box endpoints are exact integers/scale. mu in [0,1], w=tan(phi/2)."""
    if nw is None:nw=nmu//2
    if nmu<32 or nmu%32 or nmu&(nmu-1) or nw&(nw-1):raise ValueError('Dyadic angle grid required')
    s=rational_box(slo,shi,scale);t=rational_box(tlo,thi,scale)
    A=[I(1),s.square(),(s*t).square()]
    w=I(np.arange(nw)/nw,np.arange(1,nw+1)/nw)
    den=1+w.square()
    y=(2*w/den).square().intersect(0,1)
    # cos^2 and sin^2 on [0,pi/2] are complementary and monotone.
    c=(1-y).intersect(0,1)
    wt=I(4)/pi_interval()/den
    vals={i:[] for i in components}
    for k in range(0,nmu,32):
        m=I(np.arange(k,k+32)[:,None]/nmu,np.arange(k+1,k+33)[:,None]/nmu)
        if mapping not in [1,2,4,8]:raise ValueError('mapping outside frozen choices')
        denmu=mapping-(mapping-1)*m
        jac=I(mapping)/denmu.square()
        m=(m/denmu).intersect(0,1)
        m2=m.square();left=(1-m2).intersect(0,1)
        W=[left*c,left*y,m2]
        # Use sum W=1 exactly before interval evaluation.
        C=1+(A[1]-1)*W[1]+(A[2]-1)*W[2]
        C=C.intersect(1,float(A[2].hi))
        B=1-(1-I(1)/A[1])*W[1]-(1-I(1)/A[2])*W[2]
        B=B.intersect(float((I(1)/A[2]).lo),1)
        cb=(C*B).intersect(1,np.inf).sqrt()
        gamma=(I(1)/cb).intersect(0,1)
        P,Q=angles(gamma)
        for i in components:
            other=I(0);diff=I(0)
            for j in range(3):
                if i!=j:
                    other=other+A[j]*W[j]
                    diff=diff+(A[j]-A[i])*W[j]
            v=(P*A[i]*other-Q*W[i]*diff.square())/(C.square()*cb)
            v=v*wt*jac
            vals[i].append((sum_out(v.lo),sum_out(v.hi,True)))
    out={}
    for i,rows in vals.items():
        a=np.asarray(rows)
        v=I(sum_out(a[:,0]),sum_out(a[:,1],True))/(nmu*nw)
        out[i]=(float(v.lo),float(v.hi))
    return out

