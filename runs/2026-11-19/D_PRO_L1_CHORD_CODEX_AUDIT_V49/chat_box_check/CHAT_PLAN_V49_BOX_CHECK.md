# chat V49 box check plan (fixed before run) — DIAGNOSTIC_ONLY / NOT_EVIDENCE

Purpose: independent (chat's own code) rigorous upper enclosure of H over selected leaves of Codex's finite cover
(commit 05d1706, cover_5/6/7.tsv.gz), using the chord formula (3) DIRECTLY (no (6), no moment tables, no Codex code).

- Kernel: (3). Average over e: m in [0,1] (pair symmetry), psi in [0,pi] (y-reflection). Upper bound = sum over cells of
  interval upper of integrand x cell measure. Arb 128 bit (python-flint 0.8.0).
- F' upper: P_N^+ = 2 sum_{n<=16} a_n h^n + 4 a_17 h^17; Q lower: sum_{n<=16} q_n h^n; h=(1-gamma)/2, gamma clipped to [0,1].
  w_sigma clipped to [0,1]; B_sigma intersected with [eps^2, 1].
- Grid: N_m = 256 equal m-cells, N_psi = 32 equal psi-cells.
- Boxes: (a) the leaf with the largest rational upper bound in each of cover_5, cover_6, cover_7 (3 boxes);
  (b) 20 leaves drawn uniformly (Python random, seed 49) from all negative leaves of the three covers.
- If a box's upper bound is >= 0: bisect along the dimension with the largest score (8*dr, 8*dz, dlambda; Codex's rule),
  depth <= 4; a box counts as confirmed only if all its final children have upper < 0. No other changes after results.
- Binary outputs per box: confirmed (all children negative) yes/no; plus the max upper and the number of children.

## Amendment 1 (implementation bug only; grid, thresholds, sample and rule unchanged)
Run 1 returned NaN upper bounds: sqrt of intervals 1-m^2 and delta+v^2 whose lower ends dip below 0 by interval
overestimation produced indeterminate balls. Fix: intersect 1-m^2 with [0,1] and delta+v^2 with [0,4] before sqrt
(both are exact true ranges). Run 1 output kept as cb_box_check_run1_NaN_bug.jsonl.
Amendment 1b: arb balls after intersection can still reach slightly below 0 (midpoint-radius form), so the two square
roots use sqrtp(x) = [sqrt(max(lower,0)), sqrt(upper)]; valid because the true values are >= 0. No other change.
