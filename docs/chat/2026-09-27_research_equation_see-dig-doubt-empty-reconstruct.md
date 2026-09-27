# 研究方程式 — 見→掘→疑→空→再

Date: 2026-09-27

> AI共同研究の軌跡として保存する研究方法論メモ。
> RAW evidence・D-OB producer/checker evidence・正式な数学的証明とは分離する。

## Research equation

```
見 → 掘 → 疑 → 空 → 再
↑                 ↓
└─────────────────┘
```

あるいは、

[
\mathcal{R}
=
(\mathrm{見}\,\mathrm{掘}\,\mathrm{疑}\,\mathrm{空}\,\mathrm{再})^{\infty}.
]

これは直線的な工程ではなく、「再」から新しい「見」へ戻る反復過程である。

## 五つの作用

### 見 — Observe

現象を見る。

理論を先に固定するのではなく、数値、図形、計算結果、失敗、例外など、実際に現れたものを観察する。

### 掘 — Dig

答えではなく、問いを掘る。

```
Q0 → A0 → Q1 → A1 → Q2 → ...
```

得られた答えを終点にせず、「なぜそうなるのか」「そもそも何を問うべきなのか」を掘り、次の問いを生成する。

### 疑 — Doubt

得られた構造を疑う。

人間の解釈もAIの推論も誤り得る。反例探索、別AIによる批判、独立実装、producer/checker、監査などによって、掘った方向そのものを疑う。

掘る力が強いほど、誤った前提まで深く掘る可能性がある。そのため「掘」と「疑」は対になる。

### 空 — Empty

前提をいったん空にする。

反証された仮説を継ぎはぎして守るのではなく、必要なら問い、定義、解釈、モデルそのものを一度解除する。

「空」は失敗ではなく、誤った問題設定への固着を防ぐ操作である。

### 再 — Reconstruct

問いを再定義し、研究を再構成する。

新しい定義、新しい座標、新しい不変量、新しい検証方法を採用し、再び現象を見る。

したがって「再」は終点ではなく、次の「見」への入口である。

## Relation to the research principle

先に得られた研究原則：

> **AI時代の研究は、答えを掘るんじゃなく、問いを掘る。**

これは研究の理念を表す。

一方、

> **見 → 掘 → 疑 → 空 → 再**

は、その理念を実際の研究循環として表した「研究方程式」である。

## Human–AI division

AI共同研究では、全ての役割を一つのAIに求める必要はない。

```
見：人間 + 計算 + 可視化
掘：対話型AI + 人間
疑：別系統AI + 反例探索 + 独立実装
空：人間による問題設定の解除
再：人間 + AIによる再構成
```

重要なのは「間違えないAI」を仮定することではない。

```
掘る
→ 疑う
→ 間違いなら空にする
→ 再構成する
→ もう一度見る
```

という循環によって、誤りを研究過程の内部で修正できる構造を作ることである。

## Compact form

> **見。掘る。疑う。空にする。再び見る。**

[
\boxed{
\mathrm{見}
\rightarrow
\mathrm{掘}
\rightarrow
\mathrm{疑}
\rightarrow
\mathrm{空}
\rightarrow
\mathrm{再}
\circlearrowleft
}
]


## SDDER Research Cycle / 🐟 REDDS Operator

The time-order research cycle is

[
oxed{
mathrm{S}ee
ightarrow
mathrm{D}ig
ightarrow
mathrm{D}oubt
ightarrow
mathrm{E}mpty
ightarrow
mathrm{R}ebuild
}
]

and is named the **SDDER Research Cycle**.

As a composition of operators, the order is written in reverse:

[
oxed{
mathcal R
=
Rcirc Ecirc D_{m doubt}circ D_{m dig}circ S
}
]

Hence the operator name is **REDDS**:

[
oxed{
Q_{n+1}=mathrm{REDDS}(Q_n)
}
]

The name has an accidental but useful second meaning: *redds* are fish spawning beds. In this methodology, REDDS is therefore also a metaphorical **spawning ground for new questions**. The fish mark 🐟 may be used informally as the symbol of the research cycle.

## Empty as an independent operation

**Empty is not merely a pause between Doubt and Rebuild.**

Its methodological role is:

[
oxed{
mathrm{Empty}
=
	ext{remove claims or structures that have lost sufficient support before rebuilding}
}
]

When a claim is downgraded, withdrawn, or found to rest on insufficient evidence, it should not remain as a hidden foundation for the next reconstruction. Empty explicitly clears that unsupported structure.

Thus,

[
mathrm{Doubt}ightarrowmathrm{Empty}ightarrowmathrm{Rebuild}
]

differs from immediately patching a doubtful claim. **Empty makes Rebuild reconstruction rather than repair.**

A concrete pattern is:

[
	ext{claim}
ightarrow
	ext{doubt / audit}
ightarrow
	ext{downgrade or withdrawal}
ightarrow
	ext{reclassify evidence}
ightarrow
	ext{rebuild the claim}
]

Evidence labels such as **Established / Diagnostic hypothesis / Strong diagnostic evidence / Proof** belong to the rebuilt state and should not be conflated.

## REDDS as a research-state operator

Using only the question (Q_n) is sometimes too coarse. The wording of a question can remain unchanged even when its evidential state has advanced.

Define a research state

[
X_n=(Q_n,E_n,H_n,D_n),
]

where (Q) is the question, (E) the evidence state, (H) the current hypotheses, and (D) the operative definitions.

Then the stronger form of the research equation is

[
oxed{
X_{n+1}=mathrm{REDDS}(X_n).
}
]

A true stagnation point is therefore better represented by

[
oxed{
X^*=mathrm{REDDS}(X^*)
}
]

rather than merely (Q_{n+1}=Q_n). Returning to the same question is not stagnation if evidence, hypotheses, or definitions have changed.

The healthy cycle is one in which REDDS continues to produce a materially updated research state and thereby gives rise to the next question.

## Human–AI functional roles

A compact role decomposition used with this cycle is

[
oxed{
	ext{Human: conception}
quad	imesquad
	ext{ChatGPT: excavation}
quad	imesquad
	ext{Claude / Code: audit}
}
]

or, operationally,

[
	ext{Conceive}
ightarrow
	ext{Excavate}
ightarrow
	ext{Audit}
ightarrow
	ext{Empty if necessary}
ightarrow
	ext{Rebuild}.
]

These are functional roles in the workflow, not claims that any one system is intrinsically reliable. Excavation and audit are intentionally separable: a system capable of digging deeply can also dig deeply in a wrong direction, so independent criticism and checking remain part of the cycle.
