"""Conservative summary and empirical cost model for fixed C21 box pilot.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Never infer signs or missing boxes.
"""
import json,statistics,math
from pathlib import Path
from fractions import Fraction as F
from .c21_regular import BOXES as REG
from .c21_special import BOXES as SP,SPECIAL
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
OUT=Path("runs/2026-11-18/D_PRO_C21_H_PILOT")
NAMES=["G2","G35","AX","EQ","CE","BD"]+[f"STRIP_{i:02}" for i in range(16)]+["LW"]
def run():
 reports={};rows=[]
 for name in NAMES:
  path=OUT/(name+".json")
  if not path.is_file():state="OPEN";reason="missing result";doc={}
  else:
   try:doc=json.loads(path.read_text());state="COMPLETED" if "H_interval" in doc else "OPEN"
   except Exception as ex:state="OPEN";doc={"error":str(ex)}
   reason=doc.get("error") if state=="OPEN" else None
  reports[name]=doc
  if state=="COMPLETED":
   box=doc["input_box"]
   widths={p:float(F(b[1])-F(b[0])) for p,b in box.items()}
   row={"name":name,"status":state,"route":doc["route"],
     "R_mid":sum(map(lambda x:float(F(x)),box["R"]))/2,
     "input_width":widths,"H":doc["H_interval"],
     "halfwidth":doc["H_interval"]["halfwidth"],
     "relative_halfwidth":doc["normalized_halfwidth"],
     "zero_included_RECORD_ONLY":doc["zero_included_RECORD_ONLY"],
     "time_seconds":doc["wall_s"],
     "mesh_cells":doc["mesh_cells"],
     "peak_RSS_KiB":doc["peak_RSS_KiB"],
     "directional_halfwidths":{a:d.get("outer_halfwidth_contribution",d.get("halfwidth_contribution",{})).get("halfwidth",None) for a,d in doc["directional_contributions"].items()},
     "spatial_point_halfwidth":doc["center_point"]["halfwidth"] if "center_point" in doc else doc["H_center_point"]["halfwidth"],
     "cap_halfwidth":doc.get("cap_correction",{}).get("halfwidth",0)}
   rows.append(row)
  else:rows.append({"name":name,"status":state,"reason":reason})
 good=[r for r in rows if r["status"]=="COMPLETED"]
 direct=[r for r in good if r["route"]=="regular direct f_rho/rho"]
 if len(direct)>1:
  n=[p["mesh_cells"] for p in direct]
  t=[p["time_seconds"] for p in direct]
  mean_n=statistics.mean(n);mean_t=statistics.mean(t)
  cov=sum((a-mean_n)*(b-mean_t) for a,b in zip(n,t))
  var=sum((a-mean_n)**2 for a in n)
  b=cov/var if var else 0;a=mean_t-b*mean_n
  fit=[a+b*x for x in n]
  err=sum((x-y)**2 for x,y in zip(t,fit))
  rss=sum((x-mean_t)**2 for x in t)
  R2=1-err/rss if rss else None
  reg={"T_seconds_approx":f"{a:.3g} + ({b:.3g}) * mesh_cells",
       "intercept_s":a,"seconds_per_cell":b,
       "R2_within_measured_boxes":R2,"sample_count":len(direct),
       "warning":"Only measured mesh policy; not transferable to new box geometry."}
 else:reg={"status":"insufficient data"}
 strip=[r for r in good if r["name"].startswith("STRIP_")]
 zero=[r["name"] for r in strip if r["zero_included_RECORD_ONLY"]]
 med=statistics.median([r["time_seconds"] for r in good]) if good else None
 result={"status":STATUS,"scope":"fixed representative pilot only",
   "box_count_planned":23,"completed":len(good),"uncomputed":len(rows)-len(good),
   "zero_included_strip_boxes_RECORD_ONLY":zero,
   "zero_not_included_strip_boxes_RECORD_ONLY":[r["name"] for r in strip if not r["zero_included_RECORD_ONLY"]],
   "completed_strips":len(strip),
   "time_model":reg,"representative_median_seconds":med,
   "time_scenario_only":{
     "hypothetical_H_boxes":[49152,98304,196608],
     "formula":"T_ideal_seconds=N_H*(a+b*cell_count)/workers, plus N_tube*t_W/workers",
     "W_tube_box_count":"unknown; must be counted separately",
     "workers_for_scenarios":12,
     "fixed_box_count_claim":None},
   "rows":rows,"condition_C21":"OPEN",
   "note":"Sign only recorded, not used to select computation. No full cover."}
 (OUT/"summary.json").write_text(json.dumps(result,indent=2)+"\n")
 (OUT/"SUMMARY.md").write_text(
 f"# D-PRO C21 representative summary\n\n**DIAGNOSTIC_ONLY / NOT_EVIDENCE**\n\n"
 f"Measured {len(good)}/23 fixed boxes, {len(strip)}/16 STRIP boxes.\n"
 f"Empirical regular-route cost: `{reg.get('T_seconds_approx','OPEN')}`, "
 f"R²={reg.get('R2_within_measured_boxes')}.\n"
 f"Median completed runtime {med} seconds.\n"
 f"STRIP intervals containing zero (RECORD ONLY): {', '.join(zero)}.\n"
 f"The signed spatial integration was order 4 with the fixed coarse mesh.\n"
 f"Any W tube costs and the global H box count remain OPEN.\n"
 f"See `summary.json`, individual logs, and `FIXED_PLAN.md`.\n")
 print(json.dumps({"complete":len(good),"regular_fit":reg,"median":med,"strips":len(strip)},indent=2))
if __name__=="__main__":run()
