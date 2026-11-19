# 弦の両端を合わせた非極 L1 の導出（計算前）

2026-11-19 ｜ **DIAGNOSTIC_ONLY / NOT_EVIDENCE**

参照球の \(q=(\rho,0,z)\)、\(\delta=1-\rho^2-z^2\)、\(L=\operatorname{diag}(1,1,\lambda)\)。V48 が照合した横 Hessian の球面密度 (V45 NP5/7) を
\[
 (\sqrt B/D)\{F'(\gamma)\gamma^2(1-\widehat v_y^2)
            -Q(\gamma)(n_y-\gamma\widehat v_y)^2\}
\]
と書く。\(F=\pi^2/4-\arccos^2\gamma,\ Q=2F'+\gamma F''\)、\(\widehat v=L(\xi-q)/D,\ n=L^{-T}\xi/\sqrt B,\ B=|L^{-T}\xi|^2\)。
面平均が \(H=E_\rho/\rho\) であり、中心と軸では \(E_{yy}\) に延長する。

## 1. 視線を基点で固定する

参照球の単位方向を \(e\) とし、\(m=e_z,\ j=e_y^2,\ v=q\cdot e,\ d=(\delta+v^2)^{1/2},\ \ell_\sigma=d-\sigma v,\ \xi_\sigma=q+\sigma\ell_\sigma e\) (\(\sigma=\pm1\))。両端で \(C=|Le|^2=1+(\lambda^2-1)m^2,\ U=1-C^{-1}\)。\(\xi_\sigma\cdot(\sigma e)=d\) であり、立体角の射影恒等式により \(d\Omega_{\xi_\sigma}=(\ell_\sigma^2/d)d\Omega_e\)。また \(k=\ell_\sigma d,\ D=\ell_\sigma\sqrt C,\ \gamma_\sigma=d/\sqrt{CB_\sigma}\)。従って \(H\) は、以下の二つの値の平均を球面上で積分したもの（確率測度）である。
\[
 K_\sigma=\frac{1-\sigma v/d}{\sqrt C\sqrt{B_\sigma}}
  \left[\frac{F'(\gamma_\sigma)d^2}{C}(1-j/C)
       -Q(\gamma_\sigma) j(dU-\sigma v)^2\right]. \tag{C1}
\]
元の \(1/D\) 特異性は射影で消える。\(|v|\le d,\ \ell_\sigma\le2d,\ B_\sigma\ge\lambda^{-2}\)。固定した有限 \(\lambda\) では括弧は \(O_\lambda(d^2)\)、前の相対重みは 0 と 2 の間にあり、\(d=0\) では全体を 0 に延長する。接触で \(\delta=0\) としても、内側トレースは有界収束で (C1) のままである。分母に境界距離の下界を取らない。偶対称により \(0\le m\le1,\ z\ge0\) に制限できる。\(m\) の測度は \(dm\)、方位は確率平均。

## 2. 符号付き積分を三つの一次元上界へ帰着する

\(y\in[0,1]\) で \(yF'(y)\le2\)（\(y=\cos\alpha\) なら \(2\alpha\cot\alpha\)）。また \(Q(y)\) は減少し、\(yQ(y)\) は増加する。後者の二つには \(A=1+t^2,\ b=1-t^2\) として
\[
 F'(y)=4\int_0^1\frac{dt}{A+by},\qquad
 Q(y)=4\int_0^1\frac{2A+by}{(A+by)^2}\,dt
\]
を用いる。\(Q\) の各被積分関数は減少し、\(yQ\) の導関数の被積分関数は \(8A^2/(A+by)^3\)。
\(B_\sigma\le1,\ d\le1\) から
\[
 \frac{Q(\gamma_\sigma)}{\sqrt{B_\sigma}}
 \ge Q(d/\sqrt C)\ge Q(1/\sqrt C)=:q_C.
\]
(C1) の重みは非負。正項の係数は \(F'\gamma_\sigma d/\sqrt C\le 2d/\sqrt C\)。二つの重みの平均は 1、負項の平方の重み付き平均は厳密に
\[
 \tfrac12\sum_\sigma(1-\sigma v/d)(dU-\sigma v)^2
       =\delta U^2+(1+U)^2v^2 . \tag{C2}
\]
正項に \(2d\le1+d^2\) を使う。 \(\overline{\cdot}\) を方位平均として
\[
 H\le\int_0^1
 \left\{\frac{(1+\delta)(1-Y/C)+\bar v^2-\overline{jv^2}/C}{C}
  -\frac{q_C}{\sqrt C}[\delta U^2Y+(1+U)^2\overline{jv^2}]\right\}dm . \tag{C3}
\]
ここで \(\bar v^2\) は \(\overline{v^2}\) の略、\(Y=(1-m^2)/2,\ J=(1-m^2)^2/8,\ \overline{v^2}=\rho^2Y+z^2m^2,\ \overline{jv^2}=\rho^2J+z^2m^2Y\)。右辺は \((\delta,\rho^2,z^2)\) の重心結合である。三つの係数の上界がすべて負なら、全ての基点、接触を含めて \(H<0\)。

## 3. 無限範囲を一つの断面で処理する

\(l=\sqrt{\lambda^2-1},\ x=lm\)。各頂点の (C3) の \(l\) 倍を \(P_i-N_i\) と書く。\(C=1+x^2\)。正と負の被積分関数（測度 \(dx\)）は次の通り。

| \(i\) | 正 | 負 |
|---|---|---|
| 中心 \(c\) | \(2(1-Y/C)/C\) | \(q_C U^2 Y/\sqrt C\) |
| 赤道端 \(e\) | \((1+Y-(Y+J)/C)/C\) | \(q_C(1+U)^2J/\sqrt C\) |
| 極端 \(p\) | \((1+m^2)(1-Y/C)/C\) | \(q_C(1+U)^2m^2Y/\sqrt C\) |

\(N_c,N_e\) は \(x\) 固定で \(Y,J\) が \(l\) について増加し、積分域も拡大するので増加する。\(N_p\) は \(m\) 固定に戻すと \(l/\sqrt C,\ q_C,\ (1+U)^2\) が全て増加するので増加する。全 \(l>0\) に
\[
 P_c\le3\pi/4,\quad P_e\le3\pi/4,\quad P_p\le\pi/2 . \tag{C4}
\]
最初は \(P_c=(3/2+1/(2l^2))\arctan l-1/(2l)\)、次は \(1+Y\le3/2\) による。最後は \(\int_0^l(1+x^2/l^2)/(1+x^2)dx=\arctan l+(l-\arctan l)/l^2\le\pi/2\)。実際 \(l-\arctan l\le l^3/(1+l^2)\le l^2\arctan(1/l)\)。

有限の \(L>1\) でこの三つの \(P_i\) 上界が \(N_i(L)\) より小さければ、全 \(\lambda\ge L\) で所要の符号が出る。\(N_i\) の下界には NP12 の非負級数を使える。\(a_0=1,\ a_{n+1}=a_n(2n+2)/(2n+3),\ h=(1-y)/2\) とすると
\(Q(y)\ge\sum_{n=0}^{M}[(4+2n)a_n-(n+1)a_{n+1}]h^n\)。
以上は試作実行前の解析である。
