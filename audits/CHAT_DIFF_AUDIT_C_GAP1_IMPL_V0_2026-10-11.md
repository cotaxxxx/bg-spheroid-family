# CHAT DIFF AUDIT — C gap ① implementation submission v0 (2026-10-11)

**Object.** `C_GAP1_IMPL_V0_SUBMISSION_2026-10-11.tar.gz`
- SHA-256 `d4ddd33db5a024a930dd3cfef21aa2b9bcd5c37e4cb5f536f02c75147156d6e8`, 189479 bytes. Received as the Judge's attachment.
- `MANIFEST.sha256` `7bbb656c…691c`. All 31 entries check.

**Authority.** Instruction v2 `48204988` with issue note `51a167c7` (main `e34f6a09`), contract v7 `a4914818`, numeric contract v1 `be67046f`, import record `b48887c1`.

**Independence.** chat wrote this before ChatGPT's diff audit was available, as issue note N3 requires. It is held unsaved and committed only by its SHA-256 until ChatGPT has submitted.

**Method.**
- Static reading only. No submitted code was imported or executed.
- chat generated its own `diff -u` of each of the 7 new files against the baseline at bg-oblate-spheroid `85eca228`, so Code's diffs were not relied on.
- It read every hunk of the producer kernel and the producer gating. For the checker kernel and the checker gating it compared their added and removed lines against the producer's, and read every difference.
- Relevant baseline functions were read in full: `g_box`, `_tube_gt_eval`, `tube_stage`, `_e0_counts`, `exterior_seed`, `exterior_cover`, `eval_exterior`, `mono_closure_box`, `_mono_truth`, `_attempt_with_tc`.

## 1. Pins
- **Baseline 7 files.** Their blobs at `85eca228` are 67dda838, a93ca173, 0616fbd7, 5fd308bb, 4eaca55d, 03df2620 and 0760764e, matching v7 §8.1.
- **New-file names.** The new files are `gap1_producer/`, `gap1_checker/` and `gap1_analysis/`, with the baseline basenames, as v2 §1.5 requires.
- **Authority hashes.** All 9 values in `GAP1_AUTHORITY_SHA256` were recomputed from main. All 9 match, including `b48887c1…44d4`, which Code had at first filled in from memory and then corrected.
- **Import pins.** `GAP1_IMPORT_CLOSURE_17` equals chat's computed closure, `audits/importclosure/closure_85eca228_blobs.txt`. The driver's `REQUIRED_C1B_BLOB_PATHS` lists the new 7 files plus all 17.
- **C1a receipt.** It is present at `85eca228` with blob `e494e789…`, and all 5 required strings occur in it exactly once. `C1A_GATING_SIGNS` is ((699/1600, −1), (281/640, +1)), and gate D is as in E3.

## 2. Hunk content, compared with the allowlist (v7 §8.2)

| File | What changes | Category | chat finding |
|---|---|---|---|
| producer and checker kernel | `MAX_ACCEPTED`/`MAX_ATTEMPTED` 1280/2400; work ceilings 61.44e9/32.768e9 | K | Match numeric contract v1 |
| producer and checker kernel | `GAP1_*` domain, region, X stage, endpoint, C1a and pin constants; `gap1_region`; `gap1_coarse_slabs`; `c1a_preflight`; `gap1_domain_controls` | K | Exact rationals. 118/7/35 slabs; shared edges are not split |
| producer kernel | `coarse_ledger` returns the 160 slabs in decreasing λ | A | The checker kernel has no queue; its gating audits the order instead |
| both kernels | `x_lower_tube`, `attempt_x` | B | Lower block [1/2,5/8] with stages X-T0/1/2 equal to T0/1/2. A cell is good only if `gt_box` is finite and its upper bound is < 0 (the baseline `_tube_gt_eval`). Negative block: `exterior_cover(slab, 1/2, 5/8)` gives `_e0_counts` = (0, 24), so only R-side boxes on [5/8, 31/32], each needing g upper < 0. No predictor, root localization or wall |
| both kernels | `attempt_l` | C | `exterior_cover(slab, 1/2, 1/2)` gives (0, 24) R-side boxes on [1/2, 31/32], each needing g upper < 0. No predictor or root |
| both kernels | `endpoint_partition`, `endpoint_gate` | D | Exactly as ruled (S1). One seed `g_box(31/32, 31/32)` with 8192 panels; 16 `gt_box` calls on t_j = 31/32 + j/512, 8192 panels each; U_cum = seed_upper + Σ (1/512)·max(0, U_j) in ball arithmetic, with the outward `.upper()`; the only PASS is U_cum < 0. Any non-finite value, guard or missing box is a FAIL. There is no direct g inside (31/32, 1), no C_Λ, no B_ob and no t-refinement. With 8192 panels the ordinary chart meets S1's conditioning bound (√2/8192 < (2/5)/512) |
| both kernels | `attempt_gap1` / `attempt_replay_gap1` dispatcher | E | R runs the baseline `attempt` (producer) or `attempt_replay` (checker) unchanged, then the endpoint gate; a right-clamped R tube is refused. L and X run their own bodies, and the checker requires `expected_tc` to be None for them. Every region must then pass the endpoint gate |
| both gatings | `gap1_serialize_record`, `gap1_exact_union`, `gap1_boundary_overlap`, plan-order audit (checker), L/X null-field checks, header | E / K / A | Union is sorted by λ_lo. Owners: 699/1600 X, 281/640 R (T_* must meet (1/2, 5/8)), 9/20 consistency only. Replay schema renamed |
| both gatings | REFINE inserts `[right, left]`; `previous_root` is None for root-free accepts | A | R continuation is the midpoint of the right neighbour's accepted T_*: correct under the decreasing order with right child first. REFINE does not update `previous_root` (baseline) |
| driver | Pins path, chain version, required blob list (7 + 17) | E/K | Non-numeric only (v2 B2) |
| producer and checker entry points | Imports switched to `gap1_*` | E | — |

