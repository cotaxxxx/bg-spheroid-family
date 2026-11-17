# Method D full source and numeric log bundle

**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

This file concatenates source and existing outputs as text. Copy each fenced block to the indicated path to reproduce. The separate ZIP preserves original standalone files and SHA256SUMS.

## r4_azimuth_pilot.py

```python
"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Non-rigorous numerical azimuth-cancellation pilot.
R4 (1),(12)-(14). Gauss-Legendre quadrature, finite-difference derivatives.
Not an Arb interval calculation. No sign certification, no W proof.
"""
import argparse, json, time
import numpy as np
from numpy.polynomial.legendre import leggauss

def gauss01(n):
    z,wt=leggauss(n)
    return (z+1)/2,wt/2

def r4_kernel(R,tau,lam,h,theta,w):
    h=h[:,None,None]; th=theta[None,:,None]; w=w[None,None,:]
    t=4*tau**2/(1+tau**2)**2
    sigma=(1-R)**2+2*R*(1-h)
    k=1-R*h
    a0=k*k/sigma
    d=lam*lam-1; e=d/(lam*lam)
    v2=(1-h*h)*np.cos(th)**2
    y2=(1-h*h)*np.sin(th)**2
    aa=(h-R)**2/sigma
    bb=v2/sigma
    X=(h*(h-R)-v2)**2/sigma
    ycore=h-t*(2*h-R)
    Y=v2*ycore*ycore/sigma
    Yt=-2*v2*ycore*(2*h-R)/sigma
    Bstar=1/(lam*lam)+e*y2
    U=(1-t)*h*h+t*v2
    C0=1+d*((1-t)*bb+t*aa)
    P=Bstar*C0+e*U+d*e*(t*(1-t)*X+Y)
    Pt=Bstar*d*(aa-bb)+e*(v2-h*h)+d*e*((1-2*t)*X+Yt)
    vc=(1-t)*bb-t*aa
    vb=(1-t)*h*h-t*v2
    DC=1+2*d*((1-t)*bb+t*aa)+d*d*vc*vc
    DB=Bstar*Bstar+2*Bstar*e*U+e*e*vb*vb
    DCt=2*d*(aa-bb)-2*d*d*vc*(bb+aa)
    DBt=2*Bstar*e*(v2-h*h)-2*e*e*vb*(h*h+v2)
    Delta=DC*DB
    Deltat=DCt*DB+DC*DBt
    ww=w*w
    A=a0*(1-ww)
    S=A*A+2*A*ww*P+ww*ww*Delta
    N=(A/2)*Deltat+ww*(P*Deltat-Delta*Pt)
    F=2*k*a0/(R*R)*N/(Delta*S)
    return F

def run(nh,nt,nw,eps):
    hs,wh=leggauss(nh);wh=wh/2
    zs,wt=gauss01(nt);theta=zs*np.pi/2
    w,ww=gauss01(nw)
    R=.75;tau=.125;lam=2559/512
    tic=time.perf_counter()
    c=r4_kernel(R,tau,lam,hs,theta,w)
    up=r4_kernel(R,tau+eps,lam,hs,theta,w)
    dn=r4_kernel(R,tau-eps,lam,hs,theta,w)
    K=np.einsum('ijk,k->ij',c,ww)
    Kt=np.einsum('ijk,k->ij',(up-dn)/(2*eps),ww)
    az=np.einsum('ij,j->i',Kt,wt)
    raw=np.einsum('ij,i,j->',np.abs(Kt),wh,wt)
    azL1=np.dot(np.abs(az),wh)
    total=np.einsum('ij,i,j->',K,wh,wt)
    dtotal=np.dot(az,wh)
    # More complete: before auxiliary w integration L1
    rawnw=np.einsum('ijk,i,j,k->',np.abs((up-dn)/(2*eps)),wh,wt,ww)
    # amount in h<cos(2) corresponds psi>2
    far=(hs<np.cos(2.0))
    far_frac=np.einsum('ij,i,j->',np.abs(Kt[far,:]),wh[far],wt)/raw
    out={'kind':'nonrigorous_Gauss_Legendre_fd','nh':nh,'nt':nt,'nw':nw,'eps':eps,
         'midpoint':{'R':R,'tau':tau,'lambda':lam},'W':total,
         'partial_tau_W':dtotal,'L1_raw_d_tau_K_after_w':raw,
         'L1_after_azimuth_average':azL1,
         'L1_before_w_average':rawnw,'azimuth_cancellation_factor':raw/azL1,
         'opposite_contact_fraction':far_frac,'time_s':time.perf_counter()-tic}
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--nh',type=int,default=100);p.add_argument('--nt',type=int,default=160);p.add_argument('--nw',type=int,default=64);p.add_argument('--eps',type=float,default=1e-5);p.add_argument('--out')
    args=p.parse_args();out=run(args.nh,args.nt,args.nw,args.eps); s=json.dumps(out,indent=2)
    print(s)
    if args.out:open(args.out,'w').write(s+'\n')
```

## spectral_pilot.py

```python
"""DIAGNOSTIC_ONLY/NOT_EVIDENCE. Numeric orthogonal control variates, not rigorous certification."""
import argparse,json,time
import numpy as np
from numpy.polynomial.legendre import leggauss,legvander
from r4_azimuth_pilot import r4_kernel,gauss01

def sample(nh,nt,nw,eps,R=.75,tau=.125,lam=2559/512):
    h,hw=leggauss(nh);hw=hw/2
    z,zw=gauss01(nt);th=np.pi/2*z
    w,ww=gauss01(nw)
    U=r4_kernel(R,tau+eps,lam,h,th,w)
    L=r4_kernel(R,tau-eps,lam,h,th,w)
    K=np.einsum('ijk,k->ij',(U-L)/(2*eps),ww)
    return h,hw,th,zw,K

def test(nh=120,nt=128,nw=64,eps=1e-5):
    t0=time.perf_counter()
    h,hw,th,tw,y=sample(nh,nt,nw,eps)
    h2,hw2,th2,tw2,y2=sample(nh+29,nt+13,nw,eps)
    res=[]
    for L,K in [(4,4),(8,8),(12,8),(16,12),(24,16),(32,20)]:
        P=legvander(h,L);Q=np.cos(2*np.outer(th,range(K+1)))
        # c_lk orthogonal projection: P norm 1/(2l+1), cosine norm 1 or .5
        A=np.einsum('il,ij,jk,i,j->lk',P,y,Q,hw,tw)
        A=A*(2*np.arange(L+1)+1)[:,None]
        A[:,1:]*=2
        predicted=P@A@Q.T
        P2=legvander(h2,L);Q2=np.cos(2*np.outer(th2,range(K+1)))
        yhat=P2@A@Q2.T
        raw=np.einsum('ij,i,j->',np.abs(y2),hw2,tw2)
        residual=np.einsum('ij,i,j->',np.abs(y2-yhat),hw2,tw2)
        maxerr=np.max(np.abs(y2-yhat))
        res.append({'Legendre_h_degree':L,'cos2theta_degree':K,'raw_L1':float(raw),'residual_L1':float(residual),'factor':float(raw/residual),'max_abs_residual':float(maxerr),'coefficient_c00':float(A[0,0])})
    return {'kind':'NONRIGOROUS_numeric_spectral','Wtau_reference':float(np.einsum('ij,i,j->',y2,hw2,tw2)),'results':res,'time_s':time.perf_counter()-t0}
if __name__=='__main__':
    ar=argparse.ArgumentParser();ar.add_argument('--out');args=ar.parse_args()
    z=test();print(json.dumps(z,indent=2));
    if args.out:open(args.out,'w').write(json.dumps(z,indent=2)+'\n')
```

