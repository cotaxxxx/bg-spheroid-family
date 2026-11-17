# R4 W stage 1: pre-registered V35 response (NOT an execution result)

**2026-11-18 / DIAGNOSTIC_ONLY / NOT_EVIDENCE**

Upstream correction: **chat V35 commit `e5f1b2450c31481f1e32bf58ad96245e92df9d4f`**.
The previously supplied different V35 short SHA was incorrect.
The 1/8 acceptance threshold is a diagnostic design parameter, **not**
a mathematical necessity. V35 estimates A≈0.325 in the parent box's
worst directional sample, contributions from R and tau, q/lambda ≈0.0008.

## Fixed choice before any W stage-1 run: option (a)

Split outer box exactly **R x tau = 2 x 2**, **do not split lambda**:

- R: [95/128, 3/4], [3/4, 97/128].
- tau: [15/128, 1/8], [1/8, 17/128].
- lambda: [1279/256, 5] in all four outer subboxes.

Each child has its own **rational** center
`(Rmid, t(tau_mid), q(2559/512))`, with
`t(x)=4 x^2/(1+x^2)^2`, `q=lambda^-2`,
and enclosing rational radii computed from transformed endpoints.
**Do not preserve the parent radius, or silently recenter the t/q
interval midpoint after transformation.**

**Pre-registered per-child acceptance:**

1. Rigorous spatial-patch majorant for all three denominator factors,
   `max_j A_j(1) <= 1/4`.
2. Rigorous integrated `B4 <= 3/100` for that child, counted over
   all spatial cells. Since the four subboxes represent alternatives,
   the *per-child* bound is the relevant comparison; do not sum their
   B4 upper bounds as if they were disjoint spatial domains.
3. Signed 35 coefficient integrals through a verified high-order
   spatial quadrature (CW7's range x volume quadrature is **banned**).
4. Final child W interval halfwidth <= 1/10, with a frozen
   diagnostic allocation: tail <= 3/100, signed coefficient
   cubature uncertainty <= 5/100, polynomial value range <= 2/100.
   If a budget or containment check fails, record `FAIL` or `OPEN`;
   do not post-hoc relax or silently exclude patches.

**Geometry/patch rule for a future full child run:** start with
h breakpoints [-1,0,1/2,3/4,7/8,15/16,31/32,63/64,127/128,1],
v breakpoints [0,1/4,1/2,3/4,1],
w breakpoints [0,1/16,1/8,1/4,1/2,1];
split the longest normalized spatial side first, tie order h,v,w;
maximum depth 16, 32,768 leaves and 60 seconds wall time per child;
record all forced splits and resource stops. After all initial
cells satisfy the A threshold, refine the accepted cell with the largest
(measure x B4 upper) contribution, one longest-normalized-edge split at
a time, until the per-child total tail <= 0.03 or a fixed cap is hit. w refinement is fixed near zero and
h refinement near contact direction. This rule is diagnostic
and not an assertion that the majorant will be efficient.

**Gate:** Run cheap pointwise preflight separately on all four children,
report `POINT_DIAGNOSTIC_ONLY`, **never** mistake samples for a
uniform cell bound or integral tail. Full W stage1 only after a
separate strict interval preflight proves every patch can be
treated within the above budget and signed cubature is available.
If the gate fails, stop rather than extend CW7 or force a result.

## Separate v3 H route

The separate §6 direct horizontal derivative H implementation uses
R3's signed spatial Taylor integral. It has no R4 fixed-denominator
majorant `A`; therefore this W-oriented acceptance threshold does
**not** automatically block the H run. The H box2 measurement is
recorded in H_box2.json and independently contract-checked.
No sign of H or W is used to select between research strategies.

The original v2 fixed branch, R3 and Julia, main, STATE.md and
prior evidence are unchanged. Global theorem and condition A: OPEN.
