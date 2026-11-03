# FT_q V3 — recovered evidence for independent audit
Date: 2026-11-04 JST. Target: μ16 / P-only / 4096 branches.
Branch: `audit/ftq-v3-recovery-20261104`.
This branch is an audit handoff. **Do not treat recovery or SHA matches as mathematical certification.** No changes to main/STATE, B7, D5 or existing evidence.

## Files already present and independently fetched back from GitHub

| Filename | SHA-256 |
|---|---|
| `FTQ_V3_JOINT_CONSTRAINT_ARCHITECTURE.md` | `e6660d52caf482837961962d4df5bf53b335fa4d8529849a6303b142cfcec62b` |
| `FTQ_V3_EXACT_PRODUCTION_REPORT_20261017.md` | `6b9e51e5a13d7dcef09fa04c96b0510bd22e552fa477903e32bd5058cb282d6d` |
| `FTQ_V3_EXACT_M0_20261017.txt` | `207b9617d61645e2c89f125debac2e40576f11f790feb09f81471564a1fd7d17` |

`FTQ_V3_CHAT_RECOVERY_REPORT_20261104.md` also records the recovered material and unresolved gaps.

## Verified locally but not yet transferred to this GitHub branch

| File | SHA-256 | Contents/status |
|---|---|---|
| `FTQ_V3_RECOVERED_PARTIAL_BUNDLE_20261104.zip` | `f36e020d3819ca3ffaca0f82cc1b9760f2229612ddab01220bae7520ab48a102` | 7,803 files, incl. 4,096 numbered branch certificates, plus 3,698 of 4,096 checker records; regenerated ZIP central directory. **PENDING UPLOAD** |
| `FTQ_V3_RECOVERY_REFERENCE_20261104.zip` | `851d16ce0d98ece92304650608d316ebccd0cc657e0d738d92bdf8ecf60cbd39` | partition manifest, SHA ledger and readback. **PENDING UPLOAD** |
| `L3_V0_2_AUDIT_BUNDLE_20261017.zip` | `e6a0edf5cc66e1876478dfb7cda112db4b9a5adc0fd4533e125b17f051abf085` | L3 source ledger and audit. **PENDING UPLOAD** |

The complete V3 audit bundle recorded on 2026-10-17 has SHA-256 `abd1202ca69e815eddc83919cee3797d67875a3020635735dc312818eca60f93`, which is **not** the same as the recovered partial ZIP. Do not label the recovered archive as that original file.

## Independent audit gates

1. Match architecture, frozen source and partition SHA-256.
2. Verify exactly 4,096 branches, exact rational multipliers, residuals, nonnegative Bernstein coefficients, positive denominators and primal/dual identities using independent code.
3. Recompute all 16 parameter-cell sums and exact minimum `m0`, and compare against recovered exact value. Claimed signed distribution is 2,230 / 0 / 1,866.
4. Separately audit inherited P1 normalization, paired-density interpretation, boundary extension and NP-T connection.
5. Report PASS/PARTIAL/FAIL by the evidence actually checked; Judge alone rules on FT_q/L3/STATE promotion.

## Missing from the archive

The original production producer and checker executable sources, 398 trailing checker outputs, final `result.json` / `checker_result.json`, and the old chat-side independent-recalculation files have not been recovered.

**Status: PARTIAL EVIDENCE RECOVERY. Mathematical independent audit: OPEN.**
