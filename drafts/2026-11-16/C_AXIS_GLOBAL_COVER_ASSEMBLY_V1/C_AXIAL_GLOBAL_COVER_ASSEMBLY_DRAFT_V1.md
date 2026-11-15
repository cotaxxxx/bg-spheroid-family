# 軸上C系列・大域被覆の組み立て v1

**状態：DRAFT / A1 chat監査待ち / GLOBAL C ASSEMBLY NOT JUDGE-CLOSED**

2026-11-16 / Dig / v0 `9f897781` の chat V22 `680eda06`（A1〜A5）への対応案。
本書は **Cの大域根数の定理と根拠の論理鎖を提示する原案**であり、独立監査やJudgeの大域裁定を先取りしない。既存の数値本走を再実行していない。

## 0. 組み立てる主張と記号

`lambda∈I=[2/5,33/50]` の扁平回転楕円体族について、軸パラメータ `t∈(-1,1)`、
`g(t,lambda)=∂_t E_lambda(t)`、`H_axis(lambda)=∂_t g(0,lambda)`、
`Phi(tau,lambda)=g(t,lambda)/t`（`tau=t²`; `t=0` では連続延長）を用いる。
正の**内部**軸根数を
```text
N_+(lambda) = #{ t∈(0,1) : g(t,lambda)=0 }.
```
と定義する。中心 `t=0` と外側端点 `t=1` は `N_+` に数えない。

中心軸係数の一意零点を `lambda_c`、C1aの `F_x=2g(1/2,lambda)` の一意零点を
`lambda_x`、境界 `B_ob(lambda)=g(1,lambda)` の一意零点を
`lambda_partial`（`lambda_∂`）と書く。根拠原本が与える範囲は
```text
2/5 < lambda_c < 83/200 < 699/1600
    < lambda_x < 281/640 < 703/1600 < 9/20 < 5/8
    < lambda_partial < 33/50 .
```
これは正本の中心軸係数Judge receipt、C1a receipt の報告用有理区間、B_ob再認証とband receiptから得るもの。
`lambda_c`、`lambda_x`、`lambda_partial` は相互に別のパラメータである。
なお `lambda_x` の端点区間は根数のPASS条件ではなく、実行済みC1aの別途認証された報告用区間である。

### 提出する大域結論（条件付き組み立て定理）

**定理 C-AXIS-V1（chat監査・A1受理を前提とする案）。**
既存のC0・C1a〜d・境界band・空白①②のJudge/機械受理結果、
V13/V19/V20の解析補題、および本稿A1移送が正当ならば、
```text
N_+(lambda) =
  0,   2/5 <= lambda <= lambda_c,
  1,   lambda_c < lambda < lambda_partial,
  0,   lambda_partial <= lambda <= 33/50.
```
`lambda=lambda_partial` では境界に唯一の根 `t=1` があるが、これは内部軸根ではない。
`lambda=lambda_c` では中心 `t=0` に退化零点があるが、正の内部根はない。
`lambda=lambda_x` の唯一の正根はちょうど `t=1/2` で、二重に数えない。
奇性により負の内部軸根は正の根と対をなす（§5）。

**制限：** 本稿は上記の部品の条件と境界をつないだ論理的な導出案であり、
球／扁長の主定理や横断D系列の結論を新たに主張しない。
A1はまだchat監査未通過であり、本稿自身のglobal C判定は **OPEN** とする。

## 1. 解析的な橋（A1を正本に追加する）

不足していた `lambda∈[83/200,9/20]`, `|t|<=1/2` の移送文書を、
別リポジトリ `cotaxxxx/bg-oblate-spheroid` の
`analysis/OBLATE_AXIAL_LOWER_HALF_LEMMA_C1A_TRANSFER.md` に提出した：

- draft commit `473d7022ba10f91bcd8c731566908c6541a00c12`
- file blob `b8370d649bac0bbe943186eb003b6b0e837a3dd6`
- branch `draft/c1a-lower-half-transfer-20261116`、chat監査待ち
- source `OBLATE_AXIAL_LOWER_HALF_ANALYTIC_LEMMA.md` blob `6fba6e4f`
- same method `OBLATE_AXIAL_LOWER_HALF_LEMMA_C0_TRANSFER.md`（commit `963b03be`, blob `0ab17896`）

