# Dig / C21 [2,5] axis-to-L2 replacement assessment
2026-11-19 — DIAGNOSTIC_ONLY / NOT_EVIDENCE — proposal only, not Judge adoption.

## 1. Geometry and logical scope
C21 coordinates rho=R(1-tau^2)/(1+tau^2), z=2R tau/(1+tau^2), 0<=R,tau<=1. For R>0 the axis rho=0 corresponds exactly to tau=1 and z=R. Thus S^2=1-R^2. The L2 domain S>=1/lambda on the axis is the exact semialgebraic region R^2+lambda^-2<=1. For lambda in [2,5], its boundary is R=sqrt(1-lambda^-2). On a lambda slab [a,b], a sufficient all-lambda criterion is R_hi^2+a^-2<=1. In a uniform 1/64 R partition, lambda=2 covers the axis faces of 55 full R bands (i=0,...,54); lambda=5 covers 62 (i=0,...,61). These are counts of axis *faces*, not deletable 2D C21 boxes. For R=0 the origin is stationary by symmetry; L2 gives E_zz(0,0)>0 but does not eliminate the origin.

For z>0, E_z(0,z)/z>0 excludes an axial stationary point because E_z>0. Reflection handles z<0. This does not prove H<0, does not cover rho>0, and does not replace a box-wide C21 sign test for an axis-adjacent 2D rectangle.

The remaining polar cap on the axis is R^2>1-lambda^-2, with equality included in L2. G1's positive interval result for lambda>=80/19 is reported by Judge as conditional on its exact cap hypotheses; the interval 2<=lambda<80/19 still needs existing C21/G1 alternatives. The origin remains an intended stationary point, not an exclusion target.

## 2. Existing C21 approach and observed costs
C21 V37/V40 uses H sign and, where needed, W/tube routes. Its axis-adjacent boxes use the mean-value identity H(rho,z)=integral_0^1 E_rhorho(s rho,z) ds, labeled AXIS_MVT; this is a box-wide H enclosure, not an axial E_z condition.
The frozen partial slab [1279/256,5] x R in [1/4,1/2] x tau in [0,1] includes 16 AXIS_MVT jobs R16_T63 through R31_T63, tau in [63/64,1], totaling 2231.690738 worker-seconds (37.19 worker-minutes); 132–147 seconds per box. There were 68 GENERAL jobs; 84 total, 25 decided, 1058 pending; the slab is PARTIAL_UNFINISHED. The 16 AXIS_MVT boxes cover rho>0 as well as the axis. Therefore zero of these 16 full-box H tasks is rigorously rendered unnecessary solely by L2. The 37.2 minutes is a measured workload for these jobs, NOT a proven saving. No complete [2,5] axis-only condition Z ledger, its total box count, or its total runtime was identified in the examined GitHub records; do not extrapolate 16 jobs to the full window.

## 3. Binary replacement judgment
YES: Replace an *axis-only stationary-point exclusion condition* Z with L2 wherever R^2+lambda^-2<=1, provided Z has no independent requirement on H, W, transversality, or a neighborhood. L2's coordinate z is the reference coordinate, and physical E_pz differs by a positive factor lambda^-1; sign is unchanged.
NO: Do not replace an AXIS_MVT/C21 *two-dimensional box-wide H test* with L2 alone. All rho>0 points in the box remain to be covered.

The north and south poles are boundary/trace cases and require the existing separate boundary logic. The G1 cap extension for lambda>=80/19 must be checked against its exact w=lambda S and z hypotheses before treating it as a replacement.

## 4. Savings and proposal
Verified deletable full-box count from L2 alone: 0. Verified full-box worker time saved: 0 seconds. Potential axis-only condition Z count and runtime saved: NOT DETERMINED, because the complete condition Z task list and measured timings were not available in the examined source records. The 16 axis-adjacent jobs and 2231.69 worker-seconds are only an upper reference for this one partial-slab route, not a saving estimate.

Propose a proof-level substitution for the one-dimensional axis Z obligation; keep C21 2D boxes unchanged until a separate rho>0 sign or neighborhood lemma is established. Request the canonical Z condition list/ledger for an exact subtraction of Z-only jobs. No computational runs, changes to STATE/main/ledgers, or interference with PID 1581407.

## Sources
C21 partial-slab README, RUN_RECEIPT.md, summary.json on research/d-pro-c21-r63-t63-cap-20261119; V37 and V40 audit records; V44 R63_T63 cap audit. L2 mathematical claim and V48 acceptance as supplied by Judge. No new numerical pilot.
