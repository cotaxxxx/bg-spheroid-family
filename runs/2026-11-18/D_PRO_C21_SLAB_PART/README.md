# D-PRO C21 — Partial Thin-λ H Survey

**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

Scope: λ=[1279/256,5] (unsplit), R=[1/4,1/2], τ=[0,1],
exact normalized (R,τ) area 1/4. Outside this region remains OPEN.

Input source: Judge's replacement §2 (2026-11-18) of
original committed instruction `884a735d419715628a01789fd7a896bcf7a4f8e2`;
C21 original `5004ebdc6e038bcdb3122f563ffb15d38070d8b6`;
V37 audit `949e9dff7b48cf993cdb9fae95ec698f482cd591`;
pinned R3 `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`.

Frozen method `PRE_RUN_FREEZE.md` committed as `d71522c...`
BEFORE CE calibration. The exact 1024-box controller sources
were separately committed as `61069b5...` BEFORE any H jobs.

## New MVT path
For rho-small or τ_hi=1 routes, replace 4-panel s-Simpson by
H=∫₀¹ Eρρ(sρ,z)ds and enclose Eρρ on an independent
box rho'∈[0,rho_hi], z∈[z_lo,z_hi], λ on the slab.
Signed Taylor angular integration order4, 16×32 base, ratio1/2,
128-bit Arb, python-flint0.8.0, frozen positive-denominator
bounds. Fixed rotation of angular integration variables uses
the midpoint of the original τ chart (not a varying chart).
If D² positivity or mesh resource bound fails: OPEN.
No fabricated interval, and no unsigned angular integral
used for signed derivative coefficients.

## Command (one line; resume in place)
```bash
cd /home/daybreak/D_PRO_C21_H_SLAB_PART_20261118/worktree && PYTHONPATH=/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source /home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python -u -m prolate_r4.c21_slabpart_adaptive --workers 12 --session-seconds 86400
```

CE calibration completed before this command's initial run; no need
to repeat it. State `state.json` is crash-resumable with
`inflight` recovery. The global wall cap is 24 hours including CE.
The controller may also be called with `--max-batches 1` and
`--session-seconds 620` for a clearly PARTIAL interactive test,
but do not claim completed subregion metrics for such a test.
The frozen input consists of 1024 1/64×1/64 boxes, with
bisects to both edges 1/256 when intervals contain zero.

## Output and audit
- `boxes/`: one JSON per executed immutable H ID, including OPEN
- `logs/`: full stdout/stderr per worker
- `state.json`: exact partition and crash-restart state
- `summary.json`: exact rational area decided/tube/pending,
  plus normalized area dividing by target measure1/4
- `checker.json`: source and exact-area consistency, not
  independent mathematical proof
- `CE_mvt.json`, `CE_calibration_status.json`: one-box MVT
  preregistered calibration
- `W_SAMPLE_DEFERRED.json` or `W_SAMPLE_RESULTS.json`: no
  tube-wide W work; three R3 quadratic W test boxes only once
  entire requested subregion completes or 24h cap reached
- `RUN_RECEIPT.md`, `SHA256SUMS`, deterministic ZIP, ZIP hash.

Optional strict checker:
```bash
cd /home/daybreak/D_PRO_C21_H_SLAB_PART_20261118/worktree && PYTHONPATH=/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source /home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python -m prolate_r4.c21_slabpart_verify
```

W three-box sample (ONLY when freeze condition holds):
```bash
cd /home/daybreak/D_PRO_C21_H_SLAB_PART_20261118/worktree && PYTHONPATH=/home/daybreak/D_PRO_R1_COROTATION_R3_DIG_20261117/source /home/daybreak/D_PRO_R4_RATMODEL_BOX2_CHAT_20261118/.venv/bin/python -m prolate_r4.c21_slabpart_w
```

The original R3, original C21, earlier slab branch, main,
STATE.md, tags, and frozen Julia sources are unchanged.
All results **DIAGNOSTIC_ONLY / NOT_EVIDENCE**. Global status OPEN.
