"""C21 H second-order cost pilot, per-box signed Hessian-only mesh switch.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. No covering, no sign-based selection.
"""
from __future__ import annotations
import argparse,json,resource,time
from pathlib import Path
import flint
from flint import fmpq as Q,arb,ctx
from prolate_r1.density import Domain
from prolate_r1.jets import Jet
from prolate_r1.intervals import Config,midpoint,radius,sym,bounds
from prolate_r1.quadrature import make_mesh,integrate
from . import c21_second_order as so
from . import c21_cost_plan as plan
STATUS=plan.STATUS
def signed_integral(mesh,kernel,params,axes,directions,order):
 """Signed spatial Taylor; exterior mixed-jet coefficient integrated.
 Correctly multiplies second derivative diagonal by 2!.
 """
 if order==4:
  return so.integral(mesh,kernel,params,axes,directions)
 names=tuple(k for k,n in directions)
 powers=tuple(n for k,n in directions)
 mult=2 if len(directions)==1 and powers==(2,) else 1
 def cb(u,v,axis,n):
  vj=kernel(u,v,params,(axis,)+names,(n,)+powers)
  return (Jet((n,),[vj.coeff(k,*powers)*mult for k in range(n+1)]),)
 return integrate(cb,mesh,order)[0]
def get_hessian_mesh(R,T,L,setting,route,outer_boxes):
 cfg=Config(precision=128,order=setting["order"],
    base_u=setting["base_u"],base_v=setting["base_v"],
    distance_ratio=Q(setting["ratio"]),max_cells=40000,max_depth=28)
 if route=="GENERAL":
  return make_mesh(R,Q(0),cfg,lam=L)
 rbox,zbox,lbox=outer_boxes
 r_geom=rbox[1]+zbox[1]
 assert r_geom<1 and lbox==L
 return make_mesh((Q(0),r_geom),Q(0),cfg,lam=lbox)
