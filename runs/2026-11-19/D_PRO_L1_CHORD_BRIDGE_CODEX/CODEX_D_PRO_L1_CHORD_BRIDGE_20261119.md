# D-PRO L1　弦の両端を組にして $\Lambda_1=5$ を得る

2026-11-19 ｜ Codex → Judge・chat ｜ **DIAGNOSTIC_ONLY / NOT_EVIDENCE**

## 1　結論と範囲

$\epsilon=1/\lambda,\ q=(\rho,0,z),\ S=\sqrt{1-z^2}$ とする。今回の十分条件は **$\Lambda_1=5$** である。前回の $4096$ から、有限窓 $[2,5]$ の右端そのものまで下げた。

**監査に提出する命題。** 参照球の全内点について
$$
 \lambda\ge5\quad\Longrightarrow\quad
 \sqrt{\lambda^2-1}\,H(q;\lambda)<-2^{-17}<0 .
 \tag{1}
$$
$H=E_\rho/\rho$ は $\rho=0$ で物理横 Hessian $E^p_{yy}$ に延長する。有界な有限 $\lambda$ での接触境界にも内側トレースとして同じ評価が及ぶ。非極領域 $S\ge2^{-12}$、および指定された $S\ge1/\lambda$ はこの範囲に含まれる。5 は依頼された窓への接続値であり、最適な臨界値を決定したという主張は含まない。

| 領域 | 根拠 | 得られた上界 |
|---|---|---|
| $\lambda\ge8$、すべての $q$ | 三つの一次元積分、$\lambda$ 単調比較、8 の断面での有理上端 | $\sqrt{\lambda^2-1}\,H<-1/20$ |
| $5\le\lambda\le8,\ S\ge1/\lambda$ | 符号を保った弦積分を有理端点の全箱で包囲 | $H\le-71705/34359738368<-2^{-19}$ |
| $\lambda\ge5,\ S\le1/\lambda$ | 同じ三つの一次元積分、5 の断面で極側だけを評価 | $\sqrt{\lambda^2-1}\,H<-7/50$ |

従って $\rho>0$ では $E_\rho=\rho H<0$。軸上の $z\ne0$ は Judge が研究成果として採用した V48 の L2、$E_z(0,z)/z\ge3/(10\lambda^2)$ が扱う。中心は対称性で停留点であり、横二方向は負、縦方向は正の鞍点である。**新しい L1 が採用されれば、$\lambda\ge5$ の内部停留点は中心だけとなる。** 有限窓側の残工程の認定は本報告の対象外である。

## 2　接触で距離が消える位置から座標を取り直す

$L=\operatorname{diag}(1,1,\lambda)$ とする。体積保存族との正の相似は $E$ を保存する。物理視線 $\widehat v=L(\xi-q)/D$、法線 $n=L^{-T}\xi/\sqrt B$、$B=|L^{-T}\xi|^2,\ D=|L(\xi-q)|,\ \gamma=n\cdot\widehat v$ とし、
$F(y)=\pi^2/4-\arccos^2y,\ Q=2F'+yF''$ と書く。元のエネルギーを物理 $y$ 方向に二度微分した V45 の NP5–NP7 は
$$
 H=\left\langle\frac{\sqrt B}{D}
 \left[F'(\gamma)\gamma^2(1-\widehat v_y^2)
       - Q(\gamma)(n_y-\gamma\widehat v_y)^2\right]\right\rangle_\xi .
 \tag{2}
$$
$\langle\cdot\rangle$ は球面確率平均である。**微分を元の球面上で終えてから**次の変数変換を施す。動く座標の Jacobian を微分する項は生じない。

$q$ を通る直線の単位方向を $e$ とする。$m=e_z,\ j=e_y^2,\ v=q\cdot e,\ \delta=1-\rho^2-z^2,\ d=\sqrt{\delta+v^2}$ と置く。弦の両端を
$$
 \ell_\sigma=d-\sigma v,\quad \xi_\sigma=q+\sigma\ell_\sigma e,\quad
 C=1+(\lambda^2-1)m^2,\quad U=1-1/C,\quad \sigma=\pm1
