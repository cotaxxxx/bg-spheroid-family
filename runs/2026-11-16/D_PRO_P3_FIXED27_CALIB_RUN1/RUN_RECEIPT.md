# D-PRO P3 | fixed 27-box calibration on daybreak-works

2026-11-16 / Dig / **DIAGNOSTIC_ONLY / NOT_EVIDENCE / NOT_FROZEN**

Source: cotaxxxx/bg-spheroid-family codex/d-pro-p3-kernel-calib-20261116, commit 556997ac2387933138296939b9c58eda32d7cdec (source unchanged).
Auditor guidance: chat V29 ce2aa83c5373bb5cedc19e50beedf5c87e84f5a3 (soundness audited but W1 width too large).

- PC: daybreak-works, Ubuntu Linux, Python 3.11.16 in a fresh isolated virtualenv, python-flint 0.8.0, mpmath 1.3.0.
- Code and boxes: original prolate_p3/SHA256SUMS validated before run; PRE_RUN_SHA256.json used by producer.
- Command from repository root: python -m prolate_p3.calibrate --out p3_calibration_20261116.
- Environment: PYTHONHASHSEED=0, OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1.
- Dataset: 27 fixed boxes, each at 128 and 192 bits, 32x64=2048 cells, series N=96. All 54 outcomes computed, stderr empty.
- Wall time (outer /usr/bin/time): 65.31 seconds. Max RSS outer process 35732 KiB; maximum child worker RSS 35188 KiB.
- Worker wall sum: 63.230067521 seconds. 54 boxes, 110592 total cells.
- Routes: Ez_over_z 36, Ezz_vertical_segment_hull 18.
- Diagnostic interval lower signs: positive 26, negative 28. These signs are NOT global proof or a method-selection criterion. Negative lower endpoints do not imply negative true V.
- Evidence: calibration_output/results.json, results.tsv, boxes_used.json, seal_used.json, individual worker stdout/stderr, source seal validation, outer timing/logs.
- No change to STATE.md, main, first lineage, Julia lineage. No proof certification run.
- Remaining: W1 improved quadrature/width, chat independent audit of revised bounds.
