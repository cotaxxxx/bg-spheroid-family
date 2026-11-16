"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Equations (3)-(8), (17), (20)."""
from dataclasses import dataclass
from flint import arb, fmpq as Q
from .jets import Jet, angle, structure
from .intervals import mag, bounds
from .quadrature import cut_location, q_of_u, distance_lower_squared

@dataclass(frozen=True)
class Domain:
    R: tuple
    lam: tuple
    kappa: Q=Q(0)
    chart: str="equator"

def seed(x,name,active,orders):
    return Jet.constant(x,orders,active.index(name) if name in active else None)

def common(u,v,params,domain,active,orders):
    R,x,lam=(seed(z,n,active,orders) for z,n in zip(params,("R","x","lam")))
    U=seed(u,"u",active,orders)
    V=seed(v,"v",active,orders)
    cut=cut_location(domain.kappa)
    U=U*(1-cut)+cut
    th=V*arb.pi()
    qc=8*U**2/(1+U**2)**2
    sp=4*U*(1-U**2)/(1+U**2)**2
    ex=1-qc; ez=sp*th.cos()
    # eta_y is unnecessary: |eta|=|m|=1 is used identically.
    a=(1-x**2)/(1+x**2); b=2*x/(1+x**2)
    if domain.chart=="pole": a,b=b,a
    elif domain.chart!="equator": raise ValueError("unknown angular chart")
    rmax=max(abs(domain.R[0]),abs(domain.R[1]))
    qlo=max(domain.kappa,Q(0),qc.c[0].lower().fmpq())
    ds=distance_lower_squared(domain.R,qlo)
    sig2=((1-R)**2+2*R*qc).cap(ds,(1+rmax)**2)
    sigma=sig2.sqrt()
    mx=(a*(1-R-qc)-b*ez)/sigma
    mz=(b*(1-R-qc)+a*ez)/sigma
    mx,mz=mx.cap(-1,1),mz.cap(-1,1)
    xx=(a*ex-b*ez).cap(-1,1)
    xz=(b*ex+a*ez).cap(-1,1)
    k=(1-R+R*qc).cap(1-rmax,1+rmax)
    d=lam**2-1; e=d/lam**2
    C=(1+d*mz**2).cap(1,domain.lam[1]**2)
    B=(1-e*xz**2).cap(1/domain.lam[1]**2,1)
    gamma=(k/sigma/C.sqrt()/B.sqrt()).cap(0,1)
    gg,rr,rp=angle(gamma)
    jac=8*U*(1-U**2)/(1+U**2)**3*(1-cut)
    return R,x,lam,a,b,k,sigma,mx,mz,xx,xz,C,B,gamma,gg,rr,rp,d,e,jac

def evaluate(u,v,params,domain,active=(),orders=(0,),mode="raw"):
    R,x,lam,a,b,k,sigma,mx,mz,xx,xz,C,B,g,gg,rr,rp,d,e,jac=common(
        u,v,params,domain,active,orders)
    f=k*gg
    if mode=="energy": return (f*jac,)
    T=d*mx*mz/C-e*xx*xz/B
    Tb=d*(mx**2-mz**2)/C-2*(d*mx*mz/C)**2-e*(xx**2-xz**2)/B-2*(e*xx*xz/B)**2
    fb=2*k*g*rr*T
    fbb=2*k*g*(rr*Tb-(rr+g*rp)*T**2)
    if mode=="raw": return tuple(z*jac for z in (f,fb,fbb))
    if mode=="bb": return (fbb*jac,)
    if mode=="W": return (fb/(R**2*a*b)*jac,)
    D=sigma*C.sqrt(); w=lam*B.sqrt()
    tx=mx/C.sqrt(); tz=lam*mz/C.sqrt()
    nx=lam*xx/w; nz=xz/w
    dx=g*tx-nx; dz=g*tz-nz
    fx=-xx*gg-2*k*rr*dx/D
    fz=-xz/lam*gg-2*k*rr*dz/D
    fxx=2*w/lam/D*(g**2*rr*(1-tx**2)-(2*rr+g*rp)*dx**2)
    fzz=2*w/lam/D*(g**2*rr*(1-tz**2)-(2*rr+g*rp)*dz**2)
    if mode=="center_W": return ((lam**2*fzz-fxx)*jac,)
    if mode=="phi": return ((R*fxx-fx)/(2*R**3)*jac,)
    if mode=="physical": return tuple(z*jac for z in (f,fx,fz,fxx,fzz))
    raise ValueError("unknown density mode")

def even_energy(u,v,params,domain,active=(),orders=(0,)):
    plus=evaluate(u,v,params,domain,active,orders,"energy")[0]
    minus=evaluate(u,v,(params[0],-params[1],params[2]),domain,active,orders,"energy")[0]
    if "x" in active:
        axis=active.index("x")
        minus=Jet(orders,[v*((-1)**a[axis])
                         for a,v in zip(structure(orders)[0],minus.c)])
    return ((plus+minus)/2,)

def axial(u,v,params,domain,active=(),orders=(0,),energy=False):
    t=seed(params[0],"R",active,orders)
    lam=seed(params[1],"lam",active,orders)
    y=seed(u,"u",active,orders)
    mu=(1-2*y**2).cap(-1,1)
    st2=(1-mu**2).cap(0,1)
    A=1-t*mu
    qlo=2*max(Q(0),y.c[0].lower().fmpq())**2
    ds=distance_lower_squared(domain.R,qlo)
    rmax=max(abs(domain.R[0]),abs(domain.R[1]))
    D=(st2+lam**2*(mu-t)**2).cap(ds,domain.lam[1]**2*(1+rmax)**2).sqrt()
    w=(lam**2*st2+mu**2).cap(1,domain.lam[1]**2).sqrt()
    # D^2 >= ds > 0 and D <= lambda_max*(1+|t|_max).
    # Form the reciprocal FIRST; D**3 may straddle zero as an Arb ball.
    if ds <= 0:
        raise ArithmeticError("axis distance has no strictly positive lower bound")
    d_lower=arb(ds).sqrt().lower().fmpq()
    invD=D.reciprocal_positive(d_lower,domain.lam[1]*(1+rmax))
    invw=w.reciprocal_positive(Q(1),domain.lam[1])
    gamma=(lam*A*invw*invD).cap(0,1)
    G,rr,_=angle(gamma)
    if energy: return (2*y*A*G,)
    term=2*lam*A*rr*st2*((lam**2-1)*mu-lam**2*t)
    # Only multiplication after the positive reciprocals: no reciprocal of
    # D^3, w*D^3, or of a product of reciprocal balls.
    return (2*y*(-mu*G-term*invw*invD*invD*invD),)