## piecewise_control_pilot.py

```python
"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Piecewise angular control variates for d_tau W.
Coefficients are floating point; all conclusions are exploratory (not interval proof).
"""
import argparse,json,time,itertools
import numpy as np
from numpy.polynomial.legendre import leggauss,legvander
from r4_azimuth_pilot import r4_kernel,gauss01
BANDS=[(-1.,-.5),(-.5,0.),(0.,.5),(.5,.875),(.875,.96875),(.96875,1.)]
MIDDLE=(.75,.125,2559/512)

def k_deriv(p, h, theta, w, ww, eps=1e-5):
    R,tau,lam=p
    up=r4_kernel(R,tau+eps,lam,h,theta,w)
    dn=r4_kernel(R,tau-eps,lam,h,theta,w)
    return np.einsum('ijk,k->ij',(up-dn)/(2*eps),ww)

def coeff_at(p,lo,hi,L,K,nh,nt,nw,eps):
    h, hw=leggauss(nh); xx=h.copy(); h=lo+(h+1)*(hi-lo)/2;hw=hw/2
    z,tw=gauss01(nt);th=z*np.pi/2
    w,ww=gauss01(nw)
    y=k_deriv(p,h,th,w,ww,eps)
    P=legvander(xx,L)
    Q=np.cos(2*np.outer(th,range(K+1)))
    coeff=np.einsum('il,ij,jk,i,j->lk',P,y,Q,hw,tw)
    coeff*= (2*np.arange(L+1)+1)[:,None]
    coeff[:,1:]*=2
    return coeff

def eval_band(p,coeff,lo,hi,nh,nt,nw,eps):
    L=coeff.shape[0]-1;K=coeff.shape[1]-1
    xx,hw=leggauss(nh);h=lo+(xx+1)*(hi-lo)/2; hw=hw/2
    z,tw=gauss01(nt);th=z*np.pi/2
    w,ww=gauss01(nw)
    Y=k_deriv(p,h,th,w,ww,eps)
    yhat=legvander(xx,L)@coeff@np.cos(2*np.outer(th,range(K+1))).T
    raw=np.einsum('ij,i,j->',np.abs(Y),hw,tw)
    res=np.einsum('ij,i,j->',np.abs(Y-yhat),hw,tw)
    absmax=np.max(np.abs(Y-yhat))
    return [float(raw),float(res),float(absmax),float(np.einsum('ij,i,j->',Y,hw,tw))]

def test(L=8,K=8,nh=48,nt=64,nw=64,eps=1e-5, eval_corners=True):
    t0=time.perf_counter()
    coeffs=[coeff_at(MIDDLE,a,b,L,K,nh,nt,nw,eps) for a,b in BANDS]
    pars=[MIDDLE]
    if eval_corners:
      for R,tau,lam in itertools.product([95/128,97/128],[15/128,17/128],[1279/256,5]): pars.append((R,tau,lam))
    results=[]
    for p in pars:
       rows=[eval_band(p,c,a,b,nh+11,nt+13,nw,eps) for c,(a,b) in zip(coeffs,BANDS)]
       wts=np.array([(b-a)/2 for a,b in BANDS]); vals=np.array(rows)
       results.append({'R':p[0],'tau':p[1],'lambda':p[2],
                       'raw_L1':float(np.dot(wts,vals[:,0])),
                       'residual_L1_with_midpoint_coefficients':float(np.dot(wts,vals[:,1])),
                       'cancellation_factor':float(np.dot(wts,vals[:,0])/np.dot(wts,vals[:,1])),
                       'integral_derivative':float(np.dot(wts,vals[:,3]))})
    return {'status':'NONRIGOROUS','kernel':'R4 rational at same physical p','bands':BANDS,
            'polynomial':'piecewise Legendre(h) x cos(2k theta)','degrees':[L,K],
            'coefficients':'trained only at physical midpoint, no corner refitting',
            'results':results,'time_s':time.perf_counter()-t0}

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--L',type=int,default=8);a.add_argument('--K',type=int,default=8);a.add_argument('--out');args=a.parse_args()
    r=test(L=args.L,K=args.K);print(json.dumps(r,indent=2));
    if args.out:open(args.out,'w').write(json.dumps(r,indent=2)+'\n')
```

## trilinear_surrogate_pilot.py

