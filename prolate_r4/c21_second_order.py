"""C21 H second-order OUTER Taylor box enclosure.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Exact frozen H spatial kernels.
No zero-order UNSIGNED angular integration is used for a signed term.
"""
from __future__ import annotations
import argparse,json,resource,time
from pathlib import Path
from flint import arb,fmpq as Q,ctx
import flint
from prolate_r1.density import Domain
from prolate_r1.jets import Jet
from prolate_r1.intervals import Config,bounds,midpoint,radius,sym
from prolate_r1.quadrature import make_mesh,integrate
from . import c21_regular as reg
from . import c21_slabpart_mvt as mvt
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
PREC=128;ORDER=4;BU=16;BV=32;RATIO=Q(1,2)
LAMBDA=(Q(1279,256),Q(5))
def enc(x):
 return reg.enc(x)
def iv(p):
 return reg.iv(p)
def initialize(R,T,L=LAMBDA):
 rt=mvt.route(R,T)
 cfg=Config(precision=PREC,order=ORDER,base_u=BU,base_v=BV,
     distance_ratio=RATIO,max_cells=40000,max_depth=28)
 if rt=="GENERAL":
  # Integral kernel: original direct f_rho/rho, no change.
  dom=Domain(R,L,Q(0),"equator")
  mesh=make_mesh(R,Q(0),cfg,lam=L)
  axes=("R","x","lam")
  full_boxes=(R,T,L)
  def kernel(u,v,params,active,orders):
   return reg.dens(u,v,params,dom,T,active,orders)[0]
  extra={"angular_distance_mode":"original_C21_regular",
         "outer_parameters":"R,tau,lambda","kappa":"0"}
 else:
  # The MVT replacement computes a FULL independent Cartesian extension.
  full_boxes=mvt.extended(R,T,L)
  rbox,zbox,lbox=full_boxes
  rhplusz=rbox[1]+zbox[1]
  assert rhplusz<1,"MVT requires positive 1-(rho_hi+z_hi)"
  if rt=="AXIS_MVT" and rbox[1]>mvt.THRESH:
   raise ArithmeticError("OPEN: AXIS MVT rho_hi > frozen threshold")
  dom=Domain((Q(0),rhplusz),lbox,Q(0),"equator")
  chart=midpoint(T)
  mesh=make_mesh(dom.R,Q(0),cfg,lam=lbox)
  axes=("rho","z","lam")
  def kernel(u,v,params,active,orders):
   return mvt.density_rr(u,v,params,dom,chart,active,orders)[0]
  extra={"angular_distance_mode":"independent_MVT_positive_rgeom_bound",
         "outer_parameters":"rho_prime,z,lambda","rhohi_plus_zhi":str(rhplusz),
         "fixed_angle_chart_tau":str(chart),"kappa":"0",
         "s_quadrature":"NONE_RANGE_MVT"}
 return rt,axes,full_boxes,mesh,kernel,extra

def integral(mesh,fn,params,axnames,directions):
 """Signed spatial Taylor integral of arbitrary external jet coefficient.
 directions: tuple of (outer_name, derivative_order) for n=1,2 only.
 Every callback's n-th spatial coeff is signed Taylor-integrated by R3.
 """
 dirs=tuple(directions)
 powers=tuple(k for _,k in dirs)
 names=tuple(a for a,_ in dirs)
 mult=2 if len(dirs)==1 and dirs[0][1]==2 else 1
 def cb(u,v,axis,n):
  j=fn(u,v,params,(axis,)+names,(n,)+powers)
  coefficients=[j.coeff(k,*powers)*mult for k in range(n+1)]
  return (Jet((n,),coefficients),)
 return integrate(cb,mesh,ORDER)[0]

