# D-PRO R4 v3 / §6 H-box2 diagnostic

**2026-11-18 — DIAGNOSTIC_ONLY / NOT_EVIDENCE**

## Scope and provenance

Judge's v3 instruction replaces v1/v2. Its only new section is §6, measuring
the horizontal derivative `H=E_rho/rho` in the **same fixed box2**. The
stage0/v2 implementation and all its evidence are inherited unchanged from
commit `2f9a0e1c515d2c271ebb1b8be51659bf22623eab`. This v3 is on a
**new branch** `research/d-pro-r4-ratmodel-v3-h-20261118` because the v2
branch is already frozen and must not be altered.

The direct H density uses the laboratory horizontal derivative of the
primitive R3 geometry. It **does not compute or use E_z or any z derivative**.
The frozen R3 source is commit
`fdfb498f2117cc0c5d72e88cc3be05eac9727bd8` in
`cotaxxxx/bg-spheroid-family/prolate_r1`. All seven imported R3 files
(`__init__.py`, `api.py`, `center_bounds.py`, `density.py`,
`jets.py`, `intervals.py`, `quadrature.py`) were SHA-256 compared with the
corresponding files at that exact commit and matched.

## Mathematical definition

For `beta=2 atan(tau)`, `rho=R cos(beta)`, `z=R sin(beta)`,
`xi=(xi_x,xi_y,xi_z)` on the unit sphere, put

```text
k = 1 - R h; h = (rho*xi_x + z*xi_z)/R
Sigma = 1 + R^2 - 2 R h
D^2 = Sigma + (lambda^2 - 1)(xi_z - z)^2
B = 1 - (1 - lambda^-2)xi_z^2
gamma = k/(D sqrt(B))
G(gamma) = acos(gamma)^2
Rfun(gamma) = acos(gamma)/sqrt(1-gamma^2)
d_gamma/d_rho = [-xi_x + k(xi_x-rho)/D^2]/[D sqrt(B)]
f_rho = -xi_x G(gamma) - 2 k Rfun(gamma) d_gamma/d_rho
H = (1/(4 pi rho)) integral_sphere f_rho dOmega
```

This is a direct horizontal derivative, not a finite difference. For the
fixed box `R=[95/128,97/128]`, `tau=[15/128,17/128]`,
`lambda=[1279/256,5]`, all denominators remain strictly positive because
`R_hi<1`, `lambda<=5`, and `rho>0`. The implementation retains
the R3 analytic angular function enclosures and positive-reciprocal bounds.

## Rigorous spatial integration and outer box

A geometry-only 8,832-cell mesh is fixed **before** evaluation:
`base_u=16`, `base_v=32`, `distance_ratio=1/2`, `kappa=0`.
Univariate even-order Taylor integration of order **4** is used on `u` and
`v` for the **signed** center-point H integrand.

The three derivatives `dH/dR`, `dH/dtau`, `dH/dlambda` are each integrated
**signed** with the same high-order Taylor rule, using mixed jets
`(space order=4, external order=1)` over the entire outer parameter box.
**No zeroth-order spatial range sum is used for a coefficient.**

Let `Hc` be the rigorous point integral, and `Dj` the three rigorous
integral-derivative intervals over the box. The standard multivariate
mean-value theorem proves

```text
H(box2) is contained in Hc
  + D_R * [-1/128,1/128]
  + D_tau * [-1/128,1/128]
  + D_lambda * [-1/512,1/512].
```

The `lambda` midpoint is `2559/512`; `beta` is never re-centered.
No sphere cap is removed since `R_hi<1`. Pre-registered H diagnostic
halfwidth budget: `1/10`. The five source reference H values are diagnostic
point checks with the supplied `1e-7` error margin; those point checks
never replace rigorous interval containment.

## One-command Dig run (on daybreak-works)

```bash
cd /home/daybreak/D_PRO_R4_RATMODEL_V3_H_20261118/worktree && PYTHONPATH=/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source /home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python -m prolate_r4.h_box2 --order 4 --base-u 16 --base-v 32 --distance-ratio 1/2 --output runs/2026-11-18/D_PRO_R4_RATMODEL_V3_H_CHAT/H_box2.json
```

`python-flint==0.8.0` (Python 3.11.16), `ctx.prec=128`.
The output includes a full H box enclosure, halfwidth, ratio
`halfwidth / abs(H_center)`, 5 reference checks, wall-clock times and peak
RSS. Run from one process with no distributed workers.

Run the independent, standard-library file/contract checker (checks endpoint
arithmetic and reference values, **not** the underlying proof of interval
quadrature) with `python -m prolate_r4.verify_h_box2
runs/2026-11-18/D_PRO_R4_RATMODEL_V3_H_CHAT/H_box2.json`.

## Stage and stop conditions

The prior v2 **stage0** single-cell result is preserved:
35/35 reference containment and PASS for the frozen stage0 budget. The
v2 **W stage1** remains unexecuted; its preliminary fixed-1/8 majorant test
found 61/125 sampled locations exceeding the threshold. No full-box W
interval or same-computer W runtime has been produced by this v3. The
historical V32 W box2 halfwidth `0.836835755` and elapsed `2728.914 s`
were obtained **on a different machine**, so they are not a calibrated
speedup ratio. Existing Julia, main, STATE.md and the prior R3 / v2 branch
have not been modified.

## Limitations

This is a one-box diagnostic, pending independent mathematical audit of
the complete integration and source. It is not a proof of the large
prolate-domain condition A or of Z/C/Q/B. Neither the sign of H nor the
sign of W is used to choose the global route. That choice remains with Judge.