- **No change to protected bodies.** The change lines touch none of `g_box`/`gt_box`, the T1/T2/T3 charts, P1/P2, `root_localize`, `predictor_accept`, `exterior_cover`/`eval_exterior` or the interval code. chat listed every `-` line in all 7 diffs. The only removed lines are:
  - the cap and ceiling constants;
  - the body of `coarse_ledger`;
  - the import lines;
  - the union blocks;
  - the REFINE insertion order;
  - the `previous_root` line;
  - the replay schema name;
  - the coarse counts in the work estimate and the header;
  - the domain print line;
  - the call sites `kernel.attempt`, `kernel.attempt_replay` and `serialize_record`, now routed through the dispatchers;
  - the checker's `verify_a1_fields` call (now R-only), its `root is None` test and its `root_outcome` test (now also allowing `ROOT_FREE_REGION` for L/X);
  - the driver's pins path, chain version and 7-path list.
- **No ① path uses the baseline domain constants.** The ① code uses `L_LO`, `L_HI`, `DLAM` and `N_COARSE` only in the reference-domain print line.

## 3. Soundness of reused machinery (Q3 bears on it)
- **Mono closure.** `eval_exterior` closes an R-side box by mono closure only if `gt_box(tp, box.tr)` has upper < 0 and the certified wall `g_box(tp, tp)` has upper < 0. On L (tp = 1/2) and on X (tp = 5/8), the interchange ∂_t g = ∫G_t needed for this holds on [1/2, 1) × [2/5, 5/8] by G0/E1 v3. So mono closure is **sound** in both regions.
- **What the contract says.** For L, numeric contract v1 §4 lists `MONO_WORK_CAP`. For the X negative block, §5 does not mention it.

## 4. Static controls
- Two SHAs of `static_controls.py` were recorded before running: the first run `7c53607b`, and the final `b0fe7331`.
- The run1 and final outputs differ only in C7's sub-check "no B_ob/C_Lambda/root path". chat read `endpoint_gate`: the terms appear only in a comment. So the C7 PASS is legitimate, and the control was not weakened in any way that matters.
- chat did not re-run Code's scripts. Its findings above come from its own reading and its own diffs.

## 5. NOT_VERIFIED (static analysis cannot settle these)
- At run time, do the `gap1_*` namespace packages and `importlib.import_module(lineage + ".global_axial_c1b_gating")` resolve to the ① gating?
- `Path`-relative receipts need the working directory to be the repository root, as in the baseline.

Both need a non-numeric import test. Running it needs Judge permission.

## 6. Open questions (Code's Q1–Q6): chat's recommendation, ruling deferred until both audits are in
- **Q1, pin manifest.** Generate `gap1_analysis/GAP1_RESUMABLE_PINS.json` on the research PC at the execution-preparation stage, with a script that chat writes and audits. It hashes only, and runs no numerics. This is not a FREEZE blocker.
- **Q2, `python -m` from the repository root.** Accept. It is the same convention as the baseline.
- **Q3, mono closure in the X negative block.** Accept and bind by record, with `MONO_WORK_CAP` as for L. It is sound by G0/E1 v3 (§3), and it is the unchanged baseline exterior machinery that v7 refers to.
- **Q4, R right clamp.** Accept as implemented. A clamped R tube never ACCEPTs: it is recorded and refined or failed. In R, t_c ≤ 5/8 makes a clamp unreachable unless the predictor is broken.
- **Q5, all 160 slabs in decreasing order.** Accept. The order only matters for R, and L/X use no predictor.
- **Q6, separate `GAP1_*` constants with the C1b reference constants kept.** Accept. The baseline self-test controls keep their domain, and no ① path uses the old constants (§2).

