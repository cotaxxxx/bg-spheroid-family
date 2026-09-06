# Volume-Preserving Triaxial Ellipsoid — December Hold Note

- status: DIAGNOSTIC_ONLY / NOT_BINDING / HOLD_UNTIL_DECEMBER
- purpose: December restart note only. Not theorem evidence, not manuscript evidence, not a certification contract.
- priority through November: C1b and D only.
- rule: no further triaxial design work before December. If any computation is run before then, limit it to a float 50x50 diagnostic scan only.

## December restart — one-line anchor

回転楕円体族は 2 次元形状空間の対称部分族、その認証済み分岐点が校正アンカー、対称性を外すと中心 Hessian の退化条件が曲線群へ展開し停留円が離散点群へ分裂しうる。

The exploratory observations recorded below are retained only as local diagnostic support for this direction. They are NOT_BINDING and are not to be used as theorem evidence or manuscript claims.

## 1. Program position

Basepoint Geometry is the primary research program. The volume-preserving ellipsoid family is the first model family.

For the triaxial family, write

\[
abc=1,\qquad a=e^u,\quad b=e^v,\quad c=e^{-u-v}.
\]

Modulo the volume constraint, the shape space is two-dimensional. The three volume-preserving spheroid subfamilies \(a=b\), \(b=c\), \(c=a\) form three symmetry lines meeting at the sphere. The certified spheroid results are therefore calibration anchors for the later triaxial study rather than merely an earlier paper.

The triaxial paper should ask what happens after leaving these high-symmetry lines.

## 2. Local diagnostic observation near the prolate central bifurcation

The preceding exploratory computation is strictly local and nonbinding. It suggested that at the prolate central critical point \(a_c\), the spheroidal degeneracy

\[
Q_x=Q_y=0
\]

unfolds in the two-dimensional triaxial shape space into two symmetry-related degeneracy curves

\[
Q_x(u,v)=0,\qquad Q_y(u,v)=0.
\]

Under the exchange symmetry \(u\leftrightarrow v\), these curves should map to one another. If they meet transversely at the spheroidal point, the local picture is an X-crossing of codimension two.

A diagnostic finite-difference split previously observed was approximately

\[
\Delta Q\sim \pm 0.025\quad\text{for}\quad \Delta(u-v)\sim 0.02,
\]

which is consistent with a nonzero transverse derivative. This earlier rough number is superseded by the more symmetric local fit recorded in §6 below; all such numbers remain diagnostic only and must not be cited as evidence.

The four local sign chambers would then be

\[
(Q_x,Q_y)=(+,+),(+,-),(-,+),(-,-).
\]

The preliminary stationary-branch observations were consistent with the interpretation

- \((+,+)\): both principal-axis stationary pairs present,
- \((+,-)\) or \((-,+)\): one principal-axis stationary pair present,
- \((-,-)\): neither principal-axis stationary pair present.

Accordingly, the rotationally symmetric \(D_{\infty h}\) pitchfork in which a stationary circle contracts to the center is expected to unfold under \(D_{2h}\) symmetry into two successive \(\mathbb Z_2\) pitchforks. Along a generic path across the X-crossing, the noncentral stationary set may therefore change schematically as

\[
4\ \text{points}\;\longrightarrow\;2\ \text{points}\;\longrightarrow\;0.
\]

This is a conjectural outlook statement only. No diagnostic numerical value from this note is to appear in a theorem, abstract, main claim, certification appendix, or GitHub evidence registry.

## 3. December restart gates

Before any triaxial scan is interpreted, enforce all three controls below.

### Gate A — sphere control

At \(u=v=0\), require

\[
(Q_x,Q_y,Q_z)=(4/3,4/3,4/3).
\]

The three directions must agree. Failure indicates a normalization or integration error and stops the scan.

### Gate B — S3 symmetry

Exploit axis permutations. Compute only one fundamental chamber, for example

\[
a\ge b\ge c,
\]

and obtain the remainder by permutation/reflection. Symmetry violation is itself a diagnostic failure.

The certified spheroidal critical values should appear on the corresponding symmetry lines as consistency anchors. In particular, the later scan must check compatibility with the certified/controlled spheroidal values associated with

\[
a_c,\qquad \lambda_{\rm axis}^{ob},\qquad \lambda_{\partial}^{ob},\qquad \lambda_{\partial}^{pro},
\]

using their exact upstream scopes and certified brackets at the time of restart.

### Gate C — boundary-entry curves

The first approximation to the triaxial bifurcation set must include both kinds of loci:

\[
Q_x=0,\quad Q_y=0,\quad Q_z=0,
\]

and the curves on which the corresponding noncentral stationary pairs enter or leave through the boundary.

The Hessian-degeneracy curves alone are not to be called the full bifurcation set.

## 4. Provisional geometric target

The long-term object is the shape-space bifurcation/discriminant set

\[
\mathcal D=\{(u,v): E_{K_{u,v}}\text{ has a degenerate stationary point}\},
\]

augmented, for the practical stationary-set census, by the boundary-entry loci.

