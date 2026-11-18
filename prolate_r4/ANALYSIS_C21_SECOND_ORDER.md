# ANALYSIS — second-order outer enclosure for C21 H
2026-11-18 — **DIAGNOSTIC_ONLY / NOT_EVIDENCE**
Pinned original C21 5004ebdc6e038bcdb3122f563ffb15d38070d8b6,
V38 922a2c7eaed62b6c40d1bf9b0e956f98a85fd104.

## 1. Rigorous exterior Taylor remainder

Let `F(P)` denote the angular integral to be enclosed,
where `P` has three outer parameters, and let
`B=∏[p_i-h_i,p_i+h_i]` be an axis-parallel box. For
`P=p+s` with `|s_i|≤h_i`, define `g(t)=F(p+ts)`.
Provided `F` is twice continuously differentiable on
a neighborhood of `B`, the one-variable Taylor formula gives

`F(P)=F(p)+Σ_i F_i(p)s_i+∫_0^1(1-t) Σ_ij F_ij(p+ts) s_i s_j dt.`

Since each Hessian coefficient is in the interval
`[F_ij](B)`, the full interval enclosure is

`[F](B) ⊂ [F](p) + Σ_i [F_i](p)*[-h_i,h_i] + 1/2 Σ_i [F_ii](B)*[0,h_i²] + Σ_{i<j} [F_ij](B)*[-h_i h_j,h_i h_j]`.

Diagonal factors are NONNEGATIVE, and mixed terms have no
extra factor 1/2 after symmetry. The full-box Hessian
enclosures are generally wide but are multiplied by h².

## 2. Signed angular coefficient integration

Integrate each spatial Taylor coefficient SIGNED, with
the pinned R3 `quadrature.integrate` on `u,v` cells:
point `H(p)` uses active `(spatial)`;
point gradient `F_i(p)` uses active
`(spatial, i)` with orders `(n,1)`;
full-box diagonal Hessian `F_ii(B)` uses
`(spatial,i)` orders `(n,2)` times 2!;
full-box mixed Hessian uses
`(spatial,i,j)` orders `(n,1,1)` times 1.
The signed integrated order4 Taylor remainder is preserved
by `prolate_r1.quadrature.integrate`; do not substitute
`range_integral` on a signed coefficient, since that loses
cancellation. For all point gradients, every outer parameter
is a point Arb, rather than enclosing the entire parameter
box as in V38's first-order mean-value implementation.

## 3. General and MVT routes

GENERAL: `F(R,τ,λ)=H(R,τ,λ)`, directly the original
co-rotated C21 kernel `c21_regular.dens`; exterior
coordinates are `R,τ,λ`.

AXIS_MVT, SMALL_RHO_MVT and CENTER_MVT:
`F(ρ',z,λ)=E_{ρρ}(ρ',z;λ)` integrated on the full
sphere in the original convention `p_z=λz`.
Fix original R,τ box. The MVT identity
`H(ρ,z)=∫_0^1 E_{ρρ}(tρ,z)dt` holds when `E_ρ(0,z)=0`.
The extension `ρ'∈[0,ρ_hi]`, `z∈[zlo,zhi]` and
unsplit `λ∈[1279/256,5]` encloses every `E_{ρρ}`
encountered, so an outer Taylor enclosure of `F` on
this extension encloses `H` on the original box.
The fixed angular chart `τ_chart=midpoint(τbox)` rotates
the integration variables only, not the physical input.
The MVT kernel's independent positive lower bound
`D>=1-(ρ_hi+z_hi)>0` is used on its full extension,
including all jets. An angular mesh distance test may only
select cells, not serve as a substitute for the geometric
positive denominator lower bound.

## 4. Limitations and audit

The mathematical Taylor formula is standard, but accurate
implementation depends on valid outward Jet derivative arithmetic,
the frozen kernel definitions (including physical `p_z=λz`),
and all point/Hessian signed quadrature coefficients.
The independent source-level and numerical audit of these
new second-order coefficients is OPEN. Thus any sign exclusion
obtained from this producer remains a diagnostic, never
a fully adopted mathematical proof.

**DIAGNOSTIC_ONLY / NOT_EVIDENCE.**
