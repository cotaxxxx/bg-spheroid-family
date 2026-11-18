# Independent numerical E-reference rule — fixed before running
2026-11-18 / DIAGNOSTIC_ONLY / NOT_EVIDENCE

Use the **primitive** E formula exactly as supplied by Judge §4,
with p=(rho,0,z), rho=R(1-tau^2)/(1+tau^2),
z=2 R tau/(1+tau^2), lambda at midpoint.
For each evaluation, integrate over the physical sphere in
theta=acos(mu)∈[0,pi], phi∈[0,pi] with Jacobian sin(theta)
using **25 decimal digit mpmath**.
Use fixed tensor Gauss–Legendre rules 24x24 and 40x40 independently.
Finite difference is the five-point centered rho stencil
with h=0.004, holding z and lambda constant:
 (8*(E(rho+h)-E(rho-h))-(E(rho+2h)-E(rho-2h)))/(12 h rho).

Run centers of: G2, G35, EQ, CE, BD, AX, LW,
STRIP_00, STRIP_08, STRIP_15. These are fixed by
geometric categories, *not* their sign. Hard overall
time cap 180 seconds. Save uncompleted records as OPEN.
Compare BOTH numerical quadrature approximations to each already
computed Arb H enclosure, where present. No claim of rigorous
error for quadrature or five-point finite difference;
the 24/40 discrepancy is diagnostic only. It is not a
substitute for the original §4 2D adaptive mpmath integral
with mathematical error certification.
