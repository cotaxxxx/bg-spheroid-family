# RUNNER INSTRUCTIONS — Judge corrections for C21 heavy slab (2026-11-18)
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**. This is an operator clarification recorded AFTER the frozen source/coverage policy commit `0b8382d96c4f89c6bc1f8ee756b26134f28fc530`. It MUST NOT alter the frozen producer, pre-selected path priority, root selection, mesh, sign predicate, or total 36-hour resource caps. Continue the 4,092+ pending boxes without asking Judge to re-decide.

## 1. Corner R63_T63: independent-extension geometry fails, NOT a routine weak distance bound

Original root `R=[63/64,1]`, `tau=[63/64,1]`. Route-priority class is AXIS_MVT. That route envelopes `E_{rho rho}(rho',z)` over independent `rho'∈[0,rho_hi]` and `z∈[z_lo,z_hi]`. Here `z_hi=1`, `rho_hi>0`. The independent extension therefore contains `(rho_hi,1)` with `rho_hi²+1>1`, outside the physical unit-body domain. This is a geometry/coordinate-dependency failure, NOT one that can be fixed simply by sharpening a positive distance estimate. Refinement preserving the top-right corner retains this extension problem. On the *true* line `(s rho,z)`, for `s∈[0,1]`, the MVT identity is still meaningful within the body; only the rectangular independent extension fails.

**Disposition fixed for THIS diagnostic run:** Keep the frozen source's conservative terminal record `TUBE_OPEN_ERROR` and `H_interval=null` for `R63_T63` (no fabricated H or sign). Additionally record it as a **SPECIAL_RESERVED_AXIS_BOUNDARY_CORNER**, with a separately reserved physical R–tau area of exactly `1/4096`. This is NOT an observed H≈0 zero-tube and must NOT be counted as such in independent analysis. The original STATE/SUMMARY terminal already claims the area once; any analytical area overlay must use **DECIDED + H_ZERO_TUBE + SPECIAL_RESERVED + OTHER_OPEN + PENDING = 1**, and must not add the reserved area a second time. Do NOT silently change the frozen controller's tube or W rules mid-run. Dedicated joint polar axis/boundary collar path is deferred until the slab measurement is complete.

## 2. Independent primitive E reference for R16_T00

This is identical to V40's `A_P1_L1_16`: `R=[1/4,17/64]`, `tau=[0,1/64]`, `lambda=[79/16,5]`. Judge supplied the independent chat 25-digit two-dimensional integration benchmark, with PHYSICAL `p_z=lambda*z`:

| Point `(R,tau,lambda)` | H chat benchmark |
|---|---:|
| center `(0.2578125,0.0078125,4.96875)` | `-0.03692977447` |
| corner `(0.25,0,5)` | `-0.03851056864` |
| corner `(0.265625,0.015625,4.9375)` | `-0.03534917096` |

Existing `c21_heavy_refs.py` n=24 vs n=40 Gauss-E values differ by ~0.0044. These are too far apart to be reference standards. The measured deviations from the above chat benchmark are:
- mid: n24 +0.00484510643; n40 +0.00035458318
- lower_corner: n24 +0.00738267697; n40 +0.00284718809
- upper_corner: n24 +0.00219541314; n40 -0.00218429922

***Operator action:*** use the supplied chat values as the comparison baseline, not the unstable n24/n40 results. Independently inspect (i) physical `p_z=lambda*z`, (ii) the angular integration convention/normalization, and (iii) splitting near contact/boundary regions and Gauss convergence. The source already has `pz=lam*z`; verify the conversion inside `E` as well rather than assuming it explains the error. Record numerical errors against chat benchmarks **without** claiming a rigorous error bound. No change to H interval producer, frozen numerical rules, or sign-driven adaptive branching for this run.

## 3. Continue and later independent audit

Continue the fixed 12-worker, <=1200s/job, <=36h cumulative experiment. The purpose is to measure real observed split counts, reserved/zero-tube area, and worker/wall cost. Do not extrapolate global costs from 12 geometrically biased roots. All uncomputed boxes are PENDING, not a tube or a decided sign. After future measured checkpoints, independent chat audit should sample sign-decided and H-evaluated near-zero tubes with primitive E; do not finite-difference `E_rho/rho` at rho=0.

**DIAGNOSTIC_ONLY / NOT_EVIDENCE.**