## Verdict
**chat diff audit: PASS (static).**
- All hunks are within A/B/C/D/E/K. The protected bodies are unchanged. The endpoint gate is exactly the ruled cumulative form. L and X cannot reach the predictor or root code. The checker independently recomputes, apart from the allowed replay labels and t_c. The pins all match.
- **Conditions before FREEZE review:**
  1. ChatGPT's independent diff audit;
  2. Judge rulings on Q1–Q6;
  3. the Judge's execution-order ruling.

The NOT_VERIFIED import test needs separate Judge permission. Nothing is frozen, and no execution is authorized.

---

## 7. Collation with ChatGPT's independent audit, and Judge rulings (2026-10-11, added after both audits)

- Sections 1–6 above were committed by SHA-256 `94ee8ff9…` before chat read ChatGPT's audit.
- **ChatGPT's audit:** `CHATGPT_PREAUDIT_FAIL (F1–F3)`, relayed as text with SHA-256 `1e1cf5e0…3c7f`.
  - ChatGPT's own SHA, baseline, 17-pin and protected-body checks agree with chat's sections 1 and 2.
  - ChatGPT independently verified that every protected function is AST-identical.

| ID | ChatGPT finding | chat's re-check | Status |
|---|---|---|---|
| F1 | The X negative block can ACCEPT through baseline mono closure. v2 §4.2 and numeric contract v1 §5 specify direct `g_box<0` only, and §5 lists no MONO cap | Confirmed (`exterior_cover` → `eval_exterior` → `mono_closure_box`). chat had seen this (§3, Q3) but judged it acceptable because it is sound. **chat withdraws that recommendation.** A method the frozen contract does not name is a contract deviation, however sound | **Blocking.** Judge ruling below |
| F2 | The checker records `ROOT_FREE_REGION` for X. But X has one simple root in (1/2,5/8) wherever g(1/2,λ) > 0 (v7 §5.2) | Confirmed (checker gating L725–727). **chat missed this (CHAT-DIFF-001).** | Blocking. Fix in v0.1 |
| F3 | A slab whose attempt passes but which is then stopped by a cap is written with `decision=ABORT`, `reason=PASS` and `failure_class=None`. The ledger never says RESOURCE_CAP | Confirmed (producer gating L708–723; the reason/decision pair is baseline behaviour, but ① added `failure_class` and its comment claims RESOURCE_CAP). **chat missed this (CHAT-DIFF-002).** | Blocking. Fix in v0.1 |

**chat's corrected verdict: v0 does not pass.** The "PASS (static)" in the Verdict section above is withdrawn. chat's static method checked conformance of the hunks and protected bodies, but it did not check the semantics of the ledger labels against v7, nor the cap paths. From now on chat's diff audits will include a pass over every machine-readable ledger field against its contract meaning.

**Judge rulings (2026-10-11).**
1. **F1: "契約どおり直接のみ" (direct only, as the contract says).** The X negative block [5/8,31/32] is closed by direct `g_box` upper < 0 only, using E0 24×8 and panels 1024→2048→4096 under E_BOX_CAP. Mono closure is not available in X: an unresolved box ends as `CERTIFICATE_INCONCLUSIVE`. In L, mono closure stays allowed, because numeric contract v1 §4 lists MONO_WORK_CAP for L. Its soundness rests on G0/E1 v3 (§3).
2. **"推奨どおりでv0.1" (v0.1 as recommended).** Code submits v0.1 containing:
   - F1 as ruled;
   - F2: L is `ROOT_FREE_REGION`; X gets a label that does not mean zero roots (for example `ROOT_COUNT_BY_C1A_SIGN_NO_T_STAR`). The ledger schema documents that X's root count depends on the sign of g(1/2,λ) (C1a with gate D), and the checker's acceptance is changed to match;
   - F3: a cap-driven ABORT records `RESOURCE_CAP` and the cap's name in machine-readable fields, with no PASS/ABORT contradiction, and replay reproduces the same classification;
   - Q2, Q4, Q5 and Q6 accepted as implemented;
   - Q10/Q11: pin `analysis/c1b_cross_lineage_compare.py` (blob `33cdd3290bfa09c88cd8936e1f4557af491f0bc2` at `85eca228`) in the driver's required list, as a pinned read-only file;
   - Q15: add DIFF-K preflight controls for L, X and endpoint that use stubbed `g_box`/`gt_box`. They are code only, and running them needs separate permission;
   - Q1, the pin manifest, is deferred to execution preparation.
3. v0.1 is saved to main and audited independently by ChatGPT and chat. Neither reads the other's record before concluding. FREEZE review follows only if both pass.
