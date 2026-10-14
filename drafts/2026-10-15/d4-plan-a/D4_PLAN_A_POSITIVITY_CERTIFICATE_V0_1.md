# D4 Plan A — positivity certificate / D-P2 handoff V0.1

**Date:** 2026-10-15 JST  
**Issuer:** Judge  
**Object:** D4 / \(B_{003}\)  
**Status:** CANONICAL DRAFT V0.1 / METHOD_SELECTED / positivity PASS (conditional) / NOT CLOSED / NOT CERTIFIED

---

## 0. Executive certificate

For

\[
B_{003}
=
\left\{
(r,\tau,\lambda):
0\le r\le\frac18,\ 
0\le\tau\le\frac18,\ 
\frac{119}{200}\le\lambda\le\frac{33}{50}
\right\},
\]

with

\[
\rho
=
r\frac{1-\tau^2}{1+\tau^2},
\qquad
z
=
\lambda r\frac{2\tau}{1+\tau^2},
\]

define, for \(\rho>0\),

\[
H(\rho,z;\lambda)
=
\frac{E_\rho(\rho,z;\lambda)}{\rho},
\]

and extend regularly to the axis by

\[
H(0,z;\lambda)=E_{\rho\rho}(0,z;\lambda).
\]

This is the unique continuous extension supplied by Lemma 6.1(iii), as confirmed in L2, under the P1 normalization.

Conditional on the P1 normalization and Lemma V bundle, the audited signed fourth-order bounds imply

\[
\boxed{
H(\rho,z;\lambda)>0
}
\]

throughout the closed \(B_{003}\) swept region.

Hence for every point of \(B_{003}\) with \(r>0\),

\[
\rho>0
\quad\Longrightarrow\quad
E_\rho(\rho,z;\lambda)
=
\rho H(\rho,z;\lambda)>0,
\]

so no noncentral stationary point occurs in \(B_{003}\).

At \(r=0\), one has \((\rho,z)=(0,0)\). The symmetry-forced central stationary point is retained; positivity of the regular extension \(H(0,0;\lambda)\) does not remove it.

Therefore:

\[
\boxed{\text{D4 Plan A: METHOD\_SELECTED}}
\]

and

\[
\boxed{\text{D4 positivity inequality: PASS (conditional)}}
\]

while

\[
\boxed{\text{D4 CLOSED / CERTIFIED is not declared here.}}
\]

---

## 1. Fixed swept region

The coordinate map satisfies

\[
\rho^2+\left(\frac z\lambda\right)^2=r^2.
\]

Therefore \(B_{003}\) is contained in the fixed swept ellipsoid

\[
\boxed{
\lambda\in\left[\frac{119}{200},\frac{33}{50}\right],
\qquad
\rho^2+\left(\frac z\lambda\right)^2\le\frac1{64}.
}
\]

No result-driven shrinking of this physical region is used.

For the final \(B_{003}\) Taylor estimate,

\[
0\le \rho\le\frac18.
\]

Also, since \(0\le\tau\le1/8\),

\[
\frac{2\tau}{1+\tau^2}
\le
\frac{16}{65},
\]

and hence

\[
0\le z
\le
\frac{33}{50}\cdot\frac18\cdot\frac{16}{65}
=
\boxed{\frac{33}{1625}}.
\]

The \(M_{22}^{-}\) certificate is stronger than required: it covers the full signed axis interval

\[
|z|\le\frac{\lambda}{8}.
\]

---

## 2. Center lower bound

The audited conservative center bound is

\[
\boxed{
E_{\rho\rho}(0,0;\lambda)
\ge
m_*
:=
\frac{1547}{4860}
}
\]

uniformly for

\[
\lambda\in\left[\frac{119}{200},\frac{33}{50}\right].
\]

This is the only center lower bound required for the present certificate.

Any later \(K_{20}\)-Bernstein strengthening of \(m_*\) is non-blocking insurance and is not used here.

---

## 3. Signed \(M_{40}^{-}\) bound — primary full-kernel route

The primary certificate uses the audited full-kernel signed fourth-directional representation, not the finite/tail bridge.

Let

\[
I_*=
\frac{193787991018310321}
{47793375000000000}.
\]

The full-kernel Bernstein certificate gives the pointwise signed kernel bound

\[
\boxed{\mathcal K_{40}\le24}
\]

on the fixed relaxed domain covering the swept region.

After the positive geometric weight is integrated,

\[
\boxed{
-E_{\rho\rho\rho\rho}(\rho,z;\lambda)
\le
24I_*
=
C
}
\]

with

\[
\boxed{
C=
\frac{193787991018310321}
{1991390625000000}
<100.
}
\]

Thus the stronger direct full-kernel result is

\[
\boxed{
E_{\rho\rho\rho\rho}(\rho,z;\lambda)\ge-C.
}
\]

