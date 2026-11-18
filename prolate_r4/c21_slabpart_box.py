"""C21 H selected 1/4-wide partial slab: single-box producer.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Uses purely geometric MVT routing.
"""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
from flint import fmpq as Q
from .c21_slabpart_mvt import calculate,route,LAMBDA,STATUS,THRESH
def parseq(x):return Q(str(x))
def evaluate_box(name,R,T,L=LAMBDA):
 import flint
 assert flint.__version__=="0.8.0"
 assert Q(1,4)<=R[0]<R[1]<=Q(1,2)
 assert Q(0)<=T[0]<T[1]<=Q(1)
 assert L==LAMBDA
 rt=route(R,T)
 t=time.monotonic()
 if rt=="GENERAL":
  from . import c21_regular as reg
  reg.BU=16;reg.BV=32;reg.RATIO=Q(1,2);reg.ORDER=4
  reg.BOXES["SLAB_PART"]=(R,T,L)
  result=reg.run("SLAB_PART")
 else:
  result=calculate(name,R,T,L)
 result["name"]=name;result["route_from_position"]=rt
 result["area_R_tau"]=str((R[1]-R[0])*(T[1]-T[0]))
 result["lambda_slab"]=list(map(str,L))
 result["worker_elapsed_s"]=time.monotonic()-t
 result["producer_route_method"]=result["route"]
 result["status"]=STATUS
 result["global_coverage_asserted"]=False
 result["H_sign_not_used_to_select_route"]=True
 return result
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--id",required=True)
 p.add_argument("--R",nargs=2,required=True)
 p.add_argument("--tau",nargs=2,required=True)
 p.add_argument("--output",required=True)
 a=p.parse_args()
 R=tuple(map(parseq,a.R));T=tuple(map(parseq,a.tau))
 print(STATUS,flush=True)
 obj=evaluate_box(a.id,R,T)
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(obj,indent=2)+"\n")
 print("H_RESULT",a.id,obj["route_from_position"],
       obj["H_interval"]["lo"],obj["H_interval"]["hi"],
       obj["worker_elapsed_s"],flush=True)
if __name__=="__main__":main()
