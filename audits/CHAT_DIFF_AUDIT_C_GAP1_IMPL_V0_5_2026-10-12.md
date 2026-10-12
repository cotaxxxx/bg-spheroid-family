# CHAT DIFF AUDIT — C gap ① implementation v0.5 (2026-10-12)

**Auditor.** chat, the sole auditor.

**Object.** `submissions/2026-10-12/C_GAP1_IMPL_V0_5_SUBMISSION_2026-10-12.tar.gz`, in main commit `71a36948` (parent `924d6de4`).
- SHA-256 `233b2bb1dfcef955cc569b962b9ba0d39231b467e8ba6225b8b7c78a0dd068e8`. MANIFEST checks.
- `v0_4_1_reference/` is byte-identical to the v0.4.1 that chat defined in the v0.4 audit §4.

**Authority.**
- Contract v9.1 delta (`b85f69ae`).
- v9 delta / v0.5 instruction §3 (`472ff013`), with m = 48.

**Method.** Static reading; nothing was executed. chat diffed v0.4.1 → v0.5 itself.

## 1. Scope
- Both kernels: +20/−10, with identical edits in producer and checker.
- Both gatings: +8/−8, with identical edits in producer and checker.
- driver, producer.py, checker.py: 0.
- All changes are DIFF-K or DIFF-E.
- The X and L method bodies (`attempt_x`, `attempt_l`) are unchanged, so the §5.1–5.3 trichotomy of X is unchanged (Astra K1).

## 2. Checks: PASS
- **Region split.** `GAP1_X_LO = 83/200` and slabs 48/78/34. Region assignment, the header `regions`, and controls c2 and c6 all follow.
- **Separation of boundary and C1a point.**
  - A new constant `GAP1_C1A_NEG_POINT = 699/1600` is used in every gating role:
    - `C1A_GATING_SIGNS`;
    - control c5;
    - the §11.1 overlap sign.
  - The C1a receipt pin text ("step 3: 699/1600 NEG") is unchanged.
  - C21 checks:
    - `GAP1_X_LO == 83/200`;
    - `GAP1_C1A_NEG_POINT == 699/1600`;
    - the two are different;
    - the slab counts are 48/78/34 and total 160.
- **§11.1 at λ = 83/200.**
  - Owner is X; L is overlap only. The field is `lambda_83_200`, and the header `ownership` is `"83/200": "X"`.
  - The sign used is that of the C1a NEG point. This is correct: gate D on the closed interval [83/200, 9/20] and F_x(699/1600) < 0 give g(1/2, 83/200) < 0 (v9.1 §1).
- **Stub controls.** The X stub slab index is now 48, the first X slab.
- **Authority pins.** The 4 new entries equal the values chat measured on main:
  - 472ff013
  - b85f69ae
  - 46bae2b5
  - run3 SHA256SUMS bc4dd50e

## 3. Notes (procedural, non-blocking)
- `GAP1_X_ROOT_COUNT_RULE` still says "contract v8 retaining v7 5.1-5.3". The mathematical content is still accurate. Update the wording in the next version.
- Astra K3–K5 (runner and diagnostic wording) are accepted:
  - run4 uses the sequential runner of run3, which stops on any nonzero exit, not the parallel diagnostic runner.
  - The v9 and v9.1 diagnostics (`924d6de4`) are NOT_EVIDENCE.

## Verdict
**v0.5: PASS (static).**

RUN_COMMIT blob table (25), branch `run/c-gap1-v0-5` from `85eca228`:

| path | git blob |
|---|---|
| gap1_analysis/c1b_resumable_driver.py | f381ae6849670f02f2c1b4d86442e3df6c6a299d |
| gap1_producer/global_axial_c1b_gating.py | baffaf4952364cce94411b8982ce57c3a5d7bea1 |
| gap1_checker/global_axial_c1b_gating.py | 36bb7983f2a806ba3d87b7f486aafd22ea1a5184 |
| gap1_producer/global_axial_c1b_kernel.py | 5503bb7da981ef90266a9cdd67de2bef07998fd8 |
| gap1_checker/global_axial_c1b_kernel.py | b4bb44bdf57dc2ec6e5a1b3b262acdfec7e07a39 |
| gap1_producer/global_axial_c1b_producer.py | 34ef3758382de5993116c49d511b5b68e4e87bfa |
| gap1_checker/global_axial_c1b_checker.py | 5b526ddc4f48dc01d3f95eafb44f3d638e2e35ed |
| producer/monotone_tube_refinement_producer.py | c2fee40053ab055ce352e93e1c6d1fc43e46310a |
| checker/monotone_tube_refinement_checker.py | 15d660265552fc2f2c83ffe897ed5efab8514da2 |
| checker/monotone_tube_interval_checker.py | f2fa2a5a42d35b8b77e3c63fa0d9ad48ce562a77 |
| producer/global_axial_c1b_endpoint_r.py | 29d441a578f10fe7f4beb38476d3699f3648a3b1 |
| checker/global_axial_c1b_endpoint_r.py | 1a953b22c12a89afc06790b28d6b0dea9680dc43 |
| producer/endpoint_interval_producer.py | 51060fea01cb9ff661518b7c52146f71187846ff |
| producer/monotone_tube_interval_producer.py | b6d96df223c0e423e804d96f4892a8e818c05827 |
| producer/global_axial_c0_producer.py | c4c8d6b59d3829e1843d149b7857eda5800287aa |
| checker/global_axial_c0_checker.py | 85978625e029b01c8ae40fa8234566f10eea251c |
| checker/endpoint_local_controls.py | c913c47d228e51a15f56957f5df9196efa1b22c3 |
| checker/oblate_axis_prototype.py | df402583c320c459ff4f72dc5294558f14f44d31 |
| checker/endpoint_interval_checker.py | 4cb16f8a975e5a3be601a7926af695ad5be57790 |
| checker/endpoint_local_checker.py | 2bddddf6e9a08ca7acae94c89bd4d5ab1de861bc |
| producer/global_axial_c0_producer_v2.py | cdbdf51f8656c1fcae97666cc1846461b250a591 |
| checker/global_axial_c0_checker_v2.py | fbec890588d2d390ea67bc90116b80bb37ebf9cc |
| producer/c0a_four_group_v2.py | 2bb556ab4f0c0cfd9ce6afa65d762551dd3791f4 |
| checker/c0a_four_group_v2.py | 18e66b6450cd2a379bbb869a99e4e5ce6999f6e5 |
| analysis/c1b_cross_lineage_compare.py | 33cdd3290bfa09c88cd8936e1f4557af491f0bc2 |

ChatGPT then proceeds without a further ruling:
1. Build RUN_COMMIT. All 25 blobs must match the table above.
2. Run run4 under FREEZE instruction v1, steps 0–6, using the sequential runner.
3. Apply the preflight check of run3: the 4 items, plus the lines containing FAIL compared lineage by lineage with run2.

Report only a STOP or the completed push.
