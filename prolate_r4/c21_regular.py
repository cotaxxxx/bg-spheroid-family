"""D-PRO C21 regular H=E_rho/rho, representative boxes only.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Independent measurements; no sign choices.
Pinned R3 physical rho derivative and rigorous signed spatial Taylor quadrature.
"""
import argparse,json,resource,time
from pathlib import Path
import flint
from flint import arb,fmpq as Q,ctx
from prolate_r1.density import common,Domain,seed
from prolate_r1.jets import Jet
from prolate_r1.intervals import Config,bounds,ball,midpoint,radius,sym
from prolate_r1.quadrature import (make_mesh,integrate,cut_location,
                                  distance_lower_squared)
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
PIN="fdfb498f2117cc0c5d72e88cc3be05eac9727bd8"
KAP=Q(1,4096);ORDER=4;BU=8;BV=16;RATIO=Q(2)
R0=(Q(63,128),Q(65,128));T0=(Q(63,128),Q(65,128))
TR=(Q(0),Q(1,64));LR=(Q(1791,512),Q(1793,512))
WIDE=(Q(1279,256),Q(5))
BOXES={
 "G2":(R0,T0,(Q(2),Q(513,256))),
 "G35":(R0,T0,LR),
 "EQ":(R0,TR,WIDE),
 "BD":((Q(63,64),Q(1)),T0,WIDE),
 "LW":(R0,T0,(Q(2),Q(9,4)))}
for k in range(1,16):BOXES[f"STRIP_{k:02}"]=((Q(k,16),Q(k+1,16)),TR,LR)
def iv(p):return arb(p[0]).union(arb(p[1]))
def enc(x):
 l,r=bounds(x)
 return {"lower":str(l),"upper":str(r),"lo":float(arb(l)),
         "hi":float(arb(r)),"mid":float(arb((l+r)/2)),
         "halfwidth":float(arb((r-l)/2))}
def cap_bound(Rbox,Tbox,Lbox):
 rho_min=Rbox[0]*(1-Tbox[1]**2)/(1+Tbox[1]**2)
 assert rho_min>0
 # |f_rho|<=G_max+2k*Rfun_max*|gamma_rho|
 # G_max=pi²/4, Rfun_max=pi/2,
 # |gamma_rho|<=(1+lambda_max)/D, 0<=k/D<=1.
 M=arb.pi()**2/4+arb.pi()*(1+arb(Lbox[1]))
 E=M*arb(KAP)/(2*arb(rho_min))
 return sym(E.upper().fmpq())
def dens(u,v,params,dom,Tbox,active=(),orders=(0,)):
 R,tau,lam,a,b,k,sigma,mx,mz,xx,xz,C,B,g,G,rr,rp,d,e,jac=common(
      u,v,params,dom,active,orders)
 rhi=dom.R[1];Lhi=dom.lam[1]
 # Positive reciprocal D. Contact cap is fixed in eta chart.
 U=seed(u,"u",active,orders)
 cut=cut_location(dom.kappa)
 U=U*(1-cut)+cut
 qc=8*U**2/(1+U**2)**2
 qlo=max(dom.kappa,Q(0),qc.c[0].lower().fmpq())
 ds=distance_lower_squared(dom.R,qlo)
 if ds<=0:raise ArithmeticError("OPEN: no positive D distance bound")
 dl=arb(ds).sqrt().lower().fmpq()
 D=sigma*C.sqrt()
 invD=D.reciprocal_positive(dl,Lhi*(1+rhi))
 invsqrtB=B.sqrt().reciprocal_positive(Q(1,Lhi),Q(1))
 dx=g*(mx/C.sqrt())-xx*invsqrtB
 fx=-xx*G-2*k*rr*dx*invD
 a_lo=(1-Tbox[1]**2)/(1+Tbox[1]**2)
 rho_lo=dom.R[0]*a_lo
 if rho_lo<=0:raise ArithmeticError("OPEN: requires second-rho route")
 invrho=(R*a).reciprocal_positive(rho_lo,rhi)
 return (fx*jac*invrho,)
def signed(mesh,params,dom,tbox,outer=None):
 if outer is None:
  return integrate(lambda u,v,axis,n:dens(u,v,params,dom,tbox,(axis,),(n,)),mesh,ORDER)[0]
 def cb(u,v,axis,n):
  full=dens(u,v,params,dom,tbox,(axis,outer),(n,1))[0]
  return (Jet((n,),[full.coeff(k,1) for k in range(n+1)]),)
 return integrate(cb,mesh,ORDER)[0]
def run(name):
 assert flint.__version__=="0.8.0"
 rbox,tbox,lbox=BOXES[name];begin=time.perf_counter()
 cap=KAP if rbox[1]==1 else Q(0)
 cfg=Config(precision=128,order=ORDER,base_u=BU,base_v=BV,
            distance_ratio=RATIO,max_cells=40000,max_depth=28)
 with ctx.workprec(128):
  dom=Domain(rbox,lbox,cap,"equator")
  mesh=make_mesh(rbox,cap,cfg,lam=lbox)
  print("MESH",name,len(mesh),flush=True)
  center_point=tuple(map(arb,(midpoint(rbox),midpoint(tbox),midpoint(lbox))))
  outer=tuple(map(iv,(rbox,tbox,lbox)))
  t=time.perf_counter();p=signed(mesh,center_point,dom,tbox)
  pointsecs=time.perf_counter()-t
  print("CENTER",name,enc(p),flush=True)
  parts={};cor=arb(0)
  for b,ax in zip((rbox,tbox,lbox),("R","x","lam")):
   t=time.perf_counter()
   d=signed(mesh,outer,dom,tbox,ax)
   term=d*sym(radius(b));cor+=term
   parts[ax]={"integrated_signed_derivative":enc(d),
              "outer_halfwidth_contribution":enc(term),
              "wall_s":time.perf_counter()-t}
   print("D",name,ax,parts[ax]["outer_halfwidth_contribution"]["halfwidth"],flush=True)
  E=cap_bound(rbox,tbox,lbox) if cap else arb(0)
  H=p+cor+E;hlo,hhi=bounds(H)
  pv=enc(p)["mid"];rel=enc(H)["halfwidth"]/abs(pv) if pv else None
  return {"status":STATUS,"name":name,"route":"regular direct f_rho/rho",
   "input_box":{"R":list(map(str,rbox)),"tau":list(map(str,tbox)),
                "lambda":list(map(str,lbox))},
   "H_interval":enc(H),"center_point":enc(p),
   "normalized_halfwidth":rel,"zero_included_RECORD_ONLY":bool(hlo<=0<=hhi),
   "outer_correction":enc(cor),"cap_correction":enc(E),
   "directional_contributions":parts,"mesh_cells":len(mesh),
   "mesh":{"order":ORDER,"base_u":BU,"base_v":BV,"distance_ratio":str(RATIO),
           "kappa":str(cap)},
   "center_wall_s":pointsecs,"wall_s":time.perf_counter()-begin,
   "peak_RSS_KiB":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
   "pinned_R3_commit":PIN,"global_claim":"OPEN"}
def main():
 p=argparse.ArgumentParser();p.add_argument("--name",choices=sorted(BOXES),required=True)
 p.add_argument("--output",required=True);a=p.parse_args()
 x=run(a.name)
 Path(a.output).write_text(json.dumps(x,indent=2)+"\n")
 print("RESULT",a.name,x["H_interval"],"seconds",x["wall_s"],flush=True)
if __name__=="__main__":main()
