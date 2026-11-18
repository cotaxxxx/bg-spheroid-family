"""One box of the λ=[79/16,5] C21 H second-order heavy slab.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Exact frozen geometry route, signed Taylor.
"""
from __future__ import annotations
import argparse,json,resource,time
from pathlib import Path
import flint
from flint import arb,fmpq as Q,ctx
from prolate_r1.density import Domain
from prolate_r1.intervals import Config,midpoint,radius,sym,bounds
from prolate_r1.quadrature import make_mesh
from . import c21_regular as reg
from . import c21_slabpart_mvt as mvt
from . import c21_second_order as so
from .c21_cost_box import signed_integral
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
L=(Q(79,16),Q(5))
KAP=Q(1,4096)
PREC=128
BASE={"base_u":16,"base_v":32,"ratio":"1/2","order":4}
HESS={"base_u":8,"base_v":16,"ratio":"1","order":4}
def route(R,T):
 if T[1]==Q(1):return "AXIS_MVT"
 if R[0]==Q(0):return "CENTER_MVT"
 if R[1]==Q(1):return "BOUNDARY_COLLAR"
 return "GENERAL"
def mk_mesh(geo,cap,setup):
 cfg=Config(precision=PREC,order=setup["order"],
   base_u=setup["base_u"],base_v=setup["base_v"],
   distance_ratio=Q(setup["ratio"]),max_cells=40000,max_depth=28)
 return make_mesh(geo,cap,cfg,lam=L)
def configure(R,T):
 rt=route(R,T)
 if rt in ("AXIS_MVT","CENTER_MVT"):
  outer=mvt.extended(R,T,L)
  rho,z,lbox=outer
  geom=rho[1]+z[1]
  if rt=="AXIS_MVT" and rho[1]>mvt.THRESH:
   raise ArithmeticError("OPEN: AXIS_MVT rho_hi > fixed 1/16 threshold")
  assert geom<1,"OPEN: MVT positive distance bound unavailable"
  chart=midpoint(T)
  dom=Domain((Q(0),geom),L,Q(0),"equator")
  axes=("rho","z","lam")
  def kernel(u,v,params,active,orders):
   return mvt.density_rr(u,v,params,dom,chart,active,orders)[0]
  info={"route":rt,"rhohi_plus_zhi":str(geom),
        "chart_tau":str(chart),
        "kernel":"MVT independent rho_prime,z,lambda"}
  return rt,outer,axes,dom.R,Q(0),kernel,arb(0),info
 cap=KAP if rt=="BOUNDARY_COLLAR" else Q(0)
 dom=Domain(R,L,cap,"equator")
 axes=("R","x","lam")
 outer=(R,T,L)
 def kernel(u,v,params,active,orders):
  return reg.dens(u,v,params,dom,T,active,orders)[0]
 cap_error=reg.cap_bound(R,T,L) if cap else arb(0)
 info={"route":rt,"kappa":str(cap),
   "kernel":"capped_direct_H" if cap else "uncapped_direct_H",
   "cap_error_source":"uniform_f_rho_cap_bound" if cap else "NONE"}
 return rt,outer,axes,R,cap,kernel,cap_error,info
