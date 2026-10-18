# D5 V4 i_r=0 A/B comparison V0 — chat audit and Judge ruling (2026-10-18)

## 1. chat audit of `D5_V4_IR0_AB_PAPER_COMPARISON_DRAFT_20261018.md` (Dig draft)

**Verdict.** PASS (static), conditional on the inherited status of the off-centre signed bounds M₄₀⁻ < 100 and M₂₂⁻ < 200. These come from D4 Plan A V0.1 and carry its P1 / Lemma V conditions. No blocking findings.

**Arithmetic.** chat recomputed every rational value with Python Fraction. All match:
- f(119/200) = 13908967163/40000000000
- f(5/8) = 5155/12288
- f(2/5) = 416/9375
- all 6 positive margins of the §5 table
- 53248/3125 = 384·416/9375
- 13312/375

**Bound (T).** The one-sided bounds, evenness, and two FTC steps give −M₄₀⁻ρ²/6 and −M₂₂⁻z²/2.

**Choice of endpoints.**
- f is monotone, so its value at the lower endpoint ℓ is used.
- In z ≤ u·r·b(τ), the upper endpoint u is used.
- D_u is increasing in τ because 100u² > 50/3.

**Separation of the two bound sets.**
- The central coefficients 23 and 18 (ec8d243, λ ≥ 119/200, centre only) are correctly excluded from use as M in (T).
- The bounds 100 and 200 are used only on [119/200, 33/50], within the domain they were stated for.

**Conditional paper closure.**
- Region (0,1,3), τ ∈ [1/8, 1/4], is fully covered by the I1 and I2 rectangles.
- The residual regions G1 and G2 are correctly described as rectangle-cover residues, not as regions where H < 0.

## 2. Assessment and Judge ruling

**Assessment.** For λ = 2/5, a paper-only closure of r ≤ 1/8 requires M₄₀⁻ < 53248/3125 ≈ 17. The high-λ bound is 100, and λ = 2/5 is more oblate than the high-λ range, so a bound six times smaller is unlikely. A paper-only closure of the whole i_r = 0 column is therefore unlikely.

**Judge ruling (2026-10-18): "紙上＋区間計算の二本立て" — two tracks, paper plus interval.** Both tracks are paper design first. No computation is authorized.

**Track P (paper).**
- Derive off-centre signed bounds M₄₀⁻(I) and M₂₂⁻(I) on the low-λ slabs [2/5, 93/200], [93/200, 53/100] and [53/100, 119/200]. Finer λ splits are allowed if they are predeclared.
- From (S)–(R), fix an explicit rational δ_I > 0 for each slab, however small.
- Re-derive every source constant on the new band. Do not transfer the high-λ constants (γ ≥ 7/8, q ≥ 1 − 2y/3, and so on).

**Track I (interval).**
- Design an interval method for the residue δ_I ≤ r ≤ 1/8 (and G1, G2) that does not lose the s-average. The V3 near hull F_ρρ(s, z) over s ∈ [−ρ, ρ] destroyed it.
- Starting point: method A of the D4 method comparison V0, which keeps s as an auxiliary integration variable or uses Taylor models.
- Required:
  - the same H as P1;
  - an independent checker;
  - an exact cover with the Track P patches, with shared faces covered twice;
  - no result-driven tuning.
- Track I is a design document only, then audit. Its predeclare comes after.

**Order.** Track P comes first, because δ_I fixes Track I's domain. Track I design may proceed in parallel.

**What this ruling does not change.**
- D5 V3 stays ABORTED / NOT_EVIDENCE and is not resumed.
- No V4 predeclare is frozen.
- No research-PC computation is authorized.
