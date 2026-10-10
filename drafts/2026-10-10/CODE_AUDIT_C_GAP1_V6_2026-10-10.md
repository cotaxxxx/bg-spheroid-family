The audit target lives in `bg-spheroid-family`, which isn't in this session yet. First I'll check the working tree, since a file changed on disk, and then attach that repository read-only.

The working tree is clean and matches the remote, so the on-disk change notice needs no action. Now attaching `bg-spheroid-family`.

HEAD matches d707e6ef. Next I'll verify the target file's identifiers and read it.

The v6 pins match (blob d800f2d3…, SHA d1f2ef5d…, 28 lines). Next I'll pull in the C1b implementation head in `bg-oblate-spheroid` and check whether all 7 blobs resolve there.

I fetched `85eca228` directly by SHA. Next I'll resolve the 7 paths at that commit and check its relation to `design/d-ob-p2`.

All 7 blobs match at `85eca228`, but that commit isn't an ancestor of `design/d-ob-p2`—only the three `rejected/c1d-driver-*` branches contain it. I'll check the full branch list next, then locate the C1b receipt.

Next I'll look up the C1a receipt `e494e789`, the C1b receipt, and the P2 documents (`5326e2b5`, `4a493191`, `c785ceda`) in both repositories.

These are short blob IDs in `bg-oblate-spheroid`. Next I'll find which path and commit each one lives at.

Next I'll locate the C1b machine receipt and read its §1.2, plus the relevant part of the C1a receipt.

The receipt's 7 blobs match v6, but I noticed a branch name mismatch (`implementation/gt-boundary-two-chart` vs. `design/d-ob-p2`) and `85eca228` doesn't appear reachable from either branch. I'll verify both discrepancies next.

The clone may be shallow (rev-list count is only 3), which would make the ancestry results unreliable. I'll check, deepen it, and repeat the test.

I'm retracting my earlier "not an ancestor" claim—that was due to a shallow clone. With full history confirmed, `85eca228` is indeed an ancestor of both branches, so now I'll check it against the P2 rules: v2.3 line 46, v2.3.1, the pre-run amendment, and kernel lines 34/35.

The constants W0=1/16, PRED_ACCEPT=1/64, and ROOT_TARGET=1/128 match across v2.3, the producer kernel, and the checker kernel. Next I'll check where these constants are used in the code and look at the NOT_BINDING status header in v2.3/v2.3.1.

The selection rule matches across both lineages (L916–927 and L909–920), with continuation chosen when within ROOT_TARGET of scan_mid, ties going to continuation. Now I'll verify no old 1/64 comparison remains anywhere in the 7 files.

No leftover 1/64 selection path in either version — `PRED_ACCEPT` is only used in `predictor_accept`, though `ROOT_TARGET` doubles as the root-enclosure width target in both kernels. Next I'll look into C3: how the baseline continuation gets its starting value and direction.

Progress so far: all 7 pins resolve and match, and the P2 rule matches in both lineages. Next I'm reading the C1a receipt and the endpoint lemma to check the X-box root-count logic (C2).

C1a's logical gate relies only on items A, D, L, R evaluated at 83/200 and 9/20, while the [699/1600, 281/640] bracket is explicitly report-only despite its certified signs. Next, I'll check how F_x is defined to see if F_x(λ) = g(1/2, λ).

F_x(λ) is defined as g(1/2, λ)/(1/2) in contract `77210a54` (L42), so F_x shares its sign with g(1/2, ·), and C1a's condition D (∂_λ F_x > 0) drives the monotone sign structure in X. Next I'll check C3 for how the baseline orders slabs and updates `previous_root` after a refinement.

Baseline C1b always treats "previous accepted root" as the left neighbour, since REFINE queues [left, right] and updates previous_root only on ACCEPT—so v6's leftward variant only makes sense if child order is also reversed, which it doesn't state. Next I'll check STATE v1.14 and later docs for whether this gap and the C7 supersessions are addressed.

STATE v1.14 shows the gap-① diff audit expanded to cover 15 imported modules beyond the original 7 files, since baseline kernels import other modules like `producer.monotone_tube_refinement_producer` and `checker.global_axial_c0_checker_v2`, but v6 §3 only audits the 7 files. I'll check the later drafts in `drafts/2026-10-10/` next.

I'll mark design v2 as SOURCE_NOT_FOUND since only v1 exists in the repo, then check the design for the slab order, DIFF-K allowlist, endpoint method, and B_ob.

