"""Stage A and possible Stage B C21 diagnostic measured report.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
import json
from pathlib import Path
OUT=Path("runs/2026-11-18/D_PRO_C21_H_SECOND_ORDER")
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
def load(path):
 p=OUT/path
 return json.loads(p.read_text()) if p.exists() else None
def build():
 gate=load("STAGE_A_GATE.json")
 sm=load("STAGE_B/summary.json")
 lines=["# C21 H second-order interval diagnostic","",
 "**DIAGNOSTIC_ONLY / NOT_EVIDENCE**","",
 "Frozen Stage-A selection: 8 boxes, 6 general, 2 axis.",
 "Prerun commit 4760c534b02621c5a31a9befc6469495fb8d9c4b.",
 "C21 source 5004ebd, V38 922a2c7, original84 2e3a091.",
 "Original physical vertical coordinate p_z=lambda*z.",
 "All spatial integrals are signed Taylor order4 at Arb128.","",
 "## Stage A: historical first order versus second order",""]
 if gate:
  lines.extend([f"Measured parallel wall time: {gate['stage_A_wall_s']:.3f} seconds.",
    f"Completed: {gate['completed']}/8. Worse: {gate['worse']}. OPEN: {gate['open']}.",
    f"Decision gate: {gate['stage_B_gate']}.","",
    "| ID | Route | Old halfwidth | New halfwidth | Point | Linear | Hessian | Old s | New s | Gate |",
    "|---|---|---:|---:|---:|---:|---:|---:|---:|---|"])
  for x in gate["results"]:
   def fmt(k):
    v=x.get(k);return "OPEN" if v is None else f"{v:.8g}" if isinstance(v,float) else str(v)
   lines.append("| "+ " | ".join([x["id"],x["route"],fmt("first_order_halfwidth"),
      fmt("second_order_halfwidth"),fmt("point_halfwidth"),
      fmt("linear_halfwidth"),fmt("quadratic_halfwidth"),
      fmt("first_order_wall_s"),fmt("second_order_parent_wall_s"),
      x.get("comparison","OPEN")])+" |")
 else:
  lines+=["Stage A not finished; no eight-box gate decision.",""]
 lines.extend(["","## Stage B: 1024 initial boxes on R=1/4..1/2, tau=0..1",""])
 if sm:
  for name in ("measured_jobs","decided_count","tube_candidate_EVALUATED_count",
       "pending_UNEVALUATED_count","split_parents","area_decided_exact",
       "area_tube_evaluated_exact","area_pending_exact",
       "area_partition_sum_exact","H_adaptive_wall_s",
       "total_experiment_wall_s_including_calibration"):
   lines.append("- "+name+": "+str(sm[name]))
  lines+=["","Exact area relation: decided + evaluated tube + pending = 1/4.",
   "The pending area is not measured tube area."]
  lines+=["","| Route | Jobs | Worker seconds |","|---|---:|---:|"]
  for rt in ("GENERAL","AXIS_MVT","SMALL_RHO_MVT","CENTER_MVT"):
   lines.append(f"| {rt} | {sm['route_jobs'].get(rt,0)} | {sm['route_worker_seconds_sum'].get(rt,0):.3f} |")
  lines+=["","| Depth | Evaluated | Terminal |","|---|---:|---:|"]
  for d,n in sorted(sm["depth_processed"].items(),key=lambda z:int(z[0])):
   lines.append(f"| {d} | {n} | {sm['depth_terminal'].get(d,0)} |")
 else:lines+=["Stage B not started. Do not estimate a full subregion cost.",""]
 w=load("STAGE_B/W_SAMPLE_RESULTS.json")
 lines+=["","## W three-box-only measurement","",
         "Measured: "+("YES" if w else "NO, deferred")]
 paired=load("STAGE_B_PAIRED12.json")
 repeat=load("REPEAT_CHECKER.json")
 acheck=load("STAGE_A_CHECKER.json")
 lines+=["","## Independent exact-fraction output audits",""]
 if acheck:lines.append(f"Stage-A 8-box exact-width and Taylor decomposition: {acheck['verdict']}; not a mathematical kernel proof.")
 if repeat:lines.append(f"Duplicated Stage A versus B interval bytewise equality: {repeat['replayed_count']} boxes, {repeat['verdict']}.")
 if paired:
  lines.extend([f"Paired 12 original first-order vs new second-order boxes:",
    f"old decided {paired['old_decided_count']}/12, new decided {paired['new_decided_count']}/12;",
    f"newly decided {paired['newly_decided']}, regressions {paired['regressions']}.",
    f"Median old/new halfwidth ratio {paired['width_ratio_median']:.6f}.",
    f"Historical worker-seconds sum {paired['old_worker_wall_sum_s']:.3f};",
    f"new worker-seconds sum {paired['new_worker_wall_sum_s']:.3f}."])
 lines+=["","## Cost extrapolation",""]
 if sm and sm["full_subregion_processed"]:
  n=sm["measured_jobs"];s=sm["H_adaptive_wall_s"]
  lines +=[f"Full requested 1/4 area measured: {n} H jobs and {s:.3f} H wall seconds.",
     f"Conditional equal-cost-per-area for full R-tau board: {4*n} jobs, {4*s:.2f} seconds.",
     "Uniform lambda thickness1/256 on [2,5] means 768 hypothetical plates.",
     "Alternative 1/1024 on [2,3] plus1/256 on [3,5] means1536 plates.",
     "Neither cost nor plate thickness is verified outside the measured region."]
 else:
  lines+=["Full subregion unfinished or gate blocked. No extrapolated box number.",
     "Plate counts 768 or1536 depend on unverified lambda thickness assumptions."]
 lines+=["","## Audit","",
   "No independent mathematical audit of new Hessian jets completed.",
   "The mathematical Taylor-2 formula is documented separately.",
   "Checker and SHA establish ledger and byte consistency only.",
   "No previous research branch, main, STATE.md, tags, or frozen Julia changed.",
   "**DIAGNOSTIC_ONLY / NOT_EVIDENCE. C21 global theorem OPEN.**"]
 (OUT/"RUN_RECEIPT.md").write_text("\n".join(lines)+"\n")
 print(json.dumps({"stage_A":gate["stage_B_gate"] if gate else "RUNNING",
       "stage_B":sm["full_subregion_processed"] if sm else "NOT_STARTED",
       "lines":len(lines)}))
if __name__=="__main__":build()
