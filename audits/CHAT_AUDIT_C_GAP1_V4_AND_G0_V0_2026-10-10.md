# CHAT AUDIT — C gap ① v4 and G0 v0 (2026-10-10)

Baseline: bg-spheroid-family main `32218d78`, STATE v1.12. Previous audit (v3), with two rulings appended: `2e656574…4887`, confirmed by ChatGPT.
Received:
- ① v4, as an attachment.
- G0 v0, as text in the message.
- **E1 v0 was not received.** The message links to a sandbox file that does not reach chat. E1 is not audited here; please send its text.

No computation was run for this audit. Sources were read on GitHub (bg-oblate-spheroid `design/d-ob-p2`).

## Overall result

| Document | Verdict |
|---|---|
| ① v4 | CONDITIONAL PASS. The λ_x box fix (X) is correct. **J1 is a real defect** in the inherited predictor rule. J2 closes AMENDMENT_STACK_PIN_OPEN in a defined way |
| G0 v0 | **Not acceptable as written (FAIL-CLOSED → v1).** It treats the kernel as an unknown placeholder although the source exists, and it has no content to audit. Also see J4: G0 and E1 can be one lemma |

---

## ① v4

What is confirmed:
- **X (λ_x box) is correct.** There is no predictor and no root gate. The tube is fixed at [1/2, 5/8] with ∂_t g < 0, and g < 0 on [5/8, 1]. The root count comes from the sign of g(1/2, λ) given by C1a.
- The case analysis is right: g(1/2) < 0 gives 0 roots; g(1/2) > 0 gives 1 root, by the intermediate value theorem with g(5/8) < 0 and continuity (Lemma 3 of `5afa815f`); g(1/2) = 0 gives only the boundary root, which is not in U₁.
- L is closed on [2/5, 699/1600]. R marches leftward from 9/20 with t_cont = 9/16, as ruled.

**J1 (major) — "P1/P2 は変更しない" inherits a rule that was superseded.**
- The P2 selection test |t_cont − t_scan| ≤ 1/64 in `c785ceda` was replaced by `GLOBAL_AXIAL_C1B_PREDICTOR_SELECTION_ADDENDUM_V2_3.md` (blob `5326e2b5`), which uses `|continuation − scan_mid| <= ROOT_TARGET`.
- `…_SUPERSESSION_ADDENDUM_V2_3_1.md` (blob `4a493191`) states that v2.3 "explicitly supersedes, and is the sole binding replacement for" the old rule. It also requires that the old rule be removed from both producer and checker.
- The executed C1b therefore did **not** use the P2 that v4 cites.
- Fix: R inherits P0 (adapted leftward), P1 from `c785ceda`, and **the P2 selection rule of v2.3 / v2.3.1** (with the value of ROOT_TARGET written out).

**J2 (major) — how to close AMENDMENT_STACK_PIN_OPEN.**
- The C1b machine receipt §1.3 pins only `8e04e2ef` and the B_ob bridge contract. On the branch there are **27** C1b amendment and addendum files (listed below). Reconciling all 27 as text is a large and error-prone task.
- What actually ran is fixed by the code blobs in receipt §1.2:
  - producer: kernel `67dda838`, gating `a93ca173`, producer `0616fbd7`, driver `5fd308bb`;
  - checker: kernel `4eaca55d`, gating `03df2620`, checker `0760764e`.
- Recommendation for v5: those seven code blobs are the authority for inherited execution details. The 27 documents are cited by blob as the explanation of that code.
- ① then needs a **new** implementation for the changes: P0 leftward, the X box, the L group and E1. Its diff against the seven blobs must be the only behavioural change, and that diff is audited before FREEZE.

C1b amendment stack on `design/d-ob-p2` (blob prefix and file):

```
59b291c1 C1B_PREFLIGHT_LSCPU_CANONICALIZATION_AMENDMENT
cf3cded3 …BUNDLED_ROOT_GT_T2_ENDPOINT_REFINEMENT…_V2_10
8cc3d6d4 …CONTROLS_FIX…_V2_10_1
8d780b2b …ENDPOINT_SAFE_R_NONFINITE_DIAGNOSTICS…_V2_6
b8226089 …GL_T_CELL_NONFINITE_FAIL_CLOSURE…_V2_5
d4fad54d …GL_T_CELL_NONFINITE_FAIL_CLOSURE…_V2_5_1
bb0f8d20 …IMPLEMENTATION_PRE_RUN_AMENDMENT
05046e03 …MONOTONE_CLOSURE_WALL_ADJACENT_EXTERIOR…_V2_4
7cc992fb …PARAMETRIC_MEAN_VALUE_CROSS_LINEAGE_COMPARISON_ADDENDUM_V2_1
af586ef7 …PARAMETRIC_MEAN_VALUE_ROOT_LOCALIZATION…
fa544b63 …POSITIVE_Q…_V2_8
cd42fe1f …POSITIVE_Q…_V2_8_1
177c2195 …POSITIVE_Q…_V2_8_2
15f7e92a …POSITIVE_Q…_V2_8_3
c785ceda …PREDICTOR_PRE_RUN_AMENDMENT
5326e2b5 …PREDICTOR_SELECTION_ADDENDUM_V2_3
4a493191 …PREDICTOR_SELECTION_SUPERSESSION_ADDENDUM_V2_3_1
8e04e2ef …C1B_PRE_RUN_AMENDMENT
80c0cfce …RECLASSIFICATION_ENCLOSURE_DERIVED_FIELDS…_V2_4_2
c5a8e709 …REGROUPED_GLAM…_V2_7
fa3f50d9 …REGROUPED_GLAM…_V2_7_1
e7081df2 …RESUMABLE_DRIVER_PRE_RUN_AMENDMENT
38a09de2 …ROOT_BRACKET_TAU_PRIME_CLAMP_TWO_PART_STRIP…_V2_12
752db7fc …ROOT_GT_T_REFINEMENT…_V2_9
90cfe906 …ROOT_GT_T_REFINEMENT…_V2_9_1
8d3e32e9 …ROOT_MV_GL_CORNER_SEPARATION…_V2_11
d5c1ab97 …ROOT_MV_GT_CLAMP…_V2_11_1
```

