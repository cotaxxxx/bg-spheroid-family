# Code 宛実装指示書 DRAFT v2 — C 空白①（2026-10-11）

発行予定：Judge（ユーザー）／起草：ChatGPT（GPT-6）  
**状態：INSTRUCTION DRAFT v2 / B1–B3 CORRECTED / JUDGE REVIEW REQUIRED / NOT ISSUED / NOT FROZEN / NO NUMERIC RUN / NO CERTIFICATE / NO COMMIT / NO PUSH**  
**作業種別：新規①コードの実装準備と静的検証。D6 の READ-ONLY 監査とは別件。**

> この指示書は、Judge が確認して Code に正式発出するための**未承認草稿**である。**この文書の共有・閲覧だけでは実装着手を許可しない。** Judge が B1（15＋2 pin）と B2（共有 driver の境界）を含めて明示的に受理・発出した場合に限り、隔離された作業領域で①専用コードの作成・静的検証・差分提出を許可する。**数値本走、証明書生成、数学的 PASS 判定、commit、push、既存コードの上書き、v7 の FREEZE は許可しない。**

## 0. 目的と現在状態

対象は C 系列の未被覆領域

\[
U_1=\{(t,\lambda):1/2<t\le1,\ 2/5\le\lambda<9/20\}.
\]

Judge が指定した **FREEZE 候補は v7 原本**であり、監査済み転送文面との同一性は確認済み。**Judge FREEZE は未実施**。実装と差分監査、D5・C 空白・扁長の計算順序に関する Judge 裁定が残る。

D6 は Judge 裁定により **`CROSS_LINEAGE_AI_AUDIT_PASS`（FREEZE 用の入力として充足）**。ただし論文で `CLOSED` と書くための補題 v1.1・同監査・Astra 監査・人間外部監査は別工程である。D6 の原補題は変更しない。

本指示書の成功条件は **「実装案7ファイル＋全差分・静的 controls・既存15 pin＋補足2 pin（計17）の照合証跡を、chat が独立監査できる状態で提出する」**ことである。**この段階で `ACCEPT` や証明完了を宣言しない。**

## 1. Authority と exact pins（着手前に照合）

### 1.1 管理正本

- `bg-spheroid-family` main：`201d4808d8cd34d527ad1d8bdc180037dd5605b7`、`STATE.md` **v1.19**。
- FREEZE 候補：`drafts/2026-10-11/C_GAP1_CONTRACT_DRAFT_V7.md`、SHA-256 **`a49148180fdeb33272e7358028caa55ec1dc06e5d4f526cd23eca50ff65c2a37`**（687行、16371 bytes）。
- 実装設計：`drafts/2026-10-10/C_GAP1_IMPLEMENTATION_DESIGN_DRAFT_V2.md`、SHA-256 **`0a407d1bec2d491befc2bdaee7dbfff29b3f93bf54f3aef466093dd9453038d1`**。
- 端点追補：`drafts/2026-10-10/C_GAP_ENDPOINT_ADDENDUM_DRAFT_V2.md`、SHA-256 **`7471800d81caabdbbe3bfb5c8dc2e020434adbd0a67ed4e6bbd38afbea33d3a4`**。
- 数値契約：`drafts/2026-10-10/C_GAP_NUMERIC_CONTRACT_DRAFT_V1.md`、SHA-256 **`be67046f8bb2d6cb5b3c0e615ee7edb1338d91956f6eb1aa2701217c05600d07`**。
- 端点合法性／Gₜ 紙上証明：`drafts/2026-10-10/G0_E1_UNIFORM_GT_PAPER_PROOF_DRAFT_V3.md`、SHA-256 **`8bf8f5d87cfc2e6f424499804b0fd85d982cf480deb99a26c284367960578671`**。
- v7 拘束補足：`audits/CHAT_RECORD_V7_CLARIFICATIONS_2026-10-11.md`、SHA-256 **`541f3025728e027467433d2ff05ef12299b7cc2c6488fbe8bf2febe73fcf4d7c`**。
- v7 原本・監査文面の同一性：`audits/CHAT_RECORD_V7_EXACT_FILE_IDENTITY_2026-10-11.md`、SHA-256 **`7118070bd071e0ee59b769dec528537515bbf8d98b5ce26fa2bf6e1494df9439`**。
- v7 の CHAT AUDIT：`audits/CHAT_AUDIT_C_GAP1_V7_2026-10-11.md`、SHA-256 **`b177c450e5eb97a7415921432f06f78b0c3dd7f9e382ad61084b345a3ffcfc67`**。

