# Separate calibration v2 — frozen before any v2 execution
2026-11-18 / DIAGNOSTIC_ONLY / NOT_EVIDENCE

The original FIXED_PLAN.md coarse-grid representative results remain
unchanged and do NOT count as having met a sign/width threshold.
This is a **second explicitly distinguished** diagnostic calibration
to quantify how much tighter a *different fixed* geometric mesh gets.

Cases chosen before any v2 run (NOT chosen by sign of H):
G2 (lambda2), G35 (lambda3.5), EQ (equator), STRIP_08
(a mid-radius equatorial strip). All primitive rational outer boxes
are identical to the original fixed plan.

For ALL FOUR calibration boxes, **uniform fixed rule**:
Python3.11.16, python-flint==0.8.0, Arb 128-bit;
signed 4th-order spatial Taylor, base_u=16, base_v=32,
distance_ratio=1/2, kappa=0 (all R upper<1),
maximum geometry cells 40000, max depth 28;
single subprocess hard timeout 240 seconds per box.
Center and all three external derivatives are signed high-order
Taylor-integrated; no zeroth-order coefficient integral.
No dynamic parameter splits or sign-driven choices.
Every result saved in separate *cal_v2* JSON/log.
A timeout/exception is OPEN, not a certificate.
The coarse FIXED_PLAN results and their logs remain immutable.

The calibrations test whether the large coarse-grid halfwidth
is merely a low-spatial-order mesh problem. They are not a
global covering or a complete mathematical audit.
