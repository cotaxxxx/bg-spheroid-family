# Instruction to Code — audit of the D6 GAP closure record v0 (chat, 2026-10-11)

## Object
bg-spheroid-family main `9943a6fbec35d67211db3a1ad6b58499310cb557`:
- `drafts/2026-10-11/D6_GAP_CLOSURE_RECORD_V0.md`, SHA-256 `d7a8d28cc300ae59c4599c8a0343ec08668a716ef60e5b5b2af78c6a0c6c401a`, 423 lines. This is the object of the audit.
- `drafts/2026-10-11/CHATGPT_D6_GAP_CLOSURE_INSTRUCTION_2026-10-11.md` (`819b1cc5…`): the instruction ChatGPT worked from.

Read them against EL `5afa815f` and C2 `7cb9b809` (bg-oblate-spheroid `design/d-ob-p2` @ `bbcfe662`), and against your own report `6d83cba5` and addendum `587e617c`.

## Independence
- Do **not** open chat's audit of this record before writing your verdict. That audit is `CHAT_AUDIT_D6_GAP_CLOSURE_RECORD_V0_2026-10-11.md`, which is not yet on main.
- Afterwards, add a short post-collation section if the Judge sends it to you.
- Disclose what you had already read. Same-lineage status is as before.

## Tasks
1. Check the pins (commit, SHA-256, line count) and the 11 sections against the instruction's item table.
2. For each of the 11 items, decide whether the GAP **you** raised is closed by (b) + (c): **CLOSED / NOTE / OPEN / FAIL**.
3. Check every source line reference (a) against the blobs.
4. **Item 3 (E-G3):** check the list of uses in ①/② against the contract v7 text. The relayed text is `255eb630`; the v7 exact file `a4914818` is not yet on main, so if you cannot see either, say so. In particular, say which derivative (∂_t E or ∂_t g) each listed use involves, and which lemma supplies the interchange for it.
5. **Item 6 (C-G2):** state on what range of γ the formula R_γ := −2γΨ′(1 − γ²) is well defined.
6. Any symbolic check must follow the same rule as before: script SHA recorded before running, exact arithmetic only, criterion stated in advance.

## Rules
- Read-only. No commit, no push, no change to any file, no certificate, no numerical search.
- Deliverable: `CODE_D6_CLOSURE_AUDIT_REPORT_V0.md`. Report its SHA-256 and line count, and end with an 11-row table.
