"""B7 V5.2 ASTRA3 interval floor, candidate only (independent audit pending).

Proved pointwise lemma (Judge: Astra second lemma, chat & Muse checked):
  b3=2 W w U^2/(lambda^2 |V|^3), rho=G^2/T^2,
  F>=-b3*[1-(3/2)rho]_+.
Here F is the sigma,beta,y,u integrand WITHOUT the p,t Jacobian.
All endpoint evaluations are exact rational / outward dyadic I intervals;
the cell measure is upper-bounded by Delta-sigma * Delta-beta_max *
Delta-y * Delta-u. The epsilon signs are separately enclosed.

Never import this module into the frozen V5.1 producer.
"""
from fractions import Fraction as Q
from functools import lru_cache
from v3_fixed_128 import I, iv, S


def intersect(x,lo=None,hi=None):
    lower=x.lo if lo is None else max(x.lo,I(lo).lo)
    upper=x.hi if hi is None else min(x.hi,I(hi).hi)
    if lower>upper:
        raise ValueError('ASTRA3 interval intersection empty; mathematical assumption failure')
    return I.raw(lower,upper)


def ceilq(q):
    q=Q(q)
    return -(-q.numerator//q.denominator)


def sigma(p):
    p=Q(p)
    return 2*p/(1+p*p)


def density_upper_raw(outer,cell,eps):
    """Upper 2^-128 integer bound of b3*[1-3rho/2]_+, one epsilon."""
    lam,tau,delta=(I(*b) for b in outer)
    y,p,t,_u=(I(*b) for b in cell)
    one=iv(1)
    A=(one-tau.sq())/(one+tau.sq())
    B=2*tau/(one+tau.sq())
    x=y*(iv(2)-y)
    N=one-A.sq()*x
    M=delta+(one-delta)*A.sq()*x
    s=((one-delta)*N).sqrt()
    sqs=s.sqrt()
    dv=M/(one+s)
    qx=(one-y)*A/N.sqrt()
    qz=B/N.sqrt()
    sig=2*p/(one+p.sq())
    g=(one-p.sq())/(one+p.sq())
    cb=eps*(one-t.sq())/(one+t.sq())
    sb=2*t/(one+t.sq())
    kap=2*sqs*sig/dv
    cp=one/(one+kap.sq()).sqrt()
    sp=kap*cp
    L=cp-sig*sp/sqs
    J=g*sp/sqs
    ox=L*qx-J*cb*qz
    oy=J*sb
    oz=L*qz+J*cb*qx
    xx=(one-2*sig.sq())*qx-2*sig*g*cb*qz
    xy=2*sig*g*sb
    xz=(one-2*sig.sq())*qz+2*sig*g*cb*qx
    H=cp+sqs*sig*sp
    lam2=lam.sq()
    # Exact identities |omega|=|xi|=1 imply these intersections.
    # U^2=omega_y^2+lambda^2 omega_z^2 >=0.
    V2=intersect(one-(one-lam2)*oz.sq(),lo=Q(4,25),hi=Q(1))
    U2=intersect(oy.sq()+lam2*oz.sq(),lo=Q(0),hi=Q(1))
    w2=intersect(lam2*(xx.sq()+xy.sq())+xz.sq(),lo=Q(4,25),hi=Q(1))
    G2=lam2*H.sq()
    rho=G2/(w2*V2)
    # Rigorous independent bound: w^2|V|^2<=1 and H>=cp>0.
    rho_secondary=lam2*cp.sq()
    # Another exact identity: T^2-G^2=|r cross v|^2,
    # r=(lambda*xi_x,lambda*xi_y,xi_z),
    # v=(omega_x,omega_y,lambda*omega_z).
    r0,r1,r2=lam*xx,lam*xy,xz
    v0,v1,v2=ox,oy,lam*oz
    c0=r1*v2-r2*v1
    c1=r2*v0-r0*v2
    c2=r0*v1-r1*v0
    cross2=c0.sq()+c1.sq()+c2.sq()
    rho_cross_lo=S-(cross2/(w2*V2)).hi
    rho_lo=max(0,rho.lo,rho_secondary.lo,rho_cross_lo)
    if rho_lo>S:
        raise ValueError('ASTRA3 rho lower >1; interval arithmetic or assumptions inconsistent')
    factor_up=ceilq(max(Q(0), Q(1)-Q(3,2)*Q(rho_lo,S))*S)
    if factor_up==0:
        return 0
    W=4*sig/(dv.sq()+4*s*sig.sq()).sqrt()
    b3=2*W*w2.sqrt()*U2/(lam2*V2*V2.sqrt())
    if b3.hi<0:
        raise ValueError('ASTRA3 b3 negative enclosure')
    # Additional certified global envelopes from the original b3 lemma:
    # w<=1, U^2<=|V|^2, |V|>=lambda, W<=2/sqrt(s).
    b3_envelope=2*W/(lam2*lam)   # 2W/lambda^3
    b3_hi=min(max(0,b3.hi),max(0,b3_envelope.hi),Q(275,4)*S)
    return ceilq(Q(b3_hi*factor_up,S))


@lru_cache(maxsize=128)
def delta_slabs(lo,hi):
    """Exact rational geometric partition of a universal delta box.

    Each outer delta belongs to exactly one slab; bounds are combined
    by their MINIMUM, never summed across universal parameter slabs.
    """
    lo,hi=Q(lo),Q(hi)
    if not Q(0)<lo<=hi:raise ValueError('invalid delta domain')
    ratio=hi/lo
    count=8 if ratio>Q(16) else 4 if ratio>=Q(3) else 2
    if lo==hi:return ((lo,hi),)
    edges=[lo]
    for k in range(1,count):
        target=lo**(count-k)*hi**k
        a,b=lo,hi
        for _ in range(64):
            mid=(a+b)/2
            if mid**count<target:a=mid
            else:b=mid
        edges.append((a+b)/2)
    edges.append(hi)
    assert all(a<b for a,b in zip(edges,edges[1:])), 'geometric slab empty'
    return tuple(zip(edges,edges[1:]))


def astra3_floor_on_slab(outer,cell):
    """Lower bound on both epsilon sheets' integral for one delta slab."""
    (ya,yb),(pa,pb),(ta,tb),(ua,ub)=cell
    if not all(a<b for a,b in cell):
        raise ValueError('ASTRA3 degenerate cell')
    ds=sigma(pb)-sigma(pa)
    if ds<=0:
        raise ValueError('ASTRA3 nonpositive sigma increment')
    # beta(t)=2 atan(t); derivative decreases on 0<=t<=1.
    db_max=Q(2)*(tb-ta)/(Q(1)+ta*ta)
    area=ds*db_max*(yb-ya)*(ub-ua)
    assert area>=0
    density_hi=sum(density_upper_raw(outer,cell,eps) for eps in (-1,1))
    return -ceilq(Q(density_hi)*area)


def astra3_floor_raw(outer,cell):
    """Valid uniform lower bound over ALL universal outer delta values."""
    la,tau,delta=outer
    return min(astra3_floor_on_slab((la,tau,d),cell)
               for d in delta_slabs(*delta))
