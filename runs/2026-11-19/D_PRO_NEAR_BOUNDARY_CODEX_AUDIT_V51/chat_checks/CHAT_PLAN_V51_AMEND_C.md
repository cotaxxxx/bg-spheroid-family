# Amendment C (fixed before run) — DIAGNOSTIC_ONLY / NOT_EVIDENCE
Observed (chat tool): near |q| = 1 at lambda ~ 1 the V enclosure of chat's lowerV2 is wider than the value.
Non-interval reference (chat_vpoint.py, mpmath quad of (2)) at (1.0039, 0.95459, 0.25494): E_z = 0.08789
(sphere axis check: E_z/z = 1.27744 at r = 1/4 vs 4/3 - 8r^2/9 = 1.27778); lowerV2 on that point box = -0.0254.
Grid tuning on that reference point only (chat_lowerV3.py): base mu 1024 x phi 192, band |mu - z| < 1/4 with mu x4,
phi cells k < 16 x4, k = 0 x16 gives point lower 0.0609. This grid is used for the V leaves still unconfirmed after
B2 (4 leaves), depth <= 6, empty sub-boxes dropped. Confirmed iff all children positive.