v7 の文書内には作成時点の古い STATE / D6 状態が残る。**後日の Judge 裁定と STATE v1.19 により、D6 は FREEZE 用に充足、Astra は論文 CLOSED 前の条件**となった。v7 の原本 `a4914818…` は編集せず、後日の拘束記録とともに読む。矛盾を独断で書き換えない。

### 1.2 実装元：C1b executed code（7本）

`bg-oblate-spheroid` の C1b implementation commit **`85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b`** を source authority とする。着手前に、下記の **path → Git blob** が一致することを確認する。

| # | lineage / role | baseline path | Git blob |
|---|---|---|---|
| 1 | producer / kernel | `producer/global_axial_c1b_kernel.py` | `67dda838369302010ef3d589937b834b96ede4d8` |
| 2 | producer / gating | `producer/global_axial_c1b_gating.py` | `a93ca173ae0bededcd5a0248aa07ac3348f9a243` |
| 3 | producer / producer | `producer/global_axial_c1b_producer.py` | `0616fbd7c9c85f77c8e80b61a5b3b536b45012a8` |
| 4 | producer / driver | `analysis/c1b_resumable_driver.py` | `5fd308bb4c02c6ddbd612ddbedb18f6b9e22bc3d` |
| 5 | checker / kernel | `checker/global_axial_c1b_kernel.py` | `4eaca55ddf79b437fc756d666294372e5d1a6ba4` |
| 6 | checker / gating | `checker/global_axial_c1b_gating.py` | `03df262012bfbebcf4d2ea173933186c70abafbf` |
| 7 | checker / checker | `checker/global_axial_c1b_checker.py` | `0760764ef7592be1ddd4ffec3966e9c6ec930a5b` |

**既存7ファイルを上書きしない。** 対応する①専用の**別 path の新規7ファイル**を作り、元ファイルと1対1で全文 diff が取れるようにする。具体的な新 path と import 解決方法を、最初に一覧で宣言する。**原則は `gap1_producer/` に3本、`gap1_checker/` に3本、`gap1_analysis/` に共通 driver 1本を置き、各 kernel/gating/entry point の既存 basename を維持する候補配置**とする（§1.5）。この配置だけで import が正しく解決するとはみなさない。追加の executable module や既存ファイル変更が不可避なら、実装前に停止して理由と差分候補を提出する。

### 1.3 既存契約が列挙した不変 import pins（15本）

下記15本は **元の Git blob と byte-identical** とする。これは v7・実装設計 v2 が列挙した15本の集合であって、C1b 基準コードの全依存を網羅した集合ではない。**既存の横断 import は削除・変更しない**（§1.4）。新規①コードによる同名 shadowing、既存依存の差替え、producer/checker の新規数値相互依存は禁止する。静的 import graph と想定 import resolution の両方を示す。

