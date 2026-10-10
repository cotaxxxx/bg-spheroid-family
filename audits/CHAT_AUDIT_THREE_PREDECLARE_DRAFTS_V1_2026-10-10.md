# CHAT AUDIT — three predeclare drafts v1 (2026-10-10)

Baseline: bg-spheroid-family main `32218d78`, STATE v1.12. v0 audit: `9a4ff4f2…805d` (including the Judge rulings).
No computation was run for this audit. Sources were read on GitHub only.

## Overall result

All v0 findings are addressed, except the ① citation (A1) and the ③ input pack (C1). None of the three can be FROZEN yet. Each one still carries its own declared blockers (E1-FORMULA, APPROX-DEGREE, QUADRATURE_CONTRACT_INCOMPLETE, and the paper proofs G0 and E1). This is correct and expected.

| Draft | Verdict | Must fix for v2 |
|---|---|---|
| ① U₁ | CONDITIONAL PASS | A1 (wrong source), A2 (the fixed t_R is stronger than the claim needs) |
| ② U₂ | CONDITIONAL PASS | B1 (the ledger pin can be fixed now) |
| ③ prolate | CONDITIONAL PASS | C1 (the input pack contains lineage-1 formulas), C2 (which shared libraries count as independent) |
| all three | — | D1 (budget units and the research PC are shared with D5) |

v0 findings confirmed as fixed:
- M1 → G0 interchange obligation.
- M2 → transversality now argued from receipts, with the 6fba6e4f condition.
- M3 → per-slab structure.
- N1 → exact U₂.
- N2 → shared endpoint method E1, with no switching during a run.
- P1 → manuscript pinned.
- P2 → Arb, FLINT and RBF are excluded.
- P3 → clean-room mechanism.
- P4 → Tier A / Tier B gates exactly as ruled (q₂ = 1/100).
- P5 → failure classes.

---

## ① U₁

**A1 (major) — wrong source.**
- `analysis/CENSUS_IDENTIFICATION_CONTRACT.md` (blob `fe675d0a`) is the census contract of the boundary tube. Its only target is "g_axis_ob(63/64, λ), λ ∈ [5/8, 33/50], sign POS". It does not define any axial census requirement for U₁.
- Citing it would tie U₁ to a contract with a different scope.
- Fix: drop the citation and state the claim directly. For each λ ∈ [2/5, 9/20), the number of zeros of g(·, λ) on (1/2, 1] is 1 if λ > λ_x and 0 if λ ≤ λ_x, and every such zero is simple.

**A2 (major) — t_R = 31/32 for every slab overreaches.**
- G2 requires ∂_t g < 0 on the whole [1/2, 31/32] × Λ for every slab. The claim does not need that.
  - On slabs entirely left of 699/1600, g(1/2, λ) < 0 and g(1, λ) < 0. There it is enough to show g < 0 on [1/2, 1]. Monotonicity is not needed.
  - On the slabs to the right, C1b itself never certified monotonicity on all of [1/2, 31/32]. All 159 C1b slabs used a left exterior cover with g > 0 on [1/2, t_minus] and t_minus > 1/2, followed by a tube.
- A stronger hypothesis can fail where the claim is true. It would then be recorded as a CERTIFICATE_FAILED that says nothing about the claim.
- Fix: predeclare one deterministic per-slab rule. This is allowed because it is fixed before the run and is not exploratory:
  - **Form N (no root):** g < 0 on [1/2, 1] × Λ. Allowed only on slabs Λ ⊂ [2/5, 699/1600].
  - **Form T (tube):** g > 0 on [1/2, t₋] × Λ, ∂_t g < 0 on [t₋, t₊] × Λ, and g < 0 on [t₊, 1] × Λ, as in C1b. t₋ and t₊ are taken from a fixed rational ladder that is written into the contract.
  - **The λ_x box [699/1600, 281/640]:** Form T with t₋ = 1/2. Transversality at λ_x is already argued.
  - Order: Form N then Form T, decided by the slab's position. Do not try one form and then switch after a failure.

**A3 (minor).** G5 can be stated as an overlap of closed boxes on the line λ = 9/20 with C1b's first slab. Since λ = 9/20 is not in U₁, identity of the branch is a statement about continuity, not a coverage obligation. Keep it, but label it as a statement and not a gate.

