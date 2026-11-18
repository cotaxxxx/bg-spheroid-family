"""Post-measurement cost arithmetic by fixed Hessian method (not a numerical rule).
DIAGNOSTIC_ONLY / NOT_EVIDENCE. All full-domain inputs are hypothetical.
"""
import json,math,statistics
from . import c21_cost_plan as plan
STATUS=plan.STATUS
OUT=plan.OUT
def load(n):return json.loads((OUT/n).read_text())
def main():
 d=load("SUMMARY.json")
 baseline={}
 for p,x in plan.PROBES.items():
  old=json.loads((plan.BASE/(x["baseline"]+".json")).read_text())
  baseline[p]=old["wall_s"]
 measured={}
 for item in d["results"]:
  if item["result"]=="COMPLETED":
   dat=load(item["source_json"])
   measured[item["id"]]=dat["timing"]["total_worker_s"]
 modes={
 "original_second_order_1_256_HESS16x32n4":{"P1":baseline["P1"],"P2":baseline["P2"],
    "P3":baseline["P3"],"P4":baseline["P4"]},
 "thick_1_8_HESS16x32n4":{
    p:measured.get("A_"+p+"_L1_8") for p in plan.PROBES},
 "hessian_only_8x16n4":{
    p:measured.get("B_"+p+"_H8x16_O4") for p in plan.PROBES},
 "hessian_only_8x16n2":{
    p:measured.get("B_"+p+"_H8x16_O2") for p in plan.PROBES}}
 stats={}
 for mode,x in modes.items():
  g=[x["P1"],x["P2"]];a=[x["P3"],x["P4"]]
  if any(v is None for v in g+a):
   stats[mode]={"available":False};continue
  gm=statistics.median(g);am=statistics.median(a)
  stats[mode]={"available":True,"median_GENERAL_s":gm,
     "median_AXIS_MVT_s":am,
     "assumed_route_weight_GENERAL":.75,
     "assumed_route_weight_AXIS":.25,
     "hypothetical_mixed_worker_box_s":.75*gm+.25*am,
     "measured_P1_P2_P3_P4_worker_s":x}
 policies={
  "UNIFORM_WIDTH_1_8_ALL_2_5_NOT_VALIDATED":24,
  "LOW_2_3_WIDTH_1_1024_PLUS_HIGH_3_5_WIDTH_1_8":1040,
  "UNIFORM_WIDTH_1_256_ALL_2_5_NOT_VALIDATED":768}
 table=[]
 for mode,coeff in stats.items():
  if not coeff["available"]:continue
  for grid in (16,32,64):
   levels=2*int(math.log2(256/grid))
   for fraction in (.25,.5,.75):
    evaluations=grid*grid*sum((2*fraction)**k for k in range(levels+1))
    for policy,platecount in policies.items():
     jobs=evaluations*platecount
     table.append({"method":mode,"initial_grid":f"{grid}x{grid}",
      "assumed_split_fraction_each_depth":fraction,
      "max_binary_depth":levels,"initial_R_tau_edge":f"1/{grid}",
      "lambda_policy":policy,"hypothetical_lambda_plates":platecount,
      "expected_equivalent_H_jobs":jobs,
      "assumed_12_workers":12,
      "conditional_wall_hours":jobs*coeff["hypothetical_mixed_worker_box_s"]/43200,
      "no_coverage_or_evidence":True})
 ret={"status":STATUS,"method_median_costs":stats,
   "unverified_route_mix":"0.75 general /0.25 axis",
   "unverified_per_depth_split_fractions":[.25,.5,.75],
   "hypothetical_plate_policies":policies,
   "all_method_grid_plate_combinations":table,
   "limitations":["Only four R-tau locations measured; full R-tau board and lambda≈2 may cost differently",
    "Hessian mesh and widened R-tau boxes were not jointly measured",
    "Changing lambda plate thickness changes sign-uncertain split fraction",
    "These totals are NOT actual H covering results or validated upper bounds"],
   "sign_not_used_to_select_parameters":True}
 (OUT/"COST_METHOD_SCENARIOS.json").write_text(json.dumps(ret,indent=2)+"\n")
 chosen=[
  ("original_second_order_1_256_HESS16x32n4",64,.5,
   "UNIFORM_WIDTH_1_256_ALL_2_5_NOT_VALIDATED"),
  ("thick_1_8_HESS16x32n4",64,.5,
   "UNIFORM_WIDTH_1_8_ALL_2_5_NOT_VALIDATED"),
  ("hessian_only_8x16n4",16,.25,
   "UNIFORM_WIDTH_1_8_ALL_2_5_NOT_VALIDATED"),
  ("hessian_only_8x16n2",16,.25,
   "UNIFORM_WIDTH_1_8_ALL_2_5_NOT_VALIDATED"),
  ("hessian_only_8x16n4",16,.25,
   "LOW_2_3_WIDTH_1_1024_PLUS_HIGH_3_5_WIDTH_1_8"),
  ("hessian_only_8x16n2",16,.25,
   "LOW_2_3_WIDTH_1_1024_PLUS_HIGH_3_5_WIDTH_1_8")]
 lines=["# D-PRO C21 H post-run method-specific COST SCENARIOS",
   "**DIAGNOSTIC_ONLY / NOT_EVIDENCE**","",
   "Pure arithmetic extrapolation, NOT a H covering or an upper bound.",
   "Assumptions: 12 workers, mix 75% general/25% axis,",
   "all boxes take four-probe median cost of the listed method,",
   "and each depth has hypothetical fraction f of boxes splitting.",
   "All lambda plate widths are unverified away from measured local boxes.",
   "No W work included. Combining enlarged R-tau initial boxes with",
   "coarse Hessian is a counterfactual combination NOT measured together.","",
   "| Mode | Initial grid | split f | lambda plates | assumed H jobs | 12-worker hours |",
   "|---|---:|---:|---:|---:|---:|"]
 for mode,grid,f,policy in chosen:
  x=next(q for q in table if q["method"]==mode and q["initial_grid"]==f"{grid}x{grid}"
    and q["assumed_split_fraction_each_depth"]==f and q["lambda_policy"]==policy)
  lines.append(f"| {mode} | {grid}² | {f} | {x['hypothetical_lambda_plates']} | "+
     f"{x['expected_equivalent_H_jobs']:,.0f} | {x['conditional_wall_hours']:,.1f} |")
 lines+=["","The conditional low-lambda 1/1024 width [2,3] is an independently",
   "assumed high-resolution policy. The λ≈2 pilot never establishes this",
   "thickness nor that the entire λ∈[2,5] signs can be covered.",
   "**DIAGNOSTIC_ONLY / NOT_EVIDENCE.**"]
 (OUT/"COST_METHOD_SCENARIOS.md").write_text("\n".join(lines)+"\n")
 print(json.dumps({"status":STATUS,"scenarios":len(table),
  "modes":len(stats),"representatives":len(chosen)}))
if __name__=="__main__":main()