| lineage | baseline module | Git blob |
|---|---|---|
| producer | `producer/monotone_tube_refinement_producer.py` | `c2fee40053ab055ce352e93e1c6d1fc43e46310a` |
| checker | `checker/monotone_tube_refinement_checker.py` | `15d660265552fc2f2c83ffe897ed5efab8514da2` |
| checker | `checker/monotone_tube_interval_checker.py` | `f2fa2a5a42d35b8b77e3c63fa0d9ad48ce562a77` |
| producer | `producer/global_axial_c1b_endpoint_r.py` | `29d441a578f10fe7f4beb38476d3699f3648a3b1` |
| checker | `checker/global_axial_c1b_endpoint_r.py` | `1a953b22c12a89afc06790b28d6b0dea9680dc43` |
| producer | `producer/endpoint_interval_producer.py` | `51060fea01cb9ff661518b7c52146f71187846ff` |
| producer | `producer/monotone_tube_interval_producer.py` | `b6d96df223c0e423e804d96f4892a8e818c05827` |
| producer | `producer/global_axial_c0_producer.py` | `c4c8d6b59d3829e1843d149b7857eda5800287aa` |
| checker | `checker/global_axial_c0_checker.py` | `85978625e029b01c8ae40fa8234566f10eea251c` |
| checker | `checker/endpoint_local_controls.py` | `c913c47d228e51a15f56957f5df9196efa1b22c3` |
| checker | `checker/oblate_axis_prototype.py` | `df402583c320c459ff4f72dc5294558f14f44d31` |
| checker | `checker/endpoint_interval_checker.py` | `4cb16f8a975e5a3be601a7926af695ad5be57790` |
| checker | `checker/endpoint_local_checker.py` | `2bddddf6e9a08ca7acae94c89bd4d5ab1de861bc` |
| producer | `producer/global_axial_c0_producer_v2.py` | `cdbdf51f8656c1fcae97666cc1846461b250a591` |
| checker | `checker/global_axial_c0_checker_v2.py` | `fbec890588d2d390ea67bc90116b80bb37ebf9cc` |

`IMPORT_BLOB_MISMATCH` または同名 shadowing の可能性があれば即停止。参照した commit / path / blob と import resolution を報告する。

### 1.4 B1：C1b の追加依存2本と B2：既存横断 import の拘束補足（Judge 受理待ち）

**B1：15本は全閉包ではない。** 基準 commit `85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b` の両 kernel は、L20 で `c0a_four_group_v2` を import する。さらに両 kernel の `C1B_NUMERIC_IMPORT_CLOSURE` 辞書に次の2本がすでに明記されている。

| lineage | 追加 pin（既存ファイル、変更禁止） | Git blob |
|---|---|---|
| producer | `producer/c0a_four_group_v2.py` | `2bb556ab4f0c0cfd9ce6afa65d762551dd3791f4` |
| checker | `checker/c0a_four_group_v2.py` | `18e66b6450cd2a379bbb869a99e4e5ce6999f6e5` |

**提案する拘束読み：** v7 と設計 v2 の「15本」は**当初列挙された15本**を指す。実装の静的依存検査・byte identity 検査の対象は**15＋追加2＝17本**とする。**これは数学的な方法・数値契約・7本の変更 allowlist を変えないが、原契約の実装監査対象を補完するため Judge の明示的受理を要する。** v7 原本 `a4914818…` と設計 v2 原本 `0a407d1b…` は編集しない。受理された場合は、別の拘束記録にこの2本と Judge 裁定を保存する。未受理のままなら `BLOCKED:IMPORT_CLOSURE_UNPINNED` で実装開始前に停止する。新たな依存漏れがあれば17本で打ち切らず、停止して追加審査を求める。

**B2：baseline の横断依存は既存の事実として維持する。** `producer/endpoint_interval_producer.py` は `checker/endpoint_local_controls.py` と `checker/oblate_axis_prototype.py` を import する。`producer/global_axial_c1b_gating.py` と `checker/global_axial_c1b_gating.py` はともに `analysis/c1b_resumable_driver.py` を import する。これらの**既存の、pin 済みの依存**は横断 import の一般禁止によって不適合扱いしない。

**新規①コードの禁止境界：** checker が `gap1_producer.*` や producer 側の新規 kernel/gating/entry point を import して数値評価・判定・区間上界を共有することは禁止。producer が `gap1_checker.*` を参照することも原則禁止。既存 pin 済みの横断依存は例外としてそのまま認めるが、**新規の横断依存を既存依存に偽装して追加しない**。

**共通 driver の裁定提案：** `gap1_analysis/c1b_resumable_driver.py` を7本のうちの共通1本とし、producer と checker の双方から import してよい。ただし共有可能なのは**exact rational label、非数値的な schema・serialization・persistence・replay plan** の機能に限る。producer の区間上界、判定結果、認証計算、数値 kernel、producer 固有の成功ロジックを checker に提供してはならない。checker は独立した区間計算と判定を行う。**この共通 driver の境界も Judge 受理待ち**。共通化が checker の独立性を損なう場合は `BLOCKED:CHECKER_INDEPENDENCE` とし、勝手に新規8本目を増やさない。

