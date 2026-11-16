"""DIAGNOSTIC_ONLY / NOT_EVIDENCE.
Independent lab-coordinate reference for tests. Upstream W1 E is unmodified.
The added Ex adapter is NEW, not an upstream Ex API or a clean-room checker.
"""
from flint import arb, fmpq as Q
from ..vendor import kernel_w1 as old
from ..jets import Jet
from ..quadrature import Cell,integrate

def lab_E(rho,z,lam,rmax,grid=(64,128)):
    return old.integrate(rho,z,lam,rmax,order=6,cells=grid).balls[0]

def lab_gradients(rho,z,lam,rmax,grid=(32,64)):
    def density(u,v,active,n):
        U=old.Jet.constant(u,n,int(active=="u"))*arb.pi()
        V=old.Jet.constant(v,n,int(active=="v"))*arb.pi()
        mu,st=U.cos(),U.sin()
        xx,yy=st*V.cos(),st*V.sin()
        dx=xx-rho; dz=lam*mu-z
        D=(dx*dx+yy*yy+dz*dz).cap((1-rmax)**2,(5*(1+rmax))**2).sqrt()
        w=(lam*lam*(1-mu*mu)+mu*mu).cap(1,25).sqrt()
        h=lam*(1-rho*xx)-z*mu
        gamma=(h/w/D).cap(0,1)
        G,rr,_=old.angle(gamma)
        fx=-lam*xx*G-2*h*rr*(gamma*dx/D-lam*xx/w)/D
        fz=-mu*G-2*h*rr*(gamma*dz/D-mu/w)/D
        scale=st*arb.pi()/(2*lam)
        return tuple(Jet((n,),(x*scale).c) for x in (fx,fz))
    nu,nv=grid
    mesh=tuple(Cell((Q(i,nu),Q(i+1,nu)),(Q(j,nv),Q(j+1,nv)))
               for i in range(nu) for j in range(nv))
    return integrate(density,mesh,6)

def sphere_series(t,N=64):
    """Exact rational coefficient series; independent of co-rotation density.
    Returns f(t), g(t), Phi_s(t^2), with strictly negative tail bounds.
    """
    t=Q(t); s=t*t
    if not 0<=t<1: raise ValueError("sphere series needs 0<=t<1")
    E=arb(0); g=arb(0); phi=arb(0)
    for j in range(1,N+1):
        c=Q(2,3) if j==1 else Q(2*(7-6*j),(2*j-3)**2*(2*j-1)**2*(2*j+1))
        E+=arb(c*s**j)
        g+=arb(2*j*c*t**(2*j-1))
        if j>=2: phi+=arb(2*j*(j-1)*c*s**(j-2))
    from ..intervals import hull
    E+=hull(-Q(6,(N+1)**4)*s**(N+1)/(1-s),0)
    g+=hull(-Q(12,(N+1)**3)*t**(2*N+1)/(1-s),0)
    phi+=hull(-Q(12,(N+1)**2)*s**(N-1)/(1-s),0)
    return E,g,phi
