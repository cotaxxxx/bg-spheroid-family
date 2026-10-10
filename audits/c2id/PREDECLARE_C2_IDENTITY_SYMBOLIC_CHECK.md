# PREDECLARE — chat symbolic check of the C2 identity (2026-10-10)

Authorized by the Judge on 2026-10-10. Status: written before any computation.

**Objects** (from `5afa815f` §1 and `7cb9b809` §2–§3):
- μ = 1 − s², δ = 1 − t, d = s² − δ, A = 1 − tμ, q = 1 − μ² + λ²(μ − t)², w² = λ²(1 − μ²) + μ².
- γ = λA/(w√q), α = arccos γ, R = α/sin α, R_γ = dR/dγ.
- F = sAα², F_t = ∂_t F, G_t = ∂_t F_t.
- ρ = s/√q, φ = d/√q, Â = A/√q, H = (1 − x)(2 − x) + λ²(2 − x)(x − δ) with x = s², N = −s²H.
- T1, T2, T3 exactly as in C2 §3.

**Checks.** Exact symbolic algebra only (SymPy). No floating-point values. No sampling used as evidence.
1. q = s²(2 − s²) + λ²d², and 1 − μ² = s²(2 − s²).
2. α_t = −γ_t / sin α. Using this, F_t = s(−μα² − 2ARγ_t), with R treated through α_t only.
3. γ_t = λN/(w q^{3/2}) with N = −μq − λ²Ad, and N = −s²H (Lemma 1(i)).
4. G_t = s(4μRγ_t − 2AR_γγ_t² − 2ARγ_tt) as a polynomial in the independent symbols R and R_γ.
5. **Main gate:** G_t − (T1 + T2 + T3) = 0 identically, with R and R_γ as independent symbols. Each coefficient (of R and of R_γ) must simplify to exactly 0 for s, λ > 0 and q > 0. The scaled identities ρ²(2 − s²) + λ²φ² = 1 and Â = (2 − s²)sρ − (1 − s²)φ are checked as well.
6. R_γ = (γR − 1)/(1 − γ²) for R = arccos(γ)/√(1 − γ²).

**PASS** if every check simplifies to 0, or to a stated equality, exactly. **FAIL** if any check leaves a nonzero residue. Either outcome is reported verbatim.
**Scope:** audit evidence for the identity only. No bound, no constant and no certificate is produced.
