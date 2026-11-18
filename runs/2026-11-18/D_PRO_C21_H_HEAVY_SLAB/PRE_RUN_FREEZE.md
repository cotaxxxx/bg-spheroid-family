# D-PRO (C21) H heavy slab — PRE-RUN FREEZE
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**, 2026-11-18.
Original second-order H commit 0427b19d84e5105aa1a03ff69c9842065d491f3c; cost measurements 4b61116b43e601171c30225593e7fe3229a6d7c8; audit V40 fe73359; R3 pin fdfb498f2117cc0c5d72e88cc3be05eac9727bd8.
All code, route overlap precedence, budgets, order and sampling rule fixed by commit BEFORE timed H measurements. New branch research/d-pro-c21-h-heavy-slab-20261118 only. No main, STATE.md, Julia, old branch, tag or R3 changes.

## Plate and mesh
lambda = [79/16,5] (one unsplit plate).
R,tau = [0,1]^2, initial 64x64 (4096 roots), min edge 1/256.
128-bit Arb, Python3.11.16/flint0.8.0. Signed Taylor spatial integration only (no unsigned zero-order integration for signed components). Point + 3 gradients use 16x32, ratio1/2, order4. Hessian 6 components alone use 8x16, ratio1, order4. Max cells40000, mesh depth28.
Outer second-order Taylor: point + signed gradients(center)×[-h,h] + 1/2 diagonal Hessian(box)×[0,h²] + mixed Hessian(box)×[-h_i*h_j,+h_i*h_j].

## Frozen route precedence (geometry ONLY)
1. tau_hi=1 => AXIS_MVT, including axis+center and axis+boundary corners.
2. R_lo=0 => CENTER_MVT.
3. R_hi=1 => BOUNDARY_COLLAR with kappa=1/4096.
4. Else GENERAL.
MVT external variables are independent rho_prime=[0,rho_hi], z, lambda with fixed angular chart. No s quadrature. If rho_hi+z_hi>=1 or AXIS rho_hi>1/16, label OPEN_ERROR/TUBE and do NOT switch method. Axis+boundary thus safely OPEN if geometry bound unavailable. The direct boundary f_rho/rho uses capped signed integral and once-only uniform cap remainder from c21_regular.cap_bound; cannot use if rho_min<=0 (axis takes priority). GENERAL uses uncapped original direct kernel.
No route choice based on computed sign; only the frozen zero-membership predicate controls splitting.

## Partition ordering and limits
Root name Rii_Tjj. First geometric pre-selected roots: (0,0),(0,63),(63,0),(63,63),(16,0),(16,63),(32,32),(63,32),(32,63),(0,32),(1,1),(62,62). Other roots sorted by interleaved 6-bit Morton code. All roots depth0 before children depth1. Split zero-containing boxes by widest R or tau, R on exact tie, until both edges <=1/256, then TUBE_MIN. 1200s hard per-box; timeout/errors TUBE_OPEN_ERROR. Nonzero H interval => DECIDED. No H interval for OPEN errors, never fabricate sign.
12 concurrent workers, cumulative 129600s wall global cap (36h), resume on checkpoints. Each batch: persist inflight BEFORE and state AFTER. A shorter interactive session is not 36h completion, and its pending boxes remain PENDING_UNEVALUATED. Maximum interactive session and max batches are operational limits, not change of frozen geometry/algorithm.

## Ledger
Record per-node route, depth, box coordinates, full signed H interval, halfwidth, signed center+gradient+6 Hess components and individual times, RSS, both mesh counts. Route×depth counts/worker time, observed zero-interval split frequency; split amount, terminal tube and unprocessed area exact rationals; DECIDED+TUBE+PENDING exactly1. Tube distribution coordinate list + graphic of evaluated tube only. Until full slab or actual 36h cap, label extrapolation NOT_ESTIMABLE_FROM_PARTIAL_SLAB. Any global λ cost scenario must explicitly separate near-2 V40 local data and λ slab thickness assumptions. Do not imply the sample represents whole board.

## W
Only select 3 evaluated tube boxes (lexicographically sorted first/middle/last) at FULL slab completion or actual cumulative 36h cap. Otherwise W_SELECTION_DEFERRED. R3 quadratic angular_quotient with lambda same plate, kappa=1/4096, base16x32 ratio1/2 order4, W hard cap1200s and within 36h global remaining. Record time/width, no tube-wide W proof.

## Verification / publishing
Independent exact fraction partition checker, per-box H components and cap-once containment, source hash and run logs. Direct E reference test only on valid deterministic samples with available terminal boxes; axis-rho=0 not blindly finite-differenced.
Deliver source, precommit freeze, node JSON, summaries, diagram, one-line run command, SHA256SUMS, ZIP with SHA. Always **DIAGNOSTIC_ONLY / NOT_EVIDENCE**. Global C21 proof remains OPEN.
