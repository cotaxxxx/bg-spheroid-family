# PLAN AXIS WIDE 1

2026-11-20 / DIAGNOSTIC_ONLY / NOT_EVIDENCE

Purpose: extend the three already recorded local axis branches to wider shape boxes, with no change to their radius brackets. This is a new, separately frozen plan after PLAN_AXIS 1; the narrow-box outcomes remain intact.

Shape boxes, with denominator 65536:
- WA: s in [81664,82176]/65536, t in [196352,196864]/65536.
- WB: s in [134144,134656]/65536, t in [196352,196864]/65536.
Each coordinate width is 1/128. WA contains the original A box and WB contains B.

Fixed candidates and expected signs:
- WA axis 1, r in [3/8,1/2], Hessian signs (-,+,+).
- WA axis 2, r in [27/32,29/32], Hessian signs (-,-,+).
- WB axis 2, r in [7/8,15/16], Hessian signs (-,-,+).
- Centers: WA (+,+,+), WB (-,+,+).

Execution order: the two centers, then WA axis 1, WA axis 2, WB axis 2. One process only. Budget: 300 seconds of this process's user+system CPU time, with a SIGXCPU handler and hard limit 305 seconds. Check the budget before each stage and stop launching new stages at 285 seconds. A raised CPU-budget signal retains all completely written rows and records termination in the summary. Do not restart after this budget.

Centers use M=128,256,512,1024,2048 in that order. Gradient endpoints use M=256,512,1024,2048,4096,8192. Each radius bracket is tried with 8 then 16 equal dyadic panels; each panel uses M=128,256,512,1024,2048, doubling only until the required Hessian signs and Ux<0 hold. There is no further refinement. If endpoint signs remain unresolved at the declared cap, retain that result and proceed to the next case without spending time on its derivative cover. If a derivative cover is incomplete, preserve its unresolved status. Always retain all stages.

The kernel is the byte-identical axis_interval.py fixed by PLAN_AXIS 1, SHA-256 09a1747b77163068910e293dec3bee1b2cb6f5b72460bce6dd131db90c68004e. The new axis_wide.py wrapper supplies only these wider interval inputs and the above execution/budget/recording rules. It explicitly replaces that imported module's shape-input function for this process, with the same formula A=(1,s²,(st)²). The mathematical kernels, rounding, angle series, quadrature coordinates and cutoff intersections do not change.

Outputs: out/axis_wide.csv (all stage bounds), out/axis_wide_run.json (budget/completion and frozen-file hashes), out/axis_wide_check.json (complete-cover/sign check, if produced). Numerical sanity comparisons are optional and never promoted to interval evidence. The inability to settle a wider box does not invalidate the retained narrow-box result.

Limitations: only the three radius brackets and centers are attempted. No exterior axial root exclusion, off-axis exclusion, boundary/collar calculation, global root count or global main-rectangle estimate.
