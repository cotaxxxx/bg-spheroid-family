# AX fallback after initial hard timeout — separate policy frozen pre-run
2026-11-18 / DIAGNOSTIC_ONLY / NOT_EVIDENCE

Initial AX four-panel s-Simpson pilot hit the pre-registered 120-second
timeout and is permanently recorded as OPEN in AX.json / AX.log.
Do not replace or retroactively relabel the initial AX attempt.

Second experiment `AX_RANGE_S` (different explicitly named result):
apply the exact integral mean-value inclusion
`H(rho,z) = integral_0^1 E_rho_rho(s*rho,z) ds`
by enclosing `E_rho_rho(s*rho,z)` **uniformly over s in [0,1]**,
then doing signed fourth-order R3 angular Taylor quadrature.
This is a RANGE in s, but **not a zeroth-order angular spatial integral**.
All first external derivatives likewise use signed fourth-order angular
quadrature with the full s interval. The s-uniform angular interval
also contains its s average, so there is no extra s discretization
error. Apply the same exact-rational 1st-order outer mean-value bound.
Policy: 128-bit Arb, python-flint0.8.0, base_u=8 base_v=16,
distance_ratio=2, order4, cap0; timeout120s; 40000 max cells.
No sign used for choosing this method; it is a post-timeout
engineering *comparison*, not a retroactive change to the first run.
