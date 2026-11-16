"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Public rational APIs; no sign decisions."""
from math import factorial
from flint import arb, fmpq as Q, ctx
from .intervals import (Config,Result,iv,ball,bounds,midpoint,radius,sym,mag,
                        tau_interval,hull)
from .jets import Jet, structure
from .density import Domain,evaluate,even_energy,axial
from .quadrature import make_mesh,integrate,range_integral

def validate(R,L):
    if not Q(0)<=R[0]<=R[1]<=Q(1): raise ValueError("radius outside [0,1]")
    if not (L==(Q(1),Q(1)) or Q(2)<=L[0]<=L[1]<=Q(5)):
        raise ValueError("lambda=1 control or lambda box in [2,5] required")

def domain_for(R,L,cfg,chart="equator"):
    return Domain(R,L,cfg.kappa if R[1]>=cfg.cap_from else Q(0),chart)

def cb_for(params,dom,mode):
    return lambda u,v,a,n:evaluate(u,v,params,dom,(a,),(n,),mode)

def deriv_integral(params,dom,mesh,mode,names,orders,even=False):
    """Mixed physical derivatives, enclosing EVERY external parameter value."""
    factor=1
    for n in orders: factor*=factorial(n)
    fn=even_energy if even else evaluate
    def cb(u,v):
        jets=(fn(u,v,params,dom,names,orders) if even else
              fn(u,v,params,dom,names,orders,mode))
        return tuple(x.coeff(*orders)*factor for x in jets)
    return range_integral(cb,mesh)

def mv_integral(boxes,dom,mesh,mode,cfg):
    p0=tuple(arb(midpoint(x)) for x in boxes)
    pt=integrate(cb_for(p0,dom,mode),mesh,cfg.order)
    corr=[arb(0) for _ in pt]
    for i,name in enumerate(("R","x","lam")):
        h=radius(boxes[i])
        if not h: continue
        d=deriv_integral(tuple(ball(x) for x in boxes),dom,mesh,mode,(name,),(1,))
        corr=[a+b*sym(h) for a,b in zip(corr,d)]
    return pt,tuple(corr)

def raw_caps(R,L,kap):
    if not kap: return (arb(0),)*3
    # Uniform upper bound; no correlation loss can UNDERestimate this.
    K=arb(((1-R[0])*kap+R[1]*kap**2/2)/2)
    ell=arb(L[1]-1/L[1]); C=arb(2*(L[1]**2-1)+2*(L[1]-1/L[1])**2)
    return (hull(0,(arb.pi()**2*K/4).upper().fmpq()),
            sym(arb.pi()*ell*K),sym(arb.pi()*C*K))

def W_cap(R,kap):
    if not kap: return arb(0)
    loss=Q(1176,5)/R[0]**2*((1-R[0])*kap+R[1]*kap**2/2)
    return sym(loss)

def merge(results,route):
    if len(results)==1: return results[0]
    n=len(results[0].balls)
    def unions(attr):
        out=list(getattr(results[0],attr))
        for r in results[1:]:
            out=[a.union(b) for a,b in zip(out,getattr(r,attr))]
        return tuple(out)
    # point_balls on a split result are unions of child centers, not evaluation
    # at one global center. The fixed-27 runner reports its center separately.
    return Result(unions("balls"),unions("point_balls"),unions("correction"),
                  unions("cap_errors"),sum(r.cells for r in results),route,
                  {"children":[r.route for r in results],
                   "point_semantics":"union of child-center enclosures"})

def angular_raw(R,beta,lam,*,angle_kind="beta",config=None):
    cfg=config or Config()
    with ctx.workprec(cfg.precision):
        R,L=iv(R),iv(lam); validate(R,L); T=tau_interval(beta,angle_kind)
        dom=domain_for(R,L,cfg)
        mesh=make_mesh(R,dom.kappa,cfg)
        pt,corr=mv_integral((R,T,L),dom,mesh,"raw",cfg)
        caps=raw_caps(R,L,dom.kappa)
        return Result(tuple(a+b+c for a,b,c in zip(pt,corr,caps)),pt,corr,caps,
                      len(mesh),"angular_raw_mean_value",
                      {"kappa":str(dom.kappa),"parameters":"R,tau,lambda"})

def center_W(R,L,cfg):
    dom=Domain((Q(0),Q(0)),L)
    mesh=make_mesh((-R[1],R[1]),Q(0),cfg)
    pt=integrate(cb_for((arb(0),arb(0),arb(midpoint(L))),dom,"center_W"),mesh,cfg.order)[0]
    corr=arb(0)
    if radius(L):
        der=deriv_integral((arb(0),arb(0),ball(L)),dom,mesh,"center_W",("lam",),(1,))[0]
        corr=der*sym(radius(L))
    remainder=arb(0)
    if R[1]:
        full=Domain((-R[1],R[1]),L)
        # M bounds E_{R R R R beta beta}; total differentiation order is six.
        d4=deriv_integral((hull(-R[1],R[1]),hull(0,1),ball(L)),
                         full,mesh,"bb",("R",),(4,))[0]
        remainder=sym(arb.pi()*arb(R[1]**2)*arb(mag(d4))/48)
    return Result((pt+corr+remainder,),(pt,),(corr+remainder,),(arb(0),),
                  len(mesh),"center_W_Taylor_R2",
                  {"remainder":str(mag(remainder)),"derivative_order":"R4 beta2",
                   "radius_effect":"analytic even Taylor remainder"})

