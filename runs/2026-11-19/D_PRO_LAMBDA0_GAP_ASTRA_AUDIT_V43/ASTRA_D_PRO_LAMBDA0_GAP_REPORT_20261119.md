# D-PRO：動く境界層の接続と、全域閾値を支配する定数

2026-11-19 / Judge の「Λ₀ の穴を埋める」依頼への回答

**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

新しい解析補題・区間計算とも独立監査前である。本報告の全域接続定理は、前報の明示的 C² 剰余評価 (P10) を仮定として使う。その評価を今回のスカラー検算で再証明したとは扱わない。既存の証拠、正本、計算機、GitHub のブランチには変更を加えていない。

## 1. 結論

**動く境界層を接続する方法は得られた。ただし、実用目標の Λ₀≤10 は得られていない。**

今回の到達点は三つである。

1. **極の薄層の閾値を 256 から 5 へ下げる評価を得た。** 元の微分核を解析的に下から包み、残る積分を Arb で全 1,024 パラメータ箱にわたり評価した。全箱で下界は 1/4 より大きい。これにより、解析の導出と実装が正しければ
   \[
   \lambda\ge5,\quad z>0,\quad1-z^2\le\lambda^{-2}
   \quad\Longrightarrow\quad E_z\ge\frac1{4\lambda}
   \tag{G1}
   \]
   となる。これは点標本だけの観察ではないが、今回の計算を独立した検収に代えることはできない。
2. **縮まない極帯まで延長できる。** 局所化した輸送演算子 \(T=\partial_z+\partial_\mu\) を用いると、\(S=\sqrt{1-z^2}\le2^{-12}\) の固定帯で \(E_z>0\) を示せる。λ≥4096 の部分は解析式と有理数比較だけで成立する。5≤λ≤4096 は (G1) が覆う。この固定帯は、前回取り残した \(\chi=\lambda^{-1}\)、\(\rho\simeq\sqrt\chi\) のような移動列も最終的に覆う。
3. **極以外の境界は、横方向 Hessian の異方的な積分上界で内部に接続できる。** 前報 (P10) を入力すると、次の十分条件が導ける。
   \[
   \boxed{\Lambda_0=2^{13000}\quad\text{（前報 P10 を仮定した十分条件）}.}
   \tag{G2}
   \]
   λ≥Λ₀ では内部の停留点は中心だけで、中心は鞍点になる。この閾値は非常に保守的であり、最小値の推定ではない。

**(G2) は実用的な達成ではない。** \(2^{13000}\) は十進で約 \(10^{3913.39}\) であり、[5,Λ₀] を被覆計算する案は実行できない。また、V42 が確認した事項に (P10) の全ての複素近傍の定数は含まれていない。全域結論を採用するには、今回の接続補題に加え、P10 の監査が必要である。

一方、(G1) は P10 に依存しない。先に監査する価値がある成果を、巨大な全域閾値から切り離して提出する。

## 2. 入力、正規化、再利用範囲

固定資料は `cotaxxxx/bg-spheroid-family`、commit
`021899b33c70be326dc8488b0ed7ef39cf3e1f2d`、
`runs/2026-11-19/D_PRO_POLE_BOUNDARY_ASTRA_AUDIT_V42/`。

| 再利用する内容 | 出典 |
|---|---|
| 元の核、E_z の核、符号分割 | `ASTRA_D_PRO_POLE_BOUNDARY_REPORT_20261119.md` §§2–3、(P1)–(P6) |
| 内部の明示的 C² 剰余 | 同 §4、(P9)–(P10)。今回の全域閾値の**仮定** |
| b の横微分、G の二階微分 | 同 §5、(P13)–(P15) |
| 横 Hessian 核と有限 λ の境界トレース | 同 §6、(P17)–(P18) |
| 既に独立に確認された範囲 | `CHAT_AUDIT_D_PRO_POLE_BOUNDARY_ASTRA_V42.md`「照合」「結論」 |
| 点求積の独立な参照実装 | `chat_pole_checks.py`。今回、新しい点の求積に流用していない |

前報の報告、V42、chat のスクリプトとログの 4 件について、固定コミットの `SHA256SUMS.txt` とバイト単位で一致した。`inputs/SOURCE_PIN_CHECK.json` に記録した。ZIP を新たに再取得して検査したという意味ではない。

