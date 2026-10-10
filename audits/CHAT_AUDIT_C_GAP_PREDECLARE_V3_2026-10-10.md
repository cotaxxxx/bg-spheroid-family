# CHAT AUDIT — C gap ① and ② predeclare drafts v3 (2026-10-10)

Baseline: bg-spheroid-family main `32218d78`, STATE v1.12. Previous audit (v2), with the E3 ruling appended: `43f3d811…10dd`, whose full 64 digits ChatGPT confirmed.
No computation was run for this audit. Sources were read on GitHub only.

## Overall result

| Draft | Verdict | Remaining before FREEZE |
|---|---|---|
| ① U₁ v3 | CONDITIONAL PASS | H1 (λ_x box: a defect in the rule itself), H2 (predictor pin and march direction), plus G0, E1_FORMULA, APPROX_DEGREE |
| ② U₂ v3 | **PASS as contract text** | Only SEAL_PATH (an L0 inspection on the research PC), E1_FORMULA and APPROX_DEGREE |

v2 findings confirmed as fixed:
- E1: the left group is closed, [2/5, 699/1600].
- E2: the C1b tube rule is adopted.
- E3: only the two endpoint signs are gating inputs, and λ_x stays NON_GATING.
- F1: all four SHA-256 values are given in full.
- F2: the clamped slabs are a ledger consistency check only.

---

## ① U₁ v3

**H1 (major — the rule cannot work on the λ_x box as written).**
- The adopted C1b rule requires, on every right-group slab, a certified root enclosure T_* with sup|t_c − T_*| ≤ 1/64.
- On the λ_x box [699/1600, 281/640], every λ < λ_x has no root in [1/2, 1] (g(1/2, λ) < 0). So any slab of that box that contains a λ < λ_x cannot produce T_*.
- The C1b predictor step P1 (`GLOBAL_AXIAL_C1B_PREDICTOR_PRE_RUN_AMENDMENT.md`, blob `c785ceda`) also needs a sign change from + to − on the grid t_k = 1/2 + k/1024. Where g(1/2, λ_mid) < 0 it finds none. It then sends the slab to λ-refinement, and the refinement can never succeed.
- The draft's own "監査注意" sees this risk. As written, the box ends in RESOURCE_CAP or CERTIFICATE_FAILED whatever the mathematics is.
- Fix (predeclare a separate rule for the λ_x box only):
  - Λ ⊂ [699/1600, 281/640]: no predictor and no acceptance gate. Fix t₋ = 1/2 and a rational t₊ written into the contract. Suggested t₊ = 1/2 + 2w₀ = 5/8; this is the largest t₊ that C1b's left-clamped geometry allows.
  - Certify ∂_t g < 0 on [1/2, t₊] × Λ and g < 0 on [t₊, 1] × Λ (t = 1 through E1).
  - Then the number of roots is 0 or 1, decided by the sign of g(1/2, λ) from C1a.
  - The C1b predictor rule applies only on [281/640, 9/20], where g(1/2, ·) > 0 is certified.
  - If t₊ = 5/8 fails, the outcome is FAIL-CLOSED and a new version. There is no search during the run.

**H2 (major — PREDICTOR_PIN_OPEN can be closed now, but the rule depends on the direction of the march).**
- The executed C1b predictor is the three-step rule P0, P1, P2 in blob `c785ceda`.
- Its P0 (continuation) starts at λ = 9/20 with t_cont = 9/16 and uses "the immediate left neighbour". It assumes a march in increasing λ.
- For [281/640, 9/20], v4 must fix one direction:
  - **Recommended:** decreasing λ, starting at 9/20 with t_cont = 9/16, the same anchor C1b used; continuation uses the right neighbour.
  - Alternatively: increasing from 281/640, where the first slab uses the P1 scan alone.
- Either way this is a recorded adaptation of P0, not a reuse of it as is.
- The code that ran C1b is pinned in the C1b machine receipt §1.2: implementation head `85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b`, with producer kernel `67dda838`, producer gating `a93ca173`, and driver `5fd308bb`. The contract stack that actually ran is §C1b.4 plus the amendments up to v2.12s (root localization by parametric mean value and others), not §C1b.4 alone.
- v4 must cite the whole stack by blob, or list explicitly which parts of it are inherited.

**H3 (minor).** The claim "simple root" in §1 needs ∂_t g ≠ 0 at the root. In the tube that is the G2 sign (∂_t g < 0). On the λ_x box it is the H1 tube. State this explicitly in G4.

## ② U₂ v3

No new findings. The text is ready.

What still blocks a FREEZE is outside the text:
- the L0 seal path, which the first read-only `ls` on the research PC settles;
- the shared E1 formula;
- the approximation degree.

---

## Next step — the paper proofs G0 and E1

ChatGPT's proposal to start G0 and E1 now, in parallel, is endorsed. They are on the critical path of both ① and ②, and they need no compute. Suggested scope for the drafts:

- **G0:** differentiation under the integral sign for g on [2/5, 9/20] × [1/2, 1). Required:
  - an explicit dominating function;
  - the identification of the machine quantity Gt (in the kernel `67dda838` / `4eaca55d`) with ∂_t g;
  - a check that the existing C2 lemma `7cb9b809` (domain [5/8, 33/50] × [63/64, 1]) is not reused.
- **E1:** the two-chart estimate on [t_e, 1] × Λ, for λ ∈ [2/5, 5/8]. Required:
  - a statement of the form |g(t, λ) − B_ob(λ)| ≤ C_Λ (1 − t)^α with C_Λ rational, or an explicit equivalent;
  - building on Lemma 5 of `OBLATE_ENDPOINT_C1_LEMMA.md` (`5afa815f`, continuity and the identity with B_ob, no rate);
  - covering the B_ob two-chart kernel used by the B_ob subgate (`0f19e387`).

Each one is drafted, then CHAT AUDIT, then a Judge ruling, as separate documents. Nothing is frozen. No computation is authorized.

---

## Judge rulings (2026-10-10, after this audit)

1. **H2: decreasing λ.** On [281/640, 9/20] the march starts at λ = 9/20 with t_cont = 9/16 (C1b's anchor). Continuation uses the certified root enclosure of the right neighbour. P1 and P2 are unchanged. ① v4 records this as an adaptation of P0 in blob `c785ceda`.
2. **G0 and E1: start drafting now**, in parallel with ① v4. Each is a separate paper-proof document, followed by CHAT AUDIT and a Judge ruling. No computation.
