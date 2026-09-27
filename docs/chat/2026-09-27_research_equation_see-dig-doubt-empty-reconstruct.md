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


## Refinement: external input, decision projection, and guarded Empty

The first research-state form,

[
X_{n+1}=mathrm{REDDS}(X_n),
]

is useful but too deterministic. Research receives responses from outside the current state: numerical experiments, audits, counterexamples, proofs, failures, and other observations. Let (I_{n+1}) denote this new external input. A more faithful formulation is

[
oxed{
X_{n+1}inmathcal R(X_n;I_{n+1}),
qquad mathcal R=mathrm{REDDS}.
}
]

The set-valued notation allows more than one legitimate reconstruction from the same state and evidence. Whether the process returns to an equivalent state is therefore not a property of REDDS alone; it also depends on the response supplied by the mathematical or computational world.

### Decision-level stagnation

Literal equality (X_{n+1}=X_n) is too strong as a definition of stagnation. A new sample can change (E_n) without changing any research-relevant judgment.

Introduce a decision projection

[
pi:Xlongrightarrowmathcal J,
]

where (mathcal J) records the judgments, claims, or decisions currently licensed by the research state.

Then

[
oxed{
pi(X_{n+1})=pi(X_n)
}
]

expresses **decision-level stagnation**. In particular,

[
X_{n+1}
eq X_n,
qquad
pi(X_{n+1})=pi(X_n)
]

means that information has accumulated but no decision-relevant state has changed.

Conversely, a cycle can revisit the same verbal question (Q) without stagnating whenever evidence, hypotheses, definitions, or licensed judgments have materially changed.

### Guarded Empty

Empty must itself be evidence-disciplined. Doubt alone is not permission to erase a claim. Otherwise the method risks deleting claims that remain legitimately supported.

Let (C) be a claim in the current research state and let (G(E,C,ho)) be an evidence guard testing whether the current evidence (E) supports claim (C) in its assigned role (ho). Then schematically,

[
oxed{
mathrm{Empty}_G(C)=
egin{cases}
C, & G 	ext{ supports the present role},\
operatorname{downgrade}(C), & G 	ext{ supports only a weaker role},\
arnothing, & G 	ext{ no longer supports a role in the rebuilt structure}.
end{cases}
}
]

Thus Empty means:

> **remove or downgrade a claim when its recorded evidence strength no longer supports the role assigned to it.**

This connects REDDS directly to the evidence discipline used in the project. The working evidence-strength distinctions include:

- **Established**
- **Diagnostic hypothesis**
- **Strong diagnostic evidence**
- **Proof only with lemma**

These labels are not interchangeable. A claim may survive Empty while being downgraded to a weaker evidential role.

## Worked example: D-OB, September 2026

The D-OB work during the week of 2026-09-27 provides an operational example of the cycle. This section is a methodology record only; it is **not D-OB machine evidence, producer/checker evidence, or a proof artifact**.

The high-level question remained approximately unchanged:

> **Can (H>0) be closed mechanically?**

At the level of (Q), the project could therefore appear stationary. At the level of the research state (X=(Q,E,H,D)), however, it changed substantially.

The evidence state moved through repeated smoke failures, a resumable execution design, and a failure map reaching roughly 15,000 nodes. The question text remained stable while the evidential and diagnostic state changed. This is precisely why (Q) alone is an insufficient state variable.

Several Empty operations also occurred in the working process:

1. a claimed global cover for (U_{m check}) was withdrawn;
2. the statement that brute-force subdivision was dead was downgraded to a **design inference** rather than retained as a stronger conclusion;
3. a claim that the canonical push was complete was returned to an unresolved/unconfirmed state when confirmation was insufficient.

These are examples of guarded Empty: the record is not erased merely because it is doubted; rather, its status is withdrawn or downgraded when the evidence no longer licenses the role it had been given.

The subsequent reconstruction is correspondingly not just “increase the cap and try again.” The design direction is being reformulated around a **machine core plus analytic delegation**. In REDDS terminology:

[
	ext{Doubt}
ightarrow
	ext{Empty unsupported roles}
ightarrow
	ext{Rebuild the certification architecture}.
]

This episode also illustrates the role of the decision projection. Large changes in raw computational evidence need not themselves constitute progress if they leave (pi(X)) unchanged; conversely, a single audit result can materially change (pi(X)) by forcing a withdrawal, downgrade, or new admissible claim.

The worked example therefore motivates the refined equation:

[
oxed{
X_{n+1}inmathrm{REDDS}(X_n;I_{n+1}),
qquad
	ext{progress judged through changes in }pi(X).
}
]

The purpose of 🐟 REDDS is not to maximize motion inside (X), but to create disciplined conditions under which genuinely new questions and justified research decisions can emerge.

## Placement

This file is the canonical methodology/history note for the SDDER/REDDS formulation.

If the D-OB episode is later used in a formal project paper or engineering/process record, only the relevant project-specific portion should be carried over, with its claims re-grounded in the appropriate D-OB artifacts. This methodology note must not be promoted into machine evidence merely because it records the history accurately.