Confirmed: Design v1 §6 clarifies that on REFINE in R, the right child goes first, so v6's silence is just a gap later filled, not an error. Next I'll check the endpoint addendum, the numeric contract, gap ② v3 for the 9/20 boundary, and where "端点補題 Lemma 3" is defined.

I've located Lemma 3's pre-limit representation of g, with continuity on [1/2,1] stated in Lemma 5. Now I'll verify whether its λ-scope I, and that of the C2 lemma, actually covers U1's range λ ∈ [2/5, 9/20).

The endpoint lemma applies generally to I = [2/5, 9/20], but the C2 lemma's scope (t ∈ [63/64,1], λ ∈ [5/8, 33/50]) doesn't cover U1, so I'll check how G0/E1 v3 bridges that gap.

I found that G0/E1 v3 extends the Gt dominating function to λ ∈ [2/5, 5/8], t ∈ [1/2, 1), which is the dependency v6 relies on but still subject to D6. Next I'll check the endpoint addendum v2 and numeric contract v1 for C7.

Numeric contract v1 is now locked in: Δλ = 1/3200 across 160 slabs (118+7+35), 160/192-bit precision, degree 50. Last steps remaining are defining its fail-closed vocabulary and the ownership rule for shared boundaries.

The narrower codes in the numeric contract v1 are a later refinement of v6's CERTIFICATE_INCONCLUSIVE, not an error in v6. Next I'll verify the P1 scan matches `c785ceda` and resolve the discrepancy between v2.3/v2.3.1's NOT_BINDING headers and v6's claim that they're binding.

Confirmed P1 matches the code in `c785ceda` (L43–60) and the kernel logic. Now I'll check whether any record overrides the NOT_BINDING status of v2.3/v2.3.1, since the C1b receipt doesn't pin them.

No ruling makes v2.3/v2.3.1 binding—their headers remain NOT_BINDING and the C1b receipt doesn't pin them, so their authority for v6 comes solely from the executed code. Next I'll check what λ range the B_ob receipt covers, since later documents use it as a consistency check over the overlap.

The B_ob receipt (`0f19e387`) covers λ ∈ [9/20, 5/8] only (L47, L109), so it overlaps U1 just at λ = 9/20. Last, I'll check v6's header pin for its audit source (SHA c2e63b3a…).

# C 空白① 事前宣言 v6 — Code 独立監査

v6 そのままでの FREEZE は不可です。追加の blocker が1件（実装設計 v2 が repo に無い）、Judge 確認事項が1件（K1）あります。

検査は読み取り専用の git 操作（clone、fetch、cat-file、show、grep）だけで行いました。実装、数値計算、commit、push、② seal の `ls` はしていません。既存の chat 監査の結論は使っていません。v6 ヘッダの監査原典 SHA を照合するためにだけ、`audits/CHAT_AUDIT_C_GAP1_V5_AND_G0E1_V1_2026-10-10.md` を開きました。

**照合元：**
- bg-spheroid-family：`d707e6ef3e583616fa3f24409351ea01b6d4be58`
- bg-oblate-spheroid：`85eca228…`、`origin/design/d-ob-p2` の先頭 `bbcfe662…`、`origin/implementation/gt-boundary-two-chart` の先頭 `30fbc5cf…`

## A. Verdict

| 対象 | 判定 |
|---|---|
| historical v6（当時の契約文として） | **PASS WITH CORRECTIONS**。数学的な矛盾は見つかりませんでした。根の数の論理（C2）は閉じています。修正は文言と出典表記です。 |
| current operational chain（v6＋後続文書） | **PASS WITH CORRECTIONS / DEPENDENCY_PENDING**。v6 単独では binding source になりません。後続文書と合わせれば、文面上の論理はほぼ閉じています。ただし後述の SOURCE_NOT_FOUND が1件と、修正が残ります。 |

**対象ファイルの照合結果：**
- `drafts/2026-10-10/C_GAP1_PREDECLARE_DRAFT_V6.md`：blob `d800f2d3…` と SHA-256 `d1f2ef5d…` はどちらも一致（MATCH）、28行。
- ヘッダの基準 commit `32218d78` は存在します（STATE v1.12、d707e6ef の2コミット前）。
- ヘッダの監査原典 SHA `c2e63b3a…` は、d707e6ef の `audits/CHAT_AUDIT_C_GAP1_V5_AND_G0E1_V1_2026-10-10.md` と一致します（MATCH）。

## B. Findings

