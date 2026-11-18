"""Independent rational-ledger audit of preregistered eight Stage A C21 boxes.
DIAGNOSTIC_ONLY / NOT_EVIDENCE: no independent proof of density jets.
"""
from __future__ import annotations
import json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"runs/2026-11-18/D_PRO_C21_H_SECOND_ORDER"
PRIOR=ROOT/"runs/2026-11-18/D_PRO_C21_SLAB_PART/boxes"
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
FIXED_IDS=("R16_T00","R18_T08","R20_T48","R23_T32",
           "R26_T00","R28_T32","R16_T63","R31_T63")
def limits(b):
 return F(b["lower"]),F(b["upper"])
def width(b):
 lo,hi=limits(b)
 assert lo<=hi
 return (hi-lo)/2
def summation_contained(whole,pieces):
 lo,hi=limits(whole)
 return lo<=sum((limits(x)[0] for x in pieces),F(0)) and hi>=sum((limits(x)[1] for x in pieces),F(0))
def run():
 sel=json.loads((OUT/"STAGE_A_SELECTION.json").read_text())
 gate=json.loads((OUT/"STAGE_A_GATE.json").read_text())
 assert sel["status"]==gate["status"]==STATUS
 assert tuple(x["id"] for x in sel["samples"])==FIXED_IDS
 assert tuple(x["id"] for x in gate["results"])==FIXED_IDS
 assert len(gate["results"])==len(sel["samples"])==8
 pass_count=0
 rows=[]
 for oldspec,gaterow in zip(sel["samples"],gate["results"]):
  name=oldspec["id"]
  assert gaterow["id"]==name and gaterow["run_result"]=="COMPLETED"
  old=json.loads((PRIOR/(name+".json")).read_text())
  new=json.loads((OUT/"stage_A_boxes"/(name+".json")).read_text())
  assert old["name"]==new["name"]==name
  assert old["route_from_position"]==new["route_from_position"]==oldspec["route"]
  assert old["input_box"]==new["input_box"]
  assert old["status"]==new["status"]==STATUS
  assert new["mesh"]["precision"]==128
  assert new["mesh"]["order"]==4
  assert new["mesh"]["base_u"]==16 and new["mesh"]["base_v"]==32
  assert new["mesh"]["distance_ratio"]=="1/2"
  assert new["mesh_cells"]>0
  old_h=width(old["H_interval"])
  new_h=width(new["H_interval"])
  assert old_h==F(oldspec["old_halfwidth_exact"])
  assert old_h==F(gaterow["first_order_halfwidth_exact"])
  assert new_h==F(gaterow["second_order_halfwidth_exact"])
  assert new_h<=old_h
  assert gaterow["comparison"]=="NONWORSE"
  assert summation_contained(new["H_interval"],
      [new["center_point"],new["linear_correction"],new["quadratic_correction"]])
  axes=new["outer_axes"];assert len(axes)==3
  assert len(new["gradient"])==3
  assert len(new["hessian"])==6
  assert set(new["gradient"])==set(axes)
  assert summation_contained(new["linear_correction"],
       [new["gradient"][v]["correction"] for v in axes])
  hessian_names=[]
  for i,a in enumerate(axes):
   for j in range(i,len(axes)):
    b=axes[j];key=a+"_"+b
    item=new["hessian"][key]
    assert item["type"]==("diagonal_half" if i==j else "cross")
    assert width(item["interval"])>=0
    hessian_names.append(key)
  assert set(hessian_names)==set(new["hessian"])
  assert summation_contained(new["quadratic_correction"],
     [new["hessian"][key]["correction"] for key in hessian_names])
  rows.append({"id":name,"route":new["route_from_position"],
    "old_halfwidth_exact":str(old_h),"new_halfwidth_exact":str(new_h),
    "improvement_ratio_exact":str(old_h/new_h),
    "new_worker_wall_s":new["wall_s"],
    "peak_RSS_KiB":new["peak_RSS_KiB"],
    "signed_component_arithmetic_contains_sum":True})
  pass_count+=1
 assert gate["completed"]==8 and gate["worse"]==gate["open"]==0
 assert gate["stage_B_gate"]=="STAGE_B_ALLOWED"
 record={"status":STATUS,
   "verdict":"PASS",
   "scope":"Stage A eight box interval-record, exact fraction width and Taylor sum arithmetic",
   "checked_original_pairs":pass_count,
   "gate":"STAGE_B_ALLOWED",
   "selection_ids":list(FIXED_IDS),
   "rows":rows,
   "not_independent_math_of_C21_Arb_or_jets":True}
 (OUT/"STAGE_A_CHECKER.json").write_text(json.dumps(record,indent=2)+"\n")
 print(json.dumps({"status":STATUS,"verdict":"PASS",
   "checked_pairs":pass_count,"stage_B_gate":gate["stage_B_gate"],
   "all_exact_interval_sums_contained":True,
   "not_mathematical_certification":True},indent=2))
if __name__=="__main__":run()