def compute(name,R,T):
 assert flint.__version__=="0.8.0"
 assert Q(0)<=R[0]<R[1]<=1
 assert Q(0)<=T[0]<T[1]<=1
 t0=time.perf_counter()
 with ctx.workprec(PREC):
  rt,outer,axes,geo,cap,kernel,caperror,info=configure(R,T)
  t=time.perf_counter()
  bm=mk_mesh(geo,cap,BASE)
  base_setup=time.perf_counter()-t
  t=time.perf_counter()
  hm=mk_mesh(geo,cap,HESS)
  hess_setup=time.perf_counter()-t
  print("MESH",name,"route",rt,"base",len(bm),"hess",len(hm),flush=True)
  point=tuple(arb(midpoint(b)) for b in outer)
  full=tuple(reg.iv(b) for b in outer)
  t=time.perf_counter()
  p=so.integral(bm,kernel,point,axes,())
  secp=time.perf_counter()-t
  print("POINT",name,reg.enc(p)["halfwidth"],"seconds",secp,flush=True)
  linear=arb(0);quadratic=arb(0);grads={};hess={}
  tgrad=0.0;thess=0.0
  for axis,box in zip(axes,outer):
   t=time.perf_counter()
   g=so.integral(bm,kernel,point,axes,((axis,1),))
   corr=g*sym(radius(box))
   sec=time.perf_counter()-t
   linear+=corr;tgrad+=sec
   grads[axis]={"interval":reg.enc(g),"correction":reg.enc(corr),
       "outer_halfwidth":str(radius(box)),"wall_s":sec}
   print("GRAD",name,axis,reg.enc(corr)["halfwidth"],"seconds",sec,flush=True)
  for i,axis in enumerate(axes):
   hi=radius(outer[i])
   t=time.perf_counter()
   hii=signed_integral(hm,kernel,full,axes,((axis,2),),4)
   term=hii*arb(0).union(arb(hi*hi))*arb(Q(1,2))
   sec=time.perf_counter()-t
   quadratic+=term;thess+=sec
   hess[axis+"_"+axis]={"interval":reg.enc(hii),
     "correction":reg.enc(term),"type":"diagonal_half",
     "factor":["0",str(hi*hi)],"wall_s":sec}
   print("HESS_DIAG",name,axis,reg.enc(term)["halfwidth"],"seconds",sec,flush=True)
   for j in range(i+1,3):
    ax2=axes[j];hj=radius(outer[j])
    t=time.perf_counter()
    hij=signed_integral(hm,kernel,full,axes,((axis,1),(ax2,1)),4)
    term=hij*sym(hi*hj)
    sec=time.perf_counter()-t
    quadratic+=term;thess+=sec
    hess[axis+"_"+ax2]={"interval":reg.enc(hij),
      "correction":reg.enc(term),"type":"cross",
      "factor":[str(-hi*hj),str(hi*hj)],"wall_s":sec}
    print("HESS_CROSS",name,axis,ax2,reg.enc(term)["halfwidth"],"seconds",sec,flush=True)
  H=p+linear+quadratic+caperror
  lo,hi=bounds(H)
  return {"status":STATUS,"id":name,"route_from_position":rt,
   "input_box":{"R":list(map(str,R)),"tau":list(map(str,T)),
                "lambda":list(map(str,L))},
   "outer_axes":list(axes),"outer_boxes":{
      a:list(map(str,b)) for a,b in zip(axes,outer)},
   "center_point":reg.enc(p),"gradient":grads,"hessian":hess,
   "linear_correction":reg.enc(linear),
   "quadratic_correction":reg.enc(quadratic),
   "boundary_cap_correction":reg.enc(caperror),
   "H_interval":reg.enc(H),
   "zero_included_RECORD_ONLY":bool(lo<=0<=hi),
   "base_mesh":{**BASE,"cells":len(bm),"setup_wall_s":base_setup},
   "hessian_mesh":{**HESS,"cells":len(hm),"setup_wall_s":hess_setup},
   "timing":{"point_s":secp,"gradient_sum_s":tgrad,
             "hessian_sum_s":thess,
             "total_worker_s":time.perf_counter()-t0},
   "peak_RSS_KiB":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
   "route_info":info,"global_C21_condition":"OPEN",
   "is_diagnostic_only":True,"no_unsigned_zero_order":True}
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--id",required=True)
 parser.add_argument("--R",nargs=2,required=True)
 parser.add_argument("--tau",nargs=2,required=True)
 parser.add_argument("--output",required=True)
 a=parser.parse_args()
 R=tuple(Q(x) for x in a.R);T=tuple(Q(x) for x in a.tau)
 print(STATUS,flush=True)
 d=compute(a.id,R,T)
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(d,indent=2)+"\n")
 print("H_RESULT",a.id,d["H_interval"],"seconds",d["timing"]["total_worker_s"],flush=True)
if __name__=="__main__":main()