### 1.5 B3：パッケージ配置と動的 import の固定（静的検証が必須）

基準の両 kernel にある `_v212_c6_write_through` は、`lineage = __name__.split(".", 1)[0]` を使い、`importlib.import_module(lineage + ".global_axial_c1b_gating")` で gating を動的に読む。さらに `_v211_schema_counts` は `Path(__file__).with_name("global_axial_c1b_gating.py")` を参照する。したがって既存 `producer/`・`checker/` 内に**別名の①ファイル**を置く案は、baseline gating を誤参照する危険がある。

**原則的な候補配置（7本）**：

| baseline | ①候補 path |
|---|---|
| `producer/global_axial_c1b_kernel.py` | `gap1_producer/global_axial_c1b_kernel.py` |
| `producer/global_axial_c1b_gating.py` | `gap1_producer/global_axial_c1b_gating.py` |
| `producer/global_axial_c1b_producer.py` | `gap1_producer/global_axial_c1b_producer.py` |
| `analysis/c1b_resumable_driver.py` | `gap1_analysis/c1b_resumable_driver.py` |
| `checker/global_axial_c1b_kernel.py` | `gap1_checker/global_axial_c1b_kernel.py` |
| `checker/global_axial_c1b_gating.py` | `gap1_checker/global_axial_c1b_gating.py` |
| `checker/global_axial_c1b_checker.py` | `gap1_checker/global_axial_c1b_checker.py` |

Code は、**数値コードを import / 実行せず**、AST とファイル配置の静的検査で以下を確認する：
1. 各新規 kernel の動的 `lineage` が自身の① package に解決され、対応する① gating の path に向く。baseline gating への silent fallback がない。
2. 各新規 entry point と gating の import が、① kernel/gating/共通 driver を参照し、baseline の7ファイルを誤参照しない。
3. 既存依存17本は **元の `producer.*` / `checker.*` に解決**され、指定 Git blob と一致する。`c0a_four_group_v2` の2本も含む。
4. 既存の hardcoded package 名、`C1B_NUMERIC_ROOTS` / `C1B_NUMERIC_IMPORT_CLOSURE`、`Path(__file__)` を用いる preflight・schema checks が① package の配置で何を読むかを**呼出し箇所ごとに列挙**する。baseline 数値核・P1/P2 本体の変更は禁止する。必要な path/metadata の修正は DIFF-E または DIFF-K の範囲でのみ提案し、根拠を示す。
5. AST だけでは動的解決を確定できない部分は `NOT_VERIFIED` とし、発出前・差分監査時に不確実性を報告する。**新 package 名だけで安全性が証明されたと扱わない。**

この7本構成で実現できない場合は、**既存ファイル変更や追加 executable module に進まず停止**し、代替配置案と必要な Judge 裁定を提出する。

## 2. 実装差分の絶対制限

**全 behavioral hunk を次のいずれか1分類へ対応付ける。** 1件でも分類不能なら `DIFF_OUTSIDE_ALLOWLIST` として停止。

- **DIFF-A**：R の高λ→低λ queue、REFINE 時の right-child-first。predictor / P1 / P2 本体は不変。
- **DIFF-B**：X の fixed path。predictor と root localization を呼ばない。
- **DIFF-C**：L の root-free negative path。predictor と root localization を呼ばない。
- **DIFF-D**：L/X/R 共通の endpoint seed + 16 Gₜ boxes + cumulative mean-value gate。
- **DIFF-E**：上記を実現する最小限の region dispatcher、ledger、replay、入力配線。
- **DIFF-K**：①固有の λ 境界、coarse slab 定数、方向表示、domain-dependent self-test/control、ledger metadata のみ。

変更禁止：`g_box` / `gt_box` の積分核、ordinary/corner `T1,T2,T3`、interval arithmetic と endpoint chart の数式、`P1` scan 符号転換、`P2` selection body、root localization target-width、`W0=1/16`、`PRED_ACCEPT=1/64`、`ROOT_TARGET=1/128`。差分監査では **式の同一性だけでなく該当 body の byte identity** を可能な範囲で検証する。元の body を修正する必要が生じたら停止する。

