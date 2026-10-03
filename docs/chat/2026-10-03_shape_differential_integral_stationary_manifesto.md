# 形・微分・積分・停留構造
## ――数学側の綱領ノート

### 1. 綱領文

> **形は微分で記述され、積分で読み解かれる。**  
> **そして停留点がその構造を語り、分岐が構造の変化を語る。**

短縮版：

> **形は微分で記述され、積分で読み解かれる。**

英語版：

> **Shape is described locally by differential geometry and understood globally through integration.**  
> **Stationary points reveal its structure, while bifurcations reveal how that structure changes.**

---

### 2. 基本図式

研究の流れは、

[
\boxed{
\mathrm{Shape}
\xrightarrow{\mathrm{differentiation}}
\mathrm{Local\ Geometry}
\xrightarrow{\int}
\mathrm{Global\ Quantity}\ E_\lambda
\xrightarrow{d_pE_\lambda=0}
\mathrm{Stationary\ Structure}
\xrightarrow{\lambda}
\mathrm{Bifurcation}
}
]

と圧縮できる。

意味としては、

[
\boxed{
\text{形}
\longrightarrow
\text{局所}
\longrightarrow
\text{大域}
\longrightarrow
\text{構造}
\longrightarrow
\text{構造の変化}
}
]

である。

---

### 3. 微分 (d) ――局所的な応答

関数をブラックボックスとして

[
x\longmapsto f(x)
]

と見ると、微分が記述するのは単なる入力と出力ではなく、

[
\boxed{
\text{入力の微小変化}
\longmapsto
\text{出力の微小変化}
}
]

である。

多変数なら、

[
df=
\frac{\partial f}{\partial x}\,dx+
\frac{\partial f}{\partial y}\,dy,
]

より一般には、

[
dF_p:T_pM\longrightarrow T_{F(p)}N.
]

したがって (d) は、ある点・ある方向における**局所的な応答則**を取り出す装置として読める。

ただし「形は (d) で記述される」の (d) は、外微分だけを意味するものではない。曲率、接続、第一・第二基本形式、shape operator などを含む**微分的装置一般の提喩**として用いる。

---

### 4. 積分 (int) ――局所から大域へ

局所的に記述された量を全体にわたって束ねることで、大域量が得られる。

概念的には、

[
E_\lambda(p)=\int F_\lambda(p,x)\,dA(x)
]

の形で、

[
\boxed{
\text{local data}
\xrightarrow{\int}
\text{global quantity}
}
]

となる。

したがって「積分で読み解く」とは、局所情報を単に足し合わせるという意味だけではなく、**局所的な形の情報が全体として何を作るかを見ること**である。

---

### 5. 再び (d) ――停留構造

積分によって大域量 (E_\lambda) を得たところで解析は終わらない。再び微分する。

ここで (d_p) は、形状パラメータ (lambda) を固定したときの、基点・状態変数 (p) に関する微分を表す。

[
d_pE_\lambda=0.
]

座標表示では、

[
\nabla_p E_\lambda=0.
]

この零点集合が停留構造を与える。

したがって研究の核心には、

[
\boxed{
d\longrightarrow\int\longrightarrow d
}
]

という往復がある。

より意味を明示すれば、

[
\boxed{
\text{形}
\xrightarrow{d}
\text{局所}
\xrightarrow{\int}
\text{大域}
\xrightarrow{d_p}
\text{構造}
}
]

である。

---

### 6. 分岐 ――構造の変化

形状パラメータを (lambda) とすれば、

[
d_pE_\lambda=0
]

の解集合を (lambda) とともに追うことで、停留構造の変化を調べられる。

候補となる退化点では、例えば

[
\det D_p^2E_\lambda=0
]

のような Hessian の退化が現れ得る。

ただし Hessian の退化だけで pitchfork 等の分岐型が確定するわけではない。対称性、横断性、非退化条件、高次項などの追加条件が必要になる。

したがって、

[
\boxed{
\text{停留点が構造を語り、分岐が構造の変化を語る}
}
]

という後半の綱領文につながる。

---

### 7. (d) と (int) を結ぶ紋章

この思想を最も深く圧縮する等式の一つが Stokes の定理である。

[
\boxed{
\int_M d\omega=\int_{\partial M}\omega
}
]

integration pairing

[
\langle\omega,c\rangle=\int_c\omega
]

を使えば、

[
\boxed{
\langle d\omega,c\rangle=
\langle\omega,\partial c\rangle
}
]

と書ける。

ここで外微分 (d) と境界作用素 (partial) は、積分による pairing を介して双対的に結び付く。

なお、これをそのまま「(d) と (partial) が随伴」と呼ぶと、内積に対する formal adjoint (d^*) と混同し得るため、ここでは**双対的対応**と表現する。

---

### 8. 三つの表現

この綱領は用途に応じて三段階で使用する。

#### 文章版

> **形は微分で記述され、積分で読み解かれる。**  
> **そして停留点がその構造を語り、分岐が構造の変化を語る。**

#### 研究図式版

[
\boxed{
\mathrm{Shape}
\rightarrow
\mathrm{Local\ Geometry}
\rightarrow
E_\lambda
\rightarrow
\mathrm{Stationary\ Structure}
\rightarrow
\mathrm{Bifurcation}
}
]

#### 紋章版

[
\boxed{
d\longrightarrow\int\longrightarrow d
}
]

その根底を象徴する等式として、

[
\boxed{
\int_Md\omega=\int_{\partial M}\omega
}
]

を置く。

---

### 9. REDDS との役割分離

REDDS は**研究方法側**の綱領である。

[
\boxed{\text{🐟 REDDS：問いを掘る}}
]

一方、本ノートは**数学対象側**の綱領である。

[
\boxed{\text{Mathematics：形を読み解く}}
]

したがって両者は混同せず、

[
\boxed{
\text{問いを掘る}
\quad\longrightarrow\quad
\text{形を読み解く}
}
]

という別階層の関係として保持する。

---

### 10. 確定文

> **形は微分で記述され、積分で読み解かれる。**  
> **そして停留点がその構造を語り、分岐が構造の変化を語る。**

[
\boxed{
\text{形}
\xrightarrow{d}
\text{局所}
\xrightarrow{\int}
\text{大域量 }E_\lambda
\xrightarrow{d_pE_\lambda=0}
\text{停留構造}
\xrightarrow{\lambda}
\text{構造の変化}
}
]

本ノートでは、この文章を数学的な中心命題としてではなく、**研究全体を圧縮した綱領文**として位置付ける。

---

### 状態

- Content audit: PASS
- Countersign: received
- 本版で (d_p) を「(lambda) を固定した (p) 方向の微分」と明示し、§5–§6 の記号を統一した。
