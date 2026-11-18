"""Measured-only checkpoint report for C21 1/4-width slab.
DIAGNOSTIC_ONLY / NOT_EVIDENCE.
"""
import json,statistics,collections
from pathlib import Path
from fractions import Fraction as F
OUT=Path("runs/2026-11-18/D_PRO_C21_SLAB_PART")
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
def load(path):
 f=OUT/path
 return json.loads(f.read_text()) if f.exists() else None
def build():
 cal=load("CE_calibration_status.json")
 sm=load("summary.json")
 state=load("state.json")
 if not cal or not sm or not state:raise RuntimeError("CE/status/state/summary required")
 assert sm["area_partition_sum_exact"]=="1/4"
 w=load("W_SAMPLE_RESULTS.json")
 tube=sm["tube_coordinates"]
 special_rows=[]
 special_total=0
 for path in sorted((OUT/"boxes").glob("*.json")):
  info=json.loads(path.read_text())
  rt=info.get("route_from_position",info.get("route"))
  if rt not in ("AXIS_MVT","SMALL_RHO_MVT","CENTER_MVT"):continue
  special_total+=1
  if len(special_rows)>=25:continue
  hiv=info.get("H_interval")
  width="—" if not isinstance(hiv,dict) else format(hiv["halfwidth"],".8g")
  seconds=info.get("worker_elapsed_s",info.get("measurement_wall_s",float("nan")))
  special_rows.append(f"| {info.get('name',info.get('id'))} | {rt} | {width} | {seconds:.3f} | {info.get('mesh_cells',info.get('mesh_cells_observed','—'))} | {info.get('peak_RSS_KiB',info.get('peak_RSS_KiB_sampled_lower','—'))} |")
 route_rows=[]
 for r in ("AXIS_MVT","SMALL_RHO_MVT","GENERAL","CENTER_MVT"):
  route_rows.append(f"| {r} | {sm['route_jobs'].get(r,0)} | {sm['route_worker_seconds_sum'].get(r,0):.3f} |")
 split_rows=[]
 for depth,c in sorted(sm["depth_processed"].items(),key=lambda x:int(x[0])):
  split_rows.append(f"| {depth} | {c} | {sm['depth_terminal'].get(depth,0)} |")
 tubes=[]
 for row in tube[:40]:
  tubes.append(f"| {row['id']} | {row['R'][0]}–{row['R'][1]} | {row['tau'][0]}–{row['tau'][1]} | {row['area']} | {row['reason']} |")
 status="COMPLETE" if sm["full_subregion_processed"] else "PARTIAL_UNFINISHED"
 if sm["full_subregion_processed"]:
  hypothetical_full_count=sm["measured_jobs"]*4
  hypothetical_full_wall=sm["H_adaptive_wall_s"]*4
  extrap=f"""The actual requested subregion is complete. Under the UNVERIFIED
  equal-cost-per-area hypothesis ONLY, the full Rτ board would have
  {hypothetical_full_count} equivalent H evaluations and take approximately
  {hypothetical_full_wall:.2f} seconds (per-plate wall-time proxy).
  Extending to λ∈[2,5] with thickness1/256 everywhere (768 slabs)
  would imply {hypothetical_full_count*768} equivalent H evaluations;
  this thickness is not justified near λ≈2.
  Alternative hypothetical widths1/1024 on [2,3] and1/256 on
  [3,5] give 1536 slabs, also not rigorously justified."""
 else:
  extrap=f"""The current subregion has {sm['pending_UNEVALUATED_count']}
  pending boxes with exact measure {sm['area_pending_exact']}.
  Therefore its *total* required H box count/time and its final
  unresolved tube area are NOT MEASURED.
  No full-Rτ-board or full-λ-range box count or time forecast is made.
  Hypothetical slab counts: uniform1/256 across [2,5] =768 slabs,
  or λ thickness1/1024 on [2,3] (1024) plus1/256 on [3,5]
  (512), total1536 slabs; neither justifies extrapolating the
  currently incomplete region or proves λ≈2 enclosure."""
 content=f"""# D-PRO C21 partial slab adaptive H diagnostic receipt
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

Execution state **{status}**. Only λ∈[1279/256,5],
R∈[1/4,1/2], τ∈[0,1] (area **1/4**). NOT a global or full
λ-slab cover.

Frozen new MVT route: `PRE_RUN_FREEZE.md`, pre-run commit
`d71522c19b9998d6640adf9d8542227690fe560b`.
Controller committed before H experiment as `61069b5c94b795af8277fa60767fa7fabdcccf42`.
Original C21 source `5004ebdc6e038bcdb3122f563ffb15d38070d8b6`,
R3 source pin `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`,
V37 `949e9dff7b48cf993cdb9fae95ec698f482cd591`.
All sign results are diagnostics; only binary zero inclusion directs
the adaptive algorithm.

## 1. Preregistered CE one-box MVT calibration
- Status: **{cal['result']}**.
- Wall time: **{cal['wall_s']:.3f} seconds**.
- Signed H interval: **{cal.get('H_interval')}**.
- Angular cell count: **{cal.get('mesh_cells')}**.
- Peak child RSS KiB: **{cal.get('peak_RSS_KiB')}**.
- No s-Simpson quadrature used.
- Fixed independent derivative parameters: rho', z, λ;
  physical primitive-E reference vertical coordinate p_z=λz.

## 2. Measured main partial-slab H work
- Initial 1/64×1/64 boxes: **1024 (16×64)**.
- Actual measured H jobs: **{sm['measured_jobs']}**, unique:
  **{sm['measured_unique_nodes']}**.
- Decided nonzero boxes: **{sm['decided_count']}**.
- EVALUATED terminal tube candidates (including per-box OPEN):
  **{sm['tube_candidate_EVALUATED_count']}**.
- PENDING / not yet evaluated: **{sm['pending_UNEVALUATED_count']}**.
- Split parents: **{sm['split_parents']}**.
- Main adaptive wall time **{sm['H_adaptive_wall_s']:.3f}s**.
- Total wall incl CE **{sm['total_experiment_wall_s_including_calibration']:.3f}s**.
- W sample wall **{sm['W_sample_wall_s']:.3f}s**.
- Sum of all worker CPU wall times by route is below (not
  the same as whole elapsed wall).

### Exact unnormalized area in (R,τ)
- Decided **{sm['area_decided_exact']}**.
- Evaluated tube candidates **{sm['area_tube_evaluated_exact']}**.
- Pending not evaluated **{sm['area_pending_exact']}**.
- Exact sum **{sm['area_partition_sum_exact']}** (=1/4).

### Relative to requested region of measure 1/4
- Decided **{sm['area_decided_normalized_exact']}**.
- Evaluated tube **{sm['area_tube_normalized_exact']}**.
- Unmeasured pending **{sm['area_pending_normalized_exact']}**.
- Sum 1 exactly. Do not call uncomputed pending a measured tube.

### Special MVT routes: measured H halfwidth and cost (first25 of {special_total})
| Box ID | Route | H halfwidth | Worker s | Mesh cells | Peak RSS KiB |
|---|---|---:|---:|---:|---:|
{chr(10).join(special_rows) if special_rows else '| — | — | — | — | — | — |'}

### Measured H jobs and worker time by route
| Route | Jobs | Sum of worker wall seconds |
|---|---:|---:|
{chr(10).join(route_rows)}

### Depth counts
| Depth | Measured jobs | Terminal |
|---|---:|---:|
{chr(10).join(split_rows) if split_rows else '| — | 0 | 0 |'}

### Observed tube candidate distribution (first40)
| Immutable ID | R interval | τ interval | Area | Reason |
|---|---|---|---|---|
{chr(10).join(tubes) if tubes else '| — | — | — | — | No final tube candidates |'}

For ALL tube candidates and PENDING coordinates inspect `summary.json`.
Each executed box has a separate JSON and stdout/stderr log;
successful H intervals include rigorous rational endpoints and
cell-count, time, peak child RSS; timed-out boxes have null H
and sampled VmHWM KiB lower bounds, clearly labelled.

## 3. W three-box tube time and width
- Status **{"MEASURED" if w else "OPEN / DEFERRED"}**.
- The frozen rule selects first/middle/last sorted terminal tube
  IDs only after the entire requested subregion is finished or
  the genuine 24h wall cap is reached.
- This checkpoint does not silently substitute a small convenience
  sample. Full-tube W is NEVER calculated.

## 4. Cost outside the requested region
{extrap}

These cost statements, if present, remain
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**, and no all-λ theorem is claimed.

## 5. Reproducibility and audit scope
Sources `prolate_r4/c21_slabpart_*.py`, frozen rule
`PRE_RUN_FREEZE.md`, `state.json` checkpoint,
`summary.json`, checker `checker.json`.
Independent exact-fraction checker verifies partition and
source records but does not mathematically certify the Arb
quadrature. The old R3 chart-based distance heuristic is used
ONLY to generate the angular cell partition: because the MVT
extension point is not necessarily chart-aligned, it must NOT
be used as a distance proof. The integrand's independent
positive lower bound D≥1−(rho_hi+z_hi)>0 is applied to ALL
Taylor coefficients. Complete mathematical auditing remains OPEN.
No changes to main, STATE.md, Julia, or earlier branches.
"""
 (OUT/"RUN_RECEIPT.md").write_text(content)
 print(json.dumps({"status":STATUS,"measured":sm["measured_jobs"],
   "pending":sm["pending_UNEVALUATED_count"],
   "complete":sm["full_subregion_processed"],
   "receipt_lines":len(content.splitlines())},indent=2))
if __name__=="__main__":build()
