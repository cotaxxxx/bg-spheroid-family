"""Post-run cost-only empirical width model and conditional global price scenarios.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. No sign-driven choices, no covering.
"""
from __future__ import annotations
import json,math,statistics as stats
from pathlib import Path
from fractions import Fraction as F
from . import c21_cost_plan as plan
STATUS=plan.STATUS
OUT=plan.OUT
def median(a):return stats.median(a) if a else None
def jsonload(p):return json.loads(p.read_text()) if p.exists() else None
def feature(h):
 x,y,z=h
 return (1.,x,y,z,x*x,x*y,y*y,x*z,y*z,z*z)
MONOMIAL=("1","h_R","h_tau","h_lambda","h_R^2",
          "h_R*h_tau","h_tau^2","h_R*h_lambda","h_tau*h_lambda","h_lambda^2")
def hc(d):
 g=d["geometric_halfwidths"]
 return tuple(float(F(g[k])) for k in ("h_R","h_tau","h_lambda"))
def aggregate_baselines():
 rows=[]
 for p,spec in plan.PROBES.items():
  raw=json.loads((plan.BASE/(spec["baseline"]+".json")).read_text())
  assert raw["status"]==STATUS
  grad=sum(x["wall_s"] for x in raw["gradient"].values())
  hess=sum(x["wall_s"] for x in raw["hessian"].values())
  rows.append({"id":p,"route":spec["route"],"source":"H_SECOND_ORDER/STAGE_B/boxes/"+spec["baseline"]+".json",
    "H_interval":raw["H_interval"],
    "halfwidth":raw["H_interval"]["halfwidth"],
    "time_s":{"point":raw["point_wall_s"],"gradient":grad,"hessian":hess,
       "total":raw["wall_s"]},"base_mesh_cells":raw["mesh_cells"],
    "historical_outside_current_pilot":True})
 return rows
def get_rows(summary):
 rows=[]
 for p in summary["results"]:
  if p["result"]!="COMPLETED":continue
  data=json.loads((OUT/p["source_json"]).read_text())
  assert data["id"]==p["id"]
  rows.append(data)
 return rows
def nearest_model(rows,baselines):
 """Piecewise empirical nonnegative additive width model from the
  actually decomposed Taylor intervals, no least-squares extrapolation.
  Hess diagonal and off-diagonal corrections scale like h_i*h_j.
  In MVT mapping rho'/z to (R,tau), nominal factors are only proxies.
 """
 out={}
 for route in ("GENERAL","AXIS_MVT"):
  subset=[r for r in rows if r["route_from_position"]==route
        and r["group"] in ("A_LAMBDA_WIDTH","C_SPATIAL_BOX")]
  # Supplemental historical baseline observations have same interval schema.
  base=[]
  for p,spec in plan.PROBES.items():
   if spec["route"]==route:
    raw=json.loads((plan.BASE/(spec["baseline"]+".json")).read_text())
    # Baseline storage has a different Hess schema but same correction object.
    base.append(raw)
  all_data=subset+base
  if not all_data:
   out[route]={"model":"INSUFFICIENT_MEASUREMENTS"}
   continue
  names=("R","x","lam") if route=="GENERAL" else ("rho","z","lam")
  coeff=[median([d["center_point"]["halfwidth"] for d in all_data])]
  slopes=[]
  # For MVT these are effective local coefficients (rho,z vs nominal hR,hTau).
  for idx,k in enumerate(names):
   vals=[]
   for d in all_data:
    h=hc(d) if "geometric_halfwidths" in d else (
       (F(d["input_box"]["R"][1])-F(d["input_box"]["R"][0]))/2,
       (F(d["input_box"]["tau"][1])-F(d["input_box"]["tau"][0]))/2,
       (F(d["input_box"]["lambda"][1])-F(d["input_box"]["lambda"][0]))/2)
    half=float(h[idx])
    if not half:continue
    c=d["gradient"][k]["correction"]
    vals.append(c["halfwidth"]/half)
   slopes.append(median(vals))
  coeff.extend(slopes)
  interactions=((0,0),(0,1),(1,1),(0,2),(1,2),(2,2))
  hess_coef=[]
  for i,j in interactions:
   key=names[i]+"_"+names[j];vals=[]
   for d in all_data:
    if "geometric_halfwidths" in d:h=hc(d)
    else:
     h=tuple(float((F(d["input_box"][k][1])-F(d["input_box"][k][0]))/2)
               for k in ("R","tau","lambda"))
    denom=h[i]*h[j]
    if not denom:continue
    vals.append(d["hessian"][key]["correction"]["halfwidth"]/denom)
   hess_coef.append(median(vals))
  coeff.extend(hess_coef)
  assert len(coeff)==10
  observed=[];predicted=[]
  for d in all_data:
   if "geometric_halfwidths" in d:h=hc(d)
   else:h=tuple(float((F(d["input_box"][k][1])-F(d["input_box"][k][0]))/2)
              for k in ("R","tau","lambda"))
   pred=sum(a*b for a,b in zip(coeff,feature(h)))
   actual=d["H_interval"]["halfwidth"]
   observed.append(actual);predicted.append(pred)
  errors=[abs(p-o) for p,o in zip(predicted,observed)]
  out[route]={"status":STATUS,"model_type":"median interval-decomposition normalized by nominal halfwidths",
   "formula":"w_hat=sum(coefficients[i]*monomials[i]); all h are HALF widths",
   "monomials":list(MONOMIAL),
   "coefficients":[float(x) for x in coeff],
   "training_count":len(all_data),
   "test_abs_error_median":median(errors),"test_abs_error_max":max(errors),
   "test_rel_error_median":median([err/max(abs(v),1e-14)
                                    for err,v in zip(errors,observed)]),
   "near_lambda_5_only":True,
   "mvt_caveat":("The actual MVT external variables are rho_prime,z,lambda; "
    "nominal h_R and h_tau are NOT outer Taylor radii. "
    "No varying tau/R axis boxes were valid for C, so the spatial "
    "coefficients are NOT identified for general axis boxes." if route=="AXIS_MVT" else
     "Training boxes sample only P1/P2 and P1 spatial enlargements; "
     "not representative of entire R-tau board.")}
 return out
