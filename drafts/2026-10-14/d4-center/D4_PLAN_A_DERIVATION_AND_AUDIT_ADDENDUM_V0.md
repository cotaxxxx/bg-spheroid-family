# D4 案A：独立導出と監査追補 V0

状態：DRAFT / NOT FROZEN / EXECUTION PROHIBITED / CHAT AUDIT REQUESTED。
方式判定：METHOD_UNDETERMINED。紙上補題案であり、D-P2 discharge・正式証明書・Judge裁定ではない。

## 1. 結果と未完了事項

Claude Code の4階式を参照せず、P1密度から中心の4階同次項を導出した。導出本文とSymPyスクリプトを、照合先の取得を始める前に固定した。さらに、中心係数とは別に、Taylor剰余に必要な掃引領域全体の上界

\[
M_{40}=M_{22}=25600
\]

を紙上で導出した。この粗い上界でも、中心部分

\[
0\le r\le\frac1{128},\quad 0\le\tau\le\frac18,\quad
\frac{119}{200}\le\lambda\le\frac{33}{50}
\]

について

\[
H\ge\frac{5629}{155520}>0
\]

を得る補題案になる。旧定数1547/4860だけを使用しており、強い中心下界の照合結果に依存しない。残る r∈[1/128,1/8] は未解決である。

|項目|状態|
|---|---|
|独立4階同次展開|導出済み・監査待ち。付録A参照|
|掃引領域の明示的4階微分上界|紙上導出済み・監査待ち|
|Claude Code 4階式との一致|UNRESOLVED：照合先本文を取得できず|
|SymPy差=0|UNEXECUTED：利用できる確認済みPythonにSymPyなし|
|07db380e の歴史的独立性|UNVERIFIED：完全参照・提出記録・アクセス記録未取得|
|74f0608e… のevidence pin|PENDING_SOURCE_IDENTITY：本文と完全識別子未取得|
|repoへの1 commit|未実施：照合・pinが揃ってからという条件を維持|

## 2. 中心係数と剰余上界を区別する

中心の E_{ρρρρ}(0,0;λ), E_{ρρzz}(0,0;λ) と、近傍全体の絶対値上界 M40,M22 は異なる。中心式の一致だけでは、中心外のTaylor剰余を保証しない。

今回のM40,M22は、λ∈[119/200,33/50]かつ |diag(1,1,λ)^{-1}p|≤1/8 の全掃引領域での上界である。φ平均による相殺を使わず、距離下界と方向微分から独立に評価した。中心の4階式の照合が未完でも、この上界の紙上監査を別に行える。

H=∫₀¹E_{ρρ}(sρ,z;λ)ds と、ρ,zそれぞれの偶性から、積分型剰余により厳密に

\[
H(\rho,z;\lambda)\ge H(0,0;\lambda)
-\frac{M_{40}}6\rho^2-\frac{M_{22}}2z^2
\]

となる。これは形式的なO(r⁴)を定量化せずに使う議論ではない。

座標式 ρ=r(1−τ²)/(1+τ²), z=λr·2τ/(1+τ²) より、ρ≤r、z≤(33/50)(16/65)r<r/6。したがって r≤1/128 の損失は325/1152以下であり、1547/4860との差は5629/155520である。有理数の演算はPython標準ライブラリFractionでも確認した。

全箱を従来の十分条件で覆うにはこの上界は粗すぎる。十分条件の不成立はHの符号変化や数学的反例を意味しない。

## 3. 「0.509」の扱いについての修正候補

今回独立に回収したμ積分下界は

\[
L(\lambda)=\lambda\left\{\frac43-\frac23(1-\lambda^2)
-\frac4{35}(1-\lambda^2)^2\right\}.
\]

これは対象帯で増加する。正確な一様下界は

\[
L(119/200)=\frac{610465550029}{1200000000000}
=0.508721291690833\ldots
<\frac{509}{1000}.
\]

したがって、このLを小数第3位へ丸めた表示が「0.509」であるなら、それを厳密な下界として使ってはいけない。上記の有理数を使うか、下向きの有理数を採用する。

ユーザーが述べた検証済みLの原典は未取得であり、今回のLと同一とは断定しない。別の強い下界がある可能性は残す。ただし、その原典が照合されるまでは509/1000を証明の前提にしない。保守側1547/4860による今回の中心部分の結論には影響しない。

## 4. D4-0への主張範囲追補

中心は対称性によりE_ρ=E_z=0となる停留点である。H(0,0;λ)=E_{ρρ}(0,0;λ)>0は横方向二次係数の正値性を述べ、中心の停留点不存在は述べない。軸方向二次係数や中心の全方向の極小性も、これだけからは結論しない。