def calculate(name,R,T,L=LAMBDA):
 assert flint.__version__=="0.8.0"
 assert R[0]>=Q(1,4) and R[1]<=Q(1,2)
 assert T[0]>=0 and T[1]<=1 and L==LAMBDA
 start=time.perf_counter()
 with ctx.workprec(PREC):
  rt,axes,boxes,mesh,kernel,extra=initialize(R,T,L)
  print("MESH",name,len(mesh),"route",rt,flush=True)
  point=tuple(arb(midpoint(b)) for b in boxes)
  full=tuple(iv(b) for b in boxes)
  t=time.perf_counter()
  value=integral(mesh,kernel,point,axes,())
  sec=time.perf_counter()-t
  print("POINT",name,enc(value),"wall_s",sec,flush=True)
  grad_terms=[];grad={};hessian={}
  linear=arb(0);quadratic=arb(0)
  for i,(axis,box) in enumerate(zip(axes,boxes)):
   h=radius(box)
   t=time.perf_counter()
   # Crucial: point params, never ball params for first derivative.
   derivative=integral(mesh,kernel,point,axes,((axis,1),))
   term=derivative*sym(h)
   linear+=term
   grad[axis]={"interval":enc(derivative),"correction":enc(term),
     "outer_halfwidth":str(h),"wall_s":time.perf_counter()-t}
   print("GRAD",name,axis,"width",enc(term)["halfwidth"],
         "seconds",grad[axis]["wall_s"],flush=True)
  for i,(axis,box) in enumerate(zip(axes,boxes)):
   h=radius(box)
   t=time.perf_counter()
   d=integral(mesh,kernel,full,axes,((axis,2),))
   # Symmetric Hessian diagonal multiplied by 1/2 s_i²;
   # [0,h²] is nonnegative, not [-h²,h²].
   tdiag=d*arb(0).union(arb(h*h))*arb(Q(1,2))
   quadratic+=tdiag
   hessian[axis+"_"+axis]={"interval":enc(d),
      "correction":enc(tdiag),"factor_interval":["0",str(h*h)],
      "type":"diagonal_half","wall_s":time.perf_counter()-t}
   print("HESS_DIAG",name,axis,enc(tdiag)["halfwidth"],
         "seconds",hessian[axis+"_"+axis]["wall_s"],flush=True)
   for j in range(i+1,len(axes)):
    axis2=axes[j];h2=radius(boxes[j])
    t=time.perf_counter()
    mix=integral(mesh,kernel,full,axes,((axis,1),(axis2,1)))
    tcross=mix*sym(h*h2)
    quadratic+=tcross
    hessian[axis+"_"+axis2]={"interval":enc(mix),
       "correction":enc(tcross),"factor_interval":[str(-h*h2),str(h*h2)],
       "type":"cross","wall_s":time.perf_counter()-t}
    print("HESS_CROSS",name,axis,axis2,enc(tcross)["halfwidth"],
          "seconds",hessian[axis+"_"+axis2]["wall_s"],flush=True)
  H=value+linear+quadratic
  lo,hi=bounds(H)
  return {"status":STATUS,"name":name,"route_from_position":rt,
    "outer_axes":list(axes),
    "input_box":{"R":list(map(str,R)),"tau":list(map(str,T)),
          "lambda":list(map(str,L))},
    "actual_outer_boxes":{axis:list(map(str,b))
            for axis,b in zip(axes,boxes)},
    "center_point":enc(value),"gradient":grad,
    "hessian":hessian,"linear_correction":enc(linear),
    "quadratic_correction":enc(quadratic),
    "H_interval":enc(H),"zero_included_RECORD_ONLY":bool(lo<=0<=hi),
    "mesh_cells":len(mesh),"mesh":{"order":ORDER,"base_u":BU,
         "base_v":BV,"distance_ratio":str(RATIO),
         "precision":PREC},"point_wall_s":sec,
    "wall_s":time.perf_counter()-start,
    "peak_RSS_KiB":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    "implementation_note":"all angular derivatives integrate signed order4",
    "global_C21_condition":"OPEN",**extra}

def main():
 p=argparse.ArgumentParser();p.add_argument("--id",required=True)
 p.add_argument("--R",nargs=2,required=True)
 p.add_argument("--tau",nargs=2,required=True)
 p.add_argument("--output",required=True)
 a=p.parse_args()
 R=tuple(Q(x) for x in a.R);T=tuple(Q(x) for x in a.tau)
 print(STATUS,flush=True)
 d=calculate(a.id,R,T)
 o=Path(a.output);o.parent.mkdir(parents=True,exist_ok=True)
 o.write_text(json.dumps(d,indent=2)+"\n")
 print("RESULT",a.id,d["H_interval"],flush=True)
if __name__=="__main__":main()
