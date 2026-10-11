# CHAT DIFF AUDIT — C gap ① implementation submission v0.2 (2026-10-11)

**Auditor.** chat, sole formal diff auditor under the roles ruling (`audits/CHAT_RECORD_AUDIT_ROLES_2026-10-11.md`). Main is `049eab82`.

**Object.** `C_GAP1_IMPL_V0_2_SUBMISSION_2026-10-11.tar.gz`
- SHA-256 `eb5f6e86ae045b2e698d49cdfb31ccb3a26ebf52e2059587a44c37b5d419ed2b`, 276325 bytes. Received as the Judge's attachment.
- `MANIFEST.sha256` is `5de81a7c…3f68`; all 39 entries check.

**Instruction.** `CODE_INSTRUCTION_C_GAP1_IMPL_V0_2_2026-10-11.md` (`2f292f89`).

**Method.** Static reading; nothing was imported or executed. chat diffed v0.1 (`df2a6915`) → v0.2 itself, then applied the three-part field pass:
1. each field against its contract meaning;
2. fields against each other within one record;
3. the ledger against resume/replay reconstruction.

## 1. Scope of change
- Both kernels and both entry points are **byte-identical to v0.1**. The changes are only:
  - producer gating: +90/−14;
  - checker gating: +89/−15;
  - driver: +3/−2.
- All of these are DIFF-E. No protected body is touched. Since v0.1, the 17 import pins, the read-only pin and the protected bodies are unchanged.

## 2. F4 — L records the method actually used: PASS
- `gap1_negative_block_closure` counts, for each stage, how many boxes were closed directly and how many by mono closure. It reads the guards the unchanged baseline `eval_exterior` already returns: sign guards `(label, side, …)`, and mono guards whose kind is `side + "_MONO"` (baseline L49). No evaluation is repeated.
- `method` is `DIRECT_G_BOX_AND_MONO_CLOSURE_G0_E1_V3` if any box was closed by mono closure, and `DIRECT_G_BOX_ONLY` otherwise. The L `rule` is taken from `GAP1_L_RULES[method]` only when the record is certified; otherwise `rule = null` and `method` is kept.
  - **Cross-field check:** the rule text equals the closure method, and the counts come from the same guards. Consistent.
- X: if the X guards show any mono attempt, the run stops with `CONTRACT_MISMATCH:X_MONO_CLOSURE`. The X code can never produce one, because `x_negative_eval` emits only `X_DIRECT_G` guards.
- R: no closure record.

## 3. F5 — counters move only on a final ACCEPT: PASS
- **Producer.** `cap_test_*` starts equal to the committed values. On `ok` it becomes committed + 1 and committed + attempt_work, and the caps are tested on those candidate values. Only on a final ACCEPT are the committed `accepted_count`/`accepted_work` and `previous_root` set. Every ABORT path leaves the committed values as they were. The cap is classified on `cap_test_*` (global first, then the accepted caps on the candidate values), and `cap_test_*` is written into the slab_record.
- **Checker.** The same scheme, for both a plan ACCEPT and a plan ABORT whose own attempt is `ok`. The committed values move only when no cap applies to a plan ACCEPT. `checker_decision` is ABORT on any cap stop or plan ABORT.
- **Cross-field check:**
  - `root_count.accepted` is set by `gap1_mark_decision` as `decision == "ACCEPT"`. The checker passes `"ABORT"` when `checker_decision == "ABORT"`.
  - It therefore equals `gap1_counts_accepted(payload)` = `decision == ACCEPT and checker_decision != ABORT`, which is exactly the rule the driver's `resume_state` now uses.
  - The counters differ from `cap_test_*` exactly on a cap ABORT. Consistent.
- **Ledger against reconstruction.** `gap1_ledger_count_audit` walks the ledger in the same way as `resume_state`: `attempt_begin`, `interrupted_attempt_charge`, then slab_records under the same acceptance rule. It requires every stored (`attempted_count`, `cumulative_work_after`, `accepted_count`, `accepted_work`) to equal the running totals, the `accepted` flag to equal the rule, and `checker_decision` to be one of {REPLAYED, ABORT}.
  - It is called at resume in both lineages (producer L629, checker L689).
  - `gap1_terminal_abort` now re-derives the cap from `cap_test_*`. Consistent.

## 4. B2 schema rule: PASS
Schema §0 fixes the reading: `decision` is the plan decision and `checker_decision` is the checker's own state. One function decides acceptance, and the driver uses the same rule.

## 5. Remaining items
- **A1, authority pins.** `GAP1_AUTHORITY_SHA256` in the code still lists the v0.1 eleven. It lacks:
  - the v0.2 instruction (`2f292f89`);
  - the v0.1 audit with the §8 rulings, as committed (`0fe5ec55`);
  - the roles record (`089ff9ae`).

  When Code built v0.2, main was still `d9457b2a`, so these were not available to it. This is **provenance completeness**: it does not affect any certificate path. But a run ledger header would not cite the documents that govern this version.
- **A7, checker `attempt_sequence` after an interruption.** Inherited from the baseline (checker gating L359, L526). After an interruption the checker's own sequence number differs from the plan's, and `replay_state` stops with `A1_REPLAY_ATTEMPT_SEQUENCE_MISMATCH`. **It fails closed** and can never ACCEPT wrongly. But a long run that is interrupted could become impossible to resume, so the run would have to start again. Code's proposed fix is to record `plan_attempt_sequence` separately and match on it; that would be DIFF-E.
- **B1–B7.** Implemented as ruled: B2 is done, the rest are as in v0.1, which is what was accepted.
- **B8–B12.** These are new v0.1 notes that were never ruled. chat's view: none affects soundness. They are recording and robustness notes, and can be accepted as they are.

## Verdict
**chat diff audit v0.2: PASS (static) for F4, F5, B2 and the three-part field pass.**

Before FREEZE review, the Judge needs to decide:
1. how to handle A1 and A7;
2. B8–B12;
3. the execution order.

Nothing is frozen and execution is not authorized. The NOT_VERIFIED runtime items (namespace import resolution, the stub-control results, the certificates actually closing) still need separate permission to test.

## Judge rulings (2026-10-11)
1. **"v0.3でA1・A7を直す"** — fix A1 and A7 in v0.3. v0.3 is a small version; chat audits only the v0.2 → v0.3 delta, together with the three-part field pass.
   - **A1:** add three documents to `GAP1_AUTHORITY_SHA256`: the v0.2 instruction, the v0.1 audit and the roles record. Also add the v0.2 audit, this record, and the v0.3 instruction. Each is pinned by the SHA-256 measured on main.
   - **A7:** in both lineages the checker records the plan's sequence number separately (`plan_attempt_sequence`), and `replay_state` and resume match on that field. The checker's own `attempt_sequence` keeps its meaning. A static control must cover interrupted-producer and interrupted-checker cases by reading the source.
2. **"現状のまま受理"** — B8–B12 are accepted as implemented.