The certified spheroid paper should serve as a calibration anchor: its one-dimensional symmetry lines provide fixed intersections and consistency tests for the two-dimensional triaxial exploration.

## 5. Labels to preserve from the spheroid paper

To make the later comparison intrinsic, each stationary component in the spheroid manuscript should, where defined, carry the label

\[
(\dim,\operatorname{index},\operatorname{nullity},G_p).
\]

The triaxial paper should compare changes in these labels under symmetry breaking, not merely positions or raw point counts.

## 6. Diagnostic shape-space update — 2026-09-06

All statements and numerical values in this section are exploratory double-precision diagnostics only.

A full-plane diagnostic scan in logarithmic shape coordinates

\[
p=\frac{u_1-u_2}{\sqrt2},\qquad q=\sqrt{\frac32}\,u_3,\qquad \sum_i u_i=0,
\]

with sixfold completion by permutation of axes, gave the following provisional picture.

### 6.1 Center-Hessian zero set

The three zero sets

\[
Q_1=0,\qquad Q_2=0,\qquad Q_3=0
\]

form a sixfold-symmetric curved triangular boundary around the sphere. The sphere lies in the interior index-0 chamber and reproduces

\[
Q_1=Q_2=Q_3=4/3
\]

at double precision.

The spheroidal calibration points are recovered on symmetry axes:

- the oblate center-degeneracy point \(a_z\) appears as a corank-1 regular point of one zero curve;
- the prolate critical point \(a_c\) appears as a corank-2 intersection of two zero curves.

Thus the one-dimensional spheroid zeros acquire different geometric meanings in the two-dimensional shape space: edge-midpoint type versus vertex/intersection type.

### 6.2 Symmetry and degeneracy rank

The diagnostic picture suggests the structural correspondence

\[
\text{continuous rotational symmetry at }a_c
\longleftrightarrow
\text{corank-2 intersection},
\]

whereas the oblate axial degeneracy is corank 1. In this sense, the type of symmetry is reflected in the rank of the center-Hessian degeneracy and in the local geometry of the discriminant curves.

### 6.3 Curved index-0 chamber

The index-0 chamber is larger than the straight triangle joining the prolate vertices. Its edges bow outward. This is only a geometric diagnostic at present; no convexity, monotonicity, or general "symmetry stabilization" claim is certified.

A useful interpretation to test later is that along the rotationally symmetric oblate line the center remains nondegenerate farther, at comparable logarithmic shape distance, than for nearby triaxial perturbations.

### 6.4 Local splitting of the stationary circle

Inside the local index-0 wedge near the prolate vertex, the stationary circle observed on the rotationally symmetric spheroid splits under triaxial perturbation into exactly two principal-axis \(\mathbb Z_2\) pairs in the numerical search:

\[
S^1\rightsquigarrow \{\pm p_x\}\cup\{\pm p_y\}.
\]

No off-axis stationary points were detected in the sampled equatorial neighborhood. The tangential derivative along the former circle had a single-sign pattern between symmetry axes, consistent with the absence of additional local off-axis branches.

The two pairs are not equivalent after symmetry breaking: one pair is tangentially minimum-like along the former circle and the other maximum-like, so the previously uniform \(S^1\)-orbit acquires an ordering under triaxial perturbation.

Along a generic path the observed local sequence is consistent with

\[
4\to2\to0
\]

as the two corank-1 curves are crossed successively.

### 6.5 Corrected local linear split

Using the exchange-antisymmetric perturbation parameter \(\delta\) for the two equatorial axes, symmetry requires the first-order split of the two transverse center-Hessian coefficients to have opposite signs. The diagnostic fit gives

\[
Q_1-Q_*\sim +c\,\delta,\qquad
Q_2-Q_*\sim -c\,\delta,
\]

with

\[
c\approx1.235.
\]

The shared quadratic coefficient in the same local fit is approximately \(-1.2\). These values supersede the earlier rough unequal finite-difference estimates and remain strictly nonbinding.

The local zero curves intersect at an angle of approximately \(83^\circ\) in the chosen diagnostic coordinates, consistent with a transverse unfolding.

### 6.6 Conceptual observation to retain for December

The present lens suggests the following hierarchy:

\[
\text{point description}
\to
\text{stationary orbit description}
\to
\text{ordered discrete orbit description under symmetry breaking}.
\]

Equivalently: a stationary orbit hidden by a point-only description becomes visible on the spheroid, and after breaking rotational symmetry the formerly uniform orbit acquires an internal ordering. This is a useful structural question for the future triaxial paper, but not a present theorem claim.

The current curved-triangle picture is also lens-dependent. A later, separate question is how the corresponding discriminant geometry changes when the basepoint functional itself is replaced. No such comparison is authorized before the current spheroid program is closed.

## 7. Hold instruction

No additional triaxial derivation, contract design, certification architecture, or manuscript claim is authorized before December 2026. Through November, ChatGPT effort remains on C1b and D.

If idle compute capacity is intentionally used before December, the only permitted triaxial activity under this note is a nonbinding float 50x50 scan, subject to the sphere and S3 controls above. Its outputs remain local diagnostics and are not promoted, pinned, or cited.
