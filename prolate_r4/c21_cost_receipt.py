"""Measured C21 H cost pilot receipt. DIAGNOSTIC_ONLY / NOT_EVIDENCE."""
import json
from fractions import Fraction as F
from . import c21_cost_plan as plan
OUT=plan.OUT
STATUS=plan.STATUS
def load(n):
 p=OUT/n
 return json.loads(p.read_text()) if p.exists() else None
def build():
 spec=load("EXPERIMENTS.json")
 summary=load("SUMMARY.json")
 model=load("COST_MODEL.json")
 checker=load("CHECKER.json")
 lines=["# C21 H second-order cost-trim experimental receipt",
 "**DIAGNOSTIC_ONLY / NOT_EVIDENCE**","",
 "Source baseline commit 0427b19d84e5105aa1a03ff69c9842065d491f3c.",
 "Source V39 commit 544ebfd138c02d2fc68806184a1d0ce2e744fa2c.",
 "Measurement only. No covering. No sign-based method selection.","",
 "## Results and scope"]
 if summary:
  for k in ("measured_jobs","completed_jobs","open_jobs",
    "invalid_geometry","unrun_valid","worker_seconds_sum","pilot_wall_s"):
   lines.append("- "+k+": "+str(summary[k]))
 else:lines.append("No run finished.")
 lines+=["","P3 C cases: tau_lower=63/64 and requested widths1/32 or1/16;",
   "both upper tau exceed1. Both are frozen NOT_RUN_OUT_OF_DOMAIN.",
   "No silent geometry changes.","",
   "## All measured boxes","",
   "| ID | Group | Route | lambda width | R width | tau width | Hess mesh | H halfwidth | Point | Linear | Hessian | Point s | Grad s | Hess s | Total s | RSS KiB | zero? |",
   "|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
 if summary:
  resultmap={x["id"]:x for x in summary["results"]}
  for x in spec["jobs"]:
   res=resultmap.get(x["id"])
   h=x["hessian_mesh"]
   fields=[x["id"],x["group"],x["route_expected"],
      str(F(x["lambda"][1])-F(x["lambda"][0])),
      str(F(x["R"][1])-F(x["R"][0])),
      str(F(x["tau"][1])-F(x["tau"][0])),
      str(h["base_u"])+"x"+str(h["base_v"])+"/"+h["ratio"]+"/n"+str(h["order"])]
   if res and res["result"]=="COMPLETED":
    d=load(res["source_json"]);t=d["timing"]
    row=[f"{d['H_interval']['halfwidth']:.7g}",
     f"{d['center_point']['halfwidth']:.6g}",
     f"{d['linear_correction']['halfwidth']:.6g}",
     f"{d['quadratic_correction']['halfwidth']:.6g}",
     f"{t['point_s']:.2f}",f"{t['gradient_sum_s']:.2f}",
     f"{t['hessian_sum_s']:.2f}",f"{t['total_worker_s']:.2f}",
     str(d["peak_RSS_KiB"]),
     "yes" if d["zero_included_RECORD_ONLY"] else "no"]
   else:
    row=[("OPEN: "+res.get("reason","") if res else "NOT_RUN")]+["—"]*9
   lines.append("| "+" | ".join(fields+row)+" |")
 for z in spec["invalid_geometry"]:
  lines.append("| "+z["id"]+" | C_SPATIAL_BOX | AXIS_MVT | 1/8 | "+
   str(F(z["R"][1])-F(z["R"][0]))+" | "+
   str(F(z["tau"][1])-F(z["tau"][0]))+
   " | — | NOT_RUN_OUT_OF_DOMAIN | — | — | — | — | — | — | — | — | — |")
 lines+=["","All ten point, gradient and Hessian signed components,",
   "individual wall times, exact H interval endpoints, base and Hess",
   "mesh sizes, and peak child RSS are in per-box JSON files.","",
   "## Historical baseline (not charged to current pilot)","",
   "| Probe | H halfwidth | Point s | Grad s | Hess s | Total s |",
   "|---|---:|---:|---:|---:|---:|"]
 if model:
  for b in model["baseline_historical"]:
   t=b["time_s"]
   lines.append(f"| {b['id']} | {b['halfwidth']:.7g} | "+
      f"{t['point']:.2f} | {t['gradient']:.2f} | "+
      f"{t['hessian']:.2f} | {t['total']:.2f} |")
  lines+=["","## Width empirical formula","",
   "All h values are nominal HALF widths. For GENERAL only:",
   "w_hat = c0 + aR hR + aT hTau + aL hLambda",
   " + bRR hR^2 + bRT hR hTau + bTT hTau^2",
   " + bRL hR hLambda + bTL hTau hLambda + bLL hLambda^2.",
   "Coefficients are medians of actual signed-component correction",
   "halfwidths divided by the corresponding monomial.",
   "They do NOT describe rigorous bounds or verified regression."]
  for route,d in model["modeled_width_by_route"].items():
   lines+=["","### "+route,
    "training_count: "+str(d.get("training_count")),
    "model scope: "+d.get("mvt_caveat","INSUFFICIENT")]
   if "coefficients" in d:
    lines+=["| Monomial | coefficient |","|---|---:|"]
    for m,c in zip(d["monomials"],d["coefficients"]):
     lines.append(f"| {m} | {c:.8g} |")
    lines.append(f"In-sample median absolute error: {d['test_abs_error_median']:.6g}; "+
       f"max: {d['test_abs_error_max']:.6g}; "+
       f"median relative: {d['test_rel_error_median']:.4g}.")
  estimate=model["global_H_cost_scenarios"]
  if estimate.get("supported"):
   lines+=["","## Hypothetical full lambda 2..5 workload (NOT forecasts)","",
    "Assume 12 workers and an UNVERIFIED route mix (75% general,25% axis).",
    "Per first R-tau cell, assume f fraction splits on every level:",
    "sum(k=0..2log2(256/d)) (2f)^k at grid dxd.",
    "The near-lambda2 plate thickness is an independent assumption.",
    "All plate thicknesses, split fractions, workload portability and",
    "route proportions are hypothetical.","",
    "| Grid | f | lambda plate policy | Plates | Equivalent H jobs | Wall hours (12 workers) |",
    "|---|---:|---|---:|---:|---:|"]
   for row in estimate["hypotheses"]:
    if row["initial_R_tau_edge"]=="1/64" or (
       row["initial_R_tau_edge"]=="1/32" and row["assumed_split_probability_each_level"]==.25):
     lines.append(f"| {row['initial_grid']} | {row['assumed_split_probability_each_level']:.2f} | "+
       f"{row['lambda_plate_policy']} | {row['hypothetical_plate_count']} | "+
       f"{row['hypothetical_total_H_jobs']:,.0f} | {row['hypothetical_wall_hours']:,.1f} |")
   lines+=["","No upper bound for the real global problem is established.",
      "Low-lambda local probes do not imply global plate width."]
 lines+=["","## Integrity and conclusion",
   "Record checker: "+(checker["verdict"] if checker else "NOT_RUN"),
   "The checker verifies input IDs, interval endpoint arithmetic,",
   "mesh and signed coefficients. Independent mathematical audit",
   "of new mixed-jets and global coverage is not included.",
   "**DIAGNOSTIC_ONLY / NOT_EVIDENCE** — C21 global theorem OPEN."]
 (OUT/"RUN_RECEIPT.md").write_text("\n".join(lines)+"\n")
 print(json.dumps({"status":STATUS,"receipt_lines":len(lines),
                   "measured":summary["completed_jobs"] if summary else None}))
if __name__=="__main__":build()
