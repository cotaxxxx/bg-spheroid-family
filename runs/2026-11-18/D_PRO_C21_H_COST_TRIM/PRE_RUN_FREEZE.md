# D-PRO (C21) COST-TRIM pilot — PRE-RUN FREEZE (2026-11-18)
**DIAGNOSTIC_ONLY / NOT_EVIDENCE** — measurements only, no covering, no certification and no `CLOSED` verdict.
Based strictly on cost-trim Judge instructions, C21 second-order baseline commit `0427b19d84e5105aa1a03ff69c9842065d491f3c`, V39 commit `544ebfd138c02d2fc68806184a1d0ce2e744fa2c`, pinned R3 `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`.
Output ONLY new branch `research/d-pro-c21-h-cost-trim-20261118`; no writes to main, STATE.md, old branches, tags, frozen Julia or pinned R3.

## Frozen probes
P1: R=[1/4,17/64], tau=[0,1/64], GENERAL, old baseline box R16_T00.
P2: R=[13/32,27/64], tau=[0,1/64], GENERAL, old baseline R26_T00.
P3: R=[1/4,17/64], tau=[63/64,1], AXIS_MVT, old baseline R16_T63.
P4: R=[7/16,29/64], tau=[63/64,1], AXIS_MVT, old baseline R28_T63.
Historical baseline uses old Stage B JSON, not new worker tasks; each baseline is exactly lambda=[1279/256,5], order4 / base16x32 / distance ratio 1/2 for all signed angular integrals.

## Fixed run list, before any measurements
(a) 4 probes x lambda widths [1/16,1/8,1/4], always L=[5-w,5], unchanged R,tau; **12 workers**.
(b) 4 probes x Hessian-only angular settings `(base_u=8,base_v=16,ratio=1,order=4)` and `(base_u=8,base_v=16,ratio=1,order=2)`, lambda=[1279/256,5], point & each gradient remain BASE `(16,32,1/2,4)`; **8 workers**.
(c) P1 fixed lower left R_lo=1/4,tau_lo=0, 1/32×1/32 and1/16×1/16, lambda=[39/8,5] (width1/8); **2 workers**.
(c) P3: tau_lo=63/64, so tau_hi=63/64+1/32>1 and tau_hi=63/64+1/16>1. Both requested boxes violate domain tau∈[0,1]. **Preregister as NOT_RUN_OUT_OF_DOMAIN**, without silently modifying corners. They contribute no measurements or empirical fit.
(optional) P1/P3 x lambda=[2,17/8], width1/8, same original1/64×1/64 R,tau; **2 workers**.
Total 24 valid executable jobs and 2 invalid prescribed cases. Sign is logged ONLY, never used for method selection, failure retry, stopping or sample selection. Fixed lexical ID `A_P1_L1_16` etc and deterministic stage order a -> b -> c -> low_lambda. No box selection changes after results.

## Frozen numerical method
- Python3.11.16, python-flint0.8.0, Arb128 bits; original C21 second-order kernel, parametrization, signed angular Taylor and fixed chart. Baseline `so.initialize(R,T,L)` supplies kernel and full base mesh. Original second-order Taylor formula:
  `H(center) + sum grad_i(center)*[-hi,hi] + 1/2 sum Hess_ii(B)*[0,hi²] + sum_{i<j} Hess_ij(B)*[-hi hj,hi hj]`.
- For Hessian coarse mesh only, recreate pinned R3 `make_mesh` with exact same geometry as frozen original and `Config(precision=128,order=hessian_order,base_u=8,base_v=16,distance_ratio=1,max_cells=40000,max_depth=28)`. Points and gradients retain the BASE mesh.
- Hessian n-th spatial Taylor coefficient remains **signed-integrated** with its own hessian order. The 2! diagonal mixed-jet multiplier and 1! mixed coefficient are unchanged. No unsigned zero-order proxy, no s-Simpson. Pinned positive denominator bound for MVT on entire extension; if invalid or mesh cap reached return OPEN (no guessed interval).
- The different mesh/order is chosen only by experiment ID. Never choose it based on observed H sign.

## Cost and stop rules
- Workers at most12 simultaneously, deterministic experiment groups and ordered checkpoint.
- Per-box hard timeout GENERAL 1800s; AXIS_MVT 2400s. Entire 4-group pilot **wall cap 7200s**, including optional near-2 probes, no background continuations unless the user requests a new run; no retry or automatic method switch.
- Record independent per-box signed center, 3 gradient and 6 Hessian intervals and their correction/elapsed time, complete outward-rational H interval, halfwidth, mesh counts for BASE and HESS, worker elapsed and peak RSS. OPEN and geometry-invalid cases must have null H with reason, not fabricated numbers. Write stdout/stderr for every actual job.
- Fixed Stage A,B,C,LOW ordering; Stage A lambda a tests are charged to this pilot, not counted as proof. Baseline4 historical times are labeled historical outside current elapsed time. No coverage, no adaptive splitting, no W evaluations.

## Cost model and extrapolation
- Build measured-only empirical width model, separately for GENERAL and AXIS_MVT near lambda=5. Use nonnegative additive terms for `hR,hTau,hLambda, hR²,hR*hTau,hTau²,hR*hLambda,hTau*hLambda,hLambda²` plus constant. Report fitting algorithm, training-point count, in-sample residuals, and domain limitations. Do not present an underdetermined or inaccurate fit as validated. For the MVT route clarify its actual external widths are rho',z,lambda; hR/hTau is only a regressor, not a Taylor variable.
- Cost extrapolation across full Rτ area uses transparent *hypothetical* uniform initial width and optional split fraction, plus mean observed per-worker cost and workers=12. Board λ counts are separately assumed: width1/8 all [2,5] means24 slabs; width1/4 all means12; baseline1/256 means768. Hypothetical lambda≈2 width must be a distinct assumption (e.g.1/1024 for [2,3], 1/8 for [3,5] gives1024+16=1040 slabs). The near-2 probes are not proof of valid λ slabs, and probes at R in [1/4,1/2] do not justify assumptions for other R.
- No numeric full domain claim without explicit hypothetical qualifiers. No proof status changes.

## Reproducibility and integrity
Preregister exact experiments in `EXPERIMENTS.json` in same pre-run commit, all policies and code fixed BEFORE any worker executes. Sources, each box JSON/log, comparison and model, one-line run command, deterministic ZIP, SHA256SUMS and ZIP SHA-256 recorded in this new branch. **DIAGNOSTIC_ONLY / NOT_EVIDENCE.**
