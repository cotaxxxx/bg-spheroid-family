# D-PRO 独立再検討・受け渡し一式

報告書は `D_PRO_GLOBAL_RETHINK_ASTRA_20261116.md`。研究・証明設計であり、大域証明の成立判定や本走の承認ではありません。

`diagnostics/` はすべて **DIAGNOSTIC_ONLY / NOT_EVIDENCE**。初回Q5の false と、その後の固定再検査の true を両方保存しています。出力は二値だけで、数値的な余裕や最悪点を含みません。

`checks/` は厳密な記号・有理演算の恒等式検算です。全域の符号を証明する証明書ではありません。

## 照合

このディレクトリで `sha256sum -c SHA256SUMS` を実行してください。実行前計画とコードの封印は、診断スクリプト自身も確認します。

## 任意の再現

`ENVIRONMENT.json` に今回のローカル診断環境を記録しています。NumPy と SymPy を用います。

```bash
python diagnostics/research_diagnostic.py
python diagnostics/identity_recheck.py
python checks/algebra_checks.py
```

出力先は同梱のJSONです。受領原本のハッシュを先に照合し、再現はコピーした作業ディレクトリで行ってください。外部PC上の既存プロセスや証明環境へ導入する手順ではありません。

正本・FREEZE・凍結済みJulia第二系統・GitHubは変更していません。新しい符号条件と小規模区間評価を独立に監査するための資料です。