## 3. λ region / boundary ownership

exact rational のみ使用する。

| region | λ interval | coarse slabs（幅1/3200） | method |
|---|---|---:|---|
| L | `[2/5,699/1600]` | 118 | interior `g_box<0` + endpoint |
| X | `[699/1600,281/640]` | 7 | lower `Gₜ<0` + negative `g<0` + endpoint |
| R | `[281/640,9/20]` | 35 | C1b tube/root + endpoint |

**total 160 coarse slabs**。region を跨ぐ slab を作らない。共有辺は両側で検算してよいが canonical owner は次のとおり。

- λ=`699/1600`：**X owner**、L は overlap check。両側で **root count 0** と `g(1/2)<0` の符号分類が一致すること。
- λ=`281/640`：**R owner**、X は overlap check。両側で **root count 1**、R の certified enclosure `T_*` と `(1/2,5/8)` の交差を確認。
- λ=`9/20`：U₁ 本体には含めない。①は boundary consistency only、上側 owner は既存 C1b / 空白②。

C1a receipt `e494e789` の certified signs `F_x(699/1600)<0`, `F_x(281/640)>0` は、**Judge ruling E3 によって①に限る gating inputs**。併せて C1a gate D：`∂_λ F_x>0` on `[83/200,9/20]` を使う。`F_x=2g(1/2,λ)`。`λ_x≈0.43775487…` は `REPORTED_EXPECTATION / NON_GATING`、分岐条件に使用しない。C1a receipt 自体は編集しない。

## 4. Region 固有の実装

### 4.1 L：root-free negative

- `[1/2,31/32]×Λ`：direct `g_box` の **strict upper < 0** を認証する path。
- `[31/32,1]×Λ`：§5 の endpoint gate。
- predictor / P0 / P1 / P2 / root localization は**到達不能**。
- 失敗時に root search に切り替えない。predeclared refinement が尽きれば `CERTIFICATE_INCONCLUSIVE` の該当細分類。

### 4.2 X：固定3ブロック

- `[1/2,5/8]×Λ`：direct `gt_box` で **`sup Gₜ<0`**。
- `[5/8,31/32]×Λ`：direct `g_box` で **`sup g<0`**。
- `[31/32,1]×Λ`：§5 endpoint gate。
- `t=5/8` の canonical sign owner は negative block。`t=31/32` は endpoint seed。重複閉辺は overlap consistency のみ。
- predictor / P0 / P1 / P2 / root localization は**到達不能**。失敗時の fallback も禁止。
- `g(1/2)<0` なら U₁ 内0根、`>0` なら `(1/2,5/8)` に単純根1個、`=0` なら `t=1/2` の境界根のみで U₁ 内0根。判定には certified C1a signs と gate D を使用する。
- ①における X の `∂ₜg=Gₜ` は **G0/E1 v3** に依存。`g(1/2,λ)=∂ₜ⁺E` の値と `∂ₜg` を混同しない（D6 の B2/K2）。`6fba6e4f` は U₁ の①結論の依存ではなく、C cover の `t≤1/2` 側に残る。

### 4.3 R：C1b continuation を逆方向に運ぶ

- λ を**高→低**へ処理。初回 `t_cont=9/16`。
- 以後、**右隣の ACCEPTED slab** の certified root enclosure `T_*` の中点を continuation center にする。REFINE で previous_root を更新しない。
- REFINE は **right child first**。他の predictor や探索方式への fallback を作らない。
- `P1` は baseline executed grid scan を保持。
- **P2 は** `abs(continuation-scan_mid) <= ROOT_TARGET` なら continuation、strict excess なら relocated。**等号は continuation 側**。`ROOT_TARGET=1/128` は P2 threshold と root enclosure target width の両用。`PRED_ACCEPT=1/64` は final acceptance distance であり P2 threshold ではない。
- `F_x(281/640)>0` と gate D から R の `g(1/2,λ)>0`。tube の left exterior `g>0`、tube 内 `∂ₜg<0`、right exterior `g<0`、§5 endpoint gate により、**各 λ∈R∩[2/5,9/20) で U₁ 内ちょうど1個の単純根**。この結論は拘束補足 `541f3025…` に従う。