def scenarios(rows,baselines):
 completed=[x for x in rows if x["group"]!="D_LOW_LAMBDA"]
 by_probe={}
 for b in baselines:by_probe[b["id"]]=b
 route_new={"GENERAL":[],"AXIS_MVT":[]}
 for x in completed:
  if x["group"] in ("A_LAMBDA_WIDTH","B_HESSIAN_COARSE","C_SPATIAL_BOX"):
   route_new[x["route_from_position"]].append(x["timing"]["total_worker_s"])
 observed_averages={r:median(s) for r,s in route_new.items()}
 if not all(observed_averages.values()):
  return {"status":STATUS,"supported":False,
    "reason":"No measurements for both general and axis routes"}
 # hypothetical route share: 75% general,25% special (not inferred)
 perbox=.75*observed_averages["GENERAL"]+.25*observed_averages["AXIS_MVT"]
 table=[]
 for start_denom,frac in ((64,.25),(64,.5),(64,.75),
                           (32,.25),(32,.5),(16,.25),(16,.5)):
  # physical edge step 1/denom, min width1/256 => double splits in 2D
  levels=2*(int(round(math.log2(256/start_denom))))
  N=start_denom**2
  multiplier=sum((2*frac)**k for k in range(levels+1))
  one_plate=N*multiplier
  for plate_policy,plates in (
      ("uniform_1_8_on_2_to_5_UNVERIFIED",24),
      ("low_1_1024_on_2_to_3_plus_high_1_8_on_3_to_5_UNVERIFIED",1040),
      ("uniform_1_256_on_2_to_5_UNVERIFIED",768)):
   table.append({"initial_grid":f"{start_denom}x{start_denom}",
    "initial_R_tau_edge":f"1/{start_denom}","assumed_split_probability_each_level":frac,
    "binary_max_depth":levels,"expected_evaluations_per_first_cell":multiplier,
    "equivalent_boxes_per_plate":one_plate,
    "lambda_plate_policy":plate_policy,"hypothetical_plate_count":plates,
    "hypothetical_total_H_jobs":one_plate*plates,
    "workers":12,"assumed_worker_s_per_box":perbox,
    "hypothetical_wall_hours":one_plate*plates*perbox/(12*3600),
    "all_geometry_and_split_and_cost_hypothetical":True})
 return {"status":STATUS,"supported":True,
    "median_worker_seconds_by_route_near5":observed_averages,
    "assumed_unverified_route_fraction":{"GENERAL":.75,"AXIS_MVT":.25},
    "mixed_worker_seconds":perbox,
    "formula_evaluations_per_initial_cell":"sum_{k=0}^{2 log2(256/d)} (2 f)^k",
    "scope_note":"These are scenario arithmetic only; lambda≈2 and R outside sample are not measured.",
    "hypotheses":table}
def build():
 sm=json.load((OUT/"SUMMARY.json").open())
 rows=get_rows(sm)
 baselines=aggregate_baselines()
 model=nearest_model(rows,baselines)
 estimate=scenarios(rows,baselines)
 comparisons={"status":STATUS,
  "samples_completed":len(rows),"baseline_historical":baselines,
  "near5_full_mesh_baseline_hypothesis":"reuse historic 4-box baseline without new time charge",
  "modeled_width_by_route":model,
  "global_H_cost_scenarios":estimate,
  "mathematical_certification":False,"no_cover":True}
 (OUT/"COST_MODEL.json").write_text(json.dumps(comparisons,indent=2)+"\n")
 print(json.dumps({"status":STATUS,"completed":len(rows),
  "general_model":model.get("GENERAL",{}).get("coefficients"),
  "axis_model":model.get("AXIS_MVT",{}).get("coefficients"),
  "scenario_count":len(estimate.get("hypotheses",[])),
  "mathematical_certification":False},indent=2))
 return comparisons
if __name__=="__main__":build()