**K1 — correction — §1（L4）。C1a 入力の書き方**
- **source：** bg-oblate-spheroid の `analysis/GLOBAL_AXIAL_C1A_MACHINE_RECEIPT.md`（blob `e494e789`）と、C1 親契約（blob `77210a54`）。
- **一致する点：**
  - F_x(699/1600) は NEG（受領書 L103）、F_x(281/640) は POS（L104）。producer と checker の両系統で再現されています（L140）。
  - 点推定の λ_x≈0.43775487 は `REPORTED_EXPECTATION / NON_GATING` です（L124–127）。
  - C1 契約 L42 の定義は F_x(λ) = g(1/2,λ)/(1/2) です。したがって F_x と g(1/2,·) は同じ符号を持ちます。
- **不一致 (a)：** C1a の論理ゲートは A、D、L、R の4つだけです（L44–47）。L・R は 83/200 と 9/20 での符号です。二分法で得た区間 [699/1600, 281/640] について、受領書は「report-only で、存在や一意性の gate にはしない」と明記しています（L50）。v6 は区間の符号を「厳密符号入力」として gate に使っています。これは格上げにあたり、その格上げをどこで宣言したかが v6 に書かれていません。
- **不一致 (b)：** §1 の「λ≤λ_x で根0個、λ>λ_x で単純根1個」を導くには、X 内で g(1/2,λ) の符号が単調であることが必要です。それを与えるのはゲート D（∂_λF_x>0 on [83/200,9/20]、L45）です。v6 は「2点のみ」と書いていますが、実際には D にも依存しています。
- **補足：** 区間の2符号は、L 群と R 群での t=1/2 における直接の認証でも独立に再確認されます。
- **最小修正文：** 「入力は C1a の論理ゲート D（∂_λF_x>0 on [83/200,9/20]）と、C1a で report-only の認証済み区間符号 F_x(699/1600)<0、F_x(281/640)>0 とする。区間符号を gate 入力として用いることは本契約で宣言する（Judge 確認事項）。F_x=2g(1/2,·)（C1 契約 77210a54 L42）。」

**K2 — note — §2 X（L7）。C2：根の数の論理は閉じている**
独立に点検しました。固定箱で ∂_t g<0 on [1/2,5/8] と g<0 on [5/8,1] が認証されたとして、各 λ について次のとおりです。
- **g(1/2,λ)>0 のとき：** g(5/8,λ)<0 です（閉箱が 5/8 を含むため）。中間値の定理と狭義単調性から、根は (1/2,5/8) にちょうど1個です。∂_t g<0 なのでその根は単純根です。
- **g(1/2,λ)<0 のとき：** [1/2,1] 全体で g<0 となり、根は0個です。
- **g(1/2,λ)=0 のとき：** (1/2,1] で g<0 です。根は t=1/2 だけで、U1 は 1/2<t なので U1 内の根は0個です。

v6 はこの「t=1/2 は U1 に含まれない」を、ゼロの場合にだけ正しく使っています。場合分けに漏れはありません。

**出典表記についての指摘：**
- 中間値の定理に必要な連続性は、5afa815f（`analysis/OBLATE_ENDPOINT_C1_LEMMA.md`）の Lemma 5 に「g は [1/2,1] で連続」と明記されています。v6 が挙げている Lemma 3 は積分表示の補題です。
- この補題は λ の範囲を「0<λ₋≤λ₊<1/√2 を満たす任意の I」として述べています（L5）。I=[2/5,9/20] はこれに当てはまりますが、v6 はその当てはめを明記していません。
- ∂_t g の存在は G0/E1 v3（範囲 λ∈[2/5,5/8]、L10・L189）に依存しています。
- **最小修正文：** 「（端点補題 Lemma 3・5、I=[2/5,9/20] として適用）」

**K3 — correction（後続文書で解消済み）— §2 R（L8）。C3：左向きの continuation**
- **一致する点：**
  - 最初の t_cont=9/16 は、baseline の `choose_predictor` と同じです（producer kernel L930、`c785ceda` L22–26）。
  - P1 の格子探索も c785ceda（L43–60）と同じです。格子 t_k=1/2+k/1024（k=0..512）、λ_mid での評価、`+→−` の最初の組、non-gating という点で、kernel の `PRED_GRID_DEN=1024`（L50）と `predictor_scan` の実装（L886–913）とも一致します。
  - `choose_predictor` 自体は進行方向に依存しません。変わるのは処理の順序だけです。
