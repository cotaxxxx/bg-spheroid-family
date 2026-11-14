"""chat DIAGNOSTIC (not evidence): end-to-end numerical check of the normalization chain on the face.
H_fd   = E_rho/rho by one-sided finite differences of E = (1/4pi lam) int int h arccos^2(gamma) dmu dphi  (P1 §1 definition)
H_dir  = (1/4pi lam) int int F_yy  (generic signed kernel, R from arccos)
H_fold = int dmu int domega int dt [P_+ + P_-]  (V3 target P = gamma F/(K A^2), V3 physical map)
Interior check: E_yy by central differences vs (1/4pi lam) int int F_yy at an interior point."""
import numpy as np, sys
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss
TL,TW=leggauss(24); TL=(TL+1)/2; TW=TW/2
def Rf(g):
    g=min(g,1.0)
    u=1-g*g
    if u<1e-6: return 1+u/6+3*u*u/40, -2*g*(1/6+3*u/20)
    R=np.arccos(g)/np.sqrt(u); return R,(g*R-1)/u
def geo(lam,rho,z,mu,phi):
    a=np.sqrt(max(1-mu*mu,0)); X=np.array([a*np.cos(phi),a*np.sin(phi),lam*mu]); p=np.array([rho,0,z])
    N=np.array([lam*a*np.cos(phi),lam*a*np.sin(phi),mu]); w=np.linalg.norm(N); Y=X-p; D=np.linalg.norm(Y)
    return Y,D,N,w
def Edens(lam,rho,z,mu,phi):
    Y,D,N,w=geo(lam,rho,z,mu,phi)
    if D<1e-15: return 0.0
    h=N@Y; g=min(max(h/(w*D),-1),1); return h*np.arccos(g)**2
def Fyy(lam,rho,z,mu,phi):
    Y,D,N,w=geo(lam,rho,z,mu,phi)
    if D<1e-15: return 0.0
    h=N@Y; g=h/(w*D); T=Y[1]/D; av=N[1]/w; e=g*T-av; R,Rp=Rf(g)
    return 2*w/D*(R*(g*g*(1-T*T)-2*e*e)-g*Rp*e*e)
def I2(f,mubreak,eps=1e-11):
    inner=lambda mu: 2*quad(lambda ph: f(mu,ph),0,np.pi,limit=200,epsabs=eps,epsrel=eps)[0]
    pts=[m for m in mubreak if -1<m<1]
    return quad(inner,-1,1,points=pts or None,limit=200,epsabs=eps,epsrel=eps)[0]
def E(lam,rho,z): return I2(lambda mu,ph: Edens(lam,rho,z,mu,ph),[z/lam])/(4*np.pi*lam)
def Hdir(lam,rho,z): return I2(lambda mu,ph: Fyy(lam,rho,z,mu,ph),[z/lam])/(4*np.pi*lam)
def Pt(lam,R,Z,mu,s,eps):
    a=np.sqrt(max(1-mu*mu,0)); X=a*eps*s-R; Y2=(1-mu*mu)*(1-s*s); Dl=mu-Z
    S=X*X+Y2+Dl*Dl
    if S<1e-28: return 0.0
    P2=X*X+Y2+lam*lam*Dl*Dl; K=P2/S; n=Y2/P2; w=np.sqrt(lam*lam+(1-lam*lam)*mu*mu); g=lam*np.sqrt(S)/(2*w*np.sqrt(K))
    t=TL; c=1-t*t; A=1+t*t+c*g; F=A*(1-n)-(2*A-g*c)*n*(1-2*K)**2
    return float(np.sum(TW*g*F/(K*A*A)))
def Hfold(lam,tau,eps_=1e-10):
    R=(1-tau*tau)/(1+tau*tau); Z=2*tau/(1+tau*tau)
    inner=lambda mu: quad(lambda th: Pt(lam,R,Z,mu,np.sin(th),1)+Pt(lam,R,Z,mu,np.sin(th),-1),0,np.pi/2,limit=200,epsabs=eps_,epsrel=eps_)[0]/np.pi
    return quad(inner,-1,1,points=[Z] if Z<1 else None,limit=200,epsabs=eps_,epsrel=eps_)[0]
def Hfd(lam,tau,d=2e-3):
    R=(1-tau*tau)/(1+tau*tau); z=lam*2*tau/(1+tau*tau)
    e=[E(lam,R-k*d,z) for k in range(4)]
    # third-order one-sided derivative
    Er=(11*e[0]-18*e[1]+9*e[2]-2*e[3])/(6*d)
    return Er/R
out=[]
mode=sys.argv[1]
if mode=='interior':
    lam=0.43; rho=0.3; z=0.2; d=1e-3
    Eyy=(E(lam,rho,0,z) if False else None)
    # E at (rho, y, z): use rotational invariance -> E depends on sqrt(rho^2+y^2)
    Ey=lambda y: E(lam,np.hypot(rho,y),z)
    Eyy=(Ey(d)-2*Ey(0)+Ey(-d))/(d*d)
    print('interior E_yy(fd)=',Eyy,' (1/4pi lam)int F_yy=',Hdir(lam,rho,z))
else:
    lam=float(sys.argv[2]); tau=float(sys.argv[3])
    R=(1-tau*tau)/(1+tau*tau); z=lam*2*tau/(1+tau*tau)
    hf=Hfold(lam,tau); hd=Hdir(lam,R,z)
    line=f'lam={lam} tau={tau} H_fold={hf:.9f} H_dir={hd:.9f}'
    if mode=='full': line+=f' H_fd={Hfd(lam,tau):.7f}'
    print(line,flush=True)
