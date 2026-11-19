# M2 sixth note: exact product identity at the axial center

2026-11-19. DIAGNOSTIC_ONLY / NOT_EVIDENCE.

## Exact identities

At rho=z=0, M1 uses epsilon=1/lambda, 0<epsilon<=1/5, mu in [0,1],
D0=epsilon^2+(1-epsilon^2)mu^2,
B0=1-(1-epsilon^2)mu^2.
Set a=1-epsilon^2. Direct algebra gives
D0+B0=1+epsilon^2
and
D0*B0=epsilon^2+a^2 mu^2(1-mu^2).
Consequently
gamma0^2=epsilon^2/(epsilon^2+a^2 mu^2(1-mu^2)),
and 0<gamma0<=1. Equality gamma0=1 occurs at mu=0 and mu=1; the minimum occurs at mu=1/sqrt(2), where
gamma0,min=epsilon/sqrt(epsilon^2+a^2/4)=2epsilon/(1+epsilon^2).
The last equality follows from 4epsilon^2+a^2=(1+epsilon^2)^2.

This identity preserves the correlation between D0 and B0; evaluating them as unrelated intervals discards the exact product structure.

## Two-layer interpretation and an exact level set

For any fixed theta in (0,1), the condition gamma0>=theta is equivalent to
mu^2(1-mu^2) <= epsilon^2 (theta^-2-1)/a^2.
Writing v=mu^2 and C=epsilon^2(theta^-2-1)/a^2, when 0<=C<1/4 the solution is the union
v in [0,(1-sqrt(1-4C))/2] and
v in [(1+sqrt(1-4C))/2,1].
For C>=1/4 the inequality holds throughout [0,1].
Thus the two endpoint layers are exact algebraic level sets of gamma0, not just heuristic scalings. For small epsilon with theta fixed away from 0 and 1, the left layer has mu=O(epsilon), while the right has 1-mu=O(epsilon^2).

## Scope and caveats

This exact decomposition concerns only the axial center z=0. For z !=0, d^2=(mu-z)^2+epsilon^2(1-mu^2) and the product formula changes. No sign of E_zz or E_z/z is inferred. In particular, gamma0=1 at mu endpoints means that expansions in powers of gamma around zero cannot be used uniformly on [0,1].

No numerical experiments performed; heavy PID 1581407 untouched; no modification to main, STATE or ledgers. Finite Lambda1 remains open.
