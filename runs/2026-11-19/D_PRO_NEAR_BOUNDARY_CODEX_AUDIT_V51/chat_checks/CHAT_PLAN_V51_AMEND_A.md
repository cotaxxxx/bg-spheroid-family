# Amendment A to CHAT_PLAN_V51_CHECK (fixed before run) — DIAGNOSTIC_ONLY / NOT_EVIDENCE
Reason (chat tool, not Codex): with t 512 x phi 64 cells the H_b enclosure width (~0.05, measured by chat_hb_width.py,
mostly cell width in t) exceeds the margin for B03 leaves (lambda in [1.75,2]); 6 of 9 B leaves were not confirmed.
Original outputs are kept (nb_check.jsonl). Change for the unconfirmed B leaves only:
- grid t 2048 x phi 256 (uniform), lambda bisection depth <= 3. Confirmed iff all children have H_b lower > 0.