移送で直接確かめた有理数は
```text
q >= 6889/160000,  w >= 83/200,
0 <= u <= 5345218321/6400000000 < 1,
|lambda² t/(1-lambda²)| <= 81/638 < 1,   1/2 <= A <= 3/2.
```
これにより原補題の Lemmas 3,4,5,6,8,9,10 が同じ議論で移り、
Lemmas 1,2,7,11,14–17, Proposition 12, Corollaries 13,18 の
依存条件が満たされる（数学的検査はchatに依頼中）。
結果として `g=t Phi(t²,lambda)`、`Phi(0,lambda)=H_axis(lambda)` と
```text
partial_tau Phi(tau,lambda)
 = (1/4) ∫_[0,1] (1-x²) partial_t³ g(x sqrt(tau),lambda) dx
```
が `0<=tau<=1/4` で使える。
C1a Gate A は `partial_t³g<0` on `[0,1/2]×[83/200,9/20]` なので
`partial_tau Phi<0`、従って `Phi` は `tau` について狭義減少する。
この一歩がv0では欠落していた。**既存C1a機械の三階微分符号を新たに計算しない。**

他の範囲は既存のC0移送（`[2/5,83/200]`）、
C1c補題（`[9/20,5/8]`）、
C1d補題（`[5/8,33/50]`, `|t|<=31/32`）による。
V20によるC0/C1c/C1dのchat監査と、A1新規の監査待ちを混同しない。

## 2. λの10区分と根数の論証（A2）

以下の表は **`N_+` の区分を重ならないように割り当てる**。
端点を重複評価する証拠があっても根は一回だけ数える。
記号 `C0a,b`、`C1a A,D,L,R` 等は§7の原本中の番号を指す。

| 区分 | λ範囲 | 下側の議論 | 上側の議論 | 内部正根 |
|---|---|---|---|---|
| 1 | `[2/5,lambda_c)` | 中心Judge：`H<0`、C0a+Cor.18で `Phi(t²)<Phi(0)=H<0`（`0<t<=1/2`） | 空白① L：`g<0`（`1/2<t<=1`） | 0 |
| 2 | `{lambda_c}` | `H=0`、C0aの `partial_tau Phi<0` により `Phi(t²)<0`（`t>0`）。中心のみ退化 | 空白① L：`g<0` | 0 |
| 3 | `(lambda_c,83/200]` | 中心Judge `H>0`、C0b `Phi(1/4)=2g(1/2)<0`、C0a+Cor.18で `Phi` は狭義減少・連続。中間値＋単調性で `(0,1/2)` に1根 | 空白① L：`g<0` | 1 |
| 4 | `(83/200,lambda_x)` | `H>0`、C1a `F_x=Phi(1/4)<0`、C1a A＋**A1移送**で `Phi` 狭義減少 → `(0,1/2)` に1根 | 空白① X：`g(1/2)<0` と `G_t<0` の帯／負の右外側 → 上側0根 | 1 |
| 5 | `{lambda_x}` | `H>0`、`F_x=Phi(1/4)=0`、A1により `Phi(t²)>0` for `0<t<1/2`。根は `t=1/2` の1個 | 空白① X：`t>1/2` で `g<0`、追加根なし | 1 |
| 6 | `(lambda_x,9/20)` | `F_x>0`、`Phi` 狭義減少 → `Phi(t²)>=Phi(1/4)>0` for `0<t<=1/2`、根0 | 空白① X（`lambda<=703/1600`）または R（`lambda>=703/1600`）の門：`t>1/2` にちょうど1根 | 1 |
| 7 | `[9/20,5/8]` | C1c Lemma／C1b正アンカー：`Phi(1/4)>0`、Cor.18 → `g>0` on `0<t<=1/2` | C1b 159受理区画：左側 `g>0`、管で `∂_tg<0`、右側 `g<0`（またはB_ob<0）、一意の管根。V21空白②で `t=1` まで覆う | 1 |
| 8 | `(5/8,lambda_partial)` | C1d：`g>0` on `0<t<=31/32`（C1d門＋正アンカー＋解析補題） | band Claims 1–3：`∂_tg<0`、`g(31/32)>0`、`B_ob(lambda)<0` → `(31/32,1)` に一意根 | 1 |
| 9 | `{lambda_partial}` | C1d：`g>0` on `0<t<=31/32` | bandで `g` 狭義減少、`B_ob=0` → `t=1` のみ。内部に根なし | 0 |
| 10 | `(lambda_partial,33/50]` | C1d：`g>0` on `0<t<=31/32` | bandで狭義減少、`B_ob>0` → `g(t)>0` on `[31/32,1]` | 0 |

