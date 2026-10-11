# CHAT RECORD — v7 exact file vs the audited relay text (2026-10-11)

## What was compared
- **Exact file.** `drafts/2026-10-11/C_GAP1_CONTRACT_DRAFT_V7.md` on bg-spheroid-family main `c286b838` (parent `09d44320`). SHA-256 `a49148180fdeb33272e7358028caa55ec1dc06e5d4f526cd23eca50ff65c2a37`, 687 lines, 16371 bytes. ChatGPT placed it on the research PC and the Judge committed it.
- **Audited text.** The relayed copy that chat audited (audit `b177c450`, verdict PASS) is saved here as `audits/v7id/C_GAP1_PREDECLARE_DRAFT_V7.relay_audited.txt`. SHA-256 `255eb630a1b98a03d89371a4fdf4b703222c1f135a27714fd66b9d4bf17668a7`, 424 lines. The relay had lost the Markdown layer: no `#` headings, no `**` or backticks, table pipes turned into tabs, and blank lines and `---` dropped.

## Method
This was not predeclared. A raw diff came first and showed only Markdown-layer differences; the normaliser was then written to remove **formatting characters only**. It deletes no words, digits or symbols of the content, apart from `|` and `-` used as table and rule syntax. `audits/v7id/normalize_markdown.py` processes both files the same way:
- it removes lines made only of `-`, `|`, `:` or spaces (blank lines, rules, table separators);
- it strips leading `#`, every `**`, backtick and `|`, and tabs;
- it normalises list bullets;
- it collapses whitespace.

The two normalised outputs were then compared as a line diff, and as a single whitespace-collapsed token stream.

## Result
- **Token stream: identical.** Both are 11923 characters, and they match exactly.
- **Line diff:** one difference, and it is a line wrap only. In the exact file, the bullet "論文本文で theorem を CLOSED と記載するには HUMAN_EXTERNAL_AUDIT_PENDING が別条件として残る" runs over 3 lines; in the relay it is on 1 line.
- So there is no difference in content. Every word, number, SHA, formula and rule in the exact file is what chat audited.

## Consequence
- The FREEZE object for C gap ① is the exact file `a4914818`. Its content is the audited v7 (PASS, `b177c450`). The 2 clarifications binding by record (`541f3025`) still apply.
- The FREEZE blocker "v7 exact file not saved / identity unchecked" is cleared.
- **Remaining before a FREEZE ruling:**
  - the ① implementation and its diff audit (7 files, plus 15 imports byte-identical, DIFF-A–E and DIFF-K);
  - the Judge's ruling on execution order (the research PC cannot run D5 and the C-gap or prolate work at the same time).
- Nothing is frozen, and no computation is authorized.
