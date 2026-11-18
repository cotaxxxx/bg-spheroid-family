"""Pre-fixed high-resolution primitive E references; 25-digit 96² and160².
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Not a rigorous integration oracle.
"""
import json,time,mpmath as mp
from pathlib import Path
from .c21_reference import ref_one,STATUS,mpq
NAMES=("G2","G35","EQ","CE","BD","AX","LW","STRIP_00","STRIP_08","STRIP_15")
OUT=Path("runs/2026-11-18/D_PRO_C21_H_PILOT")
def inside(name,a,b,fine=False):
 p=OUT/(name+("_cal_v2" if fine else "")+".json")
 if not p.exists():return None
 j=json.loads(p.read_text())
 if "H_interval" not in j:return None
 q=j["H_interval"];lo=mpq(q["lower"]);hi=mpq(q["upper"])
 return bool(lo<=mp.mpf(a)<=hi and lo<=mp.mpf(b)<=hi)
def run():
 mp.mp.dps=25;results=[];start=time.monotonic()
 p=OUT/"primitive_E_hires.json"
 for i,name in enumerate(NAMES):
  t=time.monotonic();print("START_HIRES",name,flush=True)
  a=ref_one(name,96);b=ref_one(name,160)
  av=mp.mpf(a["H_center_num"]);bv=mp.mpf(b["H_center_num"])
  row={"name":name,"n96":a,"n160":b,
       "quadrature_absolute_difference":str(abs(av-bv)),
       "coarse_interval_contains_both":inside(name,av,bv),
       "fine_interval_contains_both":inside(name,av,bv,True),
       "elapsed_s":time.monotonic()-t,
       "reference_is_nonrigorous":True}
  results.append(row)
  p.write_text(json.dumps({"status":STATUS,"complete":False,
       "results":results,"uncomputed":NAMES[len(results):]},indent=2)+"\n")
  print("END_HIRES",name,b["H_center_num"],row["quadrature_absolute_difference"],flush=True)
 obj={"status":STATUS,"complete":True,"reference":"primitive E 25d two grids",
      "n1":96,"n2":160,"stencil_step":"0.004","all":results,
      "overall_s":time.monotonic()-start,
      "rigorous_error_claim":False}
 p.write_text(json.dumps(obj,indent=2)+"\n")
 print("FINISHED",len(results),flush=True)
if __name__=="__main__":run()
