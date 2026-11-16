# D-OB 大域組み立て v0.1｜扁球の内部停留点（C＋D）

2026-11-16 / Dig / **Judge V24：D-OB GLOBAL CLOSED、v0はchat監査PASS。v0.1は任意の引用修正M1・M2のみ。**

この文書の目的は、採用済みの **C-AXIS-V1（軸上の根の構造）** と、
Judge V18でCLOSEDとなった **横断D系列の全域 H>0** を接続し、
体積保存扁球族の**内部**停留点を数える大域定理を一つの短い論証で提出すること。
新しい数値計算や証明範囲の拡張はしていない。採用証拠はJudge V24（family evidence/c-gap2-freeze-20261115 commit 127be52）。

## 1．対象と既採用の入力

```text
K_lambda = { (x,y,z) : x²+y²+z²/lambda² <= 1 }
lambda in I = [2/5,33/50]  (the P1/C reference ellipsoid; see similarity normalization below)
p=(rho cos theta, rho sin theta, z),  rho>=0.
M_lambda = { (rho,z) : rho>=0, rho²+z²/lambda² <=1 }.
E_lambda(p) = the adopted axial/meridional E functional.
```

ここで停留点とは **p∈int(K_lambda)** における ```∇E_lambda(p)=0``` をいう。
```rho²+z²/lambda²=1``` の境界面は内部停留点の個数に含めない。
回転・上下反転対称性を使う（P1 ``6.1–6.2）。

**体積保存族への同定。** 上の`K_lambda`はP1/C証明で用いる
半径1・軸長`lambda`の参照楕円体で、**この表示自体は体積一定ではない**。
体積を`4π/3`に固定した同じ形状の楕円体は
`K_lambda^vol=lambda^(-1/3) K_lambda`（半軸`lambda^(-1/3)`、
縦半軸`lambda^(2/3)`）である。Eの定義
`E_K(p)=∫_(∂K) alpha_(K,p)^2 ((x-p)·nu_K(x))/(3Vol(K))dA(x)`
では正の相似拡大`(K,p)↦(cK,cp)`により角`alpha`は不変、
正規化された円錐面積測度は分子・分母とも`c³`倍で不変なので
`E_(cK)(cp)=E_K(p)`。したがって停留点は正の相似写像で
一対一に対応し、根の個数は不変である。**以下の座標は
参照楕円体K_lambda上の座標**であり、体積保存族の停留点座標は
`lambda^(-1/3)`倍する（軸上の±根は`z=±lambda^(2/3)t_*`）。

### C（Judge V23 CLOSED）

正の軸を ```p=(0,0,lambda t), t∈(0,1)``` と書き、
```g(t,lambda)=∂_t E_lambda(0,0,lambda t)``` とする。
採用済み C-AXIS-V1 は

```text
N_+(lambda) := #{t∈(0,1):g(t,lambda)=0}
 = 0    for 2/5 <= lambda <= lambda_c,
 = 1    for lambda_c < lambda < lambda_partial,
 = 0    for lambda_partial <= lambda <= 33/50.
```

```2/5<lambda_c<83/200<lambda_x<9/20<5/8<lambda_partial<33/50```。
```lambda=lambda_c``` は軸中心の三次非退化（```c3<0```）、
```lambda=lambda_x``` では根がちょうど ```t=1/2```（単純根）、
```lambda=lambda_partial``` では根が ```t=1``` に達し**内部の根ではない**。
```g(-t,lambda)=-g(t,lambda)``` と ```g(0,lambda)=0``` も採用済み。

**採用証拠：** family evidence/c-gap2-freeze-20261115 commit ```434c700f1e90947fd6616a4745400ee576ee9aa6``` の
```JUDGE_RULING_C_AXIAL_GLOBAL_CLOSED_20261116.md```、chat V23（A1移送・組み立てv1 PASS）。
v1.1（B1〜B3）はchat V24の差分監査でPASS。数学的変更はなく、C-AXIS-V1の採用済み内容はそのまま維持する。

### D（Judge V18 CLOSED）

P1 Lemma 6.1 により、```rho>0``` では
```text
H(rho,z;lambda) := (1/rho) ∂_rho E_lambda(rho,0,z),
∂_rho E_lambda(rho,0,z)=rho H(rho,z;lambda).
```

```rho=0``` では ```H(0,z)=E_rhorho(0,z)``` に連続延長。
P1 Lemma 6.2の```z↦−z```反射により、正の子午面
```Q_lambda={(rho,z):rho>=0,z>=0,rho²+z²/lambda²<=1}``` で判定すれば足りる。
V18で閉じたD5全域は次の無次元化による閉箱全域に対し ```H>0```：

```text
0<=r<=1, 0<=tau<=1, lambda in I,
rho = r(1-tau²)/(1+tau²),
z   = lambda r·2tau/(1+tau²).
```

```rho²+z²/lambda²=r²``` より、写像は各```Q_lambda```を覆う。
Judge V18は、中心列・一般域V4・Plan Bカラー・薄層・境界面を
有理端点まで接続し、P1条件を解消してD5 CLOSEDと裁定した。
D2 O2・D3はこの全域H>0の関門から除外済みで、再導入しない。

