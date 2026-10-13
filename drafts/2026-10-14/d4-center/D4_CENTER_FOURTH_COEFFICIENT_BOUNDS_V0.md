# D4 centre fourth-order coefficients: rational bounds V0

DRAFT / NOT FROZEN / EXECUTION PROHIBITED / CHAT AUDIT REQUESTED.
METHOD_UNDETERMINED. This is new paper/symbolic work, not covered by the earlier
chat PASS for phase A. P1 normalization and regularity dependencies are retained.

## Result and interpretation

For every lambda in [119/200,33/50], the centre coefficients obey

\[
|E_{\rho\rho\rho\rho}(0,0;\lambda)|<23,
\qquad |E_{\rho\rho zz}(0,0;\lambda)|<18.
\]

These are uniform rational absolute upper bounds, the alternative expressly
allowed by the task. They are not evaluations of the signed coefficients and
do not claim their actual maxima are 23 or 18. The derivation integrates
analytic majorants of the phi-averaged K40/K22 kernels. No numerical parameter
scan or numerical quadrature is used.

Compared with 25600, the centre upper bounds are smaller by factors greater
than 1100 and 1400 respectively. Thus the centre coefficients are demonstrably
well below the proposed order-180 scale. Continue the analytic refinement route.
This does not establish a bound on the off-centre derivatives or select a final
D4 certification method.

## 1. Exact polynomial numerators

Use the audited phase-A T_j and set y=mu^2, c=1-lambda^2, q=1-cy. Define

\[
P_{40,j}(c,y)=q^4\langle[x^4]T_j\rangle_\phi,
\quad
P_{22,j}(c,y)=\lambda^2q^4\langle[x^2z^2]T_j\rangle_\phi.
\]

These are ordinary polynomials with rational coefficients. The exact kernels are

\[
K_{40}=-\frac{24}{q^4}\sum_{j=0}^3\gamma_0^{j+1}R^{(j)}P_{40,j},
\quad
K_{22}=-\frac4{\lambda^2q^4}\sum_{j=0}^3\gamma_0^{j+1}R^{(j)}P_{22,j}.
\]

The companion JSON contains every polynomial coefficient; key "a,b" means the
coefficient of c^a y^b. The script constructs them with exact Fraction arithmetic
from the homogeneous formulas, using <b^2>=(1-y)/2 and <b^4>=3(1-y)^2/8.
There is no floating-point substitution in this construction.

## 2. Uniform bounds on the angular function

At the centre,

\[
w^2q=\lambda^2+c^2y(1-y)\le(1+\lambda^2)^2/4,
\quad
1\ge\gamma_0\ge\frac{2\lambda}{1+\lambda^2}>\frac78.
\]

The last lower bound follows at lambda=119/200 and monotonicity for lambda<1.
For R=2 integral_0^1 [1+gamma+(1-gamma)s^2]^{-1} ds, differentiate under the
integral. Its denominator is at least 15/8. Since the integrals of
1,(1-s^2),(1-s^2)^2,(1-s^2)^3 are 1,2/3,8/15,16/35,

\[
(|R|,|R'|,|R''|,|R'''|)
\le\left(\frac{16}{15},\frac{256}{675},
\frac{32}{15}(\frac8{15})^3,
\frac{192}{35}(\frac8{15})^4\right)=:(r_0,r_1,r_2,r_3).
\]

Also gamma_0^(j+1)<=1, lambda^-2<=(200/119)^2, and q>=1-2y/3.

## 3. A polynomial absolute majorant that preserves cancellation

Let c_-=1-(33/50)^2, c_+=1-(119/200)^2, and write
c=c_-+(c_+-c_-)t. Convert each polynomial to the tensor Bernstein basis:

\[
P(c,y)=\sum_{h=0}^{m}\sum_{k=0}^{n} b_{hk}B_{h,m}(t)B_{k,n}(y).
\]

All b_hk are rational. If P(c(t),y)=sum a_ij t^i y^j, then