- **不一致 (a)：** baseline が引き継ぐのは、直前に受理した根包囲 T_prev の中点 (a+b)/2 です（kernel L930、c785ceda L28–36）。v6 の「root enclosure を引き継ぐ」は、中点を使うことを明記していません。
- **不一致 (b)：** baseline では REFINE のとき `[left, right]` の順でキューの先頭に戻します（gating L326–329 とプロデューサのループ）。このため「直前に受理した根」は幾何的に左隣の slab のものになります。左向きに進めて「右隣」を正しく引き継ぐには、子 slab の順序も逆にする必要があります。v6 はこれを書いていません。
- **解消状況：** 実装設計 v1 §6（L96–102「right child first」）と数値契約 v1 L23 付近（「R は高 λ → 低 λ の順で処理し、REFINE 時は right child first」）で解決済みです。v6 の誤りではなく、当時の記述が不足していたものです。
- **最小修正文：** 「t_cont は右隣 slab の認証済み T_* の中点とする。」

**K4 — correction — §2 R・§3（L8、L22）。P2 文書の拘束力の根拠**
- **一致する点：**
  - v2.3（`5326e2b5`、analysis/GLOBAL_AXIAL_C1B_PREDICTOR_SELECTION_ADDENDUM_V2_3.md）の L46 は `ROOT_TARGET = 1/128.` です。
  - 等号の場合は continuation 側です（L35）。
  - コードでも、producer kernel L916–927 と checker kernel L909–920 が `abs(continuation - scan_mid) <= ROOT_TARGET` なら continuation、そうでなければ scan_mid（ラベルは "relocated"）を選びます。
  - 7本のファイルのどこにも、旧規則 `|t_cont−t_scan|≤1/64` の残りはありません（grep で確認）。
- **不一致：** v6 は 5326e2b5 と 4a493191 を「P2 の拘束文書」と呼んでいます。しかし両文書のヘッダ（各 L3）は今も `NOT_BINDING` です。C1b 受領書 §1.3 はこの2文書を pin していません。両文書を binding にする裁定記録は、design/d-ob-p2 の範囲では SOURCE_NOT_FOUND でした。拘束力の実際の根拠は、v2.3.1 の自己宣言と、実行済みコード（受領書 §1.2）です。
- **最小修正文：** 「v2.3／v2.3.1 の文書ヘッダは NOT_BINDING である。P2 規則の権威は、C1b 実行コード（§1.2 の kernel 2本）が実装した規則とし、本契約の FREEZE で採用する。」

**K5 — note — §2 R（L8）。ROOT_TARGET の二重の役割**
コード上、ROOT_TARGET は P2 の選択閾値であると同時に、根包囲の幅の目標でもあります（producer kernel L1282・L1412・L1415、checker kernel L1259・L1389・L1392）。PRED_ACCEPT は最終受理の判定（`predictor_accept` L1423／L1400）にだけ使われています。v6 は両者の役割を取り違えてはいません。ただ、ROOT_TARGET を「選択閾値」とだけ呼んでいる点は補足が望ましいです。X で「root target を適用しない」としている点とは整合しています。

**K6 — correction（後続文書で解消済み）— §3（L22）。差分監査の対象範囲**
- v6 は差分監査の対象を実行コード7本に限っています。
- 実際には kernel が他のモジュールを import しています。例：producer kernel L25–26 の `producer.monotone_tube_refinement_producer`、checker kernel L27 の `checker.global_axial_c0_checker_v2`。
- これは実装設計 v1 §4（L64–84、baseline の import 群15本が byte-identical であること）で補われています。
- 15本の一覧そのものは、今回の照合範囲外です。

**K7 — superseded — §3（L22）。** v6 の許容差分 (a)〜(e) は、実装設計 v1 L27–47 の DIFF-A〜E と DIFF-K に置き換えられています。DIFF-K は①固有の定数と self-test に限られ、積分核・P1/P2・根の局在化は変更禁止です。

**K8 — superseded — §5（L27）。B_ob 符号ゲート**
- 既存の B_ob 受領書（`0f19e387`）が対象とする λ の範囲は [9/20,5/8] だけです（L47、L109）。U1 と重なるのは λ=9/20 の1点だけです。
- したがって v6 の書き方では、①に新しい B_ob の証拠が必要になるところでした。
- 現在は、端点追補 v2 §5（L151–）、実装設計 v1 §10（L168–176）、数値契約 v1 により、「B_ob<0 は端点証明書の帰結」「既存受領書は照合のみ」とされています。