**Dの被覆台帳（STATE v1.60 `D5の採用範囲）：**

| 部品 | rの閉区間（τ∈[0,1]、λ∈I は共通） | 状態 |
|---|---|---|
| 中心列 | [0,1/8] | Judge V18 CLOSED |
| 一般域 V4 | [1/8,15/16] | Judge V18 CLOSED |
| Plan B | [15/16,1−2⁻¹⁶] | Judge V18 CLOSED |
| 外側薄層 | [59999/60000,1] | Judge V18 CLOSED（H≥607/6000） |
| 外側面 B′ | r=1 | Judge採用（H≥1/5） |

```59999/60000 < 1−2⁻¹⁶``` であるため、Plan Bと薄層は重なる。
各部品は閉区間を含み、```[0,1]``` を漏れなく覆う。
一般域V4・Plan Bについて残る独立producer比較は**採用後補強事項**であり、
V18 CLOSEDの前提条件にはしない（問題発見時の再審査規則は維持する）。

**採用証拠：** family ```STATE.md v1.60``` `D5・
```runs/2026-11-15/D5_GLOBAL_COVER_P1_AUDIT_V17/```、
```runs/2026-11-15/D5_JUDGE_CLOSED_RULING_V18/```。
正本```cotaxxxx/bg-oblate-spheroid``` ```design/d-ob-p2``` の
```analysis/D_OB_P1_DESIGN_NOTE.md``` Lemmas 6.1–6.2、
```analysis/D_OB_P2_CERTIFICATION_SPEC_V3.md``` `0
（座標・H・正の子午面の適用範囲）にも接続する。

## 2．二つの採用結果を接続する証明

**補題 D-OB-G1：軸外に内部停留点はない。**
```p∈int(K_lambda)```、```rho>0``` とする。
軸対称性により回転させて ```p=(rho,0,z)``` としてよい。
Dの閉領域は```rho>0```で ```H(rho,z;lambda)>0``` を与えるので
```∂_rho E_lambda(p)=rho H(rho,z;lambda)>0```。
停留点ならこの偏微分も0でなければならないため矛盾。
```z<0``` は上下反転対称性で同じ。したがって内部停留点はすべて
**```rho=0``` の回転軸上**にある。□

**補題 D-OB-G2：軸上の停留点とgの根は一対一。**
内点 ```p=(0,0,z)``` を ```z=lambda t```、```|t|<1``` と書く。
P1 Lemma 6.1(i)（軸上で E_ρ＝0）、P1 §2（内部 C^∞ と E(0,λt)＝E_λ(t)）および回転対称性から
```∂_xE=∂_yE=0```。一方、鎖律により
```text
g(t,lambda)= d/dt E_lambda(0,0,lambda t)
           = lambda ∂_z E_lambda(0,0,lambda t).
```
```lambda>0``` なので ```∇E_lambda(p)=0 ⇔ g(t,lambda)=0```。
Cから ```t=0``` は常に根で、非零根は対称対
```t=±t_*(lambda)``` だけである。□

**定理 D-OB-GLOBAL（Judge V24採用・CLOSED）。**
```lambda∈[2/5,33/50]``` の各扁球の
```int(K_lambda)``` にある停留点集合は次のとおり。

| λ | 内部停留点集合 | 個数 |
|---|---|---:|
| ```2/5<=lambda<=lambda_c``` | ```{(0,0,0)}``` | 1 |
| ```lambda_c<lambda<lambda_partial``` | ```{(0,0,0), (0,0,+lambda t_*), (0,0,−lambda t_*)}``` | 3 |
| ```lambda_partial<=lambda<=33/50``` | ```{(0,0,0)}``` | 1 |

ここで ```0<t_*(lambda)<1``` はC-AXIS-V1の唯一正根。
```lambda=lambda_x``` では ```t_*=1/2``` で内部停留点は3個。
```lambda=lambda_c``` は中心の退化を伴うが非零の内部停留点はまだ無い。
```lambda=lambda_partial``` では```t=±1```は境界```(0,0,±lambda)```で
あって内部停留点ではない。したがって内部停留点は中心1個に戻る。

**証明：** G1で軸外を除外し、G2で軸内点を```g=0```に帰着する。
Cの ```N_+``` と奇性から、中心1個＋正根数と同数の負根の対を得る。
すなわち ```N_{\mathrm{stat,int}}(lambda)=1+2N_+(lambda)```。
表はCLOSED C-AXIS-V1の根数を代入したもの。□

## 3．射程・監査事項

- これは**扁球区間だけ**を対象とする。球の接続、扁長族、
  全形状族の連続的分類、内部停留点のMorse index／極値分類は扱わない。
- 証明は**内部停留点**に限定。境界```t=±1```の端点符号と
  内部の根の個数を混同しない。```r=1```のD5採用は被覆・連続性の証拠で、
  境界での変分的な停留点条件を新たに立証しない。
- DのH>0は軸外の**ρ方向**だけで停留点を除外するのに十分。
  E_zの符号を軸外で別途証明する必要はない。
- CとDは同じ ```E_lambda```・正規化を使う必要がある。
  P1 `6のH同定とC1 Lemma 3のg同定をchatが正本の式で照合すること。
- P1継承条件・D5 global閉箱の端点証拠がV17/V18で本当に
  解消していること、採用後補強事項が採用条件に戻されていないことを確認する。
- v0原稿はchat V24でPASSしており、
  **D-OB globalはV24でJudge CLOSED**。v0.1は引用修正のみであり、新規のJudge裁定は不要。
  外部人間による解析補題監査は論文・投稿の別工程であり、
  Judge C-AXIS-V1 CLOSEDやV18 CLOSEDの条件には再度加えない。

## 4．短い数論的被覆補助検査

同梱```domain_join_check.py```は、採用済みDの5帯を有理分数で
[0,1]へ被覆させ、Cのλの5境界の順序と
内部停留点個数```1+2N_+```の記帳を確認する。
**符号証明や数値計算の代わりではなくNOT_EVIDENCE**。
