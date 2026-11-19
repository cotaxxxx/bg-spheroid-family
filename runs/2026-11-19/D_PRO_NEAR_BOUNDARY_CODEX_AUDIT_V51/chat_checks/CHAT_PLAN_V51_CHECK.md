# chat V51 check plan (fixed before run) — DIAGNOSTIC_ONLY / NOT_EVIDENCE
Target: Codex near-sphere/boundary bundle (commit a2d394b, ZIP sha256 17273548...), final/ ledgers, lambda in [1,2].
chat's own Arb code (chat_vz_check_B.py functions + new chord functions), not Codex's kernel:
- E leaves (all 15): action H_positive -> chord (3) i=y LOWER > 0; action radial_curvature_negative -> chord (3) i=x
  UPPER < 0. Per-side bounds combined with w_+ + w_- = 1. Grid m 512 x psi 64 on [0,pi].
- B leaves (all 9): H_b by (9) (verified numerically against the chord limit in V50) LOWER > 0; t 512 x phi 64 cells.
- V leaves: 3 weakest + 5 random (seed 51) -> lowerV (V50-B) > 0. Z leaves: 3 weakest -> lowerZ > 0.
- Bisection depth <= 4 (largest of dl, 4 dr, 4 dz; B leaves: dl). Confirmed iff all children satisfy the sign.
