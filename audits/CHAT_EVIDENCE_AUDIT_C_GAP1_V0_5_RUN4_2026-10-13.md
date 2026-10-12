# CHAT EVIDENCE AUDIT — C gap ① v0.5 run4 (2026-10-13)

**Auditor.** chat, the sole auditor (roles record 2026-10-11).
**Object.** `runs/2026-10-12/C_GAP1_V0_5_RUN4/` at bg-spheroid-family main `40e83b5c94f822b6a78682b1851b72d2d6b8de00`, and RUN_COMMIT `26d81e1049340d44ef7f08ae8e17d0692983395b` = bg-oblate-spheroid `refs/heads/run/c-gap1-v0-5` (parent `85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b`).
**Method.** Independent reconstruction from the committed bytes (fresh clone / fetch on 2026-10-13 ~04:10 JST). Nothing re-executed; no Arb evaluation re-run. Checks listed below were each computed by chat, not read from the run's own PASS lines.

## Verdict
**run4 evidence: PASS (machine, both lineages).** No finding. Status of the gap-① claim remains conditional (see §4).

## 1. Integrity of the evidence directory
- `SHA256SUMS.txt`: 24/24 OK; every file in the directory is listed (no unlisted file).
- `GAP1_RESUMABLE_PINS.json` in the evidence dir is byte-identical (SHA-256 `9a69b084…`) to `gap1_analysis/GAP1_RESUMABLE_PINS.json` at RUN_COMMIT.
- `sequence.log`: STEP0–STEP5 PASS → RUN4_COMPLETED → FINALIZE PASS COMPLETED, timestamps monotone (producer 15:25:42→20:40:43, checker 20:40:43→01:56:55 JST). `other_run_check.txt` empty = STEP0 `no_other_full_run` as the runner defines it.

## 2. Source identity (RUN_COMMIT ↔ audited v0.5)
- Audited blob table (v0.5 static audit §Verdict, 25 rows) == `RUN_COMMIT_25_BLOBS.tsv` == `expected_blobs` for producer and checker in the pins JSON == `identity.expected_blobs` in both ledger headers: all four equal, 25/25.
- `git ls-tree -r 26d81e10` (fetched from GitHub): 25/25 paths carry exactly these blob ids; `26d81e10` adds only the 7 gap1 files + the pins JSON on top of `85eca228` (8 files, 0 deletions).
- The 7 gap1 blobs recomputed with `git hash-object` from `submissions/2026-10-12/C_GAP1_IMPL_V0_5_SUBMISSION_2026-10-12.tar.gz` (SHA-256 `233b2bb1…`, MANIFEST 0 failures) match the table — i.e. what ran is byte-for-byte what chat audited statically.
- Ledger headers: `head` = RUN_COMMIT, `ref` = run/c-gap1-v0-5, `clean_status` empty, Python 3.11.16, python-flint 0.9.0 / mpmath 1.4.1 wheel SHA-256 as pinned, lscpu canonical `7562aa15…` identical at header and segment_end for both lineages (identity before/after unchanged).

## 3. Ledgers and the mathematical scope
- Both ledgers: 325 records, `sequence` 0…324 contiguous, `prev_sha256` chain intact, `record_sha256` recomputes from canonical JSON (checked on a sample record in each lineage).
- Slab records: 160 per lineage, `coarse_index` 0…159 once each, decision ACCEPT 160/160, refinement_depth 0 for all, REFINE/ABORT 0. λ-intervals form an exact tiling of [2/5, 9/20] with uniform width 1/3200 (no gap, no overlap).
- Group boundaries match contract v9.1: L = ROOT_FREE_REGION 48 slabs on [2/5, 83/200]; X = ROOT_COUNT_BY_C1A_SIGN_NO_T_STAR 78 slabs on [83/200, 703/1600]; R = RESOLVED_WITH_CERTIFIED_T_STAR 34 slabs on [703/1600, 9/20]; each group contiguous.
- Checker: 160/160 `checker_decision=REPLAYED`, `checker_full_ok=True`, `checker_reason=PASS`, labels `A1_EXACT_EQUALITY` / `A2_LINEAGE_INDEPENDENT`. Checker precision 192 ≥ producer 160. Checker header `producer_ledger_sha256` = actual producer ledger `4b58a61f…`; both lineages report `replay_sha256 7297f30f…` = actual `checker_replay_exact.jsonl`; the 160 replay rows agree with the producer slab records on (λ_lo, λ_hi, decision).
- Producer vs checker slab records differ only in checker-side fields and in enclosure digits (`T_star` 30, `sup_error` 21, `trace` 82, `gap1` 160 — all numeric-width differences at 160 vs 192 bit), never in decision, tiling or outcome class.
- Endpoint gate (t_e anchor, [2/5, 1281/3200]): PASS in both lineages with negative seed and cumulative upper bounds.
- Preflight: both stdout files contain only negative-control `FAIL` lines; chat recomputed the FAIL-line sets and they equal run2's sets lineage-by-lineage (same rule the runner applies).
- Import independence: `gap1_checker/*` imports only `checker/*` numerics and the shared persistence module `gap1_analysis/c1b_resumable_driver.py`; no `gap1_producer`/`producer` import (import-only origin test 24/24 PASS).

## 4. What this does and does not close
- Closes: the machine gate for gap ① U_check = {1/2 < t ≤ 1, 2/5 ≤ λ < 9/20} on the v9.1 tiling, both lineages.
- Does not close by itself: gap ① as a *mathematical* statement stays conditional on the same C-side analytic bundle as C1a–d (D6 list), on the G0/E1 v3 integration lemma, and on gap ② (31/32 < t < 1 on the non-clamp C1b slab) plus the global cover assembly before "C CLOSED" can be written.
- Carry-over (procedural, next version only; no new round): the v9/v9.1 parallel diagnostics directories inside the evidence commit are NOT_EVIDENCE per README and should stay so in any receipt.
