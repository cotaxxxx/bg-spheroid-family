"""D-PRO C21 axis/center regularization: H=integral f_rho_rho(s rho,z) ds.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Uses no E_z derivatives.
"""
from __future__ import annotations
import argparse,json,time,resource
from pathlib import Path
import flint
from flint import arb,fmpq as Q,ctx
from prolate_r1.density import Domain,seed
from prolate_r1.jets import Jet,angle
from prolate_r1.intervals import Config,bounds,ball,midpoint,radius,sym,mag
from prolate_r1.quadrature import make_mesh,integrate
from .c21_regular import (enc,iv,STATUS,KAP,ORDER,BU,BV,RATIO,BOXES,
                            PIN)
BOXES["AX"]=((Q(63,128),Q(65,128)),(Q(63,64),Q(1)),(Q(1279,256),Q(5)))
BOXES["CE"]=((Q(0),Q(1,64)),(Q(63,128),Q(65,128)),(Q(1279,256),Q(5)))
BOXES["STRIP_00"]=((Q(0),Q(1,16)),(Q(0),Q(1,64)),(Q(1791,512),Q(1793,512)))
SPECIAL=("AX","CE","STRIP_00")
def rr(u,v,s,params,dom,active=(),orders=(0,)):
 R,tau,lam=(seed(z,n,active,orders) for z,n in zip(params,("R","x","lam")))
 U=seed(u,"u",active,orders)
 V=seed(v,"v",active,orders)
 S=seed(s,"s",active,orders)
 qc=8*U**2/(1+U**2)**2
 sp=4*U*(1-U**2)/(1+U**2)**2
 ex=1-qc;ez=sp*(V*arb.pi()).cos()
 a=(1-tau*tau)/(1+tau*tau);b=2*tau/(1+tau*tau)
 xi_x=a*ex-b*ez;xi_z=b*ex+a*ez
 rho=S*R*a;z=R*b
 rhi=dom.R[1];lhi=dom.lam[1]
 k=(1-rho*xi_x-z*xi_z).cap(1-rhi,1+rhi)
 D2=1+rho*rho+z*z-2*rho*xi_x-2*z*xi_z+(lam*lam-1)*(xi_z-z)**2
 dlow=(1-rhi)**2
 if dlow<=0:raise ArithmeticError("regularized route requires Rhi<1")
 D2=D2.cap(dlow,lhi*lhi*(1+rhi)**2)
 D=D2.sqrt()
 invD=D.reciprocal_positive(1-rhi,lhi*(1+rhi))
 invD2=D2.reciprocal_positive(dlow,lhi*lhi*(1+rhi)**2)
 B=(1-(1-1/lam**2)*xi_z**2).cap(1/lhi**2,1)
 invB=B.sqrt().reciprocal_positive(Q(1)/lhi,Q(1))
 g=(k*invD*invB).cap(0,1)
 G,rr_,rp=angle(g)
 P=xi_x-rho
 dg=(-xi_x+k*P*invD2)*invD*invB
 ddg=(-2*xi_x*P-k+3*k*P*P*invD2)*invD*invD2*invB
 frr=4*xi_x*rr_*dg-2*k*(rp*dg*dg+rr_*ddg)
 jac=8*U*(1-U*U)/(1+U*U)**3
 return (frr*jac,)
def signed_angular(mesh,s,params,dom,outer=None):
 if outer is None:
  return integrate(lambda u,v,axis,n:rr(u,v,s,params,dom,(axis,),(n,)),mesh,ORDER)[0]
 def cb(u,v,axis,n):
  j=rr(u,v,s,params,dom,(axis,outer),(n,1))[0]
  return (Jet((n,),[j.coeff(k,1) for k in range(n+1)]),)
 return integrate(cb,mesh,ORDER)[0]
