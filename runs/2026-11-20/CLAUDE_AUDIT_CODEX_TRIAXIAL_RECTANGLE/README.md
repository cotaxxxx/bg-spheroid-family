# Claude Code による監査：Codex の主矩形の区間台帳に対する点ごとの包含検査

2026-11-20 ／ **DIAGNOSTIC_ONLY / NOT_EVIDENCE** ／ 検査側の数値は非区間

対象は branch `codex/triaxial-rectangle-interval-20261120`（commit `43854bc`）の `runs/2026-11-20/CODEX_TRIAXIAL_RECTANGLE_INTERVAL/` と `CODEX_TRIAXIAL_FIRST_ATLAS/` である。結果は `AUDIT_REPORT.md` にある。

- 監査のスクリプトは、検査側の核（`../CLAUDE_TRIAXIAL_FIRST_MAP/triaxial_map_20261120.zip` の中の `code/`）を使う。原本の配置では、スクリプトの 1 つ上の階層に `code/` がある。
- 原本の場所：`cotaxxxx/basepoint-geometry`、branch `ccr-1e5ce365-5ksfyr`、commit `f3170e6`、`diagnostics/triaxial_map_20261120/audit_codex_rectangle/`。
- この監査は、区間演算そのもの、求積の剰余、被覆の完全性を検査していない（`AUDIT_REPORT.md` の §4）。
