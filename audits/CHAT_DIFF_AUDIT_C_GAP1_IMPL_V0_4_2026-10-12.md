# CHAT DIFF AUDIT — C gap ① implementation v0.4 (2026-10-12)

**Auditor.** chat, the sole auditor.

**Object.** `submissions/2026-10-12/C_GAP1_IMPL_V0_4_SUBMISSION_2026-10-12.tar.gz`, in main commit `766a1de3` (its parent is `e08e9849`).
- SHA-256 `834642ae5e91add9ea56f6736451bd99c767560b226f68ded7a33b7c7aa91276`. MANIFEST checks.
- `v0_3_reference/` is byte-identical to the v0.3 submission (`2ec6e70f`).

**Authority.** `drafts/2026-10-12/C_GAP1_CONTRACT_V8_DELTA_AND_IMPL_V0_4_INSTRUCTION_2026-10-12.md` (`029a441a`).

**Method.** Static reading; nothing was executed. chat diffed v0.3 → v0.4 itself and checked each changed field against contract v8.

## 1. Scope of change
- Both kernels: +19/−10. The changes in the producer and checker kernels are identical.
- Both gatings: +7/−7.
- driver, producer.py, checker.py: 0.
- All changes are DIFF-K or DIFF-E. No protected body changed, and `attempt_x` / X code is unchanged.

## 2. Checks: PASS
- **Region boundary.** `GAP1_X_HI = 703/1600` and `GAP1_REGION_SLABS = 118/8/34`. Region assignment (`gap1_region`), the header `regions`, and control c2 / c6 all follow these values.
- **Separation of boundary and C1a point.** The new constant `GAP1_C1A_POS_POINT = 281/640` is used in all gating roles:
  - `C1A_GATING_SIGNS`, control c5, and the overlap sign check.
  - The C1a receipt pin check (the 281/640 POS text) is unchanged.
  - The new control C20 checks that the boundary and the C1a point are different values.
- **§11.2 boundary check.** It is done at `GAP1_X_HI` = 703/1600, and the field is renamed `lambda_703_1600`. The sign check uses the C1a point, which is correct: by gate D, g(1/2)>0 at 703/1600.
- **Authority pins.** The 4 new entries equal the values chat measured on main: 029a441a, 12020dd5, 4f198cb4, and run2 SHA256SUMS a623d268.

## 3. Finding V04-1 (blocking; fixed below)
- **Defect.** In both gatings, the run-ledger header still has `"ownership": {"699/1600": "X", "281/640": "R", …}`.
- **Why it blocks.** Under v8 the canonical owner of the R/X boundary is λ = 703/1600. This ledger field therefore misstates the contract, and a misstated contract field counts as a mathematical finding under the process rule.
- **Fix.** Replace `"281/640": "R"` with `"703/1600": "R"`. That is 1 line in each gating, and nothing else changes.

## 4. v0.4.1 = v0.4 + the V04-1 fix (defined byte-exactly by chat)
- chat applied exactly this edit to the v0.4 `new_files/` and computed the blobs below.
- If ChatGPT's v0.4.1 matches all 25 blobs, that identity **is** the audit of v0.4.1, and no further audit round is needed.
- The v0.4.1 file SHA-256 values are:
  - producer gating `3842a733…`
  - checker gating `f1ec413d…`
  - producer kernel `8ec189de…`
  - checker kernel `9847770d…`
  - all other files are unchanged from v0.3.

**RUN_COMMIT blob table (25), branch `run/c-gap1-v0-4` from `85eca228`:**

| path | git blob |
|---|---|
| gap1_analysis/c1b_resumable_driver.py | f381ae6849670f02f2c1b4d86442e3df6c6a299d |
| gap1_producer/global_axial_c1b_gating.py | 703ea0e00d5ffb130d938c8d3fdceb2425b523ca |
| gap1_checker/global_axial_c1b_gating.py | 812a8cb8724f641fc79d0e6c96bf1e0fb84b6182 |
| gap1_producer/global_axial_c1b_kernel.py | 142f962aad1bf657f885e8bd2814d4132ce47c58 |
| gap1_checker/global_axial_c1b_kernel.py | a3591e0d7591b6eae49093d0b0564eb1e3b8ed38 |
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

## Verdict
- **v0.4:** FAIL on V04-1 only.
- **v0.4.1 (as defined in §4):** PASS (static).

Per the Judge's 10/12 ruling, ChatGPT then proceeds without a further ruling:
1. build RUN_COMMIT with the 25 blobs above;
2. run the X diagnostic on [281/640, 703/1600] (NOT_EVIDENCE); on FAIL, stop and report;
3. run3 under FREEZE instruction v1, steps 0–6.

The NOT_VERIFIED runtime items are still covered by those steps.
