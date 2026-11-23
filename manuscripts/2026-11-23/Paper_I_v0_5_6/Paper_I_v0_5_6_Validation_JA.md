# Paper I v0.5.6｜製作側チェック記録（Dig、通常監査ではない）

| 項目 | 結果 |
|---|---|
| 親版v0.5.4原本ZIPの外部SHA-256 | `e58dd99e455d82993f791d18a4a68b317dc26f408a1348e90ed75558811eb0e8` 一致 |
| 親版v0.5.4原本PDFの外部SHA-256 | `6fa3a41e1ea1f5e79a65e4f5b1f805d67827bbd583c7c6b9ef023b0e5de722bb` 一致 |
| tex差分 | `main.tex`、`sections/core.tex`、`sections/related_work.tex`、`sections/numerical_discussion.tex` |
| bib差分 | `references_additions.bib` の追記のみ |
| 他の既存ファイル | バイト一致（含: 定理の計算データと証拠原本） |
| LICENSE | 新規追加、文書CC BY 4.0／コードMIT |
| patch独立適用試験 | PASS（原本に適用後の全対象ファイルが成果物と一致） |
| TeXビルド | pdflatex + BibTeX + pdflatex 3回、39ページ |
| 未解決引用・LaTeXエラー | 0 |
| AI provenance / author verification | pendingを保持。Judge決裁なし |
| 数学的監査・公開判定 | **未実施・未裁定** |

この記録は製作側の形式検査であり、Claude通常監査を代替しない。
