"""Readable evidence receipt for C21 thin-slab adaptive cost measurements.
DIAGNOSTIC_ONLY / NOT_EVIDENCE. Uses observed data only.
"""
import json,collections,statistics
from pathlib import Path
from fractions import Fraction as F
OUT=Path("runs/2026-11-18/D_PRO_C21_SLAB_ADAPTIVE")
def read(name):
 p=OUT/name
 return json.loads(p.read_text()) if p.exists() else None
def build():
 cal=read("calibration_status.json")
 state=read("state.json")
 sm=read("summary.json")
 if not cal or not state or not sm:raise RuntimeError("calibration, state, summary required")
 rows=[]
 for c in cal["results"]:
  h=c.get("H_interval")
  rows.append(f"| {c['name']} | {c['status']} | "
   f"{'—' if h is None else format(h['halfwidth'],'.8g')} | "
   f"{c.get('wall_s',c.get('parent_wall_s')):.3f} | "
   f"{c.get('mesh_cells','—')} | {c.get('peak_RSS_KiB','—')} |")
 route_times="\n".join(
  f"| {key} | {sm['route_jobs'].get(key,0)} | {sm['route_worker_seconds_sum'].get(key,0):.3f} |"
  for key in ("AXIS","CENTER","BOUNDARY","REGULAR"))
 depths="\n".join(f"| {k} | {val} | {sm['depth_terminal'].get(k,0)} |"
  for k,val in sorted(sm["depth_processed"].items(),key=lambda x:int(x[0])))
 w=read("W_SAMPLE_RESULTS.json")
 extrap=""
 if sm["full_slab_processed"]:
  count=sm["measured_jobs"];wall=sm["H_adaptive_wall_s"]
  extrap=(f"Entire thin slab complete: {count} H box evaluations, "
      f"{wall:.2f}s H wall. If (UNPROVED) all λ slabs have the same "
      f"observed complexity, uniform thickness1/256 across [2,5] "
      f"is 768 slabs, giving {768*count} equivalent H evaluations "
      f"and {768*wall/86400:.2f} single-slab-wall-days. "
      f"An alternative UNPROVED thickness policy of 1/1024 in [2,3] "
      f"and 1/256 in [3,5] is 1536 slabs, giving "
      f"{1536*count} equivalent H evaluations and "
      f"{1536*wall/86400:.2f} days. These are CONDITIONAL "
      f"cost extrapolations, NOT covered boxes or measured global work.")
 else:
  extrap=(f"Full slab incomplete: {sm['pending_UNEVALUATED_count']} "
    f"uncomputed rectangles remain with exact area "
    f"{sm['area_pending_exact']}. NO all-λ cost extrapolation, "
    f"and NO claimed final slab box count. Even an optimistic "
    f"cost forecast cannot be grounded before pending regions "
    f"are measured at the fixed rule.")
 tube=sm["tube_coordinates"]
 terminal=state["terminal"]
 decided=[r for r in terminal if r["kind"]=="DECIDED_NONZERO"]
 left=tuple(sm["plate_lambda"])
 dists=[]
 for r in tube[:30]:
  dists.append(f"| {r['id']} | {r['R'][0]}..{r['R'][1]} | "
    f"{r['tau'][0]}..{r['tau'][1]} | {r['area']} | {r['reason']} |")
 if len(tube)>30:dists.append(f"| ... {len(tube)-30} additional | see summary.json | | | |")
 report=f"""# C21 adaptive H slab: execution receipt

**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

Research scope: **only λ∈[{left[0]},{left[1]}]**, normalized
(R,τ)∈[0,1]². No broader λ region has been covered.
Frozen calibration commit and fixed adaptive plan are in the
GitHub new-branch history. H evaluation is 128-bit Arb using
frozen R3 spatial Taylor quadrature. Source version: python-flint 0.8.0.

## Calibration before adaptive cover

| Route | Status | H halfwidth | Wall s | Cells | Peak RSS KiB |
|---|---|---:|---:|---:|---:|
{chr(10).join(rows)}

Calibration total elapsed wall {cal['total_parent_wall_s']:.3f} seconds.

## Actual measured adaptive counts

- Initial rational partition: **256 boxes**.
- H jobs actually executed: **{sm['measured_jobs']}** (unique IDs:
  {sm['measured_unique_nodes']}).
- Resolved nonzero H boxes: **{sm['decided_count']}**.
- Evaluated zero/min-width and timed-out/error tube candidates:
  **{sm['tube_candidate_EVALUATED_count']}**.
- Remaining UNCOMPUTED boxes: **{sm['pending_UNEVALUATED_count']}**.
- Zero-containing parent boxes split: **{sm['split_parents']}**.
- Is the fixed λ slab fully evaluated? **{sm['full_slab_processed']}**.
- Cumulative total experiment wall including calibration:
  **{sm['total_experiment_wall_s_including_calibration']:.3f}s**.
- Adaptive H sessions wall:
  **{sm['H_adaptive_wall_s']:.3f}s**.
- Three-box W samples wall (separate): **{sm['W_sample_wall_s']:.3f}s**.

### Exact rational area ledger

- Decided: **{sm['area_decided_exact']}**
- Evaluated tube candidates: **{sm['area_tube_evaluated_exact']}**
- Pending uncomputed: **{sm['area_pending_exact']}**
- Area sum: **{sm['area_partition_sum_exact']}**
- Evaluated tube plus *uncomputed pending* worst-case upper area:
  **{sm['area_potential_tube_including_pending_exact']}**.

Do NOT count the pending area as a measured tube region.
The desired two-way identity (decided + tube =1) holds
**only when pending=0**. If partial, the three-way identity is the
appropriate exact check.

### Counts by H route

| Route | Number of measured jobs | Sum of worker execution seconds |
|---|---:|---:|
{route_times}

### Counts by split depth

| Depth | Evaluated | Terminal |
|---|---:|---:|
{depths or '| 0 | 0 | 0 |'}

### Evaluated tube candidate distribution (up to first 30)

| ID | R bounds | τ bounds | Exact area | Reason |
|---|---|---|---|---|
{chr(10).join(dists) if dists else '| — | — | — | — | No terminal tube candidates yet |'}

All evaluated H-box inputs/outputs, finite enclosures, reasons
for OPEN, wall seconds, peak RSS and mesh cell counts are in
`boxes/`, `logs/`, `state.json`, and `summary.json`.
A per-box `H_interval=null` means no interval was produced.

## W: exactly three tube samples, if eligible

Selection rule: sorted evaluated tube IDs, first/middle/last,
frozen only when the slab is finished or the 24h cap is reached.
W uses pinned R3's second-order angular quotient, not CW7.
Status: **{"measured" if w else "OPEN / not launched"}**.
There is NO tube-wide W calculation.

## Cost inference permitted by the observed data

{extrap}

The `N_H × t_H + N_W_tube × t_W` cost model must account for
W separately; no W tube count is assumed.

## Audit and reproducibility

- Any `checker.json` tests exact output consistency, not
  independent mathematics of the interval quadrature.
- Fixed rules: `CALIBRATION_RULE_FREEZE.md`,
  `COVER_RULE_FREEZE.md`, `INTERACTIVE_SUBRUN_FREEZE.md`.
- Restart: the controller reads `state.json`, including a
  recovered inflight batch if necessary, and writes atomically.
- Any shortened interactive run remains explicitly PARTIAL.
- Original R3, prior C21 branches, main, STATE.md and Julia
  have not been changed.

**DIAGNOSTIC_ONLY / NOT_EVIDENCE. C21 global condition: OPEN.**
"""
 (OUT/"RUN_RECEIPT.md").write_text(report)
 print(json.dumps({"measured":sm["measured_jobs"],
     "pending":sm["pending_UNEVALUATED_count"],
     "full_slab":sm["full_slab_processed"],
     "total_wall":sm["total_experiment_wall_s_including_calibration"],
     "receipt_lines":len(report.splitlines())},indent=2))
if __name__=="__main__":build()
