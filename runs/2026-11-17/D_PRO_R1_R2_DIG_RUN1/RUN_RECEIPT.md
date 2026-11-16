# D-PRO R1 R2｜Dig固定環境 動作検査 RUN1

2026-11-17 / Dig / **DIAGNOSTIC_ONLY / NOT_EVIDENCE / R2_RUNTIME_TESTS_PASS / MATHEMATICAL_INTERVAL_AUDIT_OPEN**

## Frozen source and lineage

- Source: cotaxxxx/bg-spheroid-family, branch codex/d-pro-r1-corotation-r2-20261117, commit bc70e1badbd9a89449cae6707ef37f5e69757a11.
- Source original ZIP: prolate_r1/artifacts/D_PRO_R1_COROTATION_R2_20261117.zip, SHA-256 1f42136c4d26aca41413806cfb04f91b022ab3bd46b747627f3b20e532b75c7d.
- Parent Dig R1 evidence: commit 1917e1ab3c22191852385cf8cd3df5f6d9958fb8. R1 original ZIP 4810f975b31d2da43903f66e28545c2f62db0f63917948738567bc1be6565664 unchanged.
- R2 source manifest: 29/29 file SHA matches; archive unzip CRC and syntax compileall clean.
- PC daybreak-works: Python 3.11.16, dedicated new virtualenv, python-flint 0.8.0; Linux-7.0.0-38-generic-x86_64-with-glibc2.43.
- Pinned environment variables PYTHONHASHSEED=0, OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1.
- Source files unchanged during runs. main, STATE.md, first lineage and frozen Julia second lineage not changed.

## Runtime diagnostics

| Test | Result | Resource/time |
|---|---|---|
| 11 R2 revision regression tests (`python -m unittest prolate_r1.tests.test_revision_r2 -v`) | **11/11 PASS** | 0.10 s, max RSS 36348 KiB |
| quick (`python -m prolate_r1.tests.run_tests --resume`) | **2/2 PASS** | 0.30 s, 36204 KiB |
| pilot box13 (`python -m prolate_r1.run_diagnostics --pilot`) | **COMPUTED** | 0.20 s, 28 box cells + 28 center cells |
| Reproduced R1 error axis_g(Q(1,2),Q(3)) in R2 | **RESOLVED IN R2 RUNTIME** | Positive inverse regression test PASS |
| Fixed full suite 23 cases | **23/23 individual cases PASS** | split execution: 22 cases in 6 parallel processes, 189.584 s wall; case 0 as separate canonical journal |

### How full 23 was run and what it means

- `python -m prolate_r1.tests.run_tests --full --list-cases` confirmed fixed IDs 0..22.
- `dig_r2_full.json` canonical journal: case 0 PASS, exit=2, other 22 cases pending.
- Cases 1..22: each run using the **same fixed R2 source**, `--full --resume --case N` with its **own** dedicated JSON journal and `.cases` folder. Six parallel workers; fixed timeout 240s/case. Each case finished PASS. Each shard exits=2 because it is one selected case of a 23-case suite, **not** because that selected case failed.
- All 23 case records passed source/environment/plan SHA consistency check, exact case names/IDs, no retries, no FAIL, no INTERRUPTED, no duplicate, no missing case.
- Identical execution plan SHA-256 for all 23: 9f37bee7e2b1f8430679eeea58f8a6f166fffc2a385e1c1b09265dba5b412a3c.
- Aggregate: `logs/FULL23_AGGREGATE.json` derived independently by `aggregate_full23.py` and explicitly labeled **AGGREGATED_PER_CASE_FIXED23_NOT_SINGLE_SUITE_SUCCESS**. It is **not** a completed single-process full-suite snapshot.
- Sharded execution `logs/full_shards/` preserves each case stdout, stderr, plan, start/result records, tracebacks if any, and receipt. `run_full_shards.py` and `aggregate_full23.py` are included solely as Dig execution/audit code; they do not change the producer or test-case content.
- Original six fixed test function bodies (`smoke`, `derivative_case`, `sphere_case`, `boundary_case`, `small_box_case`, `_quick_axis`) were independently compared as Python AST against R1 and found identical.

## Scope and limitations

- R2 improves reciprocal-positive behavior and durable test recording; these runtime PASS results do NOT independently certify rigorous enclosure formulae or Peano remainder.
- W and conditions A, Z, C, Q, B remain OPEN as global mathematical claims.
- Entire fixed27 diagnostic and R2 vs old V comparison **NOT_RUN** pending chat mathematical audit.
- This evidence branch records R2 diagnostic tests only. No main, STATE.md, original ZIP or source code edits.

## Evidence

- `R2_SOURCE_ORIGINAL.zip`: exact original ZIP as in Codex R2 commit.
- `SOURCE_SHA256_CHECK.stdout`, environment.txt, Python 3.11.16/flint 0.8.0 proof of environment, quick/pilot/regression logs and resource values.
- `logs/dig_r2_quick.json.cases/`, `logs/dig_r2_full.json.cases/`, `logs/full_shards/`: raw case journals.
- `logs/FULL23_AGGREGATE.json`: independently verified 23 case status summary.
- `run_full_shards.py`, `aggregate_full23.py`: exact Dig orchestration and verification code.
- `SHA256SUMS.txt`: byte-level verification of all evidence files other than the manifest itself.

**Dig verdict: SOURCE_29_SHA_PASS / 11_R2_REGRESSION_PASS / QUICK_2_PASS / PILOT_COMPUTED / FULL_23_CASES_INDIVIDUALLY_PASS / MATH_AUDIT_OPEN / DIAGNOSTIC_ONLY_NOT_EVIDENCE.**
