# CHAT AUDIT — three predeclare drafts v2 (2026-10-10)

Baseline: bg-spheroid-family main `32218d78`, STATE v1.12.
Previous audit (v1), full SHA-256: `66f2461d753ca263d7fbdcf6424d1e674f3a8de3dda1489bfbbaafd38f5aaa4b`.
No computation was run for this audit. Sources were read on GitHub only.

## Overall result

| Draft | Verdict | Remaining before FREEZE |
|---|---|---|
| ① U₁ | CONDITIONAL PASS | E2 (the tube rule: a concrete rule is offered below), E3 (status of the λ_x bracket: Judge), plus the declared blockers G0, E1_FORMULA, APPROX_DEGREE |
| ② U₂ | CONDITIONAL PASS | F1 (the full SHA values are given below; the seal path must be confirmed on the PC), plus E1_FORMULA and APPROX_DEGREE |
| ③ prolate | PASS as a framework (no new findings) | The declared blockers INPUT_PACK_OPEN and QUADRATURE_CONTRACT_INCOMPLETE |

v1 findings confirmed as fixed:
- A1: the wrong citation is removed and the claim is stated directly.
- A2: the per-position scheme is in place for the left group.
- B1: the ledger is identified through receipt §1.1.
- C1: the clean-room pack excludes lineage-1 formulas, and gates I0–I4 are added (I2: symbolic comparison before any numbers).
- C2: sharing GMP/MPFR is allowed, Arb/FLINT is forbidden.
- D1: the unit is core-hours; D5 and these runs may not occupy the PC at the same time; the order is decided by the Judge; otherwise SCHEDULING_HOLD.

---

## ① U₁

**E1 (resolves the draft's BOUNDARY_OPEN) — λ = 699/1600 is not λ_x.**
- C1a receipt (`e494e789`), bisection step 3: "699/1600 NEG at 65536 panels". The certified enclosure is F_lo = [−0.002 ± 5.46e−4], entirely below 0.
- So F_x(699/1600) < 0 strictly. Since F_x is strictly increasing on [83/200, 9/20] (gate D), F_x < 0 on [83/200, 699/1600]. Together with C0b on [2/5, 83/200], g(1/2, λ) < 0 on all of [2/5, 699/1600].
- The left group can therefore be the closed set [2/5, 699/1600]. The half-open workaround is not needed.
- This depends on E3.

**E2 (TUBE_RULE_OPEN) — use C1b's own predeclared rule.**
- The C1 crossing/tube contract (`77210a54`) §C1b.4 already holds an audited, deterministic rule:
  - a rational predictor centre t_c on each slab;
  - fixed half-width w0 = 1/16, never narrowed during a gating run;
  - t₋ = max(1/2, t_c − w0) and t₊ = t_c + w0;
  - acceptance requires a certified root enclosure T_* with sup|t_c − T_*| ≤ 1/64;
  - the only allowed repairs are, in this order, exact λ-bisection and then recentring by the predeclared predictor rule.
- Adopt it for the right group [699/1600, 9/20] and cite it by blob. Pin the predictor rule itself as code, by blob.
- On the λ_x box [699/1600, 281/640], the left clamp t₋ = 1/2 applies, and the left wall condition is replaced by the C1a sign of F_x, as the draft already says.
- This brings the method in line with what C1b actually did. All 159 C1b slabs had t₋ > 1/2, a left exterior cover and a narrow tube. It removes the overreach of t_L = 1/2 with t_R = 31/32 for every slab.

**E3 (Judge) — the λ_x bracket is "report-only" in the C1a receipt.**
- The receipt classifies the bisection as "report-only and does not gate existence or uniqueness" ("C1A_REPORTED_CERTIFIED_BRACKET PASS").
- The two endpoint signs are certified enclosures, and the 192-bit checker reproduced them ("same exact bracket [699/1600, 281/640]").
- ① now uses the bracket as a gating input: it decides which group a slab belongs to and where the λ_x box is.
- That is a change of status. Either the Judge accepts the two certified endpoint signs as gating input (the recommendation), or ① must work without the bracket. In that case the λ_x box would be the whole of [83/200, 9/20], which is much harder.

## ② U₂

**F1 (resolves LEDGER_PIN_INCOMPLETE) — the full values from receipt §1.1 (blob `bdcafce7`), read again for this audit:**

| object | SHA-256 |
|---|---|
| Phase 1 seal `phase1_v212s_seal_20260918T222551Z`, `ledger.jsonl` | `1e46da3a4ef38409fa1c2130f81cf1125a672b6e44e714f2028a9708cea64b5f` |
| Phase 2 seal `phase2_v212s_seal_20260920T140743Z`, `ledger.jsonl` | `09caf7b9da493aecc922f73f795bc3f4c4321b6cb0598d5b2b08f6c066b76b38` |
| replay plan `checker_replay_exact.jsonl` (Phase 1 seal) | `c31af672d12981ca08c15464439b8ca81c75f7dd2dd801ad3c78dbbfdffc5b69` |
| extract `/home/daybreak/basepoint-geometry-artifacts/C1b/c1b_receipt_extract.json` | `8a332e568838b673c6d45ae934a47794cce3b9e1bb7cad9128dd7a3fcdfde81b` |

- These are 64-digit values, not prefixes.
- The receipt gives only the seal directory names, not their parent directory. The first step of L0 is to confirm the absolute path on the research PC (`ls`, read-only) and record it. This is an inspection, not a design input.

**F2 (minor) — clarify the clamped-slab sentence.** "clamped slab は既存 tube の閉区間被覆を別途検証" should say that it is a ledger consistency check (t_plus = 1 recorded, right wall supplied by B_ob). It is not a re-proof of C1b, which the draft itself excludes.

## ③ Prolate

Nothing further. The gates I0–I4 and the tiered gates match the rulings. Before FREEZE, two things must exist and be audited:
- the bytes of the input pack (INPUT_PACK_OPEN);
- the validated quadrature contract (QUADRATURE_CONTRACT_INCOMPLETE).

---

## What actually stands between these drafts and a FREEZE

Contract wording is no longer the bottleneck. The remaining blockers are mathematical work products, each needing a draft, an audit and a ruling of its own:

1. **G0** — an interchange lemma for g on λ ∈ [2/5, 9/20], t ∈ [1/2, 1), identifying the machine quantity Gt with ∂_t g. Used by ①.
2. **E1** — the two-chart endpoint estimate |g(t, λ) − B_ob(λ)| ≤ C_Λ (1 − t)^α, or an explicit equivalent. Shared by ① and ②.
3. **The ③ quadrature lemma** — the remainder bounds for the validated integration.

Status: v2 → v3 for ① (E2, E3 per the ruling) and ② (F1, F2). ③ stays at v2 until its pack and quadrature contract are drafted. Nothing is frozen. No computation is authorized.

---

## Judge ruling (2026-10-10, after this audit)

**E3: accepted as a gating input, restricted to the two endpoint signs.** The certified enclosures F_x(699/1600) < 0 and F_x(281/640) > 0, recorded in C1a receipt `e494e789` and reproduced by the 192-bit checker, may be used as gating inputs for ①. The point estimate λ_x ≈ 0.43775487… stays REPORTED_EXPECTATION / NON_GATING. The C1a receipt itself is not edited (version-up only). This ruling is the record of the change of status.
