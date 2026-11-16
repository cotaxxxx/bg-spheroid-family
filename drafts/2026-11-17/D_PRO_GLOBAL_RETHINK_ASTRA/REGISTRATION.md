# D-PRO 再検討報告：GitHub登録記録

登録日：2026年11月17日（日本時間）

ユーザーの「githubに登録して下さい」という指示により、提出済みの研究報告書と検算一式を追加登録する。研究案の採用裁定、証明書、認証本走の承認ではない。

- Repository: `cotaxxxx/bg-spheroid-family`
- Branch: `research/d-pro-global-rethink-20261117`
- Base commit: `c86c10d4db81614256909ef0cdf1c98fa7240686`
- Path: `drafts/2026-11-17/D_PRO_GLOBAL_RETHINK_ASTRA/`
- Status: `RESEARCH_DESIGN / DIAGNOSTIC_ONLY / NOT_EVIDENCE`

## 原本の照合

- `D_PRO_GLOBAL_RETHINK_ASTRA_20261116.zip`
  - SHA-256: `60a526ecba2ddaccd7b1541a5f4773b7b2c3acd2b50c73c15a5586cd8e7b7c43`
- `D_PRO_GLOBAL_RETHINK_ASTRA_20261116.md`
  - SHA-256: `d9df1a27be0735d60cae158b488ac4901dc18a1d3ea772d04c42781c01d0479f`

ZIP内の14ファイルを、そのまま閲覧用にも展開して登録する。`SHA256SUMS` の全13項目、診断前の二つの封印、ZIPと展開ファイルの一致を照合済み。原本ファイルは変更していない。ZIPのハッシュは `ARCHIVE_SHA256SUMS` でも照合できる。

今回の登録で追加するファイルは、本記録と `ARCHIVE_SHA256SUMS` の二つのみ。これらは原本ZIPの外側の登録用記録である。

同梱報告書とREADMEにある「GitHubは変更していない」は、研究原本の作成時点における実施範囲を述べたもの。今回の追加登録とは区別する。

## 研究上の状態

共回転の角度微分核、球冠誤差評価、条件付き構造定理を提案している。全域の W>0、軸上 E_z>0、赤道上 Φ_s<0 は未証明。診断出力には初回の勾配照合不一致と、固定した追加検査の結果を両方保存している。

main、STATE、既存FREEZE、既存証明書、凍結済みJulia第二系統を変更しない。追加の数値計算、Actionsの起動、PR作成・マージは本登録に含まれない。
