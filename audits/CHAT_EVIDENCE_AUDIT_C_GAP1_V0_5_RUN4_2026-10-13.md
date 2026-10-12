# CHAT EVIDENCE AUDIT — C gap ① v0.5 run4 — 2026-10-13

**Auditor:** ChatGPT (evidence readback; no code modification or rerun).
**Object:** run4 evidence at family commit `40e83b5c94f822b6a78682b1851b72d2d6b8de00`.
**Verdict:** **CHAT_EVIDENCE_AUDIT_PASS** for the recorded machine run and evidence identity. This does not independently establish the analytic D6 lemmas, the G0/E1 integration lemma, gap ②, or global C CLOSED.

## 1. Authority and source pins

- Source run branch `run/c-gap1-v0-5` resolved to `26d81e1049340d44ef7f08ae8e17d0692983395b`.
- Evidence family `origin/main` resolved to `40e83b5c94f822b6a78682b1851b72d2d6b8de00` before this receipt commit.
- Evidence path: `runs/2026-10-12/C_GAP1_V0_5_RUN4/`.
- Static implementation audit: `audits/CHAT_DIFF_AUDIT_C_GAP1_IMPL_V0_5_2026-10-12.md`, recording v0.5 static PASS and submission tarball SHA-256 `233b2bb1dfcef955cc569b962b9ba0d39231b467e8ba6225b8b7c78a0dd068e8`.

## 2. Byte integrity

SHA-256 readback on the committed evidence files:

| Artifact | SHA-256 |
|---|---|
| `run4/producer/ledger.jsonl` | `4b58a61f92180462b9570f664c391db0b3d64c47d3c129610ba39e5627bb91d9` |
| `run4/checker/ledger.jsonl` | `5636da10eca81926d6f42240532104df409fb4d6d048033940fdeb962f701240` |
| `run4/producer/checker_replay_exact.jsonl` | `7297f30fb0f5609f7105fc5947c1af95a0777ee26cd08667d52cb9ae43e9221a` |

`sha256sum -c SHA256SUMS.txt`: exit 0, all listed files matched.

## 3. Sequential run and terminal statuses

`run4/sequence.log` contains:
- `STEP0_PASS`, `STEP1_PASS`, `STEP2_PASS`, `STEP3_PASS`.
- `EXIT_ZERO producer_run` at 2026-10-12 20:40:43 JST, then `STEP4_PASS producer`.
- `EXIT_ZERO checker_run` at 2026-10-13 01:56:55 JST, then `STEP5_PASS checker`.
- `RUN4_COMPLETED` and `FINALIZE PASS COMPLETED`.
- `PUSH_COMPLETE status=PASS family_commit=40e83b5c94f822b6a78682b1851b72d2d6b8de00 run_commit=26d81e1049340d44ef7f08ae8e17d0692983395b reason=COMPLETED` at 2026-10-13 01:57:01 JST.

## 4. Ledger readback

Both producer and checker ledger files contain 325 records each: 1 header, 1 segment_begin, 160 attempt_begin, 160 slab_record, 1 segment_end, 2 lscpu_raw_trace.

- Producer: 160/160 ACCEPT, coarse indices 0–159 each exactly once, depth 0 for all, segment_end reason `completed`, no abort cause.
- Checker: 160/160 ACCEPT, coarse indices 0–159 each exactly once, depth 0 for all, segment_end reason `completed`, no abort cause.
- The paired producer/checker slab records agree on `coarse_index`, `lambda_lo`, `lambda_hi`, `decision`, and `refinement_depth` for all 160 records.
- Every checker slab has `checker_full_ok=true`, `checker_decision=REPLAYED`, `checker_reason=PASS`, `a1_label=A1_EXACT_EQUALITY`, and `a2_label=A2_LINEAGE_INDEPENDENT`.
- Checker root outcomes: 48 `ROOT_FREE_REGION` (L), 78 `ROOT_COUNT_BY_C1A_SIGN_NO_T_STAR` (X), 34 `RESOLVED_WITH_CERTIFIED_T_STAR` (R).
- Final accepted work is 123,912,192 in both ledgers.

## 5. Evidence classification and limits

**PASS:** run identity, manifest hashes, terminal machine status, fixed replay, 160/160 matching slab decisions, and checker recorded equality/independence labels.

**NOT_EVIDENCE:** parallel v9/v9.1 diagnostics; they are not promoted by this audit.

**Outside this audit:** independent mathematical audit of C-side analytic D6 bundle and G0/E1 v3, gap ②, and global cover assembly. Those remain Judge conditions. A successful machine ledger does not itself imply global C CLOSED.

## Conclusion

**CHAT_EVIDENCE_AUDIT_PASS.** This evidence audit supports the Judge's **CONDITIONAL_CLOSED** ruling for gap ① only.