def endpoint_W(R,X,L,cfg,chart):
    dom=domain_for(R,L,cfg,chart); mesh=make_mesh(R,dom.kappa,cfg)
    rc,xc,lc=map(midpoint,(R,X,L))
    point_dom=Domain((rc,rc),(lc,lc),dom.kappa,chart)
    sign=1 if chart=="equator" else -1
    bb0=integrate(cb_for((arb(rc),arb(0),arb(lc)),point_dom,"bb"),mesh,cfg.order)[0]
    # E_chart''(0)=4 E_beta_beta(endpoint); no singular x division.
    D0=4*bb0
    if xc:
        d4=deriv_integral((arb(rc),hull(-xc,xc),arb(lc)),point_dom,mesh,
                         "energy",("x",),(4,),even=True)[0]
        D0+=arb(xc**2/6)*d4
    def pref(r,x):
        return sign*(1+x*x)**3/(4*r*r*(1-x*x))
    P0=pref(arb(rc),arb(xc)); pt=P0*D0
    rp,xp=ball(R),ball(X); PP=pref(rp,xp)
    line=(rp,hull(-X[1],X[1]),ball(L))
    D=deriv_integral(line,dom,mesh,"energy",("x",),(2,),even=True)[0]
    corr=arb(0)
    if radius(R):
        DR=deriv_integral(line,dom,mesh,"energy",("x","R"),(2,1),even=True)[0]
        corr+=(PP*DR-2*PP/rp*D)*sym(radius(R))
    if radius(X):
        D4=deriv_integral(line,dom,mesh,"energy",("x",),(4,),even=True)[0]
        DX=xp*D4/3
        PX=PP*(6*xp/(1+xp*xp)+2*xp/(1-xp*xp))
        corr+=(PX*D+PP*DX)*sym(radius(X))
    if radius(L):
        DL=deriv_integral(line,dom,mesh,"energy",("x","lam"),(2,1),even=True)[0]
        corr+=PP*DL*sym(radius(L))
    cap=W_cap(R,dom.kappa)
    return Result((pt+corr+cap,),(pt,),(corr,),(cap,),len(mesh),
                  chart+"_even_quotient_mean_value",
                  {"kappa":str(dom.kappa),"endpoint_derivative_order":4,
                   "mixed_derivatives":"x2 R, x2 lambda",
                   "cap_charge_count":int(bool(dom.kappa))})

def angular_quotient(R,beta,lam,*,angle_kind="beta",config=None):
    cfg=config or Config()
    with ctx.workprec(cfg.precision):
        R,L=iv(R),iv(lam); validate(R,L); T=tau_interval(beta,angle_kind)
        return _angular_quotient(R,T,L,cfg)

def _angular_quotient(R,T,L,cfg):
    if L==(Q(1),Q(1)):
        return Result((arb(0),),(arb(0),),(arb(0),),(arb(0),),0,
                      "sphere_rotation_identity",{"exact_identity":True})
    if R[1]<=cfg.center_to:
        return center_W(R,L,cfg)
    if R[0]<cfg.center_to:
        return merge([center_W((R[0],cfg.center_to),L,cfg),
                      _angular_quotient((cfg.center_to,R[1]),T,L,cfg)],"radial_split")
    pieces=[]
    regions=((Q(0),Q(1,4),"equator"),(Q(1,4),Q(3,5),"middle"),
             (Q(3,5),Q(1),"pole"))
    for lo,hi,chart in regions:
        a,b=max(T[0],lo),min(T[1],hi)
        if a>b: continue
        if a==b and T[0]!=T[1]: continue
        if chart=="middle":
            dom=domain_for(R,L,cfg); mesh=make_mesh(R,dom.kappa,cfg)
            pt,corr=mv_integral((R,(a,b),L),dom,mesh,"W",cfg)
            cap=W_cap(R,dom.kappa)
            pieces.append(Result((pt[0]+corr[0]+cap,),pt,corr,(cap,),len(mesh),
                                 "middle_W_mean_value",{"kappa":str(dom.kappa),
                                 "cap_charge_count":int(bool(dom.kappa))}))
        else:
            X=(a,b) if chart=="equator" else ((1-b)/(1+b),(1-a)/(1+a))
            pieces.append(endpoint_W(R,X,L,cfg,chart))
    return merge(pieces,"angular_chart_split")

