# Dig M3 audit response: retain exact T and correlated margin

2026-11-19. DIAGNOSTIC_ONLY / NOT_EVIDENCE.
Judge's review of M3: the uniform lower bound g(lambda) is algebraically correct but unsuitable as an L1 target. At lambda=5, V46 diagnostic values R2/S about 3 while g(5) about 0.589, so proving R2/S<g(lambda) would be false at these sample points.

## Corrected L1 target
Define T(lambda,S,z)=(pi/2)A_lambda(z)-(3S/2)B_lambda(z), with S=sqrt(1-z^2)>0 and A,B retained exactly as elementary functions.
The exact M1 identity is
H=(1/lambda)[-(pi S/2)A_lambda+(3S^2/2)B_lambda+R_H^(2)].
Therefore the *correlated margin*
Delta_H := T(lambda,S,z)-R_H^(2)/S = -lambda H/S
is an exact identity. Delta_H>0 is equivalent to H<0. No new sign estimate follows from this identity alone.

Do NOT use R_H^(2)/S<g(lambda) as the L1 target. It fails at known lambda=5 diagnostic points. Preserve the full z,S dependence of T and of R_H^(2), including correlations if they can be kept in the same integral or Taylor model.

## Two proposed evaluation tracks
A. Direct L1 on lambda*S>=K (if G1/G9 separately prove E_z>0 for lambda*S<=K), with exact T, and contact-collar treatment retaining t,phi,delta correlation.
B. Evaluate Delta_H directly using a shared expression; this is algebraically equivalent to -lambda H/S, so a naive re-expression is not progress. It is useful only if a common-numerator analytic decomposition or interval model demonstrably gives narrower bounds than separately bounding T and R2.

The G1 route is conditional: G1 presently covers lambda*S<=1 per Judge; extending K requires an independent proof and improvement of G9 north-term control.

## Quantitative constraints from Judge's V46 values (diagnostic only)
At lambda=5, center R2/S=3.023, T=3.145, margin=0.122; q=(0.3,0.4) R2/S=2.876, T=3.328, margin=0.452. These are non-rigorous guidance for target precision, not global bounds or evidence.

## Deliverables and governance
No finite Lambda1, no L1/L2 proof, no numerical pilot. Before any future numerical pilot freeze a plan and SHA-256, keep analytic derivation and numerical results separate. No modification to main/STATE/ledgers, no interference with heavy PID 1581407. Await chat audit.
