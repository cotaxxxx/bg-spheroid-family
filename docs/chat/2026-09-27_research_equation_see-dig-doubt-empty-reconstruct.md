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

を **decision-level no-change** と呼ぶ。1ステップで判断が変わらないことは通常あり得るため、それだけでは停滞とはしない。固定した観測窓 \(k\ge2\) に対して \(\pi(X_{n+j})=\pi(X_n)\ (j=1,\ldots,k)\) が続く状態を、その窓に関する **decision-level stagnation** と呼ぶ。\(k\) は観測コストと更新頻度に応じて事前に定める。特に、

\[
X_{n+1}\neq X_n,
\qquad
\pi(X_{n+1})=\pi(X_n)
\]

は「情報は増えたが、決定関連の状態は動いていない」ことを表す。

逆に、問い \(Q\) の文面が同じでも、証拠・仮説・定義または licensed judgment が変われば停滞ではない。

## Guarded Empty

Empty は Doubt の直後に自動的に削除する操作ではない。「根拠を失った」という判定自体が証拠を必要とする。これを欠けば、まだ生きている主張を過剰に削除する危険がある。

現在の研究状態にある主張を \(C\)、その役割を \(\sigma\)、証拠 guard を \(G(E,C,\sigma)\) とする。概念的には、

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

これにより REDDS と証拠規律を接続する。証拠区分は一列の序列に潰さず、方針書 §6 と同じく別軸として扱う：

1. **事実の軸** — Established。
2. **仕組みについての主張の軸** — Diagnostic hypothesis → Strong diagnostic evidence → Proof only with lemma。
3. **設計判断の軸** — Design inference。

したがって Empty の guard は、強弱だけでなく、主張がどの軸のどの役割を担っているかを確認する。

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

高水準の問いはおおむね同じだった： **Can \(H>0\) be closed mechanically?** 問い \(Q\) が同じでも、研究状態 \(X=(Q,E,H,D)\) は大きく動いた。

計算上の出来事は二種類に分ける。実行そのものが3回失われた件は、セッションのパイプ、PC の再起動、プロセスの消滅によるもので、アルゴリズムの失敗ではない。一方、resumable 版 smoke が §7 の gate に不合格となった件は、アルゴリズム／certification design 側の結果である。

ledger には約15,400 node の判定記録があり、split と accepted も含む。unresolved は約7,200件（4,078 + 3,140）である。点の極限診断では、深さ12で unresolved だった点のうち **62/186** が accept に移った。また帯 B は、near column の作り方、すなわち除外球の中心を軸上に置く構成から構造的に生じていた。これらは機械側の構成を直す選択肢も開く。

### Empty が正しく働いた例

- 「細分の力技は死んだ」という主張は、強い結論として保持せず **Design inference** へ格下げした。
- 「\(B_{\rm cut}=0\) なので (ii) は除外される」という一般化は、監査側がいったん受け入れた。その後、同日の再監査で (ii) に当たる点が44点あることが確認され、撤回された。

### Empty が過剰に働いた例：canonical push

canonical push を「済み」とする主張は、監査側が別の repository `basepoint-geometry` を照合したため「origin にない」と判定され、一度 UNRESOLVED に差し戻された。その後、正しい repository `bg-oblate-spheroid` で照合し直すと commit は push 済みで、ファイル SHA もすべて一致し、RESOLVED に復帰した。

これは、**guard の根拠・照合対象・provenance 自体も監査対象でなければならない**ことを示す、過剰な Empty の実例である。

### \(U_{\rm check}\) に関する記録境界

以前の版では global cover を「撤回した」例として記載したが、現在確認できた一次記録からはその経過を裏付けられないため、Empty の実例から外す。確認できる範囲では、C-side は「各 component は条件付きで閉じているが global cover は未確認」とされ、\(U_{\rm check}\) は receipt-based verification が必要な領域として扱われていた。撤回の時点と対象主張が一次記録で確定するまで、それ以上の研究史を補わない。

### Rebuild の現在位置

Rebuild の方向を一つに固定しない。現在は、**解析への委譲や、near column の作り方の見直しを含む再設計を検討する方向**にある。これは同じ問いに対する licensed judgment、すなわち \(\pi(X)\) が動いた具体例でもある。ただし、この方法論ノート自体は数学的結論を証明しない。

\[
\boxed{
X_{n+1}\in\mathrm{REDDS}(X_n;I_{n+1})
}
\]

🐟 REDDS の目的は \(X\) 内部の変化量を最大化することではない。**新しい問いと、証拠に裏付けられた新しい判断が生まれる条件を維持すること**である。

## Placement and evidence boundary

このファイルを SDDER / REDDS formulation の methodology/history 正典とする。

D-OB episode を将来の論文または工程記録へ利用する場合、必要な project-specific 部分だけを移し、D-OB の正式 artifact によって再度 grounding すること。

> **正確な研究史記録であることを理由に、この方法論ノートを machine evidence へ昇格させてはならない。**