```python
"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Double-precision surrogate, not interval certification.
Exact integral of EACH FROZEN rational polynomial exists by Legendre/Fourier orthogonality.
Fit floating coefficients here ONLY to diagnose possible shape of a rigorous implementation.
"""
import json,time,itertools,argparse
import numpy as np
from numpy.polynomial.legendre import leggauss,legvander
from r4_azimuth_pilot import r4_kernel,gauss01
from piecewise_control_pilot import BANDS,MIDDLE
BOUNDS=((95/128,97/128),(15/128,17/128),(1279/256,5.0))
CORNERS=list(itertools.product(*[(lo,hi) for lo,hi in BOUNDS]))

def K(p,h,theta,w,ww):
    return np.einsum('ijk,k->ij',r4_kernel(*p,h,theta,w),ww)

def coeff_at(p,lo,hi,L,Kc,nh,nt,nw):
    x,hw=leggauss(nh);h=lo+(x+1)*(hi-lo)/2;hw=hw/2
    z,tw=gauss01(nt);th=z*np.pi/2
    w,ww=gauss01(nw)
    y=K(p,h,th,w,ww)
    P=legvander(x,L);Q=np.cos(2*np.outer(th,range(Kc+1)))
    coeff=np.einsum('il,ij,jk,i,j->lk',P,y,Q,hw,tw)
    coeff*=(2*np.arange(L+1)+1)[:,None];coeff[:,1:]*=2
    return coeff

def weights(p):
    ls=[(x-a)/(b-a) for x,(a,b) in zip(p,BOUNDS)]
    return [np.prod([ (l if y==b else 1-l) for l,y,(a,b) in zip(ls,c,BOUNDS)]) for c in CORNERS]

def eval_band(p,coeff,lo,hi,nh,nt,nw):
    L=coeff.shape[0]-1;Kc=coeff.shape[1]-1
    x,hw=leggauss(nh);h=lo+(x+1)*(hi-lo)/2;hw=hw/2
    z,tw=gauss01(nt);th=z*np.pi/2
    w,ww=gauss01(nw)
    val=K(p,h,th,w,ww)
    appr=legvander(x,L)@coeff@np.cos(2*np.outer(th,range(Kc+1))).T
    return (float(np.einsum('ij,i,j->',np.abs(val),hw,tw)),
            float(np.einsum('ij,i,j->',np.abs(val-appr),hw,tw)),
            float(np.einsum('ij,i,j->',val,hw,tw)),float(coeff[0,0]))

def run(L=8,Kc=8,nh=40,nt=64,nw=64):
    start=time.perf_counter()
    coeffs=[[coeff_at(p,a,b,L,Kc,nh,nt,nw) for a,b in BANDS] for p in CORNERS]
    pts=[MIDDLE]+CORNERS
    # include 4 interior non-mid points
    pts.extend([tuple(a+(b-a)*f for a,b in BOUNDS) for f in [1/4,3/4]])
    rows=[]
    for p in pts:
        we=weights(p)
        combined=[sum(w*C[i] for w,C in zip(we,coeffs)) for i in range(len(BANDS))]
        v=np.array([eval_band(p,c,a,b,nh+17,nt+15,nw) for c,(a,b) in zip(combined,BANDS)])
        widths=np.array([(b-a)/2 for a,b in BANDS])
        raw=float(np.dot(widths,v[:,0]));res=float(np.dot(widths,v[:,1]));signed=float(np.dot(widths,v[:,2]));anal=float(np.dot(widths,v[:,3]))
        rows.append({'point':list(p),'actual_W':signed,'surrogate_exact_angular_integral':anal,
                     'signed_difference':signed-anal,'raw_L1':raw,'residual_L1':res,
                     'suppression_factor':raw/res})
    return {'kind':'NONRIGOROUS_3_parameter_trilinear_piecewise_angular_surrogate',
            'basis':'piecewise Legendre(h) x cos(2k theta)',
            'coefficients':'floating-point fits at 8 parameter corners',
            'L':L,'K':Kc,'training_quadrature':[nh,nt,nw],
            'validation_quadrature':[nh+17,nt+15,nw],
            'basis_bands':BANDS,'results':rows,'seconds':time.perf_counter()-start}

if __name__=='__main__':
    arg=argparse.ArgumentParser();arg.add_argument('--L',type=int,default=8);arg.add_argument('--K',type=int,default=8);arg.add_argument('--out');a=arg.parse_args()
    out=run(a.L,a.K);s=json.dumps(out,indent=2);print(s)
    if a.out:open(a.out,'w').write(s+'\n')
```

## three_dim_surrogate_pilot.py

```python
"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. 3D angular x w orthogonal surrogate; no interval certification."""
import numpy as np,json,time,argparse
from numpy.polynomial.legendre import leggauss,legvander
from r4_azimuth_pilot import r4_kernel,gauss01
from piecewise_control_pilot import BANDS,MIDDLE
WBANDS=[(0.,1/32),(1/32,1/16),(1/16,1/8),(1/8,1/4),(1/4,1/2),(1/2,1.)]

def train(Rtl, hb, wb,L,K,M,nh,nt,nw):
  ha,hbmax=hb;wa,wbmax=wb
  x,hw=leggauss(nh);hw=hw/2;h=ha+(x+1)*(hbmax-ha)/2
  y,tw=gauss01(nt);th=y*np.pi/2
  z,ww=leggauss(nw);ww=ww/2;w=wa+(z+1)*(wbmax-wa)/2
  f=r4_kernel(*Rtl,h,th,w)
  Pl=legvander(x,L);Fq=np.cos(2*np.outer(th,range(K+1)));Pz=legvander(z,M)
  C=np.einsum('il,jm,kn,ijk,i,j,k->lmn',Pl,Fq,Pz,f,hw,tw,ww,optimize=True)
  C*= (2*np.arange(L+1)+1)[:,None,None]
  C[:,1:,:]*=2
  C*= (2*np.arange(M+1)+1)[None,None,:]
  return C

def evaluate(Rtl,hb,wb,C,nh,nt,nw):
  ha,hbmax=hb;wa,wbmax=wb
  x,hw=leggauss(nh);hw=hw/2;h=ha+(x+1)*(hbmax-ha)/2
  y,tw=gauss01(nt);th=y*np.pi/2
  z,ww=leggauss(nw);ww=ww/2;w=wa+(z+1)*(wbmax-wa)/2
  f=r4_kernel(*Rtl,h,th,w)
  Pl=legvander(x,C.shape[0]-1);Fq=np.cos(2*np.outer(th,range(C.shape[1])));Pz=legvander(z,C.shape[2]-1)
  c1=np.einsum('il,lmn->imn',Pl,C,optimize=True)
  c2=np.einsum('jm,imn->ijn',Fq,c1,optimize=True)
  q=np.einsum('kn,ijn->ijk',Pz,c2,optimize=True)
  raw=np.einsum('ijk,i,j,k->',np.abs(f),hw,tw,ww)
  res=np.einsum('ijk,i,j,k->',np.abs(f-q),hw,tw,ww)
  signed=np.einsum('ijk,i,j,k->',f,hw,tw,ww)
  return raw,res,signed,C[0,0,0]

def run(L=6,K=6,M=6):
  s=time.perf_counter();total=np.zeros(4)
  for hb in BANDS:
    for wb in WBANDS:
      C=train(MIDDLE,hb,wb,L,K,M,24,36,16)
      v=evaluate(MIDDLE,hb,wb,C,29,43,19)
      factor=(hb[1]-hb[0])/2*(wb[1]-wb[0]);total+=factor*np.array(v)
  return {'kind':'NONRIGOROUS_3D_piecewise_polynomial_angular_w','degrees':[L,K,M],
          'h_bands':BANDS,'w_bands':WBANDS,
          'raw_L1':float(total[0]),'residual_L1':float(total[1]),
          'W_numeric':float(total[2]),'surrogate_analytic_integral':float(total[3]),
          'signed_difference':float(total[2]-total[3]),
          'L1_suppression':float(total[0]/total[1]),'seconds':time.perf_counter()-s}
if __name__=='__main__':
  a=argparse.ArgumentParser();a.add_argument('--L',type=int,default=6);a.add_argument('--K',type=int,default=6);a.add_argument('--M',type=int,default=6);a.add_argument('--out');args=a.parse_args()
  o=run(args.L,args.K,args.M);s=json.dumps(o,indent=2);print(s)
  if args.out:open(args.out,'w').write(s+'\n')
```

## trilinear_3D_pilot.py