The previously adopted contract constant

\[
\boxed{
M_{40}^{-}
=
C+2\times10^{-8}
=
\frac{387575982116276267}
{3982781250000000}
<100
}
\]

remains valid automatically, since it is slightly larger than the directly proved full-kernel bound.

### Reference-only finite bridge

The earlier finite bridge uses a tail premise

\[
\varepsilon_{40}<10^{-8}.
\]

Its corrected \(J_{\rm low}\) evaluation uses

\[
c_{\min}=\frac{1411}{2500}.
\]

That route is retained only as a consistency/reference route. It is **not** needed for the primary D4 certificate, so the tail premise is not a logical condition of the main proof.

---

## 4. Signed \(M_{22}^{-}\) bound on the axis

On the axis,

\[
E_{\rho\rho}(0,z;\lambda)
=
\int_{-1}^{1}K_{20}(z,\lambda,\mu)\,d\mu.
\]

The audited common-integral representation is

\[
K_{20}
=
\frac1\lambda
\int_0^1
\left(
\frac P\Omega+\frac Q{\Omega^2}
\right)dt,
\]

with

\[
\Omega=(1+t^2)wd+(1-t^2)h_0>0.
\]

The signed mixed derivative has the exact representation

\[
-\partial_z^2K_{20}
=
\frac1\lambda
\int_0^1
\frac{\mathcal N_{22}}{\Omega^4}\,dt.
\]

The independently audited \(\phi\)-averaged mixed full kernel satisfies

\[
\frac{\mathcal N_{22}}{\Omega^4}
=
\frac{w}{2d^3}\mathcal K_{22},
\]

with exact Bernstein certificate

\[
\boxed{
\mathcal K_{22}\le48.
}
\]

The certificate used a fixed \(4\times4\times4=64\) auxiliary partition, with \(405\) Bernstein coefficients per box:

\[
64\times405=25920.
\]

All coefficients were positive in the positivity polynomial certificate, with

\[
\boxed{
\min b=\frac{139515}{1792}>0,
\qquad
\max b=\frac{744477}{512}.
}
\]

The positive geometric weight obeys the same audited bound \(I_*\), hence

\[
\boxed{
-E_{\rho\rho zz}(0,z;\lambda)
\le
48I_*
=
\frac{193787991018310321}
{995695312500000}
<200.
}
\]

Therefore

\[
\boxed{
M_{22}^{-}
=
\frac{193787991018310321}
{995695312500000}
}
\]

and

\[
\boxed{M_{22}^{-}\le200:\ \mathrm{PASS}.}
\]

There is no \(\phi\)-series truncation in this route:

\[
\boxed{\varepsilon_{22}=0.}
\]

The exact slack is

\[
200-M_{22}^{-}
=
\frac{5351071481689679}
{995695312500000}
>0.
\]

The certificate holds on

\[
|z|\le\frac{\lambda}{8},
\]

which strictly contains the axis segment needed by \(B_{003}\).

---

## 5. Three-stage FTC

The proof of positivity uses only the two signed derivative bounds and the center lower bound.

### Stage 1 — radial quotient as an average

For \(\rho>0\), the \(\rho\mapsto-\rho\) evenness of \(E\) gives
\(E_\rho(0,z;\lambda)=0\). This evenness is the one furnished by the P1 paired representation; equivalently, it relies on the reflection identity
\[
F(-\rho,-b)=F(\rho,b)
\]
recorded in L2 draft `9eb8ddee`. The fundamental theorem of calculus then gives

\[
E_\rho(\rho,z;\lambda)
=
\int_0^\rho
E_{\rho\rho}(s,z;\lambda)\,ds.
\]

Therefore

\[
\boxed{
H(\rho,z;\lambda)
=
\int_0^1
E_{\rho\rho}(t\rho,z;\lambda)\,dt.
}
\]

This formula also gives the regular extension at \(\rho=0\).

### Stage 2 — off-axis radial loss

By the same \(\rho\mapsto-\rho\) evenness (P1 paired representation; L2 draft `9eb8ddee` reflection identity
\(F(-\rho,-b)=F(\rho,b)\)),

\[
E_{\rho\rho\rho}(0,z;\lambda)=0.
\]

Hence, for \(x\ge0\),

\[
E_{\rho\rho}(x,z;\lambda)
=
E_{\rho\rho}(0,z;\lambda)
+
\int_0^x
(x-s)
E_{\rho\rho\rho\rho}(s,z;\lambda)\,ds.
\]

Using

\[
E_{\rho\rho\rho\rho}\ge-M_{40}^{-},
\]

we get

\[
E_{\rho\rho}(x,z;\lambda)
\ge
E_{\rho\rho}(0,z;\lambda)
-
\frac{M_{40}^{-}}2x^2.
\]

