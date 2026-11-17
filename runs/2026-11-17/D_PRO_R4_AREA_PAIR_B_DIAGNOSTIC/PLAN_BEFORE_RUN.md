# D-PRO R4 / Method B — FIXED PRE-RUN DIAGNOSTIC PLAN

2026-11-17 / Judge-go / chat / `DIAGNOSTIC_ONLY / NOT_EVIDENCE`

## Inputs frozen before running

- Mathematical study input: Astra `ASTRA_D_PRO_R4_AREA_PAIR_REPORT_20261117.md`, uploaded file SHA-256 `5330f2b20055aa1236c6321cba208c48a71db020ef23ab81cb216a9ea13cee4f`. Method B is §6.3 (R4-29), Method C is (R4-1). This run covers **only B**.
- Frozen source: `cotaxxxx/bg-spheroid-family` R3 commit `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`, untouched `prolate_r1/`.
- Prior numerical baseline (not rerun): R3 `outputs/R3_WIDTH_TIME.tsv`: box2 half-width 8,020,670.30469, FAIL; lambda5 point at different coordinates half-width 0.000702314494447, PASS. Compare only identical physical coordinates in this study.
- Method B invokes exactly the R3 `density.evaluate(...,mode="W")` through R3 `api.mv_integral`; no changes to R3 functions, mesh, derivative routines, constants or setting; only the **route selection** is changed for boxes away from angle endpoints.
- Fixed input box 2: `R=[95/128,97/128]; tau=[15/128,17/128]; lambda=[1279/256,5]`.
- Fixed physical midpoint: `R=3/4, tau=1/8, lambda=2559/512`. Do not substitute midpoint after mapping to `t=4tau^2/(1+tau^2)^2`.
- `Config()`: 128-bit Arb / python-flint 0.8.0; quadrature order 6, base_u 32, base_v 64, distance_ratio 1/4, kappa=1/4096, cap_from=15/16, max_depth 28, max_cells 200000.
- Time: monotonic (nanoseconds) for each integral and stage; per-case resource guard 3600 seconds; process exit status and full Python stack trace preserved on failure.
- Diagnostic thresholds: point half-width <= 1/20; box half-width <= 3/10; **no sign-dependent splitting**; no parameter retune.
- R3 mode='W' has `f_beta/(R^2 a b)` with tau=tan(beta/2), `a=cos(beta),b=sin(beta)`. This is valid on box2 because tau lower 15/128>0 and upper 17/128<1; neither angle endpoint is in the box. `R>0` is verified.
- R3 `domain_for` determines whether cap is applied; on box2 cap is 0. Cap contributions are recorded separately even when zero.
- In the box evaluation, first evaluate at the **same physical midpoint** and then use R3's existing parameter-box mean value correction `mv_integral`. Both the point output and each correction component are recorded.
- All intermediate boxes use rational `fmpq` input endpoints; Arb values are bound outward to exact rational endpoints.
- No comparison to Method C yet, and neither method certifies the global W>0 statement.

## Failure/next-step decision

- If B box half-width <=3/10, record width PASS (still `NOT_EVIDENCE`) and propose independent math audit before use.
- If B box fails or times out, preserve result and reason; no hidden reruns with lower order/looser tolerances.
- Following B, prepare an **isolated C implementation specification** based on the Astra report, with exact symbolic identities and rigorous 3D quadrature obligations. Do not modify R3.
- Future Method C comparisons must use a new pre-run plan; no automatic runner or background jobs should be left running.

## Protection

Write only under `runs/2026-11-17/D_PRO_R4_AREA_PAIR_B_DIAGNOSTIC/` on the new branch `diagnostic/d-pro-r4-area-pair-b-20261117`. Do not alter R1/R2/R3 originals, main, STATE.md, FREEZE, Julia or earlier Dig evidence.
