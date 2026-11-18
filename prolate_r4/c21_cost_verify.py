"""Independent exact-rational consistency checker, C21 cost pilot only.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Does NOT certify density jets.
"""
from __future__ import annotations
import json
from fractions import Fraction as F
from . import c21_cost_plan as plan
STATUS=plan.STATUS
OUT=plan.OUT
def bounds(d):
 return F(d["lower"]),F(d["upper"])
def contained(target,parts):
 lo,hi=bounds(target)
 return lo<=sum((bounds(x)[0] for x in parts),F(0)) and hi>=sum((bounds(x)[1] for x in parts),F(0))
def verify():
 reg=plan.plan()
 frozen=json.loads((OUT/"EXPERIMENTS.json").read_text())
 assert frozen==reg,"PRE_RUN_FROZEN_REGISTRY_MISMATCH"
 state=json.loads((OUT/"STATE.json").read_text())
 sm=json.loads((OUT/"SUMMARY.json").read_text())
 assert state["status"]==sm["status"]==STATUS
 assert not state["inflight"]
 assert not state["is_cover"] and not sm["is_cover"]
 assert sm["measured_jobs"]==len(state["finished"])
 assert sm["invalid_geometry"]==2
 assert len(state["finished"])<=24
 seen=set();checked=0;errors=0
 for entry in state["finished"]:
  name=entry["id"]
  assert name not in seen
  seen.add(name)
  original=next(x for x in reg["jobs"] if x["id"]==name)
  source=OUT/entry["source_json"]
  log=OUT/entry["source_log"]
  assert source.exists() and log.exists()
  d=json.loads(source.read_text())
  assert d["status"]==STATUS
  assert d["id"]==name and d["experiment_input"]==original
  if entry["result"]=="OPEN":
   assert d["H_interval"] is None and "reason" in d
   errors+=1;continue
  assert d["no_cover"] is True and d["sign_does_not_control_method"] is True
  assert d["route_from_position"]==original["route_expected"]
  assert d["base_mesh"]["order"]==4
  assert d["base_mesh"]["base_u"]==16 and d["base_mesh"]["base_v"]==32
  assert d["base_mesh"]["ratio"]=="1/2"
  for field in ("order","base_u","base_v","ratio"):
   assert d["hessian_mesh"][field]==original["hessian_mesh"][field]
  assert len(d["gradient"])==3 and len(d["hessian"])==6
  assert contained(d["H_interval"],
    (d["center_point"],d["linear_correction"],d["quadratic_correction"]))
  assert contained(d["linear_correction"],
    [v["correction"] for v in d["gradient"].values()])
  assert contained(d["quadratic_correction"],
    [v["correction"] for v in d["hessian"].values()])
  z=bounds(d["H_interval"])
  assert (z[0]<=0<=z[1])==d["zero_included_RECORD_ONLY"]
  for i,a in enumerate(d["outer_axes"]):
   b=tuple(F(x) for x in d["actual_outer_boxes"][a])
   h=(b[1]-b[0])/2
   assert d["gradient"][a]["halfwidth_outer"]==str(h)
   for j in range(i,len(d["outer_axes"])):
    other=d["outer_axes"][j]
    elem=d["hessian"][a+"_"+other]
    if i==j:
     assert elem["type"]=="diagonal_half"
     assert elem["factor"]==["0",str(h*h)]
    else:
     h2=(F(d["actual_outer_boxes"][other][1])-
         F(d["actual_outer_boxes"][other][0]))/2
     assert elem["type"]=="cross"
     assert elem["factor"]==[str(-h*h2),str(h*h2)]
  if original["group"]=="B_HESSIAN_COARSE":
   # Point and gradient are unchanged from original Stage B.
   old=json.loads((plan.BASE/(plan.PROBES[original["probe"]]["baseline"]+".json")).read_text())
   assert old["center_point"]==d["center_point"]
   for k,v in d["gradient"].items():
    assert old["gradient"][k]["interval"]==v["signed_derivative"]
    assert old["gradient"][k]["correction"]==v["correction"]
   assert old["mesh_cells"]==d["base_mesh"]["cells"]
  checked+=1
 assert sm["completed_jobs"]==checked and sm["open_jobs"]==errors
 assert len(state["invalid_geometry"])==2
 for invalid in state["invalid_geometry"]:
  assert invalid["H_interval"] is None
  assert F(invalid["tau"][1])>1
  assert invalid["run_status"]=="NOT_RUN_OUT_OF_DOMAIN"
 record={"status":STATUS,
   "verdict":"PASS" if all(x["result"]=="COMPLETED" for x in state["finished"]) else "PARTIAL_OR_OPEN_WITH_CONSISTENCY_PASS",
   "verified_completed":checked,"verified_open":errors,
   "invalid_geometry_confirmed":2,
   "source_identifiers_disjoint":True,"signed_interval_sum_contains_all_components":True,
   "coarse_Hessian_point_grad_equal_historical_baseline":True,
   "independent_mathematical_jets_audit":False,
   "no_coverage":True}
 (OUT/"CHECKER.json").write_text(json.dumps(record,indent=2)+"\n")
 print(json.dumps(record,indent=2))
 return record
if __name__=="__main__":verify()
