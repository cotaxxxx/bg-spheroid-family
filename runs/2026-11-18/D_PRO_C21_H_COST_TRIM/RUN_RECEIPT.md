# C21 H second-order cost-trim experimental receipt
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

Source baseline commit 0427b19d84e5105aa1a03ff69c9842065d491f3c.
Source V39 commit 544ebfd138c02d2fc68806184a1d0ce2e744fa2c.
Measurement only. No covering. No sign-based method selection.

## Results and scope
- measured_jobs: 24
- completed_jobs: 24
- open_jobs: 0
- invalid_geometry: 2
- unrun_valid: 0
- worker_seconds_sum: 10456.176473035943
- pilot_wall_s: 1644.7112228730693

P3 C cases: tau_lower=63/64 and requested widths1/32 or1/16;
both upper tau exceed1. Both are frozen NOT_RUN_OUT_OF_DOMAIN.
No silent geometry changes.

## All measured boxes

| ID | Group | Route | lambda width | R width | tau width | Hess mesh | H halfwidth | Point | Linear | Hessian | Point s | Grad s | Hess s | Total s | RSS KiB | zero? |
|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A_P1_L1_16 | A_LAMBDA_WIDTH | GENERAL | 1/16 | 1/64 | 1/64 | 16x32/1/2/n4 | 0.02340093 | 0.000613048 | 0.0036724 | 0.0191155 | 25.67 | 133.99 | 475.88 | 635.63 | 32544 | no |
| A_P2_L1_16 | A_LAMBDA_WIDTH | GENERAL | 1/16 | 1/64 | 1/64 | 16x32/1/2/n4 | 0.01501294 | 0.000350956 | 0.0039925 | 0.0106695 | 28.23 | 146.45 | 509.08 | 683.89 | 32060 | no |
| A_P3_L1_16 | A_LAMBDA_WIDTH | AXIS_MVT | 1/16 | 1/64 | 1/64 | 16x32/1/2/n4 | 0.005698179 | 0.000293552 | 0.00343007 | 0.00197456 | 22.92 | 118.04 | 430.80 | 571.85 | 32956 | no |
| A_P4_L1_16 | A_LAMBDA_WIDTH | AXIS_MVT | 1/16 | 1/64 | 1/64 | 16x32/1/2/n4 | 0.007146381 | 0.000306902 | 0.00395468 | 0.0028848 | 22.43 | 115.62 | 437.85 | 576.04 | 32308 | no |
| A_P1_L1_8 | A_LAMBDA_WIDTH | GENERAL | 1/8 | 1/64 | 1/64 | 16x32/1/2/n4 | 0.03865206 | 0.000606841 | 0.00628481 | 0.0317604 | 27.57 | 142.98 | 486.46 | 657.11 | 32060 | yes |
| A_P2_L1_8 | A_LAMBDA_WIDTH | GENERAL | 1/8 | 1/64 | 1/64 | 16x32/1/2/n4 | 0.02495908 | 0.000347933 | 0.00644028 | 0.0181709 | 26.59 | 139.52 | 497.82 | 664.03 | 32040 | no |
| A_P3_L1_8 | A_LAMBDA_WIDTH | AXIS_MVT | 1/8 | 1/64 | 1/64 | 16x32/1/2/n4 | 0.009331987 | 0.00029154 | 0.00598828 | 0.00305216 | 22.89 | 117.47 | 429.27 | 569.77 | 32328 | no |
| A_P4_L1_8 | A_LAMBDA_WIDTH | AXIS_MVT | 1/8 | 1/64 | 1/64 | 16x32/1/2/n4 | 0.01068549 | 0.000304737 | 0.00619388 | 0.00418688 | 22.46 | 115.40 | 422.46 | 560.40 | 32272 | no |
| A_P1_L1_4 | A_LAMBDA_WIDTH | GENERAL | 1/4 | 1/64 | 1/64 | 16x32/1/2/n4 | 0.1409377 | 0.000594609 | 0.0117634 | 0.12858 | 25.81 | 136.39 | 483.58 | 645.87 | 32372 | yes |
| A_P2_L1_4 | A_LAMBDA_WIDTH | GENERAL | 1/4 | 1/64 | 1/64 | 16x32/1/2/n4 | 0.08937432 | 0.000341943 | 0.0115775 | 0.0774549 | 28.23 | 146.95 | 508.58 | 683.87 | 32548 | yes |
| A_P3_L1_4 | A_LAMBDA_WIDTH | AXIS_MVT | 1/4 | 1/64 | 1/64 | 16x32/1/2/n4 | 0.01815821 | 0.000287736 | 0.0113562 | 0.0065143 | 23.13 | 117.77 | 430.16 | 571.14 | 32732 | no |
| A_P4_L1_4 | A_LAMBDA_WIDTH | AXIS_MVT | 1/4 | 1/64 | 1/64 | 16x32/1/2/n4 | 0.01939631 | 0.000300611 | 0.0108992 | 0.00819646 | 22.93 | 116.84 | 422.94 | 562.85 | 32300 | no |
| B_P1_H8x16_O4 | B_HESSIAN_COARSE | GENERAL | 1/256 | 1/64 | 1/64 | 8x16/1/n4 | 0.02191162 | 0.000618925 | 0.00129725 | 0.0199954 | 25.27 | 129.27 | 110.20 | 264.83 | 32332 | no |
| B_P2_H8x16_O4 | B_HESSIAN_COARSE | GENERAL | 1/256 | 1/64 | 1/64 | 8x16/1/n4 | 0.01665431 | 0.000353807 | 0.00176816 | 0.0145323 | 26.19 | 134.10 | 113.00 | 273.45 | 32492 | no |
| B_P3_H8x16_O4 | B_HESSIAN_COARSE | AXIS_MVT | 1/256 | 1/64 | 1/64 | 8x16/1/n4 | 0.005162836 | 0.000295506 | 0.00110502 | 0.00376231 | 20.47 | 105.06 | 94.01 | 219.63 | 33012 | no |
| B_P4_H8x16_O4 | B_HESSIAN_COARSE | AXIS_MVT | 1/256 | 1/64 | 1/64 | 8x16/1/n4 | 0.007864458 | 0.000308999 | 0.00192153 | 0.00563393 | 21.47 | 109.83 | 97.95 | 229.40 | 32628 | no |
| B_P1_H8x16_O2 | B_HESSIAN_COARSE | GENERAL | 1/256 | 1/64 | 1/64 | 8x16/1/n2 | 0.03844877 | 0.000618925 | 0.00129725 | 0.0365326 | 24.86 | 128.21 | 45.34 | 198.51 | 32852 | no |
| B_P2_H8x16_O2 | B_HESSIAN_COARSE | GENERAL | 1/256 | 1/64 | 1/64 | 8x16/1/n2 | 0.02552966 | 0.000353807 | 0.00176816 | 0.0234077 | 25.38 | 132.01 | 46.34 | 203.82 | 32860 | no |
| B_P3_H8x16_O2 | B_HESSIAN_COARSE | AXIS_MVT | 1/256 | 1/64 | 1/64 | 8x16/1/n2 | 0.01316315 | 0.000295506 | 0.00110502 | 0.0117626 | 20.44 | 104.59 | 38.09 | 163.20 | 32760 | no |
| B_P4_H8x16_O2 | B_HESSIAN_COARSE | AXIS_MVT | 1/256 | 1/64 | 1/64 | 8x16/1/n2 | 0.01844904 | 0.000308999 | 0.00192153 | 0.0162185 | 21.35 | 109.88 | 39.36 | 170.68 | 32860 | no |
| C_P1_RTau1_32 | C_SPATIAL_BOX | GENERAL | 1/8 | 1/32 | 1/32 | 16x32/1/2/n4 | 0.2400418 | 0.000602834 | 0.00747578 | 0.231963 | 23.13 | 119.20 | 428.88 | 571.28 | 32588 | yes |
| C_P1_RTau1_16 | C_SPATIAL_BOX | GENERAL | 1/8 | 1/16 | 1/16 | 16x32/1/2/n4 | 3.920036 | 0.000600235 | 0.010067 | 3.90937 | 23.28 | 120.95 | 436.09 | 580.39 | 32272 | yes |
| D_P1_LOW2_L1_8 | D_LOW_LAMBDA | GENERAL | 1/8 | 1/64 | 1/64 | 16x32/1/2/n4 | 0.0979718 | 0.00424966 | 0.0335019 | 0.0602202 | 4.27 | 22.11 | 80.10 | 106.50 | 32028 | no |
| D_P3_LOW2_L1_8 | D_LOW_LAMBDA | AXIS_MVT | 1/8 | 1/64 | 1/64 | 16x32/1/2/n4 | 0.05314415 | 0.00693833 | 0.0355261 | 0.0106797 | 3.50 | 18.19 | 66.68 | 88.38 | 32028 | no |
| C_P3_RTau1_32 | C_SPATIAL_BOX | AXIS_MVT | 1/8 | 1/32 | 1/32 | — | NOT_RUN_OUT_OF_DOMAIN | — | — | — | — | — | — | — | — | — |
| C_P3_RTau1_16 | C_SPATIAL_BOX | AXIS_MVT | 1/8 | 1/16 | 1/16 | — | NOT_RUN_OUT_OF_DOMAIN | — | — | — | — | — | — | — | — | — |

