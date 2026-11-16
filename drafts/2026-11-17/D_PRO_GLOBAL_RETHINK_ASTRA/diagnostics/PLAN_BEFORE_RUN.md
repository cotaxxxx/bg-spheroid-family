# DIAGNOSTIC_ONLY / NOT_EVIDENCE

This plan is fixed before running the new research script. It does not modify any repository or previous FREEZE. Only Boolean answers are recorded; no margins, extrema or locations are recorded or used to choose certification partitions.

Parameters: lambda = [2, 206539/100000, 5/2, 3, 4, 118/25, 472438/100000, 472439/100000, 19/4, 5]; R = [1/8, 1/2, 15/16, 63/64, 255/256, 59999/60000, 1]; tau = [0, 1/16, 1/4, 1/2, 3/4, 15/16, 1]. cos(beta)=(1-tau^2)/(1+tau^2), sin(beta)=2tau/(1+tau^2). Endpoints R=1 are boundary diagnostics, not claims about boundary stationary points.

Integration: contact-centered coordinates on the reference unit sphere, u=tan(psi/4); panels [0,2^-12,2^-11,...,1], Gauss-Legendre with n=12 and n=24 on each panel, periodic midpoint with m=96 and m=192 respectively. Both rules are run with float64, not interval arithmetic.

Questions, interpreted ONLY on this fixed finite sample:

1. Is W=lambda^2 E_z/z-E_rho/rho positive? At equator use E_beta_beta/R^2; at pole use -E_beta_beta/R^2. For other angles use E_beta/(R^2 sin(beta)cos(beta)).
2. Is E_z positive on the positive axis at the listed R and lambda?
3. Is r E_rr-E_r strictly negative on the equator at the listed r=R and lambda? This tests whether F/r decreases with r^2.
4. Is E_zz positive on the positive axis at the listed R and lambda? This is a possible stronger axial route, not a required hypothesis of the angular route.
5. Does the co-rotating E_beta agree with -R sin(beta) E_rho+lambda R cos(beta) E_z to absolute tolerance 2e-5 at every non-endpoint angle for both rules?
6. At lambda=[2,7/2,5], R=[1/8,1/2,7/8], tau=[1/8,1/2,7/8], do centered finite differences of the directly evaluated energy agree with the analytic co-rotating first/second beta derivatives? Fixed step 1/1000, second-order central differences; tolerances 2e-5 and 2e-4 respectively. All 27 points, both rules.
7. Is the analytic centered coefficient lambda^2 E_zz(0)-E_xx(0) positive at every listed lambda, with both rules?

A false answer to a sign question is a failed finite-sample hypothesis, not a rigorous counterexample. A true answer is not a theorem. Any non-finite number makes the corresponding answer false. No producer/checker or certification is run.
