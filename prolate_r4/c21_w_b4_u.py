"""W B4 auxiliary U contact-coordinate variant.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Pre-registered FIXED_W_U_VARIANT.md.
No W signed coefficient cubature or full-box inference.
"""
import argparse,itertools,json,time,resource
from pathlib import Path
from flint import fmpq as Q,ctx
from . import c21_w_b4_axisdepth as X
from . import v35_w_split_preflight as V
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
U=(Q(0),Q(1,64),Q(1,32),Q(1,16),Q(1,8),Q(1,4),Q(1,2),Q(1))
VV=(Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1))
WW=(Q(0),Q(1,16),Q(1,8),Q(1,4),Q(1,2),Q(1))
def h(u):return 1-8*u*u/(1+u*u)**2
def to_h(cell):
 u,v,w=cell
 return ((h(u[1]),h(u[0])),v,w)
def init_u():
 return [(tuple((p[k],p[k+1]) for p,k in zip((U,VV,WW),idx)),(0,0,0))
   for idx in itertools.product(range(len(U)-1),range(len(VV)-1),range(len(WW)-1))]
def measure_u(cell):
 p=to_h(cell)
 return (p[0][1]-p[0][0])*(p[1][1]-p[1][0])*(p[2][1]-p[2][0])/2
def split_u(cell,counts):
 allowed=[i for i in range(3) if counts[i]<16]
 if not allowed:return None
 ax=max(allowed,key=lambda i:cell[i][1]-cell[i][0])
 a,b=cell[ax];mid=(a+b)/2;out=[]
 for item in ((a,mid),(mid,b)):
  cp=list(cell);cp[ax]=item
  dd=list(counts);dd[ax]+=1
  out.append((tuple(cp),tuple(dd)))
 return out,ax
def run(path):
 ctx.prec=128
 # v35 majorant only reads a rectangular h,v,w enclosure; exact
 # monotone rational mapping u -> h ensures rigorous coverage.
 original=X.M.majorant
 X.M.majorant=lambda cell:original(to_h(cell))
 X.init=init_u;X.measure=measure_u;X.divide=split_u
 began=time.monotonic();results=[]
 for i,j in itertools.product(range(2),repeat=2):
  print("START_U",i,j,flush=True)
  obj=X.run_child(i,j);results.append(obj)
  print("DONE_U",i,j,obj["rigorous_full_B4_cover"],
        obj["stop_reason"],obj["partial_accepted_patches"],flush=True)
 report={"status":STATUS,"variant":"U_CONTACT_COORDINATE",
         "V36_input":"16d8c01b86327b8387f731bf09d1740c6ee31273",
         "fixed_plan":"FIXED_W_U_VARIANT.md",
         "u_breakpoints":list(map(str,U)),
         "all_four_full_B4_cover":all(x["rigorous_full_B4_cover"] for x in results),
         "children":results,"W_35_coefficients_computed":False,
         "W_box2_enclosure":None,
         "wall_s":time.monotonic()-began,
         "peak_RSS_KiB":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 Path(path).write_text(json.dumps(report,indent=2)+"\n")
 print("FINAL_U",report["all_four_full_B4_cover"],flush=True)
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True)
 z=p.parse_args();run(z.output)
