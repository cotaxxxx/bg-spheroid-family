# D-PRO (C21) — frozen adaptive λ slab pilot (PRE-RUN)
2026-11-18 / **DIAGNOSTIC_ONLY / NOT_EVIDENCE**

This document must be committed BEFORE any adaptive slab job is run.
Input pins: H C21 `5004ebdc6e038bcdb3122f563ffb15d38070d8b6`,
chat V37 audit `949e9dff7b48cf993cdb9fae95ec698f482cd591`,
R3 `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`.
Source-calibration rules frozen separately in `CALIBRATION_RULE_FREEZE.md`.

## Domain / geometric partition

- **Only one λ slab**, exact λ∈[1279/256, 5]. No λ subdivisions.
- (R,τ) exactly [0,1]². Start with 16×16 rational rectangles
  R∈[i/16,(i+1)/16], τ∈[j/16,(j+1)/16] for i,j=0..15.
- Initial ID `Rii_Tjj` with exactly two-digit zero-padded i,j.
  Initial processing order: ascending *least-significant-bit-first
  interleaved Morton index* of (i,j), 4 bits each. First IDs:
  R00_T00, R00_T08, R08_T00, R08_T08, R00_T04, ...
  Every child ID appends `.R0`/`.R1` or `.tau0`/`.tau1`.
- Processing order: (depth, initial Morton rank, lexical full ID)
  sorted, max 12 tasks per batch. A batch commits ALL its results
  in deterministic submitted-ID order; worker timing does not
  change the partition tree.

## One-box evaluation

- Python 3.11.16, python-flint **0.8.0**, Arb 128-bit.
- Signed Taylor angular quadrature: order4, base_u=16,
  base_v=32, distance_ratio=1/2, max_cells40000,
  max geometry depth28. All three outer derivatives are integrated
  signed, using the first-order mean-value exterior interval form.
  Do NOT use a zeroth-order angular range×measure integral on a
  signed coefficient or its outer derivative.
- Exact route precedence, based **only on box location**:
  (1) `τ_hi=1` -> AXIS using the horizontal second-rho identity
  and 4 s-Simpson panels with nonnegative s-remainder;
  (2) `R_lo=0` -> CENTER with the same horizontal second-rho route;
  (3) `R_hi=1` -> BOUNDARY with R3 contact cap κ=1/4096
  (one rigorous cap-error term); otherwise REGULAR direct
  `f_rho/rho`. All routes compute only horizontal rho derivatives.
- At the AXIS∩BOUNDARY double corner (R_hi=1 and τ_hi=1),
  the current f_rho_rho kernel has no proven uniform s cap.
  **DO NOT invent a bound:** mark that box OPEN and count as
  a tube candidate for this diagnostic. Preserve its coordinates.
- Hard per-box wall time caps, fixed NOW:
  REGULAR 180 seconds, CENTER 600 seconds, AXIS 600 seconds,
  BOUNDARY 300 seconds. Any per-box timeout, invalid denominator,
  mesh resource limit, or exception => `TUBE_TIMEOUT_OR_ERROR`
  terminal candidate with H interval null and explicit reason.

## Adaptive decision and stop rules

- For an evaluated H interval: if **zero is excluded**, label
  DECIDED_NONZERO and do not subdivide. Record the sign but
  DO NOT branch based on which sign.
- If zero is included, split the longer normalized R or τ edge
  exactly at its rational midpoint, ties break R first.
  Continue until **both** R width and τ width are ≤1/256.
  At that resolution, a zero-containing box is a
  `TUBE_AT_MINIMUM` terminal candidate.
- All boundary grid/child intervals are closed and adjacent.
  Duplicate edge ownership is harmless for outer enclosures;
  areas use exact rational widths.
- No other adaptive variable, test, or routing heuristic is allowed.
- 12 worker subprocesses maximum; one process measures each
  H box wall time and peak RSS. Batch-level wall clock is measured
  separately from the sum of worker execution seconds.

## 24-hour cap / resumability

- The **overall experiment wall budget** is 86400 seconds including
  the already-measured AX/CE/BD calibration elapsed wall time and
  any later W-three-box sample. The controller uses one fixed
  state file `state.json`, and checkpoints before each batch
  and after it, with atomic rename and file fsync.
- An interactive `--session-seconds` or `--max-batches` argument
  may deliberately stop EARLY for a partial pilot. Such a
  partial pilot is NOT an incomplete-domain W proof or a complete
  H slab survey. Any worker interrupted purely due to session
  deadline is requeued, NOT counted as a measured tube candidate.
- Crash recovery requeues uncommitted inflight work; a source JSON
  is only accepted when the enclosing state checkpoint records it.
- At any partial stop, rigorously preserve the rational partition
  `area_decided + area_tube_evaluated + area_pending = 1`.
  `area_decided + area_tube_evaluated = 1` may be claimed
  ONLY after the pending count is zero. Never silently count
  unmeasured boxes as evaluated tube boxes.
- Append per-box logs, JSON, process time, cell count, max RSS,
  depth, route, exact area; summary computes a depth histogram,
  route seconds, partial tube geometry, and the exact fractions.
  Terminal timeout/open boxes carry `H_interval: null`.

## W sample in the tube

- Frozen R3 `angular_quotient` (the R3 quadratic formula
  previously reviewed in chat V32): order4, base_u=16,
  base_v=32, ratio1/2, 128 bits, center_to1/16,
  cap_from15/16, κ1/4096. W uses the same unsplit λ slab.
- Select **exactly 3** evaluated tube candidate boxes by sorting
  their immutable IDs and taking first, midpoint (`n//2`),
  last. Freeze selection JSON at a complete slab or a
  hard 24-hour cutoff, not at an intermediate short session.
  Selection cannot change on resume. If fewer than 3 exist
  or time is insufficient, report OPEN; do not fabricate samples.
- Each W sample receives a hard cap 1200 seconds, three at most
  in parallel, subject to global remaining wall budget.
  The three W results are **measurements only**, not a proof
  that W excludes zero throughout the tube.

## Cost extrapolation

- Record **actual** evaluated H boxes, decided boxes, tube boxes,
  pending count and actual wall times; do not infer a hypothetical
  box count from a smoothness guess.
- Only if the ENTIRE thin slab is processed, an extrapolation can
  use its actually measured H box count/time. For illustration
  λ∈[2,5] requires exactly 768 slabs if every slab has width
  1/256; this is NOT supported near λ≈2 by the pilot.
  A more conservative explicit but **UNVERIFIED** thickness
  assumption is width1/1024 on [2,3] (1024 slabs) and
  width1/256 on [3,5] (512 slabs), total 1536 slabs.
  Neither assigns an invented number of H boxes per slab:
  any scaling of measured counts is labeled CONDITIONAL.
  H≈0 tube W cost remains separate, not multiplied silently.
- If the slab is unfinished, report **only a lower bound** on
  boxes already processed and exact pending area, not a
  768/1536-multiplied cost forecast.

## Integrity

- New branch `research/d-pro-c21-h-slab-cover-20261118` only.
  Never modify main, STATE.md, other branches or frozen Julia.
- All artifacts explicitly `DIAGNOSTIC_ONLY / NOT_EVIDENCE`.
  All numerical statements are diagnostics pending independent
  mathematical inspection. No full λ-domain covering.
