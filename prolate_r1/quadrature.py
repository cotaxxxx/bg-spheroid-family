"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Geometry-only mesh, even Taylor integration."""
from dataclasses import dataclass
from flint import arb, fmpq as Q
from .intervals import ball, bounds, midpoint

def q_of_u(u):
    return 8*u*u/(1+u*u)**2

def cut_location(kappa):
    k=arb(kappa)/2
    return k.sqrt()/(1+(1-k).sqrt())

def distance_lower_squared(R,qlo):
    if R[0]<0:
        return (1-max(abs(R[0]),abs(R[1])))**2
    star=min(R[1],max(R[0],1-qlo))
    return (1-star)**2+2*star*qlo

@dataclass(frozen=True)
class Cell:
    u: tuple
    v: tuple
    depth: int=0

def make_mesh(R,kappa,cfg,axis=False):
    cut=cut_location(kappa)
    cv=1 if axis else cfg.base_v
    pending=[Cell((Q(i,cfg.base_u),Q(i+1,cfg.base_u)),
                  (Q(j,cv),Q(j+1,cv)))
             for i in range(cfg.base_u) for j in range(cv)]
    out=[]
    while pending:
        c=pending.pop()
        du=c.u[1]-c.u[0]; dv=c.v[1]-c.v[0]
        if axis:
            qlo=2*c.u[0]**2
            a,b=4*du,Q(0)
        else:
            lo=max(Q(0),(cut+(1-cut)*arb(c.u[0])).lower().fmpq())
            hi=min(Q(1),(cut+(1-cut)*arb(c.u[1])).upper().fmpq())
            qlo=max(kappa,q_of_u(lo))
            a=4*(hi-lo)
            spmax=min(Q(1),4*hi,4*(1-lo))
            b=Q(22,7)*spmax*dv
        ds=distance_lower_squared(R,qlo)
        if ds>0 and (a+b)**2 <= cfg.distance_ratio**2*ds:
            out.append(c)
            continue
        if c.depth>=cfg.max_depth or len(out)+len(pending)+2>cfg.max_cells:
            raise ArithmeticError("OPEN: geometry mesh resource limit; no enclosure returned")
        if a>=b or axis:
            mid=midpoint(c.u)
            pending.extend((Cell((c.u[0],mid),c.v,c.depth+1),
                            Cell((mid,c.u[1]),c.v,c.depth+1)))
        else:
            mid=midpoint(c.v)
            pending.extend((Cell(c.u,(c.v[0],mid),c.depth+1),
                            Cell(c.u,(mid,c.v[1]),c.depth+1)))
    return tuple(out)

def moment(h,k):
    return arb(h**k/Q(2**k*(k+1)))

def integrate(callback,mesh,order,axis=False):
    """callback(u_ball,v_ball,active,order) -> tuple of univariate Jets."""
    total=None
    for c in mesh:
        ui,vi=ball(c.u),ball(c.v)
        um,vm=arb(midpoint(c.u)),arb(midpoint(c.v))
        hu,hv=c.u[1]-c.u[0],c.v[1]-c.v[0]
        if axis:
            mid=callback(um,vm,"u",order)
            full=callback(ui,vm,"u",order)
            vals=[]
            for x,y in zip(mid,full):
                val=sum((moment(hu,k)*x.coeff(k) for k in range(0,order,2)),arb(0))
                val+=moment(hu,order)*y.coeff(order)
                vals.append(val.intersection(y.c[0])*arb(hu))
        else:
            mid=callback(um,vm,"v",order)
            vf=callback(um,vi,"v",order)
            uf=callback(ui,vi,"u",order)
            ul=callback(um,vi,"u",order) if order>2 else None
            vals=[]
            for j in range(len(mid)):
                val=sum((moment(hv,k)*mid[j].coeff(k) for k in range(0,order,2)),arb(0))
                val+=moment(hv,order)*vf[j].coeff(order)
                for k in range(2,order,2):
                    val+=moment(hu,k)*ul[j].coeff(k)
                val+=moment(hu,order)*uf[j].coeff(order)
                vals.append(val.intersection(uf[j].c[0])*arb(hu*hv))
        if total is None: total=[arb(0) for _ in vals]
        total=[a+b for a,b in zip(total,vals)]
    if total is None or not all(x.is_finite() for x in total):
        raise ArithmeticError("non-finite/empty quadrature")
    return tuple(total)

def range_integral(callback,mesh,axis=False):
    total=None
    for c in mesh:
        vals=callback(ball(c.u),ball(c.v))
        area=(c.u[1]-c.u[0])*(1 if axis else c.v[1]-c.v[0])
        if total is None: total=[arb(0) for _ in vals]
        total=[a+arb(area)*b for a,b in zip(total,vals)]
    if total is None or not all(x.is_finite() for x in total):
        raise ArithmeticError("non-finite derivative enclosure")
    return tuple(total)
