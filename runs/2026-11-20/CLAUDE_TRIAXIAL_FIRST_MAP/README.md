# Claude Code の成果：三軸楕円体の族の最初の地図（診断用）

2026-11-20 ／ **DIAGNOSTIC_ONLY / NOT_EVIDENCE** ／ 数値はすべて非区間

指示書「体積を保つ三軸楕円体の族：停留点の構造の定式化と、最初の地図」を、Codex と並行して実行した結果である。
この branch（`claude/triaxial-map-audit-20261120`）は Claude Code 専用の新しい branch で、main、STATE.md、公式の台帳、既存の branch には書き込んでいない。

| ファイル | 内容 |
|---|---|
| `REPORT.md` | 報告書（定式化、数値の地図、分岐集合の分類、証明、証明の設計、Judge への判断点） |
| `fig/` | 図 1（楔の上の地図）、図 2（主平面） |
| `triaxial_map_20261120.zip` | 計画、コード、出力、図、再現手順の一式 |
| `*.sha256` | 報告書と ZIP の SHA-256 |
| `ADDENDUM_crosscheck_codex.md` | Codex の要約に書かれた数値との照合 |

- 原本の場所：`cotaxxxx/basepoint-geometry`、branch `ccr-1e5ce365-5ksfyr`、commit `f3170e6`、`diagnostics/triaxial_map_20261120/`。
- 追補と監査（`../CLAUDE_AUDIT_CODEX_TRIAXIAL_RECTANGLE/`）は ZIP より後に作ったので、ZIP には入っていない。追補が参照する `code/crosscheck_codex.py` と `out/crosscheck_codex.json` は原本の場所にある。
- 報告書を書いた時点では、この repository を読めていなかった。報告書の「前提の branch が存在しない」という記述は、`basepoint-geometry` の remote についてのものである。`evidence/c-gap2-freeze-20261115` はこの repository にある。
