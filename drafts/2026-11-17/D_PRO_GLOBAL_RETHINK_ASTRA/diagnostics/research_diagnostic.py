#!/usr/bin/env python3
"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. New co-rotation derivation; float64 only."""
import hashlib, json
from pathlib import Path
import numpy as np

LAM=[2,206539/100000,5/2,3,4,118/25,472438/100000,472439/100000,19/4,5]
RAD=[1/8,1/2,15/16,63/64,255/256,59999/60000,1]
TAU=[0,1/16,1/4,1/2,3/4,15/16,1]

def grid(n,m):
    x,w=np.polynomial.legendre.leggauss(n)
    edges=[0.]+[2.**k for k in range(-12,1)]
    u=np.concatenate([(a+b)/2+(b-a)*x/2 for a,b in zip(edges,edges[1:])])[:,None]
    wu=np.concatenate([(b-a)*w/2 for a,b in zip(edges,edges[1:])])[:,None]
    theta=(np.arange(m)+.5)*2*np.pi/m
    q=8*u*u/(1+u*u)**2
    sp=4*u*(1-u*u)/(1+u*u)**2
    weight=wu*16*u*(1-u*u)/(1+u*u)**3/(2*m)
    return q,sp*np.cos(theta),sp*np.sin(theta),weight

def angle(c):
    c=np.clip(c,0.,1.)
    t=1-c
    coeff=[1.]
    for n in range(32): coeff.append(coeff[-1]*(n+1)/(2*n+3))
    near=t<.125
    R=np.empty_like(c); Rp=np.empty_like(c)
    R[near]=np.polynomial.polynomial.polyval(t[near],coeff)
    Rp[near]=-np.polynomial.polynomial.polyval(t[near],[n*coeff[n] for n in range(1,len(coeff))])
    R[~near]=np.arccos(c[~near])/np.sqrt(1-c[~near]**2)
    Rp[~near]=(c[~near]*R[~near]-1)/(1-c[~near]**2)
    return np.arccos(c)**2,R,Rp

def evaluate(lam,rad,beta,quad):
    q,ey,ez,weight=quad
    a,b=np.cos(beta),np.sin(beta)
    ex=1-q; vx=1-rad-q
    sigma=np.sqrt((1-rad)**2+2*rad*q)
    xx=a*ex-b*ez; zz=b*ex+a*ez
    mx=(a*vx-b*ez)/sigma; mz=(b*vx+a*ez)/sigma
    d=lam*lam-1; e=d/(lam*lam)
    C=1+d*mz*mz; B=1-e*zz*zz
    k=1-rad+rad*q
    c=k/(sigma*np.sqrt(C*B))
    if np.any(c < -1e-12) or np.any(c > 1+1e-12): raise ArithmeticError('cosine geometry')
    c=np.clip(c,0.,1.)
    G,A,Ap=angle(c)
    T=d*mx*mz/C-e*xx*zz/B
    Tp=d*(mx*mx-mz*mz)/C-2*(d*mx*mz/C)**2-e*(xx*xx-zz*zz)/B-2*(e*xx*zz/B)**2
    energy=np.sum(weight*k*G)
    eb=np.sum(weight*2*k*c*A*T)
    ebb=np.sum(weight*2*k*c*(A*Tp-(A+c*Ap)*T*T))
    D=sigma*np.sqrt(C); w=lam*np.sqrt(B); h=lam*k
    tx=mx/np.sqrt(C); tz=lam*mz/np.sqrt(C)
    nx=lam*xx/w; nz=zz/w
    dx=c*tx-nx; dz=c*tz-nz
    fx=-lam*xx*G-2*h*A*dx/D
    fz=-zz*G-2*h*A*dz/D
    fxx=2*w/D*(c*c*A*(1-tx*tx)-(2*A+c*Ap)*dx*dx)
    fzz=2*w/D*(c*c*A*(1-tz*tz)-(2*A+c*Ap)*dz*dz)
    return np.array([energy,eb,ebb,np.sum(weight*fx)/lam,np.sum(weight*fz)/lam,np.sum(weight*fxx)/lam,np.sum(weight*fzz)/lam])

def main():
    root=Path(__file__).resolve().parent
    pins=json.loads((root/'PRE_RUN_SHA256.json').read_text())
    for name,digest in pins.items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest: raise RuntimeError('pre-run seal mismatch')
    answers={k:True for k in ['Q1_angular_W_positive','Q2_axis_Ez_positive','Q3_equatorial_quotient_decreasing','Q4_axis_Ezz_positive','Q5_gradient_identity','Q6_energy_finite_difference_identity','Q7_center_angular_coefficient_positive']}
    for n,m in [(12,96),(24,192)]:
        quad=grid(n,m)
        for lam in LAM:
            v=evaluate(lam,0,0,quad)
            answers['Q7_center_angular_coefficient_positive'] &= bool(np.isfinite(v).all() and lam*lam*v[6]-v[5]>0)
            for rad in RAD:
                for tau in TAU:
                    beta=2*np.arctan(tau)
                    v=evaluate(lam,rad,beta,quad)
                    en,eb,ebb,ex,ez,exx,ezz=v
                    W=ebb/rad**2 if tau==0 else -ebb/rad**2 if tau==1 else eb/(rad**2*np.sin(beta)*np.cos(beta))
                    answers['Q1_angular_W_positive'] &= bool(np.isfinite(v).all() and W>0)
                    if tau==1:
                        answers['Q2_axis_Ez_positive'] &= bool(ez>0)
                        answers['Q4_axis_Ezz_positive'] &= bool(ezz>0)
                    if tau==0: answers['Q3_equatorial_quotient_decreasing'] &= bool(rad*exx-ex<0)
                    if tau not in [0,1]:
                        residual=eb-(-rad*np.sin(beta)*ex+lam*rad*np.cos(beta)*ez)
                        answers['Q5_gradient_identity'] &= bool(abs(residual)<2e-5)
        for lam in [2,7/2,5]:
            for rad in [1/8,1/2,7/8]:
                for tau in [1/8,1/2,7/8]:
                    beta=2*np.arctan(tau); step=.001
                    v=evaluate(lam,rad,beta,quad)
                    ep=evaluate(lam,rad,beta+step,quad)[0]; em=evaluate(lam,rad,beta-step,quad)[0]
                    answers['Q6_energy_finite_difference_identity'] &= bool(abs((ep-em)/(2*step)-v[1])<2e-5 and abs((ep-2*v[0]+em)/step**2-v[2])<2e-4)
    out={'classification':'DIAGNOSTIC_ONLY / NOT_EVIDENCE','answers':{k:bool(v) for k,v in answers.items()}}
    (root/'OUTPUT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
