"""Human readable checkpoint, transparent incomplete area and cost.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
import json,datetime
from . import c21_heavy_cover as c
STATUS=c.STATUS;OUT=c.OUT
def build():
 st=c.readstate()
 v=c.counts(st)
 checker=OUT/"CHECKER.json"
 ck=json.loads(checker.read_text()) if checker.exists() else None
 lines=["# D-PRO (C21) — Heavy λ slab adaptive H diagnostic checkpoint",
 "**DIAGNOSTIC_ONLY / NOT_EVIDENCE**","",
 "λ ∈ [79/16,5] unsplit; (R,τ)∈[0,1]².",
 "Fixed rules and exact initial 4096 roots: PRE_RUN_FREEZE.md and REGISTRY.json.",
 "The fixed experiment code and root order were committed before H run.",
 "",
 "## Coverage accounting (not a certified H sign)","",
 "| State | Boxes | R×τ area, exact rational |",
 "|---|---:|---:|",
 f"| Evaluated decided nonzero H | {v['decided_count']} | {v['decided_area_exact']} |",
 f"| Evaluated terminal tube candidates | {v['tube_evaluated_count']} | {v['tube_area_exact']} |",
 f"| PENDING_UNEVALUATED (NOT a tube) | {v['pending_unprocessed_count']} | {v['pending_area_exact']} |",
 f"| Sum | — | {v['area_total_exact']} |",
 "",
 f"Initial roots: **4096**. Processed attempts: {v['attempted_terminal_or_split_nodes']}.",
 f"Completed H boxes: {v['evaluated_complete_nodes']}.",
 f"OPEN error/timeouts: {v['failed_OPEN_nodes']}.",
 f"Zero-containing split parents: {v['split_parent_count']}.",
 f"Observed split frequency among completed interval boxes: {v['observed_split_fraction_of_completed_evaluated']}.",
 "**This split rate is on processed boxes only, not on 4096 roots.**",
 "No attempt to fill unmeasured area with a guess.",
 "",
 "## Measured costs","",
 f"Cumulative wall time actually charged to 36h cap: {v['elapsed_wall_cumulative_s']:.3f} s.",
 f"Worker time sum (including session-interrupted work): {v['H_worker_seconds']:.3f} s.",
 "Global wall cap 129600s (36h). Per box limit1200s, workers12.",
 "Each operation session may end earlier; a session checkpoint",
 "must NOT be labeled 36h exhaustion or complete slab.",
 "",
 "## Route × depth measured counts and worker times",
 "",
 "| Route and depth | Processed count | Worker seconds |",
 "|---|---:|---:|"]
 for route in sorted(v["route_depth_processed"]):
  lines.append(f"| {route} | {v['route_depth_processed'][route]} | {v['route_depth_worker_seconds'][route]:.3f} |")
 lines+=["","## Evaluated tube coordinates and chart","",
 "Tube types: "+json.dumps(v["tube_by_kind"],ensure_ascii=False)+".",
 "Coordinates of **evaluated** terminal tubes are in",
 "SUMMARY.json under tubes_coordinates.",
 "TUBE_DISTRIBUTION.svg draws only terminal measured outcomes;",
 "the large gray area is PENDING_UNEVALUATED, not a sign result.",
 "",
 "## Full λ domain cost extrapolation (conditional, not a prediction)","",
 "V40's independent cost-only local λ≈2 data measured",
 "P1 ≈106.50s, P3 ≈88.38s on λ=[2,17/8] with H halfwidths",
 "0.09797 and 0.05314, respectively. Those samples are",
 "NOT a full λ≈2 slab and do not establish safe plate widths.",
 "Original V40 36-plate scenario (near5 width1/16 and near2 width1/8)",
 "was hypothetical ~26 days with12 workers BEFORE spatial splitting",
 "and W costs. It is not updated by partial-board sampling.",
 "",
 "GLOBAL H COST STATUS: "+v["global_cost_estimate"]+".",
 "Until a representative entire λ≈5 plate or genuine 36h cap",
 "is measured, the full-board split fraction and terminal tube",
 "area are unknown. Low-λ width remains a separate hypothetical assumption.",
 "",
 "## W three-box timing","",
 v["W_status"],
 "Sorted first/median/last tube selection is frozen, but",
 "is deferred until full plate completion or actual cumulative36h",
 "and at least three evaluated tubes. Arbitrary interim tubes",
 "cannot substitute for frozen W sample selection.",
 "",
 "## Independent checks and E-reference","",
 f"Exact interval/checkpoint ledger checker: {ck['verdict'] if ck else 'NOT_RUN'}.",
 "Direct-E sample status: see E_REFERENCE_STATUS.json if present;",
 "do not treat missing reference or any finite differences near rho=0",
 "as proof of the axis point.",
 "This is a measurement of a computational procedure, NOT a proof.",
 "**DIAGNOSTIC_ONLY / NOT_EVIDENCE — C21 global theorem OPEN.**"]
 (OUT/"RUN_RECEIPT.md").write_text("\n".join(lines)+"\n")
 print(json.dumps({"status":STATUS,"receipt_lines":len(lines),
        "sampled":v["attempted_terminal_or_split_nodes"],
        "pending":v["pending_unprocessed_count"]}))
if __name__=="__main__":build()