Substituting \(x=t\rho\) and integrating \(t\in[0,1]\),

\[
\boxed{
H(\rho,z;\lambda)
\ge
E_{\rho\rho}(0,z;\lambda)
-
\frac{M_{40}^{-}}6\rho^2.
}
\]

### Stage 3 — axial loss from the center

Reflection symmetry in \(z\) gives

\[
E_{\rho\rho z}(0,0;\lambda)=0.
\]

Thus

\[
E_{\rho\rho}(0,z;\lambda)
=
E_{\rho\rho}(0,0;\lambda)
+
\int_0^z
(z-s)
E_{\rho\rho zz}(0,s;\lambda)\,ds.
\]

Using

\[
E_{\rho\rho zz}(0,s;\lambda)\ge-M_{22}^{-},
\]

we obtain

\[
\boxed{
E_{\rho\rho}(0,z;\lambda)
\ge
m_*
-
\frac{M_{22}^{-}}2z^2.
}
\]

Combining the three stages,

\[
\boxed{
H(\rho,z;\lambda)
\ge
m_*
-
\frac{M_{40}^{-}}6\rho^2
-
\frac{M_{22}^{-}}2z^2.
}
\]

---

## 6. Exact \(B_{003}\) positivity margin

On \(B_{003}\),

\[
\rho^2\le\frac1{64},
\qquad
z^2\le
\left(\frac{33}{1625}\right)^2.
\]

Therefore

\[
H(\rho,z;\lambda)
\ge
\frac{1547}{4860}
-
\frac{M_{40}^{-}}{384}
-
\frac{M_{22}^{-}}2
\left(\frac{33}{1625}\right)^2.
\]

Using the adopted contract value

\[
M_{40}^{-}
=
\frac{387575982116276267}
{3982781250000000}
\]

and the signed mixed certificate

\[
M_{22}^{-}
=
\frac{193787991018310321}
{995695312500000},
\]

the exact margin is

\[
\boxed{
\frac{900009544615558979777197}
{36346861687500000000000000}
>0.
}
\]

Numerically,

\[
\approx0.0247616851.
\]

Hence

\[
\boxed{
H(\rho,z;\lambda)>0
\quad\text{on the whole closed }B_{003}\text{ swept region}.
}
\]

For comparison, even replacing \(M_{22}^{-}\) by the contractual target \(200\) gives

\[
\boxed{
\frac{55022792357943797893}
{2326199148000000000000}
>0.
}
\]

---

## 7. \(r=0\) and the central stationary point

At

\[
r=0,
\]

the coordinate map gives

\[
(\rho,z)=(0,0).
\]

The energy has the symmetry-forced central stationary point there.

The present certificate proves

\[
H(0,0;\lambda)
=
E_{\rho\rho}(0,0;\lambda)
\ge
\frac{1547}{4860}>0,
\]

which states positive radial curvature of the regular extension. It does **not** assert that the center ceases to be stationary.

For every \(r>0\) in \(B_{003}\),

\[
0\le\tau\le\frac18<1
\]

implies

\[
\rho
=
r\frac{1-\tau^2}{1+\tau^2}>0.
\]

Since \(H>0\),

\[
E_\rho=\rho H>0,
\]

so no point with \(r>0\) can be stationary.

Thus the only stationary point retained by this local certificate is the symmetry-forced center at \(r=0\).

---

## 8. Audit and provenance record

The mathematical content used here is the combination of two independently audited signed certificates.

The independent chat audit package is:

`d4_chat_audit_records_20261015.zip`

with SHA-256

`da0238890bc3366b2bbe90ec216b9f93c9f678eb6777fc930c8a48b57baa3f3e`.

Its `pkg/d4_chat_audit_SHA256SUMS.txt` records the audit-script and rerun-log hashes used below.

### \(M_{40}^{-}\)

Primary full-kernel route:

- Legendre derivative identity \(k=1,\dots,4\)
- fourth-directional composite kernel
- rationalization
- fixed Bernstein certificate
- \(256\) boxes
- exact positive minimum coefficient
- corrected geometric-weight evaluation with
  \[
  c_{\min}=\frac{1411}{2500}
  \]

Independent chat audit records:

- `pkg/d4_chat_audit_M40_identities_and_weight.py`
  SHA-256 `6b2add92a26c39a4f449820c67b868efce098b98b4e99dd428f8aa1c90b109a5`
- `pkg/d4_chat_audit_M40_bernstein_256.py`
  SHA-256 `50a16b3dcf6a2b1f6fbdc61c0d7276b695d5462c55e9b15b54a7477996a58d91`

These are the records previously denoted audit7 / audit8.

The finite/tail bridge is reference-only in this certificate.

### \(M_{22}^{-}\)