def odd_axis(u,v,params,dom,active,orders):
    a=axial(u,v,params,dom,active,orders)[0]
    opposite=Domain((-dom.R[1],-dom.R[0]),dom.lam)
    b=axial(u,v,(-params[0],params[1]),opposite,active,orders)[0]
    if "R" in active:
        ax=active.index("R")
        b=Jet(orders,[x*((-1)**idx[ax]) for idx,x in zip(structure(orders)[0],b.c)])
    return ((a-b)/2,)

def axis_g(t,lam,*,config=None):
    cfg=config or Config()
    with ctx.workprec(cfg.precision):
        T,L=iv(t),iv(lam); validate(T,L)
        if T[1]>=1: raise ValueError("axis_g requires t<1")
        if T==(Q(0),Q(0)):
            return Result((arb(0),),(arb(0),),(arb(0),),(arb(0),),0,"axis_reflection_zero")
        dom=Domain(T,L); mesh=make_mesh(T,Q(0),cfg,axis=True)
        fn=odd_axis if T[1]<=cfg.center_to else axial
        p0=(arb(midpoint(T)),arb(midpoint(L)))
        pt=integrate(lambda u,v,a,n:fn(u,v,p0,dom,(a,),(n,)),mesh,cfg.order,axis=True)[0]
        corr=arb(0)
        for name,h in (("R",radius(T)),("lam",radius(L))):
            if not h: continue
            def cb(u,v):
                return tuple(x.coeff(1) for x in fn(u,v,(ball(T),ball(L)),dom,(name,),(1,)))
            corr+=range_integral(cb,mesh,axis=True)[0]*sym(h)
        return Result((pt+corr,),(pt,),(corr,),(arb(0),),len(mesh),
                      "axis_reflected_mean_value" if fn is odd_axis else "axis_mu_1_minus_2y2_mean_value")

def coefficient_point(R,L,mesh,cfg,derivative,divisor):
    """Integral of E_R^derivative / divisor, at R=0, with high-order quadrature."""
    dom=Domain((Q(0),Q(0)),L)
    params=(arb(0),arb(0),arb(midpoint(L)))
    def cb(u,v,a,n):
        j=evaluate(u,v,params,dom,(a,"R"),(n,derivative),"energy")[0]
        fac=Q(factorial(derivative),divisor)
        return (Jet((n,),[j.coeff(k,derivative)*arb(fac) for k in range(n+1)]),)
    return integrate(cb,mesh,cfg.order)[0]

def center_phi(S,L,cfg):
    rhi=arb(S[1]).sqrt().upper().fmpq()
    mesh=make_mesh((-rhi,rhi),Q(0),cfg)
    pt=coefficient_point((Q(0),Q(0)),L,mesh,cfg,4,6)
    corr=arb(0)
    dom=Domain((Q(0),Q(0)),L)
    if radius(L):
        d=deriv_integral((arb(0),arb(0),ball(L)),dom,mesh,"energy",
                         ("R","lam"),(4,1))[0]/6
        corr+=d*sym(radius(L))
    rem=arb(0)
    if S[1]:
        full=Domain((-rhi,rhi),L)
        d6=deriv_integral((hull(-rhi,rhi),arb(0),ball(L)),full,mesh,"energy",
                          ("R",),(6,))[0]
        rem=sym(arb(S[1])*arb(mag(d6))/60)
    return Result((pt+corr+rem,),(pt,),(corr+rem,),(arb(0),),len(mesh),
                  "phi_center_H4_over_6",{"derivative_order":6,
                  "radius_effect":"analytic even Taylor remainder"})

def equatorial_phi_s(s,lam,*,config=None):
    cfg=config or Config()
    with ctx.workprec(cfg.precision):
        S,L=iv(s),iv(lam); validate(S,L)
        threshold=cfg.center_to**2
        if S[1]<=threshold: return center_phi(S,L,cfg)
        if S[0]<threshold:
            return merge([center_phi((S[0],threshold),L,cfg),
                          equatorial_phi_s((threshold,S[1]),L,config=cfg)],"phi_radial_split")
        R=(max(Q(0),arb(S[0]).sqrt().lower().fmpq()),
           min(Q(1),arb(S[1]).sqrt().upper().fmpq()))
        dom=domain_for(R,L,cfg); mesh=make_mesh(R,dom.kappa,cfg)
        pt,corr=mv_integral((R,(Q(0),Q(0)),L),dom,mesh,"phi",cfg)
        cap=arb(0)
        if dom.kappa:
            kap=arb(dom.kappa)
            # |f_x|<=9, |f_xx|<=37/sigma (lambda>=1), normalized measure.
            loss=(arb(R[1])*37*(kap/(2*arb(R[0]))).sqrt()+9*kap/2)/(2*arb(R[0])**3)
            cap=sym(loss)
        return Result((pt[0]+corr[0]+cap,),pt,corr,(cap,),len(mesh),
                      "phi_common_density_mean_value",{"kappa":str(dom.kappa),
                      "cap_charge_count":int(bool(dom.kappa))})
