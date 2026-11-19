# M2 tail — explicit leading-term bound and conditional threshold

2026-11-19. DIAGNOSTIC_ONLY / NOT_EVIDENCE. Follow-up to M2_TAIL_PRELIMINARY_20261119.md.

## Normalization caveat

All statements involving lambda in the asinh/atan arguments below are **conditional on epsilon=1/lambda**. The normalization must be independently reconciled with the original M1 definition before any proof use.

## Exact elementary bound

Let S=sqrt(1-z^2)>0, lambda>0, and
A=asinh(lambda(1-z))+asinh(lambda(1+z)),
B=atan(lambda(1-z))+atan(lambda(1+z)).
Since asinh(x)=log(x+sqrt(1+x^2))>=log(2x) for x>0,
A>=2 log(lambda)+log(4S^2).
Also 0<B<pi for |z|<1.
Therefore the supplied M1 identity gives
H/epsilon <= -pi S log(lambda) -(pi S/2)log(4S^2) +(3pi S^2/2)+R_H^(2).

## Conditional uniform threshold

If a rigorously proved uniform upper bound R_H^(2)(q,lambda)<=C holds for all S>=S0, 0<rho<S and lambda>=lambda_base, then
H/epsilon <= -pi S log(lambda) -(pi S/2)log(4S^2) +(3pi S^2/2)+C.
Since S>=S0 and S<=1,
H/epsilon <= -pi S [log(lambda)+log(2S)-3/2-C/(pi S)].
Thus the sufficient condition
log(lambda)>3/2+C/(pi S0)-log(2 S0)
implies H<0 uniformly, provided C>=0.
A safe explicit integer threshold would be
Lambda_T1 = max(lambda_base, 1+ceil(exp(3/2+C/(pi S0))/(2 S0))).
This is only a *conditional formula*, not an achieved Lambda1. The required uniform C has not been established.

A sharper route is R_H^(2)<=C_S S, yielding
Lambda_T1=max(lambda_base,1+ceil(exp(3/2+C_S/pi)/(2 S0))).
The reduction from exp(O(1/S0)) to O(1/S0) is substantial, but requires a proved S-weighted remainder bound.

## Geometry and axis

For a fixed m, a horizontal core reference exists for all |z|<=sqrt(1-S0^2) only if m<=1-sqrt(1-S0^2). Even with that, rho_m(z) can be zero at the endpoint; NP10's transfer margin vanishes. A z-dependent core or direct near-axis treatment is needed.

The axis target T2 requires a common-numerator odd divided difference and a uniform explicit remainder; the pointwise asymptotic 3pi S alone is insufficient.

## Status

No numerical experiment executed. No CPU or process touched. No finite Lambda1 established. Main, STATE, ledgers unchanged.
