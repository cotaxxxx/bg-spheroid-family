統合補題 G0/E1 v3 — 一様 \(G_t\) 支配関数と端点 Lipschitz 評価（紙上導出草稿）
状態：DRAFT v3 / PAPER DERIVATION CANDIDATE / GT_SOURCE_FORMULA_IDENTIFICATION_PASS / GT_ANALYTIC_DEPENDENCY_EXTERNAL_AUDIT_PENDING / NOT_BINDING / NOT_CERTIFIED / NOT FROZEN。
基準：STATE v1.12 / 32218d7855e3e6218dddbe315eacb38cd2dd8295。
前版監査：G0/E1 v2 = CONDITIONAL PASS。新規南半分評価 \(M_S\) は PASS。
依存原典は引き続き EXTERNAL_AUDIT_PENDING / NOT_BINDING：
- OBLATE_ENDPOINT_C1_LEMMA blob 5afa815ff24760ab5ebbb63bcbae912c9c7a84c6
- MONOTONE_TUBE_C2_INTERCHANGE_LEMMA blob 7cb9b8091596510203d74e09387bc1e8188b8b47
この v3 は v2 の整理版である。新しい数学的主張は追加せず、監査で認められた南半分評価を維持し、(i) \(\pi<22/7\) の根拠、(ii) machine Gt 実装4モジュールの blob pin、(iii) GT_IDENTIFICATION_OPEN の状態分解、の3点を反映する。数値本走・証明書生成・commit は行わない。
1. 定義と目標
\(s\in[0,\sqrt2]\), \(t\in[1/2,1)\), \(\lambda\in[2/5,5/8]\) とする。
\[
\mu=1-s^2,\qquad
\delta=1-t,\qquad
d=s^2-\delta,
\]
\[
A=1-t\mu,\qquad
q=s^2(2-s^2)+\lambda^2d^2,
\]
\[
w^2=\lambda^2s^2(2-s^2)+\mu^2,\qquad
\gamma=\frac{\lambda A}{w\sqrt q},
\]
\[
\alpha=\arccos\gamma,\qquad
R=\frac{\alpha}{\sin\alpha}.
\]
端点補題 Lemmas 3,5 により
\[
F_t=s[-\mu\alpha^2-2AR\gamma_t],
\qquad
g(t,\lambda)=\int_0^{\sqrt2}F_t\,ds,
\]
および
\[
g(1,\lambda)=B_{\mathrm{ob}}(\lambda)
\]
とする。
また
\[
H=(1-s^2)(2-s^2)
+\lambda^2(2-s^2)(s^2-\delta),
\]
\[
N=-s^2H,
\qquad
\gamma_t=\frac{\lambda N}{wq^{3/2}}.
\]
C2 §2–3 による second-\(t\) derivative と corner-scaled 恒等式は
\[
G_t=\partial_tF_t=T_1+T_2+T_3
\]
であり、
\[
\rho=\frac{s}{\sqrt q},
\qquad
\phi=\frac{d}{\sqrt q},
\qquad
\widehat A=\frac{A}{\sqrt q},
\]
\[
R_\gamma=\frac{\gamma R-1}{1-\gamma^2}
\]
（\(\gamma=1\) では連続延長）として
\[
T_1=
-\frac{4(1-s^2)R\lambda\rho^3H}{w},
\]
\[
T_2=
-\frac{2R_\gamma\lambda^2H^2\widehat A\rho^5}{w^2},
\]
\[
T_3=
-\frac{2R\lambda^3\widehat A\rho^3
\left[3\phi H-(2-s^2)\sqrt q\right]}{w}.
\]
全域で
\[
0<\gamma\le1,\qquad
1\le R\le\frac{\pi}{2},
\qquad
|R_\gamma|\le1,
\qquad
w\ge\lambda_-=\frac25.
\]
有理化では古典的不等式
\[
\pi<\frac{22}{7}
\]
を用い、
\[
\frac{\pi}{2}<\frac{11}{7}
\]
とする。
さらに scaled identity
\[
\rho^2(2-s^2)+\lambda^2\phi^2=1,
\]
\[
\widehat A=(2-s^2)s\rho-(1-s^2)\phi
\]
を用いる。
2. 北半分 \(N\)：具体的な有理上界
\(s\in[0,1]\) では
\[
2-s^2\in[1,2].
\]
したがって
\[
0\le\rho\le1,
\qquad
|\phi|\le\frac1{\lambda_-}=\frac52,
\]
\[
|\widehat A|
\le2+\frac52
=\frac92.
\]
端点補題 Lemma 2 により
\[
|H|
\le2+2\lambda_+^2
<4.
\]
また \(|d|\le1\) なので
\[
q
\le s^2(2-s^2)+\lambda_+^2d^2
\le1+\frac{25}{64}
<2,
\]
従って
\[
\sqrt q<\frac32.
\]
ここで
\[
\lambda\le\frac58,\qquad
w\ge\frac25,\qquad
R\le\frac{11}{7},\qquad
|R_\gamma|\le1
\]
を用いる。
\(T_1\)
\[
|T_1|
\le
4\cdot\frac{11}{7}\cdot\frac58\cdot4\cdot\frac{5}{2}
<40.
\]
\(T_2\)
\[
|T_2|
\le
2\left(\frac58\right)^2
4^2
\frac92
\left(\frac52\right)^2
<352.
\]
\(T_3\)
\[
|T_3|
\le
2\cdot\frac{11}{7}
\left(\frac58\right)^3
\frac92
\left[
3\cdot\frac52\cdot4
+
2\cdot\frac32
\right]
\frac52
<300.
\]
よって
\[
|G_t|
\le |T_1|+|T_2|+|T_3|
<692
<1000.
\]
したがって北半分では
\[
\boxed{M_N:=1000}
\]
を一様支配定数として採用できる。
この評価は C2 §4 の式を用いるが、\(t\ge63/64\) には依存せず、\(t\ge1/2\) と \(\lambda\in[2/5,5/8]\) 上で成立する。
3. 南半分 \(S\)：明示上界
\(s\in[1,\sqrt2]\), \(\delta\in[0,1/2]\) では
\[
d=s^2-\delta
\ge1-\delta
=t
\ge\frac12.
\]
したがって、端点補題 Lemma 2 と同じ論証により
\[
q
\ge\lambda^2d^2
\ge
\left(\frac25\right)^2
\left(\frac12\right)^2
=
\frac1{25}.
\]
よって
\[
\sqrt q\ge\frac15.
\]
さらに
\[
0\le\rho
=\frac{s}{\sqrt q}
\le5\sqrt2,
\]
scaled identity から
\[
|\phi|
\le\frac1{\lambda_-}
=\frac52.
\]
また
\[
|1-s^2|\le1,\qquad
0\le2-s^2\le1,
\]
より
\[
|\widehat A|
\le
(2-s^2)s\rho
+
|1-s^2||\phi|
\le
10+\frac52
=
\frac{25}{2}.
\]
端点補題 Lemma 2 の南半分評価から
\[
|H|
\le
\frac14+\lambda_+^2
=
\frac14+\frac{25}{64}
=
\frac{41}{64}
<1.
\]
さらに
\[
0\le s^2(2-s^2)\le1,
\qquad
0\le d\le2,
\]
なので
\[
q
\le
1+4\left(\frac58\right)^2
=
\frac{41}{16}
<4,
\]
従って
\[
\sqrt q<2.
\]
有理化に
\[
\sqrt2<\frac32
\]
を用いれば
\[
\rho^3
\le(5\sqrt2)^3
=
250\sqrt2
<375,
\]
\[
\rho^5
\le(5\sqrt2)^5
=
12500\sqrt2
<18750.
\]
\(T_1\)
\[
|T_1|
\le
4\cdot\frac{11}{7}
\cdot\frac58
\cdot375
\cdot\frac52
<4000.
\]
\(T_2\)
\[
|T_2|
\le
2
\left(\frac58\right)^2
\frac{25}{2}
\cdot18750
\left(\frac52\right)^2
<1200000.
\]
\(T_3\)
\[
|T_3|
\le
2\cdot\frac{11}{7}
\left(\frac58\right)^3
\frac{25}{2}
\cdot375
\left[
3\cdot\frac52+2
\right]
\frac52
<100000.
\]
したがって
\[
|G_t|
\le
|T_1|+|T_2|+|T_3|
<
4000+1200000+100000
=
1304000.
\]
ゆえに南半分では
\[
\boxed{M_S:=1304000}
\]
を採用できる。
これは既存 C2 §5 の「compactness により有限」という存在評価を、同じ scaled identity から具体的な有理上界に置き換えたものである。v2 監査では、この新規南半分評価は PASS と判定された。
4. 一様微分交換 G0 と端点 E1
\[
M:=\max(M_N,M_S)=1304000
\]
とする。
すると全
\[
s\in[0,\sqrt2],\qquad
t\in[1/2,1),\qquad
\lambda\in[2/5,5/8]
\]
について
\[
|G_t(s,t,\lambda)|\le M.
\]
\(s=0,t=1\) では \(q=0\) となるが、この一点は \(s\)-積分における零測度点であり、\(t=1\) の \(G\) は固定 \(s>0\) の \(t\to1-\) 極限として扱う。
端点補題 Lemma 3 により
\[
g(t,\lambda)
=
\int_0^{\sqrt2}F_t(s,t,\lambda)\,ds.
\]
C2 §2 の
\[
\partial_tF_t=G_t
\]
と上の一様支配により、\(t<1\) で微分と積分を交換でき、
\[
\partial_tg(t,\lambda)
=
\int_0^{\sqrt2}G_t(s,t,\lambda)\,ds.
\]
従って
\[
|\partial_tg(t,\lambda)|
\le
\int_0^{\sqrt2}|G_t|\,ds
\le
\sqrt2\,M.
\]
\(t<u<1\) で積分し、端点補題 Lemma 5 の
\[
g(u,\lambda)\to B_{\mathrm{ob}}(\lambda)
\qquad (u\to1-)
\]
を用いると
\[
|g(t,\lambda)-B_{\mathrm{ob}}(\lambda)|
\le
\sqrt2\,M(1-t).
\]
さらに
\[
\sqrt2<\frac32
\]
より
\[
|g(t,\lambda)-B_{\mathrm{ob}}(\lambda)|
\le
\frac32M(1-t).
\]
よって
\[
\boxed{\alpha=1}
\]
および
\[
\boxed{
C_\Lambda
=
\frac32M
=
1956000
}
\]
を、すべての
\[
\Lambda\subseteq[2/5,5/8]
\]
に共通する明示有理定数として採用できる。
すなわち
\[
\boxed{
|g(t,\lambda)-B_{\mathrm{ob}}(\lambda)|
\le
1956000(1-t)
}
\]
が得られる。
この評価は \(B_{\mathrm{ob}}\) の符号証明を代替しない。また \(C_\Lambda(1-t)\) が粗すぎて箱を消去できない場合、契約で別途固定した direct Gt enclosure を用いる必要がある。
\(t=1\) での左微分
各固定 \(s>0\) について、C2 §6 と同様に
\[
t\to1-
\]
で \(q,\gamma,R,R_\gamma,T_1,T_2,T_3\) の点ごとの極限が存在する。
一様支配 \(M\) により支配収束を適用し、
\[
\lim_{t\to1-}\partial_tg(t,\lambda)
=
\int_0^{\sqrt2}G_{\mathrm{boundary}}(s,\lambda)\,ds.
\]
端点補題 Lemma 5 の \(g\) の連続性と微積分学の基本定理から、
\[
\boxed{
\partial_tg(1-,\lambda)
=
\int_0^{\sqrt2}G_{\mathrm{boundary}}(s,\lambda)\,ds
}
\]
を得る。
ここで \(t=1\) の導関数は 左側微分としてのみ主張する。
5. machine Gt とのソース式同一性
v2 では MACHINE_GT_IDENTIFICATION_OPEN としていたが、その後、研究用 PC 上で machine Gt が参照する4モジュールを読み取りのみで確認した。
5.1 blob pin
系統	ファイル	blob
producer	producer/monotone_tube_refinement_producer.py	c2fee40053ab055ce352e93e1c6d1fc43e46310a
producer	producer/monotone_tube_interval_producer.py	b6d96df223c0e423e804d96f4892a8e818c05827
checker	checker/monotone_tube_refinement_checker.py	15d660265552fc2f2c83ffe897ed5efab8514da2
checker	checker/monotone_tube_interval_checker.py	f2fa2a5a42d35b8b77e3c63fa0d9ad48ce562a77


