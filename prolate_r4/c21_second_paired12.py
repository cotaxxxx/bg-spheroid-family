"""Measured paired first 12 C21 H boxes: old MVT-1 vs frozen Taylor-2.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. All boxes same exact rational inputs.
"""
import json,statistics
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/"runs/2026-11-18/D_PRO_C21_SLAB_PART/boxes"
OUT=ROOT/"runs/2026-11-18/D_PRO_C21_H_SECOND_ORDER"
NEW=OUT/"STAGE_B/boxes"
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
def width(b):
 return (F(b["upper"])-F(b["lower"]))/2
def exclude0(b):
 return F(b["upper"])<0 or F(b["lower"])>0
def run():
 state=json.loads((OUT/"STAGE_B/state.json").read_text())
 first_names=[p["id"] for p in state["processed_jobs"][:12]]
 assert len(first_names)==12
 pairs=[]
 for name in first_names:
  old=json.loads((OLD/(name+".json")).read_text())
  new=json.loads((NEW/(name+".json")).read_text())
  assert new["status"]==old["status"]==STATUS
  assert new["input_box"]==old["input_box"]
  assert new["route_from_position"]==old["route_from_position"]
  a=width(old["H_interval"]);b=width(new["H_interval"])
  pairs.append({"id":name,"route":new["route_from_position"],
   "old_halfwidth_exact":str(a),"new_halfwidth_exact":str(b),
   "ratio_old_over_new":float(a/b) if b else None,
   "old_zero_excluded":exclude0(old["H_interval"]),
   "new_zero_excluded":exclude0(new["H_interval"]),
   "old_worker_s":old["worker_elapsed_s"],
   "new_worker_s":new["wall_s"],
   "old_cells":old["mesh_cells"],"new_cells":new["mesh_cells"]})
 result={"status":STATUS,"paired_measured_boxes":len(pairs),
   "old_decided_count":sum(p["old_zero_excluded"] for p in pairs),
   "new_decided_count":sum(p["new_zero_excluded"] for p in pairs),
   "newly_decided":sum(p["new_zero_excluded"] and not p["old_zero_excluded"] for p in pairs),
   "regressions":sum(p["old_zero_excluded"] and not p["new_zero_excluded"] for p in pairs),
   "width_ratio_median":statistics.median(p["ratio_old_over_new"] for p in pairs),
   "old_worker_wall_sum_s":sum(p["old_worker_s"] for p in pairs),
   "new_worker_wall_sum_s":sum(p["new_worker_s"] for p in pairs),
   "pairs":pairs,"not_mathematical_certification":True}
 (OUT/"STAGE_B_PAIRED12.json").write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps({k:result[k] for k in result if k!="pairs"},indent=2))
if __name__=="__main__":run()
