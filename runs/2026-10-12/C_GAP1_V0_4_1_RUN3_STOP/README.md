# C_GAP1 v0.4.1 run3 — STOP / NOT CLOSED

Producer full run STOP at 2026-10-12T10:56:50+09:00, coarse slab 117 depth 3 `[11183/25600,699/1600]`.
Ledger segment_end: `MAX_DEPTH_EXHAUSTED`, `CERTIFICATE_INCONCLUSIVE/L_NEGATIVE_INCONCLUSIVE`. This is **not** a mathematical counterexample.
Producer and checker preflight passed; the 14 lines containing FAIL matched run2's corresponding producer/checker preflight output respectively. Checker full run was not started.

- `run3/`: complete sequential-run output, producer ledger and replay, preflight stdout and records.
- `x_diagnostic_NOT_EVIDENCE/`: earlier slab125 X-only diagnostic, not proof evidence.
- `GAP1_RESUMABLE_PINS.json`: pinned execution manifest.
- `run3_sequential.sh`: final local sequential driver with resumption logic. Prior false-positive stops are recorded in `run3/sequence.log`.
- `SHA256SUMS.txt`: relative-path SHA-256 checksums of all included evidence files (excluding this checksum file).

RUN_COMMIT `d68dfd918b73f3de0158947f5330ee2605646a4b` (local `bg-oblate-spheroid` branch `run/c-gap1-v0-4`). No checker run, rerun, or code change was performed after producer STOP.