## 5. L/X/R 共通：endpoint gate（DIFF-D）

固定 seed `t_e=31/32`、固定16区間

\[
t_j=31/32+j/512\quad(j=0,\dots,16),\qquad
Q_j=[t_j,t_{j+1}]\times\Lambda.
\]

各 current λ slab Λ に対して：

1. `g_box` は **seed `g(31/32,Λ)` だけを1回**評価し、その certified upper bound を `G_seed` とする。seed s-panels=8192。
2. 16個の `Q_j` で **全て** `gt_box` の certified upper `U_j` を得る。各 s-panels=8192。`j=0…14` は ordinary、`j=15` は既存 corner/ordinary endpoint dispatch。
3. certified interval upper を使い、外向き丸めで
   \[
   U_{\mathrm{cum}}=G_{\mathrm{seed}}+\sum_{j=0}^{15}\frac1{512}\max(0,U_j)
   \]
   を評価する。**唯一の endpoint 成功条件は `U_cum < 0`**。`G_seed<0` は必要だが、それ単独で ACCEPT しない。
4. λ を事前宣言範囲内で refine しても、**同じ16 t-boxes** を再使用する。追加 t refinement は禁止。

**禁止：** `(31/32,1)` 内の direct `g_box`、`C_Λ(1-t)` への runtime switch、`U_j<0` を各 box の必要条件にすること、`max(0,U_j)` を point estimate / midpoint に替えること、端点で B_ob receipt を代替 gate にすること。`g(1,λ)=B_ob(λ)<0` は endpoint certificate と continuity の**帰結**。既存 B_ob receipt は **NON-GATING CONSISTENCY CHECK** のみで、不一致は fail-closed。

## 6. 固定 numeric contract（①のみ）

**次の値をコードと ledger metadata に固定し、runtime adaptive escalation を実装しない。** 詳細・未掲示定数は必ず numeric contract v1 exact SHA に従う。②の precision ladder と混同しない。

| item | value |
|---|---|
| λ coarse width | `1/3200` |
| L / X / R | `118 / 7 / 35` slabs |
| MAX_DEPTH | `3` |
| MAX_ACCEPTED / MAX_ATTEMPTED | `1280 / 2400` |
| producer / checker precision | `160 / 192 bits` |
| approximation degree | `50` |
| U_STAR / W0 | `3/5` / `1/16` |
| PRED_ACCEPT / ROOT_TARGET | `1/64` / `1/128` |
| R PRED_GRID_DEN / PRED_SCAN_PANELS | `1024 / 256` |
| R tube T0 / T1 / T2 | `8×4×4096` / `16×8×4096` / `32×16×8192` |
| R root MV steps | `8` |
| R root G / Gₜ / Gλ s-panels | `32768 / 8192 / 8192` |
| R root Gₜ / Gλ t-cells | `16 / 16` |
| R ROOT_GL_CORNER_K / TAU | `16` / `65535/65536` |
| R ROOT_GT_CLAMP_TAU | `255/256` |
| R ROOT_GL_CORNER_WALL_PANELS | `8192` |
| R ROOT_GT_REFINE_DEPTH / T2_ENDPOINT_REFINE_DEPTH | `2 / 4` |
| L interior E0 t/λ boxes | `24 / 8` |
| L interior panel ladder | `1024→2048→4096` |
| X lower tube T0/T1/T2 | `8×4×4096` / `16×8×4096` / `32×16×8192` |
| X negative block t/λ boxes | `24 / 8` |
| X negative block panel ladder | `1024→2048→4096` |
| E_BOX_CAP / MONO_WORK_CAP | `4096 / 1,048,576` |
| endpoint seed / each Gₜ box panels | `8192 / 8192` |
| endpoint t partition | `16 × (1/512)` |
| ATTEMPT_WORK_CEILING | `25,600,000` |
| GLOBAL_ATTEMPT_WORK_CEILING | `61,440,000,000` |
| ACCEPTED_WORK_CEILING | `32,768,000,000` |
| CPU / RAM / output budgets | `96 core-hours / 32 GiB / 10 GiB` |