**3と4の境界：** `lambda=83/200` は区分3が担当するが、C0bの負端点とC1aの門Lの符号が一致する。C1a移送は閉端点を含む。

**6のX/R接続：** C1a受領書の `lambda_x<281/640<703/1600` より、
`703/1600` では `g(1/2)>0`。空白① Xの `[1/2,5/8]` 単調区間で
`g(1/2)>0`, `g(5/8)<0` なら一意根があり、Rでは管内に一意根。
X/Rの共有端点は同じ函数 `g` の同じ一意零点を指す。
`lambda=9/20` は区分7が担当し、空白①の右端（開）とC1bの左端（閉）の間に空白がない。

**7と8の接続：** `lambda=5/8` は区分7が担当する。
C1b clampedの管 `[t_-,1]` は根1個。
一方C1dは `g>0` on `(0,31/32]`、bandは `g(31/32)>0`,
`B_ob(5/8)<0` かつ `∂_tg<0` on `[31/32,1]` より
`(31/32,1)` にちょうど1個。両ルートは同じgの同じ根であって
足し合わせて2個とはしない（C1b receipt §5.2の31/32はbookkeeping cut）。

## 3. 空白①のL・X・R（A3）

空白① `U_check = {1/2<t<=1, 2/5<=lambda<9/20}` のv9.1、
run4 producer/checker `160/160` PASS、Judge CONDITIONAL_CLOSED。
160個のλ小区画（幅1/3200）を `48+78+34` に分ける。

| 群 | λの区間・slab | 門と根数の帰結 |
|---|---|---|
| **L** | `[2/5,83/200]`・48 | ROOT_FREE_REGION。`g(1/2)<0` を用い、`g<0` on `(1/2,1]`、根0 |
| **X** | `[83/200,703/1600]`・78 | ROOT_COUNT_BY_C1A_SIGN_NO_T_STAR。C1a門 Dの `F_x` 単調、`F_x(lambda_x)=0` を採用。凍結門の `G_t<0` on `[1/2,5/8]`、`g<0` on `[5/8,31/32]` と端点門を連結し、`g(1/2)` の符号で上側根0または1を決める |
| **R** | `[703/1600,9/20]`・34 | RESOLVED_WITH_CERTIFIED_T_STAR。`t_-<t_+, g(t_-)>0, ∂_tg<0` in tube、右側負を検証し、`(1/2,1)` の根を一意に特定する |

`lambda=83/200` はv9.1 §1.1でX側owner、L側は一致確認。
`lambda=703/1600` は同じ一意根のX/R共有境界。
`lambda=9/20` はC1b側owner。C1aの符号を空白①のXへ流すのは
Judge v7規則E3とv9.1 §0–1によるもので、**根数を単なるslab数から推論しない**。

## 4. 空白②・C1b内部の閉被覆と帯（A4を含む）

C1bは `[9/20,5/8]` を、封印台帳の159受理区画で正確に被覆する。
chat V22は封印C1b台帳の両系統について次を独立検算した：
`[1/2,t_-]` のL/L_MONO、左壁LEFT、`[t_-,t_+]` のGT/corner、
右壁RIGHT、unclamped124の右R/R_MONO、clamped35の `t_+=1` と
B_ob<0。unclamped124中の106は `t_+<31/32`、
`[t_+,31/32]` の右外側が必要。残18は `t_e>31/32`。
空白② `t∈[t_e,1]`, `t_e=max(31/32,t_+)` で `g<0` を
Judge V21がCLOSEDとしている（124親各深さ0・ABORT0）。
以上の分割で`U2=[9/20,5/8]×(1/2,1]`に隙間がない。
ここでの `t_+=1` はclampされた区画の管終点で、
`t=31/32` はbookkeeping cutであって管終点とは限らない。

