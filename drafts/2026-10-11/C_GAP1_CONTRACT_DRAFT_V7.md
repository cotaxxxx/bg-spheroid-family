# C 空白① 事前宣言 DRAFT v7 — 統合拘束文書

**状態：DRAFT v7 / CONSOLIDATED CONTRACT CANDIDATE / NOT FROZEN / EXECUTION PROHIBITED / NO COMMIT。**

基準：
- `bg-spheroid-family` main `8bc2c00508727f6e6455b21fa75a27b11f165f47`
- `STATE.md` v1.15
- 対象：C 空白①
  \[
  U_1=\{(t,\lambda):1/2<t\le1,\ 2/5\le\lambda<9/20\}.
  \]

この v7 は、v6 とその後の設計・端点追補・数値契約・Code 独立監査の受理結果を、**一本の現在契約**として整理するための草稿である。

v7 が CHAT AUDIT を通り Judge FREEZE された場合、空白①の current operational contract として v6 を置き換える。v6 は履歴資料として残す。

この文書は実行許可ではない。新実装、数値本走、証明書生成、commit、push を許可しない。

---

## 0. Authority / incorporated records

### 0.1 この v7 に取り込む current documents

以下を exact SHA-256 で取り込む。詳細な数値定数・実装差分表・端点処理の詳細は、ここに全文再掲せず、該当文書を exact content として参照する。

| document | SHA-256 | role |
|---|---|---|
| `C_GAP1_IMPLEMENTATION_DESIGN_DRAFT_V2.md` | `0a407d1bec2d491befc2bdaee7dbfff29b3f93bf54f3aef466093dd9453038d1` | implementation / diff allowlist |
| `C_GAP_ENDPOINT_ADDENDUM_DRAFT_V2.md` | `7471800d81caabdbbe3bfb5c8dc2e020434adbd0a67ed4e6bbd38afbea33d3a4` | cumulative endpoint method |
| `C_GAP_NUMERIC_CONTRACT_DRAFT_V1.md` | `be67046f8bb2d6cb5b3c0e615ee7edb1338d91956f6eb1aa2701217c05600d07` | λ grid / precision / degree / caps |
| `G0_E1_UNIFORM_GT_PAPER_PROOF_DRAFT_V3.md` | `8bf8f5d87cfc2e6f424499804b0fd85d982cf480deb99a26c284367960578671` | endpoint legality / \(G_t\) paper proof |
| `CHAT_AUDIT_THREE_PREDECLARE_DRAFTS_V2_2026-10-10.md` | `43f3d811f62ad50de041e2a234c64f7bb9e9c1d9b2103a141c696f1d54ea10dd` | Judge ruling E3 |
| `CHAT_REVIEW_OF_CODE_AUDIT_C_GAP1_V6_2026-10-10.md` | `a1437832be8e6b298cd73ddb25cc912ac841bf4ebfadfb1cf1c3792199a43386` | Code findings classification |
| `CHAT_AUDIT_C_GAP1_V4_AND_G0_V0_2026-10-10.md` | `f8a1f95490c7e4b7a2327e39b2bdde79433bc682b23245214747e41136c03df1` | 27-document amendment list / J2 |

Code 独立監査本文は `CODE_AUDIT_C_GAP1_V6_2026-10-10.md`、SHA-256
`0d882b5313cbb26cf41a9ec22cb8524b6e2b78525de3154c58f36bb07c82da3b`
として保存済み。

### 0.2 優先順位

v7 が FREEZE された後、空白①に関する矛盾があれば優先順位は：

1. Judge が FREEZE した v7
2. v7 が exact SHA で取り込んだ design v2 / endpoint addendum v2 / numeric contract v1
3. 実行済み C1b code blobs
4. 過去の amendment / addendum 文書
5. v6 以前の草稿

とする。

ただし既存 C1b の事実関係について、v7 が executed code の内容を創作的に変更してよいという意味ではない。許される差分は §8 の allowlist だけである。

---

## 1. Claim and classification

