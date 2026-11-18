# D-PRO C21 / second-order outer enclosure — PRE-RUN FREEZE
2026-11-18 • **DIAGNOSTIC_ONLY / NOT_EVIDENCE**

**Preregistration required BEFORE ANY second-order test call.**
New branch only: `research/d-pro-c21-h-second-order-20261118`.
Inputs: 84-box pilot `2e3a091ad3c7a98a5962b8c016d2e1fb51bcf0e9`;
V38 `922a2c7eaed62b6c40d1bf9b0e956f98a85fd104`;
C21 base `5004ebdc6e038bcdb3122f563ffb15d38070d8b6`;
R3 frozen `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`.

## Stage A: eight fixed initial 1/64 boxes

Take sorted *GENERAL* box IDs from all 84 measured nodes, indices
0,11,22,33,44,55 (zero-based, stride 11). Take sorted AXIS_MVT
box IDs at the first and last indices. Exact frozen selections:

1. `R16_T00` (GENERAL)
2. `R18_T08` (GENERAL)
3. `R20_T48` (GENERAL)
4. `R23_T32` (GENERAL)
5. `R26_T00` (GENERAL)
6. `R28_T32` (GENERAL)
7. `R16_T63` (AXIS_MVT)
8. `R31_T63` (AXIS_MVT)

All inputs exactly reuse each named node's previous `input_box`
from the frozen 84-box commit. No post-results selection.

## Stage A numerical rule

Outer centers and halfwidths are **exact rational midpoints** of:
- GENERAL: independent outer `(R,τ,λ)`, original c21_regular.dens;
- AXIS/SMALL_RHO/CENTER: independent `(ρ',z,λ)` extension
  `rho'=[0,rho_hi],z=[zlo,zhi]`, fixed angular chart
  `(tau_lo+tau_hi)/2`, original `c21_slabpart_mvt.density_rr`.
  No Simpson or quadrature in `s`. Route selection and positive
  distance logic from frozen slabpart MVT source; no switching back.
- `H(p0)`: signed order4 spatial Taylor integral at point center.
- `∂i H(p0)`: signed order4 angular integral of mixed
  spatial-order-n / external-order-1 jet, with ALL external
  variables held as **points**, not interval balls.
- `Hess_ii(P)`: signed order4 angular integration of mixed
  spatial-order-n / external-order-2 jet over FULL external box.
  Multiply coefficient by 2! to recover second derivative.
- `Hess_ij(P)`: signed order4 angular integration of mixed
  spatial-order-n / i-order-1 / j-order-1 jet over FULL external box.
  Cross-coefficient multiplier 1!×1!=1.
- Assemble exact **interval** corrections:
  `H(p0) + sum grad_i(p0)*[-h_i,h_i] +
  1/2 sum Hess_ii(P)*[0,h_i^2] +
  sum_{i<j} Hess_ij(P)*[-h_i*h_j,h_i*h_j]`.
  All arithmetic outward rounded Arb at 128-bit.
  Do NOT replace diagonal product [0,h²] with symmetric [-h²,h²].
  No unsigned zeroth-order angular range integral in center,
  gradient, Hessian, or any signed term.
- Angular mesh: pinned R3 `make_mesh`, base_u16/base_v32,
  distance_ratio1/2, signed Taylor spatial order4,
  max_cells40000, max_depth28, python-flint==0.8.0,
  precision128, C21 angular cap if needed (the target has R_hi<1).
- The nominal positive distance bound of the MVT extension
  must be checked on its own extended box; old R3 chart-aligned
  mesh is only the partition, NOT a distance proof.

**Stage A resource caps**, fixed in advance: at most **8 concurrent**
subprocesses; GENERAL1800 seconds each, AXIS_MVT2400 seconds
each. Every attempt records worker wall time, peak RSS,
mesh cells, base H, three signed gradient intervals,
six signed Hessian intervals, decomposed correction halfwidth,
and the historical first-order halfwidth from the 84-box file.
If any box times out or fails, Stage A is **INCONCLUSIVE** and
Stage B is NOT launched. Never invent an H interval.

## Gate to Stage B

Proceed **only if all 8** attempts return finite, valid H
enclosures and **every one** has new second-order H halfwidth
`<=` old first-order H halfwidth (exact rational endpoints
used for comparison). If ANY box is wider, return
`STAGE_B_BLOCKED_WORSE_WIDTH`; if ANY is OPEN, return
`STAGE_B_BLOCKED_STAGE_A_OPEN`. No changing the 8 samples or
mesh after seeing the result.

## Stage B (only after passing gate)

Restart a brand NEW controller state, not previous 84-box H
`state.json`, with same specified
λ=[1279/256,5] unsplit, R=[1/4,1/2], τ=[0,1].
Start **1024** exact 1/64×1/64 boxes, separate 12-worker
subprocesses, lexicographic immutable IDs from frozen prior
controller, same ordering, split longer normalized R or τ edge
(tie R), stop each edge at 1/256. Binary H-contains-zero only.
Terminals: DECIDED_NONZERO, TUBE_AT_MINIMUM,
TUBE_TIMEOUT_OR_ERROR. Per-box 1800s GENERAL, 2400s special.
Checkpoint every ordered batch and reconstruct inflight on
restart. Entire **combined** 24h experiment time includes
Stage A, Stage B, optional W. Earlier 84-box runs are inputs,
not newly charged experiment wall time.
At intermediate checkpoints, exact rational area identity is
DECIDED + EVALUATED_TUBE + PENDING = **1/4**.
Never describe PENDING as measured tube area.
Report depth counts, route time, box logs, peak RSS, final
tube distribution; lambda-extrapolation only if the entire
requested subregion was evaluated. Hypothetical λ plate
widths1/256 throughout [2,5] =>768; alternative widths1/1024
in [2,3] plus1/256 in [3,5] =>1536. Both are UNVERIFIED and
cannot generate a global cost when subregion unfinished.

## W separate cost

Only after Stage B subregion fully finished or genuine 24h
hard cap, sort all TERMINAL evaluated tube IDs, take
first/middle/last exactly3 and measure pinned R3 second-order W,
not full-tube W. If insufficient candidates/time, mark OPEN.

## Integrity

Before Stage A commit this rule and implementation sources.
New branch ONLY; DO NOT touch main, STATE.md, previous branches,
existing frozen Julia, R3 source, or make tag. Write
`ANALYSIS_C21_SECOND_ORDER.md`, producer/checker scripts,
fixed 8 sample JSON, exhaustive per-box outputs actually run,
one-line run command, exact ledger, ZIP, SHA256SUMS and SHA.
**All results are DIAGNOSTIC_ONLY / NOT_EVIDENCE; no proof
status conclusion beyond OPEN.**
