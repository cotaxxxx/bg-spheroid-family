"""One D-PRO C21 H slab box at frozen fine-calibration settings.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Only rho derivatives; never z derivatives.

The separate 12-worker controller determines the route from box POSITION.
This module owns only one worker's interval computation and JSON.
"""
from __future__ import annotations
import argparse,json,resource,time
from pathlib import Path
from flint import fmpq as Q
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
LAMBDA=(Q(1279,256),Q(5))
def parseq(s):
 return Q(str(s))
def route(R,T):
 # Mandatory precedence: axis, center, boundary collar, regular.
 if T[1]==1:return "AXIS"
 if R[0]==0:return "CENTER"
 if R[1]==1:return "BOUNDARY"
 return "REGULAR"
def evaluate_box(name,R,T,L=LAMBDA):
 import flint
 from . import c21_regular as reg, c21_special as sp
 assert flint.__version__=="0.8.0"
 assert 0<=R[0]<R[1]<=1 and 0<=T[0]<T[1]<=1
 assert L==LAMBDA,"the lambda slab must never be subdivided"
 r=route(R,T);t0=time.monotonic()
 # Geometry at R=1 and tau=1 is a double contact case; the current
 # f_rho_rho regularizer requires R_hi<1, and no valid axis cap bound
 # has been implemented. Never pretend an interval was computed.
 if r=="AXIS" and R[1]==1:
  raise ArithmeticError("OPEN_UNSUPPORTED_AXIS_BOUNDARY: no uniform s rho2 cap estimate")
 if r in ("AXIS","CENTER"):
  sp.BU=16;sp.BV=32;sp.RATIO=Q(1,2);sp.ORDER=4
  sp.BOXES["SLAB_DYN"]=(R,T,L)
  sp.SPECIAL=(*sp.SPECIAL,"SLAB_DYN")
  j=sp.run("SLAB_DYN")
 else:
  reg.BU=16;reg.BV=32;reg.RATIO=Q(1,2);reg.ORDER=4
  reg.BOXES["SLAB_DYN"]=(R,T,L)
  j=reg.run("SLAB_DYN")
 j["name"]=name;j["route_from_position"]=r
 j["area_R_tau"]=str((R[1]-R[0])*(T[1]-T[0]))
 j["lambda_slab"]=list(map(str,L))
 j["worker_elapsed_s"]=time.monotonic()-t0
 j["producer_route_method"]=j["route"]
 j["status"]=STATUS
 j["global_coverage_asserted"]=False
 j["sign_used_only_for_binary_zero_inclusion"]=True
 return j
def main():
 pa=argparse.ArgumentParser()
 pa.add_argument("--id",required=True)
 pa.add_argument("--R",nargs=2,required=True)
 pa.add_argument("--tau",nargs=2,required=True)
 pa.add_argument("--output",required=True)
 args=pa.parse_args()
 R=tuple(map(parseq,args.R));T=tuple(map(parseq,args.tau))
 result=evaluate_box(args.id,R,T)
 path=Path(args.output)
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(result,indent=2)+"\n")
 print("H_RESULT",args.id,result["route_from_position"],
       result["H_interval"]["lo"],result["H_interval"]["hi"],
       result["worker_elapsed_s"],flush=True)
if __name__=="__main__":main()