右端 `lambda=5/8` の根の二重計上防止は§2・区分7/8のとおり。
band `lambda∈[5/8,33/50]`, `t∈[31/32,1]` では
Judge receipt Claims 1,2 `∂_tg<0`（片側 `t=1` を含む）、
Claim 3 `g(31/32)>0`。境界関数 `B_ob` の一意零点と符号は
`analysis/BOB_ENDPOINT_RECERTIFICATION_MACHINE_RECEIPT.md`、
同定はC1 Lemma 3・C2 Lemma、境界での極限連続性はC1 Lemma 5。
ゆえに§2の区分8〜10で各λの内部根数が閉じる。

## 5. 中心・横断・境界の異なる三つの事象（A2/A5）

- **中心 `lambda=lambda_c`:** `H_axis(lambda_c)=0` かつ
  `∂_lambda H_axis>0`（CENTER_AXIS_COEFFICIENT_JUDGE_RECEIPT）。
  C0a `∂_t³g(0,lambda_c)<0` より
  `c3=(1/6)∂_t³g(0,lambda_c)<0`
  （CENTER_PITCHFORK_RELATION_TO_C0、C0移送のLemma 16）。
  この条件は中心三次の非退化を与える。根数と境界での接続は§2のとおり。
- **中央切断面 `lambda=lambda_x`:** C1a門 A,D,L,Rにより
  `F_x=Phi(1/4)` が狭義増加し、唯一零点は `lambda_x`。
  `lambda=lambda_x` では `g(1/2)=0`、
  `∂_t g(1/2)=Phi(1/4)+(1/2)∂_tau Phi(1/4)
                  =(1/2)∂_tau Phi(1/4)<0`（A1＋門A）。
  よって根はこの断面を横断し、`t=1/2` を二度数えない。
- **境界 `lambda=lambda_partial`:** `B_ob(lambda_partial)=0`、
  bandの `∂_t g<0` と `g(31/32)>0` により
  `t=1` へ進む唯一の根は、到達時は内部から除外される。
  `B_ob`の単純零点と境界到達は別の解析的事実で、
  center/crossingとは異なる事象である。

**奇性の出典（A5）：** lower-half lemma Lemma 2 の
`E_lambda(-t)=E_lambda(t)`（`|t|<1`）。微分可能性と
`g=∂_tE` は各解析補題の Proposition 12/Corollary 13
（`|t|<=1/2`、C1dは `|t|<=31/32`）、
`1/2<=|t|<1` ではendpoint C1補題 Lemma 3による。
従って `g(-t,lambda)=-g(t,lambda)` on `(-1,1)`。
`t=±1` はendpoint C1補題 Lemma 5の連続性によって左右に延長する。
常に `g(0,lambda)=0` だが、**中心は内部正根数N_+に含めない**。
正根が1個なら負根も対称に1個存在し、正根が0なら負根も0である。
外側端点根 `t=±1` はN_+の内部数に数えない。

## 6. 有理領域の被覆の別検査と限界

v0の `exact_tile_check.py` はλ境界
`2/5,83/200,9/20,5/8,33/50`、
t境界 `0,1/2,31/32,1` を区切りとして、
開閉区間を含む正半軸の宣言範囲が覆われていることを検査した
（12内部セルと54代表的境界点）。v1も同じ根拠部品を使うので
この被覆結果を継承する。

この機械的な有理端点チェックは符号・根数・枝の同一性を検査しない。
C1b内側の全159区画の閉被覆はV22（両系統）、
空白②の124親の門とR/R_MONOはV21の独立検収が根拠である。
§2の論理鎖には**新A1移送のchat監査**を要する。

## 7. 出典の番号と証拠ピン

**正本本体:** `cotaxxxx/bg-oblate-spheroid`、
`design/d-ob-p2` を出典とし、各受領書の明示した凍結実行commit/blobを優先。
参照の歴史的文言「EXTERNAL_AUDIT_PENDING」等は、
後続chat V13/V19/V20の検収状態に自動的に書き換えない。

