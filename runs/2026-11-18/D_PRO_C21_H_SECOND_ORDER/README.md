# C21 second-order H outer Taylor diagnostic
**DIAGNOSTIC_ONLY / NOT_EVIDENCE** — 2026-11-18

## Frozen inputs and policy
- Original C21 commit `5004ebdc6e038bcdb3122f563ffb15d38070d8b6`.
- Prior 84-box diagnostic `2e3a091ad3c7a98a5962b8c016d2e1fb51bcf0e9`.
- V38 audit `922a2c7eaed62b6c40d1bf9b0e956f98a85fd104`.
- R3 frozen `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`.
- Pre-run fixed 8-sample selection and Hessian rule:
  `PRE_RUN_FREEZE.md`, commit `4760c534b02621c5a31a9befc6469495fb8d9c4b`.
- Stage A selects 6 historical general boxes by fixed sorted indices
  and 2 axis boxes; Stage B starts **new** 1024-box controller only
  when all 8 complete AND new halfwidth <= original halfwidth.

## One-line reproducible command (resumes)
```bash
cd /home/daybreak/D_PRO_C21_H_SECOND_ORDER_20261118/worktree && PYTHONPATH=/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source /home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python -u -m prolate_r4.c21_second_pipeline --session-seconds 86400
```

Working environment: research PC, Python3.11.16,
python-flint0.8.0, R3 signed angular Taylor order4,
base_u16/base_v32, ratio1/2, precision128.
Run only with frozen R3 in PYTHONPATH.

## Stage A
- Producer: `prolate_r4/c21_second_order.py` (general: R,τ,λ;
  MVT: independent rho',z,λ).
- Driver: `prolate_r4/c21_second_stage_a.py`.
- `stage_A_boxes/*.json`, `stage_A_logs/*.log`,
  `STAGE_A_GATE.json`. Compare exact halfwidths from rational
  H endpoints; never use approximate rounded bounds for gating.
- Per box hard limits: 1800s general / 2400s axis MVT;
  8 workers, combined run 24h cap for both stages.

## Stage B, only if gate passes
- Fresh adaptive controller:
  `prolate_r4/c21_second_cover.py`.
- The target region is strictly λ∈[1279/256,5] unsplit,
  R∈[1/4,1/2], τ∈[0,1], initial 16×64=1024 rational boxes,
  edges shrink to at least1/256; 12 workers.
- B output path: `STAGE_B/state.json`,
  `STAGE_B/summary.json`, `STAGE_B/boxes/*.json`,
  `STAGE_B/logs/*.log`. Exact normalized area ledger:
  decided+tube+pending=1/4; pending is never counted as tube.
- Re-run within remaining global 24h budget using the same
  one-line command. Inflight work is requeued after interruption.
- Independent consistency checker:
  `python -m prolate_r4.c21_second_verify`
  (not mathematical proof). R3 W sample:
  `python -m prolate_r4.c21_second_w`; 3 candidates only
  after completion or true24h cutoff, not full tube W.

## Evidence
- `RUN_RECEIPT.md`, full signed Taylor decomposition per
  H box, one-line `RUN_COMMAND.txt`, `SHA256SUMS`,
  deterministic ZIP and exact ZIP_SHA256.
- Mathematically based on multidimensional Taylor's theorem,
  described in `prolate_r4/ANALYSIS_C21_SECOND_ORDER.md`.
- Hessian producer arithmetic still requires independent
  interval audit. No full-λ theorem is claimed.

No main/STATE.md/older branches/tags/frozen Julia edits.
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**.