All ten point, gradient and Hessian signed components,
individual wall times, exact H interval endpoints, base and Hess
mesh sizes, and peak child RSS are in per-box JSON files.

## Historical baseline (not charged to current pilot)

| Probe | H halfwidth | Point s | Grad s | Hess s | Total s |
|---|---:|---:|---:|---:|---:|
| P1 | 0.01504781 | 27.61 | 142.72 | 512.43 | 682.84 |
| P2 | 0.009334381 | 28.36 | 147.03 | 513.62 | 689.10 |
| P3 | 0.002653366 | 22.94 | 116.83 | 427.35 | 567.21 |
| P4 | 0.004208824 | 22.48 | 115.18 | 418.10 | 555.86 |

## Width empirical formula

All h values are nominal HALF widths. For GENERAL only:
w_hat = c0 + aR hR + aT hTau + aL hLambda
 + bRR hR^2 + bRT hR hTau + bTT hTau^2
 + bRL hR hLambda + bTL hTau hLambda + bLL hLambda^2.
Coefficients are medians of actual signed-component correction
halfwidths divided by the corresponding monomial.
They do NOT describe rigorous bounds or verified regression.

### GENERAL
training_count: 10
model scope: Training boxes sample only P1/P2 and P1 spatial enlargements; not representative of entire R-tau board.
| Monomial | coefficient |
|---|---:|
| 1 | 0.00059742186 |
| h_R | 0.13298395 |
| h_tau | 0.02071484 |
| h_lambda | 0.0803263 |
| h_R^2 | 22.599287 |
| h_R*h_tau | 83.814208 |
| h_tau^2 | 159.5017 |
| h_R*h_lambda | 3.5732684 |
| h_tau*h_lambda | 13.755805 |
| h_lambda^2 | 0.48713922 |
In-sample median absolute error: 0.00967462; max: 3.61418; median relative: 0.5146.

