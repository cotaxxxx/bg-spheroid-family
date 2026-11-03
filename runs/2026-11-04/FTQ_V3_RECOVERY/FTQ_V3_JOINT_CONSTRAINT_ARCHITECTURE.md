# FT_q V3 joint-constraint architecture

2026-10-16 / architecture submission / chat audit requested

## 0. Executive verdict

**FT_q V3 joint-constraint architecture: READY_FOR_CODEX**

**V3 METHOD_SELECTED candidate:** 非負 Bernstein polynomial multipliers ＋ 非負 Bernstein residual ＋ exact rational LP primal/dual certificate。

これは、固定条件で実装し独立検査できる証明書形式が成立したという判定である。whole-face positivity、固定次数での成功、計算時間を保証する判定ではない。V3 production / LP solve は実施していない。次工程は chat architecture audit → Judge → implementation/production である。

今回、物理写像を表す6本の lifted polynomial equalities と、4変数上の8本の低次数 joint inequalities を導出した。最適化には後者を使用する。**この reduced domain は物理集合を包含する joint semialgebraic 外包であり、物理集合の exact projection と同一とは主張しない。** 残存緩和を §7 に列挙する。

FT_q: PARTIAL / whole-face m0: UNPROVED / L3: FREEZE HOLD / L1: PAUSED / D-P2: NOT_CERTIFIED を維持する。V1/V2 の負の certificate は物理反例ではない。

## 1. 原典・採用事項・今回の検算範囲

本報告の入力は Judge の V3 指示書に記された accepted V2 identities、fixed physical partition、V2 fixed enclosure recipe である。V2 production の集計結果と chat ACCEPTED は Judge から受領した状態として継承し、今回再計算していない。

使用した固定原典・実装（以下5件は今回、手元の bytes の SHA-256 と一致確認）：

|入力|SHA-256|
|---|---|
|FTQ_CORRELATION_RECOVERY_ARCHITECTURE_V2.md|03f6a799db51a7813f622391f67373b858e64344f2c68c02f0218eade17420b5|
|ftq_v2_fixed_enclosure.py|c83709482525da48fe7fb28fdd15d5dd7f999909a51be855e808847d6f1f1b1f|
|ftq_algebra.py|e24ff38dae62d7457aedc65ab46e528c8a737c5887e3ff037b098c4fdb6ed30b|
|V1.1 reference|cafc0516b794d2a7643fcfa2b2d975333ce2cbe851f55573590310478dc57e3a|
|fixed physical partition|9c0509d1f025811bd463ec826a3830996ab642e24a3983bd12d5a7c4c7afd38b|

P1 normalization、paired density、boundary extension および endpoint NP-T への接続は、監査済み V2 の入力を継承する。この報告で P1/NP-T 原典の独立再監査を済ませたとは主張しない。

今回実行したのは有理係数多項式の恒等式検査、次数検査、係数数の計算のみ。添付ソースは callable specification と architecture checks であり、LP producer / independent checker の完成実装ではない。診断走査、数値積分、512箱の評価、LP solve は行っていない。旧 m0、−26.70 の試算、V2 の最悪箱や margin を、次数・制約・分割の選択に使用していない。

## 2. 固定された幾何と kernel

physical box の変数は (τ,μ,s,λ,t)、branch は ε∈{−1,+1}。s∈[0,1] は folded cosine の絶対値で、実際の cosine は εs とする。

\[
R=\frac{1-\tau^2}{1+\tau^2},\quad Z=\frac{2\tau}{1+\tau^2},\quad a=\sqrt{1-\mu^2},
\]
\[
X=a\epsilon s-R,\quad Y^2=(1-\mu^2)(1-s^2),\quad \Delta=\mu-Z,
\]
\[
S=X^2+Y^2+\Delta^2,\quad P_2=X^2+Y^2+\lambda^2\Delta^2,
\]
\[
u=\sqrt S,\quad K:=k^2=P_2/S,\quad n=Y^2/P_2,\quad
w^2=\lambda^2+(1-\lambda^2)\mu^2,\quad
\gamma=\frac{\lambda u}{2wk}.
\]

比による定義は S>0 で用い、contact では後述の閉包と γ=0 の連続延長を用いる。ν=(ξ−Q)/u と書けば K=νx²+νy²+λ²νz²、Kn=νy² である。

最終 active ordering は (t,γ,k,n)。以下は V2 から変更しない。

\[
c=1-t^2,\quad A=1+t^2+c\gamma,
\]
\[
F=A(1-n)-(2A-\gamma c)n(1-2K)^2,
\]
\[
B=KF,\quad \mathcal W=\frac{\gamma}{K^2A^2},\quad
\mathcal P:=\mathcal WB=\frac{\gamma F}{KA^2}.
\]

V3 で積分下界に使うのは **合成対象 P の constrained lower bound** である。B と W の下界も同じ証明機構で記録するが、別々の extrema を掛けて P の下界を作らない。これにより γ と signed kernel の相関を certificate identity 内に保持する。これは B⁺−B⁻ decomposition ではない。

## 3. Full lifted physical equations

d=1+τ²、r=1−τ²、z0=2τ と置く。physical variables 5個と auxiliaries (a,u,w,k,γ,n) の計11変数について、次の6 equalities は有理係数多項式である。

