# D-PRO (C21): horizontal H representative pilot — mathematical analysis

**2026-11-18 / DIAGNOSTIC_ONLY / NOT_EVIDENCE**
Input pins: H v3 `d1ac5c652a6da43e245a399e4c9c2c5b5858d656`,
chat V36 `16d8c01b86327b8387f731bf09d1740c6ee31273`,
R3 `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`.

## Geometry

**Normalization:** In the original primitive E integral the physical
vertical coordinate is `p_z=lambda*z` while the co-rotated normalized
coordinate in R3 is `z=R sin(beta)`. Thus the primitive-E distance term
`(lambda*xi_z-p_z)^2` is `lambda^2*(xi_z-z)^2`, matching the R3
rational D² below. Earlier numerical references made with `p_z=z`
are invalid and preserved only in the separate ERRATUM record.

The laboratory coordinates are (p=(\rho,0,z)), (ξ=(ξ_x,ξ_y,ξ_z)in S^2),
(λge2). Define

[
 k=1-\rho\xi_x-z\xi_z,quad
 D^2=1+\rho^2+z^2-2\rho\xi_x-2z\xi_z
    +(\lambda^2-1)(\xi_z-z)^2,quad
 B=1-(1-\lambda^{-2})\xi_z^2,quad
 \gamma={k\over D\sqrt B}.
]

The sphere kernel is (f=kG(\gamma)), where
(G(\gamma)=\arccos^2\gamma) and
(ℛ(\gamma)=\arccos\gamma/\sqrt{1-\gamma^2}).
For a fixed ξ and fixed z, write (P=\xi_x-\rho).
Using (k_\rho=-\xi_x) and
(D_\rho=-P/D):

[
 \gamma_\rho={-\xi_x+kP/D^2\over D\sqrt B},
\qquad
 \gamma_{\rho\rho}={-2\xi_x P-k+3kP^2/D^2\over D^3\sqrt B}.
]

Since (G'=-2\mathcal R) and
(\mathcal R'=(\gamma\mathcal R-1)/(1-\gamma^2)), direct differentiation gives

[
 f_\rho=-\xi_x G-2k\mathcal R\gamma_\rho,
\quad
\boxed{f_{\rho\rho}=
4\xi_x\mathcal R\gamma_\rho-
2k\left(\mathcal R'\gamma_\rho^2+
\mathcal R\gamma_{\rho\rho}\right).}
]

This is a direct derivative of the primitive energy kernel and contains
**no z derivative**. The interval implementation uses the frozen R3
analytic Taylor enclosure for (G,\mathcal R,\mathcal R'), and performs
no finite-difference differentiation.

## Axis and center regularization

Reflection \(\rho\mapsto-\rho\) under \(\xi_x\mapsto-\xi_x\) shows
(E(\rho,z)) is even in \(\rho\). Hence (E_\rho(0,z)=0), and
for every \(\rho>0\),

[
 H(\rho,z)={E_\rho(\rho,z)\over \rho}
   =\int_0^1 E_{\rho\rho}(s\rho,z)\,ds.
]

The same formula defines the continuous limit at \(\rho=0\) and at
the center. The angular chart is kept aligned with the ORIGINAL
((R,\tau)) for every (s), while the physical point moves to
((s R\cos\beta,R\sin\beta)); z stays fixed.
For (R_{hi}<1), the rigorous distance bound (D\ge1-R_{hi}>0)
holds uniformly for all (sin[0,1]).

We use the pre-registered **four Simpson s panels**. For each panel
the signed angular integral of each of its three Simpson samples is
evaluated by the frozen R3 **fourth-order spatial Taylor quadrature**.
The outward Simpson error is bounded using
\(L^5\sup|f^{(4)}_s|/2880 = L^5\sup|j_{4,s}|/120\).
A zeroth-order angular range×area sum is used only for the
**nonnegative s remainder**. It is not used for any signed coefficient
or signed outer derivative integral. Each of the three outer
first derivatives is projected out of a mixed `(space=4,outer=1)`
R3 jet before signed angular quadrature. For its s remainder, the
`(s=4,outer=1)` jet coefficient is used.

## General boxes and boundary collar

For (ρ_{lo}>0), the direct (f_\rho/\rho) kernel is integrated
with signed fourth-order R3 spatial Taylor quadrature. Over any
parameter box, the point-center integral plus each integrated
first parameter derivative times the full corresponding box
halfwidth yields a rigorous first-order multivariate mean-value
enclosure. This is an enclosing (possibly loose) interval.

For (R_{hi}=1) (BD and STRIP_15), fix the contact cap
(q=1-\eta_x\le\kappa=1/4096). On its complement the R3
contact-chart integration and its outer derivatives use a single
fixed removed cap. For (0\le\gamma\le1) and (\lambda\le5):

[
 |\xi_x|\le1,quad 0\le G\le\pi^2/4,quad
 0\le\mathcal R\le\pi/2,quad
 |\gamma_\rho|\le(1+\lambda_{max})/D .
]

Here (0\le k=(\xi-p)\cdot\xi\le|\xi-p|\le D).
Thus

[
 \boxed{|f_\rho|\le \pi^2/4+
 \pi(1+\lambda_{max}).}
]

The normalized cap area is κ/2, so the single final correction is
the symmetric interval with radius at most

[
 {\kappa\over2\rho_{min}}
 \left({\pi^2\over4}+\pi(1+\lambda_{max})\right),\qquad
 \rho_{min}=R_{lo}{1-\tau_{hi}^2\over1+\tau_{hi}^2}>0.
]

Arb computes the outward upper endpoint of this expression.
No cap correction is used for boxes with (R_{hi}<1).

## W B4 auxiliary

W B4 uses fixed four R×τ outer children, unsplit λ, A<=1/4,
and per-child integrated B4<=0.03. The prior shared total depth cap
16 is replaced by a per-coordinate maximum of 16 bisections,
preserving fixed longest-normalized-edge splitting and the same
CW7 positive-denominator interval majorant. Coefficient cubature
is **not** launched if the B4 gate is incomplete.

## Limitations and required audit

- These are **representative boxes**, not an exhaustive partition.
- The V36 H box2 proof reasoning was audited separately; the new
  (f_{\rho\rho}\), Simpson s remainder implementation, and boundary
  cap estimate require separate independent checks before being used
  as proof components.
- Several coarse-mesh intervals may be too wide to determine a
  sign. **No sign is used to decide the method**, only recorded.
- A per-box timeout or failed inequality produces OPEN; no
  artificial certificate or partial-range substitution is allowed.
- Any time/box-count empirical model is illustrative. No global
  H-cover or W-tube box count follows without an adaptive cover.

**Condition (C21) global theorem: OPEN.**