**J3 (minor).** The appendix that copies v3 in full makes the document longer without adding anything. The v3 file is pinned by the audit chain, so a reference is enough. This is not a blocker.

---

## G0 v0

**J4 (major) — the source exists, and the draft does not use it.** The draft says "K, Ω, μ は原典の厳密定義で置換すべきプレースホルダであり、現草稿は原典に無い具体式を創作しない". The definitions are already in the repository:

- `analysis/OBLATE_ENDPOINT_C1_LEMMA.md` (blob `5afa815f`, EXTERNAL_AUDIT_PENDING):
  - §1 defines F_t = s[−μα² − 2ARγ_t] and the integration variable s ∈ [0, √2].
  - Lemma 1 gives q > 0 and 0 < γ ≤ 1 for t < 1.
  - **Lemma 2 gives an explicit integrable majorant |F_t| ≤ M(s)** for t ∈ [1/2, 1).
  - Lemma 3 proves g = ∫F_t ds on [1/2, 1).
  - Scope: **any I = [λ₋, λ₊] with 0 < λ₋ ≤ λ₊ < 1/√2**. This includes [2/5, 9/20] and [2/5, 5/8].
- `analysis/MONOTONE_TUBE_C2_INTERCHANGE_LEMMA.md` (blob `7cb9b809`) does exactly the G0 step one derivative higher, on [5/8, 33/50] × [63/64, 1]:
  - G_t := ∂_t F_t, a corner-scaled identity G_t = T1 + T2 + T3 that removes the negative powers of q;
  - on the north half s ∈ [0, 1], explicit bounds in λ₋ and λ₊ only (for example |T1| ≤ 4(π/2)λ₊·4/λ₋);
  - on the south half s ∈ [1, √2], a compact bound using q ≥ λ₋²(63/64)²;
  - in §6, dominated differentiation that is **uniform up to t = 1**.

So G0 is not new territory. It is the C2 lemma on a different domain. The method may be followed; the domain-dependent steps must be re-proved:

1. **North half:** the bounds depend only on λ₋ and λ₊. Re-evaluate them with λ₋ = 2/5 and check every use of λ₋ = 5/8 (for example |φ| ≤ 1/λ₋ and w ≥ λ₋).
2. **South half:** the C2 bound q ≥ λ₋²(63/64)² uses t ≥ 63/64. For t ∈ [1/2, 1] a new lower bound for q is needed. This is the one genuinely new estimate.
3. **Identification with the machine Gt:** term-by-term against the kernels `67dda838` and `4eaca55d`, as the draft already says.

**J5 (major, simplification) — G0 and E1 should be one lemma.**
- If the majorant max(M_N, M_S) for G_t holds uniformly on [1/2, 1] × [2/5, 5/8], then for t < 1:
  - |g(t, λ) − B_ob(λ)| = |∫_t^1 ∂_t g| ≤ √2 · max(M_N, M_S) · (1 − t).
- That is exactly the E1 target with **α = 1** and C_Λ = √2 · max(M_N, M_S), using Lemma 5 for the limit.
- It also gives the one-sided derivative at t = 1 (C2 §6). So the machine can enclose ∂_t g directly on boxes that reach t = 1, as the band's Claim 1 did on [63/64, 1].
- Recommendation: one paper proof, "G0/E1: uniform G_t majorant on [1/2, 1] × [2/5, 5/8]", covering the λ-ranges of both ① and ②.
- Caution: the coarse constants may be large. A large C_Λ makes the (1 − t) route weak near t = 1, but it does not make it wrong. Whether boxes near t = 1 use the C_Λ(1 − t) bound or a direct enclosure of G_t is decided in the contract, before any run.

---

**Status:** ① v4 → v5 (J1, J2). G0 v0 → a combined G0/E1 lemma v1 built on `5afa815f` and `7cb9b809` (J4, J5). E1 v0: please send its text. Nothing is frozen. No computation is authorized.

---

## Judge ruling (2026-10-10, after this audit)

**J5: G0 and E1 are merged into one lemma.**
- ChatGPT drafts a single paper proof, "G0/E1: uniform G_t majorant on [1/2, 1] × [2/5, 5/8]".
- It is built on `5afa815f` (Lemmas 1–3 and 5) and follows the method of `7cb9b809`.
- New work is limited to:
  - re-deriving the north-half constants with λ₋ = 2/5;
  - a new lower bound for q on the south half for t ∈ [1/2, 1];
  - identifying the machine Gt term by term with the kernels `67dda838` and `4eaca55d`.
- E1 then follows with α = 1 and C_Λ = √2 · max(M_N, M_S).
- The separate E1 v0 draft is set aside; there is no need to send it.
