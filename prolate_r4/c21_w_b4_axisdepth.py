"""W B4 gate: per-axis depth<=16, V35 (a) four children.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. NONNEGATIVE tail only; no W coefficient run.
Plan fixed before execution in FIXED_PLAN.md.
"""
import argparse,itertools,json,time,resource,sys
from pathlib import Path
# The pinned v3 majorant has top-level imports; resolve it within this
# new isolated worktree without copying or editing upstream files.
sys.path.insert(0,str(Path(__file__).resolve().parent))
from flint import fmpq as Q,ctx
from . import v35_w_split_preflight as V
from . import v35_w_b4_cover as C
import majorant as M
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
CAPS=(16,16,16);MAXLEAVES=32768;TIMELIMIT=60.0
ALIMIT=Q(1,4);BUDGET=Q(3,100)
def init():
 return [(tuple((p[i],p[i+1]) for p,i in zip((C.H,C.VV,C.WW),indices)),(0,0,0))
          for indices in itertools.product(range(len(C.H)-1),range(len(C.VV)-1),range(len(C.WW)-1))]
def measure(cell):
 m=Q(1,2)
 for a,b in cell:m*=b-a
 return m
def divide(cell,depths):
 candidates=[i for i in range(3) if depths[i]<CAPS[i]]
 if not candidates:return None
 ax=max(candidates,key=lambda i:(cell[i][1]-cell[i][0])/(Q(2) if i==0 else Q(1)))
 lo,hi=cell[ax];mid=(lo+hi)/2
 children=[]
 for ends in ((lo,mid),(mid,hi)):
  pp=list(cell);pp[ax]=ends
  dd=list(depths);dd[ax]+=1
  children.append((tuple(pp),tuple(dd)))
 return children,ax
def run_child(i,j):
 ctx.prec=128
 outer=V.configure(V.RBOUNDS[i],V.TBOUNDS[j])
 pending=init();accepted=[];valsum=Q(0)
 start=time.monotonic();checked=0;splitA=0;splitTail=0
 reason=None
 while True:
  if time.monotonic()-start >= TIMELIMIT:reason="TIME_LIMIT";break
  if len(pending)+len(accepted)>MAXLEAVES:reason="LEAF_LIMIT";break
  if pending:
   cell,counts=pending.pop()
   m=M.majorant(cell);checked+=1
   if not m["convergent"] or m["A"]>ALIMIT:
    part=divide(cell,counts)
    if part is None:reason="AXIS_DEPTH_LIMIT_A";break
    children,ax=part
    pending.extend(children);splitA+=1;continue
   x=measure(cell)*m["tail_upper"]
   accepted.append((x,cell,counts,m["A"]));valsum+=x
  else:
   if valsum<=BUDGET:break
   which=max(range(len(accepted)),key=lambda k:accepted[k][0])
   x,cell,counts,a=accepted.pop(which);valsum-=x
   part=divide(cell,counts)
   if part is None:reason="AXIS_DEPTH_LIMIT_TAIL";break
   children,ax=part
   pending.extend(children);splitTail+=1
 completed=(not pending and reason is None and valsum<=BUDGET)
 if completed:
  assert sum((measure(cell) for _,cell,_,_ in accepted),Q(0))==1
  assert all(a<=ALIMIT for _,_,_,a in accepted)
 return {"status":STATUS,"child":[i,j],**outer,
   "rigorous_full_B4_cover":bool(completed),
   "B4_upper_if_complete":str(valsum) if completed else None,
   "max_A_accepted_if_complete":str(max((a for _,_,_,a in accepted),default=Q(0))) if completed else None,
   "partial_B4_currently_accepted_NOT_GLOBAL":str(valsum),
   "partial_accepted_patches":len(accepted),"pending":len(pending),
   "evaluations":checked,"A_splits":splitA,"tail_splits":splitTail,
   "stop_reason":reason,"wall_s":time.monotonic()-start,
   "no_signed_W_coefficients":True}
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",required=True)
 a=p.parse_args()
 begin=time.monotonic();allres=[]
 for i,j in itertools.product(range(2),repeat=2):
  print("START",i,j,flush=True)
  z=run_child(i,j);allres.append(z)
  print("FINISH",i,j,z["rigorous_full_B4_cover"],z["stop_reason"],z["partial_accepted_patches"],round(z["wall_s"],3),flush=True)
 result={"status":STATUS,"route":"C21 auxiliary W four-child B4-only gate",
         "V36_input":"16d8c01b86327b8387f731bf09d1740c6ee31273",
         "fixed_A":"1/4","fixed_B4_budget_per_child":"3/100",
         "per_axis_split_depth":list(CAPS),"max_leaves":MAXLEAVES,
         "per_child_timeout_s":TIMELIMIT,
         "all_four_full_B4_cover":all(z["rigorous_full_B4_cover"] for z in allres),
         "children":allres,"W_35_coefficients_computed":False,
         "W_box_enclosure":None,"wall_s":time.monotonic()-begin,
         "peak_RSS_KiB":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 Path(a.output).write_text(json.dumps(result,indent=2)+"\n")
 print("DONE complete",result["all_four_full_B4_cover"],flush=True)
if __name__=="__main__":main()
