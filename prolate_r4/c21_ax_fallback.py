"""AX fallback: signed angular Taylor, exact interval s in [0,1].
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Separate from timed-out Simpson run.
"""
import argparse,json,time,resource
from pathlib import Path
from flint import arb,fmpq as Q,ctx
from prolate_r1.density import Domain
from prolate_r1.intervals import Config,midpoint,radius,sym,bounds
from prolate_r1.quadrature import make_mesh
from .c21_regular import enc,iv,ORDER,BU,BV,RATIO,STATUS
from .c21_special import signed_angular,BOXES
def run():
 name="AX_RANGE_S";rbox,tbox,lbox=BOXES["AX"];start=time.perf_counter()
 cfg=Config(precision=128,order=ORDER,base_u=BU,base_v=BV,
    distance_ratio=RATIO,max_cells=40000,max_depth=28)
 with ctx.workprec(128):
  dom=Domain(rbox,lbox,Q(0),"equator")
  mesh=make_mesh(rbox,Q(0),cfg,lam=lbox)
  p=tuple(map(arb,(midpoint(rbox),midpoint(tbox),midpoint(lbox))))
  full=tuple(iv(a) for a in (rbox,tbox,lbox))
  s=iv((Q(0),Q(1)))
  print("MESH",name,len(mesh),flush=True)
  t=time.perf_counter();center=signed_angular(mesh,s,p,dom)
  ps=time.perf_counter()-t
  print("CENTER",enc(center),flush=True)
  corr=arb(0);dirs={}
  for a,axis in zip((rbox,tbox,lbox),("R","x","lam")):
   t=time.perf_counter()
   d=signed_angular(mesh,s,full,dom,axis)
   term=d*sym(radius(a));corr+=term
   dirs[axis]={"signed_derivative_interval":enc(d),
      "outer_halfwidth_contribution":enc(term),"time_s":time.perf_counter()-t}
   print("DERIV",axis,enc(term)["halfwidth"],flush=True)
  H=center+corr;lo,hi=bounds(H)
  obj={"status":STATUS,"name":name,"route":"rho2_s_uniform_range_with_signed_angular_Taylor",
   "box":{"R":list(map(str,rbox)),"tau":list(map(str,tbox)),
          "lambda":list(map(str,lbox))},
   "H_interval":enc(H),"H_center_point":enc(center),
   "normalized_halfwidth":enc(H)["halfwidth"]/abs(enc(center)["mid"]) if enc(center)["mid"] else None,
   "contains_zero_RECORD_ONLY":lo<=0<=hi,
   "directional_contributions":dirs,
   "spatial_cells":len(mesh),"order":4,"base_u":8,"base_v":16,
   "ratio":"2","s_interval":"[0,1]",
   "wall_s":time.perf_counter()-start,"center_s":ps,
   "peak_RSS_KiB":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
   "note":"not the original AX Simpson result; original AX remains OPEN",
   "global_condition":"OPEN"}
  return obj
if __name__=="__main__":
 pa=argparse.ArgumentParser();pa.add_argument("--output",required=True)
 a=pa.parse_args()
 j=run()
 Path(a.output).write_text(json.dumps(j,indent=2)+"\n")
 print("RESULT",j["H_interval"],flush=True)