global kernel は既存 pin：
- producer kernel 67dda838369302010ef3d589937b834b96ede4d8
- checker kernel 4eaca55ddf79b437fc756d666294372e5d1a6ba4
を用いる。
5.2 ordinary chart
producer の ordinary 実装は
\[
T_1=
-\frac{4\mu R\lambda\rho^3H}{w},
\]
\[
T_2=
-\frac{2R_\gamma\lambda^2H^2\widehat A\rho^5}{w^2},
\]
\[
T_3=
-\frac{2R\lambda^3\widehat A\rho^3
(3\phi H-(2-s^2)\sqrt q)}{w}
\]
をそのまま生成する。
checker の _ordinary_refinement も同じ3式を別実装で形成する。
従って、解析原典 C2 §3 の
\[
G_t=T_1+T_2+T_3
\]
と producer/checker ordinary implementation は、符号・係数・\(\lambda\) の次数・\(\rho\) の次数・\(w\) の分母・角括弧内部の式までソースレベルで一致する。
5.3 corner chart
producer の corner 実装も同じ
\[
T_1,\quad T_2,\quad T_3
\]
を interval hull 上で形成する。
checker の _corner も同じ3項の和を直接形成する。
corner では
\[
R\in[1,\pi/2],
\qquad
R_\gamma\in[-1,-1/3]
\]
等の enclosure を使用するが、計算する代数式自体は ordinary chart と同じ \(T_1+T_2+T_3\) である。
5.4 global gt_box
producer global kernel と checker global kernel は、いずれも \(s\)-panel ごとに
- \(t\)-box が \(t=1\) に達し、
- かつ最初の \(s\)-panel
で corner chart を使用し、それ以外は ordinary chart を使用する。
各 panel で得た \(T_1+T_2+T_3\) の enclosure を panel 幅で積分し、gt_box を形成する。
以上から、
\boxed{\texttt{GT_SOURCE_FORMULA_IDENTIFICATION_PASS}}
とする。
これは 解析式と machine source が同じ \(G_t\) 式を実装していることのソースレベル確認である。
ただし、以下はこの判定だけからは昇格しない：
1. C2 の解析的 second-\(t\) derivative 自体の外部監査。
2. R, R_\gamma, corner hull、series enclosure 等の interval implementation の正当性。
3. machine certificate 全体の binding status。
従って machine Gt を「完全に認証済み」とは扱わない。
状態は
\boxed{\texttt{GT_ANALYTIC_DEPENDENCY_EXTERNAL_AUDIT_PENDING}}
を併記する。
6. 状態と残る監査条件
この v3 での状態を次のように固定する。
紙上数学
- 北半分明示上界 \(M_N=1000\)：監査候補。
- 南半分明示上界 \(M_S=1304000\)：v2 監査 PASS。
- 一様上界 \(M=1304000\)。
- E1：\[
  \alpha=1,\qquad C_\Lambda=1956000.
  \]
- \(t=1\) は左微分のみ主張。
machine source
- GT_SOURCE_FORMULA_IDENTIFICATION_PASS
- producer/checker ordinary：解析式 \(T_1+T_2+T_3\) とソース式一致。
- producer/checker corner：同じ3項の interval hull。
- global gt_box：panel 積分として同式を使用。
継続条件
- GT_ANALYTIC_DEPENDENCY_EXTERNAL_AUDIT_PENDING
- OBLATE_ENDPOINT_C1_LEMMA (5afa815f...) は NOT_BINDING
- MONOTONE_TUBE_C2_INTERCHANGE_LEMMA (7cb9b809...) は NOT_BINDING
- interval enclosure 全体の binding 判定は未実施
- NOT_CERTIFIED
- NOT FROZEN
この文書は数値本走・証明書生成・commit を許可しない。依存補題の外部監査が閉じるまでは FREEZE しない。