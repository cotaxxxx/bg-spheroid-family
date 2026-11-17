# RUN RECEIPT: D-PRO R4 v3 §6 H and V35 W split gate

2026-11-18 / **DIAGNOSTIC_ONLY / NOT_EVIDENCE**

## Verdict and scope

- **H (horizontal) box2 one-box Arb interval obtained.** Producer's signed
  high-order Taylor/mean-value method meets the pre-registered development
  halfwidth target `1/10`.
- H is measured **without any z derivative**. All 5 requested reference
  values are contained with the source's `1e-7` diagnostic margin.
- **W stage0 remains the previous v2 PASS** (35/35 reference inclusion).
  The full box2 W is **OPEN / not computed**.
- New **V35 option (a)** 2x2 R×tau W stage1 split and threshold were
  fixed before the pointwise preflight. The exact patch/depth/time rules
  were fixed before the continuous-patch preflight. Five-by-five-by-five
  point preflight per child found no `A>1/4` violation, but the subsequent
  **continuous Arb-patch B4 cover STOPPED in every child** at the frozen
  depth=16 cap. No rigorous B4 integral over an entire child was produced.
- No full-domain computations, sign decisions or official certification.

## Environment

- Device: `daybreak-works` (single process)
- Python: `3.11.16`
- `python-flint==0.8.0`, Arb 128-bit
- Read-only R3 lineage: pinned `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`
- H spatial quadrature: signed 4th-order Taylor, 8,832 fixed cells,
  `base_u=16`, `base_v=32`, `distance_ratio=1/2`, cap=0
- H outer evaluation: first-order multivariate mean value with **signed**
  4th-order spatial integration of all derivative integrands (not CW7
  zero-order range × measure).

## H box2 result

| Quantity | Value |
| --- | ---: |
| H interval lower (display) | −0.19906239819194732 |
| H interval upper (display) | −0.12023792779020574 |
| H interval halfwidth | **0.03941223520087078** |
| H central point integral interval | [−0.15979136029729696, −0.15950896568485612] |
| H central point integration halfwidth | 0.0001411973062204197 |
| R contribution halfwidth | 0.011478725442430004 |
| τ contribution halfwidth | 0.027484691236168146 |
| λ contribution halfwidth | 0.00030762113419768866 |
| H halfwidth / abs(source H center reference) | **0.24686601418204498** |
| Fixed H halfwidth budget | 0.1, **PASS** |
| Wall time | **172.89816685020924 seconds** |
| Center integration | 28.136802014894783 seconds |
| R derivative signed integration | 48.20118935033679 seconds |
| τ derivative signed integration | 48.168739643879235 seconds |
| λ derivative signed integration | 48.27106551127508 seconds |
| peak RSS | **36,288 KiB** |
| Reference containment | 5/5 with stated 1e−7 margin |
| Kernel crosschecks vs pinned R3 fx/ρ | 15/15 interval intersections |

Full rational endpoints and the exact Arb-derived interval are in
`H_box2.json`. Numbers in this table are presentation approximations only.

## W comparison (not a matched-machine speedup)

- Historical frozen V32 W center reference: approximately 2.0659.
- Historical V32 W 2nd-order box2 halfwidth: 0.836835755,
  runtime 2728.914 seconds, **recorded on another computer**.
- v2 stage0 was a single spatial cell, not a full W box2 interval.
- This v3 does not deliver a box2 W enclosure or a same-machine runtime
  for W. Ratios of H and W widths or runtimes cannot establish one
  route's overall cost.

## V35 correction / frozen W option (a)

Correct audit commit:
`e5f1b2450c31481f1e32bf58ad96245e92df9d4f`.
The A<=1/8 threshold of v2 was only a research design choice, not
a mathematical requirement.

Pre-registered before W diagnostic: split R and tau each into 2;
keep original λ interval unchanged; require `A<=1/4` **and**
per-child rigorous `B4 integral<=0.03`. Rules and hard depth/leaf/time
caps are recorded in `STAGE1_W_RULE_FREEZE.md`.

### Pointwise preflight

4 children × 125 rational spatial points = 500 point evaluations.
All four children had 0 pointwise A>1/4 failures.
The maximum sampled A by child was:

- [0,0] 0.15173996538596699
- [0,1] 0.15076445817334885
- [1,0] 0.15395751436767455
- [1,1] 0.1529801288630641

These are **NOT** interval bounds over the spatial continuum.

### Arb continuous B4 cover preflight

The pre-registered spatial patch subdivision stopped with
`DEPTH_LIMIT_A` in all four children, after 11.4460 seconds total.
The latest accepted patch counts were 11004, 10655, 12438 and 11965
respectively, but these are **incomplete partial sets**. No rigorous
full-child B4 upper bound exists, and no box2 W enclosure follows.
Code did not loosen the threshold, depth, or other limits in response
to the result. Full 35-coefficient integrals of W over each child were
not launched.

## Verification

- `checker.json` passes the exact-rational file/contract checks
  (interval addition, correct outer box, 5 references, gradient
  correction radii and fixed width budget). This **does not**
  independently certify the producer's analytic quadrature.
- `h_kernel_crosschecks.json` performs 15 pointwise interval overlap
  checks against the pinned R3 physical rho derivative. This shares
  its geometric upstream and is **not a clean-room mathematical proof**.
- The first H run failed **only at JSON generation**, where a decimal
  reference string was passed directly to `fmpq`; original stack
  trace is saved as `H_initial_failed.log`. The exact decimal parser
  was corrected and the entire fixed H integration was re-executed.
- Existing main, STATE.md, R1–R3, Julia, v2 branch and historical
  evidence remain unchanged. A separate v3 branch is used.

## Outstanding

Independent mathematical code audit of the H enclosure; a newly
frozen refinement rule or a more correlated majorant for the four
W children; signed higher-order coefficient integration for W
over the **full** spatial domain; comparison of full H/W costs.
No assertion of the global prolate theorem.

**Condition A: OPEN.**