これらは**実行の予算許可ではない**。今は定数の静的実装だけを行う。未確定値や仕様衝突を勝手に補完しない。

## 7. Ledger、replay、独立 checker

最低限の ledger fields：`region`, `diff_categories_used`, exact `lambda_lo/hi`, `coarse_index`, `depth`, `endpoint_partition_id`, `endpoint_seed_t`, `endpoint_seed_g_upper`, **16**個の endpoint Gₜ box labels と upper bounds、**16**個の `max(0,U_j)` contributions、`endpoint_cumulative_mvt_upper`, L/X/R guards、R のみ predictor/root fields、baseline blob pins、numeric contract SHA、producer/checker lineage と version。

- L/X の predictor/root fields は null。非 null なら `CONTRACT_MISMATCH`。
- R の P2 rule の旧式が記録されたら `PREDICTOR_RULE_MISMATCH` または `CONTRACT_MISMATCH`。
- exact rational box labels、decision labels、replay plan は checker に渡してよい。
- **producer interval bounds / enclosure / 成功判定を checker が流用することは禁止**。checker は独立 kernel / precision / interval evaluation で再計算する。checker が producer の新規 module を import しないことを静的に示す。**Judge が B2 を受理した場合に限り**、両系統が `gap1_analysis` の共通 driver のうち非数値 schema・persistence・replay plan 機能を利用することは認める。共有 driver が数値計算や producer 判定を checker に供給しないことを静的に検査する。
- accepted slab と共有境界の重複・欠落・所有者不一致を fail-closed とする。

## 8. Fail-closed と禁止 fallback

少なくとも次の分類を保つ：

- `CERTIFICATE_INCONCLUSIVE`（umbrella）と細分類 `PRECISION_INCONCLUSIVE`, `APPROX_DEGREE_INCONCLUSIVE`, `ENDPOINT_SEED_G_INCONCLUSIVE`, `ENDPOINT_GT_CELL_INCONCLUSIVE`, `ENDPOINT_CUMULATIVE_MVT_INCONCLUSIVE`、その他 `*_INCONCLUSIVE`。
- `NONFINITE`, `RESOURCE_CAP`, `CONTRACT_MISMATCH`, `DIFF_OUTSIDE_ALLOWLIST`, `IMPORT_BLOB_MISMATCH`, `PREDICTOR_RULE_MISMATCH`。
- endpoint 追補の `ENDPOINT_PARTITION_MISMATCH`, `ENDPOINT_NONFINITE`, `ENDPOINT_RESOURCE_CAP`, `BOB_SIGN_CONSISTENCY_FAILED` も保持する。

これらは**数学的反例を意味しない**。不確定を `ACCEPT` に読み替えず、precision / degree / panel count / endpoint method / region method を実行中に変更しない。

## 9. 今回許す静的 controls（数値実行は禁止）

**許可：** `git cat-file` / `git rev-parse` / `git show` / `git hash-object`、SHA-256 照合、全文 diff、`git diff --check` 相当の whitespace check、Python ソースの **AST parse / compile-only（import 実行なし）**、静的 import graph、**AST による動的 import 呼出しの発見と path 推定（import は実行しない）**、到達可能性・分岐条件のソース検査、exact rational 定数のソース比較。静的 control を走らせた場合は、コードと出力を両方提出する。

**禁止：** producer / checker / driver の実行、`g_box` / `gt_box` / interval kernel の呼出し、数値探索、smoke run、証明書や receipt の生成、実行結果を使うチューニング、runtime precision escalation、commit、push、既存 C1b 7本や import 17本（当初15本＋補足2本）の編集。作業ツリーの既存未追跡ファイルは触らない。**B1/B2 の Judge 受理前は新規実装ファイルの作成も行わない。**

必須の静的 controls（各々 `PASS / FAIL / NOT_VERIFIED` を記載）：

