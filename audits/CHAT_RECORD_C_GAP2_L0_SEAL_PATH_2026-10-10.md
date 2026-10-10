# RECORD — ② L0 steps (a)(b): seal path and full SHA match (2026-10-10, research PC, read-only)

Run by the user on the research PC (daybreak-works) on 2026-10-10 at 23:36–23:37 JST. Commands: `ls -d`, `sha256sum` and `ls -la` only; nothing was written.

**(a) Seal path.** The parent is `/home/daybreak/basepoint-geometry-artifacts/C1b/`. Both pinned seal directories exist under their exact pinned names:
- `phase1_v212s_seal_20260918T222551Z`
- `phase2_v212s_seal_20260920T140743Z`

**(b) Full SHA-256 match** against C1b machine receipt §1.1 (blob `bdcafce7`) and ② contract v3 §2:

| object | observed SHA-256 | pinned | result |
|---|---|---|---|
| phase1 `ledger.jsonl` | 1e46da3a4ef38409fa1c2130f81cf1125a672b6e44e714f2028a9708cea64b5f | same | MATCH |
| phase2 `ledger.jsonl` | 09caf7b9da493aecc922f73f795bc3f4c4321b6cb0598d5b2b08f6c066b76b38 | same | MATCH |
| phase1 `checker_replay_exact.jsonl` | c31af672d12981ca08c15464439b8ca81c75f7dd2dd801ad3c78dbbfdffc5b69 | same | MATCH |
| `c1b_receipt_extract.json` | 8a332e568838b673c6d45ae934a47794cce3b9e1bb7cad9128dd7a3fcdfde81b | same | MATCH |

**A third directory matched the glob: `sealed/`.** It holds one subdirectory, `phase1_v211_0886a7b_20260915T192742Z`, dated 2026-09-15/17. This is a phase1 seal from the earlier v2.11 line, which the v2.12 run superseded. Its name differs from both pinned seal names and it contains no top-level `ledger.jsonl`. It is therefore **not a candidate**, and there is no ambiguity under the "multiple candidates" rule. Recorded for provenance only; it is not to be used.

**Status:** SEAL_PATH_OPEN → **RESOLVED**. LEDGER_PIN → **4/4 MATCH**.
Step (c) of L0 (reading the per-slab rows of both ledgers and cross-checking them) is not done. By contract it is the first step of the authorized run, after FREEZE.
