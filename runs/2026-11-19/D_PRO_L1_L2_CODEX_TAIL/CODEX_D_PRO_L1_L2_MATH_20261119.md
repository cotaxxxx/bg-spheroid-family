# D-PRO の針側尾部　非極の横微分と軸上の縦微分

2026-11-19 ｜ Codex → Judge・chat ｜ **DIAGNOSTIC_ONLY / NOT_EVIDENCE**

## 1. 得られた十分条件

参照座標は \(q=(\rho,0,z)\)、物理座標は \(p=(\rho,0,\lambda z)\)。縦微分は参照座標の \(z\) で取る。相似不変性により赤道半径を 1 と置く。\(\epsilon=1/\lambda,\ S=\sqrt{1-z^2},\ S_0=2^{-12}\)。

| 対象 | 本稿の解析的な十分条件 | 範囲 |
|---|---|---|
| L1-A | \(R_H^{(2)}/S\le29/2\) | \(\lambda\ge4096,\ S_0\le S\le1,\ 0\le\rho\le S\)。右端は内側トレース |
| L1-B | \(T_\lambda(z)>29/2,\ \partial_\lambda T_\lambda(z)>0\) | 前行の領域。従って \(H<0\) |
| L2 | \(E_z(0,z)/z\ge3/(10\lambda^2)\) | \(\lambda\ge5,\ |z|<1\)。中心は \(E_{zz}(0,0)\)。焦点より外側では既存の G1 を使用 |
| 組立 | \(\Lambda_1=4096\) は十分 | 既存の G21 と合わせ、内部の停留点は中心のみ。横二方向は負、縦方向は正 |

これは独立監査に提出する導出である。定数は最適値ではない。以下は有限 \(\epsilon>0\) の解析で、試作の値を前提としない。既存の監査入力と新しい不等式の境界は §9 に記した。

## 2. 元の微分と、二つの尾を引く厳密な積分

