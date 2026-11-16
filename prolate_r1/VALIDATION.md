# DIAGNOSTIC_ONLY / NOT_EVIDENCE — R2実行状況

## 固定した旧版の実行証拠
commit `1917e1ab3c22191852385cf8cd3df5f6d9958fb8` の
`runs/2026-11-17/D_PRO_R1_COROTATION_DIG_RUN1/RUN_RECEIPT.md` とログを参照した。
R1 ZIPの整合、24件のソースハッシュ、Python compileall、
quick 2/2、pilot成功はDigが報告している。
fullは23件中6件のPASS表示で外部タイムアウト。全件結果ではない。
axis_g(1/2,3)とy=[3/4,7/8]セルの非有限値も同じ証拠にある。

## 新版 R2
CodexのPython実行環境への呼び出しは
`No usable execution environment is available` で失敗した。
このため、R2のPython構文検査・import・Arb実行・11回帰検査・quick・full・pilotは未実行。
未実行を成功扱いにしていない。

GitHubの固定R1ソースへ限定した変更を適用し、
テスト関数の本文と固定ケース列挙条件の不変を文字列で照合する。
ハッシュ計算、ZIPのCRCと内容照合、登録treeの比較は、
Python/Arbとは別のJavaScript実行環境で行う。
それらは数値積分核の動作検査ではない。

新たに追加した回帰検査：
- 正値逆数の多重係数恒等式、広い正値区間の逆数三乗の係数。
- 正の保証がない入力や不整合な値域の拒否。
- 問題セルの2/4/6次jetと外側パラメータ微分の有限性。
- 報告されたデフォルトaxis_gの呼び出し。
- ケースごとの保存・再開、失敗とtracebackの保持。
- 完了記録がない試行の回収、SIGTERMスタック、識別情報相違の拒否。
- 明示的resumeなしの既存出力への書込み拒否。

数学的な区間包囲の独立監査は未了。全域の符号判定は実施しない。