**K9 — superseded — §4（L24）。** 未確定としていた近似次数と数値規則は、数値契約 v1 で確定しています（Δλ=1/3200、118+7+35=160 slab、MAX_DEPTH 3、160/192 bits、degree 50、実行中の精度引き上げ禁止）。端点処理の抽象的な記述も、端点追補 v2 で置き換えられています（t_e=31/32、seed g(t_e) の1点＋Δt≤1/512 の Gt 累積平均値形）。

**K10 — correction（後続 chain 側）— §4（L24）。C6：失敗の分類語**
- v6 の4分類（CERTIFICATE_INCONCLUSIVE、NONFINITE、RESOURCE_CAP、CONTRACT_MISMATCH）は互いに区別されています。「数学的反例と混同しない」も明記されていて妥当です。
- ただし数値契約 v1 §13（L295–326）には `CERTIFICATE_INCONCLUSIVE` がありません。代わりに PRECISION_／APPROX_DEGREE_／ENDPOINT_*_INCONCLUSIVE に細分されています。②v3 の分類語は CERTIFICATE_FAILED と MATHEMATICAL_CONTRADICTION です。
- v6 の語から現行の語への対応表が、どこにも書かれていません。
- **最小修正文（数値契約側）：** 「v6 の CERTIFICATE_INCONCLUSIVE は §13 の *_INCONCLUSIVE 各語に細分する。」

**K11 — note — §2（L9）。C1：共有境界での照合内容**
- λ 方向の被覆に穴はありません。L∪X∪R＝[2/5,9/20] は U1 の λ 範囲を含み、t の範囲 [1/2,1] は U1 の (1/2,1] を含みます。
- 境界 699/1600 は L と X の両方に、281/640 は X と R の両方に含まれます。どちらも同じ結論を主張するので、矛盾はありません。
  - 699/1600：L の主張は根0個、X の主張は g(1/2)<0 なので根0個。
  - 281/640：X の主張は (1/2,5/8) に根1個、R の主張も根1個。
- ただし v6 の「重複照合」は、何を比べるのかを書いていません。数値契約 v1 にも、t 方向の境界の分担規則（L96–98）はありますが、λ 方向の境界の規則はありません。
- **最小修正文：** 「各 λ 境界で両群の根の個数を比較し、281/640 では R の T_* が (1/2,5/8) と交わることを確認する。不一致は CONTRACT_MISMATCH とする。」

**K12 — note — §2（L9）。λ=9/20 の責任分担**
λ=9/20 は U1 に含まれません。この点の分担は次のとおりで、穴はありません。
- t≤t_+ の部分：C1b（kernel の `L_LO=9/20`、L30）
- 31/32<t<1 の部分：②v3 L5
- t=1：B_ob 受領書

**K13 — note — §3。C5：実装 head とブランチ**
- 受領書 §1 が記す実装 head 85eca228 のブランチは `implementation/gt-boundary-two-chart` です。監査依頼の「design/d-ob-p2」とは名前が違います。
- 履歴を深く取得し直した結果、85eca228 は両方のブランチの祖先でした。浅い clone で最初に出た「祖先でない」という結果は誤りで、撤回します。

**K14 — SOURCE_NOT_FOUND**
- 実装設計 v2：d707e6ef には存在しません。`drafts/2026-10-10/` にあるのは v1（blob `86946eb9`）だけです。
- v6 §3 の「27件の C1b 改訂文書」：一覧がどこにも書かれていないため照合できません。

## C. Pin table

| 項目 | 期待値 | Code の照合結果 |
|---|---|---|
| producer/global_axial_c1b_kernel.py | 67dda838… | MATCH（85eca228、受領書 §1.2） |
| producer/global_axial_c1b_gating.py | a93ca173… | MATCH（同上） |
| producer/global_axial_c1b_producer.py | 0616fbd7… | MATCH（同上） |
| analysis/c1b_resumable_driver.py | 5fd308bb… | MATCH（同上） |
| checker/global_axial_c1b_kernel.py | 4eaca55d… | MATCH（同上） |
| checker/global_axial_c1b_gating.py | 03df2620… | MATCH（同上） |
| checker/global_axial_c1b_checker.py | 0760764e… | MATCH（同上） |
| 役割の対応（producer／checker） | 表のとおり | MATCH。path・役割・受領書 §1.2 の7行が一致 |
| W0／PRED_ACCEPT／ROOT_TARGET | 1/16, 1/64, 1/128 | MATCH（producer kernel L34、checker kernel L35） |
| P2 の規則（≤ROOT_TARGET なら continuation、等号は continuation） | v2.3 L29–35・L46 | MATCH（producer kernel L916–927、checker kernel L909–920） |
| 旧 1/64 選択規則が残っていないこと | — | 7本すべてで残存なし（PRED_ACCEPT は受理判定のみ） |
| v2.3／v2.3.1 の blob | 5326e2b5…／4a493191… | 存在し、path も一致。ヘッダは NOT_BINDING（K4） |
| c785ceda（P0/P1） | 旧 P2 は失効 | MATCH。P1 の格子、P0 の初期値 9/16 と中点の引き継ぎがコードと一致 |
| C1a の区間符号 | F_x(699/1600)<0、F_x(281/640)>0 | MATCH（e494e789 L103–104・L140）。ただし report-only（K1） |
| λ_x の点推定 | NON_GATING | MATCH（L124–127） |

