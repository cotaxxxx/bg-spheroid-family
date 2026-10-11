# CHAT DIFF AUDIT — C gap ① implementation submission v0.1 (2026-10-11)

**Object.** `C_GAP1_IMPL_V0_1_SUBMISSION_2026-10-11.tar.gz`
- SHA-256 `df2a691585e0aebf7558f0e9cf0de1dfd2b55949fcff41c586173e172fb70077`, 271429 bytes. Received as the Judge's attachment.
- `MANIFEST.sha256` is `acdf7cfd…a691`; all 40 entries check.

**Authority.** Instruction v2 `48204988` with issue note `51a167c7`, and v0.1 instruction `f8f436f3` (Judge rulings in `bbba3f04` §7). Main is `d9457b2a`.

**Independence.** Written before ChatGPT's v0.1 audit was seen. Held unsaved; only its SHA-256 is disclosed until both audits are in.

**Method.**
- Static reading only; nothing in the submission was imported or executed.
- chat regenerated its own diffs, baseline (`85eca228`) → v0.1 and v0 (`d4ddd33d`) → v0.1, and did not rely on Code's diffs.
- New this time (after CHAT-DIFF-001/002): a pass over every machine-readable ledger field touched by v0.1, checked against its contract meaning.

## 1. Scope of change, v0 → v0.1
- Kernels: +179/−8 each, with identical change text in producer and checker.
- Gatings: producer +136/−7, checker +163/−19.
- Driver: +1 line (the pinned path of compare.py).
- Entry points: unchanged.
- The **lines removed from the baseline**, compared with v0, are all cap or replay wiring in the two gatings: the old unrecorded `raise` exits, the `check_ceiling` calls, the checker's old root_outcome/ACCEPT test and its `replay_state` signature. No kernel body was removed. The protected bodies are unchanged as in v0, including `exterior_cover`, `eval_exterior` and `mono_closure_box`.

## 2. F1 — X negative block is direct-only (DIFF-B)
- `x_negative_seed` places 24 t-boxes on [5/8, 31/32] × 8 λ-boxes, all R-side.
- `x_negative_eval` resolves a box only if `g_box` is finite with upper < 0. It does not call `gt_box`, uses no wall and no mono closure.
- `x_negative_cover` runs the E_STAGES ladder 1024 → 2048 → 4096 with baseline `e_children` refinement and E_BOX_CAP; anything left unresolved FAILs.
- `attempt_x` now calls `x_negative_cover`, not `exterior_cover`.
- The names it uses (`e_children`, `EBox`, `_checked_finite`, `_nonfinite_record`, `split`, `E_STAGES`, `E0_*`) exist in both kernels, so the checker uses its own independent evaluators.
- L still uses baseline `exterior_cover` with mono closure, as ruled.
- **PASS.**

## 3. F2 — root-count labels (field-semantics pass)
- `GAP1_ROOT_COUNT_LABELS`: L `ROOT_FREE_REGION`, X `ROOT_COUNT_BY_C1A_SIGN_NO_T_STAR`, R `RESOLVED_WITH_CERTIFIED_T_STAR`.
- `gap1_root_outcome` gives a region label only when the whole attempt holds (`attempt_reason == PASS`, body plus endpoint); otherwise `UNRESOLVED`. R additionally needs T_* at TARGET_WIDTH.
- `root_count`: L is 0 when certified. **X is always null**, with the rule "0 roots in U₁ if g(1/2,λ) ≤ 0, one simple root in (1/2, 5/8) if > 0, sign from C1a with gate D, no λ_x". R is 1 when certified.
- This matches v7 §5.1–5.3, including g(1/2) = 0 giving 0 roots in U₁.
- The checker accepts a plan ACCEPT only when its own outcome equals the region label, so an unresolved attempt stops with `CHECKER_REPLAY_UNRESOLVED`.
- The schema document (§2, §2.2) states the same, and explicitly says the X label does not mean no root.
- **PASS.**

## 4. F3 — resource-cap stops (field-semantics pass)
- `gap1_cap_exceeded` tests the caps in a fixed order: global work, MAX_ACCEPTED, accepted work, MAX_ATTEMPTED; a cap is exceeded when value > ceiling. MAX_ATTEMPTED is tested with attempted + 1 before each attempt, which is equivalent to the baseline's `attempted >= MAX`.
- `gap1_mark_decision`, when a cap applies, sets:
  - `reason = RESOURCE_CAP:<cap>`
  - `failure_class = RESOURCE_CAP`
  - `abort_cause = RESOURCE_CAP`
  - `resource_cap = <cap>`
  - `root_count.accepted = false`

  The attempt's own reason and class are kept in `attempt_reason` and `attempt_failure_class`.
- An ABORT with no cause is a `CONTRACT_MISMATCH`. A checker attempt that passes while the plan ABORTs with no cap is recorded as `CONTRACT_MISMATCH:PLAN_ABORT_NOT_REPRODUCED`, never as PASS.
- segment_end carries the same fields. After a cap stop the run raises `RESOURCE_CAP:<cap>`.
- Resume and replay re-derive the classification from the stored counters (`gap1_terminal_abort`), require it to match, and refuse to resume past a terminal ABORT.
- Every path chat traced (live producer, live checker, start of resume, plan ABORT in the checker) yields no record with reason PASS and decision ABORT.
- A cap-stopped checker record can have `decision = ACCEPT` together with `checker_decision = ABORT` (B2). chat checked that this cannot reach the union: the checker raises before `gap1_exact_union`.
- **PASS.**