\[
\begin{aligned}
E_a&=a^2+\mu^2-1=0,\\
E_w&=w^2-\lambda^2-(1-\lambda^2)\mu^2=0,\\
E_S&=du^2-2(d-ra\epsilon s-z_0\mu)=0,\\
E_K&=d^2u^2(K-1)+(1-\lambda^2)(d\mu-z_0)^2=0,\\
E_n&=u^2Kn-(1-\mu^2)(1-s^2)=0,\\
E_\gamma&=2wk\gamma-\lambda u=0.
\end{aligned}
\]

physical box bounds、a,u≥0、w,k>0、0≤γ,n≤1 を併用する。d>0 による denominator clearing のみであり、D_min は導入しない。

S>0 では、正根の符号を固定したこれらの式は上記の physical mapping と同値である。一般点 a,u>0 では a,w,u,k,n,γ をこの順に決定でき、6等式は generically independent。a=0/contact での Jacobian degeneracy を無視しない。u=0 では k,n の余分な fiber が残るため、lifted set 全体を物理写像の exact graph と呼ばない。

この full lift は geometry audit 用である。11変数の Bernstein optimization は行わず、次節の含意を使って4変数へ外包する。

## 4. Joint identities と低次数必要条件

\[
T:=\gamma^2K
\]

と置く。物理集合上で

\[
4w^2T=\lambda^2S,\tag{J0}
\]
\[
4w^2T(1-K)=\lambda^2(1-\lambda^2)\Delta^2,\tag{Jz}
\]
\[
4w^2TKn=\lambda^2Y^2.\tag{Jy}
\]

Jz は J0 と SK=S−(1−λ²)Δ² から、Jy は J0 と SKn=Y² から従う。添付スクリプトはそれらの polynomial ideal combination を exact difference=0 で検査する。これは数値点での一致検査ではない。

方向に関する identity は

\[
K\{1-(1-\lambda^2)n\}-\lambda^2
=(1-\lambda^2)\nu_x^2\ge0.\tag{D1}
\]

さらに Q=(R,0,Z)、R²+Z²=1、Q·ν=−u/2 より

\[
1-Kn-\frac{w^2}{\lambda^2}T
=(Z\nu_x-R\nu_z)^2\ge0.\tag{D2}
\]

これは2次元 Gram identity と u²/4=(w²/λ²)T による。特に、k,n,γ の独立区間では失われる joint restriction を含む。

## 5. 全枝共通の8制約生成規則

各 branch の V2 fixed enclosure trace を変更せず使用する。λ∈[l,h] とし、その trace から

\[
S\in[S_-,S_+],\quad \Delta^2\in[z_-,z_+],\quad
Y^2\in[y_-,y_+],\quad w^2\in[v_-,v_+]
\]

を取得する。v± は **raw exact w2 interval** であり、丸めた w interval を再度二乗して置き換えない。v_->0。全下端は非負である。

\[
\alpha=\max\{1,v_-/h^2\},
\]
\[
L_T=\frac{l^2S_-}{4v_+},\quad U_T=\frac{h^2S_+}{4v_-},
\]
\[
L_Z=\frac{l^2(1-l^2)z_-}{4v_+},\quad
U_Z=\frac{h^2(1-h^2)z_+}{4v_-},
\]
\[
L_Y=\frac{l^2y_-}{4v_+},\quad U_Y=\frac{h^2y_+}{4v_-}.
\]

ここで λ²≤(93/200)²<1/2 なので λ²(1−λ²) は帯上で増加する。各係数は事前固定された式から生成する有理数である。

使用する joint inequalities は以下の8本で固定する。

\[
\begin{aligned}
Q_1&=K\{1-(1-l^2)n\}-l^2\ge0,\\
Q_2&=1-Kn-\alpha T\ge0,\\
Q_3&=T-L_T\ge0, &Q_4&=U_T-T\ge0,\\
Q_5&=T(1-K)-L_Z\ge0, &Q_6&=U_Z-T(1-K)\ge0,\\
Q_7&=TKn-L_Y\ge0, &Q_8&=U_Y-TKn\ge0.
\end{aligned}
\]

Q1 の正当性：D1 左辺の λ² に関する微分は Kn−1≤0。λ² を l² に下げると左辺は増加する。Q2 の正当性：α≤w²/λ² かつ T≥0 なので D2 より従う。Q3–Q8 は J0/Jz/Jy と上記係数の区間包含から従う。

この規則は1024枝すべて共通。coefficient の符号・最悪箱・production 結果による式選択、制約削除、追加制約、次数変更はしない。ある制約が特定枝で冗長でも8本を保持し、必要ならその multiplier が0になる。

### 制約の分類

|制約|役割|冗長性・独立性|
|---|---|---|
|Q1|k,n の方向相関、V1/V2 の非物理方向の排除|full lift の帰結。reduced rectangle では非冗長になり得る|
|Q2|γ,k,n の Gram 相関|Q1 だけからは従わない|
|Q3,Q4|γ²k² と box の chord-length 情報|joint moment の上下界|
|Q5,Q6|γ²k²(1−k²) と Δ²|軸方向の情報を保持|
|Q7,Q8|γ²k⁴n と Y²|横方向の情報を保持|