空白①では、各固定 \(\lambda\in[2/5,9/20)\) に対して \(g(t,\lambda)\) の \(t\in(1/2,1]\) 上の根構造を認証し、既存 C 系列の global cover の穴を閉じる。

λ-domain は exact rational に

\[
L=[2/5,699/1600],
\]

\[
X=[699/1600,281/640],
\]

\[
R=[281/640,9/20]
\]

へ分ける。

\(9/20\) は U1 本体には含まれない。空白①では boundary consistency のためだけに使う。

---

## 2. C1a gating inputs — E3 and gate D

### 2.1 Judge ruling E3

`CHAT_AUDIT_THREE_PREDECLARE_DRAFTS_V2_2026-10-10.md`
SHA-256 `43f3d811...10dd` の Judge ruling E3 により、C1a receipt `e494e789` の機械認証済み2符号：

\[
F_x(699/1600)<0,
\qquad
F_x(281/640)>0
\]

を、**空白①に限る gating inputs** として採用する。

C1a receipt 本体の report-only 表示は編集しない。格上げの authority は Judge ruling E3 である。

点推定

\[
\lambda_x\approx0.43775487\ldots
\]

は `REPORTED_EXPECTATION / NON_GATING` のままであり、判定に用いない。

### 2.2 Code K1(b) correction

根数分類は上の2符号だけではなく、C1a gate D：

\[
\boxed{
\partial_\lambda F_x>0
\quad\text{on }[83/200,9/20]
}
\]

にも依存する。

C1 親契約では

\[
F_x(\lambda)
=
\frac{g(1/2,\lambda)}{1/2}
=
2g(1/2,\lambda).
\]

したがって \(F_x\) と \(g(1/2,\lambda)\) は同符号である。

v7 は「2点のみで根数構造が決まる」とは主張しない。2点の certified signs と gate D を組にして使う。

---

## 3. Continuity source — Code K2 correction

\(t\) 方向の根数論理で用いる閉区間上の連続性は、

`OBLATE_ENDPOINT_C1_LEMMA` blob

`5afa815ff24760ab5ebbb63bcbae912c9c7a84c6`

の **Lemma 5** を根拠とする。

適用する λ interval は

\[
I=[2/5,9/20].
\]

Lemma 3 は \(g\) の pre-limit integral representation の根拠として使うが、閉区間 \([1/2,1]\) の continuity の引用は Lemma 5 とする。

---

## 4. L region

\[
L=[2/5,699/1600].
\]

L では predictor、root target、P0/P1/P2 を使わない。

current method は design v2 / numeric contract v1 に従い、

- lower/interior block では direct `g_box<0`
- endpoint block は §7 の cumulative mean-value gate

で

\[
g(t,\lambda)<0
\]

を閉じる。

したがって U1 内の根は 0 個。

失敗時に root search へ切り替えない。

---

## 5. X crossing region

\[
X=[699/1600,281/640].
\]

X では predictor、root localization、P0/P1/P2 を一切使わない。

固定 method：

1. \([1/2,5/8]\times\Lambda\) で
   \[
   \partial_tg=G_t<0
   \]
   を認証。
2. \([5/8,31/32]\times\Lambda\) で
   \[
   g<0
   \]
   を認証。
3. \([31/32,1]\times\Lambda\) は §7 の endpoint gate。

各固定 λ について：

### 5.1 \(g(1/2,\lambda)<0\)

\([1/2,5/8]\) の strict decrease と右側負値から U1 全体で負。

根 0 個。

### 5.2 \(g(1/2,\lambda)>0\)

\(g(5/8,\lambda)<0\)、Lemma 5 の continuity、および \([1/2,5/8]\) の strict decrease から、

\[
(1/2,5/8)
\]

にちょうど1個の根。

\(G_t<0\) なので単純根。

### 5.3 \(g(1/2,\lambda)=0\)

\(t=1/2\) の boundary root のみ。

U1 は \(1/2<t\) なので、U1 内の根は 0 個。

---