\(\mu=\xi_z,\ s=\sqrt{1-\mu^2},\ x=s\cos\phi,\ y=s\sin\phi,\ t=(\mu-z)/\epsilon,\ w=\epsilon t\) と置く。
\[
 A=(x-\rho)^2+y^2,\quad k=1-z\mu-\rho x,\quad B=s^2+\epsilon^2\mu^2,\quad
 D^2=t^2+A,\quad \gamma=k/(D\sqrt B),\quad m=s^2/\sqrt B .
\]
\(\overline{\cdot}\) は \(\phi\) の確率平均、球面平均は \(\tfrac12\int_{-1}^1\overline{\cdot}\,d\mu\)。\(F(\gamma)=\pi^2/4-\arccos^2\gamma,\ Q=2F'+\gamma F''\)。元の \(E=\pi^2/4-\langle kF\rangle\) は \(\langle k\rangle=1\) による。

物理視線 \(v=(x-\rho,y,\lambda(\mu-z))\)、単位視線 \(u=v/D\)、法線 \(n=(x,y,\epsilon\mu)/\sqrt B\) に対して \(\gamma=n\cdot u\)。\(kF=\sqrt B D\,\varphi(\gamma),\ \varphi=\gamma F\) を二度微分すると、\(\nabla D=u,\ \nabla\gamma=(n-\gamma u)/D\) より
\[
 \nabla_v^2(kF)=\frac{\sqrt B}{D}\{-\gamma^2F'(I-uu^\mathsf T)+Q(n-\gamma u)(n-\gamma u)^\mathsf T\}.
\]
横の \(y\) 方向を選ぶと、回転対称性から \(E_{yy}^p=E_\rho/\rho=H\)。\(\rho=0\) ではこの Hessian を用いる。従って、\(t_-=-(1+z)/\epsilon,\ t_+=(1-z)/\epsilon\) として
\[
 \lambda H=\tfrac12\int_{t_-}^{t_+}\overline K\,dt,\quad
 K=\frac{\sqrt B}{D}F'\gamma^2(1-y^2/D^2)
       -\frac{m}{D}\sin^2\phi\, Q(1-k/D^2)^2. \tag{1}
\]
内点・固定 \(\epsilon>0\) では求積前に微分できる。接触は §3 の積分トレースで扱う。

使うスカラー不等式は
\[
 K\le 2\sqrt B/D,\quad |K|\le2\pi\sqrt B/D,\quad 0<F'\le\pi,\quad
 10/3\le Q\le2\pi,\quad 0\le2\pi-Q\le6\gamma . \tag{2}
\]
最初の二つは V45 (NP8) の密度の固有値評価である。スカラー側では
\(F'=2\int_0^1(1-h(1-v^2))^{-1}dv,\ h=(1-\gamma)/2\) なので \(F''\le0,\ F'''\ge0,\ F''(0)=-2\)。\(Q(0)=2\pi,\ Q'=3F''+\gamma F'''\ge-6\) と \(F'\le\pi\) を使った。下界は (NP12) の非負係数（定数項 \(10/3\)）からも出る。具体的に \(a_j=\int_0^1(1-v^2)^j\,dv,\ a_{j+1}/a_j=(2j+2)/(2j+3)\) とすると \(Q\) の \(h^j\) 係数は \((4+2j)a_j-(j+1)a_{j+1}>0\)。

M1 の二つの尾を再導出する。固定内点でまず \(\epsilon=0,\mu=z\) と凍結し、その後 \(T=|t|\to\infty\) とすると \(k_0=S^2-\rho S\cos\phi,\ Q=2\pi-6\gamma+O(\gamma^2)\)。よって (1) の初めの二項は \(c/T+d/T^2\) で、
\[
 c=-2\pi S\sin^2\phi,\qquad d=6k_0\sin^2\phi,\qquad
 \bar c=-\pi S,\quad \bar d=3S^2 .
\]
有限 \(\epsilon\) では次式を定義する。
\[
 r=K-\frac{c}{\sqrt{1+t^2}}-\frac d{1+t^2},\qquad
 R_H^{(2)}=\tfrac12\int_{t_-}^{t_+}\bar r\,dt. \tag{3}
\]
二つの尾の積分はそれぞれ \(-\pi S A_\lambda/2,\ 3S^2B_\lambda/2\)。したがって
\[
 \lambda H/S=-T_\lambda+R_H^{(2)}/S,\quad
 T_\lambda=\tfrac{\pi}{2}A_\lambda-\tfrac{3S}{2}B_\lambda,\quad
 A_\lambda=\sum_\pm\operatorname{asinh}(\lambda(1\pm z)),\
 B_\lambda=\sum_\pm\arctan(\lambda(1\pm z)). \tag{4}
\]
(3)–(4) は近似を含まない。

## 3. 接触点と遠方点で破れる点別評価

\(t=\phi=0,\ \rho<S\) では \(D=S-\rho=\delta/(S+\rho)\)、\(\gamma=S/\sqrt B\)、\(K=\sqrt B F'\gamma^2/(S-\rho)\)。また \(z=0,\rho=1/2,\phi=\pi/2,\mu=1/2,\ t=1/(2\epsilon)\) では (1)–(3) から \(t r\to2\pi(1-\sqrt3/2)>0\)。有限 \(\epsilon\) の動く遠方全体に \(|r|\le M/(1+T)^3\) を課すと、内点でも一様な \(M\) は存在しない。

一方、\(\lambda\ge4096,\ S\ge S_0\) なら \(\epsilon\le S\)。角度を \(-\pi\le\phi\le\pi\) とし、\(0<b\le1/4,\ |t|\le bS,\ |\phi|\le b\) の小領域を考える。\(|s^2-S^2|\le2\epsilon |t|\)、\(|\sin\phi|\ge2|\phi|/\pi\) より \(s^2\ge S^2/2,\ \sqrt B\le2S,\ D^2\ge S^2[(t/S)^2+\phi^2/\pi^2]\)。(2) を使い、\((t/S,\phi/\pi)\) の矩形を半径 \(\sqrt2 b\) の円板に含めると
\[
 \frac1{4\pi S}\int_{\rm 小領域}|r|\,dt\,d\phi
 \le 2\sqrt2\,\pi^2 b+6 b^2 . \tag{5}
\]
尾は \(|c|\le2\pi S,\ |d|\le12S^2\) を使った。有界であるだけでなく、右辺は \(\delta\) によらず 0 に向かう。固定した有限 \(\lambda,z\) ではこの外で接触極限の分母は正であり、内側から \(\rho=S\) への積分トレースが得られる。(5) は後の近領域積分に含まれる。

## 4. L1-A の主領域　\(h=\epsilon/S\le1/8\)

反射により \(z\ge0\)。外向き・内向きに \(d_\pm=1\mp z,\ U_\pm=d_\pm/(\epsilon S),\ v=T/S\) と書く。\(U_\pm\ge1/(2h)\ge4\)。以下の寄与はすべて \(R_H^{(2)}/S\) の正規化を含む。

| \(3S\) と 1 の順序 | \(|t|\le1\) | \(|t|>1\) |
|---|---|---|
| \(3S\le1\) | \(T\le3S\) は §4.1、残りは §4.2 | §4.2 |
| \(3S>1\) | §4.1 | \(1<T\le3S\) は §4.1、残りは §4.2 |

### 4.1　\(T\le3S\)

\(D^2\ge t^2+s^2\sin^2\phi\) を (2) に入れる。\(0<u\le1\) に対して \(\operatorname{asinh}(a/u)\le\operatorname{asinh}a-\log u\) であり、\(\overline{-\log|\sin\phi|}=\log2\)。既知の二つの尾を引いた項のこの帯での総和は正確に \(f(S)=\pi\operatorname{asinh}(3S)-3S\arctan(3S)\)。

* \(S\le1/16\)。この帯は \(\mu\ge0\)。外向きは \(s\ge S/2,\sqrt B\le(65/64)S\)、内向きは \(s\ge S,\sqrt B\le(4/3)S\)。実際 \(2\epsilon T\le3S^2/4,\ \epsilon^2\le S^2/64\)。二つの半区間を積分すると上界は
\[
 (65/64)(\operatorname{asinh}6+\log2)
 +(4/3)(\operatorname{asinh}3+\log2)+3\pi/16<15/2. \tag{6}
\]
* \(S\ge1/16\)。\(\lambda\ge4096\) より \(h\le1/256,\ s\ge15S/16,\sqrt B\le17S/16\)。上界は
\[
 (17/8)(\operatorname{asinh}(16/5)+\log2)+f(S)<10 . \tag{7}
\]
実際 \(f''=-27\pi S/(1+9S^2)^{3/2}-18/(1+9S^2)^2<0\)。
\(f(1/2)<7\pi/8\) は \(\operatorname{asinh}(3/2)<5/4,\ \arctan(3/2)>\pi/4\) による。
\(f'(1/2)=6\pi/\sqrt{13}-3\arctan(3/2)-18/13\in(-2,2)\)。接線より \(f(S)<7\pi/8+1<4\)。
共通に \(\log2<7/10,\ \pi<22/7,\ \operatorname{asinh}6<5/2,\ \operatorname{asinh}(16/5)<2\) を使える。

### 4.2　\(T\ge3S\)。角度平均が残す符号

\(0\le T^{-1}-D^{-1}\le A/(2T^3),\ 1-(1-k/D^2)^2\le2k/D^2,\ \sqrt B\,\gamma^2\le k/D,\ m\gamma\le k/D\) である。(1) の負項の主要部を同じ密度内で相殺し、(2) を使うと
\[
 K+2\pi m\sin^2\phi/T
 \le(\pi+6\sin^2\phi)k/T^2+
       2\pi m\sin^2\phi(A/2+2k)/T^3.
\]
\(k_b=1-z\mu\) とする。\(\bar k=k_b,\ \overline{k\sin^2\phi}=k_b/2,\ 
\overline{A\sin^2\phi}=(s^2+\rho^2)/2\) である。\(k_b\le S^2+|w|,\ (s^2+\rho^2)/4\le(S^2+|w|)/2\)。
(3) の \(d\ge0\) と \(1/\sqrt{1+t^2}\le1/T\) を使うと
\[
 \bar r\le\frac{\pi(S-m)}T+\frac{(\pi+3)k_b}{T^2}
              +\frac{3\pi m(S^2+\epsilon T)}{T^3}. \tag{8}
\]
ここで \(k_b=S^2+(s^2-S^2+w^2)/2\) を代入する。最初の二項中の \(S-s\) の係数は
\[
 T^{-1}\big[\pi-(\pi+3)(s+S)/(2T)\big].
\]
\(s/S\le\sqrt{1+2hv}\) であり、\((1+\sqrt{1+2hv})/v\) は \(v\) について減少する。\(v\ge3,\ h\le1/8\) では \((s+S)/T\le(1+\sqrt{7/4})/3<4/5\)。従って括弧は 0 と \(\pi\) の間にあり、
\[
 \bar r\le\frac{\pi(S-s)_+}{T}+\frac{\pi(s-m)}{T}
 +(\pi+3)\big(S^2/T^2+\epsilon^2/2\big)
 +3\pi m(S^2+\epsilon T)/T^3 . \tag{9}
\]
この符号付き係数が、動く方位円のずれを積分できる形にする。

(9) の各項を \(dt/(2S)\) で両側に積分する。

1. \(u=v/U_\pm\) とすると \(s/S=\sqrt{(1-u)(1+(d_\pm/d_\mp)u)}\)。両側で \(\sqrt{1-u}\) 以上、内向きでは \(\sqrt{1-u^2}\) 以上である。\(\int_0^1(1-\sqrt{1-u})\,du/u=2(1-\log2)\)。内向きの対応積分はその半分。よって第一項は \((3\pi/2)(1-\log2)<\pi/2\) である。
2. \(s-m\le\epsilon^2/(2s)\)。上端の \(s=0\) は可積分で、\(\int_3^U dv/[v\sqrt{1-v/U}]=2\operatorname{atanh}\sqrt{1-3/U}\le\log(4U/3)\)。\(U\le2/(hS^2)\) を使い上界は \(\pi h^2\log(8/(3hS^2))/2\)。
3. 第三項は \((\pi+3)(1/3+h/2)\)。定数項では元の \(t\) 区間の全長 \(2/\epsilon\) が効く。
4. \(m\le s\le S\sqrt{1+2hv}\)。第四項は \(3\pi J(h)\) 以下である。
\[
 J(h)\le\int_3^\infty (1+hv)(1+\sqrt{2hv})\,dv/v^3
 =1/18+h/3+\frac{2\sqrt{2h}}{9\sqrt3}
                   +\frac{2h\sqrt{2h}}{\sqrt3}.
\]

これらの和を \(U_f\) とする。\(h^2\log(8/(3hS^2))\) はここでは \(h\) について増加し、\(S\ge2^{-12}\) で最大値を上から押さえられる。次の代入はすべて有理数比較に落ちる。

| 条件 | 対数を含む項 \(h^2\log(8/(3hS^2))\) の上界 | \(\sqrt{2h}\) 上界 | \(U_f\) |
|---|---|---|---|
| \(h\le1/8\) | \(30\log2/64\) | \(1/2\) | \(<7\) |
| \(h\le1/256\) | \(35\log2/256^2\) | \(1/10\) | \(<9/2\) |

ここでは \(1/\sqrt3<3/5\)。(6) と 7、または (7) と \(9/2\) の和により、いずれも \(R_H^{(2)}/S<29/2\) を得る。

## 5. L1-A の残り　\(h>1/8\) で負の帯を取り戻す

ここは \(\epsilon\le S<8\epsilon,\ S<1/512,\ 4096\le\lambda<32768,\ z>15/16\)。接触点から離れた \(-1/2\le\mu\le1/2\) まで捨てると定数を失う。まず \(\lambda H\) の上側に入れる寄与を計算し、次にこの帯の負項を一度だけ差し引く。

| \(T\) | 正規化 \(\tfrac12\int\bar K\,dt\) に入れる上界 | 根拠 |
|---|---|---|
| \(0\le T\le\epsilon/4\) | \(18\epsilon[\operatorname{asinh}(\sqrt2/4)+\log2]\) | \(s^2\ge\epsilon^2/2,\sqrt B\le9\epsilon\)、(2) を角度平均 |
| \(\epsilon/4<T\le1\) | \(18\epsilon\log(4/\epsilon)+4\sqrt{2\epsilon}\) | \(\sqrt B\le9\epsilon+\sqrt{2\epsilon T},\ D\ge T\)、(2) |
| \(T>1\) | \(\pi[64\epsilon^2+\epsilon\log(2/\epsilon)]\) | (1) の正項のみを \(\pi k/T^2\) で押さえ、平均 \(k_b\le S^2+\epsilon T\) を使う |

各半区間を必要なら端点で切り、正の比較関数のみ積分域を広げた。三行の和は \(3/20\) 未満。右辺は \(\epsilon\le1/4096\) で増加し、その上端で \(\operatorname{asinh}(\sqrt2/4)<3/8,\ \log2<7/10,\ \sqrt2<3/2\) を使えばよい。

一方、\(-1/2\le\mu\le1/2\) は \(T>1\) の内部である。この帯では \(D^2/\lambda^2\le9/4+4\epsilon^2<(8/5)^2,\ D^2\ge16,\ k\le2,\ m\ge3/4\)。
\(dt=\lambda d\mu\) に戻し、(1) の負項の絶対寄与の下界を取る。帯の長さ 1、角度平均 \(\overline{\sin^2\phi}=1/2\)、\((1-k/D^2)^2\ge3/4\) より
\[
 \frac14\frac58\frac34\frac{10}3\frac34=\frac{75}{256}>\frac14 .
\]
従って \(\lambda H<3/20-1/4=-1/10\)。ここで初めて (4) を使う。凹関数 \(\operatorname{asinh}\) の Jensen 不等式から \(T_\lambda\le\pi\operatorname{asinh}\lambda\)。ゆえに
\[
 R_H^{(2)}/S< -512/10+\pi\operatorname{asinh}(32768)<0. \tag{10}
\]
\(\operatorname{asinh}(32768)<12\) で十分である。この評価を支えるのは幅 1 の帯の \(75/256\) である。(6)–(10) により、全非極域で \(C=29/2\) を得た。

## 6. L1-B　正確な予算の全半直線での比較

\(d=1\pm z\) とすると (4) そのものを微分して
\[
 \partial_\lambda T_\lambda
 =\tfrac12\sum_d\frac{d}{1+\lambda^2d^2}
       [\pi\sqrt{1+\lambda^2d^2}-3S]>0 . \tag{11}
\]
\(S\le1,\ \pi>3,\ d>0\) なので各項で従う。よって \(L=4096\) を評価すればよい。\(z_x=\sqrt{1-x^2}\) とおく。\(\operatorname{asinh}\) と \(\arctan\) はそれぞれ正半軸で導関数が減少するため \(A_L,B_L\) は \(|z|\) について非増加。\(S\in[a,b]\) の厳密な端点比較は
\[
 T_L(z)\ge(\pi/2)A_L(z_a)-(3b/2)B_L(z_b). \tag{12}
\]
次表はこの有限個の初等関数の比較である。全域を粗い対数予算に置き換える必要はない。各行で \(B_L<\pi\)。

| \(S\) | \(A_L\) に使う引数と厳密な比較 | (12) をさらに下から押さえた値 |
|---|---|---|
| \([S_0,1/16]\) | 大きい引数 \(\ge7680\)、\(\operatorname{asinh}7680>19/2\) | \(149\pi/32\) |
| \([1/16,1/4]\) | 小さい引数 \(\ge LS^2/2\ge8\)、大きい引数 \(\ge4096\)。各値 \(>2,\ >17/2\) | \(39\pi/8\) |
| \([1/4,1]\) | 小さい引数 \(\ge128\)、大きい引数 \(\ge4096\)。各値 \(>5,\ >17/2\) | \(21\pi/4\) |

一例として \(e<11/4,\ (11/4)^{19}<15360^2\) から \(2\sinh(19/2)<15360\)。他の下界も同様で、(10) の逆向き比較は \(e>8/3,\ (8/3)^{12}>65537\) を使う。 \(\pi>25/8\) より最小の \(149\pi/32\) でも \(29/2\) を超える。以上で (4) の \(H<0\) が全 \(\lambda\ge4096\) に従う。

## 7. L2　軸上の視線と法線を符号付き角で組にする

\(D_2=(\mu-z)^2+\epsilon^2s^2,\ k=1-z\mu\) とする。両ベクトルの子午平面内の傾きから
\[
 a(\mu,z)=\arctan\frac{\mu-z}{\epsilon s}-\arctan\frac{\epsilon\mu}{s},
 \qquad E(0,z)=\tfrac12\int_{-1}^1 k a^2\,d\mu . \tag{13}
\]
両ベクトルの水平成分は正で内積も正だから \(\cos a=\gamma,\ |a|=\arccos\gamma\)。従って元の汎関数と同じである。内点、有限 \(\epsilon>0\) で
\[
 a_z=-\epsilon s/D_2,\quad a_\mu=\epsilon k/(sD_2)-\epsilon/(sB),\quad
 k a_z+s^2a_\mu=-\epsilon s/B. \tag{14}
\]
(13) を微分し、(14) の移流恒等式を使うと \(-s^2(a^2)_\mu\) が現れる。\(\mu=\pm1\) で \(s^2a^2\to0\)、\((s^2)_\mu=-2\mu\)。従って
\[
 E_z=\tfrac12\int_{-1}^1[-3\mu a^2-2\epsilon s\,a/B]d\mu . \tag{15}
\]
固定内点では \(D_2,B\) は閉区間上で正、\(1/s\) は可積分。微分と部分積分はまず端点を切ってから極限を取れる。

\(z\ge0,\ 0<\mu<1\) とし、\(b=\arctan(\epsilon\mu/s),\ \theta_\pm=\arctan((\mu\pm z)/(\epsilon s)),\ D_a=\theta_+-\theta_-,\ \Sigma=\theta_++\theta_--2b\)。
(15) の \(\pm\mu\) を組にして二乗の差を因数分解すると
\[
 \frac{E_z}{z}=\frac12\int_0^1
 \frac{D_a}{z}\left(3\mu\Sigma+\frac{2\epsilon s}{B}\right)d\mu,\qquad
 \frac{D_a}{z}=\int_{-1}^1\frac{\epsilon s\,du}{(\mu+uz)^2+\epsilon^2s^2}. \tag{16}
\]
\(z=0\) でも右の商は \(2\epsilon s/(\mu^2+\epsilon^2s^2)\) となる。固定 \(\epsilon>0\) の中心近傍では分母には正の一様下界があり、\(E_{zz}(0,0)\) へ連続に延びる。

\(L_\pm=(\mu\pm z)^2+\epsilon^2s^2\) とする。\(\theta_++\theta_-\in[0,\pi)\)、\(2b\in[0,\pi)\) なので \(\Sigma\in(-\pi,\pi)\)。三角関数の加法定理によって
\[
 \sin\Sigma=\frac{2\epsilon\mu s(S^2-\epsilon^2)}
                   {B\sqrt{L_+}\sqrt{L_-}} . \tag{17}
\]
実際、\(\sin(\theta_++\theta_-)=2\epsilon s\mu/\sqrt{L_+L_-}\)、\(\cos(\theta_++\theta_-)=(\epsilon^2s^2-\mu^2+z^2)/\sqrt{L_+L_-}\)。残る分子は \(s^2-\epsilon^2\mu^2-(\epsilon^2s^2-\mu^2+z^2)=S^2-\epsilon^2\) である。

従って \(S\ge\epsilon\) なら角度和 \(\Sigma\ge0\)。焦点 \(S=\epsilon\) ではこれがゼロになり、(16) の第二項は依然正である。\(\mu\in[0,1/2]\) 上で \(s^2\ge3/4,\ B\le1,\ (\mu+uz)^2+\epsilon^2s^2\le9/4+1/25<5/2\)。この部分だけ残せば \(D_a/z\ge(4/5)\epsilon s\) より
\[
 \frac{E_z(0,z)}{z}\ge \frac{3}{10}\epsilon^2 . \tag{18}
\]
\(S\le\epsilon,\ z>0\) では既存の G1 により \(E_z/z\ge\epsilon/(4z)\ge\epsilon/4\ge3\epsilon^2/10\)。負の \(z\) は反射で従う。これで L2 の十分な閾値は 5 である。

**二つの層。** 動く帯は (16) の正の分母に残る。\(|\mu+uz|\le\epsilon s\) の内外、および \(\mu=0\) を帯が横切るときも同じ分子を使える。極端層 \(1-\mu\le\epsilon^2\) では \(B=\epsilon^2+(1-\epsilon^2)s^2\) と \(s/B\le1/s\) を用いる。固定 \(\epsilon\) で \(D_a\le\pi\)、また \(z=0\) は上の連続式がある。\(S\ge\epsilon\) では端層も移動帯も正の積分であり、重なる部分を含めて符号の見積もりに負の誤差を生じない。\(S<\epsilon\) では (17) の符号が反転するため、この理屈で \(\Sigma\) を捨てることはできず、上記の G1 が必要になる。

**\(\lambda\) によらない正の正規化下界。** \(b_0=S_0^2/8,\ L_b=b_0^{-2}=2^{54}\)。\(\lambda\ge L_b,\ S\ge S_0\) では \(\mu=z+w,\ \epsilon\le w\le b_0\) だけの寄与を取れる。\(1-z\ge S_0^2/2\)、\(s^2\ge S^2-2b_0\ge S_0^2/4\)。\(b\le2\epsilon/S_0<\pi/8,\ \theta_\pm\ge\pi/4\) より \(\Sigma\ge\pi/4\)。また
\[
 D_a/z\ge\sin(D_a)/z=2\epsilon s/\sqrt{L_+L_-}
       \ge \epsilon s/[w(\mu+z)] .
\]
最後は両引数 \(\mu+z,\ w\ge\epsilon s\) による。中心は極限で解釈する。\(\mu/(\mu+z)\ge1/2\) なので (16) の下界は \((3\pi S_0/32)\epsilon\log(b_0\lambda)\)。
\(\log(b_0\lambda)\ge(\log\lambda)/2\ge(1+\log\lambda)/4\)。\(5\le\lambda\le L_b\) には (18) を使う。全域で
\[
 \frac{\lambda E_z}{z(1+\log\lambda)}\ge
 \min\left\{\frac{3\pi S_0}{128},\
       \frac3{10L_b(1+\log L_b)}\right\}>0. \tag{19}
\]
この小さい定数は全域正値の補足であり、L2 の閾値は (18) と G1 から決まる。

## 8. 極側を縦微分へ割り当てる方法との比較

\(w_p=\lambda S,\ u_p=\rho/S,\ z=\sqrt{1-\epsilon^2 w_p^2}\) とする。既存 G1 は \(w_p\le1\) 全体を覆う。ここでは既存の北端補正を含めて誤差を評価し、監査済みの有限な余裕の範囲でだけ \(K>1\) を与える。

V43 §3 の G9 の右辺を \(\mathcal B(w_p)\) とする。\(\theta\in[\arccos(3/4),\pi-1/64],\ \phi\in[0,\pi],\ d^2=(z-\mu)^2+\epsilon^2A,\ T_0=s/\sqrt B,\ f_1=\mu k,\ f_2=\mu k+k^2(z-\mu)/d^2\) として
\[
 \mathcal B=\int\frac{T_0}{d}
 [\pi(f_1+f_2)-\gamma((f_1)_++2(f_2)_+)]
 \frac{d\theta\,d\phi}{2\pi}
 -\frac\pi{64z}-\frac{\epsilon w_p^2\sqrt{1+w_p^2}}{1+z}. \tag{20}
\]
\(1\le w_p\le5/4,\ 0<\epsilon\le1/5,\ 0\le u_p\le1\) で \(z\ge19/20>3/4,\ k\in[0,2]\)。G9 を導いた三つの比較の仮定は満たされる。すなわち \(\mu\in[3/4,z]\) の両項は非負、\(\mu>z\) の絶対損は G6 に \(X=w_p^2\) を代入した値、南端では方位角平均後の \((1-z\mu)/(z-\mu)\le1/z\) が効く。従って \(\lambda E_z\ge\mathcal B\)。

固定 \(\epsilon,u_p\) でプライムを \(w_p\) 微分とする。\(d\ge1/5,\ |z'|=\epsilon^2 w_p/z<1/16,\ |\rho'|\le1/5,\ |k'|\le1\)。\(d\) は長さなので \(|d'|\le |z'|+\epsilon|\rho'|<1/8\)。\(\epsilon/\sqrt B\le1,\ 0\le\gamma\le1\) より \(|\gamma'|\le5+5/8<6\)。\(g=(z-\mu)/d^2\) は \(0\le g\le5,\ |g'|\le25(1/16+2/8)<8\)。順に
\[
 |f_1|\le2,\ |f_2|\le22,\quad |f_1'|\le1,\ |f_2'|\le53 .
\]
角括弧の絶対値は 142 未満、Lipschitz 定数は 600 未満（正部は 1-Lipschitz）。\(T_0\le1,\ \mathrm{Lip}(1/d)<4\) より積分密度の Lipschitz 定数は \(4\cdot142+5\cdot600<3600\)。正規化積分領域の測度は 2 未満。南端補正の定数は 1 未満、北端補正は 10 未満である。後者は \(w_p\le5/4,\ \sqrt{1+w_p^2}<2,\ 1+z\ge1,\ |z'|<1/16\) を (20) 最終項に直接代入して得る。従って全体で \(\mathrm{Lip}(\mathcal B)<8192\)。

監査済み G10 の下端 \(47473218194072764542240096942353646083/2^{127}>17/64\) は \(w_p=1\) を含む。したがって \(1\le w_p\le1+2^{-19}\) では損が \(8192\cdot2^{-19}=1/64\) 以下。**\(K=1+2^{-19}\)** まで \(\lambda E_z>1/4\) というごく短い延長を得る。大きな \(K\) では北端補正の成長と正の積分量の評価が必要である。

| 方法 | 接触カラーで使うもの | 得られた範囲・次の課題 |
|---|---|---|
| H の直接法 | (5) の一様可積分性と (9) の角度平均、極寄りは §5 の負の帯 | 全非極域で \(C=29/2,\ \Lambda_1^{(L1)}=4096\)。§4.1 の正の近接寄与と §4.2 で捨てた負項の差を同じ方位平均で残すことが次の課題 |
| G1 併用 | \(w_p\le K\) の接触は G6 の上界で吸収 | \(\lambda\ge5\) から該当する隅を外せる。今回の \(K\) だけでは全域の閾値改善は出ない。より大きな \(K\) の下界と、その外側の H 上界が必要 |

小さな \(\lambda\) まで停留点排除を運ぶ場合、極寄りの接触カラーの割当ては後者が簡単である。直接法は H 自体の上界を与える。現時点で数付きの全域閾値を与えるのは直接法である。

## 9. 組立、費用、監査箇所

\(z>0\) とその反射について、\(S\le S_0\) は G21。\(S\ge S_0,\rho>0\) は §4–6 により \(E_\rho=\rho H<0\)。残る軸の \(z\ne0\) は §7。中心は反射と回転対称で停留点であり、既存の中心横 Hessian の負値と (18) により鞍点である。従って **全体の十分な閾値は \(\max(4096,5)=4096\)**。有限性に未監査の Cauchy 定数 A1 を仮定する箇所はない。

| 全域の候補 | \([5,\Lambda_1]\) に旧 C21 をそのまま使う日数（依頼書の幅 1 あたり 16 日） | この報告が与える根拠 |
|---|---:|---|
| 5 | 0 日 | 軸のみ達成。全非極での L1 は未解決 |
| 10 | 80 日 | L1 の目標。依頼書のこの付近の閾値・残差は標本情報 |
| 4096 | 65,456 日、約 179 年 | L1 と L2 の解析的な十分条件。日数は一定速度を仮定した外挿 |

**Judge への提案。** 先に (16)–(18) の独立導出を依頼する。L1 の監査は (8)→(9) の符号、(6)–(7) の正規化、§5 の帯の \(75/256\)、最後に (11)–(12) の順がよい。有限閾値を研究成果として先に記録する選択と、実用窓への接続まで採用を保留する選択がある。前者を推奨する。広域の旧 C21 を発注するよりも、まず \(5\le\lambda\le10\) で使える符号付き近領域上界を研究する方が、この費用差に即している。今回の標本検算は別紙に置く。最終採用は chat の独立監査と Judge の裁定による。

**出典と再利用範囲。** すべて cotaxxxx/bg-spheroid-family。完全なファイルパスと Git/SHA-256 の対照は同梱の SOURCE_PINS.json にある。

| 資料と固定コミット | 再利用箇所 |
|---|---|
| Dig M1、b5f4353717a62bbd0dfcbf792f7b9f25238dbf9f、MATH_DERIVATION_BEFORE_PROBE §§1,2,5、MATH_ADDENDUM_POST_PROBE §§1–2 | 元の規約、(1)、二項の (3)–(4)。本稿で再導出 |
| M2、91d486bb9e18b13c691782f7f4096f7fd7ad1d38、M2_AXIS_DIFFERENCE / KERNEL_DERIVATIVE / TWO_SCALES、M2_TAIL_* | 既存の反射差商と二層の課題 |
| M3、dde63e5aa5d1750073ff975c002d21a0015bdd2f、M3_AUDIT_CORRECTION_EXACT_MARGIN、M3_V47_EXACT_BUDGET | 正確な予算 (4) |
| V43、cf541c0e429cce27670654832bbc7fbd532fb547、ASTRA_D_PRO_LAMBDA0_GAP_REPORT §§3.1–3.4, 4、同監査の G1/G21 | 極領域の補題と (20) の出発点。G21 の依存関係の訂正は V45 |
| V45、fbe6e36c7c2ee77f3350639c3710453d35d741e0、CHAT_AUDIT_D_PRO_NONPOLAR_ASTRA_V45 の「手で導き直したもの」および追補 | NP4–NP12、中心 \(H(0)<0\) |
| V46、25f46a8cd209b44e2651cc35d9c6d014a4068904、CHAT_AUDIT_D_PRO_TAIL_AXIS_DIG_V46、V47、ed0d258d33992b5880b5ce4996248f42fce2e579、CHAT_AUDIT_D_PRO_M2_DIG_V47 | 既存の二項恒等式・差商と未解決部分の境界 |

新しい部分は (5)–(12) の一様定数・単調比較、(13)–(19) の子午角による軸補題、(20) 直後の定量的延長である。特に \(\Lambda_1\le10\) の全域帰結は OPEN。
