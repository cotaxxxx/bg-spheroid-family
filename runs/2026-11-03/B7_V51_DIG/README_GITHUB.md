# B7 V5.1 — Dig audit handoff (2026-11-03)

**Status: D0 8/8 PASS reported, B7 global 8/40 PASS and 32/40 OPEN. V5.1 independent Claude audit pending.**

The code retains V5 K'=275/4 and its bound_policy. It changes only the zero-gain inner fallback, the source filename pin, and priority_rule text.

- [Source and tests ZIP](B7_V51_DIG_SOURCE_TESTS_20261103.zip) (413,739 bytes; SHA256 `4e5fb2dec83df90bba7693892e1e6a6edd9e3e34e96953d3c43ce00fcaffeec8`).
- [V5 → V5.1 three-hunk patch](V5_TO_V51_DIFF_20261103.patch)
- [Source code](v6_b7_unified_outerrem_v51.py)
- [V5.1 checkpoint recertifier](dig_b7_v51_recert.py)
- [64-cell test results](TEST_REPORT_V51_20261103.md) and [machine-readable report](TEST_RESULTS_V51_20261103.json)
- [User-reported prior D0 audit status](D0_AUDIT_STATUS_REPORTED_20261103.md)
- [SHA manifest](SHA256_MANIFEST_V51_20261103.txt)

The 64-cell tests use a synthetic contact cutoff to prevent early success and **do not certify any entire outer box**. V5 stopped without splitting, V5.1 completed 150 splits; exact J decreased by 72 dyadic raw units from outward rounding, not an improvement in this test. The same source intervals matched exactly across all 64 initial leaves. Checkpoint interruption/restart matched the uninterrupted leaf SHA256. The original V4/V4.1 jobs have been stopped, and D1-D4 32-box production has NOT started pending independent audit.
