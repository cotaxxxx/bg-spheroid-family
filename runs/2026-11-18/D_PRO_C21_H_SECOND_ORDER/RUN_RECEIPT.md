# C21 H second-order interval diagnostic

**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

Frozen Stage-A selection: 8 boxes, 6 general, 2 axis.
Prerun commit 4760c534b02621c5a31a9befc6469495fb8d9c4b.
C21 source 5004ebd, V38 922a2c7, original84 2e3a091.
Original physical vertical coordinate p_z=lambda*z.
All spatial integrals are signed Taylor order4 at Arb128.

## Stage A: historical first order versus second order

Measured parallel wall time: 628.535 seconds.
Completed: 8/8. Worse: 0. OPEN: 0.
Decision gate: STAGE_B_ALLOWED.

| ID | Route | Old halfwidth | New halfwidth | Point | Linear | Hessian | Old s | New s | Gate |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| R16_T00 | GENERAL | 0.098312391 | 0.015047812 | 0.00061892484 | 0.0012972512 | 0.013131636 | 157.24457 | 601.71404 | NONWORSE |
| R18_T08 | GENERAL | 0.11254193 | 0.01807734 | 0.00073156457 | 0.0014589264 | 0.015886849 | 168.58998 | 611.46806 | NONWORSE |
| R20_T48 | GENERAL | 0.5350852 | 0.088129788 | 0.0021232202 | 0.00230712 | 0.083699448 | 170.28156 | 626.51654 | NONWORSE |
| R23_T32 | GENERAL | 0.2083422 | 0.036382344 | 0.0011517531 | 0.0019983083 | 0.033232282 | 163.59499 | 613.75937 | NONWORSE |
| R26_T00 | GENERAL | 0.056591554 | 0.0093343812 | 0.00035380672 | 0.0017681612 | 0.0072124133 | 161.83746 | 628.51464 | NONWORSE |
| R28_T32 | GENERAL | 0.16650076 | 0.029774527 | 0.00097179513 | 0.0022653404 | 0.026537391 | 172.31913 | 623.01168 | NONWORSE |
| R16_T63 | AXIS_MVT | 0.014705832 | 0.0026533664 | 0.00029550574 | 0.0011050213 | 0.0012528393 | 132.56275 | 509.18031 | NONWORSE |
| R31_T63 | AXIS_MVT | 0.022273842 | 0.0047644109 | 0.00031442211 | 0.0021712299 | 0.0022787589 | 137.76357 | 533.47433 | NONWORSE |

## Stage B: 1024 initial boxes on R=1/4..1/2, tau=0..1

- measured_jobs: 12
- decided_count: 12
- tube_candidate_EVALUATED_count: 0
- pending_UNEVALUATED_count: 1012
- split_parents: 0
- area_decided_exact: 3/1024
- area_tube_evaluated_exact: 0
- area_pending_exact: 253/1024
- area_partition_sum_exact: 1/4
- H_adaptive_wall_s: 690.561067182105
- total_experiment_wall_s_including_calibration: 1319.096144808922

Exact area relation: decided + evaluated tube + pending = 1/4.
The pending area is not measured tube area.

| Route | Jobs | Worker seconds |
|---|---:|---:|
| GENERAL | 6 | 4011.473 |
| AXIS_MVT | 6 | 3385.174 |
| SMALL_RHO_MVT | 0 | 0.000 |
| CENTER_MVT | 0 | 0.000 |

| Depth | Evaluated | Terminal |
|---|---:|---:|
| 0 | 12 | 12 |

## W three-box-only measurement

Measured: NO, deferred

## Independent exact-fraction output audits

Stage-A 8-box exact-width and Taylor decomposition: PASS; not a mathematical kernel proof.
Duplicated Stage A versus B interval bytewise equality: 3 boxes, PASS.
Paired 12 original first-order vs new second-order boxes:
old decided 8/12, new decided 12/12;
newly decided 4, regressions 0.
Median old/new halfwidth ratio 5.731122.
Historical worker-seconds sum 1815.805;
new worker-seconds sum 7394.312.

## Cost extrapolation

Full subregion unfinished or gate blocked. No extrapolated box number.
Plate counts 768 or1536 depend on unverified lambda thickness assumptions.

## Audit

No independent mathematical audit of new Hessian jets completed.
The mathematical Taylor-2 formula is documented separately.
Checker and SHA establish ledger and byte consistency only.
No previous research branch, main, STATE.md, tags, or frozen Julia changed.
**DIAGNOSTIC_ONLY / NOT_EVIDENCE. C21 global theorem OPEN.**
