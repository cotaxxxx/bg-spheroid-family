# D-PRO R1 共回転｜Dig研究用PC 動作検査 RUN1

2026-11-17 / Dig / **DIAGNOSTIC_ONLY / NOT_EVIDENCE / R1_EXECUTION_INCOMPLETE / MATH_AUDIT_OPEN**

## 原本と環境

- Source repository: cotaxxxx/bg-spheroid-family, branch codex/d-pro-r1-corotation-20261117, commit 4b7f1f73421f2765d347e4d2ffc9ab004393695c.
- ZIP SHA-256: 4810f975b31d2da43903f66e28545c2f62db0f63917948738567bc1be6565664.
- `python -m prolate_r1.verify_manifest`: all 24 source SHA entries matched. ZIP integrity and Python compileall succeeded.
- PC: daybreak-works; Python 3.11.16 isolated virtualenv; python-flint 0.8.0; Linux-7.0.0-38-generic-x86_64-with-glibc2.43.
- Environment: PYTHONHASHSEED=0, OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1.
- Original source, main, STATE, first-lineage and frozen Julia lineage not changed.

## Results

| Command | Result | Exit | Research PC wall time |
|---|---|---:|---:|
| Source manifest verification | 24/24 PASS | 0 | not separately timed |
| quick tests | 2/2 PASS | 0 | 0.10 s |
| fixed box-13 pilot | computed, 28 cells + 28 point cells | 0 | 0.30 s |
| full test suite | **INCOMPLETE: external 480s timeout** | **124** | **480.13 s** |
| additional four-API diagnostic | 3 RAN, axis_g FAILED | 1 | 0.30 s |
| axis_g(1/2,3), default Config | **FAILED** | 1 | 0.10 s |

## Reproduced axis_g error

Reproduction: `from flint import fmpq as Q; from prolate_r1 import axis_g,Config; axis_g(Q(1,2),Q(3),config=Config())`.

Traceback: `prolate_r1/api.py:193` calls `integrate`, which throws at `prolate_r1/quadrature.py:95`:

    ArithmeticError: non-finite/empty quadrature

Cell investigation: on axial integration interval y=[3/4,7/8], the true distance interval D has a strictly positive lower bound but the wide interval product D**3 contains 0; dividing by this wide interval produces NaN jet coefficients. This is an interval dependency / denominator evaluation implementation problem, NOT evidence of singular true integrand. Assess reciprocal-first evaluation with rigorous denominator control. No source was edited.

## Full suite timeout

Six visible PASS records before timeout: static arithmetic-input test, then 5 differential/identity cases at (lambda,R,tau):
- (2,1/8,1/4); (2,1/4,1/2); (2,1/2,3/4); (7/2,1/8,1/4); (7/2,1/4,1/2).
- A subsequent test was unfinished when the guard ended the process.
- There was no displayed FAIL but no full-suite PASS. The script writes JSON at completion; `dig_tests_full.json` was not created. Stdout retains the completed records.

## Not run and decision

- Fixed27 diagnostic: **NOT_RUN** (full suite incomplete).
- No R1 mathematical interval-soundness audit, no R2 comparison, no global sign certification.
- Next implementation version must keep original ZIP immutable, correct axis_g and provide executable / resumable test diagnostics. Re-seal SHA; Dig re-tests separately.
- Outcome: SOURCE_SHA_PASS / QUICK_PASS / PILOT_COMPUTED / AXIS_G_BUG / FULL_TIMEOUT_124 / FIXED27_NOT_RUN / DIAGNOSTIC_ONLY_NOT_EVIDENCE.

## Evidence

- The exact source original ZIP is copied to R1_SOURCE_ORIGINAL.zip.
- `logs/` stores stdout, stderr, timing, exit statuses, quick JSON and pilot JSON, default axis traceback, cell and intermediary diagnosis.
- `SHA256SUMS.txt` checks every evidence file except itself.
