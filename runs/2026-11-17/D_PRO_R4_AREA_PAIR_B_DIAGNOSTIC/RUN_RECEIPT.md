# D-PRO R4 Method B｜指定箱2の直接W評価・研究用PC実測

2026-11-17 / chat–Dig / **DIAGNOSTIC_ONLY / NOT_EVIDENCE / WIDTH_B_BOX_FAIL / R4_MATH_AUDIT_OPEN**

## Provenance

- Pre-run frozen plan and exact diagnostic driver: commit `1cb5a08e67e79f92e1c120443fd14ed4bfdf2215` on `diagnostic/d-pro-r4-area-pair-b-20261117`.
- Plan SHA-256: `995f4e6431090809e7993fd05a1b98fe8454b7322a39a42c03644f343be87184`.
- Driver SHA-256: `4d5491109859f2ff21cfca76787c64eb6cde663e645be6aba2e1426bf9f423ae`.
- Source R3 commit: `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`; `prolate_r1/` source unchanged.
- Astra R4 source report: `ASTRA_D_PRO_R4_AREA_PAIR_REPORT_20261117.md` SHA-256 `5330f2b20055aa1236c6321cba208c48a71db020ef23ab81cb216a9ea13cee4f`, Method B §6.3, eq (R4-29).
- Comparison baseline: sealed R3 `prolate_r1/outputs/R3_WIDTH_TIME.tsv` row 33, box2 half-width `8,020,670.30469`, FAIL; R3 original remains unchanged.
- Python 3.11.16, python-flint 0.8.0, 128-bit Arb, default `Config()` (order 6, base 32×64, distance ratio 1/4, no sign-dependent refinements).
- Both point/box executed on research PC `daybreak-works`, with `PYTHONHASHSEED=0`, `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` and 3600s per-case time guard.

## Fixed geometry and method

- Full box: `R=[95/128,97/128]`, `tau=[15/128,17/128]`, `lambda=[1279/256,5]`.
- Same physical midpoint (NOT midpoint after t-transform): `R=3/4`, `tau=1/8`, `lambda=2559/512`.
- Method B reuses the existing R3 `density.evaluate(mode='W')`, `quadrature.make_mesh`, `api.integrate`, `api.deriv_integral` with unchanged settings; unlike the R3 router, it does not send the box to the even-endpoint 4th Taylor quotient branch.
- Geometric denominator `R² sin(beta) cos(beta)` is strictly positive throughout box2; rational lower `2178860625/17791291456 >0`.
- `domain.kappa=0`, so no cap contribution for this box.
- Same-point center evaluation and the R, tau, lambda outer-box derivative correction are computed and recorded separately.

## Results

| Item | Half-width | Outcome |
|---|---:|---|
| Direct Method B at physical box midpoint | `0.00035333001915205386` | **PASS** (threshold 1/20) |
| Direct Method B at full box 2 | `3.9948115795850754` | **FAIL** (threshold 3/10) |
| Prior R3 endpoint-Taylor method at the *same full box* | `8,020,670.30469` | **FAIL** (R3 source log; not rerun) |

- Full box Method B interval approximately `[-1.9289053992631053, 6.060717759907045]`, so **zero remains included**. Not a W>0 certificate.
- Ratio of **same-box** previous half-width / direct-B half-width: approximately **2,007,772**. This is a diagnostic width ratio only.
- Full box B midpoint component half-width: `0.0003519980855344329`.
- Full box B mean-value correction half-width: R `0.6819115057587624`, tau `3.2919227331876755`, lambda `0.020625334640499204`. Tau term is the dominant residual width.
- Point mesh 34,688 cells, elapsed **185.068 s** (wall guard time 185.20s), peak RSS **38,652 KiB**, exit 0.
- Box mesh 34,816 cells, elapsed **235.562 s** (wall guard time 235.64s), peak RSS **39,468 KiB**, exit **1 due solely to preregistered half-width FAIL**, not an exception.
- No stderr or runtime failures. R3 row33 was measured on the Codex machine; its 983s is not used for a hardware-normalized speedup claim.

## Interpretation and next work

1. Existing endpoint-Taylor quotient is confirmed to be unnecessary for box2's positive tau interval; evaluating the previously available direct W kernel reduces the box half-width by approximately 2.0 million-fold, without any changes to R3 quadrature precision, derivative definition or mesh rule.
2. B still misses the fixed 0.3 width criterion by a factor of about 13.3; the remaining overestimation comes largely from outer tau derivative interval range integration, not the midpoint point quadrature.
3. Astra's Method C (reflection-pair rational kernel R4-1) has **not been run with rigorous intervals here**. Its advantage remains a mathematical proposal pending new implementation and independent audit.
4. Neither an independently verified interval-soundness proof for this new route nor a global W>0 proof has been issued; R3 and its FAIL remain frozen.
5. The next isolated C experiment should first hold exactly the same full box/midpoint and thresholds, rigorously record each external derivative correction, and test whether its reflection-polynomial correlation reduces tau variation.

## Evidence

- `logs/point.json`, `logs/box.json`: complete exact-rational interval bounds, individual derivative terms, configuration, timing and half-width judgments.
- `logs/point.stdout`, `logs/box.stdout`, stderr, `.exit`, `.time` keep raw process evidence.
- `SHA256SUMS.txt` verifies all evidence files other than itself. The original plan and source driver were already sealed before testing.

**Verdict: R4_B_SOURCE_UNCHANGED / POINT_WIDTH_PASS / BOX_WIDTH_FAIL / SAME_BOX_2M_FACTOR_REDUCTION / METHOD_C_OPEN / DIAGNOSTIC_ONLY_NOT_EVIDENCE.**