```python
"""DIAGNOSTIC_ONLY / NOT_EVIDENCE: triple-variable surrogate trilinearly interpolated over box2."""
import json,time,argparse
import numpy as np
from three_dim_surrogate_pilot import train,evaluate,BANDS,WBANDS
from trilinear_surrogate_pilot import CORNERS,weights,MIDDLE,BOUNDS

def run(L=6,K=6,M=6):
    t0=time.perf_counter()
    mesh=[(hb,wb) for hb in BANDS for wb in WBANDS]
    cc=[[train(p,hb,wb,L,K,M,20,30,15) for hb,wb in mesh] for p in CORNERS]
    points=[MIDDLE]+CORNERS+[tuple(a+(b-a)*f for a,b in BOUNDS) for f in (1/4,3/4)]
    rows=[]
    for p in points:
        ww=weights(p);v=np.zeros(4)
        for j,(hb,wb) in enumerate(mesh):
            C=sum(vv*cc[i][j] for i,vv in enumerate(ww))
            v+=(hb[1]-hb[0])/2*(wb[1]-wb[0])*np.array(evaluate(p,hb,wb,C,25,37,19))
        rows.append({'point':list(p),'W':float(v[2]),'Q_exact_moment':float(v[3]),
                    'signed_difference':float(v[2]-v[3]),
                    'raw_L1_before_w':float(v[0]),'residual_L1_before_w':float(v[1]),
                    'ratio':float(v[0]/v[1])})
    return {'kind':'NONRIGOROUS_3D_corners_interpolation','degrees':[L,K,M],
            'frozen_fits':'eight corners only; interior not refit',
            'h_bands':BANDS,'w_bands':WBANDS,'rows':rows,'time_s':time.perf_counter()-t0}
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--L',type=int,default=6);a.add_argument('--K',type=int,default=6);a.add_argument('--M',type=int,default=6);a.add_argument('--out');u=a.parse_args()
    r=run(u.L,u.K,u.M);s=json.dumps(r,indent=2);print(s)
    if u.out:open(u.out,'w').write(s+'\n')
```

## multi_point_pilot.py

```python
"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Pointwise angular surrogate quality scan."""
import json,time
import numpy as np
from trilinear_surrogate_pilot import coeff_at,eval_band
from piecewise_control_pilot import BANDS
PTS=[(.1,.125,2.),(.5,.5,2.),(.75,0.,5.),(.75,.125,5.),(.75,1.,5.),(.9,.125,5.),(.98,.125,5.),(.99,.125,5.)]

def run():
  rows=[]; t0=time.perf_counter()
  for p in PTS:
    coeffs=[coeff_at(p,a,b,8,8,40,64,64) for a,b in BANDS]
    vals=np.array([eval_band(p,c,a,b,57,79,64) for c,(a,b) in zip(coeffs,BANDS)])
    wd=np.array([(b-a)/2 for a,b in BANDS]); raw=np.dot(wd,vals[:,0]);res=np.dot(wd,vals[:,1]);W=np.dot(wd,vals[:,2]);ap=np.dot(wd,vals[:,3]);
    rows.append({'p':p,'W':float(W),'surrogate':float(ap),'residual_abs_integral':float(res),'residual_signed':float(W-ap),'raw_L1':float(raw),'factor':float(raw/res)})
  return {'kind':'NONRIGOROUS_numeric_pilot','rows':rows,'seconds':time.perf_counter()-t0}
if __name__=='__main__':
  r=run();s=json.dumps(r,indent=2);print(s);open('/mnt/data/d_pro_cost_wall/multi_point_scan.json','w').write(s+'\n')
```

## w_dimension_pilot.py

```python
"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Test separation of w-integrated vs raw residual norms."""
import numpy as np,json
from numpy.polynomial.legendre import leggauss,legvander
from r4_azimuth_pilot import r4_kernel,gauss01
from trilinear_surrogate_pilot import coeff_at,MIDDLE,BANDS

def test(nw=96):
    acc=np.zeros(4)
    for a,b in BANDS:
        c=coeff_at(MIDDLE,a,b,8,8,44,64,nw)
        xx,hw=leggauss(57);hw=hw/2;h=a+(xx+1)*(b-a)/2
        z,tw=gauss01(79);th=z*np.pi/2
        w,ww=gauss01(nw)
        F=r4_kernel(*MIDDLE,h,th,w)
        Q=legvander(xx,8)@c@np.cos(2*np.outer(th,range(9))).T
        Kw=np.einsum('ijk,k->ij',F,ww)
        aw=(b-a)/2
        acc[0]+=aw*np.einsum('ijk,i,j,k->',np.abs(F-Q[:,:,None]),hw,tw,ww)
        acc[1]+=aw*np.einsum('ij,i,j->',np.abs(Kw-Q),hw,tw)
        acc[2]+=aw*np.einsum('ijk,i,j,k->',np.abs(F),hw,tw,ww)
        acc[3]+=aw*np.einsum('ij,i,j->',np.abs(Kw),hw,tw)
    return {'not_proof':True,'w_Gauss_nodes':nw,'L1_before_w_using_same_Q':float(acc[0]),
            'L1_after_w_using_same_Q':float(acc[1]),'L1_raw_F_before_w':float(acc[2]),'L1_raw_K_after_w':float(acc[3])}
if __name__=='__main__':
    r=test();print(json.dumps(r,indent=2));open('/mnt/data/d_pro_cost_wall/w_dimension_comparison.json','w').write(json.dumps(r,indent=2)+'\n')
```

## symbolic_moments.py

```python
"""Exact moments of the surrogate basis. DIAGNOSTIC_ONLY / NOT_EVIDENCE.
Proves the polynomial integration shortcut; does NOT prove an enclosure for R4.
"""
import sympy as s
x,y=s.symbols('x y',real=True)
maxdeg=8
moments_l=[s.integrate(s.legendre(j,x),(x,-1,1))/2 for j in range(maxdeg+1)]
moments_n=[s.integrate(s.legendre(j,y),(y,-1,1))/2 for j in range(maxdeg+1)]
# Exact angle integral via sin(m*pi)/(m*pi) =0 for integer m>=1;
# cos(2m theta) is the Chebyshev identity cos(2m theta) = T_m(2cos²theta-1).
assert all(v==int(i==0) for i,v in enumerate(moments_l))
assert all(v==int(i==0) for i,v in enumerate(moments_n))
q=s.symbols('q0:3')
trilinear=sum(s.prod(q[j] if (k>>j)&1 else 1-q[j] for j in range(3)) for k in range(8))
assert s.expand(trilinear-1)==0
theta=s.symbols('theta',real=True)
angle_moments=[s.simplify(2/s.pi*s.integrate(s.cos(2*m*theta),(theta,0,s.pi/2))) for m in range(maxdeg+1)]
assert all(v==int(i==0) for i,v in enumerate(angle_moments))
print('EXACT MOMENTS: Legendre h 9/9, Legendre w 9/9; Fourier nonconstant averages 8/8 (sin(m*pi)=0).')
print('TRILINEAR PARTITION OF UNITY:',s.expand(trilinear))
print('STATUS: symbolic control-variate identities only; NOT_EVIDENCE for W')
```

