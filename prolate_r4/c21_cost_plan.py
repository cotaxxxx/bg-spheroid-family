"""Frozen C21 H cost-trim experiment registry.
DIAGNOSTIC_ONLY / NOT_EVIDENCE; only costs, never coverage.
"""
from __future__ import annotations
import json
from pathlib import Path
from fractions import Fraction as F
from flint import fmpq as Q
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"runs/2026-11-18/D_PRO_C21_H_COST_TRIM"
BASE=ROOT/"runs/2026-11-18/D_PRO_C21_H_SECOND_ORDER/STAGE_B/boxes"
PROBES={
 "P1":{"R":["1/4","17/64"],"tau":["0","1/64"],"route":"GENERAL","baseline":"R16_T00"},
 "P2":{"R":["13/32","27/64"],"tau":["0","1/64"],"route":"GENERAL","baseline":"R26_T00"},
 "P3":{"R":["1/4","17/64"],"tau":["63/64","1"],"route":"AXIS_MVT","baseline":"R16_T63"},
 "P4":{"R":["7/16","29/64"],"tau":["63/64","1"],"route":"AXIS_MVT","baseline":"R28_T63"}
}
BASE_MESH={"base_u":16,"base_v":32,"ratio":"1/2","order":4}
COARSE_MESHES=(("H8x16_O4",{"base_u":8,"base_v":16,"ratio":"1","order":4}),
               ("H8x16_O2",{"base_u":8,"base_v":16,"ratio":"1","order":2}))
CAPS={"GENERAL":1800,"AXIS_MVT":2400}
BUDGET=7200
MAX_WORKERS=12
def case(name,group,probe,R,T,L,hess=BASE_MESH):
 return {"id":name,"group":group,"probe":probe,
   "R":R,"tau":T,"lambda":L,
   "hessian_mesh":dict(hess),"point_grad_mesh":dict(BASE_MESH),
   "route_expected":PROBES[probe]["route"],
   "per_box_limit_s":CAPS[PROBES[probe]["route"]],
   "status":STATUS}
def plan():
 experiments=[]
 for den in (16,8,4):
  lo=str(F(5)-F(1,den))
  for p,v in PROBES.items():
   experiments.append(case(f"A_{p}_L1_{den}","A_LAMBDA_WIDTH",p,
     v["R"],v["tau"],[lo,"5"]))
 for suffix,mesh in COARSE_MESHES:
  for p,v in PROBES.items():
   experiments.append(case(f"B_{p}_{suffix}","B_HESSIAN_COARSE",p,
       v["R"],v["tau"],["1279/256","5"],mesh))
 for den in (32,16):
  v=PROBES["P1"]
  experiments.append(case(f"C_P1_RTau1_{den}","C_SPATIAL_BOX","P1",
      ["1/4",str(F(1,4)+F(1,den))],
      ["0",str(F(1,den))],["39/8","5"]))
 for p in ("P1","P3"):
  v=PROBES[p]
  experiments.append(case(f"D_{p}_LOW2_L1_8","D_LOW_LAMBDA",p,
      v["R"],v["tau"],["2","17/8"]))
 skipped=[]
 for den in (32,16):
  t0=F(63,64);t1=t0+F(1,den)
  assert t1>1
  skipped.append({"status":STATUS,"id":f"C_P3_RTau1_{den}",
   "group":"C_SPATIAL_BOX","probe":"P3",
   "R":["1/4",str(F(1,4)+F(1,den))],
   "tau":["63/64",str(t1)],"lambda":["39/8","5"],
   "run_status":"NOT_RUN_OUT_OF_DOMAIN","H_interval":None,
   "reason":"frozen lower-left tau=63/64 plus requested width exceeds 1; no silent box move"})
 assert len(experiments)==24 and len(skipped)==2
 assert len({x["id"] for x in experiments+skipped})==26
 assert [x["group"] for x in experiments]==(
   ["A_LAMBDA_WIDTH"]*12+["B_HESSIAN_COARSE"]*8+
   ["C_SPATIAL_BOX"]*2+["D_LOW_LAMBDA"]*2)
 for p,v in PROBES.items():
  baseline=json.loads((BASE/(v["baseline"]+".json")).read_text())
  assert baseline["status"]==STATUS
  assert baseline["input_box"]["R"]==v["R"]
  assert baseline["input_box"]["tau"]==v["tau"]
  assert baseline["input_box"]["lambda"]==["1279/256","5"]
  assert baseline["route_from_position"]==v["route"]
 for spec in experiments:
  assert F(spec["R"][0])>=F(1,4) and F(spec["R"][1])<=F(1,2)
  assert F(0)<=F(spec["tau"][0])<F(spec["tau"][1])<=F(1)
  assert F(2)<=F(spec["lambda"][0])<F(spec["lambda"][1])<=F(5)
 return {"status":STATUS,"baseline_commit":"0427b19d84e5105aa1a03ff69c9842065d491f3c",
  "V39_commit":"544ebfd138c02d2fc68806184a1d0ce2e744fa2c",
  "pinned_R3_commit":"fdfb498f2117cc0c5d72e88cc3be05eac9727bd8",
  "base_mesh":BASE_MESH,"probes":PROBES,"time_caps":CAPS,
  "total_wall_cap_s":BUDGET,"max_parallel":MAX_WORKERS,
  "jobs":experiments,"invalid_geometry":skipped,
  "sign_only_recorded":True,"is_cover":False}
def frozen_write():
 OUT.mkdir(parents=True,exist_ok=True)
 p=OUT/"EXPERIMENTS.json"
 doc=plan()
 if p.exists():
  assert json.loads(p.read_text())==doc,"FROZEN_EXPERIMENTS_MISMATCH"
 else:p.write_text(json.dumps(doc,indent=2)+"\n")
 return doc
if __name__=="__main__":
 doc=frozen_write()
 print(STATUS,"jobs",len(doc["jobs"]),"invalid",len(doc["invalid_geometry"]))