## 5. Q10/Q11 and Q15
- `GAP1_READ_ONLY_PINS` pins `analysis/c1b_cross_lineage_compare.py` to `33cdd329…`, the value chat measured at `85eca228`. `gap1_read_only_pin_check` runs before `v211_preflight_controls`. The driver's required list is now 25 paths. **PASS.**
- `gap1_stub_controls` has 11 cases: L 3, X 3, endpoint 5. The endpoint cases include the two required ones; chat checked the arithmetic: −1 + 16/512 = −31/32 < 0 gives PASS, and −1/64 + 16/512 = +1/64 gives FAIL.
  - In the X cases, mono closure, `eval_exterior` and `exterior_cover` are replaced by a stub that raises, so reaching them would show up.
  - Globals are restored in `finally`.
  - The cases are written only, not executed. They do run inside every production preflight (B7), so they will execute as part of any later run that the Judge authorizes.
- **PASS.**

## 6. Static controls
- The pre-run SHAs are recorded for 4 successive versions of the scripts.
- Run1 had C11 FAIL: its ladder sub-check printed the correct values (24, 8, 4096, (1024, 2048, 4096)) but compared them wrongly. The final run is all 16 PASS.
- chat's findings above come from its own reading, not from these controls.

## 7. Code's B-questions — chat's recommendations (ruling after both audits)
- **B1** Accept. Depth exhaustion is not a resource cap; it records that the certificate did not close (`MAX_DEPTH_EXHAUSTED` plus the attempt class).
- **B2** Accept. Keep `decision` as the plan's fixed decision, which is the baseline meaning, and keep `checker_decision` for the checker's own stop. This is documented, and it cannot reach the union.
- **B3** Accept. Testing all caps at resume start is the safe side.
- **B4** Accept the split into `certified` and `accepted`.
- **B5, B6** Accept. These are wording and diff-locality only, and the machine-readable fields are complete.
- **B7** Note: the stub controls are part of every preflight. Any later execution permission must cover them explicitly.

## Verdict
**chat diff audit v0.1: PASS (static).**
- F1–F3 are fixed as ruled.
- Q10/Q11 and Q15 are done.
- No new removed baseline lines outside cap and replay wiring.
- Protected bodies are unchanged; the 17 import pins and the authority pins (now 11) match.
- **Still required before FREEZE review:**
  1. ChatGPT's independent v0.1 audit;
  2. Judge rulings on B1–B7;
  3. the Judge's execution-order ruling.

**Execution remains unauthorized.** The non-numeric import test (NOT_VERIFIED) and every numeric step each need separate permission.

---

## 8. Collation with ChatGPT's independent v0.1 audit, and Judge rulings (2026-10-11, added after both audits)

- Sections 1–7 above were sealed at SHA-256 `cd4b3c08…` before chat read ChatGPT's audit.
- **ChatGPT's audit:** `CHATGPT_DIFF_AUDIT_C_GAP1_IMPL_V0_1.md`, SHA-256 `f1ffe1f8…2ff3c`, 192 lines, verdict **`DIFF_AUDIT_FAIL`** (F4, F5).
  - It agrees with chat's sections 1–6 on: pins (11/11 authority, 17/17 imports, the read-only pin), protected bodies, F1, F2, R, endpoint, checker independence and shared edges.

| ID | ChatGPT finding | chat re-check | Status |
|---|---|---|---|
| F4 | L's `root_count.rule` always says "g<0 … by direct certificate", but L closes through `exterior_cover`, and on unresolved boxes that calls `mono_closure_box`, which is allowed for L. The machine-readable rule can be false | Confirmed. chat itself wrote in §2 that L uses mono closure, yet passed the rule string in §3. **Missed (CHAT-DIFF-003).** | Blocking |
| F5 | The producer adds `accepted_count`/`accepted_work` and sets `previous_root` before the accepted-cap test. When the cap then makes `decision=ABORT`, the record holds counters that include this slab while `root_count.accepted=false`, and `resume_state()` counts only ACCEPT records, so ledger and reconstruction disagree | Confirmed (producer gating L846–858; driver `resume_state` counts `decision=="ACCEPT"` only). The order comes from the baseline, but v0.1's `accepted` field makes it a semantic contradiction. chat accepted B4 without checking the counters. **Missed (CHAT-DIFF-004).** | Blocking |

**chat's corrected verdict: v0.1 does not pass.** The PASS (static) in the Verdict section above is withdrawn.

chat's field-semantics pass checked each field against the contract, but not each field against **the other fields of the same record** and against the reconstruction path. From now on the pass includes:
1. **cross-field consistency within a record**, for example `accepted` against the counters, and `rule` against the guards actually used;
2. **ledger against resume/replay reconstruction**, field by field.

**Judge rulings (2026-10-11).**
1. **"v0.2でF4・F5を直す"** — fix F4 and F5 in v0.2.
   - **F4:** L records machine-readably which method closed each part, with counts of directly resolved and mono-closed boxes. The rule text must match what was actually used.
   - **F5:** the cap test uses candidate values. When the final decision is ABORT, the committed `accepted_count`, `accepted_work` and `previous_root` are not updated. The candidate values may be recorded as separate fields. The schema states what `accepted_count` counts in each lineage.
   - **Audit:** ChatGPT and chat audit the v0.1 → v0.2 diff and all ledger fields independently, including the two cross-checks above.
2. **"両監査の一致どおり受理"** — accept B1–B7 as both audits agree.
   - B2: on condition that the schema fixes how to read `decision` and `checker_decision`.
   - B4: accepted once F5 is fixed.
   - B7: any future execution permission must state explicitly that the preflight stub controls will run.
