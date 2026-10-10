# CHAT AUDIT — C gap ① v5 and combined lemma G0/E1 v1 (2026-10-10)

Baseline: bg-spheroid-family main `32218d78`, STATE v1.12. Previous audit, with the J5 ruling appended: `f8a1f954…03df1`, confirmed by ChatGPT.
No computation was run for this audit. Sources were read on GitHub.

## Overall result

| Document | Verdict |
|---|---|
| ① v5 | CONDITIONAL PASS. J1 and J2 are fixed. ROOT_TARGET_PIN_OPEN is **closed below** (value 1/128). The remaining blockers all come from other documents (G0/E1, approximation degree, the code diff audit, B_ob, 6fba6e4f) |
| G0/E1 v1 | CONDITIONAL — the structure is right. **Several items marked OPEN are already settled in the sources, which ChatGPT did not have.** A source pack is now provided (below). One item is genuinely new work: the explicit south majorant M_S |

The main obstacle in this round is that ChatGPT does not have the source texts ("原典未取得"). The pack in §3 fixes that.

---

## 1. ① v5

- **ROOT_TARGET_PIN_OPEN — closed.**
  - The addendum v2.3 (`5326e2b5`), line 46, sets "ROOT_TARGET = 1/128". The equality case uses the continuation branch (≤) and strict excess uses the relocated branch (>), as stated in lines 154–155.
  - The executed code agrees. At implementation head `85eca228`, both `producer/global_axial_c1b_kernel.py` (`67dda838`) line 34 and `checker/global_axial_c1b_kernel.py` (`4eaca55d`) line 35 contain `W0, PRED_ACCEPT, ROOT_TARGET = Fraction(1, 16), Fraction(1, 64), Fraction(1, 128)`.
  - So the half-width 1/16 and the acceptance bound 1/64 are also confirmed in code. ①'s "半幅 1/16 等は照合前には継承確定としない" can be cleared for these three constants.
- Good: P2 restoration is explicitly forbidden as a behavioural change. The allowed differences are limited to (a)–(e).
- Remaining: the full SHA and path for all 7 code blobs in v6, and the line-by-line diff audit once a ① implementation exists.

## 2. G0/E1 v1

What is confirmed: the logic of §5 is correct. Given a uniform M, |∂_t g| ≤ √2·M, |g − B_ob| ≤ √2·M·(1 − t) (α = 1), and C_Λ = 3M/2 because √2 ≤ 3/2. The draft also correctly says that an endpoint Lipschitz bound does not by itself identify the machine Gt at t = 1.

**L1 — SOUTH_Q_LOWER_BOUND: settled by the source.**
- Lemma 2 of `5afa815f` already proves it for all t ∈ [1/2, 1). On [1, √2], d = s² − δ ≥ 1 − δ = t ≥ 1/2, so q ≥ λ²d² ≥ λ₋²/4. The proof text reads: "d >= 1 - delta >= 1/2, so q >= lambda_-^2 / 4".
- The same argument holds at t = 1 (δ = 0, d = s² ≥ 1).
- With λ₋ = 2/5 this gives **q_* = 1/25**, which is the candidate in the draft. The underlying fact is d ≥ t, not "q ≥ λ₋²t²". Cite Lemma 2 and close this item.

**L2 — NORTH_CONSTANTS: none of the C2 hypotheses needs t near 1.** I read C2 §4 line by line:
- 0 ≤ ρ ≤ 1 and |φ| ≤ 1/λ₋ follow from the scaled identity ρ²(2 − s²) + λ²φ² = 1 with 2 − s² ≥ 1. No t is involved.
- |Â| ≤ 2 + 1/λ₋ follows from Â = (2 − s²)sρ − (1 − s²)φ. No t is involved.
- w ≥ λ₋ comes from the definition of w. No t is involved.
- |H| ≤ 4 holds on [0, 1] for δ ≤ 1/2, i.e. t ≥ 1/2. This is Lemma 2 of `5afa815f`: "|H| <= 2 + 2 lambda_+^2 < 4".
- 1 ≤ R ≤ π/2 and −1 ≤ R_γ ≤ 0 follow from 0 < γ ≤ 1 (Lemma 1).
- q ≤ 2: on the north half, s²(2 − s²) ≤ 1 and λ²d² ≤ λ₊² < 1 because |d| ≤ 1 for t ≥ 1/2.

