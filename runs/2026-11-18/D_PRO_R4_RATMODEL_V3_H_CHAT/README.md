# D-PRO R4 v3: horizontal H box2 and V35 W gate

**2026-11-18 / DIAGNOSTIC_ONLY / NOT_EVIDENCE**

Repo: `cotaxxxx/bg-spheroid-family`  
New branch: `research/d-pro-r4-ratmodel-v3-h-20261118`  
Upstream v2 commit: `2f9a0e1c515d2c271ebb1b8be51659bf22623eab`  
Correct V35 commit: `e5f1b2450c31481f1e32bf58ad96245e92df9d4f`

## New files

- `prolate_r4/h_box2.py`: §6 direct horizontal `E_rho/rho` Arb
  integration, signed 4th-order spatial Taylor and outer box derivatives.
- `prolate_r4/test_h_kernel.py`: 15 comparison points to the pinned R3
  physical `fx/rho` integrand; shares upstream geometry.
- `prolate_r4/verify_h_box2.py`: exact-rational contract checker for
  the emitted JSON; not an independent proof of the quadrature engine.
- `prolate_r4/ANALYSIS_V3_H.md`: equations, proof obligations and limits.
- `prolate_r4/v35_w_split_preflight.py`: four child 500-point A preflight.
- `prolate_r4/v35_w_b4_cover.py`: interval patch B4 preflight with
  frozen resource/acceptance conditions; NOT 35-coefficient cubature.
- `runs/2026-11-18/D_PRO_R4_RATMODEL_V3_H_CHAT/`:
  `H_box2.json`, `H_box2.log`,
  `H_initial_failed.log`,
  `checker.json`, `h_kernel_crosschecks.json`,
  `STAGE1_W_RULE_FREEZE.md`,
  `W_stage1_4child_point_preflight.json` and `.log`,
  `W_stage1_4child_B4_cover.json` and `.log`,
  `RUN_RECEIPT.md`, `SHA256SUMS`, evidence ZIP and its checksum.

## Run command (daybreak-works, Python 3.11.16)

```bash
cd /home/daybreak/D_PRO_R4_RATMODEL_V3_H_20261118/worktree && PYTHONPATH=/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source /home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python -m prolate_r4.h_box2 --order 4 --base-u 16 --base-v 32 --distance-ratio 1/2 --output runs/2026-11-18/D_PRO_R4_RATMODEL_V3_H_CHAT/H_box2.json
```

Pinned frozen R3 source directory is **read-only** and all seven direct
source-file hashes were compared with exact commit `fdfb498f...`.
No worktree or repository branch outside the new v3 branch was changed.

## Result and limits

- H box2 enclosure `[-0.1990623982,-0.1202379278]`,
  halfwidth 0.0394122352, wall 172.90 s,
  peak RSS 36288 KiB, 5/5 diagnostic references included.
- W v2 stage0: unchanged PASS.
- W v3 four-child A pointwise preflight: 0/500 violations.
- W v3 **continuous B4 preflight: all 4 children incomplete**,
  `DEPTH_LIMIT_A`. No W child or full-box interval was computed.

The H sign is not used to select a global research method. V32 W
performance was measured on different hardware, so no matched-machine
speedup is claimed. The v3 W coefficient/full spatial stage1 was not run.
All files here are research diagnostics, **not mathematical evidence**.
