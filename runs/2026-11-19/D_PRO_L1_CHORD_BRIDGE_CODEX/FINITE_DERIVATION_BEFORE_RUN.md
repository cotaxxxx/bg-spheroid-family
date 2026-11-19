# 有限区間 [5,8] の符号付き弦積分の上側包囲（試作前）

**DIAGNOSTIC_ONLY / NOT_EVIDENCE** ｜ 2026-11-19

弦座標、\(d,v,m,j,U,C,\ell_\sigma\) と \(K_\sigma\) は計算前導出 (C1)。\(S\ge1/\lambda\) を必要域とする。有限区間を処理するにあたって、次のセル上界を用いる。有限範囲での符号を前提としない。

方向は北半球 \(0\le m\le1\)。方位を第 1 象限の \(\phi\in[0,\pi/2]\) と \(e_x=\eta\sqrt{1-m^2}\cos\phi,\ \eta=\pm1\) に分ける。\(e_y\) の符号は積分に影響しない。よって \(dm\) の等分点と \(\phi\) の等角セル、二つの \(\eta\) の単純平均である。半端な接触パッチを除く操作は要らない。

正の重みを \(w_\sigma=(1-\sigma v/d)/2\) と置く。\(d=0\) ではセル計算上 \(w_\sigma\in[0,1]\) と置ける。(C1) は次の正負の和である。
\[
 C^{-3/2}d^2(1-j/C)\sum_\sigma w_\sigma F'(\gamma_\sigma)/\sqrt{B_\sigma}
 -
 C^{-1/2}j\sum_\sigma w_\sigma (dU-\sigma v)^2 Q(\gamma_\sigma)/\sqrt{B_\sigma}. \tag{F1}
\]
\(t\in[0,1]\) に対する \(A=1+t^2,\ b=1-t^2\) を使うと、\(a=\sqrt B,\ y=d/\sqrt C\) に関して二つの係数は
\[
 4\int_0^1\frac{dt}{Aa+by},\qquad
 4\int_0^1\frac{2Aa+by}{(Aa+by)^2}\,dt .
\]
どちらも \(a,y\) のそれぞれについて非増加である。第 2 式の \(Aa\) に関する導関数は \(-2Aa/(Aa+by)^3\)、\(by\) については \(-(3Aa+by)/(Aa+by)^3\)。従って \(F'/\sqrt B\) の上界 \(p_\sigma\) は両変数の下端で、\(Q/\sqrt B\) の下界 \(n_\sigma\) は上端で評価できる。正項の上界側で \(y/a>1\) となる場合は 1 への切り下げが上界を広げる。負項の下界側では実点で \(y\le a\le a_{\rm hi}\) なので \(y_{\rm hi}\) を \(a_{\rm hi}\) で切れる。各 \(\gamma\) の単調包囲には前稿 §2 と NP12 の非負級数を使う。

\(p_\sigma\) の大きい側を \(i\)、\(n_\sigma\) の大きい側を \(k\) とする。両端をそれぞれ足し込むと重みの和が膨らむので \(\sum w_\sigma=1\) と (C2) を保つ。
\[
 \sum w_\sigma p_\sigma\le p_{-i}+(p_i-p_{-i})\,\sup w_i,\qquad
 \sum w_\sigma (dU-\sigma v)^2 n_\sigma
 \ge n_{-k}[\delta U^2+(1+U)^2v^2]
   +(n_k-n_{-k})\,\inf w_k\,\inf(dU-kv)^2 .\tag{F2}
\]
正項には \(2d(1-j/C)/C\) の上界もあり、小さい方を採る。

各方位セル \([a,b]\) 上に \(M_i=\langle\cos^i\phi\rangle\)、\(D_i=M_i-M_{i+2}\) と置く。等角平均の積分は
\(M_0=1,\ M_1=(\sin b-\sin a)/(b-a),\ M_i=[\sin\phi\cos^{i-1}\phi]_a^b/[i(b-a)]+(i-1)M_{i-2}/i\) である。非負重み \(\sin^2\phi\) で三項をまとめる。\(v_0=zm,\ v_1=\rho\sqrt{1-m^2}\) として
\[
 \begin{split}
 \langle v^2\rangle&=(v_0+\eta v_1 M_1)^2+v_1^2(M_2-M_1^2),\\
 \langle jv^2\rangle&=(1-m^2)D_0[(v_0+\eta v_1 D_1/D_0)^2+
                    v_1^2(D_2/D_0-(D_1/D_0)^2)],\\
 \langle j\rangle&=(1-m^2)D_0 .
 \end{split}\tag{F3}
\]
正幅のセルでは \(D_0>0\)。従って \(\langle d^2(1-j/C)\rangle=\delta+\langle v^2\rangle-(\delta\langle j\rangle+\langle jv^2\rangle)/C\)。二つの分散は非負である。(F2) でモーメントに掛ける係数の上・下端はセル全体で有効なので、同じ外側箱の全パラメータについて積分の片側包囲が成立する。

極の近くの法線には \(B=1-(1-\epsilon^2)\xi_z^2=\epsilon^2+(1-\epsilon^2)(\xi_x^2+\xi_y^2)\) の両式を用い、\([\epsilon^2,1]\) と交差する。\(\xi_\sigma=q+\sigma\ell_\sigma e,\ |v|\le d\le1,\ 0\le\ell_\sigma\le2d\) の相関を保持する。接触に近いセルでも (F1) の積は有界である。