## D. Current-chain reconciliation（v6 の節ごと）

| v6 の節 | 判定 | 根拠 |
|---|---|---|
| ヘッダ（STATE v1.12／32218d78） | STILL_VALID（当時の表記） | 基準 commit は存在し、v1.14 では後続文書が上位に立つ |
| §1 対象・主張 | NEEDS_CORRECTION | K1（区間符号の格上げの宣言、ゲート D への依存の明記） |
| §2 L 群 | STILL_VALID | 端点処理は端点追補 v2 に従う |
| §2 X 群 | STILL_VALID（出典表記の修正のみ） | K2 |
| §2 R 群 | STILL_VALID＋NEEDS_CORRECTION | K3（中点）、K4（拘束力の根拠）、K5。子 slab の順序は実装設計 v1 で解消済み |
| §2 境界の扱い | STILL_VALID（note） | K11、K12 |
| §2 t=1 の扱い | SUPERSEDED_BY_LATER_RULING | 端点追補 v2（累積平均値形） |
| §3 7本の pin | STILL_VALID | Pin table のとおり |
| §3 許容差分 (a)〜(e) | SUPERSEDED_BY_LATER_RULING | DIFF-A〜E＋K（K7） |
| §3 差分監査の範囲（7本のみ） | SUPERSEDED_BY_LATER_RULING | import 群15本の追加（K6） |
| §4 方式、未確定の数値規則 | SUPERSEDED_BY_LATER_RULING | 数値契約 v1（K9） |
| §4 失敗の分類語 | STILL_VALID（v6 単独として）／NEEDS_CORRECTION（chain の対応表） | K10 |
| §4 計算資源（96 core-h、D5 との排他） | DEPENDENCY_PENDING | 実行順は Judge 裁定待ち |
| §5 FREEZE 阻止条件 | 一部 SUPERSEDED（B_ob ゲート、近似次数）／DEPENDENCY_PENDING（差分監査、G0/E1 の外部監査、C1a の依存補題） | K8、K9 |
| §6 pin 監査の境界 | STILL_VALID | 「移植済み」とは主張していない点を確認 |

## E. Final status

- **v6 単独での FREEZE：不可**
  - 理由1：§3〜§5 の多くが後続の裁定で置き換えられており、v6 単独は binding source になりません。
  - 理由2：K1 と K4 の文言修正が必要です。
- **後続文書と合わせた chain：** v6、実装設計、端点追補 v2、数値契約 v1、G0/E1 v3、②v3 を合わせれば、論理（被覆、根の数、P2、端点、B_ob の位置づけ）はほぼ閉じています。ただし次の点が残ります。
  - 実装設計 v2 が SOURCE_NOT_FOUND（K14）
  - 失敗分類語の対応表がない（K10）
  - λ 境界での照合内容が未定義（K11）
- **残る blocker：**
  1. D6：5afa815f と 7cb9b809 の外部監査（既知）
  2. ①の実装と全差分監査（7本＋import 群15本）（既知）
  3. ②の封印ディレクトリの確認（既知）
  4. **追加：** 実装設計 v2 の本文を repo に置いて pin すること。現在の chain は v2 を参照していますが、d707e6ef に存在しません。
  5. **追加（Judge 確認事項）：** K1。C1a で report-only とされた区間符号を、gate 入力に格上げすることの確認。代わりの方法として、L・R 群で t=1/2 を直接認証して同じ符号を得る形に書き換えれば、この格上げは不要になります。
- K2、K3、K5、K11 の修正は、FREEZE を止めるものではありません。

最終的な FREEZE の判断は Judge が行います。