r>0かつτ≤1/8ではρ>0なので、H>0からE_ρ=ρH>0となり、子午面の停留点を排除できる。r=0は正則延長と閉被覆の端点として含め、停留点排除とは区別する。

中心部分をD-P2に引き渡す際は、元の閉じたパラメータ領域、座標式、Hの延長、ρ>0での排除の含意、r=0の扱いを明記する。将来の外側領域[1/128,1/8]とはr=1/128で重複する閉被覆を用いる。外側領域の証明とhandoff監査が揃うまではB_003全体をdischargeしない。

## 5. 出典と独立性の記録

数学的出発点は cotaxxxx/bg-oblate-spheroid、commit 111c3169d950939bf375012673b43495e4480ee1 の analysis/D_OB_P1_DESIGN_NOTE.md（blob f81e120e44a866d206117d4fab5fac627f26ccd1、SHA-256 2c304ee6159f6cf7012ca8fb6068d9e14a4bf8a9d01ceb756395d759145012e9）。領域・座標の基準は同commitのanalysis/D_OB_P2_CERTIFICATION_SPEC_V3.md（blob b52fcb622888844d3d46707072d45c77aae2e230、SHA-256 511d2f371784a07359c2b691abfb224ef772cddf298f2890b5596a5dc2309330）。今回の独立性は4階式の導出についてであり、既存背景・ユーザーが提示した結果を知らなかったという主張ではない。

独立導出固定時刻：2026-10-13T20:12:42.196863+00:00（JST 2026-10-14 05:12:42）。これは今回の作業順序の記録であり、外部署名付き時刻証明ではない。固定本文とスクリプトのhashは付録Cに収録する。

07db380eと74f0608eは、cotaxxxx/bg-oblate-spheroid、bg-spheroid-family、basepoint-geometryのcommit参照として取得を試みたが解決できなかった。確認したtreeとファイル検索でも照合本文を特定できなかった。非存在を断定するものではなく、別repo・未push・commit以外の識別子である可能性は未確認である。

過去の「Codex文書を読む前の提出」を証拠化するには、対象本文の完全hash、提出時刻の記録、Codex文書の最初のアクセス時刻または両者の順序を示すログが必要である。commitの自己申告時刻だけではアクセス以前の提出を独立に立証しない。

74f0608e…は原典未照合の参照候補としてのみ保持し、完全pinや正式証拠への昇格は行わない。

## 6. 実施範囲と次工程

数値積分・parameter sweep・D4 producer/checker・証明書生成・D5実行資産の読み取り/変更・契約変更・commit/pushは行っていない。以下のスクリプトは紙上式のexact symbolic検算用であり、本走や証明書checkerではない。

SymPyの導入試行はネットワーク承認が成立せず完了しなかった。依存ライブラリがないため実行結果を捏造せず、UNEXECUTEDとした。付録Bは独立式の内部検算用で、まだ得られていないClaude式との差分検算を実装済みとするものではない。

次工程は、照合原典と完全識別子を取得し、固定済み独立式に対して正規化を明示したSymPy差分検算を行うこと。その後、この追補・導出・照合結果・時刻記録・完全pinを一つのcommitにまとめる。式が一致しない場合は双方UNRESOLVEDのままchat監査へ渡す。


## 付録A：照合前に固定した独立導出（原文）

# D4 independent derivation — phase A, before counterpart access

2026-10-14. DRAFT / NOT FROZEN / EXECUTION PROHIBITED / CHAT AUDIT REQUESTED.
No Claude Code fourth-order formula or the contents of 07db380e / 74f0608e have been read during this derivation. The user's summary (including the approximate 0.509 claim) is known. This is formula-level independent derivation, not independence from all background mathematics or a claim about different model lineage.

## A1. Independent homogeneous expansion

Use the P1 density F=h G(gamma), G=acos²(gamma), with signed basepoint coordinates x=rho,z. At the physical centre set q=1-(1-lambda²)mu², gamma0=lambda/(w sqrt(q)), b=sqrt(1-mu²)cos(phi).

Let ell=b x+lambda mu z, k=b x+(mu/lambda)z, v2=x²+z². Then h=lambda(1-k), D²=q-2ell+v2, gamma=gamma0(1-k)(1+(-2ell+v2)/q)^(-1/2).

The homogeneous degree 1,2,3,4 components gamma/gamma0-1 are:

d1=ell/q-k.

d2=-v2/(2q)+3ell²/(2q²)-k ell/q.

