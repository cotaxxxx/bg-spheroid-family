# D-PRO (C21) — Heavy λ slab adaptive H diagnostic checkpoint
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

λ ∈ [79/16,5] unsplit; (R,τ)∈[0,1]².
Fixed rules and exact initial 4096 roots: PRE_RUN_FREEZE.md and REGISTRY.json.
The fixed experiment code and root order were committed before H run.

## Coverage accounting (not a certified H sign)

| State | Boxes | R×τ area, exact rational |
|---|---:|---:|
| Evaluated decided nonzero H | 7 | 7/4096 |
| Evaluated terminal tube candidates | 1 | 1/4096 |
| PENDING_UNEVALUATED (NOT a tube) | 4092 | 511/512 |
| Sum | — | 1 |

Initial roots: **4096**. Processed attempts: 12.
Completed H boxes: 11.
OPEN error/timeouts: 1.
Zero-containing split parents: 4.
Observed split frequency among completed interval boxes: 0.36363636363636365.
**This split rate is on processed boxes only, not on 4096 roots.**
No attempt to fill unmeasured area with a guess.

## Measured costs

Cumulative wall time actually charged to 36h cap: 545.466 s.
Worker time sum (including session-interrupted work): 3607.391 s.
Global wall cap 129600s (36h). Per box limit1200s, workers12.
Each operation session may end earlier; a session checkpoint
must NOT be labeled 36h exhaustion or complete slab.

## Route × depth measured counts and worker times

| Route and depth | Processed count | Worker seconds |
|---|---:|---:|
| AXIS_MVT|depth0 | 4 | 736.682 |
| BOUNDARY_COLLAR|depth0 | 2 | 1032.862 |
| CENTER_MVT|depth0 | 2 | 447.268 |
| GENERAL|depth0 | 4 | 1390.579 |

## Evaluated tube coordinates and chart

Tube types: {"TUBE_OPEN_ERROR": 1}.
Coordinates of **evaluated** terminal tubes are in
SUMMARY.json under tubes_coordinates.
TUBE_DISTRIBUTION.svg draws only terminal measured outcomes;
the large gray area is PENDING_UNEVALUATED, not a sign result.

## Full λ domain cost extrapolation (conditional, not a prediction)

V40's independent cost-only local λ≈2 data measured
P1 ≈106.50s, P3 ≈88.38s on λ=[2,17/8] with H halfwidths
0.09797 and 0.05314, respectively. Those samples are
NOT a full λ≈2 slab and do not establish safe plate widths.
Original V40 36-plate scenario (near5 width1/16 and near2 width1/8)
was hypothetical ~26 days with12 workers BEFORE spatial splitting
and W costs. It is not updated by partial-board sampling.

GLOBAL H COST STATUS: NOT_ESTIMABLE_FROM_PARTIAL_SLAB.
Until a representative entire λ≈5 plate or genuine 36h cap
is measured, the full-board split fraction and terminal tube
area are unknown. Low-λ width remains a separate hypothetical assumption.

## W three-box timing

DEFERRED_UNTIL_FULL_PLATE_OR_GENUINE_36H_CAP
Sorted first/median/last tube selection is frozen, but
is deferred until full plate completion or actual cumulative36h
and at least three evaluated tubes. Arbitrary interim tubes
cannot substitute for frozen W sample selection.

## Independent checks and E-reference

Exact interval/checkpoint ledger checker: ACCOUNTING_PASS_NOT_CERTIFICATION.
Direct-E sample status: see E_REFERENCE_STATUS.json if present;
do not treat missing reference or any finite differences near rho=0
as proof of the axis point.
This is a measurement of a computational procedure, NOT a proof.
**DIAGNOSTIC_ONLY / NOT_EVIDENCE — C21 global theorem OPEN.**

## Post-checkpoint numerical E reference appendix

**DIAGNOSTIC_ONLY / NOT_EVIDENCE.** The original heavy H
producer was not edited after the pre-run freeze. The independently
computed primitive-E Gauss-Legendre (24² and 40²) five-point physical
rho finite-difference reference was tested at R16_T00 midpoint and
its two corners. Both quadrature samples were contained in the actual
H interval at all three positions. This is only a numerical diagnostic:
there is NO rigorous Gauss/difference error estimate.

For the evaluated tube R63_T63 (OPEN mathematical distance exception),
no H interval was produced. One finite-rho corner reference was
computed but containment is untestable; axis-near-zero points were
skipped. These exclusions are explicit in E_REFERENCE_RESULTS.json.
The first reference CLI encountered a post-save reporting TypeError;
its traceback was retained in E_REFERENCE_FIRST_RUN_ERROR.log.
The completed result JSON remained valid and was verified separately;
corrected CLI status is in E_REFERENCE_RUN.log.

**Remaining: 4,092 PENDING_UNEVALUATED nodes.** W 3-box sample
selection is deferred by the preregistered completion/36h condition.
No full slab or full lambda-domain cost inference has been made.
**DIAGNOSTIC_ONLY / NOT_EVIDENCE.**
