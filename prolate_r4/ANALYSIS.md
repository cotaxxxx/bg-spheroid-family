# D-PRO R4 fixed-denominator ratmodel — Chat Stage 0

**2026-11-18 / DIAGNOSTIC_ONLY / NOT_EVIDENCE**

## Source and scope

The implementation follows the exact Codex instruction v2 at commit `da8ad02b97c3d1a58f941bd1f905a57974540881` (V34). It uses the CW7/CW4 polynomial identities and positive denominator bounds, but **does not reuse CW7's spatial interval-range × volume quadrature for coefficients**.

Fixed box2: R=[95/128,97/128], tau=[15/128,17/128], lambda=[1279/256,5]. Outer Taylor variables (R,t,q), t=4tau²/(1+tau²)², q=lambda^-2, centered at (3/4,256/4225,(512/2559)^2) with enclosing rational radii. Total outer degree 4 (35 coefficients).

Stage0 cell: h=[0,1/8], theta=[pi/8,3pi/16], w=[1/4,3/8]. Parameter v=2theta/pi belongs to [1/4,3/8]. The measure is (1/2)dh dv dw. Four equal subintervals per axis yield 64 spatial patches.

## Certified component: signed coefficient quadrature

For each `c_alpha` the tensor Simpson rule uses three nodes and positive rational weights in each axis, summed with factor (subcell volume/2). At a given subcell, three separate 4th-order univariate jets are evaluated with the other two space variables as enclosing Arb intervals. If the Taylor coefficient of order four is `j_{4,x}`, then `f_x^{(4)}=24 j_{4,x}`. Classical Simpson's exact derivative remainder yields an integral error per axis bounded by

  (subcell measure) * (L_x^4 / 120) * sup |j_{4,x}|.

The product quadrature error follows from telescoping the three integration operators and the three positive-weight Simpson operators. Summing absolute error contributions for the three axes gives an interval enclosing the signed integral of each `c_alpha`. **No zero-order spatial Riemann sum is used for these coefficients.**

All computations involving the 35 outer Taylor coefficients and their spatial jets are 128-bit Arb via python-flint 0.8.0. Positive denominators are inverted using separately proven positive rational endpoints, preserving inclusion even when a broad Arb ball crosses zero.

The fixed stage0 budget for the **sum of the 35 coefficient interval halfwidths** was 1/100000. Measured sum: ~8.784275482426082e-6, hence this component meets its budget. Wall: 26.250740916933864 seconds (one process). Peak RSS: 33112 KiB.

Independent **nonrigorous** mpmath reference uses a separate implementation of the positive polynomial `p`, 60-digit working precision, and tensor Gauss-Legendre 8 vs 12 nodes. Max observed difference ~4.5045782399e-20; this grid difference does not prove 50 correct decimal digits. All 35 numerical reference values fall in their respective Arb intervals, checked with exact rational comparisons of their decimal strings.

## Certified component: algebraic remainder for the same cell

The CW7-style degree-4 majorant uses strict positive lower bounds for D0 and S0, interval absolute coefficient bounds for the R², delta, s factors and numerator, and the upward-rounded tail G(1)-sum(g_0,...,g_4). The scalar `B4` bound is nonnegative, hence a zero-order positive upper Riemann sum is allowed **only for the tail**, in agreement with v2.

On all 64 spatial patches the fixed acceptance threshold A_j(1)<=1/8 held; maximum ~0.12313286327269117. Integrated tail upper bound ~2.760816305700633e-6. Coefficient interval-halfwidth sum plus this tail is ~1.1545091788126715e-5, for **this spatial cell only**, not the box2 W.

## Stage 1 fixed-rule feasibility gate

A preflight evaluated the same degree-4 denominator majorant at 125 degenerate spatial points on the 5×5×5 grid h=-1,-1/2,0,1/2,1; v,w=0,1/4,1/2,3/4,1.

At **61/125 points**, A_j(1)>1/8; maximum ~0.32498926031659753. Under the specific coefficientwise-absolute-value majorant currently implemented, merely subdividing space cannot lower a whole-cell upper bound below the value at a contained point. A full box2 run with this fixed threshold and no outer-box splitting would therefore be futile. This does not say the Taylor model fails, and does not preclude a stronger correlated majorant or a separately frozen subdivision of the outer box.

**Stage 1 was NOT executed.** No full-box2 interval W was produced. No global proof, sign claim, or total-box count is asserted.

## Files and limits

- `prolate_r4/stage0.py`: rigorous coefficient quadrature, interval jets and bounded Simpson remainder.
- `prolate_r4/majorant.py`: rigorous nonnegative order-4 outer-model remainder on spatial subcells.
- `prolate_r4/reference50.py`: independent nonrigorous high-precision numerical comparison.
- `runs/.../stage0_split4.json`, `majorant_split4.json`, `reference_check.json`, `stage1_preflight.json`: machine-readable receipts.
- `stage0_split2.json`, `stage0.json`: failed coarse spatial rules retained, not deleted.
- `SHA256SUMS`: final artifact SHA-256 list.

**OPEN:** independent verification of the program and the derivation of the spatial remainder, stage1 box2 coverage with an admissible fixed majorant strategy, proof that W>0 on the box2, conditions A/Z/C/Q/B, and all global claims.

The user's original CW7 archive and V34 instruction are not modified; the independent new branch is the only output target.
