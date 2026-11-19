# M2 axis divided difference and compact-to-collar obstruction (third note)

2026-11-19. DIAGNOSTIC_ONLY / NOT_EVIDENCE.

## Sources and scope
Read original M1 files on branch research/d-pro-tail-axis-dig-math-probe-20261119:
runs/2026-11-19/D_PRO_TAIL_AXIS_DIG_M1/MATH_DERIVATION_BEFORE_PROBE.md
and MATH_ADDENDUM_POST_PROBE.md.
Original M1 explicitly sets epsilon=lambda^-1, q=(rho,z), S=sqrt(1-z^2).
No full T1/T2 proof is claimed.

## 1. Exact integral formula for the axis odd divided difference
Original M1 defines, for rho=0,
I(mu,z;epsilon)=mu(F(gamma)+gamma F'(gamma))-k gamma F'(gamma)(mu-z)/d^2,
k=1-z mu, d^2=(mu-z)^2+epsilon^2(1-mu^2),
B=1-(1-epsilon^2)mu^2, gamma=epsilon k/(d sqrt(B)).
The audited reflection formula is
E_z(0,z)/z=(1/2) integral_0^1 [I(mu,z)-I(mu,-z)]/z dmu.

For fixed epsilon>0 and |z|<1, if I is differentiable along the segment [-z,z], the fundamental theorem of calculus gives the exact common-numerator identity
[I(mu,z)-I(mu,-z)]/z = integral_{-1}^1 (partial_z I)(mu,u z;epsilon) du.
Therefore
E_z(0,z)/z=(1/2) integral_0^1 integral_{-1}^1 (partial_z I)(mu,u z;epsilon) du dmu.
At z=0 this yields integral_0^1 (partial_z I)(mu,0;epsilon) dmu, consistent with M1. This removes explicit division by z and is a mathematically valid interval-enclosure target. It does not assert the integrand is nonnegative; sign-preserving factorization of partial_z I is still needed.

Caution: at mu=1 and z=1 the expression requires endpoint interpretation, but the target has S>=S0>0 and hence |z|<=sqrt(1-S0^2)<1. For epsilon>0 the denominators remain positive on this compact z range (mu=1 has d^2=(1-z)^2>0).

## 2. Refined geometric core obstruction
Let Z0=sqrt(1-S0^2). A horizontal reference on the fixed-radius core |q|<=1-m at height z exists iff |z|<=1-m. Therefore to include all target heights |z|<=Z0 one must choose m<=1-Z0, exactly
m<=S0^2/(1+Z0).
At equality the core reference at |z|=Z0 is rho'=0; NP10 then supplies no negative anchor of the form -rho' h*. Strict positivity of the transfer margin requires m<1-Z0 and rho'>0, or a separate near-axis mechanism.

## 3. Stronger remainder target
With original exact two-term M1 identity and S>=S0,
H/epsilon <= -pi S log(lambda) -(pi S/2)log(4S^2)+(3pi S^2/2)+R_H^(2).
If a proved uniform bound R_H^(2)<=C_S S with C_S>=0 exists, then
H<0 whenever lambda>exp(3/2+C_S/pi)/(2 S0).
This threshold is **conditional**, not a derived numerical Lambda1.

## 4. Why the axis integral alone does not close T2
The double-integral identity is cancellation-safe in z but partial_z I can change sign in mu. A uniform lower bound on its full integral is required. Pointwise interior asymptotics and finite-epsilon numerical samples are insufficient. One possible next algebraic step is to differentiate I symbolically while preserving k,d^2,B,gamma as shared symbols, and group the result before any interval extension.

## 5. Computation and governance
This note is analytic only. No numerical pilot executed. Heavy PID 1581407 untouched. No change to main, STATE, or ledgers. Independent audit pending.