\[
b_{hk}=\sum_{i\le h,j\le k}
a_{ij}\frac{\binom hi}{\binom mi}\frac{\binom kj}{\binom nj}.
\]

By nonnegativity and partition of unity of the Bernstein basis,

\[
|P(c,y)|\le\sum_{k=0}^n v_kB_{k,n}(y),
\qquad v_k=\max_h|b_{hk}|.
\]

This is one global algebraic bound over the whole lambda band, with no adaptive
subdivision. The JSON stores every v_k. Taking absolute values after polynomial
cancellation and phi averaging is much sharper than the original directional
bound.

## 4. Exact rational integration bound

For n,k define

\[
I_{nk}=\int_{-1}^1\frac{B_{k,n}(\mu^2)}{(1-2\mu^2/3)^4}\,d\mu.
\]

The nonnegative binomial series gives

\[
I_{nk}=\binom nk\sum_{i=0}^{\infty}
\binom{i+3}{3}(2/3)^i\beta(i+k,n-k),
\]

where the rational quantity

\[
\beta(a,m)=\int_{-1}^1\mu^{2a}(1-\mu^2)^m\,d\mu
=\frac2{2a+1}\prod_{j=1}^{m}\frac{2j}{2a+2j+1}
\]

is positive. Termwise integration is justified by positivity (also uniform
convergence holds because 2mu^2/3<=2/3).

Take N=64 symbolically. The first N terms are exact rational numbers. For i>=N,
beta(i+k,n-k)<=beta(N+k,n-k), and successive binomial-series coefficients have
ratio at most r_N=(2/3)(N+4)/(N+1)<1. Therefore a rational upper bound U_nk is

\[
\binom nk\left[
\sum_{i=0}^{N-1}\binom{i+3}{3}(2/3)^i\beta(i+k,n-k)
+\frac{\binom{N+3}{3}(2/3)^N\beta(N+k,n-k)}{1-r_N}
\right].
\]

Thus the two final bounds are

\[
|E_{40}|\le24\sum_j r_j\sum_k v_{40,j,k}U_{n_jk}<23,
\]
\[
|E_{22}|\le4(200/119)^2\sum_j r_j\sum_k v_{22,j,k}U_{n_jk}<18.
\]

The exact fractions are in the JSON. Their decimal displays are approximately
22.89148 and 17.06422; only the exact rational comparisons to 23 and 18 are used.
N=64 is an algebraic series truncation index, not a spatial partition or a
parameter sampling count.

## 5. Verification performed and limits

Executed d4_center_rational_bounds.py with the Python standard library only.
The exact final comparisons to 23 and 18 passed. No SymPy installation or rerun
of the previously audited script was performed.

As an additional normalization check, specializing these polynomial kernels to
the sphere c=0 gives E40=-16/3, E22=-16/9, agreeing with the rotational fourth-order
tensor relation E40=3 E22. This does not replace an independent audit of the
new polynomial/majorant computation. The JSON is a symbolic calculation record,
not a D-P2 interval certificate or a producer/checker run receipt.

## 6. Consequence for the next step

If the same bounds held throughout the swept box, the full-box Taylor loss would be

\[
\frac{23}{384}+9(\frac{33}{1625})^2
=\frac{64497959}{1014000000}<0.064,
\]

well below the exact centre lower bound. This statement is explicitly hypothetical:
only centre coefficients have been bounded here. Centre values alone cannot be
used as M40/M22 in the remainder inequality.

The next analytic target is to bound the change in these derivatives between
(0,0) and the swept box, preserving phi averaging/cancellation. Possible paper
routes are a uniform off-centre kernel bound or rigorously bounded sixth-order
remainders. Neither has been proved here. Evenness alone supplies no quantitative
variation bound. No diagnostic value has been used to choose a spatial partition;
the existing 1/128 patch and outer ring remain unchanged.

Recommended next action: CONTINUE ANALYTIC OFF-CENTRE DERIVATIVE BOUNDS.
No machine certification is started; METHOD_UNDETERMINED remains in force.