d3=-3ell v2/(2q²)+5ell³/(2q³)+k v2/(2q)-3k ell²/(2q²).

d4=3v2²/(8q²)-15ell²v2/(4q³)+35ell⁴/(8q⁴)+3k ell v2/(2q²)-5k ell³/(2q³).

Define T0=d4-k d3, T1=d1 d3+d2²/2-k d1 d2, T2=d1²d2/2-k d1³/6, T3=d1⁴/24. Since G^(j+1)=-2R^(j), the homogeneous fourth-order part of F is

F[4]=-2lambda sum(j=0..3) gamma0^(j+1) R^(j)(gamma0) Tj.

Phi mean is the exact linear functional b^(odd)->0, b²->(1-mu²)/2, b⁴->3(1-mu²)²/8. Let A40_j=<[x⁴]Tj>, A22_j=<[x²z²]Tj>. The mu integral kernels for the ENERGY DERIVATIVES (not Taylor coefficients) are

K40=-24 sum gamma0^(j+1)R^(j) A40_j,
K22=-4 sum gamma0^(j+1)R^(j) A22_j.

E_rhorhorhorho(0,0)=integral[-1,1]K40 dmu;
E_rhorhozz(0,0)=integral[-1,1]K22 dmu.

The factors use E=(1/(4pi lambda))integral F dphi dmu, 4! for x⁴, and 2!2! for x²z². The H expansion coefficients are E40/6 and E22/2, respectively. These three notions must not be interchanged.

The companion exact SymPy script expands these four polynomials and checks a separate directional chain-rule formula. No numerical values, parameter sweep, or certificate computation is used.

## A2. Explicit uniform fourth-derivative bound on the SWEPT NEIGHBOURHOOD

Work on |diag(1,1,lambda)^(-1)p|<=1/8 and lambda in [119/200,33/50]. All signed meridional FTC segments lie here. The earlier distance proof gives D>=833/1600>1/2, lambda>1/2, h<=wD, and |h_v|<=w for any Euclidean unit direction v.

For n=1..4, the inverse-distance expansion uses Legendre polynomials P_n(a), |a|<=1, with |P_n(a)|<=1. This bound follows directly from the four polynomials P1=a, P2=(3a²-1)/2, P3=(5a³-3a)/2, P4=(35a⁴-30a²+3)/8. Thus |(D^-1)^(n)|<=n!D^(-n-1), and affinity of h yields

|gamma^(n)|<=2 n! D^(-n), n>=1 up to 4.

Use R(gamma)=2 integral[0,1] [1+gamma+(1-gamma)s²]^-1 ds. On [0,1], this gives