前々報 `ASTRA_D_PRO_NEEDLE_REPORT_20261118.md` の (N12)–(N15) の写しも同梱した。a,b の出典であり、新しい λ≥5 の極評価には使っていない。

参照球の座標を \(q=(\rho,0,z)\)、物理座標を \(p=(\rho,0,\lambda z)\) とする。E は \(E_{K_\lambda}(Lq)\) を表す。体積保存族への正の相似で E は変わらない。以下の z 微分は参照座標微分で、物理座標の微分はその 1/λ 倍である。符号と停留点は変わらない。

\[
\epsilon=\lambda^{-1},\quad \mu=\xi_z,\quad s=\sqrt{1-\mu^2},
\quad S=\sqrt{1-z^2},\quad\chi=S^2,
\]
\[
\begin{split}
k&=1-z\mu-\rho s\cos\phi,\\
A&=s^2+\rho^2-2\rho s\cos\phi,\\
d^2&=(\mu-z)^2+\epsilon^2 A,\qquad B=s^2+\epsilon^2\mu^2,\\
\gamma&=\frac{\epsilon k}{d\sqrt B},\qquad
F(y)=\pi^2/4-\arccos^2y.
\end{split}\tag{G3}
\]

内点では k>0、0<γ≤1。接触点の一点で密度を商として定義しない。以下の境界の記述は内側からの積分のトレースである。

元の定義と \(\int k\,d\Omega=4\pi\) より
\[
E=\frac{\pi^2}{4}-\frac1{4\pi}\int kF(\gamma)\,d\mu d\phi.
\]
\(k_z=-\mu\)、\(\gamma_z/\gamma=-\mu/k+(\mu-z)/d^2\) を代入すると
\[
E_z=\frac1{4\pi}\int I\,d\mu d\phi,\quad
I=\mu(F+\gamma F')-\frac{k\gamma F'(\mu-z)}{d^2}.
\tag{G4}
\]

