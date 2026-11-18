# DIG HANDOFF — JUDGE R63_T63 ADOPTION & POST-RUN HEAVY SLAB SUMMARY
2026-11-19 / Judge adoption verified against commit 546986fa7192e6e91b50cb36dfaef2bb75dd2c2e
**JUDGE ADOPTED STATIONARY EXCLUSION, NOT AN H SIGN CERTIFICATE**

## Sources transferred
- `inputs/JUDGE_RULING_R63_T63_ADOPT_20261119.md` exact GitHub blob SHA-256 ca139ca89f488d43927935588d3d1bba71b5601150c6e785cf47e652c2f3c827. Original commit `546986fa7192e6e91b50cb36dfaef2bb75dd2c2e`.
- Independent audit V44 `de7569d6126e9ad962892f2eac4a3c580b4956f3`; independent G9 mathematical audit V43 `cf541c0`; Dig 128 box cap `fe83a02f96523a4fe6604bc948b77edda917d3f6`.
- `inputs/ASTRA_INSTRUCTION_D_PRO_NONPOLE_REMAINDER_20261119.md` exact GitHub blob SHA-256 d1635aa1bea69dd733f90375329073d568b87fff87b55b0c927160ea0d05e0af. This request was FOUND IN GitHub evidence/c-gap2-freeze-20261115, not evidenced as already DELIVERED to separate Astra session; HANDOFF READY, not an Astra receipt.

## Immediate task: supplementary ledger
Use `ledger/JUDGE_ADOPTED_R63_T63.json` as the dated **Judge-adopted overlay**. This overrides the prose interpretation "waiting for dedicated axis-boundary route" for stationarity purposes.
The original frozen H controller retains `TUBE_OPEN_ERROR` for `R63_T63` and `H_interval=null`, because H was NOT evaluated. Do NOT edit that controller, original box JSON, `STATE.json`, or `SUMMARY.json` while 36h process is running.

Classification:
- `E_z>0` excludes **interior stationary points** of `R63_T63`, including axis.
- `H` sign is unknown; root NOT counted as H-DECIDED.
- `R=1` is boundary trace only; original condition B remains to be handled.
- Root area `1/4096` counted exactly once; category "adopted stationary exclusion (E_z)" split out of original OPEN/TUBE, never added on top.
- No need for separate polar axis-boundary route to rule out *interior stationary points* in this root.

## After current heavy slab process ends (not before)
Running process: PID `1581407`. **DO NOT stop/restart/change its workers**. After natural completion or 36h cap, validate no running process and state contains no inflight. Run `python3 ledger/postrun_aggregate.py --write` from this handoff directory (or equivalent) on the completed original `runs/2026-11-18/D_PRO_C21_H_HEAVY_SLAB/STATE.json`.
Aggregator must report:
  A. Original H-sign-decided boxes and area, untouched.
  B. Exactly one Judge-adopted E_z stationary exclusion `R63_T63`, area 1/4096.
  C. Remaining unresolved H tubes/OPEN and their area, separately.
  D. Pending/unevaluated area (never counted as sign-decided or tube).
  E. Exact fractional identity A+B+C+D=1 and box counts, route/depth and worker/wall times.
  F. Whether the full slab was actually completed or capped with pending work; no fictitious completion.
  G. W 3-box sampling per preregistered rules, if condition is met, separately from E_z analytic exclusion.
  H. Full λ domain cost extrapolation ONLY if actual representative data support it.

`postrun_aggregate.py` is provided as a read-only state/accounting helper and can print an interim snapshot; it only writes final archive when `--write` and heavy process stopped with empty inflight. Existing H evidence/STATE must not be rewritten.
Please register the FINAL Dig summary in a fresh evidence commit/branch after run. Judge controls adoption of any additional conclusions.

## Astra remainder request
The exact instruction is in `inputs/ASTRA_INSTRUCTION_D_PRO_NONPOLE_REMAINDER_20261119.md`, aiming at practical `Lambda_0<=10` in nonpolar region without relying on unverified giant P10 constants.
This handoff is accessible to Dig through the authorized remote machine and to Astra via a shareable GitHub link; it is **NOT** proof of direct delivery into Astra's separate chat/session. Do not assert sent-to-Astra or received-by-Astra without a separate acknowledgment.
