"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Independent floating comparison with the original energy."""
import json
from time import perf_counter
import numpy as np
from numpy.polynomial.legendre import leggauss

STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
pts=[(5,0,0),(5,1/4,1/4),(5,31/32,0),(5,0,15/16),
     (6,9/16,3/8),(8,1/4,1/2),(10,1/4,3/4),(32,1/2,1/4)]


def quadrature(end,extras):
    cuts=sorted(set([end*i/16 for i in range(17)]+[x for x in extras if 0<x<end]))
    x,w=leggauss(20)
    nodes=np.concatenate([(a+b+(b-a)*x)/2 for a,b in zip(cuts,cuts[1:])])
    weights=np.concatenate([(b-a)*w/2 for a,b in zip(cuts,cuts[1:])])
    return nodes,weights


def test(lam,r,z):
    pi=np.pi
    contact=np.arccos(z)
    cuts=[contact+s*2.**(-i) for i in range(8) for s in (-1,1)]+[contact]
    theta,tw=quadrature(pi,cuts)
    phi,pw=quadrature(pi,[pi*2.**(-i) for i in range(1,9)])
    mu=np.cos(theta)[:,None];s=np.sin(theta)[:,None]
    x=s*np.cos(phi); y=s*np.sin(phi)
    eps=1./lam
    weights=tw[:,None]*s*pw[None,:]/(2*pi)

    def energy(radius):
        vx,vy,vz=x-radius,y,lam*(mu-z)
        nx,ny,nz=x,y,eps*mu
        dc=np.sqrt((vy*nz-vz*ny)**2+(vz*nx-vx*nz)**2+(vx*ny-vy*nx)**2)
        k=1-radius*x-z*mu
        return np.sum(weights*k*np.arctan2(dc,k)**2)

    step=1/1024
    e0,e1,e2=(energy(np.hypot(r,j*step)) for j in (0,1,2))
    fd=(-2*e2+32*e1-30*e0)/(12*step**2)
    # Angular average after pulling the already differentiated kernel to chords.
    theta,tw=quadrature(pi/2,[])
    m=np.cos(theta)[:,None];s=np.sin(theta)[:,None]
    horiz=s*np.cos(phi);ey=s*np.sin(phi)
    weights=tw[:,None]*s*pw[None,:]/pi
    v=r*horiz+z*m
    d=np.sqrt(1-r*r-z*z+v*v)
    C=1+(lam**2-1)*m**2
    quad,w=leggauss(24)
    result=0.
    for side in (-1,1):
        length=d-side*v
        az=z+side*length*m
        B=1-(1-eps**2)*az**2
        gamma=d/np.sqrt(B*C)
        fp=np.zeros_like(gamma);q=np.zeros_like(gamma)
        for ti,wi in zip((1+quad)/2,w/2):
            A,b=1+ti*ti,1-ti*ti
            fp+=4*wi/(A+b*gamma)
            q+=4*wi*(2*A+b*gamma)/(A+b*gamma)**2
        val=length/(d*np.sqrt(B*C))*(fp*d**2/C*(1-ey**2/C)
                                     -q*ey**2*(length-d/C)**2)
        result+=np.sum(weights*val)/2
    return dict(lam=lam,rho=r,z=z,H_energy=float(fd),H_chord=float(result),
                difference=float(abs(fd-result)),matched=bool(abs(fd-result)<2e-6))


if __name__=="__main__":
    start=perf_counter()
    print(json.dumps(dict(status=STATUS,numpy=np.__version__)),flush=True)
    results=[test(*args) for args in pts]
    for r in results: print(json.dumps(r),flush=True)
    print(json.dumps(dict(matched=sum(r["matched"] for r in results),count=len(results),
                          wall_seconds=round(perf_counter()-start,3))))
    if not all(r["matched"] for r in results): raise SystemExit(1)