def s_error(mesh,interval,params,dom,outer=None):
 # 4th s jet, Simpson remainder L^5/2880 * 24 j4 = L^5*j4/120.
 # Cell×area range is applied ONLY to the nonnegative s remainder,
 # never directly to the signed spatial integrand/outer derivative.
 lo,hi=interval;tot=Q(0)
 for cell in mesh:
  if outer:
   j=rr(iv(cell.u),iv(cell.v),iv(interval),params,dom,("s",outer),(4,1))[0]
   a=mag(j.coeff(4,1))
  else:
   j=rr(iv(cell.u),iv(cell.v),iv(interval),params,dom,("s",),(4,))[0]
   a=mag(j.coeff(4))
  tot+=a*(cell.u[1]-cell.u[0])*(cell.v[1]-cell.v[0])
 return sym(tot*((hi-lo)**5)/120)
def h_signed(mesh,params,dom,outer=None):
 out=arb(0);errors=[]
 for i in range(4):
  lo,hi=Q(i,4),Q(i+1,4)
  for s,w in ((lo,Q(1,6)),((lo+hi)/2,Q(2,3)),(hi,Q(1,6))):
   val=signed_angular(mesh,arb(s),params,dom,outer)
   out+=val*arb((hi-lo)*w)
  e=s_error(mesh,(lo,hi),params,dom,outer)
  out+=e;errors.append(enc(e)["halfwidth"])
 return out,errors
def run(name):
 assert flint.__version__=="0.8.0"
 assert name in SPECIAL
 rbox,tbox,lbox=BOXES[name];start=time.perf_counter()
 cfg=Config(precision=128,order=ORDER,base_u=BU,base_v=BV,
            distance_ratio=RATIO,max_cells=40000,max_depth=28)
 with ctx.workprec(128):
  dom=Domain(rbox,lbox,Q(0),"equator")
  mesh=make_mesh(rbox,Q(0),cfg,lam=lbox)
  print("MESH",name,len(mesh),flush=True)
  point=tuple(map(arb,(midpoint(rbox),midpoint(tbox),midpoint(lbox))))
  full=tuple(iv(a) for a in (rbox,tbox,lbox))
  t=time.perf_counter();pc,pane=h_signed(mesh,point,dom)
  pcsecs=time.perf_counter()-t
  print("CENTER",name,enc(pc),flush=True)
  co=arb(0);dirs={}
  for box,axis in zip((rbox,tbox,lbox),("R","x","lam")):
   t=time.perf_counter();di,pane_d=h_signed(mesh,full,dom,axis)
   term=di*sym(radius(box));co+=term
   dirs[axis]={"signed_derivative_integral":enc(di),
               "halfwidth_contribution":enc(term),
               "s_remainder_panels":pane_d,
               "wall_s":time.perf_counter()-t}
   print("DERIV",name,axis,enc(term)["halfwidth"],flush=True)
  H=pc+co
  hlo,hhi=bounds(H);pv=enc(pc)["mid"]
  return {"status":STATUS,"name":name,"route":"rho2_integral_at_fixed_z",
   "input_box":{"R":list(map(str,rbox)),"tau":list(map(str,tbox)),
                 "lambda":list(map(str,lbox))},
   "H_interval":enc(H),"H_center_point":enc(pc),
   "normalized_halfwidth":enc(H)["halfwidth"]/abs(pv) if pv else None,
   "zero_included_RECORD_ONLY":bool(hlo<=0<=hhi),
   "H_outer_correction":enc(co),"directional_contributions":dirs,
   "center_s_remainders":pane,
   "mesh_cells":len(mesh),
   "mesh":{"order":ORDER,"base_u":BU,"base_v":BV,
           "ratio":str(RATIO),"kappa":"0","s_panels":4,
           "s_method":"Simpson with bounded fourth derivative"},
   "center_wall_s":pcsecs,"wall_s":time.perf_counter()-start,
   "peak_RSS_KiB":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
   "pinned_R3_commit":PIN,"global_C21_condition":"OPEN"}
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--name",required=True,choices=SPECIAL)
 p.add_argument("--output",required=True);a=p.parse_args()
 x=run(a.name)
 Path(a.output).write_text(json.dumps(x,indent=2)+"\n")
 print("RESULT",a.name,enc if False else x["H_interval"],flush=True)
if __name__=="__main__":main()
