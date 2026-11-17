# D-PRO R4 Stage0 — Chat implementation (2026-11-18)

**DIAGNOSTIC_ONLY / NOT_EVIDENCE.**

Repository branch: `codex/d-pro-r4-ratmodel-box2-20261118` (created fresh from frozen instruction v2, commit `da8ad02b`). Implementation by ChatGPT, **not** by Codex; the branch name is the pre-agreed output destination.

## Environment
Python 3.11.16, python-flint==0.8.0, mpmath==1.3.0. Ryzen 9 9900X research PC. Separate venv `/home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv`. No changes to main, STATE.md, frozen Julia lineage, R1–R3, or any evidence branches.

## One-line reproduction (stage0 only)
```bash
/home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python prolate_r4/stage0.py --split 4 --output /tmp/d_pro_r4_stage0_replay.json
```

## Additional checks
```bash
/home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python prolate_r4/majorant.py --split 4 --output /tmp/d_pro_r4_majorant_replay.json
/home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python prolate_r4/reference50.py --n 8 --n-compare 12 --output /tmp/d_pro_r4_reference_replay.json
```

## Outcomes

- Stage0 signed coefficient quadrature: budget PASS (sum of 35 halfwidths ~8.7843e-6 versus 1e-5).
- Stage0 positive remainder bound: all 64 subcells A<=1/8, total B4~2.7608e-6.
- Reference: 35/35 included, 60-digit mpmath working precision but quadrature itself is not certified to 50 correct digits.
- Stage1 preflight: 61/125 points violate A<=1/8 at the full fixed outer box. Hence stage1 is not started. Another stage1 plan must freeze a more appropriate remainder-majorant strategy before execution.
- **No full-box2 enclosure**; condition A remains OPEN.

See `ANALYSIS.md`, `RUN_RECEIPT.md`, and the original stdout/JSON receipts for exact rational intervals and resource measurements.