用いる基本不等式は
\[
\pi y-y^2\le F(y)\le\pi y,\quad
\pi-2y\le F'(y)\le\pi,\quad
F(y)\ge yF'(y)\ge0,\quad yF'(y)\le2.
\tag{G5}
\]
最後の式は y=cosα として \(yF'(y)=2\alpha\cot\alpha\le2\) から従う。F′ は減少するため、F(0)=0 より F≥yF′。例えば
\(F'(y)=2\int_0^\infty (v^2+2yv+1)^{-1}dv\)
を微分すればこの単調性を直接確かめられる。残りは前報で証明した評価である。

## 3. 極の薄層：λ≥5 の下界

### 3.1 接触点側の負の寄与を改善する

μ>z では (G4) の第一項は非負。v=μ−z として、第二項の絶対値は
\[
\frac{k\gamma F'v}{d^2}
=\frac{\sqrt B}{\epsilon}\,\gamma^2F'\frac vd
\le\frac{2\sqrt B}{\epsilon}.
\]
χ≤ε²X なら B≤ε²(X+1)。正規化した負の寄与 N は
\[
\boxed{N\le\frac{\epsilon^2X\sqrt{X+1}}{1+z}.}
\tag{G6}
\]
ここでは μ の区間の長さが \(1-z=\epsilon^2X/(1+z)\)、方位角を含む正規化が 1/2 である。前報 (P5) より X の増大に対して鋭い。A の正の下界は不要で、接触まで同じ評価を使える。

### 3.2 パラメータを無限区間 λ から有限箱へ移す

\[
0\le\epsilon\le\frac15,\quad0\le w,u\le1,\qquad
z=\sqrt{1-\epsilon^2w^2},\quad\rho=\epsilon wu.
\tag{G7}
\]
これで全 λ≥5、χ≤λ⁻²、ρ≤√χ を覆う。ε=0 は正規化した下界の連続極限として含める。E 自体を λ=∞ で微分する操作ではない。

\(c=3/4\)、\(\delta_\theta=1/64\) とする。

- \(\mu\in[c,z]\) は (G4) の両項が非負なので捨てる。
- \(\mu>z\) の寄与を (G6) で引く。
- 南端 \(\theta\in[\pi-\delta_\theta,\pi]\)、μ=cosθ の負の寄与は \(-\pi\epsilon\delta_\theta/z\) 以上。
- 残り \(\theta\in[\arccos c,\pi-\delta_\theta]\) を直接下から積分する。

南端の評価は、μ<0 で第二項を捨て、F+γF′≤2πγ を用いた後に d≥z−μ、√B≥s と置く。**方位角の平均を先に取る**と k の ρcosφ 項が消え、
\((1-z\mu)/(z-\mu)\le1/z\)、\(|\mu|\le1\)
から上の値を得る。特異な南端を数値セルで包む必要がなくなる。

### 3.3 保持する領域の下側包絡

\[
T_0=\frac{s}{\sqrt B},\quad
f_1=\mu k,\quad f_2=\mu k+\frac{k^2(z-\mu)}{d^2}.
\]
保持領域における \(I\,s/\epsilon\) は厳密に
\[
\frac{T_0}{d}\left[f_1\frac{F(\gamma)}\gamma+f_2F'(\gamma)\right].
\]
\(F(\gamma)/\gamma\in[\pi-\gamma,\pi]\) を使い、係数の符号を残せば
\[
\boxed{\mathcal L=
\frac{T_0}{d}\left\{\pi(f_1+f_2)
-\gamma\bigl[(f_1)_++2(f_2)_+\bigr]\right\}
\le I\,s/\epsilon.}
\tag{G8}
\]
ここで \(x_+=\max(x,0)\)。負の係数に誤って下側の F の値を掛けてはいない。ρ,z,ε の相関は (G7) から構成し、独立した外箱に作り直さない。

\(\phi\mapsto2\pi-\phi\) の反射を使い
\[
\lambda E_z\ge
\frac1{2\pi}\int_0^\pi\int_{\arccos c}^{\pi-\delta_\theta}
\mathcal L\,d\theta d\phi
-\frac\pi{64z}
-\frac{\epsilon w^2\sqrt{1+w^2}}{1+z}.
\tag{G9}
\]

### 3.4 区間積分と結果

`cap_interval.py` は (G9) を **セル上の値域×セルの面積** で包む。Gauss 求積の推測誤差や差分微分を用いない。

- Arb 128 bit、python-flint 0.8.0。
- θ を 96 等分、φ∈[0,π] を 48 等分。
- ε を [0,1/5] の 16 等分、w,u を各 8 等分：計 1,024 外箱。
- 精度、格子、箱、1/4 の判定基準を実行前に固定。
- 平方は有理数端点から非負の包囲を作る。A は \((s-\rho)^2+2s\rho(1-\cos\phi)\) として包む。
- γ は幾何学的に [0,1] に属するので、その区間と交差を取る。
- 保持領域では \(z-c\ge\sqrt{24/25}-3/4>0\)、s≥sin(1/64)>0。分母は正である。

厳密な最小下端は
\[
\frac{47473218194072764542240096942353646083}
{170141183460469231731687303715884105728}
\approx0.2790224990>\frac14.
\tag{G10}
\]

`check_cover.py` は全インデックス、重複なし、端点、1/4 との比較を Python Fraction で確認した。**これは被覆と結果の検査であり、独立再積分ではない。** 1,024 行全てに有理数下端を保存した。実行時間はこの環境の 4 ローカルプロセスで約 58.9 秒。研究用 PC の速度を測った値ではない。

最初の非区間診断 36 点と、最初の区間パイロット 4 箱も保存した。パイロットは 2 箱が基準未達だった。その後、事前計画 R2 を作り、外側箱の各幅を半分にした上記全被覆を行った。未達の結果を上書きしていない。

λ=5 の R63_T63 について、前報で確認した
\(\chi\le2032381/65044225<1/25\)
が同じ座標定義の箱に適用されるなら、幾何学的には (G1) の領域に入る。ただし、その箱の既存証拠や判定を変更したわけではない。有限の λ 板へ適用する際は、その板の最大 λ でも \(\lambda^2\chi\le1\) かを別途確認する。

## 4. 移動する極帯：局所輸送で固定幅まで広げる

以下は新しい解析補題である。

\[
S_0=2^{-12},\quad 0<S\le S_0,\quad S\ge4\epsilon,
\quad h=S^2/4,\quad v=\mu-z.
\tag{G11}
\]
帯 \(z-h\le\mu\le z+h\) の中で \(\ell=s-\rho\cos\phi\) と置く。
帯は球面の端点に達しない。s²≥S²/3、z≥99/100、μ>0 が成り立つ。

### 4.1 帯の内部は非負にできる

\(T=\partial_z+\partial_\mu\)、f=kF(γ) とする。前報 P19 の重み付き輸送とは異なり、帯の端点項を残す。
\[
I=-\partial_z f=\partial_\mu f-Tf,
\]
\[
k=s\ell+\mu v,\quad -Tk=z+\mu\ell/s,\quad
A_\mu=-2\mu\ell/s,\quad B_\mu=-2(1-\epsilon^2)\mu.
\]
T は v を固定するため、\(T(d^2)=\epsilon^2A_\mu\)。よって
\[
-Tf=(-Tk)(F+\gamma F')
+k\gamma F'\left[\frac{\epsilon^2A_\mu}{2d^2}+\frac{B_\mu}{2B}\right].
\tag{G12}
\]
\(\ell/s\ge1-\sqrt3>-3/4\) なので −Tk>0。(G5) より
\[
-Tf\ge\gamma F'C,\qquad
C=2z+2\mu\ell/s-k\mu\left[
\frac{\epsilon^2\ell}{sd^2}+\frac{1-\epsilon^2}{B}\right].
\tag{G13}
\]

\((1-\epsilon^2)/B\le1/s^2\) を用いる。ℓ≥0 のとき、A≥ℓ² と
\(|v|\epsilon\ell/(v^2+\epsilon^2\ell^2)\le1/2\) から
\[
\frac{\epsilon^2k\ell}{sd^2}
=\frac{\epsilon^2\ell^2}{d^2}
+\frac{\epsilon^2\mu v\ell}{sd^2}
\le1+\frac{\epsilon\mu}{2s}.
\]
従って
\[
C\ge2z-\mu+\frac{\mu\ell}s-\frac{\mu^2v}{s^2}
-\frac{\epsilon\mu^2}{2s}
\ge\frac{49}{50}-\frac34-\frac7{32}
=\frac9{800}>0.
\tag{G14}
\]
最後に v≤h、s²≥S²/3、ε≤S/4、√3<7/4 を使った。

ℓ<0 のとき、(G13) の ε²ℓ の項は非負の寄与になるので捨てられる。その結果
\[
C\ge2z+\frac{\mu\ell}s-\frac{\mu^2v}{s^2}
\ge\frac{99}{50}-\frac34-\frac34=\frac{12}{25}>0.
\tag{G15}
\]
したがって帯の内部で −Tf≥0。**μ=z の距離分母の大きな項を、絶対値積分で失わずに処理した**ことがこの補題の要点である。

### 4.2 端点項と、帯の上側を包む

帯全体の寄与は \(f(z+h)-f(z-h)-\int Tf\) であり、f≥0 より −f(z−h) 以上。
μ=z−h では
\[
s\ge S,\quad s^2\le\tfrac32 S^2,\quad
k\le\tfrac52 S^2,\quad d\ge h.
\]
F≤πγ から f(z−h)≤25πεS。方位角の正規化後の帯の損失は
\[
\frac{25\pi}{2}\epsilon S.
\tag{G16}
\]

μ≥z+h では k≤2S²、d≥v≥h、√B≥s。負の項を積分すると
\[
N_{\mathrm{upper}}\le32\pi\epsilon
\int_{z+h}^1\frac{d\mu}{s}
\le32\pi\epsilon\arcsin S\le64\pi\epsilon S.
\tag{G17}
\]
帯とその上側の損失の合計は \((153\pi/2)\epsilon S\)。S→0 で消え、X=λ²S² の上限は必要ない。

### 4.3 離れた正の領域を残す

c=15/16 とし、0≤μ≤c の正の寄与を前報 (P6) と同じ方法で残す。ただしここでは
\[
\epsilon\le e_0=S_0/4,\quad\rho\le r_0=S_0,
\quad\chi\le\chi_0=S_0^2,\quad z\ge z_0=9999/10000
\]
を使う。χ≤ε²X を仮定していない。
\[
Q=\frac{e_0^2(1+r_0)^2}{(z_0-c)^2},\quad
U=\frac{e_0^2}{1-c^2},\quad v_0=1-\frac{r_0}{1-c},
\]
\[
K=\frac{v_0}{1+Q},\quad L=\frac{v_0}{\sqrt{(1+Q)(1+U)}},\quad
G=e_0\left[\frac{1+\chi_0/(z_0-c)}{\sqrt{1-c^2}}+
\frac{r_0}{z_0-c}\right].
\tag{G18}
\]
この領域で γ≥εL/s、γ≤G、\(k(z-\mu)/d^2\ge K\)。有理数で
K,L≥99/100、G≤1/1000 を確認できる。

負の半球には前報 P4 の \(\pi\epsilon(1+\rho/2)/z\) を使用し、c<μ<z−h は非負なので捨てる。(G16)–(G18) を合わせると
\[
\begin{split}
E_z/\epsilon\ge{}&\frac{99}{200}
\left[\left(2\frac{157}{50}-\frac3{1000}\right)\frac{13}{20}
+\left(\frac{157}{50}-\frac2{1000}\right)\frac{99}{100}\frac65\right]\\
&-\frac{22/7}{9999/10000}(1+S_0/2)
-\frac{153}{2}\frac{22}{7}S_0\\
={}&\frac{2248950598883}{3393600000000}>\frac12.
\end{split}\tag{G19}
\]
π、arcsin c の有理数評価は `exact_checks.py` で再確認した。

### 4.4 S<4ε とつなぐ

λ≥4096、S≤4ε では (G6) の X=16 を使える。e₀=1/4096、r₀=4e₀、χ₀=r₀² として (G18) を再評価すると K,L≥93/100、G≤3/250。ρ≤1/256、z≥9999/10000 で、
\[
N/\epsilon\le\frac{e_0\,16\sqrt{17}}{1+z}<\frac1{100}.
\]
従って
\[
E_z/\epsilon\ge
\frac{93}{200}\left[
\left(2\frac{157}{50}-\frac9{250}\right)\frac{13}{20}
+\left(\frac{157}{50}-\frac6{250}\right)\frac{93}{100}\frac65\right]
-\frac{22/7}{9999/10000}\left(1+\frac1{512}\right)-\frac1{100}
=\frac{6097089757}{17675000000}>\frac14.
\tag{G20}
\]

(G19),(G20) は λ≥4096 の固定極帯を覆う。5≤λ≤4096 では S≤1/4096≤1/λ なので (G1) が覆う。結果として
\[
\boxed{\lambda\ge5,\quad z>0,\quad S\le2^{-12}
\quad\Longrightarrow\quad E_z\ge\frac1{4\lambda}.}
\tag{G21}
\]
λ≥4096 だけなら、この結論に §3 の区間計算は不要である。

南側は反射で同様。以上の計算はまず内点で行う。有限λの微分トレースと一様可積分性（前報P17–P18）で、ρ=S の接触点や極へ延長する。∞ と境界の極限を無条件に交換してはいない。

## 5. 極以外の境界：Hessian の異方性を保持する

### 5.1 12/|ξ−q| をそのまま使わない

物理距離 \(D_p=\sqrt{A+\lambda^2(\mu-z)^2}=d/\epsilon\) を残す。前報 P17 の途中の不等式から
\[
|E_{\rho\rho}|\le\frac{12}{4\pi}\int\frac{d\Omega}{D_p}.
\tag{G22}
\]
ここで S≥S₀。\(a_0=S_0^2/8\)、\(b_0=S_0/2\) とする。|μ−z|≤a₀ では s≥b₀ であり、
\[
A=(\rho-s\cos\phi)^2+s^2\sin^2\phi\ge b_0^2\sin^2\phi.
\]
従って、この帯の正規化した \(\lambda/D_p\) 積分は
\[
\left\langle\operatorname{asinh}
\frac{\lambda a_0}{b_0|\sin\phi|}\right\rangle_\phi
\le\log(1+\lambda)+\log2.
\]
asinh x≤log(1+2x)、\(2a_0/b_0\le1\)、
\(\langle-\log|\sin\phi|\rangle=\log2\) を使った。φ=0,π の一点では上界は無限だが、角度積分は有限である。

帯の外では λ/Dₚ≤1/|μ−z| なので上界は log(2/a₀)。よって、全ての 0≤ρ≤S に対し
\[
\boxed{|\lambda E_{\rho\rho}|\le
M_\lambda:=12\{\log(1+\lambda)+\log(32/S_0^2)\}.}
\tag{G23}
\]
反射と \(H=\int_0^1 E_{\rho\rho}(t\rho,z)dt\) から
\[
|\lambda H|\le M_\lambda,\qquad
|\partial_\rho(\lambda H)|
=\left|\frac{\lambda E_{\rho\rho}-\lambda H}{\rho}\right|
\le\frac{2M_\lambda}{\rho}\quad(\rho>0).
\tag{G24}
\]
この評価は接触まで有効で、λ倍しても O(logλ) にとどまる。前報の一様な 12 という粗い Hessian 上界を λ 倍した O(λ) とは異なる。

### 5.2 b の横方向係数も移す

前報の
\[
\frac{b_\rho}{\rho}=\pi\left[z\arcsin z+S\log(4S)
+S\frac{G'(u)}u\right],\qquad u=\rho/S,
\]
\(|G''|\le11\)、G′(0)=0 を使う。u≥1/4 では
\[
\left|\partial_\rho\frac{b_\rho}{\rho}\right|
=\pi\left|\frac{G''(u)}u-\frac{G'(u)}{u^2}\right|
\le88\pi.
\tag{G25}
\]
主要係数 \(a_\rho/\rho=\pi S\) は、z を固定するとρに依存しない。このため境界へ横方向に移す際、logλ の主要項同士を差し引く誤差は生じない。

## 6. 条件付きの全域接続定理

### 6.1 明示する入力仮定

本節は前報 P10 を次の形で仮定する。
\[
E=\pi^2/4-\{a\log\lambda+b\}/\lambda+R_\lambda,
\]
\[
\|\lambda R_\lambda\|_{C^2(K_m)}
\le6\,2^{100}m^{-40}\lambda^{-1/5}\log(2\lambda)
\quad\left(\lambda\ge(2/m)^5\right),\quad
K_m=\{|q|\le1-m\}.
\tag{A1}
\]
0<m≤1、λ≥2 とする。これは C⁰ の上界を形式的に微分したものではなく、前報の C² 補題そのものへの依存である。**本節の数値閾値は A1 の定数まで正しい場合の結論である。**

### 6.2 λ とともに薄くする内部集合

\[
L=\log(2\lambda),\quad
\delta=\frac{S_0}{2^{20}L},\quad
m=\frac{S_0\delta}{4}=\frac1{2^{46}L}.
\tag{G26}
\]
まず S≥S₀、q∉Kₘ の点を考える。\(\rho^2>S^2-2m\) より ρ≥S/2。
\(q'=(\rho-\delta,0,z)\) とすれば、δ≤ρ、δ≤S/4 によって
\[
1-|q'|\ge\frac{\rho\delta}{2}\ge m,
\qquad \rho-\delta\ge S/4.
\]
したがって q′∈Kₘ であり、接続する線分上では (G24),(G25) を使える。

\(H=-(\pi S\log\lambda+b_\rho/\rho)/\lambda+R_\rho/\rho\)
を q,q′ で引く。主要係数が等しいことから
\[
\boxed{
\left|\lambda\frac{R_\rho}{\rho}(q)\right|
\le D_\lambda+left(\frac{8M_\lambda}{S_0}+88\pi\right)\delta,
\quad
D_\lambda=6\,2^{1940}\lambda^{-1/5}L^{41}.}
\tag{G27}
\]
q∈Kₘ では第一項だけでよい。\(R_\rho/\rho=\int_0^1R_{\rho\rho}(t\rho,z)dt\) によりρ=0も連続に扱える。

これが前報の穴を埋める接続である。固定 m の結果を境界へ無断で延長するのではなく、m=m(λ) として、その依存を Dλ に全て残す。非極境界の外側カラーには (G27)、極へ動く列には (G21) を用いる。全領域で同時に H<0 を示す必要はない。

### 6.3 整数の閾値で定数を閉じる

λ≥2¹³⁰⁰⁰ とする。閾値で L=13001log2<2¹⁴ なので
\[
D_\lambda\le6\,2^{1940-2600+574}=6\,2^{-86}<1/8192.
\]
\(\lambda^{-1/5}L^{41}\) は L>205 で減少するため、閾値より上でも成立する。また \(\lambda\ge2^{235}L^5=(2/m)^5\) は閾値で成立し、\(\lambda/L^5\) が増加するので全域で保たれる。

\(\log(32/S_0^2)=29\log2\)、\(\log(1+\lambda)\le L\) から接続誤差は
\[
\left(\frac{8M_\lambda}{S_0}+88\pi\right)\delta
\le\frac{96}{2^{20}}\left(1+\frac{29}{13001}\right)
+\frac{88(22/7)2^{-12}}{2^{20}(13001\cdot2/3)}
=\frac{4483154283}{48859011088384}<\frac1{8192}.
\tag{G28}
\]
結果として S≥S₀ では \(\lambda|R_\rho/\rho|<1/4096\)。

前報 P15 は λ≥65536 で
\(\pi S\log\lambda+b_\rho/\rho\ge\pi/64\)
を与える。この係数の評価は (A1) とは独立である。従って
\[
\boxed{S\ge S_0,\quad\rho>0,\quad\lambda\ge2^{13000}
\quad\Longrightarrow\quad H<-\frac1{32\lambda}.}
\tag{G29}
\]

### 6.4 回転軸も排除する

ρ=0、S≥S₀ の点は Kₘ に入る。前々報 N15 より
\[
\frac{b_z(0,z)}{\pi z}
=(2-3z^2)\frac{\arcsin z}{z}-3S\log S.
\]
\(\arcsin z/z\le\pi/2\)、\(-S\log S\le1/e<1/2\) なので
\[
\frac{b_z(0,z)}z\le\pi(\pi+3/2)<15.
\]
A1 を z の反射商に使うと
\[
\lambda\frac{E_z(0,z)}z
\ge3\pi S\log\lambda-15-D_\lambda
>\frac{78000}{4096}-15-\frac1{8192}
=\frac{33119}{8192}>1.
\tag{G30}
\]
z=0 では二階微分への連続延長で解釈する。

S≤S₀ は (G21)、S≥S₀ かつρ>0は(G29)、残るρ=0,z≠0は(G30)が覆う。中心は対称性で停留点である。中心で横方向は負、軸方向は正なので鞍点となる。これで **A1 を前提とする** (G2) の組立証明が得られる。

## 7. 何が Λ₀ を大きくしているか

| 領域・部品 | 得られた条件 | 実用閾値への影響 |
|---|---|---|
| 極の薄層 S≤1/λ | λ≥5、区間下界の最小は0.2790 | 256の障害は除けた。独立検収は必要 |
| 固定極帯 S≤2⁻¹² | λ≥4096は解析、5≤λ≤4096は薄層補題 | 全体ではλ≥5。極の移動列は残らない |
| 非極境界への移送 | 誤差は O(δ logλ/S₀)。δ=S₀/(2²⁰log(2λ)) | 一様接続が可能になった |
| 二項近似の H の余裕 | λ≥65536でπ/64 | 有限だが粗い。実際のλ≈5に直結しない |
| 内部の C² 剰余 A1 | \(6\,2^{1940}\lambda^{-1/5}L^{41}\) | **全域の巨大な閾値を決める主因** |
| 軸方向係数 b_z/z | 上界15 | 主要項と比較できるが、極以外の一様下界を粗く取っている |

2¹³⁰⁰⁰ という選択では各不等式に大きい余裕がある。整数指数を少し下げる最適化はできても、5〜10に近づく改善ではない。今回、P9/P10 の Cauchy 評価を実用的な導関数評価に置き換えるところまでは到達していない。

特に A1 の m⁻⁴⁰ を、m∼1/logλ に代入したため L⁴¹ が生まれた。これは真の残差がその大きさだという主張ではない。**弱い評価を採用した費用が式に明示された**ということである。

## 8. 次の計算と解析の分担

依頼書の「λ幅1当たり約16日」を、研究用PC全体の所要時間としてそのまま使う。12コアでさらに割ってはいない。

| 仮に解析側で確保できた閾値 Λ₁ | [5,Λ₁] の単純外挿 | 現時点の解析側 |
|---:|---:|---|
| 5 | 追加0日 | 全域の残差・条件C21は未解決 |
| 6 | 約16日 | 同上 |
| 8 | 約48日 | 同上 |
| 10 | 約80日 | 同上 |
| 2¹³⁰⁰⁰ | 実行不能 | A1を前提に全域接続ができるだけ |

これは性能上限の保証ではなく、λが増しても速度が同じと仮定した外挿である。現在の結果から「何日で全域を終えられる」とは言えない。

**推奨は次の分担である。**

1. chat は (G6)–(G10) を先に独立監査する。1,024 箱の単純な値域積分で、既存の高次 jet producer を読む必要がない。Dig が動作を再確認する場合も新しい作業フォルダで実行する。採用できれば、既存窓の該当する極の隅を軽くできる。
2. 数学の監査では、局所輸送の (G12)–(G20) と、非極の異方的ポテンシャル評価 (G23) を優先する。この二つは A1 に依存せず、今後別の残差評価へ置き換えても使える。
3. 有限 Λ₀ の存在を数付きで記録する研究上の価値はある。ただし (G2) の採用には A1/P10 の定数の監査が別途必要。実用的計算計画の根拠にはしない。
4. [5,8] や [5,10] の大きな追加被覆を先に発注しない。その上端から先を解析で処理できる保証がまだないためである。既存 [2,5] の C21 計算の方針は、本報告だけで変更しない。
5. 次の解析上の狙いは、λが5〜10のときにも使える、**同じ密度の中で a logλ+b を除いた微分残差の上界**である。別々に包んだ大区間の引き算では足りない。特に \(R_{\rho\rho}\) の球面積分の相殺を保ち、A1 の m⁻⁴⁰ と λ⁻¹ᐟ⁵ を置き換える必要がある。今回その実装の速度や成功率は測っていない。

Judge への選択肢は、「極の補題と接続構造の監査を先に行う」（推奨）と、「実用閾値が得られるまで全域閾値の採用を保留する」である。両者は両立する。既存計算の停止や再開、証拠の採用をこの報告から自動的に決めない。

## 9. 成立条件、限界、OPEN

- **実用的な全域 Λ₀≤10：OPEN。** 点の余裕や今回の極補題から推定で埋めない。
- **A1/P10 の明示的 C² 定数の独立監査：OPEN。** 本報告の全域数値閾値はこの仮定に依存する。スカラー比較が全て成立しても、P10 の複素近傍・界面項の評価を確認したことにはならない。
- 新しい極帯・異方的ポテンシャルの証明は本稿に付けたが、独立監査前である。
- λ≥5の薄層は全パラメータ箱を包んだ。独立の再積分、外向き丸め実装の確認、幾何学的領域との照合は今後必要。
- H<0を極まで一律に証明したわけではない。停留点排除に必要な領域別の符号を使った。
- 同じ方法で有限窓 [2,5] 全体の停留円を分類したわけではない。既存の軸条件Z、赤道条件C、分岐・境界の条件は別工程である。
- 本稿は厳密な有限領域での計算機援用評価を含むが、標題どおり全て研究資料である。

## 10. 納品と再現

| ファイル | 内容 |
|---|---|
| 本報告書 | 新しい解析と仮定付きの組立 |
| `PLAN_BEFORE_RUN.md` | 最初の固定診断計画 |
| `PLAN_INTERVAL_R1_BEFORE_RUN.md` / `PLAN_INTERVAL_R2_BEFORE_RUN.md` | パイロット、全被覆それぞれの事前宣言 |
| `cap_envelope_probe.py` / `CAP_ENVELOPE_PROBE.json` | 36点の非区間診断。証明には使用しない |
| `cap_interval.py` / `CAP_INTERVAL_PILOT_R1.json` | 区間の下側包絡、最初の4箱。未達2箱を保存 |
| `cap_cover_r2.py` / `CAP_COVER_R2.jsonl` | 全1,024箱の区間計算と全出力 |
| `check_cover.py` / `CAP_COVER_CHECK.json` | 被覆と有理数下端の検査 |
| `exact_checks.py` / `EXACT_CHECKS.json` | 有理数による40項目。解析補題そのものの証明ではない |
| `algebra_checks.py` / `ALGEBRA_CHECKS.json` | 輸送・軸係数の厳密記号計算11件 |
| `inputs/` | 固定資料の写し、出典・SHA照合 |
| `SHA256SUMS` | 同梱ファイルのSHA-256 |

新しいフォルダに展開し、python-flint 0.8.0、SymPy、NumPyを用意した上で、

```bash
python cap_cover_r2.py && python check_cover.py && python exact_checks.py && python algebra_checks.py
```

で今回の主要な計算を再現できる。コードは同じフォルダに出力を書き込むため、封印原本の中で実行しないこと。元資料を写した部分を clean-room 実装とは呼ばない。核と係数は明記した出典を再利用し、今回の輸送、帯の分割、異方的ポテンシャル評価、区間包絡コードは新しく作成した。

ZIP自身のSHAは外側の `.sha256` に記録する。ZIP内部のSHA256SUMSは自分自身を含めない。

[固定資料のディレクトリ](https://github.com/cotaxxxx/bg-spheroid-family/tree/021899b33c70be326dc8488b0ed7ef39cf3e1f2d/runs/2026-11-19/D_PRO_POLE_BOUNDARY_ASTRA_AUDIT_V42/)
