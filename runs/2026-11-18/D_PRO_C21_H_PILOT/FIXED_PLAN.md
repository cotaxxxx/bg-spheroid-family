# D-PRO C21 representative-box pilot / FIXED RUN PLAN
2026-11-18. DIAGNOSTIC_ONLY / NOT_EVIDENCE.

ONLY the named representative boxes: G2, G35, AX, EQ, CE, BD, STRIP_00...STRIP_15, LW.
No global-domain covering. H is calculated solely from laboratory rho derivatives, never Ez.

G2 R[63/128,65/128] tau[63/128,65/128] lambda[2,513/256].
G35 same R/tau, lambda[1791/512,1793/512].
AX same R, tau[63/64,1], lambda[1279/256,5].
EQ same R, tau[0,1/64], lambda[1279/256,5].
CE R[0,1/64], tau[63/128,65/128], lambda[1279/256,5].
BD R[63/64,1], tau[63/128,65/128], lambda[1279/256,5].
STRIP_k R[k/16,(k+1)/16] k=0..15, tau[0,1/64], lambda[1791/512,1793/512].
LW same R/tau as G2, lambda[2,9/4].

Fixed Arb: Python 3.11.16, python-flint 0.8.0, 128 bits, single-process measurements.
Spatial signed Taylor quadrature: order 4, base_u=8, base_v=16, distance_ratio=2,
max_cells=40000, max_depth=28. No zeroth-order spatial range*measure integral
for any coefficient or external-parameter derivative.
Regular route: direct rho derivative / rho, signed 4th-order center and
three signed 4th-order outer derivatives plus a first-order mean-value bound.
AX, CE, STRIP_00: regularized H = integral_0^1 E_rho_rho(s*rho,z) ds
at fixed z. Four equal Simpson panels in s, signed 4th-order angular
Taylor for nodes and first external derivatives, with outward 4th s
derivative remainders. Nonnegative s remainders may be bounded by suprema.
BD, STRIP_15: fixed contact cap kappa=1/4096 and one cap correction
using |f_rho| <= pi^2/4 + pi*(1+lambda_max) and rho>=Rlo*cos(beta_hi).
All other strip boxes: regular rho derivative.
Fixed per-box runtime cap 120 seconds; timeouts -> OPEN, never PASS.
Record exact interval, halfwidth, normalized halfwidth, zero-inclusion
as metadata only (not strategy selection), direction contributions, seconds,
RSS, failures. Never invent interval for incomplete meshes.

W B4 independent pilot:
Keep v3 (a) R x tau = 2 x 2; lambda unsplit; max_j A<=1/4,
B4 per-child rigorous spatial integral <=3/100. Replace prior SHARED
depth 16 by PER-AXIS depth counters (each axis at most 16).
Fixed h/v/w initial breakpoints inherited from v3, choose longest
normalized available axis (tie h,v,w), cap active/accepted leaves
32768, time cap 60 sec per child. Pre-registered greatest-B4
contribution tail-first refinement if initial A checks pass.
Never run 35-coefficient W full-child integral unless rigorous B4
cover gate passes. No global W runs.

No sign of H/W used to decide between methods. Record errors honestly.
Input pins: H v3 d1ac5c652a6da43e245a399e4c9c2c5b5858d656,
V36 audit 16d8c01b86327b8387f731bf09d1740c6ee31273,
R3 fdfb498f2117cc0c5d72e88cc3be05eac9727bd8.
