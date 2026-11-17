# D-PRO R4 box2 — Chat implementation receipt (2026-11-18)

**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

Original instruction: fixed V34 / Codex R4 v2 at commit `da8ad02b97c3d1a58f941bd1f905a57974540881`. This implementation was written by ChatGPT because Codex access was unavailable. Source reuses the CW7 polynomial and positive-denominator constructions, not the CW7 zero-order coefficient integration.

## Stage 0: one spatial cell

- Integration coordinates: h in [0,1/8], v=2theta/pi in [1/4,3/8], w in [1/4,3/8].
- 64 smaller cells (4 subintervals along each spatial axis).
- 35 outer-degree-4 coefficients, each integrated with 3D tensor Simpson and proven interval fourth-derivative error; **no zero-order Riemann quadrature of signed coefficients**.
- Precision: python-flint 0.8.0; 128-bit Arb; Python 3.11.16.
- Stage0 35-coefficient sum of interval halfwidths: **8.7842754824261e-06**, fixed component budget 1e-5.
- Algebraic outer-model remainder B4 integrated upper: **2.7608163057006e-06**.
- Sum of halfwidths and B4: **1.1545091788127e-05**. This number applies ONLY to the single spatial cell.
- Fixed relative-denominator-majorant threshold: 1/8. Maximum across 64 cells: **0.12313286327269**. Violations: 0.
- Independent 60-dps mpmath numerical reference, 8- vs 12-point tensor Gauss-Legendre grid: maximum grid difference 4.504578239907913819418e-20. All 35 reference values are contained in Arb intervals (diagnostic only, not a rigorous reference-integral error bound).
- Chat's coefficient quadrature wall time on daybreak-works: **26.251 s**, peak RSS **33112 KiB**; single process.
- Stage0 automated receipt: **PASS** under the frozen single-cell budgets.

## Earlier low-resolution attempts retained

- Single unsubdivided spatial cell: **FAIL**, sum-halfwidth ≈89655.7493.
- Spatial 2x2x2: **FAIL**, sum-halfwidth ≈0.007212083760.
- Spatial 4x4x4: **PASS**, sum-halfwidth ≈8.784275e-6.

The first two failures are numerical-precision diagnostics, not violations of rigorous inclusion and not claims that W is negative.

## Stage1: only a cheap fixed-rule preflight

- 5x5x5 exact grid of spatial point locations; 125 tests.
- At 61/125 locations the fixed CW7-style outer majorant A_j(1) exceeds 1/8.
- Maximum pointwise A_j(1) ≈0.3249892603166.
- Under the same pointwise coefficientwise-absolute-value majorant, spatial refinement alone cannot make the upper bound <=1/8 at a cell containing such a point.
- **Stage1 was not executed**. No full-box2 W interval, no conditional or global mathematical proof was obtained. A newly frozen outer-box division or sharper majorant is required.

## Provenance and scope

All receipts are diagnostic only. mpmath reference precision is not a rigorous quadrature accuracy guarantee. The Arb Taylor/Simpson and CW7-derived majorant routines have not undergone a separate external mathematical audit. Full box2 and global A/Z/C/Q/B remain **OPEN**.

No changes to main, STATE.md, R1–R3, Julia, existing branches or prior evidence.
