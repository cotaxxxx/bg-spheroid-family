# 論文 I v0.5.6 日本語訳：規則と訳語

## 目的
英語の LaTeX ソースを、日本語の LaTeX ソースに訳す。著者（日本語話者の数学研究者）が自分の論文を日本語で読み直すための参考訳である。英語版が正本。

## 絶対に守ること
1. **数式は 1 文字も変えない。** `$...$`、`\[...\]`、`equation`/`align`/`aligned`/`gather`/`cases` などの数式環境の中身、`\label`、`\ref`、`\eqref`、`\cite`/`\citep`/`\citet`、`\href` の URL、`\path{...}`、`\url{...}`、`\texttt{...}` の中身、ファイル名、コード名、commit、数値はそのまま写す。数式の中の `\text{...}`・`\mathrm{...}` の英語（例：`\text{if }`、`\mathrm{axis}`）もそのままにする。
2. **内容を足さない、削らない、言い換えで意味を変えない。** 文の数と順序を保つ。訳注は付けない。
3. **LaTeX の構造を保つ。** 環境（theorem、proof、table、figure、itemize、enumerate…）、コマンド、表の列、コメント行（`%`）はそのまま。`\begin{proof}[...]` の `[...]` の中、`\caption{...}`、`\section{...}`、表の見出しや本文のセルの英語は訳す。行の並びもできるだけ元と同じにする（1 行ずつ対応させる）。
4. 文体は「である」体の論文調。簡潔に。カタカナ語を増やしすぎない。
5. 人名、論文名、ソフト名、記録の ID（V24、C1〜C6 など）は原語のまま。
6. 引用符 ``...'' は「…」にする。英語のダッシュ `---` は「——」か読点・かっこに直す。数の範囲 `--` は数式外では「〜」でよいが、`C1--C6` のようなラベルの範囲は「C1--C6」のまま。
7. 和文と数式・欧文の間に空白は入れない（LuaLaTeX-ja が調整する）。ただし LaTeX コマンドの直後に和文が続いて区切りが要るときは `{}` を使う。
8. 出力は UTF-8。ファイル全体を訳し、途中で省略しない。

## 訳語（必ずこれを使う）
| English | 日本語 |
|---|---|
| spheroid | 回転楕円体 |
| volume-preserving spheroids / family | 体積保存回転楕円体（族） |
| oblate / prolate | 扁平 / 扁長 |
| flat end | 扁平の極限 |
| prolate tail | 扁長側の裾 |
| near-sphere band | 球に近い帯 |
| window (parameter window) | 窓 |
| stationary point / set / component | 停留点 / 停留集合 / 停留成分 |
| critical point / critical manifold | 臨界点 / 臨界多様体 |
| saddle / saddle circle / index-one saddle | 鞍点 / 鞍点円 / 指数 1 の鞍点 |
| Morse--Bott | Morse--Bott（そのまま） |
| nondegenerate | 非退化 |
| centre | 中心 |
| basepoint / moving basepoint | 基点 / 動く基点 |
| energy | エネルギー |
| cone volume measure | 錐体積測度 |
| cone-volume-weighted | 錐体積で重み付けた |
| radial--normal angle | 動径–法線角 |
| squared radial--normal angle | 動径–法線角の二乗 |
| radial Gauss map | 動径 Gauss 写像 |
| support function | 支持関数 |
| axis / axial pair / equator / equatorial circle / pole | 軸 / 軸上の対 / 赤道 / 赤道円 / 極 |
| meridian section | 子午線断面 |
| boundary trace / full-gradient boundary trace | 境界トレース / 全勾配の境界トレース |
| threshold | 閾値 |
| classification / conditional classification | 分類 / 条件付き分類 |
| computational assertion | 計算主張 |
| validated numerics | 精度保証付き数値計算 |
| interval arithmetic / interval enclosure | 区間演算 / 区間包囲 |
| enclosure | 包囲 |
| outward rounding | 外向き丸め |
| box / leaf / ledger | 箱 / 葉 / 台帳 |
| coverage | 被覆 |
| sign margin | 符号の余裕 |
| audit / audit scope | 監査 / 監査の範囲 |
| replay | 再実行 |
| independent recomputation | 独立な再計算 |
| reproducibility / availability | 再現性 / 入手先 |
| certification | 認証 |
| proof-development manuscript | 証明の整備段階の原稿 |
| transverse Hessian | 横断方向の Hessian |
| chord identity | 弦の恒等式 |
| polar cap | 極冠 |
| signed angle | 符号付き角 |
| kernel (integral kernel) | 核 |
| crossing | 交差 |
| symmetry factor | 対称性の因子 |
| monotonicity / monotone | 単調性 / 単調 |
| concavity / concave | 凹性 / 凹 |
| bifurcation / branch | 分岐 / 枝 |
| triaxial | 三軸 |
| remainder / tail bound | 剰余 / 尾の上界 |
| lemma / proposition / theorem / corollary / claim / remark / definition / conjecture | 補題 / 命題 / 定理 / 系 / 主張 / 注意 / 定義 / 予想（環境名は変えない。本文中の参照「Theorem~\ref{...}」は「定理~\ref{...}」とする） |
| Section~\ref / Table~\ref / Figure~\ref / equation \eqref | 第~\ref{...}節 / 表~\ref{...} / 図~\ref{...} / 式~\eqref{...} |
| Proof. / Proof of ... | 証明（`\begin{proof}[Proof of X]` は `[X の証明]`） |
