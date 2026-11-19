# Dig M3 / V47 response: exact elementary-function residual budget

2026-11-19. DIAGNOSTIC_ONLY / NOT_EVIDENCE. Analytic derivation only; no numerical pilot.

## Inputs
epsilon=lambda^-1, lambda>=5, S=sqrt(1-z^2) in [S0,1], S0=2^-12.
A_lambda(z)=asinh(lambda(1-z))+asinh(lambda(1+z)).
B_lambda(z)=atan(lambda(1-z))+atan(lambda(1+z)).
Exact M1 two-term identity yields H<0 iff
R_H^(2)/S < T_lambda(S,z):=(pi/2)A_lambda(z)-(3S/2)B_lambda(z).

## A rigorous uniform positive budget
For a,b>=0, asinh(a)+asinh(b)>=asinh(a+b), e.g. sinh(asinh a+asinh b)=a sqrt(1+b^2)+b sqrt(1+a^2)>=a+b and sinh is increasing. With a=lambda(1-z), b=lambda(1+z), this yields
A_lambda(z)>=asinh(2lambda).
Because atan is concave on [0,infinity), Jensen yields
B_lambda(z)<=2 atan(lambda).
Therefore
T_lambda(S,z)>=(pi/2)asinh(2lambda)-3S atan(lambda)
>=g(lambda):=(pi/2)asinh(2lambda)-3atan(lambda).

g'(lambda)=pi/sqrt(1+4lambda^2)-3/(1+lambda^2).
For lambda>=5, g'>0: pi>3 and (1+lambda^2)>sqrt(1+4lambda^2) since lambda^4-2lambda^2>0. Also g(5)=(pi/2)asinh(10)-3atan(5)>0 (direct elementary evaluation, approximately 0.59). Consequently T_lambda(S,z)>=g(5)>0 for all lambda>=5 and all S in [S0,1]. This is a uniform *positive allowance*, NOT an upper bound on R_H^(2)/S, and does not prove T1.

The S-dependent allowance (pi/2)asinh(2lambda)-3S atan(lambda) is stronger for S small. Preserve the exact T_lambda in final interval tests; use this lemma only as an analytic fallback.

## G1 alternative and partition
The Judge's alternative is to prove E_z>0 for lambda S<=K, thereby reducing the H-based T1 obligation to lambda S>=K. This is a proposed division of labor, not an established sign result beyond the existing G1 scope. A comparison must explicitly account for the growth of G9's northern term at large w. Do not extend the existing G1 conclusion beyond lambda S<=1 without proof.

## Remaining obstacles
L1: rigorously bound R_H^(2)/S from above in the contact collar, possibly only on lambda S>=K.
L2: bound the integrated axis derivative from below, preserving the moving mu~u z layer and the mu~1 endpoint layer.
No explicit Lambda1, no cost extrapolation.

## Governance
Mathematics precedes any numerical pilot. No pilot plan or pilot SHA is applicable yet. Any later pilot requires a frozen plan and SHA-256 before execution, and separate derivation/results reports. Heavy PID 1581407 untouched; no changes to main, STATE or ledgers. Await independent chat audit.