例えば l=2/5, α=1 の全球範囲で、(k,n,γ)=(2/5,1/2,0) は Q2>0 だが Q1<0。一方 (1,1,1) は Q1=0 だが Q2<0。従って最初の2本は互いの代用にならない。この検査は constraint algebra の論理例であり physical diagnostic sample ではない。全8本の各枝での最小独立性は主張しない。

## 6. Reduced semialgebraic domain と containment

V2 fixed recipe が返す active rectangle を A_j と書く。j は physical box と ε を含む branch ID。

\[
\mathcal S_j=A_j\cap\{Q_1\ge0,\ldots,Q_8\ge0\}.
\]

\[
\text{physical image}_j\subseteq\mathcal S_j\subseteq A_j.
\]

A_j は単に係数を Bernstein 座標へ写すための containing rectangle であり、最終下界は制約付き集合 S_j 上に証明する。A_j 上だけの extrema を V3 結果として採用しない。

消去後の active variables は (t,γ,k,n) の4個、equalities は0本、joint inequalities は8本、加えて4座標の上下界がある。枝ごとの物理変数は Q の有理係数と A_j の構成にだけ残る。

### Moving diagonal

k≥λ≥2/5、w≥λ>0 なので γ=0 ⇔ u=0。contact を含む physical box では S_-=z_-=y_-=0 であり、Q3/Q5/Q7 の下端と矛盾しない。γ=0 では P=0、W=0。k,n の極限方向は一意でなくても、k の正下界により product は一様に0へ延長される。

contact fiber で追加の非物理 k,n を外包しても product=0 を変えない。ただし Q1/Q2 と active bounds はその fiber にも課す。contact を含む branch に strictly-positive pointwise lower bound を強制してはならない。負または0の branch bound を許容して全積分を合算する。

## 7. Retained / relaxed correlation ledger

|情報|V3 の扱い|
|---|---|
|V=k²n≤k²|n∈[0,1] により保持|
|γ≤1|active domain により保持|
|V2 の non-diagonal γ_min>0|fixed enclosure をそのまま保持|
|Δ² 由来の n upper bound|V2 fixed enclosure をそのまま保持|
|directional (k,n) condition|Q1 で保持|
|Gram (γ,k,n) condition|Q2 で保持|
|S,Δ²,Y² と γ,k,n の moment relations|Q3–Q8 で両側に保持|
|同一 τ,μ,s,λ から生じる全 joint relations|完全には保持しない|
|moment constants 間の同時 attainability|独立上下界へ外包している|
|X の枝依存符号、Q·ν の向きの詳細|full lift に存在するが reduced set に全ては残らない|
|k,n の contact 方向 fiber|安全な closed outer fiber を許容|

したがって、V3 でも残存緩和で失敗する可能性はある。8制約を「完全な物理射影」と呼ぶことも、V2 の violation counts が全て解消すると事前に断定することもしない。

## 8. 選択する certificate mechanism

各 A_j を x∈[0,1]^4 へ affine map する。幅0の座標は定数代入し、formal Bernstein coordinate は残して degree elevation する。幅0で除算しない。

3対象の順序を固定する。

|対象|N|D|用途|
|---|---|---|---|
|B|KF|1|signed kernel の constrained lower bound|
|W|γ|K²A²|weight の constrained lower bound|
|P=WB|γF|KA²|**唯一の積分用 lower bound**|

全 denominator は正である。

\[
D_B=1,\quad D_W\ge16/625,\quad D_P\ge4/25.
\]

A=(1+γ)+(1−γ)t²≥1、k≥2/5 から従う。距離 D の正下界は使わない。各 branch で denominator Bernstein coefficients の strictly-positive condition も検査する。A の上の非負積表示と degree elevation によって、この coefficient positivity は理論上も確保できる。

multiplier tensor degree と residual tensor degree を、結果に先立ち固定する。

\[
m=(0,2,2,1),\qquad r=(4,4,6,2).
\]

β_{α,m}(x) を tensor Bernstein basis とし、

\[
\sigma_q(x)=\sum_{\alpha\le m}a_{q\alpha}\beta_{\alpha,m}(x),\quad a_{q\alpha}\ge0.
\]

求める証明書は

\[
\boxed{N-\ell D=\sum_{i\le r}b_i\beta_{i,r}+\sum_{q=1}^8\sigma_qQ_q,\qquad b_i,a_{q\alpha}\ge0.}\tag{C}
\]

残差・multipliers は全 rectangle 上で非負、Q は S_j 上で非負である。従って N/D≥ell が S_j 全体、moving diagonal、closed physical boundaries を含めて成立する。

この形式は completeness theorem を必要としない sufficient certificate である。固定次数で真の最小値まで達する保証はなく、非正の最適値は数学的反例ではない。

選定理由：有理係数恒等式のみで exactness を検査でき、正分母を保持し、γ=0 を除外せず、fixed box と両立する。独立 checker は LP solver を実行せずに証明書を検査できる。SOS matrix や floating-point PSD 判定は不要。次数は branch ごとに変えない。

## 9. 係数変換と exact LP の完全仕様

monomial x^a を degree r の Bernstein 表示へ変換する係数は、i≥a のとき

\[
\prod_{v=1}^4\frac{\binom{i_v}{a_v}}{\binom{r_v}{a_v}},
\]

その他は0。affine substitution、polynomial product、degree elevation はすべて有理数演算とする。