### AXIS_MVT
training_count: 8
model scope: The actual MVT external variables are rho_prime,z,lambda; nominal h_R and h_tau are NOT outer Taylor radii. No varying tau/R axis boxes were valid for C, so the spatial coefficients are NOT identified for general axis boxes.
| Monomial | coefficient |
|---|---:|
| 1 | 0.00029805854 |
| h_R | 0.0023471357 |
| h_tau | 0.17533053 |
| h_lambda | 0.075090769 |
| h_R^2 | 0.3550346 |
| h_R*h_tau | 5.1681858 |
| h_tau^2 | 26.91844 |
| h_R*h_lambda | 0.16024817 |
| h_tau*h_lambda | 2.2376918 |
| h_lambda^2 | 0.059893031 |
In-sample median absolute error: 0.000939913; max: 0.00306615; median relative: 0.09344.

## Hypothetical full lambda 2..5 workload (NOT forecasts)

Assume 12 workers and an UNVERIFIED route mix (75% general,25% axis).
Per first R-tau cell, assume f fraction splits on every level:
sum(k=0..2log2(256/d)) (2f)^k at grid dxd.
The near-lambda2 plate thickness is an independent assumption.
All plate thicknesses, split fractions, workload portability and
route proportions are hypothetical.

| Grid | f | lambda plate policy | Plates | Equivalent H jobs | Wall hours (12 workers) |
|---|---:|---|---:|---:|---:|
| 64x64 | 0.25 | uniform_1_8_on_2_to_5_UNVERIFIED | 24 | 190,464 | 2,629.5 |
| 64x64 | 0.25 | low_1_1024_on_2_to_3_plus_high_1_8_on_3_to_5_UNVERIFIED | 1040 | 8,253,440 | 113,946.4 |
| 64x64 | 0.25 | uniform_1_256_on_2_to_5_UNVERIFIED | 768 | 6,094,848 | 84,145.0 |
| 64x64 | 0.50 | uniform_1_8_on_2_to_5_UNVERIFIED | 24 | 491,520 | 6,785.9 |
| 64x64 | 0.50 | low_1_1024_on_2_to_3_plus_high_1_8_on_3_to_5_UNVERIFIED | 1040 | 21,299,200 | 294,055.2 |
| 64x64 | 0.50 | uniform_1_256_on_2_to_5_UNVERIFIED | 768 | 15,728,640 | 217,148.5 |
| 64x64 | 0.75 | uniform_1_8_on_2_to_5_UNVERIFIED | 24 | 1,296,384 | 17,897.8 |
| 64x64 | 0.75 | low_1_1024_on_2_to_3_plus_high_1_8_on_3_to_5_UNVERIFIED | 1040 | 56,176,640 | 775,570.6 |
| 64x64 | 0.75 | uniform_1_256_on_2_to_5_UNVERIFIED | 768 | 41,484,288 | 572,729.1 |
| 32x32 | 0.25 | uniform_1_8_on_2_to_5_UNVERIFIED | 24 | 48,768 | 673.3 |
| 32x32 | 0.25 | low_1_1024_on_2_to_3_plus_high_1_8_on_3_to_5_UNVERIFIED | 1040 | 2,113,280 | 29,175.8 |
| 32x32 | 0.25 | uniform_1_256_on_2_to_5_UNVERIFIED | 768 | 1,560,576 | 21,545.2 |