| 証拠名（本文内略号） | 原本と使う箇所 | 提出時の状態 |
|---|---|---|
| CENTER | `analysis/CENTER_AXIS_COEFFICIENT_JUDGE_RECEIPT.md` §Scoped claim（`∂_λH>0`, `lambda_c`） | Judge PASS within scope |
| C0 | `analysis/GLOBAL_AXIAL_C0_JUDGE_RECEIPT.md` C0a・C0b、および `analysis/CENTER_PITCHFORK_RELATION_TO_C0.md` | Judge PASS conditional on lower-half lemmas; V20のC0移送chat PASS |
| C1a | `analysis/GLOBAL_AXIAL_C1A_MACHINE_RECEIPT.md` §Logical C1a gate A,D,L,R、§Reported certified crossing bracket | MACHINE PASS。区分4〜6へのA1移送は未監査 |
| A1 | **新規** `analysis/OBLATE_AXIAL_LOWER_HALF_LEMMA_C1A_TRANSFER.md` draft commit `473d7022ba10f91bcd8c731566908c6541a00c12` blob `b8370d649bac0bbe943186eb003b6b0e837a3dd6` | **DRAFT / chat監査待ち** |
| C1b | `analysis/GLOBAL_AXIAL_C1B_MACHINE_RECEIPT.md` §§5.2,6、sealed159区画 | MACHINE CLOSED、空白②Judge V21が上側を補完 |
| C1c | `analysis/GLOBAL_AXIAL_C1C_ANALYTIC_ASSEMBLY.md` §§F1–F3,L、§§4–5 | 構成根拠、解析補題V20 chat PASS |
| C1d | `analysis/GLOBAL_AXIAL_C1D_MACHINE_RECEIPT.md` §1、`analysis/GLOBAL_AXIAL_C1D_ANALYTIC_ASSEMBLY.md` §§F1–F3,L | 組み立て根拠、解析補題V20 chat PASS |
| band | `analysis/LOCAL_ENTRY_BAND_JUDGE_REQUEST.md` §§1,4–7、`LOCAL_ENTRY_BAND_JUDGE_RECEIPT.md` | Judge PASS conditional on C1/C2、V19 chat PASS |
| B_ob | `analysis/BOB_ENDPOINT_RECERTIFICATION_MACHINE_RECEIPT.md` §§1–2、`LOCAL_ENTRY_BAND_JUDGE_REQUEST.md` §§3–6 | 単純境界零点と端点同定、条件の分離 |
| GAP1 | `bg-spheroid-family` `audits/C_GAP1_JUDGE_RECEIPT_2026-10-13.md`、v9.1 `drafts/2026-10-12/C_GAP1_CONTRACT_V9_1_DELTA_2026-10-12.md`、run4 `26d81e1` | Judge条件付きCLOSED、両系統160/160 |
| GAP2 | family V21 Judge裁定 `evidence/c-gap2-freeze-20261115` commit `151d3c5`、本走 `4ecb713`、比較補完 `a2255fa`、比較SHA256 `6fb9d29238cd73c023c96f87f202255c743e968c7b39a32853ff25c8df3b975b` | **Judge V21 CLOSED** |
| D6 | family chat監査 V13、V19、V20（V20 `fc9e48e`）、C1c blob `6fba6e4f`、C0移送 `963b03be`、C1d `35656381` | chat監査PASS、外部人間監査とは区別 |
| V22 | family `evidence/c-gap2-freeze-20261115` commit `680eda0`、`CHAT_AUDIT_C_AXIAL_ASSEMBLY_V0_20261116.md`、ZIP SHA256 `e96412f6a6e256d343df47bbc953b2915a68ce9c61944f4c8c29f0a859c67e18` | v0監査、A1〜A5を要求、C1b内部被覆独立検算PASS |

## 8. 独立監査・Judgeへの境界

chatはまずA1の七補題を監査し、続いて本稿§2の各区分の
下側／上側の符号・閉端点・X/R境界・`lambda=5/8`・奇性の
論理接続を受領書の番号と突き合わせる。A1や他部品の未充足が
見つかれば、v1はOPENを維持し、必要な修正を特定する。

**本稿v1の提出はglobal CのJudge CLOSEDを意味しない。**
chatの独立監査PASS後にのみ、Judgeに大域軸根数の採否を裁定していただく。
