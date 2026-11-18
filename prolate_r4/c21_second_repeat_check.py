"""Replay check: identical Stage A and Stage B boxes under frozen C21 Hessian.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Compares exact interval endpoints, not CPU times.
"""
import json
from pathlib import Path
OUT=Path("runs/2026-11-18/D_PRO_C21_H_SECOND_ORDER")
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
REPEATS=("R16_T00","R16_T63","R26_T00")
def run():
 record=[]
 for name in REPEATS:
  a=json.loads((OUT/"stage_A_boxes"/(name+".json")).read_text())
  b=json.loads((OUT/"STAGE_B/boxes"/(name+".json")).read_text())
  assert a["status"]==b["status"]==STATUS
  for k in ("input_box","route_from_position","outer_axes",
     "actual_outer_boxes","center_point","linear_correction",
     "quadratic_correction","H_interval","mesh_cells","mesh"):
   assert a[k]==b[k],(name,"mismatch",k)
  for k in a["gradient"]:
   for prop in ("interval","correction","outer_halfwidth"):
    assert a["gradient"][k][prop]==b["gradient"][k][prop]
  for k in a["hessian"]:
   for prop in ("interval","correction","factor_interval","type"):
    assert a["hessian"][k][prop]==b["hessian"][k][prop]
  record.append({"id":name,"same_H_endpoints":True,
     "same_all_gradient_and_Hessian_intervals":True,
     "mesh_cells":a["mesh_cells"],"stage_A_wall_s":a["wall_s"],
     "stage_B_wall_s":b["wall_s"]})
 out={"status":STATUS,"verdict":"PASS","replayed_count":len(record),
    "records":record,
    "not_an_independent_mathematical_validation":True}
 (OUT/"REPEAT_CHECKER.json").write_text(json.dumps(out,indent=2)+"\n")
 print(json.dumps(out,indent=2))
if __name__=="__main__":run()