N,D の degree-r coefficients を n_i,d_i、β_{α,m}Q_q の degree-r coefficients を h_{i,qα} とする。d_i>0。

\[
\ell_0=\min_i n_i/d_i,\quad b_i^0=n_i-\ell_0d_i\ge0.
\]

この ell0 は LP の初期 feasible certificate だけであり、joint constraints を外して production を終える別方式ではない。全8制約を含む次のLPを解く。

\[
\begin{array}{ll}
\text{maximize}& z\\
\text{subject to}&d_i z+\sum_{q,\alpha}h_{i,q\alpha}a_{q\alpha}\le b_i^0\quad(525\text{ rows}),\\
&z\ge0,\quad a_{q\alpha}\ge0,
\end{array}\tag{LP}
\]

ell=ell0+z、b_i=b_i^0−d_i z−Σh a とする。初期解 z=a=0 は常に feasible。physical set が非空で D>0 なので任意の certificate ell は physical point の N/D 以下であり、目的は有界。有限次元の rational LP なので exact optimum を証明できる形式である。

producer は exact rational revised simplex と Bland rule を使用する。変数順は z、q=1,…,8 内の α lexicographic、その後 residual slacks を lexicographic。入基・退基の同率はこの固定番号で処理する。初期 basis は residual slacks。floating point solution を判定根拠にしない。

独立 optimality check 用に dual y_i を保存する。

\[
y_i\ge0,\quad\sum_i d_i y_i\ge1,\quad
\sum_i h_{i,q\alpha}y_i\ge0\quad(\forall q,\alpha),
\]
\[
\boxed{z=\sum_i b_i^0y_i.}
\]

primal/dual feasible とこの equality により、固定 certificate cone での最適性が exact に確認できる。これは物理集合上の真の最小値との一致を意味しない。

resource policy candidate：1 LP あたり最大20,000 pivots。これを超えた場合は RESOURCE_LIMIT / INCOMPLETE とし、次数・分割・別方式へ自動移行しない。20,000 は数学的終了保証や所要時間の予測ではなく事前固定の運用上限。上限到達を METHOD FAIL や物理反例として扱わない。この resource policy も chat/Judge の architecture 審査対象とする。

## 10. Exact complexity ledger

ordering はすべて (t,γ,k,n)。

|polynomial|tensor multidegree|
|---|---|
|Q1|(0,0,2,1)|
|Q2|(0,2,2,1)|
|Q3,Q4|(0,2,2,0)|
|Q5,Q6|(0,2,4,0)|
|Q7,Q8|(0,2,4,1)|
|B numerator|(2,1,6,1)|
|B denominator|(0,0,0,0)|
|W numerator|(0,1,0,0)|
|W denominator|(4,2,4,0)|
|P numerator|(2,2,4,1)|
|P denominator|(4,2,2,0)|
|each multiplier|(0,2,2,1)|
|common residual/elevated identity|(4,4,6,2)|

deg(σQ)≤(0,4,6,2) であり、common residual degree に収まる。

|項目|固定サイズ|
|---|---:|
|full lifted variables / equalities|11 / 6|
|optimization variables / reduced equalities|4 / 0|
|joint inequalities|8|
|multiplier coefficients each|1×3×3×2=18|
|nonnegative multiplier unknowns|144|
|residual coefficients|5×5×7×3=525|
|LP nonslack variables|145|
|LP rows / slacks|525 / 525|
|LPs per branch / all branches|3 / 3072|
|certificate rationals per target, without dual|144+525+1=670|
|certificate rationals per target, with dual|1195|
|certificate rationals per branch, with dual|3585|
|all1024 certificate rationals, with dual|3,671,040|
|dense multiplier matrix H entries per branch|525×144=75,600|
|H unique entries using t-independence|105×144=15,120|

最後の certificate counts は box metadata、input coefficients、denominator arrays、hashes、LP basis/pivot logs を含まない。N,D arrays は3対象×2×525=3150係数。H は同じ branch の3LPで共有する。

**Complexity: HIGH for producer, structured/polynomial for checker.** 1024枝を一括 dense memory に置かない。branch 単位で enclosure→constraints→H を構成し、3LPを順に処理して certificate を streaming 保存する。checker も branch 単位で再構成する。H の t-independent rows は反復保持を避ける。slack identity block は implicit とする。

有理数 bit-size は production 前には観測していない。32-bit root witnesses があっても、LP解の分母が32bitに収まるとは限らない。行ごとに denominator LCM を払った整数行列/RHS の絶対値最大を M≥1 とする。basic nonslack variables の数 p≤145 に対する Cramer determinant は p!M^p 以下なので、numerator/denominator に O(p log M+log(p!)) bits の上界を与えられる（ell0 の加算分は別途加える）。これは保守的な算術上界であり実測値ではない。producer は最大 input/solution bit-size と pivots を記録する。

## 11. 固定 physical partition と積分・parameter aggregation

\[
\tau_i=7/8+i/32\ (i=0,\ldots,4),\quad
\mu_j=-1+j/2\ (j=0,\ldots,4),
\]
\[
s_h=h/2\ (h=0,1,2),\quad
\lambda_a=2/5+13a/800\ (a=0,\ldots,4),\quad
t_b=b/4\ (b=0,\ldots,4).
\]

