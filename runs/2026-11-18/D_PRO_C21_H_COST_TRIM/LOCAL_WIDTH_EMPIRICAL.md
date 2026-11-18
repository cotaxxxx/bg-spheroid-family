# C21 H observed width and fit limitations
**DIAGNOSTIC_ONLY / NOT_EVIDENCE** — post-measurement interpretation only.

## Formal empirical function (not a bound)

COST_MODEL.json provides a separately fitted nonnegative additive model
for GENERAL and AXIS_MVT:

w_hat(h_R,h_tau,h_lambda) =
c0 + a_R*h_R + a_tau*h_tau + a_lambda*h_lambda
+ b_RR*h_R^2 + b_Rtau*h_R*h_tau + b_tautau*h_tau^2
+ b_Rlambda*h_R*h_lambda + b_taulambda*h_tau*h_lambda
+ b_lambdalambda*h_lambda^2.

All h are halfwidths; each coefficient is a median of actual
signed correction halfwidth divided by the nominal monomial.
This is an empirical decomposition, not a rigorous upper bound.
The formal model is NOT reliable for large boxes.

- GENERAL training count 10: median relative in-sample error 0.514566;
  maximum absolute error 3.614183.
- AXIS_MVT training count 8: median relative error 0.093444;
  maximum absolute error 0.003066.
- In AXIS_MVT, actual Taylor variables are rho_prime,z,lambda;
  nominal h_R,h_tau are NOT their halfwidths. No valid enlarged
  P3 tau experiment was available, so varying axis spatial
  coefficients is not identifiable from these samples.

## More faithful local P1 spatial-scaling interpolation

For P1, hold h_R=h_tau=h and h_lambda=1/16
(lambda width=1/8), with original 16x32 ratio1/2 order4
for all signed terms. Exactly three measured values:

| h_R=h_tau | H halfwidth | H second-order correction halfwidth |
|---|---:|---:|
| 1/128 | 0.038652064045891166 | 0.03176041290862486 |
| 1/64 | 0.2400418280158192 | 0.2319632088765502 |
| 1/32 | 3.92003570869565 | 3.9093684181571007 |

Piecewise interpolation, NOT a bound or an extrapolation:

If 1/128 <= h <= 1/64:
w_hat_P1(h;h_lambda=1/16) =
0.038652064045891166 * (h/(1/128))^2.634668459528212.

If 1/64 <= h <= 1/32:
w_hat_P1(h;h_lambda=1/16) =
0.2400418280158192 * (h/(1/64))^4.029509069476699.

These exponents differ because the outer Hessian interval itself
inflates when the spatial box is enlarged. A single quadratic
polynomial in physical h_R,h_tau,h_lambda does not capture it.
No prediction is supported for other points, lambda thicknesses
or beyond this h interval.

## Cost extrapolation warning

COST_METHOD_SCENARIOS.md and COST_METHOD_SCENARIOS.json show
method-specific arithmetic for 12 workers and 3 assumed initial grids.
The attractive low-cost cases require simultaneously:
1. wide lambda slabs valid even at lambda approximately2;
2. a very low spatial splitting fraction at 1/16 base grids;
3. fast coarse Hessian mesh remains effective on those wide boxes.

NONE of these three combinations has been independently established.
In fact, the measured P1 1/16 spatial box H halfwidth=3.9200
cautions strongly against treating the assumed f=0.25 as measured.
The near-2 local P1 and P3 intervals do NOT give a full
lambda-slab sign certificate. Cost estimates are scenarios only.

**DIAGNOSTIC_ONLY / NOT_EVIDENCE**.
