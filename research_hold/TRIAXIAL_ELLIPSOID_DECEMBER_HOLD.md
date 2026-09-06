# Volume-Preserving Triaxial Ellipsoid — December Hold Note

- status: DIAGNOSTIC_ONLY / NOT_BINDING / HOLD_UNTIL_DECEMBER
- purpose: December restart note only. Not theorem evidence, not manuscript evidence, not a certification contract.
- priority through November: C1b and D only.
- rule: no further triaxial design work before December. If any computation is run before then, limit it to a float 50x50 diagnostic scan only.

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

which is consistent with a nonzero transverse derivative. This number is diagnostic only and must not be cited as evidence.

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

## 6. Hold instruction

No additional triaxial derivation, contract design, certification architecture, or manuscript claim is authorized before December 2026. Through November, ChatGPT effort remains on C1b and D.

If idle compute capacity is intentionally used before December, the only permitted triaxial activity under this note is a nonbinding float 50x50 scan, subject to the sphere and S3 controls above. Its outputs remain local diagnostics and are not promoted, pinned, or cited.