## 6. R region and predictor

\[
R=[281/640,9/20].
\]

C1a gate D と \(F_x(281/640)>0\) から、

\[
g(1/2,\lambda)>0
\]

を得る。

R は C1b executed method を最小差分で継承し、λ=9/20 側から低 λ 方向へ進む。

### 6.1 P0 — Code K3 correction

最初の continuation center：

\[
t_{\rm cont}=9/16.
\]

その後は、**右隣の accepted slab の certified root enclosure \(T_*\) の中点**を continuation center とする。

REFINE の場合は

\[
\text{right child first}
\]

で queue に戻し、左向き continuation を壊さない。

### 6.2 P1

P1 の格子符号転換探索は `c785ceda` の executed logic を継承する。

P1 の method を空白①の都合で変更しない。

### 6.3 P2 — Code K4 correction

P2 の authority は説明文書 `5326e2b5`, `4a493191` の header ではない。両文書は `NOT_BINDING` のままである。

空白①が採用する P2 の authority は、C1b machine receipt §1.2 の executed kernels：

- producer `67dda838369302010ef3d589937b834b96ede4d8`
- checker `4eaca55ddf79b437fc756d666294372e5d1a6ba4`

に実装された規則と、この v7 の採用宣言である。

唯一の selection rule：

\[
|\mathrm{continuation}-\mathrm{scan\_mid}|
\le
ROOT\_TARGET
\]

なら continuation。

strict excess なら relocated scan。

等号は continuation 側。

固定値：

\[
W0=1/16,
\qquad
PRED\_ACCEPT=1/64,
\qquad
ROOT\_TARGET=1/128.
\]

`PRED_ACCEPT` を P2 selection threshold に使ってはならない。

### 6.4 ROOT_TARGET の二重の役割

Code K5 の確認どおり、`ROOT_TARGET=1/128` は

1. P2 selection threshold
2. root enclosure target width

の両方に使われる。

`PRED_ACCEPT=1/64` は predictor center と certified root の最終 acceptance distance。

---

## 7. Endpoint method — current rule

endpoint method は `C_GAP_ENDPOINT_ADDENDUM_DRAFT_V2.md`
SHA-256 `7471800d...d3a4` と numeric contract v1 を authority とする。

空白①では

\[
t_e=31/32.
\]

direct `g_box` は seed

\[
g(31/32,\lambda)
\]

の1回だけ。

\([31/32,1]\) は16等分：

\[
t_j=31/32+j/512,
\qquad
j=0,\ldots,16.
\]

各

\[
Q_j=[t_j,t_{j+1}]\times\Lambda
\]

で

\[
U_j=\sup_{Q_j}G_t
\]

を interval enclosure する。

成功条件は唯一：

\[
\boxed{
U_{\rm cum}
=
\sup_{\lambda\in\Lambda}g(31/32,\lambda)
+
\sum_{j=0}^{15}
\frac1{512}\max(0,U_j)
<0
}.
\]

禁止：

- \((31/32,1)\) で direct `g_box` を使うこと
- runtime で \(C_\Lambda(1-t)\) へ切り替えること
- `Gt<0` を各 box の必要条件にすること
- partition を run 中に変えること
- B_ob receipt で endpoint failure を救済すること

### 7.1 B_ob

endpoint certificate が通れば、G0/E1 continuity により

\[
g(1,\lambda)=B_{\rm ob}(\lambda)<0
\]

は帰結する。

したがって `B_ob<0` は独立 gating condition ではない。

既存 B_ob receipt は sign-consistency check のみ。

---

## 8. Implementation authority and diff contract

### 8.1 C1b executed-code authority — 7 files