512 folded physical boxes / 1024 branches を変更しない。追加 subdivision、worst-box-only refinement、result-driven multiplier degree を使わない。

P の branch certificate lower bounds を ell+、ell− とする。measure は ds/(π sqrt(1−s²)) であり、folded s の2セルの mass は1/6、1/3。μ幅1/2、t幅1/4を掛け、

\[
L_{ijhab}=\begin{cases}(\ell_++\ell_-)/48&h=0,\\(\ell_++\ell_-)/24&h=1.\end{cases}
\]

\[
S_{ia}=\sum_{j,h,b}L_{ijhab},\qquad m_0=\min_{i,a}S_{ia}.
\]

τ,λ は一様 parameters であり積分しない。16 parameter sums を足してはいけない。全 cell は closed endpoints を含む。s に通常の Lebesgue Bernstein integral 1/(n+1) を流用しない。raw s-parity を仮定せず、両 ε branch を必ず含める。

## 12. Producer certificate object

branch record は少なくとも以下を含む。

1. physical/parameter-cell ID、ε、exact endpoints、partition/source pins。
2. unchanged V2 enclosure trace 全体、32-bit root witnesses、active intervals。
3. S±,z±,y±,v± と l,h、α,LT,UT,LZ,UZ,LY,UY の生成 trace。
4. Q1–Q8 の exact polynomial representation、active affine maps。
5. 各 N,D、degree、elevated coefficients、positive denominator minimum。
6. H の完全再現可能な exact representation と hash。hashだけを証明にしない。
7. 各 target の ell0、z、ell、144 multiplier coefficients、525 residual coefficients。
8. 525 dual coefficients、primal/dual feasibility、exact objective equality。
9. fixed solver ordering、basis、pivot count、resource status、max rational bit-size。
10. P の branch lower、paired physical-cell contribution、parameter index。

16 exact S_ia、m0、argmin、全 completeness/error flags を別の最終 manifest に保存する。rationals は reduced numerator/positive-denominator pair とし、小数は表示用のみ。

## 13. Independent checker contract

checker は producer の PASS/FAIL、保存 extrema、hash一致のみを信用しない。独立実装で以下を再構成する。

1. source/partition identity、全1024枝の重複・欠落・closed cover。
2. V2 fixed enclosure containment、root rounding の整数 witness inequalities。
3. raw w² などから全8制約係数を再生成し、幾何学的 containment derivation と一致確認。
4. target identities、affine substitutions、Bernstein transformation / product / elevation。
5. denominator coefficients >0。
6. a≥0,b≥0 と certificate (C) の各係数の差=0。
7. dual feasibility と primal/dual objective equality。
8. P lower の使用、arcsine factors、512 paired-cell values、16 sums、exact min。

独立 checker に simplex solver は不要。証明書 identity と符号の exact recomputation が中心である。架空の positive denominator、負の multiplier、identity mismatch、box欠落は CHECK_ERROR。certificate cone の非正最適値と区別する。

## 14. 成功・失敗・未完了の区別

全 production が完了し checker が受理し、m0>0 なら FT_q SIGNED CERTIFICATE CANDIDATE V3 として chat recomputation / Judge へ渡す。FT_q はその時点でも PARTIAL。

m0≤0 なら METHOD FAIL / MATHEMATICAL CLAIM NOT REFUTED。追加 subdivision、multiplier degree変更、B⁺−B⁻ 同時導入へ自動移行しない。

RESOURCE_LIMIT は INCOMPLETE であって METHOD FAIL ではない。CHECK_ERROR は実装・証明書エラーであって mathematical failure ではない。

失敗時には branch ごとに constraints、active multiplier、certificate gain z、dual support、残存 γ/k/n correlation の可能性を記録する。negative constrained lower bound のみを physical B<0 の証拠にしてはならない。

V3 は V2 の Wmax Bmin 合成から full-product certificate へ変わる。この差と joint-constraint 効果を混同しないため、同じ P に対する初期 unconstrained ratio ell0 と constrained optimum ell の差 z≥0 を全枝で記録する。これは同一対象の certificate improvement の exact comparison であり、物理最小値の変化ではない。V2 との差全体を joint constraints だけの効果と呼ばない。

## 15. 今回の到達点と未確認事項

**確認済み：** joint identity の exact polynomial reductions、Gram identity、制約導出、containment、positive denominator、固定degreeで certificate identity が表現可能であること、LP初期feasibility、coefficient counts。添付 checks は exact arithmetic で完了。

**未確認：** 各枝の LP optimum、非零 multiplier の実際の効き方、全16 parameter sums、m0の符号、production runtime/実際のbit-size、20,000pivot以内での終了。これらを READY 判定へ紛れ込ませない。

**推奨次工程：** 本 V3 architecture と callable specification を chat が監査し、Judge 承認後に fixed exact producer と独立 checker を実装する。今回 production は開始しない。

**Final verdict: FT_q V3 joint-constraint architecture — READY_FOR_CODEX.**

**FT_q: PARTIAL / whole-face m0: UNPROVED / L3: FREEZE HOLD / L1: PAUSED / D-P2: NOT_CERTIFIED.**

---

## Appendix — reproducible architecture-only sources and results

以下に本提出の実際の source bytes と result を同梱する。別ファイルへ取り出す場合は各 code block の本文を UTF-8 で保存する。これらは production 実装ではない。