## cost_scenarios.py

```python
"""DIAGNOSTIC_ONLY / NOT_EVIDENCE. Conditional runtime budgets, not predictions."""
import json
cases=[('old_cover_B_reference',200000,235.562,12),
       ('goal_20k_240sec',20000,240,12),
       ('goal_5k_300sec',5000,300,12),
       ('goal_20k_300sec',20000,300,12),
       ('expensive_5k_1800sec',5000,1800,12),
       ('2D_4096cells_300sec',4096,300,12)]
rows=[]
for name,boxes,secs,cores in cases:
    wall=boxes*secs/cores
    rows.append(dict(name=name,boxes=boxes,seconds_per_box=secs,cores=cores,
                     ideal_wall_hours=wall/3600,ideal_wall_days=wall/86400,
                     wall_days_at_70pct_efficiency=wall/86400/0.7))
out={'status':'DIAGNOSTIC_ONLY / NOT_EVIDENCE','formula':'number_boxes * seconds_per_box / simultaneous_workers','assumption':'core=worker; true workers limited by RAM and CPU; scenarios not measured for method D','cases':rows}
s=json.dumps(out,ensure_ascii=False,indent=2)
print(s)
open('/mnt/data/d_pro_cost_wall/cost_scenarios.json','w').write(s+'\n')
```

## azimuth_n120_n160_w64.json

```json
{
  "kind": "nonrigorous_Gauss_Legendre_fd",
  "nh": 120,
  "nt": 160,
  "nw": 64,
  "eps": 1e-05,
  "midpoint": {
    "R": 0.75,
    "tau": 0.125,
    "lambda": 4.998046875
  },
  "W": 2.065906147743482,
  "partial_tau_W": -0.4140187488873248,
  "L1_raw_d_tau_K_after_w": 80.78382839758233,
  "L1_after_azimuth_average": 34.72302193891102,
  "L1_before_w_average": 81.6382992796465,
  "azimuth_cancellation_factor": 2.326520673796973,
  "opposite_contact_fraction": 0.7566567210327484,
  "time_s": 0.15070963900006973
}
```

## azimuth_n180_n192_w96.json

```json
{
  "kind": "nonrigorous_Gauss_Legendre_fd",
  "nh": 180,
  "nt": 192,
  "nw": 96,
  "eps": 1e-05,
  "midpoint": {
    "R": 0.75,
    "tau": 0.125,
    "lambda": 4.998046875
  },
  "W": 2.0659062847389364,
  "partial_tau_W": -0.41402448913441714,
  "L1_raw_d_tau_K_after_w": 80.77095523516907,
  "L1_after_azimuth_average": 34.690619172266324,
  "L1_before_w_average": 81.6384714934945,
  "azimuth_cancellation_factor": 2.328322675190013,
  "opposite_contact_fraction": 0.7495657837843197,
  "time_s": 0.1603902519998428
}
```

## spectral_degree_comparison.json

```json
{
  "kind": "NONRIGOROUS_numeric_spectral",
  "Wtau_reference": -0.41402519181283826,
  "results": [
    {
      "Legendre_h_degree": 4,
      "cos2theta_degree": 4,
      "raw_L1": 80.78071101682013,
      "residual_L1": 57.45589213632147,
      "factor": 1.4059604335297335,
      "max_abs_residual": 643.884778375222,
      "coefficient_c00": -0.41401874888843204
    },
    {
      "Legendre_h_degree": 8,
      "cos2theta_degree": 8,
      "raw_L1": 80.78071101682013,
      "residual_L1": 20.576444532273417,
      "factor": 3.9258828652403226,
      "max_abs_residual": 283.0954428420796,
      "coefficient_c00": -0.41401874888843204
    },
    {
      "Legendre_h_degree": 12,
      "cos2theta_degree": 8,
      "raw_L1": 80.78071101682013,
      "residual_L1": 10.112558854352718,
      "factor": 7.988157318070879,
      "max_abs_residual": 268.00807969620314,
      "coefficient_c00": -0.41401874888843204
    },
    {
      "Legendre_h_degree": 16,
      "cos2theta_degree": 12,
      "raw_L1": 80.78071101682013,
      "residual_L1": 2.760038543490591,
      "factor": 29.2679648287294,
      "max_abs_residual": 101.1421248886773,
      "coefficient_c00": -0.41401874888843204
    },
    {
      "Legendre_h_degree": 24,
      "cos2theta_degree": 16,
      "raw_L1": 80.78071101682013,
      "residual_L1": 1.0935846825981757,
      "factor": 73.8678149961817,
      "max_abs_residual": 143.85236144892116,
      "coefficient_c00": -0.41401874888843204
    },
    {
      "Legendre_h_degree": 32,
      "cos2theta_degree": 20,
      "raw_L1": 80.78071101682013,
      "residual_L1": 0.5328838876526613,
      "factor": 151.59158099648485,
      "max_abs_residual": 97.62681674460751,
      "coefficient_c00": -0.41401874888843204
    }
  ],
  "time_s": 0.26171310500012623
}
```

## piecewise_L8_K8.json

