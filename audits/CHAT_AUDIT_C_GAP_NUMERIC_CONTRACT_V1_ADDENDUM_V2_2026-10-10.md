# CHAT AUDIT — ①② numeric contract v1 and endpoint addendum v2 (2026-10-10)

Previous audit, with the S1 ruling appended: `9b026f66…f526`, confirmed by ChatGPT. No computation was run for this audit.

**Verdict: both PASS as contract text.** S1 is implemented exactly, and S2 (the reason ① uses fixed precision) is written out.

What was checked:
- **① partition:** t_j = 31/32 + j/512 for j = 0…16 is exact; 16 × 1/512 = 1/32. ✓
  - The seed at 31/32 is well conditioned (q ≥ λ²/1024).
  - The boxes j ≤ 14 have δ ≥ 1/512, and the s-panel width √2/8192 ≈ 1.7·10⁻⁴ is well below λ₋δ = 7.8·10⁻⁴, so the ordinary chart is well conditioned.
  - Box 15 touches 1 and gets the corner chart through the kernel's `tr == T_HI` dispatch (T_HI = 1). ✓
- **Cumulative gate:** for t in Q_m, g(t) ≤ g(t₀) + Σ_{j<m} Δ·max(0, U_j) + (t − t_m)·max(0, U_m) ≤ U_cum. Every term is non-negative, so U_cum < 0 gives g < 0 on the whole strip, t = 1 included (G0/E1: C¹ on [t₀, 1) with left derivative at 1). ✓
- **② rule:** N = ⌈512(1 − t_*)⌉ is the smallest equal-box count of width ≤ 1/512, and 1 ≤ N ≤ 16. When N ≥ 2, Δt > 1/1024, so the non-final boxes have δ ≥ 1/1024 > panel width / λ₋ (with λ ≥ 9/20). ✓
- The precision fixed for ① (baseline identity) and the precision ladder kept for ② are each predeclared, and the reason is now stated. ✓
- B_ob is non-gating (BOB_SIGN_CONSISTENCY_CHECK only). ✓

**T1 (required, small) — implementation design v1 is now inconsistent with the ruling.**
- Design v1 §9 and the definition of DIFF-D still describe "interior g_box + final mean-value box". Control #9 in §13 does the same.
- Addendum v2 and numeric contract v1 replace this per S1.
- A design v2 must update §9, DIFF-D and control #9 to: seed g only, Gt boxes plus the cumulative sum. Otherwise the diff audit would be done against a superseded definition.
- Text only; no new decision is needed.

**T2 (note, no change required) — the ② seed sits at t_* = max(31/32, t₊).**
- When t₊ is close to 1, the seed is less well conditioned.
- This is the same right wall that C1b already certified negative for every unclamped slab: receipt §5.2, sup g(t₊, Λ) < 0.
- So the evaluation is known to be feasible, and the 4096 → 8192 → 16384 ladder is predeclared. Recorded only.

**Status:**
- numeric contract v1: text PASS.
- addendum v2: text PASS.
- design v1 → v2 for T1.

Remaining FREEZE blockers: D6 (`5afa815f`, `7cb9b809`); the ① implementation and its full diff audit, including the import-closure identity; the ② seal path (L0). Nothing is frozen. No computation is authorized.