def calculate(spec):
 assert flint.__version__=="0.8.0"
 assert spec["status"]==STATUS and not spec.get("is_cover")
 name=spec["id"];R=tuple(Q(x) for x in spec["R"])
 T=tuple(Q(x) for x in spec["tau"])
 L=tuple(Q(x) for x in spec["lambda"])
 assert Q(1,4)<=R[0]<R[1]<=Q(1,2)
 assert Q(0)<=T[0]<T[1]<=1
 assert Q(2)<=L[0]<L[1]<=Q(5)
 start=time.perf_counter()
 with ctx.workprec(128):
  st=time.perf_counter()
  route,axes,outer,base_mesh,kernel,extra=so.initialize(R,T,L)
  assert route==spec["route_expected"]
  base_mesh_setup=time.perf_counter()-st
  hess_setting=spec["hessian_mesh"]
  if hess_setting==plan.BASE_MESH:
   hess_mesh=base_mesh;hess_setup=0.0
  else:
   st=time.perf_counter()
   hess_mesh=get_hessian_mesh(R,T,L,hess_setting,route,outer)
   hess_setup=time.perf_counter()-st
  print("MESH",name,"route",route,"BASE",len(base_mesh),
        "HESS",len(hess_mesh),"hess_order",hess_setting["order"],flush=True)
  center=tuple(arb(midpoint(b)) for b in outer)
  full=tuple(so.iv(b) for b in outer)
  st=time.perf_counter()
  point_value=so.integral(base_mesh,kernel,center,axes,())
  point_sec=time.perf_counter()-st
  print("POINT",name,so.enc(point_value)["halfwidth"],point_sec,flush=True)
  grads={};hessian={}
  linear=arb(0);quadratic=arb(0)
  grad_seconds=0.;hess_seconds=0.
  for axis,b in zip(axes,outer):
   st=time.perf_counter()
   derivative=so.integral(base_mesh,kernel,center,axes,((axis,1),))
   term=derivative*sym(radius(b))
   sec=time.perf_counter()-st
   grad_seconds+=sec;linear+=term
   grads[axis]={"signed_derivative":so.enc(derivative),
       "correction":so.enc(term),"halfwidth_outer":str(radius(b)),
       "wall_s":sec}
   print("GRAD",name,axis,"halfwidth",so.enc(term)["halfwidth"],
         "seconds",sec,flush=True)
  for i,(axis,b) in enumerate(zip(axes,outer)):
   hi=radius(b)
   st=time.perf_counter()
   second=signed_integral(hess_mesh,kernel,full,axes,((axis,2),),hess_setting["order"])
   term=second*arb(0).union(arb(hi*hi))*arb(Q(1,2))
   sec=time.perf_counter()-st;hess_seconds+=sec;quadratic+=term
   hessian[axis+"_"+axis]={"signed_derivative":so.enc(second),
       "correction":so.enc(term),"factor":["0",str(hi*hi)],
       "type":"diagonal_half","wall_s":sec}
   print("HESS_DIAG",name,axis,"halfwidth",so.enc(term)["halfwidth"],
         "seconds",sec,flush=True)
   for j in range(i+1,len(outer)):
    other=axes[j];hj=radius(outer[j])
    st=time.perf_counter()
    mixed=signed_integral(hess_mesh,kernel,full,axes,((axis,1),(other,1)),
          hess_setting["order"])
    c=mixed*sym(hi*hj)
    sec=time.perf_counter()-st;hess_seconds+=sec;quadratic+=c
    hessian[axis+"_"+other]={"signed_derivative":so.enc(mixed),
      "correction":so.enc(c),"factor":[str(-hi*hj),str(hi*hj)],
      "type":"cross","wall_s":sec}
    print("HESS_CROSS",name,axis,other,"halfwidth",so.enc(c)["halfwidth"],
       "seconds",sec,flush=True)
  H=point_value+linear+quadratic
  lo,hi=bounds(H)
  result={"status":STATUS,"id":name,"group":spec["group"],
      "probe":spec["probe"],"experiment_input":spec,
      "input_box":{"R":list(map(str,R)),"tau":list(map(str,T)),
                   "lambda":list(map(str,L))},
      "outer_axes":list(axes),"actual_outer_boxes":{
         a:list(map(str,b)) for a,b in zip(axes,outer)},
      "geometric_halfwidths":{"h_R":str(radius(R)),
          "h_tau":str(radius(T)),"h_lambda":str(radius(L))},
      "route_from_position":route,"center_point":so.enc(point_value),
      "gradient":grads,"hessian":hessian,
      "linear_correction":so.enc(linear),
      "quadratic_correction":so.enc(quadratic),
      "H_interval":so.enc(H),
      "zero_included_RECORD_ONLY":bool(lo<=0<=hi),
      "base_mesh":{"base_u":16,"base_v":32,"ratio":"1/2","order":4,
         "cells":len(base_mesh)},
      "hessian_mesh":{**hess_setting,"cells":len(hess_mesh)},
      "timing":{"base_mesh_setup_s":base_mesh_setup,
         "hessian_mesh_setup_s":hess_setup,"point_s":point_sec,
         "gradient_sum_s":grad_seconds,"hessian_sum_s":hess_seconds,
         "total_worker_s":time.perf_counter()-start},
      "peak_RSS_KiB":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      "no_cover":True,"sign_does_not_control_method":True,
      "global_C21_condition":"OPEN",**extra}
  return result
def main():
 p=argparse.ArgumentParser();p.add_argument("--id",required=True)
 p.add_argument("--output",required=True);a=p.parse_args()
 doc=plan.frozen_write()
 spec=next((x for x in doc["jobs"] if x["id"]==a.id),None)
 if spec is None:raise RuntimeError("UNREGISTERED_EXPERIMENT")
 print(STATUS,flush=True)
 obj=calculate(spec)
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(obj,indent=2)+"\n")
 print("H_RESULT",obj["id"],obj["H_interval"],
        "worker_s",obj["timing"]["total_worker_s"],flush=True)
if __name__=="__main__":main()
