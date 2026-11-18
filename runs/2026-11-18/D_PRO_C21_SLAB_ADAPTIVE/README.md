# D-PRO (C21) — adaptive H slab research pilot
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

Source: C21 H `5004ebdc6e038bcdb3122f563ffb15d38070d8b6`;
chat V37 `949e9dff7b48cf993cdb9fae95ec698f482cd591`;
R3 source `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`.

Target: only λ∈[1279/256,5]; (R,τ)∈[0,1]². Not all λ.
Python 3.11.16, python-flint 0.8.0, Arb 128-bit.
All code and rules in `prolate_r4/slab_*.py` and
`runs/2026-11-18/D_PRO_C21_SLAB_ADAPTIVE/COVER_RULE_FREEZE.md`.

The preregistered AX/CE/BD calibration `calibration_status.json`
**must exist before the adaptive controller starts**.
Run once before the adaptive phase:

```bash
cd /home/daybreak/D_PRO_C21_H_SLAB_20261118/worktree && PYTHONPATH=/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source /home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python -m prolate_r4.slab_calibrate
```

**Single-command actual 12-worker slab pilot (up to remaining overall 24h):**

```bash
cd /home/daybreak/D_PRO_C21_H_SLAB_20261118/worktree && PYTHONPATH=/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source /home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python -u -m prolate_r4.slab_adaptive --workers 12 --session-seconds 86400
```

The 24h cap includes the measured calibration wall time. The
controller loads `state.json` and **resumes** across sessions.
A one-batch interactive partial subrun is expressly frozen in
`INTERACTIVE_SUBRUN_FREEZE.md`; it is **not** the full slab run.

Optional source consistency check:

```bash
cd /home/daybreak/D_PRO_C21_H_SLAB_20261118/worktree && PYTHONPATH=/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source /home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python -m prolate_r4.slab_verify
```

Once the complete slab or hard 24h cap has actually been reached, run the
**three-box W-only** measurement (with remaining global time budget):

```bash
cd /home/daybreak/D_PRO_C21_H_SLAB_20261118/worktree && PYTHONPATH=/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source /home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python -m prolate_r4.slab_w_sample
```

No W full-tube cover is computed. All H sign statements are diagnostic
metadata; the selection logic uses only whether an interval contains
zero, never which sign was observed.

Files: `boxes/` and `logs/` per fixed ID, `state.json`
checkpoint, `summary.json` with exact rational area accounting,
`checker.json`, `calibration_status.json`, and final SHA/ZIP.
A run with pending boxes has an **OPEN** slab scope; it must never
be represented as a fully measured adaptive cover.

No writes to main, STATE.md, frozen Julia, original R3 or C21 branches.
