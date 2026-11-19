# chat V49-B box check plan (new plan version, fixed before run) — DIAGNOSTIC_ONLY / NOT_EVIDENCE

Plan A (CHAT_PLAN_V49_BOX_CHECK.md) was too loose to decide: the 4 boxes finished all ended with positive upper
bounds after depth-4 bisection (and one NaN). That is wrapping of chat's naive enclosure, not a sign result.
Plan A outputs are kept (cb_box_check_run1_NaN_bug.jsonl, cb_box_check_planA_run2.jsonl).

Changes (enclosure method only; same 23 boxes, same selection rule and seed):
- Per side sigma: u_sigma = upper(pos_sigma - neg_sigma) on the cell. Combine with sum w = 1:
  sum_sigma w_sigma u_sigma <= u_min + sup(w_argmax) (u_max - u_min).   (same structure as Codex (6), chat's own code)
- B_sigma = eps^2 + (1-eps^2) * clip(1 - xz^2, 0, 1), intersected with eps^2 + (1-eps^2) clip(xi_x^2 + xi_y^2, 0, 1).
- Grid: N_m = 512, N_psi = 64 on [0, pi].
- Bisection depth <= 6 with Codex's score rule.
- Binary per box: confirmed (all final children upper < 0) yes/no.
Amendment B1 (implementation only): arb .intersection() produced indeterminate results downstream (NaN after sqrt) in the
[7,8] box; clip() now builds [max(lower,lo), min(upper,hi)] explicitly from endpoints. No change in grid/rule/sample.
