# Paper I v0.5.7 日本語版の整合性検査
英語正本: bg-spheroid-family commit 2009fda4c1393349408f354dd4a6fc518ab16806。
この検査は日本語訳全文の意味的な完全性を保証するものではない。

| 比較対象 | 一致した数式環境 | ラベル | 参照 | 引用 |
|---|---:|---:|---:|---:|
| sections/core.tex | 31 | 49 | 39 | 4 |
| sections/related_work.tex | 0 | 1 | 2 | 25 |
| sections/prolate_tail.tex | 40 | 59 | 59 | 0 |
| sections/radial_experiment.tex | 0 | 2 | 2 | 0 |
| sections/computational_evidence.tex | 2 | 10 | 13 | 9 |
| sections/numerical_discussion.tex | 0 | 5 | 7 | 3 |

各節で対応する数式環境はTeXの空白以外一致し、ラベル・式参照・引用キーの多重集合も一致。
参考文献BibTeXとLICENSEは英語原本とバイト一致。
PDF42ページ、LaTeX致命的エラー・未解決参照・Overfull hbox無し。
条件付きの要旨、3.1節の符号表、8節の規模表と証拠参照、V24の監査表現を反映。
数学の独立監査または英語論文の新しい公開承認ではない。