### ftq_v3_joint_constraint_spec.py

SHA-256: `d17cd115ee1da13a1470cf5afb17414db158b0f1cf447847dbc27ec0054b153a`

```python
"""Frozen-candidate V3 constraints; callable specification, no production loop.
Receives the unchanged V2 geometry trace and physical lambda interval.
"""
from fractions import Fraction as F
from ftq_algebra import var

MULTIPLIER_DEGREE=(0,2,2,1)
RESIDUAL_DEGREE=(4,4,6,2)
TARGET_ORDER=('B','physical_weight','physical_product')

def constraints(trace,lambda_bounds):
    lo,hi=map(F,lambda_bounds)
    assert F(2,5)<=lo<=hi<=F(93,200)
    Slo,Shi=map(F,trace['S'])
    dzlo,dzhi=map(F,trace['delta2'])
    ylo,yhi=map(F,trace['y2'])
    vlo,vhi=map(F,trace['w2'])
    assert vlo>0 and min(Slo,dzlo,ylo)>=0
    alpha=max(F(1),vlo/(hi*hi))
    LT=lo*lo*Slo/(4*vhi);UT=hi*hi*Shi/(4*vlo)
    LZ=lo*lo*(1-lo*lo)*dzlo/(4*vhi)
    UZ=hi*hi*(1-hi*hi)*dzhi/(4*vlo)
    LY=lo*lo*ylo/(4*vhi);UY=hi*hi*yhi/(4*vlo)
    t,g,k,n=map(var,range(4));K=k*k;T=g*g*K
    q=[K*(1-(1-lo*lo)*n)-lo*lo,
       1-K*n-alpha*T,
       T-LT,UT-T,
       T*(1-K)-LZ,UZ-T*(1-K),
       T*K*n-LY,UY-T*K*n]
    constants={'lambda_lower_squared':lo*lo,'alpha':alpha,'LT':LT,'UT':UT,'LZ':LZ,'UZ':UZ,'LY':LY,'UY':UY}
    return q,constants

def targets():
    t,g,k,n=map(var,range(4));c=1-t*t;A=1+t*t+c*g
    f=A*(1-n)-(2*A-g*c)*n*(1-2*k*k)**2
    return [(k*k*f,k**0),(g,k**4*A*A),(g*f,k*k*A*A)]
```


### ftq_v3_architecture_checks.py

SHA-256: `68c96f1c5c35bd4e7e8c541190a57cebc98d43d538dfc092d18d841996770c08`

```python
"""Exact V3 architecture checks only. No LP solves or production boxes."""
from fractions import Fraction as Q
from math import prod
import json
from ftq_algebra import var
t,g,k,n,lam,w,S,Z2,Y,u=map(var,range(10))
K=k*k
ET=4*w*w*g*g*K-lam*lam*S
EJ=S*K-S+(1-lam*lam)*Z2
EN=S*K*n-Y
Ez=4*w*w*g*g*K*(1-K)-lam*lam*(1-lam*lam)*Z2
Ey=4*w*w*g*g*K*K*n-lam*lam*Y
assert not(Ez-((1-K)*ET-lam*lam*EJ))
assert not(Ey-(K*n*ET+lam*lam*EN))
EG=2*w*k*g-lam*u
assert not(ET-(2*w*k*g+lam*u)*EG-lam*lam*(u*u-S))
Qdir=K*(1-(1-lam*lam)*n)-lam*lam
assert not(S*Qdir-(1-lam*lam)*(S-Z2-Y)-(EJ-(1-lam*lam)*EN))
R,Z,vx,vz=map(var,range(4))
assert not((R*R+Z*Z)*(vx*vx+vz*vz)-(R*vx+Z*vz)**2-(Z*vx-R*vz)**2)
# Back to active variables t,g,k,n. Representative rational coefficients do not
# depend on any diagnostic; they only verify the symbolic degree envelopes.
t,g,k,n=map(var,range(4));K=k*k;T=g*g*K
alpha=Q(1);ll2=Q(4,25)
qs=[K*(1-(1-ll2)*n)-ll2,1-K*n-alpha*T,T,T*-1+1,T*(1-K),1-T*(1-K),T*K*n,1-T*K*n]
def degree(p):return tuple(max(idx[j] for idx in p) for j in range(4))
qd=[degree(p) for p in qs]
expected=[(0,0,2,1),(0,2,2,1),(0,2,2,0),(0,2,2,0),(0,2,4,0),(0,2,4,0),(0,2,4,1),(0,2,4,1)]
assert qd==expected
beta=(0,2,2,1);residual=(4,4,6,2)
c=1-t*t;A=1+t*t+c*g;f=A*(1-n)-(2*A-g*c)*n*(1-2*K)**2
targets=[(K*f,k**0),(g,K*K*A*A),(g*f,K*A*A)]
for p,d in targets:
    assert all(x<=y for x,y in zip(degree(p),residual))
    assert all(x<=y for x,y in zip(degree(d),residual))
assert all(all(x+b<=r for x,b,r in zip(q,beta,residual)) for q in qd)
def vq1(k,n):return k*k*(1-Q(21,25)*n)-Q(4,25)
def vq2(k,n,g):return 1-k*k*(n+g*g)
assert vq1(Q(2,5),Q(1,2))<0<vq2(Q(2,5),Q(1,2),0)
assert vq1(1,1)==0 and vq2(1,1,1)<0
nb=prod(x+1 for x in beta);nr=prod(x+1 for x in residual)
data={'mode':'ARCHITECTURE ONLY / NO PRODUCTION / NO SOLVER RUN',
'exact_identity_checks':'difference=0: ET, Ez, Ey, directional identity, Gram identity',
'joint_inequality_count':8,'reduced_equality_count':0,'lifted_equality_count':6,
'active_order':['t','gamma','k','n'],'constraint_tensor_degrees':qd,
'multiplier_tensor_degree':beta,'coefficients_per_multiplier':nb,'multiplier_count':8,
'nonnegative_multiplier_unknowns':8*nb,'LP_non_slack_variables':8*nb+1,
'residual_tensor_degree':residual,'residual_coefficients':nr,
'LP_inequalities':nr,'LPs_per_branch':3,'LPs_for_1024_branches':3072,
'target_certificate_rationals_without_dual':8*nb+nr+1,
'target_certificate_rationals_with_dual':8*nb+2*nr+1,
'branch_certificate_rationals_with_dual':3*(8*nb+2*nr+1),
'all_branches_certificate_rationals_with_dual':1024*3*(8*nb+2*nr+1),
'H_dense_entries_per_branch':nr*8*nb,
'H_unique_entries_using_t_independence':prod(x+1 for x in residual[1:])*8*nb,
'physical_projection_equality_claim':False,
'certificate_mechanism':'nonnegative Bernstein polynomial multipliers + exact Bernstein residual + exact LP dual',
'whole_face_m0':'UNPROVED'}
print(json.dumps(data,indent=2))
open('ftq_v3_architecture_checks_result.json','w').write(json.dumps(data,indent=2))
```


