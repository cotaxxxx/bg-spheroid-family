# D-PRO C21 H heavy slab — reproducible adaptive H diagnostic
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**. 2026-11-18.

Exact plate λ=[79/16,5] unsplit; Rτ=[0,1]² initial 4096 boxes of edge1/64.
Longest-edge adaptive binary split only when rigorous H interval includes 0,
min edge1/256, R wins tie. 12 workers, per box1200s, aggregate36h wall cap.
Never call a partial checkpoint a full slab or a proof.

## One-line reproducible resume command
```bash
cd /home/daybreak/D_PRO_C21_H_HEAVY_SLAB_20261118/worktree && PYTHONPATH=/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source /home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python -u -m prolate_r4.c21_heavy_pipeline --session-seconds 129600
```

Session can be bounded with `--session-seconds 800 --max-batches 1`.
This is an explicit SHORT session and may leave 4,096 nodes pending.
Exact fixed plan and root registry in PRE_RUN_FREEZE.md and REGISTRY.json.

Fixed routes by position only:
- Axis tau_hi=1 (takes precedence even for axis+boundary, may return OPEN)
- Center R_lo=0
- Boundary R_hi=1, kappa1/4096, analytic cap error added ONCE
- General elsewhere
Point and 3 gradients 16x32, ratio1/2 order4.
6 Hessian integrals 8x16, ratio1 order4.
All 0th derivative signed quadrature uses Taylor, not unsigned range.

Results:
- STATE.json restartable checkpoint, SUMMARY.json exact fraction areas,
- boxes/*.json and logs/*.log for all completed/OPEN evaluated nodes,
- TUBE_DISTRIBUTION.svg: ONLY evaluated terminal tube distribution;
  PENDING remains gray.
- W_DEFERRED.json until actual full slab completion or real36h cap.
- RUN_RECEIPT.md measured counts and route/depth worker seconds;
- CHECKER.json rational arithmetic ledger (not independent mathematical proof);
- SHA256SUMS, deterministic ZIP, ZIP_SHA256.txt and original R3 pins.

R3 frozen branch `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`.
User-designated target branch research/d-pro-c21-h-heavy-slab-20261118.
Never update main, STATE.md, old branches, tags, or Julia.
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**.
