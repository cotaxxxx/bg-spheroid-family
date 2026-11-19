# D-PRO L1　原本と再現方法

2026-11-19 ｜ **DIAGNOSTIC_ONLY / NOT_EVIDENCE**

数学報告は CODEX_D_PRO_L1_CHORD_BRIDGE_20261119.md。§2–4 が証明の導出、§5 が有限被覆、§6 が別実装の抜取照合と費用である。ドメインは全有限の $\lambda\ge5$、全ての基点。中心と接触での延長は報告 §1–2 の定義に従う。新しい数学的結論は独立監査・Judge 裁定待ちである。

## 証拠ファイルをたどる順序

| ファイル | 記録 |
|---|---|
| DERIVATION_CHORD_BEFORE_RUN.md、FINITE_DERIVATION_BEFORE_RUN.md | それぞれ試作 1、2 より前に固定した数学導出 |
| PLAN_1.md ～ PLAN_5.md、PRE1.sha256 ～ PRE5.sha256 | 各試作の実行前固定。追加計画 3 と 5 の入力と選択理由を含む |
| chord_tail.py、probe1.stdout.jsonl | 無限側と極側に使う有理上端。5、8 のほかの断面もすべて収録 |
| make_tables.py、geometry.tbl、chord_box.cpp | 係数と方位モーメントの有向表・生成器・整数セル実装 |
| finite_pilot.py、probe2.stdout.jsonl | 12 固定点、各点から作った計 12 外箱。$\lambda=5$ は 9 点、6 と 7 は計 3 点 |
| run_cover.py、cover_5.tsv.gz、cover_6.tsv.gz、cover_7.tsv.gz | 分割した親、負の有理上端・空を区別した終端の全行。各台帳の先頭に分類と列定義 |
| verify_cover.py、cover3.stdout.jsonl、cover3.verify.jsonl、cover3.replay.jsonl | 実行時間、全箱の分割と符号の分数検査、別コンパイルでの再演算 |
| spot_arb.py、spot4.stdout.jsonl、spot_followup.py、spot5.stdout.jsonl | 最弱三箱の別式の区間包囲。初回の非負上端 4 件と再分割の全出力 |
| original_crosscheck.py、original4.stdout.jsonl | 元の $E$ の差分と弦表示の照合。通常浮動小数の診断 |
| check_claims.py、EXACT_RESULTS.json | 引用値と厳密な比較、最弱箱・再分割箱の突き合わせ |
| 同名の .stderr 各ファイル | 各実行の標準エラー原文。本実行ではすべて 0 バイト |
| SOURCE_PINS.json、SHA256SUMS | 参照した GitHub 原本の内容識別子と、本納品物のハッシュ |

## 再現

Linux、C++20、Python 3.12、python-flint 0.8.0、NumPy 2.3.5。実行元は g++ 14.2.0。ZIP 内 SHA256SUMS は自分自身を除く全メンバーを列挙する。外側の .zip.sha256 と合わせて照合できる。台帳の整数上端は実時間に依存しない。

展開したディレクトリで実行する。次の一行は新しい一時ディレクトリを作り、表・全三板の台帳を原本とバイト照合し、診断を含む全段階を再演算する。

    bash reproduce.sh

別々の Python 環境を使う場合は FLINT_PYTHON と NUMPY_PYTHON に各実行ファイルの絶対パスを設定できる。出力ディレクトリを指定するときは、未作成のパスを引数に渡す。主被覆は 3 プロセス、抜取再検査は最大 4 プロセス。原本上での再計算を必要としない。

独立監査で最初に確認する式は、報告 (3) の面積変換、(4) の代数、(5) の三係数、極端係数の固定 $m$ での単調性、(6) の符号とモーメントである。核の再演算と幾何学的被覆検査は分けて行える。
