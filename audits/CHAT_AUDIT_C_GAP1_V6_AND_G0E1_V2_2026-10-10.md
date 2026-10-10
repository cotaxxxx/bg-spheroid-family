# CHAT AUDIT — C gap ① v6 and combined lemma G0/E1 v2 (2026-10-10)

Baseline: bg-spheroid-family main `32218d78`, STATE v1.12. Previous audit: `c2e63b3a…a629`.
No numerical computation was run for this audit. The inequalities below were checked by hand, and sources were read on GitHub.

## Overall result

| Document | Verdict |
|---|---|
| ① v6 | **PASS as contract text.** The seven 40-digit blob IDs match the C1b receipt §1.2 exactly. ROOT_TARGET, W0 and PRED_ACCEPT are recorded correctly. What still blocks FREEZE lies outside this document: the ① implementation and its diff audit, G0/E1, the approximation degree, the B_ob sign gate, and 6fba6e4f |
| G0/E1 v2 | **The arithmetic of §2–§4 is CHAT AUDIT PASS line by line (M_N = 1000, M_S = 1304000, C_Λ = 1956000).** Still conditional on three things: (i) the C2 identity G_t = T1 + T2 + T3 itself, which is inherited and not yet re-derived (P1 below); (ii) the external audit of the two source lemmas; (iii) the machine Gt identification. The source code for (iii) is now provided |

---

## 1. G0/E1 v2 — line-by-line check

**Definitions** (§1):
- w² = λ²s²(2 − s²) + μ² equals the source definition w² = λ²(1 − μ²) + μ², because 1 − μ² = s²(2 − s²). ✓
- R_γ = (γR − 1)/(1 − γ²). Derived independently: dR/dγ = −(1 − γR)/(1 − γ²). ✓ Its range is [−1, −1/3] (−1 at γ = 0, −1/3 as γ → 1), so |R_γ| ≤ 1. ✓
- π/2 ≈ 1.5708 ≤ 11/7 ≈ 1.5714. ✓
- w ≥ λ₋: w² = λ²(1 − μ²) + μ² ≥ λ² because λ < 1. ✓
- T1, T2, T3 are transcribed exactly from C2 §3. ✓

**North half** (s ∈ [0, 1], t ∈ [1/2, 1), λ ∈ [2/5, 5/8]):
- ρ ≤ 1, |φ| ≤ 1/λ ≤ 5/2, and |Â| ≤ 2·1·1 + 1·5/2 = 9/2. ✓
- |H| < 4 (Lemma 2, valid for δ ≤ 1/2). ✓
- d ∈ [−1/2, 1], so q ≤ 1 + 25/64 < 9/4 and √q < 3/2. ✓
- |T1| ≤ 4·(11/7)·(5/8)·1·4/(2/5) = 39.29 < 40. ✓
- |T2| ≤ 2·1·(25/64)·16·(9/2)·1/(4/25) = 351.56 < 352. ✓
- |T3| ≤ 2·(11/7)·(125/512)·(9/2)·1·[30 + 3]/(2/5) = 284.9 < 300. ✓
- Sum < 692 ≤ M_N = 1000. ✓

**South half** (s ∈ [1, √2]):
- d ≥ t ≥ 1/2, so q ≥ 1/25 (Lemma 2 of `5afa815f`). ✓
- ρ ≤ √2·5 = 5√2; |φ| ≤ 5/2; |Â| ≤ 1·√2·5√2 + 1·5/2 = 25/2. ✓
- H ∈ [−1/4, λ²], so |H| ≤ 41/64 holds. The sharper value is 25/64, but the bound used is valid.
- q ≤ 1 + 4·(25/64) = 41/16, so √q < 2. ✓
- ρ³ = 250√2 ≈ 353.6 < 375, and ρ⁵ = 12500√2 ≈ 17677.7 < 18750. ✓
- |T1| ≤ 4·(11/7)·(5/8)·375·1/(2/5) ≈ 3683 < 4000. ✓
- |T2| ≤ 2·(25/64)·1·(25/2)·18750/(4/25) ≈ 1,144,410 < 1,200,000. ✓
- |T3| ≤ 2·(11/7)·(125/512)·(25/2)·375·[7.5 + 2]/(2/5) ≈ 85,422 < 100,000. ✓
- Sum < 1,304,000 = M_S. ✓

**§4:** M = 1,304,000, and √2·M ≤ (3/2)·M = 1,956,000 = C_Λ. ✓ The left-derivative-only claim at t = 1 is stated correctly. Treating s = 0, t = 1 as a measure-zero point is legitimate, because the scaled bounds hold uniformly as q → 0 (ρ ≤ 1 on the north half for every q > 0).