## ② U₂

**B1 (resolves LEDGER_PIN_MISSING) — the sealed ledger is identified in the C1b machine receipt §1.1 (blob `bdcafce7`).**
- Phase 1 (producer) seal `phase1_v212s_seal_20260918T222551Z`: `ledger.jsonl` SHA-256 `1e46da3a4ef38409fa1c2130f81cf1125a672b6e44e714f2028a9708cea64b5f`.
- Phase 2 (checker) seal `phase2_v212s_seal_20260920T140743Z`: `ledger.jsonl` SHA-256 `09caf7b9da493aecc922f73f795bc3f4c4321b6cb0598d5b2b08f6c066b76b38`.
- Canonical extract `/home/daybreak/basepoint-geometry-artifacts/C1b/c1b_receipt_extract.json`: SHA-256 `8a332e568838b673c6d45ae934a47794cce3b9e1bb7cad9128dd7a3fcdfde81b`.
- Both ledgers are on the research PC (seal directories mode 555, files mode 444). They are not on GitHub.
- v2 should pin these three SHA-256 values. L0 should then:
  - read both ledgers on the research PC, read-only;
  - check that both give the same Λ and t_plus for every slab;
  - check the totals of 159 accepted slabs and 35 clamped slabs.
- Only the per-slab rows (Λ, clamped flag, t_plus) are read. The method is already fixed in v1, so the order rule still holds.

**B2 (minor).** "t_* は ledger の厳密有理数であることを必須" is correct. Also require that t_plus in the ledger is the same value the C1b checker used for the right wall (both lineages), not a display value.

## ③ Prolate second lineage

**C1 (major) — the input pack must not contain lineage-1's reduction formulas.**
- The manuscript (`4b30c2b2…a257`) contains the derived kernels: the h-derivative chain (for example the h₁(36ℓ² − 120ℓ + 105) term), the Q, H₄ and Q_z integrands, and F_z″(0).
- These are lineage-1's results. A pack holding "the definitions from the manuscript" would hand them to the second lineage. That defeats C/P3.
- Fix: the pack contains only the primary objects:
  - the functional E_a (cone-volume weight, h = arccos²);
  - the prolate spheroid and its parametrization;
  - the definitions of Q, H₄ and Q_z as derivatives of the reduced function, not as explicit integrands;
  - the gate statements.
- The second lineage derives the integrands itself. After derivation, and before any numerical comparison, Astra checks symbolically that the derived integrands equal the manuscript's. This equality is a separate gate (C-EQ). A mismatch is CLAIM_MISMATCH, which is not the same as MATHEMATICAL_CONTRADICTION.

**C2 (minor) — which shared libraries are acceptable.**
- Julia's BigFloat and IntervalArithmetic.jl run on MPFR and GMP. FLINT 3 also links GMP and MPFR.
- State in v2 that sharing GMP and MPFR (basic arbitrary-precision arithmetic) is allowed. What is forbidden is the Arb/FLINT ball arithmetic and the integration algorithms.
- Without this sentence, the rule "same core → INDEPENDENCE_FAILED" is ambiguous.

**C3 (note).** q₂ = 1/100 is about 1/9 of lineage 1's lower bound (~0.0886). This leaves a wide margin and is suitable for Tier A.

## All three

**D1 (Judge-level, recorded) — budget units and the shared PC.**
- The CPU budgets add up to 96 + 48 + 120 + 240 = 504 CPU-hours.
- The drafts do not say whether these are CPU-hours or wall-clock hours.
- They do not say which machine runs them, or how they share the 12-core research PC with D5 (150–170 h wall-clock, still waiting for its contract re-ruling).
- Fix in v2: state the unit, the machine, and the scheduling rule relative to D5.
- Installing Julia on the research PC needs your explicit approval when ③ is frozen.

---

**Status: v1 → v2 requested (A1, A2, B1, C1, C2, D1).** In addition, the paper proofs G0 (interchange on [2/5, 9/20] × [1/2, 1)), E1 (two-chart endpoint) and the ③ quadrature lemma each need their own audit before any FREEZE. None of the three can be frozen yet. No computation is authorized.
