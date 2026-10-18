# D4 中心下界・全 λ 域への拡張 — exact paper audit

2026-10-18 JST / Judge 提出用 / Code 再導出

**総合判定：PASS conditional on P1 §1 のエネルギー正規化・定義、および中心近傍の微分交換と H の軸上同定（P1 §2、Lemma V(b)、Lemma 6.1 の内部部分）。**

\[
\boxed{H(0,0;\lambda)\ge
2\lambda\left[\lambda^2-\frac4{27}(1-\lambda^2)^2\right]
\ge\frac{416}{9375}>0},\qquad
\lambda\in[2/5,33/50].
\]

係数・符号・端点・算術に誤りはない。主張の修正は不要。積の下界を取る前に N の正値性を明記すると証明順序が完全になる。中心外の下界、D4 全箱の認証、A/B 方式選定、V4、FREEZE、実行許可については裁定しない。

## 1. 原典と監査の性質

出発原典は family main の読み戻し時 HEAD を固定した以下の文書である。

- Repository: `cotaxxxx/bg-spheroid-family`
- Commit: `24392bb23d54c587aaf425c15d63d972a6690393`
- Path: `drafts/2026-10-13/D4_CENTER_BAND_SOURCE_AUDIT_V0.md`
- 使用箇所：§3 正則化・対称性、§4 中心公式。
- Git blob: `e52ec2a3c07fc18ae923ee09892be062c60917db`
- SHA-256: `aa374e0cfae0457484deae18885ffb187bbb9dbd16a69dcfcd44b90a9fca3221`

