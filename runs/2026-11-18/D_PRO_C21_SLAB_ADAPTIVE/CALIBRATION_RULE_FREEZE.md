# D-PRO C21 / slab calibration: pre-run fixed rules
2026-11-18 — DIAGNOSTIC_ONLY / NOT_EVIDENCE

Source: C21 pilot commit `5004ebdc6e038bcdb3122f563ffb15d38070d8b6`, V37 `949e9dff7b48cf993cdb9fae95ec698f482cd591`; frozen R3 `fdfb498f2117cc0c5d72e88cc3be05eac9727bd8`.

**Calibration precedes ANY slab adaptive-cover computation.**

Exactly three fixed previous C21 representative boxes:
- AX R=[63/128,65/128], τ=[63/64,1], λ=[1279/256,5].
- CE R=[0,1/64], τ=[63/128,65/128], λ=[1279/256,5].
- BD R=[63/64,1], τ=[63/128,65/128], λ=[1279/256,5].

All use python-flint==0.8.0, 128-bit, one process per box,
signed spatial Taylor order 4, base_u=16, base_v=32, ratio=1/2,
R3 geometry mesh, max_depth=28, max_cells=40000.
- AX, CE: original C21 `f_rho_rho` 4-panel Simpson in s, with rigorous s-error and signed angular Taylor coefficient integrals.
- BD: original C21 horizontal `f_rho/rho`, cap κ=1/4096 added once.
- Fixed per-box subprocess wall caps: AX=600s, CE=600s, BD=300s.
- Run in **three separate, parallel subprocesses**; each independently records own wall time and peak RSS. This calibration's wall time is the interval from batch submission to all three completion/timeout.
- On any exception, timeout, or unproved bound, store `OPEN`, never a synthetic interval.
- Center reference values from primitive E are only diagnostic; no sign used to choose a rule.

**No mesh, threshold, or route may change in response to the results of this calibration run.**
The adaptive slab rule will be committed separately, *after* the calibration results are recorded.
