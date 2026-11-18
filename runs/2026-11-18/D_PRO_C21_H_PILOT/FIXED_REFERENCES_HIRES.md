# High-resolution independent E reference — fixed before the second run
2026-11-18 / DIAGNOSTIC_ONLY / NOT_EVIDENCE

The earlier fixed 24x24 / 40x40 25-digit primitive-E reference
results remain unchanged. These grid levels have non-negligible
disagreement at some boxes and are not rigorous error bounds.

This is a separate, pre-specified high-resolution check:
same fixed 10 named centers G2 G35 EQ CE BD AX LW
STRIP_00 STRIP_08 STRIP_15; same exact primitive E
formula, fixed z, rho 5-point derivative step h=0.004
and 25-digit mpmath. Use fixed 96x96 and 160x160
Gauss-Legendre tensor rules with exact spherical theta
Jacobian. Hard total wall cap 180 seconds; partial results
must be explicitly marked incomplete.
Compare each point reference to the existing coarse-grid
H interval only, and to the four fine-grid H intervals when
such a fine interval exists. No numerical sign decision
is used to select the proof route. No rigorous quadrature
error is claimed.