| lineage | role | path | blob |
|---|---|---|---|
| producer | kernel | `producer/global_axial_c1b_kernel.py` | `67dda838369302010ef3d589937b834b96ede4d8` |
| producer | gating | `producer/global_axial_c1b_gating.py` | `a93ca173ae0bededcd5a0248aa07ac3348f9a243` |
| producer | producer | `producer/global_axial_c1b_producer.py` | `0616fbd7c9c85f77c8e80b61a5b3b536b45012a8` |
| producer | driver | `analysis/c1b_resumable_driver.py` | `5fd308bb4c02c6ddbd612ddbedb18f6b9e22bc3d` |
| checker | kernel | `checker/global_axial_c1b_kernel.py` | `4eaca55ddf79b437fc756d666294372e5d1a6ba4` |
| checker | gating | `checker/global_axial_c1b_gating.py` | `03df262012bfbebcf4d2ea173933186c70abafbf` |
| checker | checker | `checker/global_axial_c1b_checker.py` | `0760764ef7592be1ddd4ffec3966e9c6ec930a5b` |

implementation head：

`85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b`.

### 8.2 Allowed differences

design v2 SHA-256 `0a407d1b...38d1` の allowlist：

- `DIFF-A`：R の左向き queue / right-child-first
- `DIFF-B`：X fixed path
- `DIFF-C`：L root-free negative path
- `DIFF-D`：endpoint cumulative mean-value path
- `DIFF-E`：必要な dispatcher / replay / ledger wiring
- `DIFF-K`：①固有の domain constants / self-test controls

以外の behavioural hunk は許可しない。

未分類 hunk が1つでもあれば

`DIFF_OUTSIDE_ALLOWLIST`.

### 8.3 Imported baseline modules

design v2 §4 の **15-module import closure** は、同文書に pin された blobs と byte-identical でなければならない。

新実装から別 blob の同名 module を読むことは禁止。

### 8.4 27 amendment documents

27件の C1b amendment / addendum の一覧は

`CHAT_AUDIT_C_GAP1_V4_AND_G0_V0_2026-10-10.md`
SHA-256 `f8a1f954...03df1`, finding J2

を provenance list とする。

これら27文書は実装内容の説明資料であり、executed behaviour の authority は §8.1 の code blobs。

特に P2 の authority は §6.3 に従う。

---

## 9. Numeric contract

数値仕様の唯一の current authority は

`C_GAP_NUMERIC_CONTRACT_DRAFT_V1.md`
SHA-256 `be67046f8bb2d6cb5b3c0e615ee7edb1338d91956f6eb1aa2701217c05600d07`.

主要な current choices：

- λ coarse width \(1/3200\)
- L/X/R = 118 / 7 / 35 coarse slabs、total 160
- `MAX_DEPTH=3`
- producer fixed 160 bits
- checker fixed 192 bits
- approximation / series degree 50
- runtime precision escalation 禁止
- endpoint 16 boxes of width \(1/512\)
- resource / work ceilings は numeric contract v1 の値を使用

ここに書いていない stage constants、panel counts、work caps も numeric contract v1 exact SHA の値が binding candidate。

---

## 10. Fail-closed vocabulary — Code K10 correction

v6 の

`CERTIFICATE_INCONCLUSIVE`

は current numeric contract における各種 inconclusive code の**上位分類名**とする。

少なくとも：

- `PRECISION_INCONCLUSIVE`
- `APPROX_DEGREE_INCONCLUSIVE`
- `ENDPOINT_SEED_G_INCONCLUSIVE`
- `ENDPOINT_GT_CELL_INCONCLUSIVE`
- `ENDPOINT_CUMULATIVE_MVT_INCONCLUSIVE`
- その他 `*_INCONCLUSIVE`

はすべて

\[
\texttt{CERTIFICATE\_INCONCLUSIVE}
\]

の細分類。

別分類として：

- `NONFINITE`
- `RESOURCE_CAP`
- `CONTRACT_MISMATCH`
- `DIFF_OUTSIDE_ALLOWLIST`
- `IMPORT_BLOB_MISMATCH`
- `PREDICTOR_RULE_MISMATCH`

を保つ。

いずれも、それだけでは数学的反例を意味しない。

method / enclosure / resource failure と mathematical contradiction を混同しない。

---

## 11. Boundary ownership and overlap audit — Code K11 correction

