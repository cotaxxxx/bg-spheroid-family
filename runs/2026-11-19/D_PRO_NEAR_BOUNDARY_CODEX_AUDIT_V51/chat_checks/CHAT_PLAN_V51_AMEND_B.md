# Amendment B to CHAT_PLAN_V51_CHECK (fixed before run) — DIAGNOSTIC_ONLY / NOT_EVIDENCE
Observed (chat tool, not Codex): every unconfirmed V/Z/E leaf touches or nearly touches |q| = 1
(r^2+z^2 upper >= 0.82). Causes in chat's code: lowerV returned None when a cell admits D = 0 (contact cell);
grids were not refined near the contact direction; depth 4 left boxes too wide.
Changes, applied only to the leaves left unconfirmed by nb_check.jsonl (outputs kept):
- lowerV2: contact cells use the a-priori ranges gamma in [0,1], u_z in [-1,1] (valid for every q in the closed ball)
  instead of returning None; phi-cell k = 0 inside the refined mu-band is split into 32.
- chord (H, E_zz): grid m 1024 x psi 128.
- bisection depth <= 8, same score. Points of a box outside the ball are not claimed; every clip used is valid for
  points inside the ball, so the bound holds on box ∩ ball.
Confirmed iff all children satisfy the sign.

## B2 (fixed before re-run)
Run 1 of B (nb_B_run1_noempty.jsonl, kept) did not drop sub-boxes lying outside the ball: depth-first search went to
the outer corner child. Fix: a sub-box with rho0^2 + z0^2 >= 1 (its lower-left corner, rho, z >= 0) meets the open
ball in the empty set and is dropped, as in Codex's cover. Nothing else changes.