```json
{
  "status": "NONRIGOROUS",
  "kernel": "R4 rational at same physical p",
  "bands": [
    [
      -1.0,
      -0.5
    ],
    [
      -0.5,
      0.0
    ],
    [
      0.0,
      0.5
    ],
    [
      0.5,
      0.875
    ],
    [
      0.875,
      0.96875
    ],
    [
      0.96875,
      1.0
    ]
  ],
  "polynomial": "piecewise Legendre(h) x cos(2k theta)",
  "degrees": [
    8,
    8
  ],
  "coefficients": "trained only at physical midpoint, no corner refitting",
  "results": [
    {
      "R": 0.75,
      "tau": 0.125,
      "lambda": 4.998046875,
      "raw_L1": 80.76941422773469,
      "residual_L1_with_midpoint_coefficients": 2.3289088430794513,
      "cancellation_factor": 34.68122613203509,
      "integral_derivative": -0.41402453171516196
    },
    {
      "R": 0.7421875,
      "tau": 0.1171875,
      "lambda": 4.99609375,
      "raw_L1": 83.6966280695867,
      "residual_L1_with_midpoint_coefficients": 11.935125634122834,
      "cancellation_factor": 7.01263066978498,
      "integral_derivative": -0.3822500606388267
    },
    {
      "R": 0.7421875,
      "tau": 0.1171875,
      "lambda": 5,
      "raw_L1": 83.81982883596045,
      "residual_L1_with_midpoint_coefficients": 12.017554398444046,
      "cancellation_factor": 6.974782560319668,
      "integral_derivative": -0.38232130102082074
    },
    {
      "R": 0.7421875,
      "tau": 0.1328125,
      "lambda": 4.99609375,
      "raw_L1": 79.68922223547436,
      "residual_L1_with_midpoint_coefficients": 9.60035021112227,
      "cancellation_factor": 8.300657838830942,
      "integral_derivative": -0.4279034141523489
    },
    {
      "R": 0.7421875,
      "tau": 0.1328125,
      "lambda": 5,
      "raw_L1": 79.79836850845648,
      "residual_L1_with_midpoint_coefficients": 9.57221433488616,
      "cancellation_factor": 8.336458599514373,
      "integral_derivative": -0.4279834772946405
    },
    {
      "R": 0.7578125,
      "tau": 0.1171875,
      "lambda": 4.99609375,
      "raw_L1": 81.53331489330799,
      "residual_L1_with_midpoint_coefficients": 9.759818620279997,
      "cancellation_factor": 8.353978497498849,
      "integral_derivative": -0.3987009101231983
    },
    {
      "R": 0.7578125,
      "tau": 0.1171875,
      "lambda": 5,
      "raw_L1": 81.65341493271248,
      "residual_L1_with_midpoint_coefficients": 9.82289447985146,
      "cancellation_factor": 8.312561546924734,
      "integral_derivative": -0.39877482909557677
    },
    {
      "R": 0.7578125,
      "tau": 0.1328125,
      "lambda": 4.99609375,
      "raw_L1": 77.5899682500484,
      "residual_L1_with_midpoint_coefficients": 11.510928397405474,
      "cancellation_factor": 6.740548248700507,
      "integral_derivative": -0.4463765805055838
    },
    {
      "R": 0.7578125,
      "tau": 0.1328125,
      "lambda": 5,
      "raw_L1": 77.69618093307344,
      "residual_L1_with_midpoint_coefficients": 11.465933364089972,
      "cancellation_factor": 6.7762630800218355,
      "integral_derivative": -0.4464596812918611
    }
  ],
  "time_s": 0.694121172999985
}
```

## trilinear_box2_L8_K8.json

```json
{
  "kind": "NONRIGOROUS_3_parameter_trilinear_piecewise_angular_surrogate",
  "basis": "piecewise Legendre(h) x cos(2k theta)",
  "coefficients": "floating-point fits at 8 parameter corners",
  "L": 8,
  "K": 8,
  "training_quadrature": [
    40,
    64,
    64
  ],
  "validation_quadrature": [
    57,
    79,
    64
  ],
  "basis_bands": [
    [
      -1.0,
      -0.5
    ],
    [
      -0.5,
      0.0
    ],
    [
      0.0,
      0.5
    ],
    [
      0.5,
      0.875
    ],
    [
      0.875,
      0.96875
    ],
    [
      0.96875,
      1.0
    ]
  ],
  "results": [
    {
      "point": [
        0.75,
        0.125,
        4.998046875
      ],
      "actual_W": 2.065906284796292,
      "surrogate_exact_angular_integral": 2.0658032488952904,
      "signed_difference": 0.0001030359010014692,
      "raw_L1": 8.722445767890498,
      "residual_L1": 0.10439686887546663,
      "suppression_factor": 83.55083693453838
    },
    {
      "point": [
        0.7421875,
        0.1171875,
        4.99609375
      ],
      "actual_W": 2.0699575921031026,
      "surrogate_exact_angular_integral": 2.069957592103103,
      "signed_difference": -4.440892098500626e-16,
      "raw_L1": 9.182551565420608,
      "residual_L1": 0.08601493386803664,
      "suppression_factor": 106.75531739068006
    },
    {
      "point": [
        0.7421875,
        0.1171875,
        5.0
      ],
      "actual_W": 2.0699210978894054,
      "surrogate_exact_angular_integral": 2.0699210978894156,
      "signed_difference": -1.021405182655144e-14,
      "raw_L1": 9.18899781284589,
      "residual_L1": 0.08633237186966128,
      "suppression_factor": 106.43745345857997
    },
    {
      "point": [
        0.7421875,
        0.1328125,
        4.99609375
      ],
      "actual_W": 2.063625907678082,
      "surrogate_exact_angular_integral": 2.063625907678088,
      "signed_difference": -5.773159728050814e-15,
      "raw_L1": 8.552018711483889,
      "residual_L1": 0.0793855957168928,
      "suppression_factor": 107.72758753341532
    },
    {
      "point": [
        0.7421875,
        0.1328125,
        5.0
      ],
      "actual_W": 2.063588231099257,
      "surrogate_exact_angular_integral": 2.0635882310992497,
      "signed_difference": 7.105427357601002e-15,
      "raw_L1": 8.557740059242068,
      "residual_L1": 0.07967207105285132,
      "suppression_factor": 107.41204472474676
    },
    {
      "point": [
        0.7578125,
        0.1171875,
        4.99609375
      ],
      "actual_W": 2.068152705982911,
      "surrogate_exact_angular_integral": 2.0681527059829192,
      "signed_difference": -8.43769498715119e-15,
      "raw_L1": 8.889937712860775,
      "residual_L1": 0.08191422834621398,
      "suppression_factor": 108.52739374272164
    },
    {
      "point": [
        0.7578125,
        0.1171875,
        5.0
      ],
      "actual_W": 2.0681190940869416,
      "surrogate_exact_angular_integral": 2.068119094086952,
      "signed_difference": -1.021405182655144e-14,
      "raw_L1": 8.896212530620346,
      "residual_L1": 0.08221595693450853,
      "suppression_factor": 108.2054246197837
    },
    {
      "point": [
        0.7578125,
        0.1328125,
        4.99609375
      ],
      "actual_W": 2.061548100620664,
      "surrogate_exact_angular_integral": 2.061548100620668,
      "signed_difference": -3.9968028886505635e-15,
      "raw_L1": 8.274593391545391,
      "residual_L1": 0.07576108449869881,
      "suppression_factor": 109.21957422200717
    },
    {
      "point": [
        0.7578125,
        0.1328125,
        5.0
      ],
      "actual_W": 2.061513261701935,
      "surrogate_exact_angular_integral": 2.0615132617019283,
      "signed_difference": 6.661338147750939e-15,
      "raw_L1": 8.280155206199872,
      "residual_L1": 0.07603375876981763,
      "suppression_factor": 108.90103738349923
    },
    {
      "point": [
        0.74609375,
        0.12109375,
        4.9970703125
      ],
      "actual_W": 2.0679739474559784,
      "surrogate_exact_angular_integral": 2.067897373904065,
      "signed_difference": 7.657355191348358e-05,
      "raw_L1": 8.949412846083547,
      "residual_L1": 0.09952863430590257,
      "suppression_factor": 89.91797092862149
    },
    {
      "point": [
        0.75390625,
        0.12890625,
        4.9990234375
      ],
      "actual_W": 2.0637531922653394,
      "surrogate_exact_angular_integral": 2.0636752128901295,
      "signed_difference": 7.797937520992448e-05,
      "raw_L1": 8.49864622833211,
      "residual_L1": 0.09478076985633183,
      "suppression_factor": 89.66635575142838
    }
  ],
  "seconds": 0.8566868949999389
}
```

