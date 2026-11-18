"""CORRECTED primitive E numerical reference; original physical pz=lambda*z.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Replaces wrong coordinate interpretation,
not the retained forensic numerical files.
"""
import json,time
from pathlib import Path
import mpmath as mp
from fractions import Fraction as F
from .c21_reference import BOXES,E_reference,STATUS,H,mpq
CASES=("G2","G35","EQ","CE","BD","AX","LW","STRIP_00","STRIP_08","STRIP_15")
OUT=Path("runs/2026-11-18/D_PRO_C21_H_PILOT")
def ref_one_corrected(name,n):
 Rbox,Tbox,Lbox=BOXES[name]
 R=mpq((Rbox[0]+Rbox[1])/2)
 tau=mpq((Tbox[0]+Tbox[1])/2)
 lam=mpq((Lbox[0]+Lbox[1])/2)
 rho=R*(1-tau*tau)/(1+tau*tau)
 z=R*(2*tau)/(1+tau*tau)
 original_pz=lam*z
 Es={k:E_reference(lam,rho+k*H,original_pz,n) for k in (-2,-1,0,1,2)}
 d1=(8*(Es[1]-Es[-1])-(Es[2]-Es[-2]))/(12*H)
 return {"E0":str(Es[0]),"H_center_num":str(d1/rho),
         "rho":str(rho),"normalized_z":str(z),
         "original_E_pz":str(original_pz),"lambda":str(lam)}
def check_interval(name,a,b,fine=False):
 key=name+("_cal_fine" if name=="LW" else "_cal_v2") if fine else name
 p=OUT/(key+".json")
 if not p.exists():return None
 j=json.loads(p.read_text())
 if "H_interval" not in j:return None
 lo=mpq(j["H_interval"]["lower"]);hi=mpq(j["H_interval"]["upper"])
 return bool(lo<=mp.mpf(a)<=hi and lo<=mp.mpf(b)<=hi)
def check_center_interval(name,a,b,fine=False):
 key=name+("_cal_fine" if name=="LW" else "_cal_v2") if fine else name
 p=OUT/(key+".json")
 if not p.exists():return None
 j=json.loads(p.read_text())
 field=j.get("center_point",j.get("H_center_point",None))
 if field is None:return None
 lo=mpq(field["lower"]);hi=mpq(field["upper"])
 return bool(lo<=mp.mpf(a)<=hi and lo<=mp.mpf(b)<=hi)
def run():
 mp.mp.dps=25
 result=[];start=time.monotonic()
 p=OUT/"primitive_E_hires_CORRECTED.json"
 for name in CASES:
  print("CORRECTED_START",name,flush=True)
  t=time.monotonic()
  a=ref_one_corrected(name,96)
  b=ref_one_corrected(name,160)
  h1=mp.mpf(a["H_center_num"]);h2=mp.mpf(b["H_center_num"])
  row={"box":name,"n96":a,"n160":b,
       "difference_96_160":str(abs(h1-h2)),
       "full_coarse_interval_contains_both":check_interval(name,h1,h2),
       "fine_interval_contains_both":check_interval(name,h1,h2,True),
       "coarse_center_point_contains_both":check_center_interval(name,h1,h2),
       "fine_center_point_contains_both":check_center_interval(name,h1,h2,True),
       "wall_s":time.monotonic()-t}
  result.append(row)
  p.write_text(json.dumps({"status":STATUS,"complete":False,
       "corrected_coordinate":"original p_z=lambda*z",
       "results":result,"uncomputed":CASES[len(result):]},indent=2)+"\n")
  print("CORRECTED_END",name,"H",b["H_center_num"],
        "centerfine",row["fine_center_point_contains_both"],flush=True)
 report={"status":STATUS,"complete":True,
   "corrected_coordinate":"original p_z=lambda*z",
   "reason":"R3 D² with lambda*(xi_z-z), primitive E pz is lambda*z",
   "retained_invalid_prior_files":["primitive_E_references.json","primitive_E_hires.json"],
   "precision_digits":25,"quadrature":[96,160],"stencil":"five-point rho, h=0.004",
   "results":result,"elapsed_seconds":time.monotonic()-start,
   "rigorous_numeric_error":False}
 p.write_text(json.dumps(report,indent=2)+"\n")
 print("CORRECTED_FINISH",len(result),flush=True)
if __name__=="__main__":run()
