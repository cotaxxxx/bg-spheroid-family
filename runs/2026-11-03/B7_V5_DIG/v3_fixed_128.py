"""Route K V3 diagnostic: dyadic outward-rounded interval evaluation.
This is NOT a certified quadrature or an independent verifier.
"""
from fractions import Fraction as Q
from math import isqrt
import time
S=1<<128

def floorq(x): return x.numerator*S//x.denominator

def ceilq(x): return -floorq(-x)

class I:
    __slots__=('lo','hi')
    def __init__(self,a,b=None,raw=False):
        if raw: self.lo,self.hi=a,b
        else:
            self.lo=floorq(Q(a));self.hi=ceilq(Q(a if b is None else b))
        if self.lo>self.hi: raise ValueError("invalid interval: lower endpoint exceeds upper endpoint")
    @classmethod
    def raw(cls,lo,hi):return cls(lo,hi,True)
    def __add__(x,y):
        y=iv(y);return I.raw(x.lo+y.lo,x.hi+y.hi)
    __radd__=__add__
    def __neg__(x):return I.raw(-x.hi,-x.lo)
    def __sub__(x,y):return x+-iv(y)
    def __rsub__(x,y):return iv(y)-x
    def __mul__(x,y):
        y=iv(y);q=[a*b for a in (x.lo,x.hi) for b in (y.lo,y.hi)]
        return I.raw(min(q)//S,-(-max(q)//S))
    __rmul__=__mul__
    def __truediv__(x,y):
        y=iv(y)
        if y.lo<=0<=y.hi: raise ZeroDivisionError("interval denominator contains zero")
        return x*I.raw((S*S)//y.hi,-((-S*S)//y.lo))
    def __rtruediv__(x,y):return iv(y)/x
    def sq(x):
        lo=0 if x.lo<=0<=x.hi else min(x.lo*x.lo,x.hi*x.hi)
        hi=max(x.lo*x.lo,x.hi*x.hi)
        return I.raw(lo//S,-(-hi//S))
    def sqrt(x):
        if x.lo<0: raise ValueError("sqrt domain failure: negative interval lower endpoint")
        a=isqrt(x.lo*S);b=isqrt(x.hi*S)
        return I.raw(a,b+(b*b<x.hi*S))
    def __repr__(x):return f'[{x.lo/S:.12g},{x.hi/S:.12g}]'

def mulq_interval(x,q):
    """Outward-round an exact rational scale of already enclosed endpoints."""
    q=Q(q)
    a=Q(x.lo)*q;b=Q(x.hi)*q
    if q<0:a,b=b,a
    return I.raw(a.numerator//a.denominator,-((-b.numerator)//b.denominator))

def iv(x):return x if isinstance(x,I) else I(x)

def calc(mode,box):
    lam=I(Q(2,5));tau=I(Q(7,8));delta=I(Q(1,25000000));v=I(1)
    p,t,u=[I(*pair) for pair in box]
    A=(1-tau.sq())/(1+tau.sq());B=2*tau/(1+tau.sq())
    N=1-A.sq()*(1-v.sq());s=((1-delta)*N).sqrt()
    qx=v*A/N.sqrt();qz=B/N.sqrt()
    sig=2*p/(1+p.sq());g=(1-p.sq())/(1+p.sq())
    cb=(1-t.sq())/(1+t.sq());sb=2*t/(1+t.sq())
    M=delta+(1-delta)*A.sq()*(1-v.sq());dv=M/(1+s)
    kap=2*s.sqrt()*sig/dv;c=(1+kap.sq()).sqrt();cp=1/c;sp=kap/c
    L=cp-sig*sp/s.sqrt();J=g*sp/s.sqrt()
    ox=L*qx-J*cb*qz;oy=J*sb;oz=L*qz+J*cb*qx
    xx=(1-2*sig.sq())*qx-2*sig*g*cb*qz
    xy=2*sig*g*sb;xz=(1-2*sig.sq())*qz+2*sig*g*cb*qx
    H=cp+s.sqrt()*sig*sp
    V2=ox.sq()+oy.sq()+lam.sq()*oz.sq();U2=oy.sq()+lam.sq()*oz.sq()
    w=(lam.sq()*(xx.sq()+xy.sq())+xz.sq()).sqrt();T=w*V2.sqrt();G=lam*H
    if mode=='producer':
        E=-s*qx*J.sq()*sb.sq()-s*J*cb*oz+(1-lam.sq())*xx*oz.sq()
        P=H.sq()*U2;R=E.sq();num=(1+u.sq())*T*(P-2*R)+(1-u.sq())*G*(P-R)
    else:
        E=oy*(xy*ox-xx*oy)+oz*(xz*ox-lam.sq()*xx*oz)
        Bh=(1+u.sq())*T+(1-u.sq())*G
        Ch=2*(1+u.sq())*T+(1-u.sq())*G
        num=Bh*H.sq()*U2-Ch*E.sq()
    Bh=(1+u.sq())*T+(1-u.sq())*G
    den=V2.sq()*Bh.sq();W=4*sig/(dv*(1+kap.sq()).sqrt())
    jac=2*(1-p.sq())/(1+p.sq()).sq()*2/(1+t.sq())
    fac=W*jac
    lower=fac.lo*num.lo//den.hi if num.lo>=0 else fac.hi*num.lo//den.lo
    upper=-(-fac.hi*num.hi//den.lo) if num.hi>=0 else -(-fac.lo*num.hi//den.hi)
    # Numerator values above are products of scaled integers, division by scaled denominator
    return I.raw(lower,upper),num,E

if __name__=='__main__':
    # Self-contained exact-rational regression, no non-distributed v2_cell.
    a,b=I(Q(1,3)),I(Q(1,6))
    assert (a+b).lo<=Q(1,2)*S<=(a+b).hi
    assert (a*b).lo<=Q(1,18)*S<=(a*b).hi
    assert (a/b).lo<=Q(2)*S<=(a/b).hi
    assert (a.sqrt().sq()).lo<=Q(1,3)*S<=(a.sqrt().sq()).hi
    q=mulq_interval(I(Q(-2),Q(3)),Q(-1,2))
    assert q.lo<=Q(-3,2)*S and q.hi>=Q(1)*S
    print('fixed-128 standalone self-test PASS')