## three_dim_L6.json

```json
{
  "kind": "NONRIGOROUS_3D_piecewise_polynomial_angular_w",
  "degrees": [
    6,
    6,
    6
  ],
  "h_bands": [
    [
      -1.0,
      -0.5
    ],
    [
      -0.5,
      0.0
    ],
    [
      0.0,
      0.5
    ],
    [
      0.5,
      0.875
    ],
    [
      0.875,
      0.96875
    ],
    [
      0.96875,
      1.0
    ]
  ],
  "w_bands": [
    [
      0.0,
      0.03125
    ],
    [
      0.03125,
      0.0625
    ],
    [
      0.0625,
      0.125
    ],
    [
      0.125,
      0.25
    ],
    [
      0.25,
      0.5
    ],
    [
      0.5,
      1.0
    ]
  ],
  "raw_L1": 8.763957658405158,
  "residual_L1": 0.197912810245494,
  "W_numeric": 2.0659062847962426,
  "surrogate_analytic_integral": 2.065906284825188,
  "signed_difference": -2.894529060881723e-11,
  "L1_suppression": 44.28191205781078,
  "seconds": 0.13325548100010565
}
```

## three_dim_L8.json

```json
{
  "kind": "NONRIGOROUS_3D_piecewise_polynomial_angular_w",
  "degrees": [
    8,
    8,
    8
  ],
  "h_bands": [
    [
      -1.0,
      -0.5
    ],
    [
      -0.5,
      0.0
    ],
    [
      0.0,
      0.5
    ],
    [
      0.5,
      0.875
    ],
    [
      0.875,
      0.96875
    ],
    [
      0.96875,
      1.0
    ]
  ],
  "w_bands": [
    [
      0.0,
      0.03125
    ],
    [
      0.03125,
      0.0625
    ],
    [
      0.0625,
      0.125
    ],
    [
      0.125,
      0.25
    ],
    [
      0.25,
      0.5
    ],
    [
      0.5,
      1.0
    ]
  ],
  "raw_L1": 8.763957658405158,
  "residual_L1": 0.08122608290265836,
  "W_numeric": 2.0659062847962426,
  "surrogate_analytic_integral": 2.065906284825188,
  "signed_difference": -2.894529060881723e-11,
  "L1_suppression": 107.89585494240707,
  "seconds": 0.12932503699994413
}
```

## trilinear_3D_L6.json

```json
{
  "kind": "NONRIGOROUS_3D_corners_interpolation",
  "degrees": [
    6,
    6,
    6
  ],
  "frozen_fits": "eight corners only; interior not refit",
  "h_bands": [
    [
      -1.0,
      -0.5
    ],
    [
      -0.5,
      0.0
    ],
    [
      0.0,
      0.5
    ],
    [
      0.5,
      0.875
    ],
    [
      0.875,
      0.96875
    ],
    [
      0.96875,
      1.0
    ]
  ],
  "w_bands": [
    [
      0.0,
      0.03125
    ],
    [
      0.03125,
      0.0625
    ],
    [
      0.0625,
      0.125
    ],
    [
      0.125,
      0.25
    ],
    [
      0.25,
      0.5
    ],
    [
      0.5,
      1.0
    ]
  ],
  "rows": [
    {
      "point": [
        0.75,
        0.125,
        4.998046875
      ],
      "W": 2.065906284805498,
      "Q_exact_moment": 2.065803248959426,
      "signed_difference": 0.00010303584607207483,
      "raw_L1_before_w": 8.764826204116874,
      "residual_L1_before_w": 0.21292082314220348,
      "ratio": 41.16472064483382
    },
    {
      "point": [
        0.7421875,
        0.1171875,
        4.99609375
      ],
      "W": 2.069957592111554,
      "Q_exact_moment": 2.06995759216344,
      "signed_difference": -5.1886051011251766e-11,
      "raw_L1_before_w": 9.231656175209311,
      "residual_L1_before_w": 0.2200050870944373,
      "ratio": 41.96110325051992
    },
    {
      "point": [
        0.7421875,
        0.1171875,
        5.0
      ],
      "W": 2.0699210978980007,
      "Q_exact_moment": 2.0699210979496168,
      "signed_difference": -5.161604477166293e-11,
      "raw_L1_before_w": 9.23809759747564,
      "residual_L1_before_w": 0.2206879630167833,
      "ratio": 41.860450706924524
    },
    {
      "point": [
        0.7421875,
        0.1328125,
        4.99609375
      ],
      "W": 2.0636259076726984,
      "Q_exact_moment": 2.063625907394051,
      "signed_difference": 2.786473274341006e-10,
      "raw_L1_before_w": 8.587814078662012,
      "residual_L1_before_w": 0.19165657581587178,
      "ratio": 44.8083455634337
    },
    {
      "point": [
        0.7421875,
        0.1328125,
        5.0
      ],
      "W": 2.063588231093771,
      "Q_exact_moment": 2.063588230811929,
      "signed_difference": 2.8184210520976194e-10,
      "raw_L1_before_w": 8.59353638410668,
      "residual_L1_before_w": 0.19225448945941076,
      "ratio": 44.69875532306343
    },
    {
      "point": [
        0.7578125,
        0.1171875,
        4.99609375
      ],
      "W": 2.0681527059838296,
      "Q_exact_moment": 2.068152707638045,
      "signed_difference": -1.654215431301509e-09,
      "raw_L1_before_w": 8.93788226559084,
      "residual_L1_before_w": 0.2080301361510259,
      "ratio": 42.96436290894945
    },
    {
      "point": [
        0.7578125,
        0.1171875,
        5.0
      ],
      "W": 2.0681190940879026,
      "Q_exact_moment": 2.068119095762473,
      "signed_difference": -1.6745702602349866e-09,
      "raw_L1_before_w": 8.944151247032298,
      "residual_L1_before_w": 0.2086747672053641,
      "ratio": 42.86168072362121
    },
    {
      "point": [
        0.7578125,
        0.1328125,
        4.99609375
      ],
      "W": 2.061548100621646,
      "Q_exact_moment": 2.0615480994452087,
      "signed_difference": 1.1764371699030107e-09,
      "raw_L1_before_w": 8.309204655140979,
      "residual_L1_before_w": 0.18268105474019816,
      "ratio": 45.484763961747454
    },
    {
      "point": [
        0.7578125,
        0.1328125,
        5.0
      ],
      "W": 2.0615132617028995,
      "Q_exact_moment": 2.0615132605106417,
      "signed_difference": 1.1922578480039192e-09,
      "raw_L1_before_w": 8.314770039166742,
      "residual_L1_before_w": 0.18325068627456348,
      "ratio": 45.373745704334056
    },
    {
      "point": [
        0.74609375,
        0.12109375,
        4.9970703125
      ],
      "W": 2.067973947465756,
      "Q_exact_moment": 2.067897374122154,
      "signed_difference": 7.657334360189338e-05,
      "raw_L1_before_w": 8.995670655142932,
      "residual_L1_before_w": 0.21788364704483368,
      "ratio": 41.286580141059886
    },
    {
      "point": [
        0.75390625,
        0.12890625,
        4.9990234375
      ],
      "W": 2.063753192271647,
      "Q_exact_moment": 2.0636752124855056,
      "signed_difference": 7.797978614165757e-05,
      "raw_L1_before_w": 8.537662231482027,
      "residual_L1_before_w": 0.199465174299477,
      "ratio": 42.802771268048936
    }
  ],
  "time_s": 1.1532356810000692
}
```

