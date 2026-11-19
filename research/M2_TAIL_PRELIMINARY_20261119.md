# Dig M2 — preliminary mathematical obstruction and work plan (2026-11-19)

Status: DIAGNOSTIC_ONLY / NOT_EVIDENCE. No claim of T1, T2, or finite Lambda1.

## 1. Geometric limitation of a fixed compact core

Let q=(rho,z), S=sqrt(1-z^2), S0=2^-12 and K_m={|q|<=1-m, S>=S0}, 0<m<1. At fixed z the outermost available core point has
rho_m(z)=sqrt((1-m)^2-z^2)
provided |z|<=1-m. For |z|>1-m there is **no** point on the same horizontal line in K_m. Consequently a single fixed m cannot transfer the H sign from K_m to the entire contact collar using NP10, including points near the polar cutoff S=S0, unless m is chosen so small that 1-m>=sqrt(1-S0^2). This requires
m<=1-sqrt(1-S0^2)=S0^2/(1+sqrt(1-S0^2)),
approximately 2^-25. This geometric restriction must be accounted for before choosing m.

For |z|<=1-m and rho>rho_m(z), NP10 gives
rho H(rho,z)<=rho_m H(rho_m,z)+(2 T_lambda(z)/lambda)(rho-rho_m).
If H(rho_m,z)<=-h_m(z)<0, the sufficient condition for H(rho,z)<0 is
rho-rho_m < lambda rho_m h_m(z)/(2 T_lambda(z)).
In particular, covering the full horizontal collar up to rho=S requires
S-rho_m < lambda rho_m h_m(z)/(2 T_lambda(z)).
The right side collapses if rho_m->0 unless h_m compensates. Hence uniform infimum h* alone may be inefficient; z-dependent margins and multiscale collars may be necessary.

## 2. Tail logarithm and remainder: required lemma, not yet established

With epsilon=1/lambda (normalization to be rechecked against M1 original), write
H/epsilon= -(pi S/2) A_lambda(z)+(3 S^2/2) B_lambda(z)+R_H^(2),
A_lambda=asinh((1-z)/epsilon)+asinh((1+z)/epsilon),
B_lambda=atan((1-z)/epsilon)+atan((1+z)/epsilon).
To prove T1 one needs an explicit upper bound for R_H^(2) uniform in q and epsilon, strong enough to beat the negative logarithmic term. The pointwise O(|t|^-3) statement on a fixed interior point does not supply such a uniform constant near contact. No finite Lambda1 follows from the supplied estimates alone.

## 3. Axis target

For z !=0, seek a lower bound on lambda E_z/[z(1+log lambda)] uniform for S>=S0 and continuous at z=0. The asymptotic limit 3 pi S is not itself a uniform lower bound. A common-numerator representation of the odd difference quotient is required; do not evaluate I(mu,z) and I(mu,-z) independently and subtract intervals.

## 4. Frozen pilot plan M2-P0 (not executed)

No numerical probe is authorized in this note. First obtain exact M1 kernel, normalization, and V45 NP10 from pinned source; derive symbolic bounds and choose all numerical domains and precision before any run. If a probe is later run, record plan identifier, CPU affinity, low scheduling priority, process PID, stdout/stderr, hashes, and check that the existing heavy PID 1581407 is untouched.

## 5. C21 cost

At the reported rate 16 days per unit lambda width, the naive cost of [5,Lambda1] is 16(Lambda1-5) days. This is a conditional planning estimate, not a benchmark.

## 6. Open decisions

Recommendation: prioritize an explicit uniform remainder lemma and a multiscale collar adapted to z before optimizing Lambda1. If this fails, report the exact missing inequality and constants rather than choosing an unsupported threshold.

No existing STATE, ledger, or main files modified.