- independent mixed-kernel construction
- \(z=0\) specialization to the existing V0 \(E_{22}\) kernel
- exact agreement with \(P_{22,j}\), \(j=0,1,2,3\)
- fixed \(64\)-box Bernstein certificate
- sphere control
  \[
  E_{22}(\lambda=1)=-\frac{16}{9}
  \]
- exact rational weight and Taylor-margin checks

Independent chat audit records:

- `pkg/d4_chat_audit_M22_kernel_bernstein_64.py`
  SHA-256 `b5d4b1570a79d466c0104c233dc00055ca0a4e33435b3e4f05069ebeb2314d71`
- `pkg/d4_chat_audit_M22_rationalization.py`
  SHA-256 `ea3e714ea6370eb7d402c0faac7af0afd5d4d4b93d43f26c8f8c291c6884ea60`
- `pkg/d4_chat_audit_rerun_20261015.log`
  SHA-256 `a6a234a01a8f80e7038a8f6f8a94e150d1d578ce591559da42ba2fbb991c6b6c`

These correspond to audit9 / audit10 plus the combined rerun log.

**M22 rerun-log note.** The first line reported by
`d4_chat_audit_M22_kernel_bernstein_64.py`,
`K22 rational form matches audited composite: False`,
is a procedural false caused by omitting the explicit substitution
\[
b=\sqrt{1-\zeta^2}=\frac{2r}{1+r^2}
\]
in that first comparison. The authoritative rational-form check is
`d4_chat_audit_M22_rationalization.py`, which returns `match: True`.
The Bernstein certificate, exact rational bound, Taylor margin, and sphere control in
`d4_chat_audit_M22_kernel_bernstein_64.py` are independently PASS and remain valid.

The submitted V0 certificate reports

\[
\boxed{
M_{22}^{-}
=
\frac{193787991018310321}
{995695312500000}
<200
}
\]

with no \(\phi\)-tail.

---

## 9. Conditions and scope

This certificate is conditional on:

\[
\boxed{\text{P1 normalization}}
\]

and

\[
\boxed{\text{Lemma V bundle}.}
\]

These remain external audit items.

The primary \(M_{40}^{-}\) proof in this certificate is the direct full-kernel route. Therefore the finite-bridge premise

\[
\varepsilon_{40}<10^{-8}
\]

is **not** a condition of the main certificate.

If the finite bridge is cited as an alternative derivation, its tail premise and the status of its complex-disk constants must be stated explicitly.

---

## 10. D-P2 handoff statement

The handoff fact supplied by D4 is:

> For every
> \[
> (r,\tau,\lambda)\in B_{003}
> \]
> with \(r>0\), conditional on P1 normalization and the Lemma V bundle,
> \[
> H(\rho,z;\lambda)>0
> \]
> and hence
> \[
> E_\rho(\rho,z;\lambda)>0.
> \]
> Therefore no noncentral stationary point occurs in \(B_{003}\).  
> At \(r=0\), the symmetry-forced center remains and is handled separately.

This is the exact local exclusion fact to be consumed by the D-P2/global-cover layer.

No theorem-level closure is asserted by this handoff alone.

---

## 11. Status after this certificate

\[
\boxed{M_{40}^{-}\le100:\ \mathrm{PASS}}
\]

\[
\boxed{M_{22}^{-}\le200:\ \mathrm{PASS}}
\]

\[
\boxed{\text{D4 positivity inequality: PASS (conditional)}}
\]

\[
\boxed{\text{D4 Plan A: METHOD\_SELECTED}}
\]

\[
\boxed{\text{sixth-order: HOLD / NOT SELECTED}}
\]

\[
\boxed{\text{D4 CLOSED / CERTIFIED: NOT DECLARED}}
\]

Remaining external conditions / process items:

- P1 normalization audit
- Lemma V bundle audit
- certificate packaging / provenance freeze
- D-P2 handoff acceptance
- final Judge discharge

---

## 12. Packaging record

The provenance package is recorded on:

`candidate/d4-offcentre-phiavg-20261014`

with the non-rewritten two-commit topology

\[
oxed{
	exttt{ec8d243f84b922f95f60d1e4a28193d2a30181b2}

\rightarrow
	exttt{990df66cbd5d4ff8c90c1b1e1cc315fccb40208e}

\rightarrow
	ext{provenance child commit}
}
\]

The first child contains this certificate V0.1 alone. The second child packages:

- Astra `D4_M40_SIGNED_CERTIFICATE_V0_1.md`
- Codex `D4_M22_SIGNED_CERTIFICATE_V0.md`
- `d4_chat_audit_records_20261015.zip`
- this certificate with the exact §8 audit filenames and SHA-256 values

No history rewrite is used. This replaces the earlier planning phrase “ec8d243f direct child / one commit” with the actual `ec8d243f` lineage / two-commit provenance record.
