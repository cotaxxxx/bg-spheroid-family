# M2 fifth note: axis center regularization and two distinct small scales

2026-11-19. DIAGNOSTIC_ONLY / NOT_EVIDENCE.

## Exact z=0 specialization of the axis derivative

Using the M1 definitions and the derivative in M2_AXIS_KERNEL_DERIVATIVE_20261119.md, at z=0 put
D0=mu^2+epsilon^2(1-mu^2),
B0=1-(1-epsilon^2)mu^2,
g0=epsilon/(sqrt(D0)*sqrt(B0)),
V0=mu/D0,
L0=mu(1/D0-1),
W0= -mu^2/D0 -1/D0 +2mu^2/D0^2.
Then
partial_z I(mu,0)=
 [mu Q(g0)-V0(F'(g0)+g0 F''(g0))]*
 epsilon L0/(sqrt(B0)*sqrt(D0))
 -g0 F'(g0) W0.
Consequently
E_zz(0,0)=integral_0^1 partial_z I(mu,0) dmu.
This formula has no z denominator and no subtraction of two separately evaluated I terms. It is a direct symbolic specialization, not a sign claim.

## Two distinct moving layers in mu

At z=0 the first denominator D0 transitions at mu~epsilon (provided mu not close to 1). The second denominator B0 transitions at 1-mu~epsilon^2 when epsilon is small. Therefore a global interval treatment in mu with a single uniform grid can miss **two different scales**, near mu=0 and mu=1. This is a geometric observation from the explicit denominators, not a quantitative error bound.

A prospective analytic/interval decomposition for z=0 is
[0,c epsilon] union [c epsilon,1-c' epsilon^2] union [1-c' epsilon^2,1],
with c,c'>0 fixed before numerical testing and with empty/misaligned intervals handled for moderate epsilon. For z !=0 the D2 layer moves to mu=z (when z in [0,1]), while the B layer remains at mu=1. Since the reflection formula includes u z for u in [-1,1], the D2 layer may cross the endpoint mu=0 as u changes. A uniform proof must account for this moving geometry.

## Correctness checks

D0 and B0 are NOT the same function: D0=epsilon^2+(1-epsilon^2)mu^2, B0=1-(1-epsilon^2)mu^2. In particular D0(0)=epsilon^2, B0(0)=1; D0(1)=1, B0(1)=epsilon^2. Any cancellation or coding that identifies these denominators would be invalid.

The fixed-z FTC representation remains valid for each epsilon>0. Its use does not imply uniformity as epsilon->0. No positive lower bound on E_zz(0,0) or on E_z/z has been obtained.

## Next needed work

Derive sign-preserving bounds separately on the D2 moving layer and B endpoint layer, including their overlap as z approaches 1. Do not infer a positive axis bound from pointwise asymptotic alone. No new numerical plan executed; no finite Lambda1.

Heavy PID 1581407 untouched. main/STATE/ledgers unchanged.
