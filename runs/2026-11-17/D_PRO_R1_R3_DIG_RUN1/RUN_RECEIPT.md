# D-PRO R1 R3｜Dig研究用PC 動作・幅診断 RUN1

2026-11-17 / Dig / **DIAGNOSTIC_ONLY / NOT_EVIDENCE / R3_FIXED23_INCOMPLETE / R3_MATH_AUDIT_OPEN**

## Input and chain

- R3 source: cotaxxxx/bg-spheroid-family `codex/d-pro-r1-corotation-r3-20261117`, commit `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`.
- R3 original ZIP: `prolate_r1/artifacts/D_PRO_R1_COROTATION_R3_20261117.zip`, SHA-256 `2ccaf1efa3c351c316a972148c07f5bce590240da42f71fd13cb5b85bbffeee6`.
- Parent R2: `bc70e1badbd9a89449cae6707ef37f5e69757a11`; R1 ZIP SHA `4810f975b31d2da43903f66e28545c2f62db0f63917948738567bc1be6565664`, R2 ZIP SHA `1f42136c4d26aca41413806cfb04f91b022ab3bd46b747627f3b20e532b75c7d` verified unchanged.
- R3 manifest: **72/72 SHA-256 matches**; ZIP integrity and Python `compileall` passed.
- Research PC: `daybreak-works`, Python 3.11.16 isolated venv, `python-flint` 0.8.0, Linux 7.0.0-38-generic.
- Environment: `PYTHONHASHSEED=0`, `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`.
- `main`, `STATE.md`, old source branches, Julia second lineage and old ZIPs not modified.

## Tests executed and results

| Test | Result | Notes |
|---|---|---|
| R2 regressions | **11/11 PASS** | `python -m unittest prolate_r1.tests.test_revision_r2 -v` |
| R3 additional regressions | **6/6 PASS** | `python -m unittest prolate_r1.tests.test_revision_r3 -v` |
| quick | **2/2 PASS** | Original two quick tests |
| Fixed 23 legacy full cases | **11 PASS / 12 INTERRUPTED / 0 FAIL** | Every case attempted once, with 210s per-case timeout |
| Fixed 36 R3 width cases | **NOT RUN HERE** | Codex R3 original tested only case IDs 8,33 (1 PASS, 1 width FAIL) |
| Center M/M6 bound 128/8 subboxes | **NOT RUN HERE** | Actual 128-box / 8-box measurement pending |
| Fixed 27 boxes and centers | **NOT RUN HERE** | No production broad sweep |

### Fixed23 test execution

- Case IDs 0..22, mathematically unchanged legacy test definitions. Dedicated journal (`--full --resume --case N`) for each ID, max six independent workers. Environment and source sealed.
- Strict per-case **210-second external operational timeout**, introduced for this Dig run (not a modification of mathematical test inputs). The R3 source runner did not receive a new tolerance or smaller sample.
- PASS cases: 0,1,2,3,4,5,6,10,11,12,13.
- INTERRUPTED (external exit 124) cases: 7,8,9,14,15,16,17,18,19,20,21,22.
- No selected case recorded a mathematical FAIL. Exit code 2 for each PASS shard means the other 22 cases in *that shard's full suite* are pending, not that the selected case failed.
- All 23 reports share plan SHA-256 `ded7b08f4ba6b7849a2471920238e43769fdf98da751aa0cbd70e5142ab826a8`; 23 case names and IDs unique, no retries, no missing IDs. Every interrupted case preserves its partial journal.
- Whole sharded attempt wall clock: **745.51 seconds** with six-process scheduling; this is not an estimate of full unbounded test runtime and no full-suite PASS should be inferred.
- Dig per-case orchestration is in `run_legacy23_shards.py`; exact execution receipts and journals are under `logs/legacy23_shards/`. No changes to the source full suite itself.

## R3 width observations preserved from Codex source (not re-run)

- Lambda=5 W point: half-width 0.000702314494447 (limit 0.05), point test PASS, measured 365.479s on Codex machine.
- W box 2: half-width 8,020,670.30469 (limit 0.3), FAIL, measured 983.340s on Codex machine.
- R3 source `outputs/R3_BOX_COMPONENTS.json` identifies box 2 half-width decomposition: 6,135,279.75 from *outer-box midpoint enclosure* (including endpoint Taylor quotient remainder), 1,885,390.55 outer mean-value correction, cap error 0. This is **not** the R=0 center Taylor M 128-box branch.
- `api.py` routes all tau within [0,1/4] through the equatorial endpoint Taylor chart even when tau has strictly positive lower bound. Box 2 has tau=[15/128,17/128]; a direct angular f_beta/(R^2 sin beta cos beta) kernel is defined throughout this box. **Proposed for a separately preregistered diagnostic**, not proven to meet the width threshold.
- These readings do NOT show false interval containment or a counterexample to W>0. New R3 jet, center M/M6 and chart routing remain independently mathematically unaudited.

## Verdict and scope

**SOURCE_72_SHA_PASS / R2_REGRESSION_11_PASS / R3_REGRESSION_6_PASS / QUICK_2_PASS / FIXED23_11_PASS_12_INTERRUPTED_0_FAIL / WIDTH_FAILURE_STILL_OPEN / CENTER_ACTUAL_MEASURE_NOT_RUN / MATH_AUDIT_OPEN.**

Original ZIP was not rebuilt or modified; no overall CERTIFIED/CLOSED designation. Full 23 cases can be resumed with a new recorded operational time budget if justified; never silently convert INTERRUPTED to PASS.

All evidence filenames and SHA-256 values are recorded in `SHA256SUMS.txt` (excluding itself).