[固定原典](https://github.com/cotaxxxx/bg-spheroid-family/blob/24392bb23d54c587aaf425c15d63d972a6690393/drafts/2026-10-13/D4_CENTER_BAND_SOURCE_AUDIT_V0.md)

P1 は `cotaxxxx/bg-oblate-spheroid`、commit `6c6282a8acbf467bcbe6a7e32236e1d32a91f400`、`analysis/D_OB_P1_DESIGN_NOTE.md`。SHA-256 は `2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9`、blob は `f81e120e44a866d206117d4fab5fac627f26ccd1`。これは中心原典が引用する P1 と同一 blob / SHA-256 である。

[固定 P1](https://github.com/cotaxxxx/bg-oblate-spheroid/blob/6c6282a8acbf467bcbe6a7e32236e1d32a91f400/analysis/D_OB_P1_DESIGN_NOTE.md)

両原典を GitHub から取得し、UTF-8 bytes から SHA-256 と Git blob SHA-1 を再計算した。原典の旧 λ 帯の定量下界を全帯へ流用せず、中心公式自体の導出と定義域を再確認した。

本監査では提示された結論を前提にせず、P1 の密度微分から中心式を再構成し、不等式と単調性を紙上で導いた。算術は新規の Python `fractions.Fraction` スクリプトで確認した。他者の数値出力の readback だけではない。ただし同一会話に既存導出が提示されているため、情報遮断された clean-room 監査や別モデル系統の独立性までは主張しない。

## 2. 中心公式の再導出と正規化 — PASS

P1 §1 の規約は半軸 (1,1,λ)、密度 F_E=hG(γ)、G(γ)=arccos²γ、

\[
E(p)=\frac1{4\pi\lambda}\int_{-1}^1\int_0^{2\pi}F_E\,d\phi\,d\mu.
\]

y=μ²、c=1−λ²、q=1−cy、b=√(1−y)cosφ とする。z=0 の近傍では

\[
h=\lambda(1-\rho b),\qquad
D^2=q+\rho^2-2\rho b,\qquad \gamma=h/(wD).
\]

ρ=0 で直接微分して

\[
h=\lambda,\quad h_\rho=-\lambda b,\quad h_{\rho\rho}=0,
\]
\[
\gamma_\rho=\gamma b(q^{-1}-1),\qquad
\gamma_{\rho\rho}=\gamma[-q^{-1}+b^2(3q^{-2}-2q^{-1})].
\]

G′=−2R、G″=−2R′ を用いれば

\[
F_{E,\rho\rho}=4\lambda bR\gamma_\rho
-2\lambda R'\gamma_\rho^2-2\lambda R\gamma_{\rho\rho}.
\]

中心では w,q,γ が φ に依存せず、平均 ⟨b²⟩φ=(1−y)/2。φ 積分の 2π と正規化 1/(4πλ) は 1/(2λ) を与える。よって

\[
H(0,0;\lambda)=E_{\rho\rho}(0,0;\lambda)
=\int_{-1}^1\left[
\frac{\gamma R}{q^2}\left\{q+(1-y)(2q-q^2-3/2)\right\}
-\frac{R'\gamma^2(1-y)(1-q)^2}{2q^2}\right]d\mu.
\]

q=1−cy を展開すると

\[
q+(1-y)(2q-q^2-3/2)
=\frac12+\left(\frac12-c\right)y-c^2y^2(1-y)=N.
\]

依頼書および原典 §4 と一致する。μ 積分は区間長2の通常の積分であり、確率測度への再正規化は行わない。この導出は 0<λ<1 で有効で、旧下界の仮定 λ≥119/200 を使っていない。

## 3. N の下界・適用域 — PASS

全対象帯で

\[
\frac{1411}{2500}\le c\le\frac{21}{25},\qquad
\frac{1411}{2500}>\frac12.
\]

y∈[0,1] に対し

\[
\frac4{27}-y^2(1-y)
=\left(y-\frac23\right)^2\left(y+\frac13\right)\ge0.
\]

\(B(\lambda):=\lambda^2-\frac4{27}(1-\lambda^2)^2=1-c-4c^2/27\) と置くと、さらに直接

\[
\boxed{N-B(\lambda)
=(c-1/2)(1-y)
c^2\left[\frac4{27}-y^2(1-y)\right]\ge0}.
\]

この分解は端点を含む全域を覆い、個々の項の符号も明示する。

B′(λ)=2λ[1+(8/27)(1−λ²)]>0 なので

\[
\boxed{N\ge B(\lambda)\ge B(2/5)=104/1875>0}.
\]

この正値性を確立してから係数の下界と掛け合わせる。

## 4. R、R′、分母、端点 — PASS

R は P1 Lemma 3.2 の

\[
R(\gamma)=\frac{\arccos\gamma}{\sqrt{1-\gamma^2}},
\qquad R'=\frac{dR}{d\gamma}
\]

であり、λ 微分・μ 微分ではない。γ=1 では可除特異点の延長を用いる。

\[
\lambda^2\le q=1-cy\le1,\quad
\lambda^2\le w^2=\lambda^2+(1-\lambda^2)y\le1.
\]

従って q,w²≥4/25、w≥2/5、q²≥16/625、w√q≥4/25。さらに

\[
w^2q-\lambda^2=c^2y(1-y)\ge0
\]

なので γ≤1。一方 w√q≤1 から γ≥λ>0。従って原典の R≥1、R′≤0 が全域で適用できる。

これらの符号は共通積分でも確認できる：

\[
R=2\int_0^1\frac{dt}{1+t^2+(1-t^2)\gamma},\quad
R'=-2\int_0^1\frac{1-t^2}{[1+t^2+(1-t^2)\gamma]^2}\,dt.
\]

分母は [1,2] に入り、R≥1、R′≤0。γ=1 では R=1、R′=−1/3 で有限である。

中心式の第2項は、R′以外の各因子が非負、分母が正で、先頭に負号があるため非負。したがって捨てても下界を保つ。

また

\[
\boxed{\frac{\gamma R}{q^2}\ge\lambda}.
\]

端点の確認：y=0 では (q,w,γ)=(1,λ,1)、y=1（μ=±1）では (q,w,γ)=(λ²,1,1)。両方で第2項は0となり、第1項も有限。√(1−γ²) の見かけの0を数値除算しない。

## 5. 積分・単調性・exact arithmetic — PASS

§3 の N≥B(λ)>0 と §4 を合わせると、各 μ において

\[
\frac{\gamma R}{q^2}N\ge\lambda N\ge\lambda B(\lambda).
\]

従って

\[
H(0,0;\lambda)\ge\int_{-1}^1\lambda B(\lambda)\,d\mu
=2\lambda B(\lambda).
\]

f(λ)=2λB(λ) とすれば

\[
f'(\lambda)=2B(\lambda)+2\lambda B'(\lambda)>0
\]

が全帯で成立する。これは下界関数 f の単調性であり、H 自身の λ 単調性の主張ではない。

左端では

\[
B(2/5)=\frac4{25}-\frac4{27}\left(\frac{21}{25}\right)^2
=\frac{104}{1875},
\]

\[
2\cdot\frac25\cdot\frac{104}{1875}=\boxed{\frac{416}{9375}}>0.
\]

新規 `check_fractions.py` はこの算術、c の exact 端点、分母定数、および y²(1−y) の因数分解を Fraction で確認した。sampling・parameter scan・区間計算は用いていない。全域の不等式と微分交換は本稿の紙上論証である。

## 6. 継承条件と証明範囲

1. **正規化**：P1 §1 の半軸 (1,1,λ) と prefactor 1/(4πλ) を使用。体積保存の座標へは数値定数を無換算で移さない。
2. **微分交換**：中心は境界ではなく内部である。中心で D=√q≥λ≥2/5。さらに全 λ 共通の Euclidean 球 |p|≤1/5 は内部にあり、D≥2/5−1/5=1/5。γ=1 での角関数の可除延長を用いれば、有限測度上の密度とその2階微分はこの compact で有界・連続となる。P1 §2 / Lemma V(b) の通常の微分交換で足りる。
3. **H の中心値**：内部の偶性と FTC から H(ρ,z)=∫₀¹E_ρρ(sρ,z)ds、従って H(0,0)=E_ρρ(0,0)。P1 Lemma 6.1 の内部部分である。ρ=0 で E_ρ/ρ を直接計算しない。
4. **境界条件**：Lemma V(c) の表面境界への連続延長は今回の中心定理に追加で必要ではない。その全域証明や外部監査を今回完了したとはしない。P1 原典の外部監査条件・統治 status を本監査によって昇格しない。
5. **中心のみ**：正値性は横方向2階係数についての結論である。中心自身は対称性による停留点であり、軸方向 E_zz の符号は主張していない。r>0 の固定半径領域や D4 全箱の正値性もまだ結論しない。

## 7. 指摘一覧と Judge への返答

**blocking finding：0件。FAIL に相当する符号・係数・定義域の誤りはない。**

- **N1（証明順序の明記）**：係数下界を掛ける前に N≥B(λ)≥104/1875>0 を記載する。負の N に正係数の下界を機械的に掛ける論法ではないことを明確にする。主張の変更は不要。
- **N2（依存範囲の明記）**：今回必要なのは P1 normalization、内部微分交換、内部軸延長。境界までの Lemma V(c) を再監査済みとはしない。
- **N3（結論範囲）**：f(λ) の単調性と H 自身の単調性を区別し、全 λ の中心下界を中心外の一様下界として流用しない。

**Judge 向け結論：提示された全 λ 域の中心下界は、上記の具体的継承条件の下で PASS。採否および A/B 設計比較は Judge に返す。**

本作業では A/B 方式選択、V4 PREDECLARE、FREEZE、研究機本計算、D5 実行・resume、run-directory 変更、commit/push を行っていない。
