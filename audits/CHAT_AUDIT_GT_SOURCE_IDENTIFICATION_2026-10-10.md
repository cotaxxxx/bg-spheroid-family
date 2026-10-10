# CHAT AUDIT — machine Gt source-formula identification, and the cross-audit of G0/E1 v2 (2026-10-10)

Input: the ChatGPT cross-audit of G0/E1 v2 (relayed 22:37). It reports CONDITIONAL PASS and claims that the machine gt_box is identical, at source level, to T1 + T2 + T3.
chat re-checked the claim independently against pack `0bfc5c4e` (implementation head `85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b`). No computation was run for this audit; the code was only read.

## Findings (chat, independent)

1. **Chart dispatch.** Both C1b kernels (`67dda838` producer, `4eaca55d` checker) define `gt_box`. It uses `_gt_corner` exactly when `tr == T_HI` (T_HI = 1, kernel line 33/34) and `si == 0`, i.e. the first s-panel; otherwise it uses `_gt_ordinary`. The result is integrated over the s-panels. ✓
2. **Ordinary chart.** Producer `_ordinary` (`c2fee400`) and checker `_ordinary_refinement` (`15d66026`) both return `-4*mu*R*lam*rho^3*H/w`, `-2*Rg*lam2*H*H*Ahat*rho^5/w2` and `-2*R*lam3*Ahat*rho^3*(3*phi*H-gap*sq)/w`, with rho = s/√q, phi = d/√q, Ahat = A/√q, gap = 2 − s², mu = 1 − s². These are exactly T1, T2 and T3. ✓
3. **Quantities.** Both lineages compute H = (1 − e)·gap + λ²(2e − 2δ − e² + δe), which equals (1 − x)(2 − x) + λ²(2 − x)(x − δ) with x = e = s². Also w² = λ²e·gap + μ² and q = e·gap + λ²d². These match the source definitions. ✓
4. **R and R_γ.** On the γ chart, R = acos γ/√u and R_γ = (γR − 1)/u with u = 1 − γ². This matches the identity confirmed symbolically (C2_IDENTITY_CHECK, check 6). On the u chart, R = Ψ(u) = Σ C(2n,n)/(4ⁿ(2n+1)) uⁿ, which is the series of arcsin(√u)/√u, and R_γ = −2γΨ′(u) by the chain rule. ✓ The tail bound c_{N+1}u^{N+1}/(1 − u) is valid because the coefficient ratios are below 1: (2n+1)²/((2n+2)(2n+3)) for Ψ, and (2n+1)²/(2n(2n+3)) < 1 for Ψ′ with n ≥ 1. ✓
5. **Corner chart.** Both lineages use ρ ∈ [0, 1/√gap], |φ| ≤ 1/λ (taken at λ's lower end), Â from the scaled identity, R ∈ [1, π/2] and R_γ ∈ [−1, −1/3]. These are exactly the bounds of the scaled identities (both PASS in C2_IDENTITY_CHECK, checks 5b and 5c) and of the range of R_γ. ✓
6. **The domain constants in these modules ([63/64, 1] × [5/8, 33/50]) appear only in `produce_record` and `verify`.** The chart functions themselves are domain-free. So they may be reused for ① and ②, provided the new driver passes the new boxes.

**Verdict: concur. GT_SOURCE_FORMULA_IDENTIFICATION_PASS (chat, independent).** The status remains NOT_BINDING / NOT_CERTIFIED. The analytic dependencies (`5afa815f` and `7cb9b809`) are still EXTERNAL_AUDIT_PENDING. The correctness of the Arb interval enclosures as such is not re-audited here.

The cross-audit's other points are accepted:
- add one line citing π < 22/7;
- record the four module pins;
- restate §5 of G0/E1 as "source identity confirmed; dependencies pending external audit".
G0/E1 v3 is a tidy-up version only.

## Combined status of G0/E1 after v2 and its audits

| item | status |
|---|---|
| north and south arithmetic (M_N = 1000, M_S = 1304000, C_Λ = 1956000) | CHAT AUDIT PASS (c7e17aae) |
| identity G_t = T1 + T2 + T3 | chat symbolic check PASS (C2_IDENTITY_CHECK, 12 of 12) |
| machine Gt = T1 + T2 + T3 at source level, both lineages | PASS (this record) |
| `5afa815f` and `7cb9b809` | EXTERNAL_AUDIT_PENDING (No.15a / D6 bundle) |
| practical note | C_Λ is too coarse to clear boxes alone; boxes near t = 1 use direct Gt enclosure, which G0/E1 now justifies |
