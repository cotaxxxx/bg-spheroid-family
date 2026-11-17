"""DIAGNOSTIC_ONLY / NOT_EVIDENCE.
R3: finite fixed parameter cover, point Taylor quadrature plus mean values.
No change to the center quotient or its remainder constants.
"""
from functools import lru_cache
from math import factorial, prod
from flint import arb, fmpq as Q
from .intervals import ball, midpoint, radius, sym, mag
from .jets import Jet
from .density import Domain, evaluate
from .quadrature import make_mesh, integrate, range_integral

def partition(lo,hi,count):
    if lo==hi:
        return ((lo,hi),)
    h=(hi-lo)/count
    return tuple((lo+i*h,lo+(i+1)*h) for i in range(count))

def derivative_point(boxes,dom,mesh,mode,nr,order):
    params=tuple(arb(midpoint(x)) for x in boxes)
    fac=factorial(nr)
    def cb(u,v,active,n):
        j=evaluate(u,v,params,dom,(active,"R"),(n,nr),mode)[0]
        return (Jet((n,),[j.coeff(k,nr)*fac for k in range(n+1)]),)
    return integrate(cb,mesh,order)[0]

def derivative_range(boxes,dom,mesh,mode,names,orders):
    params=tuple(ball(x) for x in boxes)
    fac=prod(factorial(n) for n in orders)
    def cb(u,v):
        j=evaluate(u,v,params,dom,names,orders,mode)[0]
        return (j.coeff(*orders)*fac,)
    return range_integral(cb,mesh)[0]

def derivative_mean_value(boxes,dom,mesh,mode,nr,order):
    """Enclose the INTEGRAL of the nr-th radial derivative for every p in B."""
    point=derivative_point(boxes,dom,mesh,mode,nr,order)
    correction=arb(0)
    for i,name in enumerate(("R","x","lam")):
        h=radius(boxes[i])
        if not h:
            continue
        if name=="R":
            names,orders=("R",),(nr+1,)
        else:
            names,orders=("R",name),(nr,1)
        gradient=derivative_range(boxes,dom,mesh,mode,names,orders)
        correction+=gradient*sym(h)
    return point+correction

@lru_cache(maxsize=32)
def center_max_bound(rhi,L,cfg,kind):
    """Maximum of rigorous subbox upper bounds; precision is in cfg/cache key."""
    if kind=="W":
        nr,mode=4,"bb"
        angles=partition(Q(0),Q(1),cfg.center_tau_parts)
    elif kind=="phi":
        nr,mode=6,"energy"
        angles=((Q(0),Q(0)),)
    else:
        raise ValueError("unknown center bound")
    radial=partition(-rhi,rhi,cfg.center_radial_parts)
    maximum=Q(0); cells=0; boxes=0
    for R in radial:
        dom=Domain(R,L)
        # Geometry is uniform in all beta: B_lower=lambda_max^(-2).
        mesh=make_mesh(R,Q(0),cfg,lam=L)
        for T in angles:
            enclosed=derivative_mean_value((R,T,L),dom,mesh,mode,nr,
                                           cfg.center_bound_order)
            if not enclosed.is_finite():
                raise ArithmeticError("non-finite R3 center subbox")
            maximum=max(maximum,mag(enclosed))
            cells+=len(mesh); boxes+=1
    return maximum,cells,boxes
