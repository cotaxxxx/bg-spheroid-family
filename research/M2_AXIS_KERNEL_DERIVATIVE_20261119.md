# M2 fourth derivation: axis kernel derivative with shared variables

2026-11-19. DIAGNOSTIC_ONLY / NOT_EVIDENCE.
Source: original M1 MATH_DERIVATION_BEFORE_PROBE.md on research/d-pro-tail-axis-dig-math-probe-20261119.

## Exact differentiation (epsilon>0, |z|<1)

On the axis rho=0, fix mu in [0,1] and define
w=mu-z, D2=w^2+epsilon^2(1-mu^2),
B=1-(1-epsilon^2)mu^2, k=1-z mu,
gamma=epsilon k/(sqrt(D2) sqrt(B)).
Define
V=k w/D2,
J(gamma)=gamma F'(gamma),
P(gamma)=F(gamma)+gamma F'(gamma).
Then M1's exact axis integrand is
I(mu,z)=mu P(gamma)-V J(gamma).
Since B does not depend on z,
partial_z gamma=epsilon/(sqrt(B) sqrt(D2))[-mu+k w/D2].
This expression avoids dividing by k or gamma, and is valid also when a factor vanishes.
Also
partial_z V=-mu w/D2-k/D2+2 k w^2/D2^2.
As P'=2F'+gamma F''=Q and J'=F'+gamma F'',
partial_z I =
 [mu Q(gamma)-V(F'(gamma)+gamma F''(gamma))] *
 epsilon[-mu+V]/(sqrt(B) sqrt(D2))
 - gamma F'(gamma)[-mu w/D2-k/D2+2 k w^2/D2^2].

Combining with the exact odd difference identity,
E_z(0,z)/z=(1/2) integral_{mu=0}^1 integral_{u=-1}^1 partial_z I(mu,u z) du dmu.
At z=0 this equals integral_0^1 partial_z I(mu,0) dmu.
All occurrences of w,k,D2,gamma,V in the derivative are to be evaluated at the common argument (mu,u z), never independently intervalized before algebraic grouping.

## Endpoint and regularity notes

For epsilon>0 and |z|<=sqrt(1-S0^2)<1, D2>0 throughout mu in [0,1]; at mu=1, D2=(1-z)^2>0. B>=epsilon^2>0. Thus differentiation and the finite-segment fundamental theorem are legitimate for each fixed epsilon. This does not imply estimates uniform as epsilon tends to zero.

## Why this is not a positivity certificate

The displayed partial_z I is not manifestly positive and can contain cancellations between its two terms. A rigorous T2 proof still needs a positive lower bound for its integrated value, uniformly in epsilon and z, including z=0 and the S=S0 endpoint. In particular, interval-enclosing partial_z I term by term without preserving common dependencies can remain too wide.

## Next analytic targets

1. Symbolically collect the expression by L=-mu+V and the shared D2 to expose cancellation.
2. Split the mu integral into the moving band |mu-z|<=c epsilon and its complement, retaining a common numerator and explicit tails.
3. Establish a uniform remainder bound for the normalized axis quantity lambda E_z/[z(1+log lambda)] rather than differentiating a C0 asymptotic of E.
4. In parallel derive a uniform upper bound on R_H^(2) for T1; do not treat a fixed-interior O(t^-3) as uniform.

No numerical probe performed. PID 1581407 untouched. No main/STATE/ledger modifications. No Lambda1 claimed.
