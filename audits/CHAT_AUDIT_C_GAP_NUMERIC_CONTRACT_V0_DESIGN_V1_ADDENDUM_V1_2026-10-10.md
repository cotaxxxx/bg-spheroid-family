# CHAT AUDIT — ① implementation design v1, endpoint addendum v1, and the ①② numeric contract v0 (2026-10-10)

Baseline: bg-spheroid-family main `1c9a6e03` (STATE v1.13). Previous audit, with the rulings appended: `e206478f…c692f`.
No computation was run for this audit. The baseline code was read at `85eca228`; the estimates in S1 are on paper.

## Overall result

| Document | Verdict |
|---|---|
| design v1 | PASS as design text. DIFF-K is added and restricted correctly. The 15-module import closure is pinned byte-identical. The t-edge ownership is written out. B_ob is non-gating |
| addendum v1 | PASS as text. **S1 below, however, affects how it is realised** |
| numeric contract v0 | CONDITIONAL. All inherited constants are correct (S0). **S1 is a structural risk in the endpoint partition** |

**S0 — the inherited constants match the baseline code exactly** (kernel `67dda838`, lines 28–53):
- BITS 160 and DEG 50;
- the T stages (8/4/4096, 16/8/4096, 32/16/8192);
- every ROOT_* constant, T2_ENDPOINT_REFINE_DEPTH 4, E0 24/8, E stages 1024/2048/4096, E_BOX_CAP 4096, MONO_WORK_CAP 2²⁰;
- PRED 1024/256 and ATTEMPT_WORK_CEILING 25.6M.
- The scaled ceilings are exact: 53.76e9 × 8/7 = 61.44e9; 28.672e9 × 8/7 = 32.768e9; MAX_ACCEPTED 1120 → 1280; MAX_ATTEMPTED 2100 → 2400.
- Δλ = 1/3200 divides all three regions: 118 + 7 + 35 = 160 slabs. ✓

---

**S1 (major) — the dyadic endpoint partition places direct-g boxes where the interval evaluation is badly conditioned.**

The interior endpoint boxes [1 − 2⁻ʲ, 1 − 2⁻⁽ʲ⁺¹⁾] go down to δ = 1 − t ≈ 2⁻¹⁶. On them the contract uses `g_box`, which integrates the **unscaled** density s(−μα² − 2ARγ_t) with γ_t = λN/(w q^{3/2}) (`_g_density_stable`). On the first s-panel, which contains s = 0:
- q is as small as about λ²δ², so q^{3/2} ≈ λ³δ³;
- the interval for s²/q^{3/2} has an upper end of about (√2/8192)²/(λ³δ³).

With λ = 2/5 and δ = 2⁻¹⁶ that is about 3·10⁻⁸ / (0.064 · 3.6·10⁻¹⁵) ≈ 10⁸. The true integrand is bounded (Lemma 2), but the enclosure is not tight. This is the corner singularity, which the scaled identity exists to remove. The ordinary Gt chart has the same problem when the box does not touch t = 1: there ρ = s/√q is evaluated as an interval quotient. Only the **corner chart** (used when the t-box touches 1) is stable.

In practice, the boxes with large j will fail as ENDPOINT_INTERIOR_G_INCONCLUSIVE, independent of the mathematics. The baseline never evaluated g_box this close to t = 1. Its g-boxes stop at 31/32, and near t = 1 it used special corner rules (ROOT_GL_CORNER_TAU = 65535/65536, T2_ENDPOINT_REFINE_DEPTH).

**Recommended fix (needs a ruling, because it changes the detail of the earlier ruling):** use the cumulative mean-value form on a **uniform** partition of [31/32, 1]:
- use g only at the seed t = 31/32. There q ≥ λ²(1/32)², which is well conditioned; it is the same edge the C1b and census evidence used;
- divide [31/32, 1] into N equal t-boxes, for example N = 16 of width 1/512, the same scale as the band's [63/64, 1] / 8 run, which closed;
- evaluate sup G_t on each box. The last box touches 1 and uses the corner chart. The others have δ ≥ 1/512, so the ordinary chart is well conditioned if the s-panel width is below λ₋δ_min, i.e. √2/P ≤ (2/5)/512, so P ≥ 1811. 4096 or 8192 panels satisfy this;
- the gate is sup g(31/32, Λ) + Σⱼ (1/512)·max(0, sup G_t on box j) < 0.

This is still the mean-value principle, justified by G0/E1 (g is C¹ on [31/32, 1) with left derivative at 1 and |G_t| ≤ M). It reduces to the monotone gate when every sup G_t < 0. It uses only well-conditioned evaluations. For ② the same applies with the seed at t_* and a uniform partition of [t_*, 1].

**S2 (minor).** ① fixes precision at 160/192 bits with no escalation. ② keeps the 256→512→1024 / 320→640→1280 ladder from its v3. The difference is allowed, because each is predeclared, but write the reason (baseline identity for ①) in the contract so that it does not look like an inconsistency.

**S3 (minor).** The final-box term (1/65536)·max(0, sup G_t) would be harmless. Under S1 it is replaced by the cumulative sum, so the separate final-box rule disappears.

---

**Status:**
- design v1: PASS as text.
- addendum v1: PASS as text, to be updated per the S1 ruling.
- numeric contract v0 → v1: S1 as ruled, S2.

Remaining FREEZE blockers: D6, the implementation and its diff audit, and the ② seal path. Nothing is frozen. No computation is authorized.

---

## Judge ruling (2026-10-10, after this audit)

**S1: cumulative mean-value form.** This replaces the detail "interior g_box + final box" of the previous ruling. The mean-value principle itself is unchanged.

- **①**
  - Seed: g at t = 31/32 only.
  - [31/32, 1] is split into 16 equal t-boxes of width 1/512.
  - Each box gets a G_t enclosure. The box touching t = 1 uses the corner chart; the others use the ordinary chart with s-panels ≥ 4096.
  - Gate: sup g(31/32, Λ) + Σⱼ (1/512) · max(0, sup G_t on box j) < 0.
- **②**: the same, with the seed at t_*(Λ) and [t_*, 1] split into the smallest number of equal boxes of width ≤ 1/512. This is a fixed rule computed from t_* alone.
- Not allowed:
  - no direct g_box inside (t_e, 1);
  - no C_Λ at run time;
  - no change to the partition during a run.
