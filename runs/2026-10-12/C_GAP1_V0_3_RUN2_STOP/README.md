# C_GAP1 v0.3 — run2 STOP evidence

Status: **STOP / NOT CLOSED**. Producer run exited nonzero at 2026-10-12T03:08:22+09:00 with `C1B_UNRESOLVED` on coarse slab 125, depth 3, interval `[5621/12800, 11243/25600]`. Checker run was **not started**. These records are for independent audit, not a proof of the mathematical claim.

- `run2/`: sequential restart; producer and checker preflight PASS; producer STOP. `run2/producer/ledger.jsonl`, `run2/producer_run.stdout`, `run2/producer/checker_replay_exact.jsonl`, preflight stdout and raw records are preserved.
- `old_run_NOT_EVIDENCE/`: superseded first run; **NOT_EVIDENCE**. Preserved unchanged for provenance.
- `SHA256SUMS.txt`: SHA-256 of every included evidence file (relative paths).

RUN_COMMIT (not pushed by this evidence-only action): `7ec8e087c1da91e8993cdec6c7ac6334149bced1` on `bg-oblate-spheroid` local branch `run/c-gap1-v0-3`.

No code/contract changes, reruns, or checker run were made during evidence preservation.
