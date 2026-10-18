# Astra / Code 独立監査依頼 — D4 中心下界の全 λ 域への拡張

**2026-10-18 JST**  
**発行：Judge（依頼文）**  
**担当：Astra または Code（独立監査側）**  
**対象：chat が導出した中心下界。未監査・未採用の主張。**  
**方法：paper-only / exact algebra、必要なら Python Fraction による有理数の確認のみ。**

## 目的・主張

以下を独立に再導出し、PASS / FAIL と指摘一覧を提出すること。出発点は family main にある `D4_CENTER_BAND_SOURCE_AUDIT_V0` §4 の中心公式とする。

\[
\boxed{H(0,0;\lambda)\ge 2\lambda\left(\lambda^2-\frac4{27}(1-\lambda^2)^2\right)\ge\frac{416}{9375}>0},
\qquad \lambda\in\left[\frac25,\frac{33}{50}\right].
\]

## 固定する原典の中心公式

\[
H(0,0;\lambda)=\int_{-1}^1\left[
\frac{\gamma R\,N}{q^2}-
\frac{R'\gamma^2(1-y)(1-q)^2}{2q^2}
\right]d\mu.
\]

記号は原典に従い、

\[
\begin{aligned}
y&=\mu^2, & c&=1-\lambda^2, & q&=1-cy,\\
w^2&=\lambda^2(1-y)+y, &
\gamma&=\frac{\lambda}{w\sqrt q},\\
N&=\frac12+\left(\frac12-c\right)y-c^2y^2(1-y).
\end{aligned}
\]

## 提示されている導出（正しいとは仮定しないこと）

\(\lambda\le33/50<1/\sqrt2\) なので \(c>1/2\)。\(0\le y\le1\) なら

\[
\left(\tfrac12-c\right)y\ge\tfrac12-c,
\qquad y^2(1-y)\le\tfrac4{27}.
\]

したがって

\[
N\ge1-c-\frac{4c^2}{27}
=\lambda^2-\frac4{27}(1-\lambda^2)^2.
\]

\(w\le1\), \(q\le1\), \(R\ge1\) から \(\gamma R/q^2\ge\lambda\)。さらに P1 Lemma 3.2 の \(R'\le0\) と中心公式の負号により第2項は非負。両項を \(\mu\in[-1,1]\) で積分し

\[
H(0,0;\lambda)\ge2\lambda\left[\lambda^2-\frac4{27}(1-\lambda^2)^2\right].
\]

右辺が指定区間で単調増加することを確認し、左端 \(\lambda=2/5\) では

\[
\lambda^2-\frac4{27}(1-\lambda^2)^2
=\frac{104}{1875},\qquad
2\lambda\times\frac{104}{1875}=\frac{416}{9375}.
\]

## 必須監査項目

1. **\(N\) の下界と適用域**：\(y\in[0,1]\) および \(\lambda\in[2/5,33/50]\) 全体で不等式が成り立つか。\(c>1/2\) の条件が端点も含め維持されるか。
2. **符号**：原典の \(R'\le0\) と中心公式の負号から第2項が非負となるか。\(R\)・\(R'\) の定義も原典と一致させる。
3. **係数・端点**：\(\gamma R/q^2\ge\lambda\) を \(\mu=\pm1\)、\(y=0\) を含む全域で検証する。\(q,w\) の正値性、定義域、分母の安全性も確認する。
4. **積分・算術**：\(2\lambda\)、\(\lambda\) に対する単調性、\(104/1875\)、\(416/9375\) を exact algebra および必要なら `fractions.Fraction` で検証する。
5. **継承条件**：中心公式自体が P1 §1 の定義、P1 Lemma V（中心での微分と積分の交換・連続延長）にどう依存するか特定する。依存する未 discharge 条件を無条件に承認しない。

## 成果物の形式

- 総合判定 **PASS / FAIL** を冒頭に記載。ただし継承条件が残る場合は **PASS conditional on [具体的条件]** と明記する。
- 各監査項目について、原典箇所・再導出・適用域・判定を簡潔に記録する。
- GAP・条件漏れ・誤った係数または符号があれば番号付き指摘一覧と修正提案を記載する。
- 監査者自身が別系統として行った検算か、他者の結果の readback かを明確に区別する。
- 監査結果を Judge に返す。**A/B 方式の選択、V4 PREDECLARE、FREEZE、実行許可は今回の権限に含まない。**

## 禁止事項・状態

数値 sampling / パラメータ掃引 / 区間計算 / D5 の実行・resume / 旧 run-directory の変更 / 勝手な commit・push を行わない。

**D5 V3:** ABORTED / NOT_EVIDENCE（2026-10-18）。V4 は DESIGN PENDING。研究用 PC での本計算は、V4 事前宣言の正式な FREEZE 後まで不可。

中心下界が独立監査に合格した後、Judge は **A（\(\lambda\) 区間別に下界を改善）** と **B（解析領域の半径上限を縮小）** の設計比較に進む。
