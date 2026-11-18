"""Create comprehensive C21 diagnostic receipt from immutable JSON records.
DIAGNOSTIC_ONLY / NOT_EVIDENCE, no math computation.
"""
import json,statistics
from pathlib import Path
from fractions import Fraction as F
OUT=Path("runs/2026-11-18/D_PRO_C21_H_PILOT")
STATUS="DIAGNOSTIC_ONLY / NOT_EVIDENCE"
NAMES=["G2","G35","AX","EQ","CE","BD"]+[f"STRIP_{k:02}" for k in range(16)]+["LW"]
def read(name):
 p=OUT/name
 return json.loads(p.read_text()) if p.exists() else None
def n(v):
 return f"{v:.5f}" if isinstance(v,(int,float)) else str(v)
def build():
 rows=[]
 for name in NAMES:
  a=read(name+".json")
  if not a or "H_interval" not in a:
   rows.append(f"| {name} | OPEN | — | — | — | — | — | — |")
   continue
  h=a["H_interval"]; dirs=a["directional_contributions"]
  cols=[]
  for ax in ("R","x","lam"):
   d=dirs[ax]
   p=d.get("outer_halfwidth_contribution",d.get("halfwidth_contribution"))
   cols.append(n(p["halfwidth"]))
  rows.append(f"| {name} | [{n(h['lo'])}, {n(h['hi'])}] | {n(h['halfwidth'])} | "
    f"{'YES' if a['zero_included_RECORD_ONLY'] else 'NO'} | {n(a['wall_s'])} | "
    f"{a['peak_RSS_KiB']} | {a['mesh_cells']} | {', '.join(cols)} |")
 calnames=["G2","G35","EQ","STRIP_08","LW"]
 fine=[]
 fine_times=[]
 for name in calnames:
  a=read(name+("_cal_fine" if name=="LW" else "_cal_v2")+".json")
  if not a or "H_interval" not in a:
   fine.append(f"| {name} | OPEN | — | — | — |")
   continue
  h=a["H_interval"];fine_times.append(a["wall_s"])
  fine.append(f"| {name} | [{n(h['lo'])},{n(h['hi'])}] | {n(h['halfwidth'])} | {n(a['wall_s'])} | {a['mesh_cells']} |")
 b4axis=read("W_B4_AXISDEPTH.json")
 b4u=read("W_B4_U_VARIANT.json")
 wrows=[]
 for title,data in (("AxisDepth16",b4axis),("ContactU",b4u)):
  if data:
   for j,c in enumerate(data["children"]):
    k=c.get("child",[j//2,j%2])
    wrows.append(f"| {title} | {k} | {str(c.get('rigorous_full_B4_cover'))} | "
      f"{c.get('stop_reason')} | {c.get('partial_accepted_patches')} | {n(c.get('wall_s'))} |")
 refs=read("primitive_E_hires.json")
 rrows=[]
 if refs and refs.get("complete"):
  for a in refs["all"]:
   h=a["n160"]["H_center_num"]
   rrows.append(f"| {a['name']} | {h} | {a['quadrature_absolute_difference']} | "
      f"{a['coarse_interval_contains_both']} | {a['fine_interval_contains_both']} |")
 summary=read("summary.json") or {}
 fit=summary.get("time_model",{})
 durations=[float(x) for x in fine_times]
 medfine=statistics.median(durations) if durations else 0
 Ncases=(24576,49152,196608)
 scenarios=[]
 for N in Ncases:
  ideal_s=N*medfine/12
  scenarios.append(f"| {N:,} | {ideal_s/86400:.2f} days | {(ideal_s/0.7)/86400:.2f} days |")
 report=f"""# D-PRO (C21) representative pilot: reproducible run receipt

2026-11-18 / **{STATUS}**

## Scope

Judge chose the (C21) route. This run is strictly a **representative
box cost-and-width survey**, NOT a global covering, sign certificate
or proof of the large prolate theorem. No H or W sign was used to choose
the algorithm. All raw JSON and logs, including failures, are retained.

All runtime measurements: daybreak-works, Python3.11.16,
python-flint0.8.0, 128-bit Arb, one measured process at a time.

## Direct horizontal geometry and special branches

- Direct lab horizontal `f_rho` for regular boxes; the full primitive
  derivation and the `f_rho_rho` formula are in
  `prolate_r4/ANALYSIS_C21.md`.
- AX, CE and STRIP_00: apply the evenness identity
  `H = integral_0^1 E_rho_rho(s rho,z) ds`, with the four-panel
  Simpson-in-s and an interval 4th-derivative remainder.
- BD and STRIP_15: fixed contact cap kappa=1/4096; single final cap
  correction uses the proven `|f_rho| <= pi^2/4 + pi(1+lambda_max)`.
- All signed angular integrals (including external gradients) use
  degree-4 spatial Taylor, not CW7 range×area summation.
- Frozen first-pass mesh: 8×16, ratio2; timeout120s.
- Derived horizontal 2nd derivative and frozen R3 `fxx` agree
  in all 9 fixed pointwise interval tests. This is not an independent
  proof of the complete spatial integrator.

## All 23 preselected first-pass representative boxes

**Each H interval and directional contribution is a producer Arb
interval pending independent mathematical audit.** Last column lists
(R, tau, lambda) correction halfwidths.

| Box | H producer interval (display) | Halfwidth | Contains zero (record only) | Wall s | Peak RSS KiB | Cells | Outer directional halfwidths |
|---|---|---:|---|---:|---:|---:|---|
{chr(10).join(rows)}

**First pass:** {summary.get('completed',0)}/23 completed.
AX 4-panel Simpson timed out at the frozen 120-second cap
and is **OPEN**; no partial interval was substituted.
A separately frozen AX fallback using the uniform `s in [0,1]`
interval and signed angular Taylor did produce an enclosure,
but its width is much larger, and it is not a retroactive
replacement for the AX initial run.

## Separate pre-registered fine-mesh calibrations

These are DIFFERENT mesh policies, not repairs to the first-pass
result. Base_u=16, base_v=32, ratio=1/2, order4.
The original four-case refinement is documented in
`FIXED_CALIBRATION_V2.md`; LW is a separate pre-registered case.

| Box | H interval | Halfwidth | Wall s | Cells |
|---|---|---:|---:|---:|
{chr(10).join(fine)}

## Independent numerical primitive-E references

The 25-digit mpmath primitive E 5-point rho derivative was
integrated by 96×96 and 160×160 Gauss-Legendre rules, with
h=0.004, holding z fixed. These do **not** have rigorous
truncation or quadrature error enclosures. Their 2-grid
disagreement measures only an observed numerical change.

| Box | 160×160 H numerical value | 96/160 difference | In coarse producer interval | In fine producer interval |
|---|---:|---:|---|---|
{chr(10).join(rrows)}

The AX coarse producer interval is OPEN, so its pointwise
containment is reported as null, not FAIL.

## W tube B4 gate

The v35 child layout R×tau=2×2, unsplit lambda, A<=1/4,
B4 integral<=0.03 was preserved.
The shared depth cap was first replaced by **per-axis depth16**
(frozen first variant); a second **u=tan(psi/4) contact coordinate**
variant was also independently frozen before its run.

| Fixed variant | Child | Full B4 cover | Stop | Partial accepted patches (not an enclosure) | Wall s |
|---|---|---|---|---:|---:|
{chr(10).join(wrows)}

**Neither variant produced a complete B4 integral over a child.**
The signed 35-coefficient W integration was NOT started. No W
tube cost or zero-exclusion proof can be claimed.

## Empirical cost and global-scope caution

Regular-route first-pass cost regression **on measured boxes only**:

`{fit.get('T_seconds_approx','not available')}`.
Fitted R²: {fit.get('R2_within_measured_boxes','OPEN')}.
This is principally a per-cell micro-cost calibration; it does
NOT predict the number of cells needed for a new box or
the sign width.

For the {len(durations)} separate fine-mesh cases, median elapsed
`{n(medfine)}` seconds. Hypothetical counts below use that median
and 12 ideal workers (70% efficiency second column); none of the
listed box counts is a validated global H cover:

| Hypothetical H boxes | Ideal 12-worker time | At assumed 70% efficiency |
|---|---:|---:|
{chr(10).join(scenarios)}

**H≈0 tube cost is separate and unknown**:
`T_total ~ N_H*t_H/workers + N_W_tube*t_W/workers`.
No tube box count, global coverage or W child cost is established.
In particular, extending sign resolution to AX/CE/BD and
lambda widths beyond the sampled cases remains OPEN.

## Record integrity and audit status

The standard-library `c21_checker.py` checks exact rational
bounds, first-order contribution sums, the fixed input boxes,
and zero flags against the stored JSON. It is NOT an independent
derivation or verification of R3 quadrature.
The complete symbolic identities, near-axis construction, and
cap error estimates must be independently audited before being
used for evidence. The parent R3 source is pinned read-only,
with file-by-file SHA-256 comparison in the final package.

No changes to main, STATE.md, R3, old v2/v3 branches, or Julia.

**DIAGNOSTIC_ONLY / NOT_EVIDENCE. Global condition A and (C21)
exclusion theorem: OPEN.**
"""
 (OUT/"RUN_RECEIPT.md").write_text(report)
 (OUT/"RUN_COMMAND.txt").write_text(
  "cd /home/daybreak/D_PRO_C21_H_PILOT_20261118/worktree && "
  "PYTHONPATH=/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source "
  "/home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python "
  "-m prolate_r4.c21_batch\n")
 print(json.dumps({"receipt_lines":len(report.splitlines()),
  "completed":summary.get("completed"),"fine":len(durations),
  "W_axis":b4axis.get("all_four_full_B4_cover") if b4axis else None,
  "W_u":b4u.get("all_four_full_B4_cover") if b4u else None,
  "reference":bool(refs and refs.get("complete"))},indent=2))
if __name__=="__main__":build()