|G'|<=4, |G''|<=2, |G'''|<=64/15, |G''''|<=384/35.

The second bound uses |R'|<=1; the next two use integrals of (1-s²)² and (1-s²)³ with denominator>=1. The fourth directional chain rule gives

|F_vvvv| <= w D^-3 C4,
C4=16*(384/35)+128*(64/15)+240*2+96*4 =166496/105.

Hence |E_vvvv|<=C4/(lambda D_min³)<16C4<25600. This is uniform on the entire swept domain, not just the centre.

For orthonormal e_rho,e_z, Q(v)=D_v^4 E obeys
12 E_rhorhozz=Q(e_rho+e_z)+Q(e_rho-e_z)-2Q(e_rho)-2Q(e_z).
Homogeneity of Q gives |E_rhorhozz|<=25600 as well. Consequently legitimate explicit bounds are M40=M22=25600. They are conservative and do not close r<=1/8 via the coarse second-order remainder criterion.

## A3. An explicit analytic central patch

rho<=r, z<=lambda r*16/65<r/6. Therefore the remainder loss is at most (13/72)*25600*r². At delta=1/128 this is 325/1152, strictly below the old verified m*=1547/4860 (difference 5629/155520).

Thus the paper argument yields a strictly positive central patch 0<=r<=1/128, all tau in [0,1/8], all lambda in [119/200,33/50], subject to chat audit. It is not a machine certificate nor a Judge discharge. It does not use the claimed 0.509 improvement.

## A4. Stronger central lower bound independently recoverable

Keeping N(y,c)=1/2+(1/2-c)y-c²y²(1-y) before integrating gives
L(lambda)=lambda[4/3-2(1-lambda²)/3-4(1-lambda²)²/35].
It is increasing on the target interval: the bracket is positive and decreases with c, while c decreases with lambda. The exact value at 119/200 must be used rather than rounding the displayed 0.509 upward. The script records the exact fraction and its difference from 509/1000. The cited external L formula has not yet been read; no identity is presumed.

## A5. Outstanding comparison

After the phase-A files and hashes are fixed: retrieve the counterpart formula and source L; compare the phi means with exact SymPy differences, allowing only documented changes of coordinates/normalization. If unequal or counterpart absent, mark the comparison UNRESOLVED. Historical timestamp evidence requires both submission and first-access records; a commit timestamp alone proves no absence of prior access.

## 付録B：固定したSymPyスクリプト（UNEXECUTED）

```python
"""D4 phase A: exact symbolic work only; no numerical integration or scan."""
import sympy as S
from pathlib import Path
import json,hashlib,datetime
x,z,b,mu,lam,q,g=S.symbols('x z b mu lam q gamma', nonzero=True)
R0,R1,R2,R3=S.symbols('R R1 R2 R3')
y=S.symbols('y')
ell=b*x+lam*mu*z
k=b*x+mu*z/lam
v2=x*x+z*z
d1=ell/q-k
d2=-v2/(2*q)+3*ell**2/(2*q**2)-k*ell/q
d3=-3*ell*v2/(2*q**2)+5*ell**3/(2*q**3)+k*v2/(2*q)-3*k*ell**2/(2*q**2)
d4=3*v2**2/(8*q**2)-15*ell**2*v2/(4*q**3)+35*ell**4/(8*q**4)+3*k*ell*v2/(2*q**2)-5*k*ell**3/(2*q**3)
T=[d4-k*d3,d1*d3+d2**2/2-k*d1*d2,d1**2*d2/2-k*d1**3/6,d1**4/24]
def avg(expr):
 p=S.Poly(S.expand(expr),b)
 moments={0:S.Integer(1),1:S.Integer(0),2:(1-y)/2,3:S.Integer(0),4:3*(1-y)**2/8}
 return S.factor(sum(co* moments[n[0]] for n,co in p.terms()).subs(mu**2,y))
out={}
for label,nx,nz,factor in [('K40',4,0,-24),('K22',2,2,-4)]:
 A=[avg(S.Poly(S.expand(t),x,z).coeff_monomial(x**nx*z**nz)) for t in T]
 out[label+'_A']=[str(a) for a in A]
 out[label]=str(S.factor(factor*sum(g**(j+1)*[R0,R1,R2,R3][j]*A[j] for j in range(4))))
# Independent directional derivative route to the quartic density.
t,l0,k0,v0=S.symbols('t ell k v2')
gam=g*(1-k0*t)*(1-2*l0*t/q+v0*t*t/q)**S.Rational(-1,2)
gd=[S.diff(gam,t,j).subs(t,0) for j in range(1,5)]
a1,a2,a3,a4=gd
chain=(-2)*(R3*a1**4+6*R2*a1*a1*a2+3*R1*a2*a2+4*R1*a1*a3+R0*a4) +8*k0*(R2*a1**3+3*R1*a1*a2+R0*a3)
series=-48*sum(g**(j+1)*[R0,R1,R2,R3][j]*T[j] for j in range(4))
delta=S.factor(chain.subs({l0:ell,k0:k,v0:v2})-series)
assert delta==0
out['directional_vs_homogeneous_difference']=str(delta)
C=S.Rational(16*384,35)+S.Rational(128*64,15)+240*2+96*4
out['C4']=str(C)
out['16C4']=str(16*C)
assert 16*C <25600
L=lam*(S.Rational(4,3)-2*(1-lam**2)/3-4*(1-lam**2)**2/35)
out['own_center_L_at_119_200']=str(L.subs(lam,S.Rational(119,200)))
out['own_center_L_minus_509_1000']=str(L.subs(lam,S.Rational(119,200))-S.Rational(509,1000))
out['local_loss_at_delta_1_128']=str(S.Rational(25600,128**2)*S.Rational(13,72))
out['old_margin_minus_local_loss']=str(S.Rational(1547,4860)-S.Rational(25600,128**2)*S.Rational(13,72))
out['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
dest=Path(__file__).with_name('d4_phase_a_result.json');dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
```

## 付録C：固定記録

```json
{
  "fixed_at_utc": "2026-10-13T20:12:42.196863+00:00",
  "counterpart_access": "not yet accessed",
  "files": {
    "D4_PHASE_A_INDEPENDENT_DERIVATION.md": "5271d5d89626f1db18939b3d3dae5547cbc12d35168ad26fb4765211aaaa55d1",
    "d4_phase_a_independent.py": "4b8fe0c9a7368ad758be70aa79a6e86a1a91960b3fc79939d3019f266e300653"
  },
  "sympy_local": "unavailable; no assertion of completed SymPy check"
}

```