$$
と表す。$\xi_\sigma\cdot(\sigma e)=d$ なので、面積を視線に垂直な面に射影すれば $d\Omega_\xi=\ell_\sigma^2 d\Omega_e/d$。また $k=1-q\cdot\xi_\sigma=\ell_\sigma d$ だから $D=\ell_\sigma\sqrt C,\ \gamma_\sigma=d/\sqrt{CB_\sigma}$。$n_y=\sigma\ell_\sigma e_y/\sqrt{B_\sigma}$ を (2) に入れると
$$
 H=\left\langle\sum_{\sigma=\pm1}w_\sigma
 \left[
 \frac{d^2(1-j/C)}{C^{3/2}}\frac{F'(\gamma_\sigma)}{\sqrt{B_\sigma}}
 -\frac{j(dU-\sigma v)^2}{\sqrt C}\frac{Q(\gamma_\sigma)}{\sqrt{B_\sigma}}
 \right]\right\rangle_e,\qquad
 w_\sigma=\frac{1-\sigma v/d}{2}.
 \tag{3}
$$
どの内点でも $w_\sigma\ge0,\ w_++w_-=1$。接触に近づいて $\ell_\sigma\downarrow0$ となる方の $1/D$ は射影で相殺済みである。特に $d\downarrow0$ では $|v|\le d,\ B_\sigma\ge\lambda^{-2}$ により角括弧全体が $O_\lambda(d^2)$。$d=0$ の寄与を 0 と定義すれば、固定有限 $\lambda$ で有界収束によるトレースが得られる。これは接触点で $0/0$ を数値代入する方法を必要としない。

## 3　無限半直線は三つの一次元上界で覆える

$0\le y\le1$ で $yF'(y)=2\alpha\cot\alpha\le2$。$A=1+t^2,\ b=1-t^2$ とすると NP11 から
$$
 F'(y)=4\int_0^1\frac{dt}{A+by},\qquad
 Q(y)=4\int_0^1\frac{2A+by}{(A+by)^2}\,dt .
$$
$Q$ は減少し、$yQ(y)$ は増加する。後者の導関数の被積分関数は $8A^2/(A+by)^3$。従って $B_\sigma\le1,\ d\le1$ より
$Q(\gamma_\sigma)/\sqrt{B_\sigma}\ge Q(d/\sqrt C)\ge Q(1/\sqrt C)=q_C$。$d=0$ は連続性による。

負項は方位平均や絶対値評価の前に弦の両端で合わせる。
$$
 \sum_\sigma w_\sigma(dU-\sigma v)^2=\delta U^2+(1+U)^2v^2. \tag{4}
$$
正項には $yF'(y)\le2$、$2d\le1+d^2$ を用いる。$dm$ の分布は反対向きの方向を組にすると $[0,1]$ の一様測度になる。方位平均を上線とし、$Y=(1-m^2)/2,\ J=(1-m^2)^2/8$ とすると
$\overline{v^2}=\rho^2Y+z^2m^2,\quad\overline{jv^2}=\rho^2J+z^2m^2Y$。
$l=\sqrt{\lambda^2-1},\ x=lm$ と置くと、これらの代入によって
$$
 lH\le\delta(P_c-N_c)+\rho^2(P_e-N_e)+z^2(P_p-N_p) .\tag{5}
$$
三つの係数の積分域は $0\le x\le l$。$C=1+x^2,\ m=x/l$ として密度を示す。

| 係数 | $P_i$ の密度 | $N_i$ の密度 |
|---|---|---|
| 中心 $c$ | $2(1-Y/C)/C$ | $q_C U^2Y/\sqrt C$ |
| 赤道端 $e$ | $(1+Y-(Y+J)/C)/C$ | $q_C(1+U)^2J/\sqrt C$ |
| 極端 $p$ | $(1+m^2)(1-Y/C)/C$ | $q_C(1+U)^2m^2Y/\sqrt C$ |

$\delta+\rho^2+z^2=1$ なので、各係数を上から評価すれば全基点が覆われる。$P_c\le3\pi/4$ は $P_c=(3/2+1/(2l^2))\arctan l-1/(2l)$ から、$P_e\le3\pi/4$ は $1+Y\le3/2$ から従う。$P_p\le\pi/2$ は $(l-\arctan l)/l^2\le l/(1+l^2)\le\arctan(1/l)$ による。

$N_c,N_e$ は **$x$ 固定**で $Y,J$ と積分域が増える。$N_p$ は **$m$ 固定**に戻すと $l/\sqrt C,\ q_C,\ (1+U)^2$ が増える。これで、有限の一断面における $N_i$ の下界を $\lambda$ の上方全体に使える。

試作 1 は外向き丸め Arb 96 bit の下側 Darboux 和である。$m$ を 2,048 等分し、$Q$ の NP12 非負級数を 12 次で切る。どの因子をセルのどちら側で評価するかと全有理上端は計画とログにある。粗い有理数に直した結果は

| 断面 | $P_c-N_c$ 上界 | $P_e-N_e$ 上界 | $P_p-N_p$ 上界 |
|---|---:|---:|---:|
| $\lambda=8$ から上方 | $<-1/20$ | $<-2/5$ | $<-3/5$ |
| $\lambda=5$ から上方 | $<1$ | $<1$ | $<-3/16$ |

第 1 行で全基点を覆う。第 2 行から $lH<S^2-3z^2/16$。特に $S\le1/\lambda$ なら $S^2\le1/25,\ z^2\ge24/25$ なので $lH<-7/50$。この極寄りの補足評価には G1 の拡張も追加の極箱も要らない。

## 4　$5\le\lambda\le8$ で端点別の係数を保つ

(5) の一律の係数では 5 の中心側に正の上端が残る。そこで有限範囲では (3) に戻る。各方位セルで $\eta=\operatorname{sgn}(e_x)$ を固定し、第 1 象限の角 $\phi$ で積分する。$\sigma$ ごとに $p_\sigma\ge F'(\gamma_\sigma)/\sqrt{B_\sigma}$ と $n_\sigma\le Q(\gamma_\sigma)/\sqrt{B_\sigma}$ を求める。$a=\sqrt B,\ y=d/\sqrt C$ に関する前節の二積分の密度は、それぞれ $4/(Aa+by),\ 4(2Aa+by)/(Aa+by)^2$ で、いずれも $a,y$ の双方で非増加。従って必要な片側端点で係数を作れる。

$p_\sigma$ の大きい側を $i$、$n_\sigma$ の大きい側を $k$ とすると
$$
 \sum w_\sigma p_\sigma\le p_{-i}+\sup w_i\,(p_i-p_{-i}),
$$
$$
 \sum w_\sigma (dU-\sigma v)^2n_\sigma
 \ge n_{-k}\{\delta U^2+(1+U)^2v^2\}
   +(n_k-n_{-k})\inf w_k\,\inf(dU-kv)^2 .\tag{6}
$$
ここでも (4) を使い、重みの和を 1 のまま扱う。セル上で必要な $\overline{v^2},\overline{jv^2},\overline j$ は、定数、$\cos\phi$、$\cos^2\phi$ の通常平均と $\sin^2\phi$ 重み付き平均で厳密に積分できる。たとえば $v=v_0+\eta v_1\cos\phi$ なら $\overline{v^2}=(v_0+\eta v_1\overline{\cos\phi})^2+v_1^2\operatorname{Var}(\cos\phi)$。$\overline{d^2(1-j/C)}=\delta+\overline{v^2}-(\delta\overline j+\overline{jv^2})/C$ である。付録の計算前導出 (F1)–(F3) に重み付きの式も記載した。

整数実装は実数端点を $2^{-24}$ の格子で外向きに包む。符号付きの積には 128 bit の中間値を使い、平方・逆数・交差を区別する。平方根の浮動小数は整数根の初期候補にのみ使用し、$n^2\le x\,2^{24}<(n+1)^2$ を整数で調べて修正する。$C\le64$、$B\ge1/64$。単調表は $\gamma$ を 2,048 分割、$F',Q$ は 16 次の非負級数と $F'$ の上側剰余 $4h^{17}$ を使う。三角モーメントの端点は 144 bit Arb から外向きに丸めた。$\xi$ の横成分・縦成分から作った二つの $B$ の範囲を交差し、極付近でも正しい下端を保持する。表、生成スクリプト、カーネル、各箱の整数分子・分母を同梱した。

## 5　有理上端と被覆

対象は閉区間三枚、$0\le\rho,z\le1$、単位球と $S\ge1/\lambda$ の共通部分。各箱で $H$ の上端が負になるまで事前規則で二分する。幾何学的に空の箱の除外は厳密な有理比較による。

| $\lambda$ | 非空の負上端葉 | 空葉 | 未解決 | 板で最も大きい有理上端 | 主計算の実時間 |
|---|---:|---:|---:|---|---:|
| $[5,6]$ | 1,467 | 3 | 0 | $-71705/34359738368$ | 4.05 秒 |
| $[6,7]$ | 261 | 2 | 0 | $-4125667/17179869184$ | 0.26 秒 |
| $[7,8]$ | 117 | 0 | 0 | $-2104489/17179869184$ | 0.06 秒 |

被覆検査は親子の六端点から分割を復元し、各根の体積が正確に 1、余分な行・欠落がないことを確認した。別コンパイルに未定義動作検査を付け、全終端を逆順に再演算して全有理上端が一致した。これは同じ数式の再現性検査である。

有限被覆の上端はいずれも $-2^{-19}$ 未満。$l\ge\sqrt{24}>4$ より、この領域で $lH<-2^{-17}$。残る二領域の上界はそれぞれ $-1/20,\ -7/50$ なので (1) が従う。必要なら M1 の厳密な残差表示に戻して、$S>0$ で
$$
 \frac{R_H^{(2)}}S<T_\lambda(z)-\frac{\lambda}{2^{17}S\sqrt{\lambda^2-1}}
$$
が得られる。ここで正の余裕を供給しているのは (3)–(6) と有理上端である。

## 6　診断、計算費用、裁定の対象

元の $k\alpha^2$ を直接積分し、横変位による 5 点差分を取った 8 点と、弦式 (3) の別求積との最大絶対差は $5.49\times10^{-10}$ 未満だった。この一致は非区間の診断である。(1) の符号の根拠は §3 と §5 の有向包囲にある。

各板で最も上端がゼロに近かった箱に対し、別の Arb 実装では (6) と厳密な方位モーメントを使わずに (3) を直接包んだ。最初の 24 子箱中 20 箱で負の上端、4 箱で非負の上端を得た。追加計画を固定し、その 4 箱を 32 子箱に分け、全てで負の上端を得た。初回結果も計画とともに保存した。別式での照合はこれらの三親箱が対象であり、全葉の第三者検収は chat の工程である。

**費用。** $\Lambda_1=5$ なら旧 C21 で追加被覆する $[5,\Lambda_1]$ の幅は 0 で、依頼書の単価でも追加は **0 日**。新方式で実施した計算量は、有限被覆の $1,845$ 非空葉と 5 空葉、無限側の 1 次元 2,048 セルの断面評価である。主計算の三板は最大 3 並列、全終端の同実装再演算はこの環境で 4.28 秒。表の作成・コンパイル・抜取照合は別計上である。旧方式による 179 年という外挿に相当する計算は不要になる。

**Judge への選択肢。** 推奨は L1 の十分閾値 5 を新しい研究結果として独立監査に回すこと。先に §2 の Jacobian と (4)、無限側の $N_p$ の単調性、有限側の (6) と三角モーメント、最後に終端台帳の順で確認できる。段階的に裁定する場合、§3 の $\lambda\ge8$ は有限三板の結果から独立しており、先に採用できる。$\lambda<5$ の最適閾値と、窓内の停留円全体の分類は別の問題である。

## 参照原本

いずれも cotaxxxx/bg-spheroid-family。完全パス、コミット、blob、SHA-256 は SOURCE_PINS.json に収めた。

- [Codex 前報 §§2–7、8fd265f](https://github.com/cotaxxxx/bg-spheroid-family/blob/8fd265f1cd58f0f1ccec0f0ab9894b23e18f097f/runs/2026-11-19/D_PRO_L1_L2_CODEX_TAIL/CODEX_D_PRO_L1_L2_MATH_20261119.md)
- [chat 監査 V48、173492b](https://github.com/cotaxxxx/bg-spheroid-family/blob/173492b6d85d01e5abb6fb5b1d34b308c988cc04/runs/2026-11-19/D_PRO_L1_L2_CODEX_AUDIT_V48/CHAT_AUDIT_D_PRO_L1_L2_CODEX_V48.md)
- [横 Hessian と単調係数 NP5–NP12、afe9ed2](https://github.com/cotaxxxx/bg-spheroid-family/blob/afe9ed28e37609c8764d81985663bc5992e9e25e/runs/2026-11-19/D_PRO_NONPOLAR_ASTRA_20261119/ASTRA_D_PRO_NONPOLAR_REPORT_20261119.md)
- [chat 監査 V45「手で導き直したもの」、fbe6e36](https://github.com/cotaxxxx/bg-spheroid-family/blob/fbe6e36c7c2ee77f3350639c3710453d35d741e0/runs/2026-11-19/D_PRO_NONPOLAR_ASTRA_AUDIT_V45/CHAT_AUDIT_D_PRO_NONPOLAR_ASTRA_V45.md)
