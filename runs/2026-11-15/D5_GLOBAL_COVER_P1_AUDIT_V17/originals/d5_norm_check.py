"""chat DIAGNOSTIC (not evidence): end-to-end normalization of the D5 V4 / Plan B density against P1.
H_G   = (1/(2 pi lam)) sum_eps int_0^1 int_0^1 G_{l=1,eps}(z,s) ds dz   (V4 design (4.2) = Plan B (3.12), float transliteration of chat_planb_iv.G_coeff)
H_fd  = E_rho/rho by central differences of P1's E = (1/4 pi lam) int int h arccos^2 gamma dmu dphi   (no reduction used)
H_dir = (1/4 pi lam) int int F_yy (generic signed kernel)
Base point p = (r a, 0, r lam b), a=(1-tau^2)/(1+tau^2), b=2 tau/(1+tau^2)."""
import sys, numpy as np
from scipy.integrate import quad

import p1_E_lib as S   # E(), Hdir() — functions copied verbatim from ../ftqsr/sr_numeric.py (no main)
def Rf(g):
    g=min(max(g,0.0),1.0); u=1-g*g
    if u<1e-6: return 1+u/6+3*u*u/40, -2*g*(1/6+3*u/20)
    R=np.arccos(g)/np.sqrt(u); return R,(g*R-1)/u
def G(d,tau,lam,z,s,eps,ell=1.0):
    a=(1-tau*tau)/(1+tau*tau); b=2*tau/(1+tau*tau); zeta=d/ell; r=1-d
    Lb=1+z*z*ell*ell; qb=z*z*ell*8/Lb**2; Bb=z*4*(1-z*z*ell*ell)/Lb**2
    C=(1-s*s)/(1+s*s)*eps; Sn=2*s/(1+s*s)
    k=zeta-qb; X=k*a-Bb*C*b; Y=Bb*Sn; Zc=(k*b+Bb*C*a)*lam
    Z=X*X+Y*Y+Zc*Zc; U=X*X+Zc*Zc
    hb=(zeta+qb*r)*lam; A0=hb-Z*(lam*ell); xiz=(1-qb*ell)*b+Bb*C*(a*ell)
    w=np.sqrt(lam*lam+xiz*xiz*(1-lam*lam)); sZ=np.sqrt(Z); g=hb/(w*sZ)
    if Z<1e-300: return 0.0
    R,Rp=Rf(g); P=hb*hb*U; Q0=Y*Y*A0*A0
    bracket=R*P-(2*R+g*Rp)*Q0
    pref=z*(ell*64)*(1-z*z*ell*ell)/(Lb**3*(1+s*s)*w*Z*Z*sZ)
    return pref*bracket
def HG(r,tau,lam,eps_=1e-10):
    d=1-r; tot=0.0
    for e in (1,-1):
        tot+=quad(lambda z: quad(lambda s: G(d,tau,lam,z,s,e),0,1,limit=200,epsabs=eps_,epsrel=eps_)[0],0,1,limit=200,epsabs=eps_,epsrel=eps_,points=[min(d,0.999)] if d<1 else None)[0]
    return tot/(2*np.pi*lam)
def Hfd(r,tau,lam,h=1e-3):
    a=(1-tau*tau)/(1+tau*tau); b=2*tau/(1+tau*tau); rho=r*a; z=r*lam*b
    Ep=S.E(lam,rho+h,z); Em=S.E(lam,rho-h,z)
    return (Ep-Em)/(2*h)/rho
r,tau,lam=map(float,sys.argv[1:4])
a=(1-tau*tau)/(1+tau*tau); b=2*tau/(1+tau*tau)
print(f'r={r} tau={tau} lam={lam}  H_G={HG(r,tau,lam):.9f}  H_dir={S.Hdir(lam,r*a,r*lam*b):.9f}  H_fd={Hfd(r,tau,lam):.7f}',flush=True)
