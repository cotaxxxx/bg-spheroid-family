# D-PRO C21 H — One-box cost-trim pilot
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**. 2026-11-18. No adaptive coverage.

Baseline: 0427b19d84e5105aa1a03ff69c9842065d491f3c.
V39: 544ebfd138c02d2fc68806184a1d0ce2e744fa2c.
Pinned R3: fdfb498f2117cc0c5d72e88cc3be05eac9727bd8.

## One-line command
```bash
cd /home/daybreak/D_PRO_C21_H_COST_TRIM_20261118/worktree && PYTHONPATH=/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source /home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python -u -m prolate_r4.c21_cost_pipeline
```

The pre-registered experiment list, numerical settings, per-box time
limits, 12-worker group ordering, and 7200s cumulative wall cap
are in PRE_RUN_FREEZE.md and EXPERIMENTS.json. This branch only
contains 24 valid cost-only probes plus 2 non-runnable P3 C probes;
all sign values are RECORD ONLY.

Groups:
(a) P1-P4 at lambda widths 1/16,1/8,1/4 (12 boxes)
(b) P1-P4 Hessian-only mesh 8x16 ratio1 order4 or2 (8 boxes),
    point and gradient remain 16x32 ratio1/2 order4
(c) P1 anchored R,tau widths1/32,1/16 at lambda width1/8
    (2 actual boxes). P3 anchored tau=63/64 exceeds tau domain
    for both widening instructions, so 2 P3 cases are recorded
    NOT_RUN_OUT_OF_DOMAIN rather than silently moved.
(d) Optional P1/P3 at lambda=[2,17/8] (2 boxes).

Sources prolate_r4/c21_cost_*.py. Direct producer per box:
```bash
python -m prolate_r4.c21_cost_box --id A_P1_L1_16 --output runs/2026-11-18/D_PRO_C21_H_COST_TRIM/boxes/A_P1_L1_16.json
```

All H intervals use signed spatial Taylor integral, 128-bit Arb,
original C21 Hessian mixed jets. Point/gradient base 16x32 ratio1/2
order4 unchanged. Hessian mesh selectively changes ONLY per frozen
variant ID. Formula diagonal [0,h_i²]/2, cross ±h_i h_j.
MVT route uses rho' in [0,rho_hi], z and lambda as independent
outer parameters with original positive lower bounds.

Files:
- boxes/ID.json: exact rational H, point/gradient/Hess component
  corrections and separate worker times, two angular mesh sizes and RSS
- logs/ID.log: complete signed output and errors
- SUMMARY.json, CHECKER.json: measured status, not mathematical proof
- COST_MODEL.json: empirical nonnegative additive decomposition and
  conditional/hypothetical full-domain cost tables with explicit
  lambda≈2 separate plate assumptions
- RUN_RECEIPT.md: human-readable model, per-box costs, comparisons
- R3_PIN_CHECK.md, SHA256SUMS, ZIP_SHA256.txt, ZIP.

NEVER claim a full H cover or a certified H sign. No main,
STATE.md, pre-existing branches, tags, R3 or Julia edits.
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**.