### ftq_v3_architecture_checks_result.json

SHA-256: `2ed94e790aa68da72a0b54f0982dcc548302a19b5a0205ced84b0bf8216b3e44`

```json
{
  "mode": "ARCHITECTURE ONLY / NO PRODUCTION / NO SOLVER RUN",
  "exact_identity_checks": "difference=0: ET, Ez, Ey, directional identity, Gram identity",
  "joint_inequality_count": 8,
  "reduced_equality_count": 0,
  "lifted_equality_count": 6,
  "active_order": [
    "t",
    "gamma",
    "k",
    "n"
  ],
  "constraint_tensor_degrees": [
    [
      0,
      0,
      2,
      1
    ],
    [
      0,
      2,
      2,
      1
    ],
    [
      0,
      2,
      2,
      0
    ],
    [
      0,
      2,
      2,
      0
    ],
    [
      0,
      2,
      4,
      0
    ],
    [
      0,
      2,
      4,
      0
    ],
    [
      0,
      2,
      4,
      1
    ],
    [
      0,
      2,
      4,
      1
    ]
  ],
  "multiplier_tensor_degree": [
    0,
    2,
    2,
    1
  ],
  "coefficients_per_multiplier": 18,
  "multiplier_count": 8,
  "nonnegative_multiplier_unknowns": 144,
  "LP_non_slack_variables": 145,
  "residual_tensor_degree": [
    4,
    4,
    6,
    2
  ],
  "residual_coefficients": 525,
  "LP_inequalities": 525,
  "LPs_per_branch": 3,
  "LPs_for_1024_branches": 3072,
  "target_certificate_rationals_without_dual": 670,
  "target_certificate_rationals_with_dual": 1195,
  "branch_certificate_rationals_with_dual": 3585,
  "all_branches_certificate_rationals_with_dual": 3671040,
  "H_dense_entries_per_branch": 75600,
  "H_unique_entries_using_t_independence": 15120,
  "physical_projection_equality_claim": false,
  "certificate_mechanism": "nonnegative Bernstein polynomial multipliers + exact Bernstein residual + exact LP dual",
  "whole_face_m0": "UNPROVED"
}
```


### ftq_algebra.py

SHA-256: `e24ff38dae62d7457aedc65ab46e528c8a737c5887e3ff037b098c4fdb6ed30b`

```python
"""Exact polynomial algebra and analytic beta-series bounds; no parameter sampling."""
from fractions import Fraction as F
from math import comb,ceil
import json
from pathlib import Path
NVAR=12 # x,z,b,mu,lambda,q; Laurent exponents allowed
class P(dict):
 def __add__(a,b):
  if not isinstance(b,P): b=P({(0,)*NVAR:F(b)})
  d=P(a)
  for k,v in b.items(): d[k]=d.get(k,F(0))+v
  return P({k:v for k,v in d.items() if v})
 __radd__=__add__
 def __neg__(a):return P({k:-v for k,v in a.items()})
 def __sub__(a,b):return a+-b
 def __rsub__(a,b):return -a+b
 def __mul__(a,b):
  if not isinstance(b,P):return P({k:v*F(b) for k,v in a.items() if v*F(b)})
  d=P()
  for k,v in a.items():
   for l,w in b.items():
    h=tuple(i+j for i,j in zip(k,l));d[h]=d.get(h,F(0))+v*w
  return P({k:v for k,v in d.items() if v})
 __rmul__=__mul__
 def __truediv__(a,b):return a*F(1,b)
 def __pow__(a,n):
  if n<0:
   assert len(a)==1
   k,v=next(iter(a.items()));return P({tuple(i*n for i in k):v**n})
  out=P({(0,)*NVAR:F(1)})
  for _ in range(n):out=out*a
  return out
def var(i):return P({tuple(int(j==i) for j in range(NVAR)):F(1)})
```