### 11.1 \(\lambda=699/1600\)

canonical owner：X。

L は overlap consistency。

比較するもの：

- root count = 0 が両側で一致
- \(g(1/2)<0\) の sign classification が一致

不一致は `CONTRACT_MISMATCH`。

### 11.2 \(\lambda=281/640\)

canonical owner：R。

X は overlap consistency。

比較するもの：

- root count = 1 が両側で一致
- R の certified root enclosure \(T_*\) が
  \[
  (1/2,5/8)
  \]
  と交わる

不一致は `CONTRACT_MISMATCH`。

### 11.3 \(\lambda=9/20\)

U1 本体には含まれない。

空白①は consistency only。

上側の canonical responsibility は既存 C1b / 空白②。

---

## 12. G0/E1 dependency and D6

G0/E1 v3：

`G0_E1_UNIFORM_GT_PAPER_PROOF_DRAFT_V3.md`  
SHA-256 `8bf8f5d87cfc2e6f424499804b0fd85d982cf480deb99a26c284367960578671`

は text audit PASS。

その内容には：

- paper derivation
- \(G_t=T_1+T_2+T_3\) の symbolic identity check
- machine Gt source-formula identification

が含まれる。

ただし source lemmas：

- `5afa815ff24760ab5ebbb63bcbae912c9c7a84c6`
- `7cb9b8091596510203d74e09387bc1e8188b8b47`

は D6 independent audit の対象。

Judge ruling により：

- Astra が両補題を full independent audit
- `AI_AUDIT_PASS` なら FREEZE 目的の D6 は discharge
- 論文本文で theorem を `CLOSED` と記載するには
  `HUMAN_EXTERNAL_AUDIT_PENDING`
  が別条件として残る

とする。

D6 PASS 前にこの依存を消えたものとして扱わない。

---

## 13. Producer / checker independence

producer と checker は別 lineage を維持する。

checker は producer の interval result を信用せず、同じ contract / exact rational boxes に対して独立再計算する。

producer から checker に渡せるのは、契約で許した exact replay labels / box endpoints / decision labels のみ。

数値 enclosure を流用しない。

---

## 14. FREEZE prerequisites

v7 は次が閉じるまで FREEZE しない。

1. **v7 自身の CHAT AUDIT → Judge FREEZE**
2. **D6 Astra independent audit PASS**
3. **① new implementation**
4. **full diff audit**
   - baseline 7 files
   - 15-module import closure
   - all hunks classified DIFF-A/B/C/D/E/K
   - unclassified hunk = 0
5. **producer/checker controls PASS**
6. **Judge scheduling ruling**
   - D5 と C 空白①を研究 PC 上で同時占有しない

② L0 seal path / SHA 4/4 match は STATE v1.15 で RESOLVED 済みであり、① v7 の blocker ではない。

---

## 15. Execution authorization

FREEZE と実行許可は別工程。

順序：

\[
\boxed{
\text{v7 DRAFT}
\to
\text{CHAT AUDIT}
\to
\text{Judge FREEZE}
\to
\text{implementation/diff state confirmation}
\to
\text{separate execution authorization}
\to
\text{producer run}
\to
\text{independent checker}
\to
\text{receipt audit}
}
\]

FAIL-CLOSED を維持する。

FREEZE だけでは本走を開始しない。

---

## 16. Current status

**C 空白① v7：DRAFT / NOT FROZEN / EXECUTION PROHIBITED。**

この v7 は Code 独立監査の accepted findings：

- K1(b)
- K2
- K3
- K4
- K10
- K11

を反映する。

K1(a) は新規裁定ではなく、既存 Judge ruling E3 を引用して解消する。

K6–K9 は後続文書を exact SHA で取り込み、v6 の旧記述を supersede する。

K14 は STATE v1.15 / main `8bc2c005...` で design v2 が保存済みとなったため、repo 保存欠落としては解消済み。

**数値計算・実装・commit・push はこの草稿作成では行っていない。**
