# 扁平回転楕円体の円板極限で、赤道縁に停留点は生じない

2026年11月20日 ／ Codex ／ **DIAGNOSTIC_ONLY / NOT_EVIDENCE** ／ Judge・chat 独立監査用

## 1　結論

\(\lambda_0=1/32\) とする。規格化された閉球 \(\rho^2+z^2\le1\) 上で、すべての \(0<\lambda\le\lambda_0\) に対して次の二式が成り立つ。

\[
 \boxed{\frac{E_z(\rho,z)}{z}\le-\frac6{55}\lambda\quad(z\ne0)},\qquad
 \boxed{E_\rho(\rho,0)\ge\frac{\lambda\rho}{24}\quad(0<\rho\le1)} .
\]

第一式は開球全体で成立する \(E_{zz}\le-6\lambda/55\) を赤道面から積分して得る。第二式の核心は、水平射影した単位円板で、動く直線 \(x=\rho/(1-\lambda^2)\) に関して積分点を鏡映することである。各式の余裕はすべての正の \(\lambda\le1/32\) に明示されている。

| 対象 | この範囲での結論 |
|---|---|
| 内部の停留点 | 中心だけ。横二方向の Hessian が正、軸方向が負の非退化鞍 |
| 境界の全勾配の内側トレース | 零集合は空。\(z\ne0\) は第一式、赤道は第二式で排除 |
| 既採用の表との接続 | 端点 \(1/32\) が重なる。V53 と Judge の採用済み範囲に接続すると、扁平・球・扁長を含む \((0,\infty)\) の分類が揃う |

新しい符号は解析だけで導いた。補間する有限 \(\lambda\) 帯は生じない。元の固定尺度漸近で未指定だった剰余の明示式と、\(\eta\) を縮められる範囲は付録Aに記す。

## 2　定義と角度関数

\(q=(\rho,0,z)\)、\(\xi=(x,y,\mu)\in S^2\)、\(L=\operatorname{diag}(1,1,\lambda)\) とする。\(\langle\cdot\rangle\) は面積 \(4\pi\) で割った球面平均である。