So the three bounds |T1|, |T2|, |T3| of C2 §4 hold on [0, 1] × [1/2, 1) × [2/5, 5/8] with λ₋ = 2/5 and λ₊ = 5/8 substituted. The proof document still has to write out each step and the resulting rational upper bound for M_N. This audit only confirms that no hypothesis fails.

**L3 — SOUTH_MAJORANT: genuinely new (C2 gives only existence).**
- C2 §5 says only "a finite compact-set bound M_S". No explicit constant is given there.
- For E1, C_Λ must be an explicit rational number. Derive explicit bounds on [1, √2] × [1/2, 1] × [2/5, 5/8] from:
  - q ≥ 1/25, so √q ≥ 1/5;
  - ρ = s/√q ≤ 5√2;
  - |φ| ≤ 1/λ₋ (the scaled identity still holds);
  - |Â|;
  - |H| ≤ 1/4 + λ₊² < 1 (Lemma 2, south part);
  - √q ≤ √(1 + λ₊²·4) (bound d ≤ 2);
  - and then T1–T3.
- This is the one estimate that is new. Coarse is fine; it only has to be finite, explicit and correct.

**L4 — ENDPOINT_GT_LIMIT.** The argument of C2 §6 (a pointwise limit for every fixed s > 0, then dominated convergence with the uniform majorant) carries over once L2 and L3 give one majorant on the closed range t ∈ [1/2, 1]. Write it out; nothing new is needed.

**L5 — GT_IDENTIFICATION: the code is now in the pack.** Compare the T1–T3 term by term with the two kernels.

## 3. Source pack for ChatGPT (attached, read from GitHub by chat)

| file | origin | SHA-256 |
|---|---|---|
| `OBLATE_ENDPOINT_C1_LEMMA__5afa815f.md` | bg-oblate-spheroid `design/d-ob-p2`, blob `5afa815ff24760ab5ebbb63bcbae912c9c7a84c6` | `74e7dfe253e9f196e7f0ab583527962a4bb808cb77d5b54f449a9acef780e4f6` |
| `MONOTONE_TUBE_C2_INTERCHANGE_LEMMA__7cb9b809.md` | same branch, blob `7cb9b8091596510203d74e09387bc1e8188b8b47` | `92ebb4479cbc7d0c9e79f11bc57f20e9208b74a5de91b3d13091cb5152e8a45b` |
| `GLOBAL_AXIAL_C1B_PREDICTOR_SELECTION_ADDENDUM_V2_3__5326e2b5.md` | same branch | `50df503f165644c5fa5ddb37fb7f07dd28596ef9983aa1be694e8e0de7b56ac2` |
| `producer_global_axial_c1b_kernel__67dda838.py` | `85eca228`:producer/global_axial_c1b_kernel.py, blob `67dda838369302010ef3d589937b834b96ede4d8` | `4244976c708c0ee034536b634b73aa85d2efb3e33ae48ab6797c564ef0bba5e9` |
| `checker_global_axial_c1b_kernel__4eaca55d.py` | `85eca228`:checker/global_axial_c1b_kernel.py, blob `4eaca55ddf79b437fc756d666294372e5d1a6ba4` | `b45caaa3e124c39e5af9d00ce70d670439f0d79f405feb6696ab5313cf28d0bb` |

Both lemma files have the status EXTERNAL_AUDIT_PENDING / NOT_BINDING. G0/E1 inherits that condition.

---

**Status:** ① v5 → v6 (pins only; ROOT_TARGET = 1/128 recorded). G0/E1 v1 → v2: cite L1, write out L2, derive L3 explicitly (the only new mathematics), write out L4, and do the L5 table using the pack. Nothing is frozen. No computation is authorized.