## multi_point_scan.json

```json
{
  "kind": "NONRIGOROUS_numeric_pilot",
  "rows": [
    {
      "p": [
        0.1,
        0.125,
        2.0
      ],
      "W": 1.4818892774951689,
      "surrogate": 1.481889277495398,
      "residual_abs_integral": 0.007847466987486798,
      "residual_signed": -2.291500322826323e-13,
      "raw_L1": 107.4923203468126,
      "factor": 13697.709148469794
    },
    {
      "p": [
        0.5,
        0.5,
        2.0
      ],
      "W": 1.3969251579117197,
      "surrogate": 1.39692515791172,
      "residual_abs_integral": 5.915717468643955e-05,
      "residual_signed": -2.220446049250313e-16,
      "raw_L1": 3.7110341277230763,
      "factor": 62731.767488783524
    },
    {
      "p": [
        0.75,
        0.0,
        5.0
      ],
      "W": 2.092413352940779,
      "surrogate": 2.092413352940842,
      "residual_abs_integral": 0.4700623793249298,
      "residual_signed": -6.306066779870889e-14,
      "raw_L1": 12.802845743750668,
      "factor": 27.236482447578993
    },
    {
      "p": [
        0.75,
        0.125,
        5.0
      ],
      "W": 2.0658883611558716,
      "surrogate": 2.0658883611558836,
      "residual_abs_integral": 0.08099325648288666,
      "residual_signed": -1.199040866595169e-14,
      "raw_L1": 8.725439076000931,
      "factor": 107.73043898839354
    },
    {
      "p": [
        0.75,
        1.0,
        5.0
      ],
      "W": 1.594796310102401,
      "surrogate": 1.5947963101046818,
      "residual_abs_integral": 0.49246675737016377,
      "residual_signed": -2.2808421817899216e-12,
      "raw_L1": 5.469825466165913,
      "factor": 11.106994298204999
    },
    {
      "p": [
        0.9,
        0.125,
        5.0
      ],
      "W": 2.042248764335417,
      "surrogate": 2.042248763741741,
      "residual_abs_integral": 0.05167169446382023,
      "residual_signed": 5.936762192959577e-10,
      "raw_L1": 6.590943273260722,
      "factor": 127.55423141533717
    },
    {
      "p": [
        0.98,
        0.125,
        5.0
      ],
      "W": 2.0243079148342997,
      "surrogate": 2.0243071697856236,
      "residual_abs_integral": 0.039487771549500505,
      "residual_signed": 7.450486760873787e-07,
      "raw_L1": 5.796692634887896,
      "factor": 146.79715789029427
    },
    {
      "p": [
        0.99,
        0.125,
        5.0
      ],
      "W": 2.021718767323569,
      "surrogate": 2.021718626947009,
      "residual_abs_integral": 0.03816391211568872,
      "residual_signed": 1.4037656015375433e-07,
      "raw_L1": 5.7090533817183395,
      "factor": 149.59298104481846
    }
  ],
  "seconds": 0.6391414629999872
}
```

## w_dimension_comparison.json

```json
{
  "not_proof": true,
  "w_Gauss_nodes": 96,
  "L1_before_w_using_same_Q": 1.9139262026230932,
  "L1_after_w_using_same_Q": 0.08084610988704193,
  "L1_raw_F_before_w": 8.764000198863497,
  "L1_raw_K_after_w": 8.722445767890498
}
```

## cost_scenarios.json

```json
{
  "status": "DIAGNOSTIC_ONLY / NOT_EVIDENCE",
  "formula": "number_boxes * seconds_per_box / simultaneous_workers",
  "assumption": "core=worker; true workers limited by RAM and CPU; scenarios not measured for method D",
  "cases": [
    {
      "name": "old_cover_B_reference",
      "boxes": 200000,
      "seconds_per_box": 235.562,
      "cores": 12,
      "ideal_wall_hours": 1090.5648148148148,
      "ideal_wall_days": 45.44020061728395,
      "wall_days_at_70pct_efficiency": 64.91457231040565
    },
    {
      "name": "goal_20k_240sec",
      "boxes": 20000,
      "seconds_per_box": 240,
      "cores": 12,
      "ideal_wall_hours": 111.11111111111111,
      "ideal_wall_days": 4.62962962962963,
      "wall_days_at_70pct_efficiency": 6.613756613756614
    },
    {
      "name": "goal_5k_300sec",
      "boxes": 5000,
      "seconds_per_box": 300,
      "cores": 12,
      "ideal_wall_hours": 34.72222222222222,
      "ideal_wall_days": 1.4467592592592593,
      "wall_days_at_70pct_efficiency": 2.066798941798942
    },
    {
      "name": "goal_20k_300sec",
      "boxes": 20000,
      "seconds_per_box": 300,
      "cores": 12,
      "ideal_wall_hours": 138.88888888888889,
      "ideal_wall_days": 5.787037037037037,
      "wall_days_at_70pct_efficiency": 8.267195767195767
    },
    {
      "name": "expensive_5k_1800sec",
      "boxes": 5000,
      "seconds_per_box": 1800,
      "cores": 12,
      "ideal_wall_hours": 208.33333333333334,
      "ideal_wall_days": 8.680555555555555,
      "wall_days_at_70pct_efficiency": 12.400793650793652
    },
    {
      "name": "2D_4096cells_300sec",
      "boxes": 4096,
      "seconds_per_box": 300,
      "cores": 12,
      "ideal_wall_hours": 28.444444444444443,
      "ideal_wall_days": 1.1851851851851851,
      "wall_days_at_70pct_efficiency": 1.693121693121693
    }
  ]
}
```