\[
 k=1-q\cdot\xi,\quad D=|L(\xi-q)|,\quad S=|L^{-T}\xi|,\quad
 g=\frac{k}{SD},\qquad E(q)=\langle k\,\arccos^2g\rangle.
\]
\(0\le g\le1\) は \(k=L^{-T}\xi\cdot L(\xi-q)\) と Cauchy–Schwarz による。\(\beta=1-\lambda^2,\ m=|\mu|,\ w=\lambda S=\sqrt{\lambda^2+\beta m^2}\) と書く。角度関数を
\[
 F(g)=\pi^2/4-\arccos^2g,\quad
 P=F',\quad Q=2P+gP',\quad J=F+gP-\pi^2/4,\quad K=g^2P
\]
とする。以下で使う評価は \(2\le P\le\pi,\ -2\le P'\le0,\ Q\ge10/3\) である。

実際、\(u=\tanh(t/2)\) と置換すると
\[
 P(g)=2\int_0^\infty\frac{dt}{\cosh t+g}
     =\frac{2\arccos g}{\sqrt{1-g^2}} .
\]
\(g=1\) では連続値を取る。微分して \(|P'|\le2\int_0^\infty\operatorname{sech}^2t\,dt=2\)。また \(Q\) の積分密度を \(c=\cosh t\) として \(2(2c+g)/(c+g)^2\) と書けば、\(g\) 導関数は \(-2(3c+g)/(c+g)^3<0\)。同じ置換で \(P(1)=2,\ P'(1)=-2/3\) が得られる。よって \(Q(g)\ge Q(1)=10/3\)。

開球では \(D>0\) で微分できる。固定した正の \(\lambda\) では、一次勾配は
\[
 E_i=\langle \xi_i J-L_{ii}S u_iK\rangle,\qquad u=L(\xi-q)/D .
\]
この密度は \(q\) に一様に有界であり、境界の接触点一つを除いて収束する。従って全勾配の内側トレースが存在する。零集合はこのトレースを使って定める。

## 3　赤道面での鏡映

この節では \(z=0,\ 0<\rho<1,\ 0<\lambda<1\) とする。\(\delta=1-\rho^2,\ s^2=1-\mu^2,\ x=s\cos\phi,\ y=s\sin\phi\)。回転対称性より \(H=E_{yy}=E_\rho/\rho\) である。\(k=1-\rho x,\ D^2=1+\rho^2-2\rho x-\beta\mu^2\)。

### 3.1　方位部分積分

勾配の式で \(\langle x\rangle=0\) を使うと
\[
 E_\rho=\left\langle x(F+gP)-(x-\rho)\frac{Pk^2}{SD^3}\right\rangle .
\]
\(\partial_\phi y=x,\ \partial_\phi k=\rho y,\ \partial_\phi D=\rho y/D\) だから、\(\langle xF\rangle_\phi=-\langle yP\,\partial_\phi g\rangle_\phi\)。まとめると
\[
 H=\left\langle \frac{P}{SD^3}N\right\rangle,\quad
 N=\delta y^2+\mu^2\{1+\beta s^2-(\rho+\beta/\rho)x\}.                 \tag{1}
\]
実際、整理前の分子は \(-y^2D^2+y^2k+xkD^2/\rho-(x-\rho)k^2/\rho\) である。式(1)自体と次の外縁の評価は既存の別報告にもある。今回の追加は負になり得る密度の積分符号を決める鏡映である。

### 3.2　鏡映で奇な項の符号を決める

\(0<\rho\le\beta\) とし、\(a=\rho/\beta,\ T=\beta/\rho-\rho\ge0\) と置く。(1)の波括弧は正確に
\[
 \beta\big((x-a)^2+y^2\big)-T(x-a) .                                  \tag{2}
\]
必要な主張は
\[
 I=\left\langle\frac{P\mu^2(x-a)}{SD^3}\right\rangle\le0.                \tag{3}
\]
上下両半球の水平射影を取り、単位円板を \(\mathbb D\) とする。面積要素は各面で \(dx\,dy/m\)。\(z=0\) なので両面が一致し、
\[
 I=\frac{\lambda}{2\pi}\int_{\mathbb D}
       \frac{x-a}{D^3}\,\frac{m}{w}P(g)\,dx\,dy .
\]

円板の右側にある任意の点 \((a+t,y)\), \(t>0\) を、左側の \((a-t,y)\) と対にする。\(a\ge0\) なので左点も円板に入る。添字 \(+,-\) が順に右、左を表す。\(r^2=t^2+y^2,\ A=1-\rho^2/\beta>0,\ C=A+\beta r^2\) とすると
\[
 D_+^2=D_-^2=\lambda^2 A+\beta r^2,\qquad
 w_\pm^2=A-\beta r^2\mp2\rho t,\qquad
 g_\pm=\frac{\lambda}{2D}\left(w_\pm+\frac{C}{w_\pm}\right).             \tag{4}
\]
\(w_-\ge w_+>0\) かつ \(w_-w_+\le(w_-^2+w_+^2)/2=A-\beta r^2\le C\)。従って
\[
 g_--g_+=\frac{\lambda(w_--w_+)}{2D}
            \left(1-\frac{C}{w_-w_+}\right)\le0 .
\]
\(P\) は減少し、\(m/w=m/\sqrt{\lambda^2+\beta m^2}\) は \(m\) とともに増加する。よって左点の重み \((m/w)P(g)\) は右点以上。二点の \(x-a\) は \(-t,+t\) で、分母と面積は等しい。右点を持たない部分はすべて左にあり、その寄与も非正である。これで (3) が従う。個々の \(N\) の符号を仮定する必要はない。

(1)–(3)に \(D\le2,\ S\le1/\lambda,\ P\ge2\) を使う。球面平均は \(\langle y^2\rangle=\langle\mu^2\rangle=1/3\)、\(\langle\mu^2(x^2+y^2)\rangle=2/15,\ \langle\mu^2x\rangle=0\) なので
\[
 H\ge\frac{\lambda}{4}\left[\frac{\delta}{3}
                 +\beta\left(\frac{2}{15}+\frac{a^2}{3}\right)\right]
 =\frac{\lambda}{4}\left[\frac13+\frac{2\beta}{15}
                        +\frac{\rho^2}{3}(\beta^{-1}-1)\right]
 \ge\frac{\lambda}{12}.                                                 \tag{5}
\]

### 3.3　外縁まで

\(\beta\le\rho<1\) では \(x\le s\) より (1)の波括弧は
\((1-\rho s)(1-\beta s/\rho)\ge0\)。特に \(x\le0\) で波括弧は \(1\) 以上である。この半球の \(\mu^2\) の全球正規化平均は \(1/6\) だから \(H\ge\lambda/24\)。\(\rho\uparrow1\) では \(E_\rho=\rho H\) の一次トレースを取る。従ってすべての扁平 \(0<\lambda<1\) で、赤道面全体に
\[
                    E_\rho(\rho,0)\ge\lambda\rho/24\quad(0<\rho\le1).    \tag{6}
\]
\(X=(1-\rho)/\lambda^2\) とすれば (5) は \(X\ge1\)、この外縁評価は \(0\le X\le1\) を扱う。二式は同じ \(X=1\) で重なる。

## 4　赤道面の外での軸方向凹性

再び一般の \(q=(\rho,0,z)\) を取る。\(p=(\rho,0),\ u_h=(x,y),\ R=|u_h-p|,\ v=\mu-z\) とする。\(D^2=R^2+\lambda^2v^2\)。この節の \(u_h\) は \(\xi\) の水平射影である。\(h_1=\lambda^2kv/D^2\) とすると
\[
 \begin{split}
 E_{zz}&=P_+-N_z,\\
 P_+&=\left\langle\frac{P\lambda^2 k^2R^2}{S D^5}\right\rangle,\qquad
 N_z=\left\langle\frac{Q}{S D}(\mu-h_1)^2\right\rangle .                \tag{7}
 \end{split}
\]
\(g_z=-(\mu-h_1)/(SD)\)、\((v/D)_z=-R^2/D^3\)、\(J'=Q,\ K'=gQ\) を \(E_z=\langle\mu J-\lambda^2 S(v/D)K\rangle\) に代入すればよい。

### 4.1　正項の上界

水平射影には、すべての \(0\le\rho<1\) で \(\langle1/R\rangle=\pi/2\) という恒等式がある。射影点 \(p\) を中心に角 \(\theta\) の半直線を取り、\(b_\theta=\sqrt{1-\rho^2\sin^2\theta}\) とする。円板内では
\[
 m^2=b_\theta^2-(R+\rho\cos\theta)^2.
\]
面積要素の \(R\) が分母の \(R\) と消え、動径積分 \(\int dR/m\) は \(\pi/2-\arcsin(\rho\cos\theta/b_\theta)\)。後半は反対向きの半直線で打ち消し合う。両面を合わせた \(1/(2\pi)\) 正規化で恒等式が得られる。

\(k=u_h\cdot(u_h-p)+\mu v\) から \(k^2\le2R^2+2m^2v^2\)。第一項の \(P_+\) への寄与は \(P\le\pi,\ S\ge1,\ D\ge R\) より \(2\pi\lambda^2\langle1/R\rangle=\pi^2\lambda^2\) 以下。第二項では \(S\ge m/\lambda\) と半球の射影を使う。その寄与は
\[
 \frac{\lambda^3}{2}\sum_{\sigma=\pm1}
       \int_{\mathbb D}\frac{v^2R^2\,dx\,dy}{(R^2+\lambda^2v^2)^{5/2}},
 \qquad v=\sigma m-z
\]
以下である。\(R\le4\lambda\) では \(t=\lambda|v|/R\) とおく。
\(t^2/(1+t^2)^{5/2}\le1/4\) より密度は \(1/(4\lambda^2R)\) 以下。\(R>4\lambda\) では \(|v|\le2\) より \(4/R^3\) 以下。各面でこの上界を平面全体に積分すると
\[
 2\pi\left[\int_0^{4\lambda}\frac{dR}{4\lambda^2}
        +\int_{4\lambda}^{\infty}\frac4{R^2}\,dR\right]=\frac{4\pi}{\lambda}.
\]
従って \(P_+\le(\pi^2+4\pi)\lambda^2<24\lambda^2\)。

### 4.2　負項を面積の大きい領域で下から押さえる

\(0<\lambda\le1/32\) とする。射影円板のうち
\[
 \Omega=\{\,|u_h|^2\le15/16,\ R\ge1/4\,\}
\]
だけを \(N_z\) に残す。ここで \(m\ge1/4\)、\(|k|\le R+m|v|\)、\(|v|\le2\)。従って
\[
 \frac{|h_1|}{m}
 \le\lambda^2\left(\frac{2}{mR}+\frac4{R^2}\right)
 \le\frac{96}{1024}<\frac1{10},\qquad
 \frac{m}{w}\ge\frac{32}{33}.
\]
最後は \(w^2/m^2\le1+1/64<(33/32)^2\) を使った。よって \(|\mu-h_1|\ge9m/10\) で、南北どちらの面にも適用できる。

\(\Omega\) の面積は \(7\pi/8\) 以上である。半径 \(1/4\) の円板をどの位置で取り除いても、その面積は \(\pi/16\) を超えない。また
\[
 \int_\Omega(R^2+4\lambda^2)\,dx\,dy
 \le\pi\frac{15}{16}\left(1+\frac{15}{32}+\frac1{256}\right)
 <\frac{3\pi}{2}.
\]
これは大きい方の円板全体で \(R^2=|u_h|^2-2p\cdot u_h+\rho^2\) を積分し、\(\rho^2\le1\) としたもの。領域平均の上界は \(12/7\) であり、\(12/7<16/9\) だから、\(u\mapsto u^{-1/2}\) の凸性より
\[
 \int_\Omega\frac{dx\,dy}{\sqrt{R^2+4\lambda^2}}\ge\frac34|\Omega|.
\]
射影の重み \(1/m\) を含めて (7) に戻すと、両面で \(D\le\sqrt{R^2+4\lambda^2}\)、\(Q\ge10/3\) より
\[
 \frac{N_z}{\lambda}
 \ge\frac{10}{3}\left(\frac9{10}\right)^2
          \frac{32}{33}\frac34\,\frac{7}{16}
 =\frac{189}{220}.
\]
最後の \(7/16\) は \(|\Omega|/(2\pi)\) の下界である。ゆえに開球全体で
\[
 E_{zz}\le\left(\frac{24}{32}-\frac{189}{220}\right)\lambda
             =-\frac6{55}\lambda .                                      \tag{8}
\]

## 5　縁の層と境界への接続

反射対称性から \(E_z(\rho,0)=0\)。(8)を固定 \(\rho\) の鉛直線上で積分すると、\(z\ne0\) で \(E_z/z\le-6\lambda/55\)。閉球の境界で \(z\ne0\) の点まで、同じ鉛直線に沿って一次勾配の連続性を使う。赤道境界には (6) を移す。境界で二階微分を仮定する段はない。中心の横 Hessian は (5) の \(\rho\downarrow0\) 極限で正、軸 Hessian は (8) で負、混合項は対称性で零である。

層の内部で横成分そのものの下界も欲しい場合、前報§7の \(\|\nabla^2 E\|\le32/\lambda^3\) と (6) から
\[
 |z|\le \rho\lambda^4/1536
 \quad\Longrightarrow\quad E_\rho(\rho,z)\ge\lambda\rho/48 .
\]
その外側には \(|E_z|\ge6\lambda|z|/55\) がそのまま及ぶ。この横成分の補足評価を使わなくても、(6)と(8)だけで零集合は決まる。特に \(\lambda\downarrow0,\ \rho\uparrow1,\ z\to0\) の相対速度を制限しない。

### Judge の既採用表に接続した分類

この表の最初の行に、新しい排除結果を使った。残りの行の入力は添付の Judge 裁定およびそこに記載された V49–V53 である。境界欄は内側からの全勾配が零となる集合を表す。

| \(\lambda\) | 中心 | 中心以外の内部 | 境界 |
|---|---|---|---|
| \((0,1/32)\) | 非退化鞍、軸方向が負 | なし | なし |
| \([1/32,\lambda_c^{ob})\) | 同上 | なし | なし |
| \(\lambda_c^{ob}\) | 退化鞍 | なし | なし |
| \((\lambda_c^{ob},\lambda_\partial^{ob})\) | 極小 | 回転軸上の鞍の対 | なし |
| \(\lambda_\partial^{ob}\) | 極小 | なし | 両極 |
| \((\lambda_\partial^{ob},1]\) | 極小 | なし | なし |
| \((1,\lambda_b^{pro})\) | 極小 | なし | なし |
| \(\lambda_b^{pro}\) | 極小 | なし | 赤道一周 |
| \((\lambda_b^{pro},\lambda_c^{pro})\) | 極小 | 赤道上の Morse–Bott 鞍の円 | なし |
| \(\lambda_c^{pro}\) | 退化鞍 | なし | なし |
| \((\lambda_c^{pro},\infty)\) | 非退化鞍、横二方向が負 | なし | なし |

各固定 \(\lambda>0\) で参照球と体積保存の物理座標は可逆な線形変換で結ばれる。勾配の零、Hessian の慣性、境界トレースの零はこの換算で対応する。極限 \(\lambda=0\) は分類の対象外である。

## 6　検算、再現、採否

**厳密な検算。** 記号恒等式と有理定数の比較を32項目実行した。結果は `verification/exact.json`。鏡映の二点の距離と \(g\) の大小の因数分解、Hessian の分解、射影面積と定数 \(189/220,\ 6/55\) を含む。積分の支配、鏡映する領域の対応、境界への極限は本文の議論による。

**非区間の数値診断。** 実行前に固定した14組の \((\lambda,\rho,z)\) を、緯度と方位の複合 Gauss–Legendre 求積（各小区間16点と32点）で評価した。高次側標本で赤道の最小 \(H/\lambda=1.9220786474\)、赤道面外の最大 \(E_z/(z\lambda)=-3.9767574943\)。\(E_{zz}/\lambda\) の標本最大は \(-3.7746455638\) だった。赤道では元の勾配と (1) の積分値の差を \(\lambda\) で割っても最大 \(4.4\times10^{-9}\) 未満。赤道境界を含む Hessian の標本値は内部の符号証明には用いていない。

\((\lambda,\rho,z)=(1/32,1/2,1/4)\) では、元の角度エネルギーの差分と解析式の絶対差が、\(E_\rho\) で \(6.7\times10^{-9}\)、\(E_z\) で \(2.0\times10^{-11}\)、\(E_{zz}\) で \(8.5\times10^{-10}\) より小さかった。二つの求積次数における \(E_{zz}/\lambda\) の最大差は \(2.0\times10^{-6}\) 未満。全数値は `verification/diagnostics.tsv` と `verification/diagnostic_summary.json` にある。これらの実数標本には区間誤差保証はない。

**再現。** ZIPを展開し、展開先で `bash reproduce.sh` を実行する。SHA-256を確認し、新しい一時ディレクトリで代数検算と数値診断を再生成する。依存は Python 3、SymPy、NumPy。今回の環境と入力の同一性は `SOURCES.md` に記した。`PLAN_AND_CODE.sha256` は初回計算前に固定した計画・コード5件を収録する。

**Judge への提案。** 独立監査では、まず (3) の鏡映で左点の重みが大きい向きと、(7) の正負両項を射影した際の \(1/(2\pi)\) を照合してほしい。これらを確認したうえで小 \(\lambda\) の行を研究成果として採用する案を推す。付録Aの明示定数は別に評価できる。今回、GeoEncloseReader による独立監査は実施していない。

## 付録A　固定尺度漸近の明示剰余

§3–§5はこの付録から独立である。\(\eta\) を空間の余白とし、\(0<\eta\le1,\ 0<\lambda\le1/32,\ |q|\le1,\ \rho\le1-\eta\) とする。前報§4の係数を
\[
 A(\rho)=\left\langle\frac{(1-\rho\cos\phi)^2}
 {\sqrt{1-2\rho\cos\phi+\rho^2}}\right\rangle_\phi,\qquad h=-A'/\rho
\]
と書く。軸では連続値を使う。以下の保守的な定数で二側評価が得られる。
\[
 \boxed{\left|H(\rho,z;\lambda)-\pi\lambda\log(1/\lambda)h(\rho)\right|
       \le 10^{10}\lambda\,\eta^{-7}} .                                  \tag{9}
\]
あえて大きい定数を残し、\(\eta\) と \(\lambda\) の依存を追えるようにした。

### A.1　分割と角度の一次項

\(b=\eta/8,\ d=\eta/2\)。\(\psi(m)=0\) を \(m\le b\)、\(\psi(m)=1\) を \(m\ge2b\) で用いる。中間は \(s_0=(m-b)/b\) として \(10s_0^3-15s_0^4+6s_0^5\) で接続する。従って \(|\psi_m|\le2/b,\ |\psi_{mm}|\le15/b^2\)。\(\chi=1-\psi\) とする。定数部分 \(\langle\pi^2 k/4\rangle=\pi^2/4\) が消えるので、\(H\) は \(-\langle k F(g)\rangle\) の横 \(y\) 二階微分である。

\(\chi\) の側では球面点を固定して微分する。\(m\le2b,\ |u_h|=\sqrt{1-m^2}\ge1-m^2\) より \(D\ge R\ge d\)。\(a_0=1/S=\lambda/w\) と書く。\(F=\pi g+F_2\) と分け、§2より \(|F_2|\le g^2,\ |F_2'|\le2g,\ |F_2''|\le2\)。横変位の微分をドットで示せば
\[
 |\dot k|\le1,\quad \ddot k=0,\quad |\dot D|\le1,\quad
 |\ddot D|\le1/D,\quad g\le2a_0/d,\quad
 |\dot g|\le3a_0/d^2,\quad |\ddot g|\le8a_0/d^3 .
\]
従って \(|(kF_2)^{\cdot\cdot}|\le124a_0^2/d^4\)。
\(\int_0^1a_0^2\,dm\le\pi\lambda/(2\sqrt\beta)\le2\lambda\) から、この部分の寄与の絶対値は \(248\lambda/d^4\) 以下である。

一次項は \(\pi a_0 k^2/D\)。\(p=q_h,\ U=(u_h)_y,\ Y=(u_h-p)_y\) とすれば、\(k^2/D\) の横二階微分は
\[
 G=\frac{2U^2}{D}-\frac{4kUY}{D^3}
          +k^2\left(-\frac1{D^3}+\frac{3Y^2}{D^5}\right).
\]
\(e_\phi=(\cos\phi,\sin\phi),\ k_0=1-p\cdot e_\phi,\ D_0=|e_\phi-p|\) とし、\(G_0\) はこれらの円周データで同じ式を評価する。\(D,D_0\ge d,\ |U|\le1,\ |Y|\le2,\ |k|\le2\)。\(G\) を独立な引数 \(U,Y,k,D\) の関数と見た偏導関数の絶対値は、順に \(20/d^3,\ 56/d^5,\ 60/d^5,\ 302/d^6\) 以下。引数の変化は順に \(m,\ m,\ 2m,\ m+2\lambda\) 以下である。最後は \(|\sqrt{1-m^2}-1|\le m^2\) と三角不等式を使う。従って
\[
 |G-G_0|\le (498m+604\lambda)/d^6.
\]
\(\int_0^1a_0m\,dm\le2\lambda,\ a_0\le1\) なので、一次項を \(G_0\) で置き換える誤差は \(1600\pi\lambda/d^6\) 以下。

係数 \(I=\int_0^1\chi a_0\,dm\) を取り出すと、全帯の積分は厳密に
\[
 \int_0^1a_0\,dm=\frac{\lambda}{\sqrt\beta}
       \left[\log(1/\lambda)+\log(1+\sqrt\beta)\right].
\]
\(1/\sqrt\beta-1\le2\lambda^2\) であり、切り落とした積分は \(2\lambda\log(1/b)\) 以下である。従って \(|I-\lambda\log(1/\lambda)|\le[3+2\log(1/b)]\lambda\)。\(|G_0|\le70/d^5\) を使うと係数置換の誤差は \(70\pi[3+2\log(1/b)]\lambda/d^5\) 以下。円周平均は回転不変だから \(\langle G_0\rangle_\phi=A'(\rho)/\rho=-h(\rho)\)。エネルギーの負号によって (9) の主項の符号は正になる。

### A.2　補帯の一様支配

\(\psi\) の側では別の取り方が必要である。各半球を射影し、\(Y_h=u_h-p\) を固定して \(p\) を横に動かす。\(\sigma=\pm1,\ \mu=\sigma m,\ R=|Y_h|,\ v=\sigma m-z,\ D^2=R^2+\lambda^2v^2\)。密度は \(W kF(g),\ W=\psi(m)/m\) であり、射影円板の外へ零延長する。\(m\le b\) の近傍で既に零なので、動く円板の境界から項は出ない。以下は \(m\ge b\) における絶対値の上界である。

| 量 | 値 | 横一階 | 横二階 |
|---|---|---|---|
| \(m\) | \(1\) | \(1/b\) | \(2/b^3\) |
| \(k\) | \(\min(2,D/\lambda)\) | \(3/b\) | \(4/b^3\) |
| \(a_0=\lambda/w\) | \(\lambda/b\) | \(\lambda/b^3\) | \(6\lambda/b^5\) |
| \(W=\psi/m\) | \(1/b\) | \(3/b^3\) | \(27/b^5\) |

実際、\(\dot m=-(u_h)_y/m\)、\(\ddot m=-1/m-(u_h)_y^2/m^3\)。
\(|\partial_m a_0|\le\lambda/b^2,\ |\partial_{mm} a_0|\le4\lambda/b^3\) は \(w\ge m\) より従う。
\(k\le D/\lambda\) は \(k=\xi\cdot(\xi-q)\le|\xi-q|\) による。
\(D\) を同じ方法で微分すると
\[
 |\dot D|\le\lambda/b,\qquad
 |\ddot D|\le\lambda^2/(b^2D)+2\lambda/b^3 .
\]
\(Dg=a_0k,\ g\le1\) を二度微分して
\[
 |\dot g|\le\frac{6\lambda}{b^3D},\qquad
 |\ddot g|\le\frac{24\lambda}{b^5D}+\frac{13\lambda^2}{b^4D^2}.
\]
\(V=kF(g)\) と置く。\(F\le\pi g,\ |P'|\le2\) から
\[
 |V|\le\frac{4\pi\lambda}{bD},\qquad
 |\dot V|\le\frac{18\pi\lambda}{b^3D},\qquad
 |\ddot V|\le\frac{130\pi\lambda}{b^6D}.
\]
最後の不等式では \(k\lambda^2/D^2\le\lambda/D\) を使う。従って \(|(WV)^{\cdot\cdot}|\le346\pi\lambda/(b^7R)\)。支持は \(|Y_h|\le2\) に入り、\(\int_{|Y_h|\le2}|Y_h|^{-1}dY_h=4\pi\)。両面を \(4\pi\) で正規化すれば補帯の寄与は \(700\pi\lambda/b^7\) 以下である。局所で同じ可積分関数が微分を支配する。固定正 \(\lambda\) で球内から境界に近づけるときも、固定 \(Y_h\ne0\) での点ごとの極限とこの支配が使える。

### A.3　\(\eta\) を縮める範囲

A.1–A.2 の絶対誤差は合計で
\[
 \lambda\left[
 \frac{700\pi}{b^7}+\frac{248}{d^4}+\frac{1600\pi}{d^6}
 +\frac{70\pi[3+2\log(1/b)]}{d^5}\right].
\]
\(b=\eta/8,\ d=\eta/2,\ \pi<4,\ \log(8/\eta)\le8/\eta\) を用いると (9) が得られる。

円周上で \(\langle \partial_\phi(\sin\phi\, k_0/D_0)\rangle_\phi=0\) を使い、\(-A'/\rho\) を整理すると
\[
 h(\rho)=(1-\rho^2)\left\langle\frac{\sin^2\phi}{D_0^3}\right\rangle_\phi
       \ge\frac{1-\rho^2}{16}\ge\frac{\eta}{16}.
\]
\(\rho=0\) では連続値 \(h(0)=1/2\)。従って (9) 単独でも
\(\eta^8\log(1/\lambda)>16\cdot10^{10}/\pi\) なら \(H>0\)。例えば \(\log(1/\lambda)>10^{11}\) に対して \(\eta(\lambda)=(10^{11}/\log(1/\lambda))^{1/8}\) と取れる。この具体例の閾値は非常に小さい。主結果の閾値 \(1/32\) は§3–§4で直接得られる。
