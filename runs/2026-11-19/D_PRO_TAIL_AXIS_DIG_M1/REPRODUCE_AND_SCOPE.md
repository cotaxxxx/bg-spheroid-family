# Reproducibility, provenance, and non-adoption controls

2026-11-19. DIAGNOSTIC_ONLY / NOT_EVIDENCE.

- Judge instruction: repository cotaxxxx/bg-spheroid-family, branch evidence/c-gap2-freeze-20261115, exact commit 00024f8e62dafc8ce3bf0f7579f3f7b9ab46d4fb, file runs/2026-11-19/D_PRO_NONPOLAR_ASTRA_AUDIT_V45/ASTRA_INSTRUCTION_D_PRO_TAIL_AXIS_20261119.md.
- Base was copied from the above Git commit. Follow-up Judge limitation: no changes to PID 1581407; math §4(1)–(4) precedes numerical work; small pre-frozen interval prototype; new branch, SHA-256, no STATE/main/ledgers changes.
- Fixed mathematical derivation MATH_DERIVATION_BEFORE_PROBE.md SHA-256 9373ac07c721c99b1ffa2b683d9f560e4fb1cea0dad124054b8eb14ef8cfa7f8.
- Frozen numerical plan PLAN_TAIL_AXIS_BEFORE_RUN.md SHA-256 0fb1fbf4e1cfbd77bfb860cb5825217fcc1b7b0975011e978908e1f628cbea86.
- Python on authorized device with python-flint 0.8.0, precision 192 bit, one CPU nice+15. No time limit modification, no adaptive grid.
- To reproduce the diagnostic, make a NEW copied working directory with these files, check the plan SHA and run tail_axis_small_probe.py. Do not overwrite the frozen original outputs in the archived package.
- check_tail_axis_probe.py checks raw rational interval endpoints, overlap of two algebraically equivalent residual evaluations, time/width consistency, and exact rational axis-reflection identities; it DOES NOT independently re-integrate or audit the mathematics.
- Results are only about the ε=0 inner-limit angular kernel for q=(ρ,z)=(1/2,0) at four t nodes. They are not intervals for finite λ H, nor a global result for λ≥5, nor proof for E_z/z on the axis.
- MATH_ADDENDUM_POST_PROBE.md was produced AFTER the numerical pilot, so its suggested second subtraction was NOT among the predeclared numerical pass/fail metrics. No second-tail numerical measurement was retrospectively added.
- Earlier UN20 box queue and the C21 heavy slab were left unchanged. The existing STATE.md, main and evidence branches were not altered.
- The notebook-style printed decimal summary in DIG_REPORT_TAIL_AXIS_20261119.md is for display only. Use the JSON rational lower and upper endpoints for every mathematical comparison.
- Novelty/prior-art, independent verification of the new analytic formulas, and Judge acceptance remain OPEN.