No upper bound for the real global problem is established.
Low-lambda local probes do not imply global plate width.

## Integrity and conclusion
Record checker: PASS
The checker verifies input IDs, interval endpoint arithmetic,
mesh and signed coefficients. Independent mathematical audit
of new mixed-jets and global coverage is not included.
**DIAGNOSTIC_ONLY / NOT_EVIDENCE** — C21 global theorem OPEN.

## Post-run method-specific scenario appendix

**DIAGNOSTIC_ONLY / NOT_EVIDENCE**. This appendix was produced
after all 24 fixed measurements, WITHOUT changing the frozen
experiment list or numerical rules. Full assumptions and all
108 hypothetical combinations are in COST_METHOD_SCENARIOS.json
and COST_METHOD_SCENARIOS.md. Neither is a covering.

| Assumed method | 75:25 route-mixed worker seconds per box |
|---|---:|
| Historical full Hessian 16×32 order4 | 654.86 |
| Lambda1/8, full Hessian 16×32 order4 | 636.70 |
| Hessian-only 8×16 order4 | 257.98 |
| Hessian-only 8×16 order2 | 192.61 |

The route mix (75% GENERAL/25% AXIS_MVT) is hypothetical, not
measured globally. Costs for enlarged spatial boxes combined with
a coarse Hessian rule were NOT jointly measured.

The spatial empirical model is **not predictive on wide boxes**.
For GENERAL, median relative residual on training cases is 51.5%
and maximum absolute residual is 3.614; do not extrapolate
a single nominal quadratic formula to 1/16 boxes.
LOCAL_WIDTH_EMPIRICAL.md gives a more faithful local P1 piecewise
interpolation, conditioned on h_R=h_tau and h_lambda=1/16.
It is still NOT a rigorous upper bound or a global result.

**DIAGNOSTIC_ONLY / NOT_EVIDENCE.**
