# 論文 I v0.5.6 日本語参考訳

2026-11-23 ／ 翻訳：Claude Code（Anthropic）／ 著者による校閲は未了

英語版 `manuscripts/2026-11-23/Paper_I_v0_5_6/Paper_I_v0_5_6_Integrated_EN.pdf`（SHA-256 `136d61aa49f9…3fb35`）の日本語訳である。**正本は英語版**であり、食い違いがあれば英語版に従う。数学的な主張、計算主張 C1--C6 の位置づけ、証拠の等級は、この訳で何も変えていない。

## 中身

| ファイル | 内容 |
|---|---|
| `Paper_I_v0_5_6_Integrated_JA.pdf` | 日本語版の PDF（39 ページ。英語版と同じページ数） |
| `source/` | 日本語の LaTeX ソース（`main.tex`、`sections/`、文献、図） |
| `TRANSLATION_RULES.md` | 訳の規則と訳語の表 |
| `check_invariants.py`、`invariants.txt` | 英語版と訳の照合（下記） |

## 作り方

- 元にしたのは、`Paper_I_v0_5_6_Manuscript_and_Verification.zip`（SHA-256 `b4b720f011bc…7034b`）の中の LaTeX ソースである。
- 本文 6 ファイルを、同じ規則と訳語の表のもとで訳し、担当ごとに割れた訳語（計算主張、個数調査、橋、参照座標、Jacobian）をそろえた。`main.tex`（題、要旨、主結果と現状）は別に訳した。
- 組版は LuaLaTeX（luatexja、原ノ味フォント）。`source/` で `lualatex main && bibtex main && lualatex main && lualatex main`。
- 英語版から変えたのは、前文（日本語の組版、定理類の見出しの日本語化）と、表紙の注記（参考訳であること）だけである。文献リストは英語のままである。

## 照合したこと

`check_invariants.py` で、6 つの本文ファイルについて、次のものが英語版と一字も違わないことを確かめた（`invariants.txt`）。

- 別行の数式 151 本（順序も一致）
- 文中の数式 958 個
- `\label` 124、`\ref`・`\eqref` 115、文献の引用 29
- リンクの URL、`\path`、`\texttt`、図のファイル名、環境の `\begin`・`\end`

数式の中の英語（`\text{...}` の「if」「on」など）は、訳さずにそのままにしてある。

## 確かめていないこと

- 訳文の全文を、英語版と 1 文ずつ突き合わせる校閲はしていない。照合したのは数式と参照であり、文の意味の正しさは抜き取りで読んだだけである。
- 訳語は、著者のこれまでの日本語の文書に合わせたつもりだが、著者の確認を受けていない。変えたい語があれば、`TRANSLATION_RULES.md` の表を直して一括で置き換えられる。
- 計算補遺（v0.4 の Computational Supplement）は訳していない。