1. 元7ファイルと import **15＋2＝17本**の blob pin が一致し、追加2本について Judge の拘束補足が受理されている。
2. ①の新規7ファイルだけが executable な新規変更であり、既存 baseline に変更がない。
3. 全 behavioral hunk に DIFF-A/B/C/D/E/K の分類があり、未分類0。
4. P1/P2 body、`g_box` / `gt_box`、ordinary/corner `T1,T2,T3`、root localization の不変性。
5. L/X から predictor/root machinery へ到達不能。失敗時の fallback もない。
6. R は descending queue、right-child-first、accepted right-neighbor midpoint、P2 `<=ROOT_TARGET`（等号 continuation）。
7. endpoint は seed g 一回＋固定16 Gₜ boxes＋累積 `U_cum<0` **以外の成功経路がない**。内部 direct g_box、CΛ fallback、B_ob gate は到達不能。
8. shared λ / t edge の owner と overlap checks が契約どおり。
9. producer/checker が独立し、checker が producer enclosure / `gap1_producer.*` を import しない。既存 pin 済み横断 import と、Judge が受理した共通 `gap1_analysis` driver の非数値機能だけを例外とする。
10. 全 caps、固定精度、degree、failure codes と ledger schema が numeric contract v1 と一致する。加えて B3 の**動的 gating import と hardcoded preflight path** を静的に解決し、baseline gating への silent fallback がない（未証明なら `NOT_VERIFIED`）。

静的解析では証明できない項目は、**`NOT_VERIFIED` と理由・将来必要なテストを記す**。動的にしか検証できない性質を静的 PASS と偽らない。数値テストの実施は Judge の別途許可を待つ。

## 10. 提出物と停止条件

Code は以下を提出する。**差分の要約だけでは不可。**

1. `IMPLEMENTATION_REPORT_V0.md`：作業環境、baseline commit/branch、参照した authority SHA、作業前後の status、変更した path、実装上の判断・未解決点。
2. **新規7ファイルの完全な本文**、および baseline 7 → new 7 の **full unified diff**（省略なし）。各 hunk に **1つの DIFF 分類**を明記。
3. 7本の **before Git blob / after SHA-256（可能なら after Git blob）** 対応表。新規 path、import resolution（通常・動的・hardcoded preflight）、各ファイルの役割。
4. import **15＋2＝17本**の path・pin・実測 blob・結果（17/17）、元の15本と追加2本を区別した表、Judge の B1 拘束補足の参照、shadowing・動的 gating import・preflight path の静的検査結果。
5. `STATIC_CONTROL_REPORT_V0.md`：§9 の controls 10項目を `PASS / FAIL / NOT_VERIFIED` で判定し、検査コマンド・静的検査スクリプト・出力を添える。
6. `LEDGER_AND_REPLAY_SCHEMA_V0.md`：exact fields、failure codes、独立 checker の入力境界、共有辺の owner と overlap 判定。
7. `OPEN_QUESTIONS.md`：仕様の衝突、未検証、変更したくなった事項、Judge 裁定を要する事項。なければ `NONE` と明記。
8. **最終報告の1行**：`IMPLEMENTATION_READY_FOR_CHAT_DIFF_AUDIT` または `BLOCKED:<reason>`。前者は **実装差分監査待ち**という意味であり、FREEZE/EXECUTION/CLOSED の宣言ではない。

**即時停止：** authority SHA 不一致、元7または import 17 blob 不一致、別名 module shadowing、allowlist 外の変更が必要、既存コード上書きが必要、P1/P2 等の body 修正が必要、未規定の numerical choice、producer/checker 独立性の維持不能、未承認の計算を要求する場面、**B1 または B2 の Judge 裁定が未受理**、B3 の silent baseline import が回避できない場面。停止時は理由・対象 path・最小限の解決選択肢を報告し、勝手に契約を変更しない。

## 11. 後続工程（Code は実行しない）

**Judge が B1・B2 の拘束補足を受理し v2 を正式発出 → Code 実装案提出 → ChatGPT 独立 full diff audit（7本＋17 imports＋controls）→ Judge の計算順序裁定（D5／C 空白／扁長）→ Judge FREEZE の可否裁定 → 別個の数値実行許可 → producer 本走 → independent checker → receipt audit。**

本**草稿**の作成・共有は実装許可を意味しない。Judge による正式発出後も、v7 の FREEZE、数値実行許可、論文での `CLOSED` を意味しない。
