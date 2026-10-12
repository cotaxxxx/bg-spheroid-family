# C_GAP1 v9 / v9.1 diagnostics — NOT_EVIDENCE

Classification: **NOT_EVIDENCE**. These records are pre-diagnostics only and must not be promoted to formal run4 evidence.

## v9 boundary-search diagnostic
- unchanged v0.4.1 body kernel
- visited-attempt record count: 45
- X checks in the v9 search passed; L did not pass through the m=109 limit
- terminal line: `STOP L_DIAGNOSTIC_EXHAUSTED m=109`
- this STOP is certificate/method inconclusiveness, not a mathematical counterexample

## v9.1 parallel body diagnostic
- requested new coverage: X slabs 48..116 (69), L slabs 0..47 (48)
- result: **117/117 PASS**
- error files: none; missing results: none
- calls `attempt_x` / `attempt_l` only; this is a **body diagnostic**, not endpoint-gate or full-driver acceptance
- JSON `leaves` arrays are visited attempt records (including internal attempts), not a claim that every possible sibling leaf was visited
- the parent parallel runner is retained only as historical diagnostic material; it is **not fail-fast** on worker nonzero exits and must not be used for run4

## Commit identity note
- implementation commit named by the contract: `70af038bd44945780bb7e94149a54c77fa177ed0`
- diagnostic worktree HEAD: `d68dfd918b73f3de0158947f5330ee2605646a4b`
- the latter is the direct child used in run3; the diagnostic classification here does not change formal run4 pinning requirements.