### ftq_v2_fixed_enclosure.py

SHA-256: `c83709482525da48fe7fb28fdd15d5dd7f999909a51be855e808847d6f1f1b1f`

```python
"""Architecture reference recipe; no production, scan, or coefficient evaluation.

Input physical box (tau,mu,s,lambda,t), folded s in [0,1], epsilon +/-1.
Output active box (t,gamma,k,nu_hat) and exact enclosure trace.
"""
from fractions import Fraction as F
from math import isqrt

def I(a,b=None):return (F(a),F(a if b is None else b))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def sub(a,b):return (a[0]-b[1],a[1]-b[0])
def mul(a,b):
    z=[x*y for x in a for y in b];return (min(z),max(z))
def div(a,b):
    assert b[0]>0
    return mul(a,(1/b[1],1/b[0]))
def sq(a):return (F(0) if a[0]<=0<=a[1] else min(x*x for x in a),max(x*x for x in a))
def cut(a,b):
    out=(max(a[0],b[0]),min(a[1],b[1]));assert out[0]<=out[1];return out
def root(a):
    assert a[0]>=0
    def ep(x,up):
        n=isqrt((x.numerator<<64)//x.denominator)
        if up and F(n*n,1<<64)!=x:n+=1
        return F(n,1<<32)
    ans=(ep(a[0],False),ep(a[1],True))
    assert ans[0]**2<=a[0] and ans[1]**2>=a[1]
    return ans

def enclosure(bounds,epsilon):
    assert epsilon in (1,-1)
    tau,mu,s,lam,t=tuple(tuple(map(F,x)) for x in bounds)
    R=lambda x:(1-x*x)/(1+x*x)
    Z=lambda x:2*x/(1+x*x)
    rr=(R(tau[1]),R(tau[0]));zz=(Z(tau[0]),Z(tau[1]))
    mu2=sq(mu);a2=sub(I(1),mu2);aa=cut(root(a2),I(0,1))
    se=mul(I(epsilon),s)
    X=sub(mul(aa,se),rr);x2=sq(X)
    y2=mul(a2,sub(I(1),sq(s)))
    delta=sub(mu,zz);d2=sq(delta);lam2=sq(lam)
    Sdot=mul(I(2),sub(sub(I(1),mul(mul(rr,aa),se)),mul(zz,mu)))
    Ssos=add(add(x2,y2),d2)
    S=cut(cut(Sdot,Ssos),I(0,4))
    # Cauchy geometry: S>=R^2(1-s^2); for epsilon=-1, S>=2(1-Z).
    transverse=rr[0]**2*(1-s[1]**2)
    negative_cosine=2*(1-zz[1]) if epsilon==-1 else F(0)
    S=cut(S,(max(S[0],transverse,negative_cosine),F(4)))
    assert S[1]>0
    zeta_lo=d2[0]/S[1]
    zeta_hi=min(F(1),d2[1]/S[0]) if S[0]>0 else F(1)
    zeta=cut((zeta_lo,zeta_hi),I(0,1))
    J=(1-(1-lam[0]**2)*zeta[1],1-(1-lam[1]**2)*zeta[0])
    k=cut(root(J),(lam[0],F(1)))
    e2=add(x2,mul(lam2,d2))
    # Shared y2 kept in numerator and denominator: monotonic y/(y+e).
    dl=y2[0]+e2[1];dh=y2[1]+e2[0]
    nlo=y2[0]/dl if dl>0 else F(0)
    nhi=y2[1]/dh if dh>0 else F(1)
    directional=(1-zeta[0])/(1-(1-lam[0]**2)*zeta[0])
    nhat=cut((nlo,min(nhi,directional)),I(0,1))
    w2=(lam[0]**2+(1-lam[0]**2)*mu2[0],lam[1]**2+(1-lam[1]**2)*mu2[1])
    w=cut(root(w2),(lam[0],F(1)));u=cut(root(S),I(0,2))
    gamma_raw=div(mul(lam,u),mul(I(2),mul(w,k)))
    # sqrt(S)>=S/2 on [0,4], w*k<=1: strict positivity cannot be lost to root rounding.
    rescue=lam[0]*S[0]/4
    gamma=cut((max(gamma_raw[0],rescue),gamma_raw[1]),I(0,1))
    trace=dict(R=rr,Z=zz,mu2=mu2,a2=a2,a=aa,X=X,x2=x2,y2=y2,delta=delta,delta2=d2,S_dot=Sdot,S_sos=Ssos,S=S,transverse_bound=transverse,negative_cosine_bound=negative_cosine,zeta=zeta,J=J,k=k,e2=e2,nu_lower_ratio=nlo,nu_upper_ratio=nhi,nu_directional_upper=directional,nu_hat=nhat,w2=w2,w=w,u=u,gamma_raw=gamma_raw,gamma_rescue=rescue,gamma=gamma)
    return (t,gamma,k,nhat),trace
```
