"""V6-B eta producer diagnostic, not an integral certificate."""
from fractions import Fraction as Q
from v3_fixed_128 import I,iv,S,mulq_interval
from v6_b_ad2_128 import D2,intersect_value

def _kernel_form(outer,inner,eps,direction=None,form="eta"):
    """direction: None, ('outer',0..2), or ('inner',0..3)."""
    if direction is not None and (not isinstance(direction,tuple) or len(direction)!=2 or direction[0] not in ('outer','inner') or not isinstance(direction[1],int) or isinstance(direction[1],bool) or not 0<=direction[1]<(3 if direction[0]=='outer' else 4)):
        raise ValueError('invalid AD direction')
    lam,tau,delta=[D2.variable(I(*b)) if direction==('outer',i) else D2(I(*b)) for i,b in enumerate(outer)]
    coords=[D2.variable(I(*b)) if direction==('inner',i) else D2(I(*b)) for i,b in enumerate(inner)]
    y,p,t,u=coords
    A=(1-tau.sq())/(1+tau.sq()); B=2*tau/(1+tau.sq())
    x=y*(2-y); aa=A.sq(); N=1-aa*x; M=delta+(1-delta)*aa*x
    s=((1-delta)*N).sqrt(); qx=(1-y)*A/N.sqrt();qz=B/N.sqrt()
    sig=2*p/(1+p.sq());g=(1-p.sq())/(1+p.sq())
    cb=eps*(1-t.sq())/(1+t.sq());sb=2*t/(1+t.sq())
    dv=M/(1+s)
    if form == "eta":
        eta=dv/(2*s.sqrt()*sig)
        root=(1+eta.sq()).sqrt();cp=eta/root;sp=1/root
        W=2/(s.sqrt()*root)
    elif form == "kappa":
        kap=2*s.sqrt()*sig/dv
        root=(1+kap.sq()).sqrt();cp=1/root;sp=kap/root
        W=4*sig/(dv.sq()+4*s*sig.sq()).sqrt()
    else: raise ValueError("unknown form")
    L=cp-sig*sp/s.sqrt();J=g*sp/s.sqrt()
    ox=L*qx-J*cb*qz;oy=J*sb;oz=L*qz+J*cb*qx
    xx=(1-2*sig.sq())*qx-2*sig*g*cb*qz
    xy=2*sig*g*sb;xz=(1-2*sig.sq())*qz+2*sig*g*cb*qx
    H=cp+s.sqrt()*sig*sp
    lam2=lam.sq()
    V2=intersect_value(1-(1-lam2)*oz.sq(),lower=Q(4,25),upper=1)
    U2=V2-ox.sq()
    w2=intersect_value(lam2*(xx.sq()+xy.sq())+xz.sq(),lower=Q(4,25),upper=1)
    w=w2.sqrt();T=w*V2.sqrt();G=lam*H
    E=-s*qx*J.sq()*sb.sq()-s*J*cb*oz+(1-lam2)*xx*oz.sq()
    P=H.sq()*U2;R=E.sq()
    Bh=intersect_value((1+u.sq())*T+(1-u.sq())*G,lower=Q(4,25))
    num=(1+u.sq())*T*(P-2*R)+(1-u.sq())*G*(P-R)
    jac=2*(1-p.sq())/(1+p.sq()).sq()*2/(1+t.sq())
    return W*jac*num/(V2.sq()*Bh.sq())

def _intersection(a,b):
    from v6_b_ad2_128 import D2
    def meet(x,y):
        lo=max(x.lo,y.lo);hi=min(x.hi,y.hi)
        if lo>hi:raise ValueError("eta/kappa enclosure intersection EMPTY")
        return I.raw(lo,hi)
    return D2(meet(a.v,b.v),meet(a.d1,b.d1),meet(a.d2,b.d2))

def kernel(outer,inner,eps,direction=None):
    # Decision uses value-only enclosure, with no AD differentiation.
    tau=I(*outer[1]);delta=I(*outer[2]);y=I(*inner[0]);p=I(*inner[1])
    A=(iv(1)-tau.sq())/(iv(1)+tau.sq());x=y*(iv(2)-y)
    N=iv(1)-A.sq()*x;M=delta+(iv(1)-delta)*A.sq()*x
    s=((iv(1)-delta)*N).sqrt();dv=M/(iv(1)+s)
    sig=iv(2)*p/(iv(1)+p.sq())
    kap=iv(2)*s.sqrt()*sig/dv
    if kap.hi<=S:return _kernel_form(outer,inner,eps,direction,"kappa")
    if kap.lo>=S:return _kernel_form(outer,inner,eps,direction,"eta")
    return _intersection(_kernel_form(outer,inner,eps,direction,"kappa"),
                         _kernel_form(outer,inner,eps,direction,"eta"))

def report(outer,cell):
    mid=[((a+b)/2,(a+b)/2) for a,b in cell]
    main=sum((kernel(outer,mid,e).v for e in (1,-1)),iv(0))
    volume=Q(1)
    for a,b in cell:volume*=b-a
    rem={}
    for i,name in enumerate('yptu'):
        h=sum((kernel(outer,cell,e,('inner',i)).d2 for e in (1,-1)),iv(0))
        width=cell[i][1]-cell[i][0]
        rem[name]=mulq_interval(h,volume*width*width/Q(24))
    main_scaled=mulq_interval(main,volume)
    total=main_scaled+sum(rem.values(),iv(0))
    return main,main_scaled,rem,total


def centered_main(outer,cell):
    mid=[((a+b)/2,(a+b)/2) for a,b in cell]
    center=[((a+b)/2,(a+b)/2) for a,b in outer]
    point=sum((kernel(center,mid,e).v for e in (1,-1)),iv(0))
    error=iv(0)
    for i in range(3):
        deriv=sum((kernel(outer,mid,e,('outer',i)).d1 for e in (1,-1)),iv(0))
        radius=(outer[i][1]-outer[i][0])/2
        error=error+deriv*I(-radius,radius)
    centered=point+error
    direct=sum((kernel(outer,mid,e).v for e in (1,-1)),iv(0))
    lo,hi=max(centered.lo,direct.lo),min(centered.hi,direct.hi)
    if lo>hi:raise ValueError('centered_main: empty intersection of two interval enclosures')
    return I.raw(lo,hi)

def cell_bound(outer,cell):
    main=centered_main(outer,cell)
    volume=Q(1)
    for a,b in cell:volume*=b-a
    rem={}
    for i,name in enumerate('yptu'):
        h=sum((kernel(outer,cell,e,('inner',i)).d2 for e in (1,-1)),iv(0))
        width=cell[i][1]-cell[i][0]
        rem[name]=mulq_interval(h,volume*width*width/Q(24))
    main_scaled=mulq_interval(main,volume)
    total=main_scaled+sum(rem.values(),iv(0))
    return main_scaled,rem,total
