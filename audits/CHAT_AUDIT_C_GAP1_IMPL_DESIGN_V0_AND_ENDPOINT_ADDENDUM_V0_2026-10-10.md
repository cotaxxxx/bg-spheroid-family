# CHAT AUDIT — C gap ① implementation design v0 and the t=1 direct-Gt addendum v0 (2026-10-10)

Baseline: bg-spheroid-family main **`1c9a6e036884d58de782bc47cb220700187fe511`**, checked on GitHub. Its parent is `32218d78`; STATE.md SHA-256 begins `0c6b6aae…`, which is v1.13. The save is confirmed.
No computation was run for this audit. Code was read at implementation head `85eca228`.

## Overall result

| Document | Verdict |
|---|---|
| ① implementation design v0 | CONDITIONAL PASS. The structure is right: seven files mirroring the baseline seven, hunks labelled DIFF-A to DIFF-E, the leftward march done by queue order only, and the X and L paths unable to reach the predictor. **Q1 is a gap in the allowlist itself.** Q2 is a robustness change to the endpoint gate |
| endpoint addendum v0 | CONDITIONAL PASS. Not using C_Λ(1 − t) at run time is right. The gate itself should be the mean-value form (Q2). The role of B_ob needs a Judge ruling (Q3) |

Confirmed in code:
- `choose_predictor(slab, previous_root)` sets t_cont = 9/16 when `previous_root is None`, and otherwise the midpoint of the previous root enclosure (kernel `67dda838`, lines 929–930).
- So the leftward P0 really can be obtained by queue order alone, starting at the slab next to 9/20, with the right child processed first on refinement. P1 and P2 stay byte-identical. ✓

---

**Q1 (major) — the allowlist has no category for domain constants and controls.**
- The baseline kernel hard-codes the C1b domain:
  - line 30: `L_LO, L_HI = Fraction(9, 20), Fraction(5, 8)`;
  - line 31: `DLAM, N_COARSE = Fraction(1, 800), 140`;
  - line 1817: the domain printout with "direction increasing";
  - self-test controls tied to historical C1b slab 105 (`Slab(105, 1, 93/160, 931/1600)` and others, lines 633, 793, 1794) and boxes built from L_LO + DLAM.
- ① must change all of these, and none of the changes is behavioural in the sense of (a)–(d).
- Also, **DLAM = 1/800 does not divide the ① regions**:
  - R = [281/640, 9/20] has width 7/640 = 8.75/800;
  - X has width 7/3200;
  - L has width 59/1600.
  - So the slab widths for each region must be fixed in the numeric contract.
- Fix: add one category, **DIFF-K (domain constants and self-test controls)**. It is limited to:
  - the region endpoints;
  - the slab width and count per region;
  - the direction printout;
  - replacing the C1b-specific controls with ① controls, which are declared in the numeric contract.
  Every DIFF-K hunk must be one of these listed items.

**Q2 (major, robustness) — use the mean-value endpoint gate instead of requiring G_t < 0 on the whole strip.**
- The gate "g(t_e) < 0 and G_t < 0 on [t_e, 1]" is sufficient but stronger than needed.
- For λ ∈ [2/5, 9/20] nothing certified says that g is decreasing on [31/32, 1]. The band certificate that showed ∂_t g < 0 there covers [5/8, 33/50] only.
- If g has an interior minimum below 31/32 … 1 and then rises towards B_ob < 0, then G_t > 0 somewhere. The gate would fail although g < 0 throughout. This is the same overreach as audit A2.
- The mean-value form uses the same two machine quantities and covers more cases:
  - for an endpoint sub-box [t_k, 1] × Λ: sup g ≤ sup g(t_k, Λ) + (1 − t_k) · max(0, sup G_t over [t_k, 1] × Λ) < 0.
  - This is legitimate by G0/E1: g is C¹ on [t_k, 1) with the left derivative at 1, and |G_t| ≤ M.
  - When sup G_t < 0 it reduces exactly to the monotone gate in the draft.
- Also, boxes [t_k, t_{k+1}] with t_{k+1} < 1 can be closed by direct `g_box`, because q > 0 there. Only the last sub-box touching t = 1 needs G_t.
- Recommendation for ① and ②: the endpoint gate is
  - g_box < 0 on the interior sub-boxes of [t_e, 1), and
  - the mean-value bound on the final sub-box [t_k, 1].
  - The sub-box partition and t_k are fixed before the run.
  - No other route exists; C_Λ is never used at run time.

**Q3 (Judge) — what B_ob becomes.** With the endpoint gate (in either form), g(1, λ) = B_ob(λ) < 0 is a **consequence** of the certificate, by continuity (Lemma 5). It is no longer a separate input. So:
- ①'s G1 ("B_ob < 0 on [2/5, 9/20], unproven") is discharged by the endpoint gate and need not be a separate gate;
- for ②, the existing B_ob receipts become consistency checks.
Recommended: record it this way. Keep the B_ob receipts and compare signs as a consistency check, without using them as gates.

**Q4 (minor) — imported modules.**
- The new ① files import the Gt chart modules and their closure: the 15 modules in pack `0bfc5c4e`, including `c2fee400`, `15d66026`, `f2fa2a5a` and `b6d96df2`.
- The design's "no 8th file" rule is right for new code. In addition, the design must state that **every imported baseline module is used unchanged, at its pinned blob**. The diff audit then checks that the import closure is byte-identical, not only the seven files.

**Q5 (minor).** X §6 step 2 says "g < 0 on [5/8, 31/32]". The joining edges at t = 5/8 and t = 31/32 must be shared closed edges, with ownership written down as in ②. This is a numeric-contract item.

---

**Status:**
- design v0 → v1: Q1, Q2 (if ruled), Q4, Q5.
- addendum v0 → v1: Q2 and Q3 as ruled.
- The numeric contract (partitions, precision, degree, caps) is still to be written.
- Nothing is frozen. No computation is authorized.

---

## Judge rulings (2026-10-10, after this audit)

1. **Q2: mean-value endpoint gate.** For ① and ②:
   - interior sub-boxes of [t_e, 1) are closed by direct g_box < 0;
   - the final sub-box [t_k, 1] is closed by sup g(t_k, Λ) + (1 − t_k) · max(0, sup G_t) < 0;
   - the partition and t_k are fixed before the run;
   - there is no other route, and C_Λ is not used at run time.
2. **Q3: B_ob is a consequence.** ①'s G1 is removed as a separate gate, because the endpoint gate implies B_ob < 0. The existing B_ob receipts are kept and used only as sign-consistency checks.
