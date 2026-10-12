# JUDGE RECEIPT — C gap ① (U_check) — 2026-10-13

**Status:** CONDITIONAL_CLOSED (Judge: user, 2026-10-13 ~04:30 JST, after chat evidence audit)
**Evidence class:** MACHINE_PASS (both lineages) + CHAT_EVIDENCE_AUDIT_PASS

> This receipt transcribes the Judge ruling supplied in chat on 2026-10-13. The separately mentioned draft attachment was not available in this session; this file is based on the Judge's full text in that message, not a byte-identical copy of an attachment.

## Scope (verbatim from contract v9.1 tiling)

Gap ① U_check = {1/2 < t ≤ 1, 2/5 ≤ λ < 9/20}, covered by 160 λ-slabs of width 1/3200 on [2/5, 9/20]:

- L = 48 slabs [2/5, 83/200] (ROOT_FREE_REGION)
- X = 78 slabs [83/200, 703/1600] (ROOT_COUNT_BY_C1A_SIGN_NO_T_STAR)
- R = 34 slabs [703/1600, 9/20] (RESOLVED_WITH_CERTIFIED_T_STAR)
- Endpoint gate at t_e on [2/5, 1281/3200].

## Pins

- RUN_COMMIT: bg-oblate-spheroid `refs/heads/run/c-gap1-v0-5` = `26d81e1049340d44ef7f08ae8e17d0692983395b` (parent `85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b`)
- Evidence: bg-spheroid-family main `40e83b5c94f822b6a78682b1851b72d2d6b8de00`, `runs/2026-10-12/C_GAP1_V0_5_RUN4/`
- Producer ledger SHA-256 `4b58a61f92180462b9570f664c391db0b3d64c47d3c129610ba39e5627bb91d9`
- Checker ledger SHA-256 `5636da10eca81926d6f42240532104df409fb4d6d048033940fdeb962f701240`
- Replay SHA-256 `7297f30fb0f5609f7105fc5947c1af95a0777ee26cd08667d52cb9ae43e9221a`
- Implementation audit: `audits/CHAT_DIFF_AUDIT_C_GAP1_IMPL_V0_5_2026-10-12.md` (tarball SHA-256 `233b2bb1dfcef955cc569b962b9ba0d39231b467e8ba6225b8b7c78a0dd068e8`)
- Evidence audit: `audits/CHAT_EVIDENCE_AUDIT_C_GAP1_V0_5_RUN4_2026-10-13.md`
- Contract: v7 (`a4914818`) + v8 delta + v9 delta (`472ff013`) + v9.1 delta (`b85f69ae`)

## conditional_on

1. C-side analytic lemma bundle (D6 list; external audit pending)
2. Integration lemma G0/E1 v3

"C CLOSED" additionally requires gap ② (31/32 < t < 1, non-clamp C1b slab) and the global cover assembly.

## Not evidence

v9 / v9.1 parallel diagnostics in the evidence commit remain **NOT_EVIDENCE**.

## Judge ruling

**C gap ①: CONDITIONAL_CLOSED**. This is not a ruling of full C CLOSED.
