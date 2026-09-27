# 研究方程式 — 見→掘→疑→空→再

Date: 2026-09-27

> AI共同研究の軌跡として保存する研究方法論メモ。
> RAW evidence・D-OB producer/checker evidence・正式な数学的証明とは分離する。

## Research equation

\[
\boxed{
\mathrm{見}\rightarrow\mathrm{掘}\rightarrow\mathrm{疑}\rightarrow\mathrm{空}\rightarrow\mathrm{再}\circlearrowleft
}
\]

これは直線的な工程ではなく、「再」から新しい「見」へ戻る反復過程である。

## 五つの作用

### 見 — See

現象を見る。理論を先に固定するのではなく、数値、図形、計算結果、失敗、例外など、実際に現れたものを観察する。

### 掘 — Dig

答えではなく、問いを掘る。

\[
Q_0\rightarrow A_0\rightarrow Q_1\rightarrow A_1\rightarrow Q_2\rightarrow\cdots
\]

得られた答えを終点にせず、「なぜそうなるのか」「そもそも何を問うべきなのか」を掘り、次の問いを生成する。

### 疑 — Doubt

得られた構造を疑う。人間の解釈もAIの推論も誤り得る。反例探索、別AIによる批判、独立実装、producer/checker、監査などによって、掘った方向そのものを疑う。

掘る力が強いほど、誤った前提まで深く掘る可能性がある。そのため「掘」と「疑」は対になる。

### 空 — Empty

前提をいったん空にする。反証された仮説を継ぎはぎして守るのではなく、必要なら問い、定義、解釈、モデルそのものを一度解除する。

「空」は失敗ではなく、誤った問題設定への固着を防ぐ操作である。

### 再 — Rebuild

問いを再定義し、研究を再構成する。新しい定義、新しい座標、新しい不変量、新しい検証方法を採用し、再び現象を見る。

したがって「再」は終点ではなく、次の「見」への入口である。

## Research principle

> **AI時代の研究は、答えを掘るんじゃなく、問いを掘る。**

これは研究の理念を表す。一方、

> **見 → 掘 → 疑 → 空 → 再**

は、その理念を実際の研究循環として表した「研究方程式」である。

## SDDER Research Cycle / 🐟 REDDS Operator

時間順の研究循環を

\[
\boxed{
\mathrm{S}ee
\rightarrow
\mathrm{D}ig
\rightarrow
\mathrm{D}oubt
\rightarrow
\mathrm{E}mpty
\rightarrow
\mathrm{R}ebuild
}
\]

とし、**SDDER Research Cycle** と呼ぶ。

作用素の合成では右から左へ作用するため、

\[
\boxed{
\mathcal R
=
R\circ E\circ D_{\rm doubt}\circ D_{\rm dig}\circ S
}
\]

となる。この逆読みから作用素名を **REDDS Operator** とする。

*redd* / *redds* が魚の産卵床を意味することは偶然の一致だが、本方法論では **新しい問いが生まれる場所 (a spawning ground for new questions)** という第二義を与える。🐟 は非公式なシンボルとして用いる。

## Research state

問い \(Q\) だけでは研究状態を表すには粗すぎる。同じ問いのままでも、証拠・仮説・定義は大きく変化し得る。

\[
\boxed{
X_n=(Q_n,E_n,H_n,D_n)
}
\]

ここで \(Q\) は Question、\(E\) は Evidence、\(H\) は Hypotheses、\(D\) は operative Definitions を表す。

### External input and non-determinism

研究は現在の状態だけで閉じていない。計算、実験、監査、反例、証明、失敗など、外部から新しい入力を受け取る。これを \(I_{n+1}\) とする。

したがって REDDS のより正確な形は、

\[
\boxed{
X_{n+1}\in\mathcal R(X_n;I_{n+1}),
\qquad
\mathcal R=\mathrm{REDDS}.
}
\]

である。集合値表記は、同一の研究状態と入力から複数の正当な再構築があり得ることを許す。状態がどこへ移るかは REDDS の性質だけではなく、数学的・計算的世界から返される応答にも依存する。

## Decision projection and stagnation

文字どおりの \(X_{n+1}=X_n\) を停滞の定義にすると厳しすぎる。サンプルが1点増えるだけでも \(E_n\) は変わるが、研究上の判断は何も変わらない場合がある。

そこで決定関連の射影

\[
\pi:X\longrightarrow\mathcal J
\]

を導入する。\(\mathcal J\) は、その研究状態から現在許される判断・主張・決定を表す。

\[
\boxed{
\pi(X_{n+1})=\pi(X_n)
}
\]

