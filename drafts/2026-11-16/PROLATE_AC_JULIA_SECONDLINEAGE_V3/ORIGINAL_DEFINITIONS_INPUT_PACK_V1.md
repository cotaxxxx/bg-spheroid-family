# CLEAN-ROOM INPUT PACK｜扁長 P1 a_c 第二系統

**版**: V1（2026-11-16）／**状態**: INPUT_PACK_DRAFT／NOT_FROZEN／NO_NUMERIC_EVIDENCE

このファイルだけを、第二系統 Julia 実装担当の**数学的入力**とする。第一系統の導出済みの核、Q/H4/Q_zの積分表現、数値評価・JSON、原稿全文、特殊関数の微分連鎖は提供しない。v2事前宣言に従う。

## 1. 原始的な幾何の定義

扁長軸を **z** とする（原リポジトリで y 軸と呼ぶ場合は y↔z の座標の交換のみ）。

形状パラメータ λ>1 の参照楕円体：

```math
K_\lambda=\{(x,y,z)\in\mathbb R^3:x^2+y^2+z^2/\lambda^2\le1\}.
```

内点 `p∈int(K_λ)`、境界点 `x∈∂K_λ`、境界の外向き単位法線 `ν_λ(x)`、表面積測度 `dA(x)` とする。

```math
\cos\alpha_{\lambda,p}(x)
=\frac{(x-p)\cdot\nu_\lambda(x)}{|x-p|},
\qquad\alpha_{\lambda,p}(x)=\arccos\!\bigl(\cos\alpha_{\lambda,p}(x)\bigr).
```

```math
E_\lambda(p)=
\frac1{3\operatorname{Vol}(K_\lambda)}
\int_{\partial K_\lambda}
\alpha_{\lambda,p}(x)^2\,[(x-p)\cdot\nu_\lambda(x)]\,dA(x).
```

体積保存での形状族は `K^\mathrm{vol}_\lambda=\lambda^{-1/3}K_\lambda`。ただし第二系統の幾何計算は参照 `K_\lambda` で実施し、幾何的な相似不変性を別に検証する。

## 2. 停留構造を表す導関数の**定義のみ**

赤道方向の軌跡 `p_r=(r,0,0)` と軸方向 `p_z=(0,0,z)` に対して

```math
Q(\lambda)=\left.\frac{d^2}{dr^2}E_\lambda(p_r)\right|_{r=0},\quad
H_4(\lambda)=\left.\frac{d^4}{dr^4}E_\lambda(p_r)\right|_{r=0},
```

```math
Q_z(\lambda)=\left.\frac{d^2}{dz^2}E_\lambda(p_z)\right|_{z=0},
\qquad
Q'(\lambda)=\frac{d}{d\lambda}Q(\lambda).
```

これらは「どの幾何量を計算するか」の定義であり、**被積分関数や評価式を与えていない**。第二系統の開発者は第一系統の式を見ず、ここから独立に微分・変数変換・定積分の式を導出しなければならない。

## 3. 定義域と証明対象の分類

- 局所分岐の係数・導関数の判定範囲：`λ∈[47/10,19/4]`。
- 端点を含む区間上での判定と、`Q(λ)=0` の根の囲いを行う。
- 必要となる定積分の変数変換・可微分性・微分交換・端点延長は**別の解析補題として証明する**。
- 署名付きの判定閾値、候補数値の桁数、実行予算、停止条件は実装の数学的入力ではないため、別の統治・認証契約にのみ保持する。

## 4. 受領・隔離の条件

入力として許容：上記の幾何定義、体積正規化、座標と定義域、Q/Q′/H₄/Q_z が意味する偏導関数。

入力として禁止：第一系統 `basepoint-geometry` の派生積分核、`₀F₁` 表現、記号微分チェーン、出力JSON、結果の小数値、旧 Julia 版の転写コード、先行スクリプト。

**Gate I0**：chat/Astraがここに派生式の混入がないことと元定義の一致を監査する。監査が終わるまで、このpackをFREEZE原本とは呼ばない。