**P1 (remaining mathematical condition) — the identity G_t = ∂_t F_t = T1 + T2 + T3 is inherited from C2 §2–§3 (EXTERNAL_AUDIT_PENDING).**
- v2 transcribes it correctly but does not re-derive it.
- Every majorant above is a majorant of T1 + T2 + T3. If the identity had an error, the bounds would bound the wrong function.
- The identity is algebra in (s, t, λ) together with R, R_γ. An exact symbolic check would settle it. See the question to the Judge.

**P2 (practical, recorded) — C_Λ = 1,956,000 is valid but too coarse for clearing boxes.**
- The term |g − B_ob| ≤ C_Λ(1 − t) is smaller than a margin of order 10⁻² only when 1 − t ≲ 5·10⁻⁹.
- Most of the work near t = 1 must therefore be done by direct enclosure of Gt on boxes that reach t = 1. G0/E1 makes this legitimate, because it gives a uniform majorant up to t = 1 and the left derivative at t = 1. The band's Claim 1 did the same on [63/64, 1].
- ① and ② must say this in their contracts before FREEZE. They must not leave it to be chosen during a run.
- Optional improvement (not required): use (2 − s²)ρ² ≤ 1 to sharpen the south ρ⁵ term, which dominates M_S.

## 2. Machine Gt identification — the missing modules are now provided

The kernels import `_gt_corner` and `_gt_ordinary` from other modules. Below is the full local import closure of those modules at implementation head `85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b`, read on GitHub. It also includes the g-density module `_g_density_stable` (v2) for the F_t identification.

| blob (40) | path | SHA-256 |
|---|---|---|
| c2fee40053ab055ce352e93e1c6d1fc43e46310a | producer/monotone_tube_refinement_producer.py | 976bb944…406b |
| b6d96df223c0e423e804d96f4892a8e818c05827 | producer/monotone_tube_interval_producer.py | 0c23fddb…988b |
| 51060fea01cb9ff661518b7c52146f71187846ff | producer/endpoint_interval_producer.py | 19e37471…4f7b |
| 29d441a578f10fe7f4beb38476d3699f3648a3b1 | producer/global_axial_c1b_endpoint_r.py | 2eafc554…138a |
| c4c8d6b59d3829e1843d149b7857eda5800287aa | producer/global_axial_c0_producer.py | 57407a56…1769 |
| cdbdf51f8656c1fcae97666cc1846461b250a591 | producer/global_axial_c0_producer_v2.py | bce25515…fa3c |
| 15d660265552fc2f2c83ffe897ed5efab8514da2 | checker/monotone_tube_refinement_checker.py | 0e9db85c…f90c |
| f2fa2a5a42d35b8b77e3c63fa0d9ad48ce562a77 | checker/monotone_tube_interval_checker.py | d13fad74…499f |
| 4cb16f8a975e5a3be601a7926af695ad5be57790 | checker/endpoint_interval_checker.py | fd1a5739…4f2 |
| 2bddddf6e9a08ca7acae94c89bd4d5ab1de861bc | checker/endpoint_local_checker.py | b5113748…ee19 |
| c913c47d228e51a15f56957f5df9196efa1b22c3 | checker/endpoint_local_controls.py | 976df829…d4ed |
| df402583c320c459ff4f72dc5294558f14f44d31 | checker/oblate_axis_prototype.py | d6dc04d2…b6001 |
| 1a953b22c12a89afc06790b28d6b0dea9680dc43 | checker/global_axial_c1b_endpoint_r.py | b07252df…54ec |
| 85978625e029b01c8ae40fa8234566f10eea251c | checker/global_axial_c0_checker.py | e2011b6d…01bf |
| fbec890588d2d390ea67bc90116b80bb37ebf9cc | checker/global_axial_c0_checker_v2.py | 01654028…e2db |

The full SHA-256 values are in `MANIFEST.txt` inside the pack.

The identification table should, for each lineage:
- locate T1, T2 and T3, or an algebraically equivalent grouping;
- state the corner/ordinary switch condition, and show that both branches enclose the same G_t;
- state how R and R_γ are evaluated near γ = 1 (endpoint_r modules).

## 3. ① v6

No findings. The blob table matches receipt §1.2 entry by entry. Section 6 is accurate: nothing has been ported yet, and the diff audit has NOT_STARTED.

---

**Status:**
- ① v6: text final; waiting for the implementation.
- G0/E1 v2: arithmetic PASS; conditional on P1, the source-lemma audits, and GT identification.
- ② v3: unchanged.

Nothing is frozen. No computation is authorized.