を **decision-level stagnation** と呼ぶ。特に、

\[
X_{n+1}\neq X_n,
\qquad
\pi(X_{n+1})=\pi(X_n)
\]

は「情報は増えたが、決定関連の状態は動いていない」ことを表す。

逆に、問い \(Q\) の文面が同じでも、証拠・仮説・定義または licensed judgment が変われば停滞ではない。

## Guarded Empty

Empty は Doubt の直後に自動的に削除する操作ではない。「根拠を失った」という判定自体が証拠を必要とする。これを欠けば、まだ生きている主張を過剰に削除する危険がある。

現在の研究状態にある主張を \(C\)、その役割を \(\rho\)、証拠 guard を \(G(E,C,\rho)\) とする。概念的には、

\[
\boxed{
\mathrm{Empty}_G(C)=
\begin{cases}
C,
& G\text{ が現在の役割を支持する},\\
\operatorname{downgrade}(C),
& G\text{ がより弱い役割のみを支持する},\\
\varnothing,
& G\text{ が再構築後の役割を支持しない}.
\end{cases}
}
\]

したがって Empty を次のように定義する。

> **Empty = 主張の記録された証拠強度が、その主張に割り当てられた役割を支えなくなったときに、除去または降格する操作。**

これにより REDDS と証拠規律を接続する。作業上の証拠強度は区別して扱う：

- **Established**
- **Diagnostic hypothesis**
- **Strong diagnostic evidence**
- **Proof only with lemma**

これらは交換可能ではない。主張は Empty によって消去されず、より弱い証拠上の役割へ降格して生き残る場合もある。

**Empty があるから Rebuild は単なる修繕ではなく再構築になる。**

## Human–AI functional roles

本研究での機能的な役割分担を簡潔に書けば、

\[
\boxed{
\text{Human: conception}
\quad\times\quad
\text{ChatGPT: excavation}
\quad\times\quad
\text{Claude / Code: audit}
}
\]

である。

これは各システムが本質的に正しいという主張ではなく、workflow 上の役割分離である。深く掘る能力は、誤った方向を深く掘る能力でもある。そのため excavation と audit を意図的に分離する。

## Worked example: D-OB, September 2026

以下は方法論上の研究史記録であり、**D-OB machine evidence、producer/checker evidence、proof artifact ではない**。

高水準の問いはおおむね同じままだった：

> **Can \(H>0\) be closed mechanically?**

問い \(Q\) だけを見れば停滞しているように見える。しかし研究状態 \(X=(Q,E,H,D)\) は大きく動いた。証拠状態は smoke の連続失敗、resumable execution、約15,000 node に達する failure map へと推移した。

ここで重要なのは、同じ問いに対する licensed judgment 自体も「純機械的に閉じる設計」から「純機械だけでは閉じない方向を疑い、解析への委譲を含む設計を検討する」方向へ更新されたことである。これは \(\pi(X)\) の変化の具体例である。ただし、この方法論ノート自体はその数学的結論を証明しない。

この期間には少なくとも次の Empty 操作があった：

1. \(U_{\rm check}\) の global cover という主張を撤回した。
2. 「細分の力技は死んだ」という主張を、より強い結論として保持せず **design inference** へ格下げした。
3. canonical push が「済み」であるという主張を、確認不足のため未確定へ差し戻した。

いずれも「疑ったから消す」のではない。証拠が従来の役割を支えなくなったため、guard に従って撤回または降格した例である。

その後の Rebuild は「cap を深くして再試行する」という修繕だけではなく、**machine core + analytic delegation** を含む certification architecture の再構築へ向かう。

\[
\boxed{
\mathrm{Doubt}
\rightarrow
\mathrm{Empty\ unsupported\ roles}
\rightarrow
\mathrm{Rebuild\ the\ certification\ architecture}
}
\]

したがって、この episode は refined REDDS equation

\[
\boxed{
X_{n+1}\in\mathrm{REDDS}(X_n;I_{n+1}),
\qquad
\text{progress is judged through changes in }\pi(X)
}
\]

の operational example である。

🐟 REDDS の目的は \(X\) 内部の変化量を最大化することではない。**新しい問いと、証拠に裏付けられた新しい判断が生まれる条件を維持すること**である。

## Placement and evidence boundary

このファイルを SDDER / REDDS formulation の methodology/history 正典とする。

D-OB episode を将来の論文または工程記録へ利用する場合、必要な project-specific 部分だけを移し、D-OB の正式 artifact によって再度 grounding すること。

> **正確な研究史記録であることを理由に、この方法論ノートを machine evidence へ昇格させてはならない。**
