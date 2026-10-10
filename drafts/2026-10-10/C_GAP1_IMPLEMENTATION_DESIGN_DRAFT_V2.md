C 空白① — 実装設計 DRAFT v2
状態：DESIGN DRAFT v2 / TEXT-ONLY CORRECTION / NOT FROZEN / EXECUTION PROHIBITED / NO COMMIT。
基準：
- bg-spheroid-family main 1c9a6e036884d58de782bc47cb220700187fe511 / STATE v1.13
- bg-oblate-spheroid C1b implementation head 85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b
- 空白① contract text v6：CHAT AUDIT PASS
- G0/E1 v3：CHAT AUDIT PASS
- 本設計 v0 監査：CHAT_AUDIT_C_GAP1_IMPL_DESIGN_V0_AND_ENDPOINT_ADDENDUM_V0_2026-10-10.md
  SHA-256 e206478f4d9bcc3e9a8089939c607d974964d46d001e50f19820f567d43c692f
- 本設計 v1 を含む後続監査：CHAT_AUDIT_C_GAP_NUMERIC_CONTRACT_V1_ADDENDUM_V2_2026-10-10.md
  SHA-256 b92ff21b014527d3ae50deadd6a0907ef086f830652aa63b7347ad0e53be56c3
Judge ruling：
1. t=1 近傍は、seed g(31/32) を1回だけ評価し、[31/32,1] を16等分した全16箱の Gt 上界を累積する mean-value endpoint gate を使う。
2. B_ob<0 は独立 gate ではなく、endpoint certificate の帰結とする。既存 B_ob receipt は consistency check のみ。
この文書は設計のみを固定する。数値本走・証明書生成・commit・push は許可しない。
1. 実装の基準7ファイル
新しい空白①実装は、C1b receipt §1.2 の次の7ファイルを一対一の比較基準とする。
lineage	role	baseline path	Git blob
producer	kernel	producer/global_axial_c1b_kernel.py	67dda838369302010ef3d589937b834b96ede4d8
producer	gating	producer/global_axial_c1b_gating.py	a93ca173ae0bededcd5a0248aa07ac3348f9a243
producer	producer	producer/global_axial_c1b_producer.py	0616fbd7c9c85f77c8e80b61a5b3b536b45012a8
producer	driver	analysis/c1b_resumable_driver.py	5fd308bb4c02c6ddbd612ddbedb18f6b9e22bc3d
checker	kernel	checker/global_axial_c1b_kernel.py	4eaca55ddf79b437fc756d666294372e5d1a6ba4
checker	gating	checker/global_axial_c1b_gating.py	03df262012bfbebcf4d2ea173933186c70abafbf
checker	checker	checker/global_axial_c1b_checker.py	0760764ef7592be1ddd4ffec3966e9c6ec930a5b


この7本を上書きしない。空白①用の別 path に対応ファイルを作り、baseline との差分を全文監査できる構成にする。
2. 差分 allowlist：DIFF-A〜E + DIFF-K
許可する意味差分は次の6種類だけとする。
- DIFF-A：R 群の左向き進行。queue traversal と child insertion order のみ。
- DIFF-B：X 群の固定 path。predictor/root machinery を呼ばない。
- DIFF-C：L 群の root-free negative path。
- DIFF-D：t=1 近傍の endpoint gate。seed g_box 1回 + 全 endpoint Gt boxes の累積 mean-value form。
- DIFF-E：A〜D を実現するための region dispatch、replay、ledger、入力配線。
- DIFF-K：①固有の domain constants と self-test controls。
DIFF-K で変更を許すもの
DIFF-K は次の項目だけに限定する。
1. λ region endpoints：
   - 2/5
   - 699/1600
   - 281/640
   - 9/20
2. 数値契約で固定する coarse slab width と region ごとの slab count。
3. traversal direction の表示文字列。
4. C1b 固有 domain に依存する self-test/control を、①の数値契約に対応する control へ置換すること。
5. 上記定数を ledger header / contract metadata に転記すること。
DIFF-K を口実に、積分核、P1/P2、root localization、interval formula、chart formula を変更してはならない。
すべての変更 hunk に DIFF-A, DIFF-B, DIFF-C, DIFF-D, DIFF-E, DIFF-K のいずれか一つを付ける。未分類 hunk が1つでもあれば DIFF_OUTSIDE_ALLOWLIST。
3. 変更禁止領域
次は baseline と同一式・同一選択規則を維持する。
- g_box の積分核
- gt_box の積分核
- ordinary/corner の T1,T2,T3
- W0=1/16
- PRED_ACCEPT=1/64
- ROOT_TARGET=1/128
- P1 scan の符号転換規則
- P2：
  abs(continuation - scan_mid) <= ROOT_TARGET
  なら continuation、strict excess なら relocated
- root localization の target-width 判定
- interval arithmetic の核となる式
- endpoint chart の代数式
旧 P2 |t_cont-t_scan|<=1/64 を復活させた場合は即 CONTRACT_MISMATCH。
4. baseline import closure 15本は byte-identical
新しい①コードが読む既存 Gt / endpoint 関連モジュールは、監査 pack 0bfc5c4e の次の15 blob を変更せず使用する。
lineage	path	blob
producer	producer/monotone_tube_refinement_producer.py	c2fee40053ab055ce352e93e1c6d1fc43e46310a
checker	checker/monotone_tube_refinement_checker.py	15d660265552fc2f2c83ffe897ed5efab8514da2
checker	checker/monotone_tube_interval_checker.py	f2fa2a5a42d35b8b77e3c63fa0d9ad48ce562a77
producer	producer/global_axial_c1b_endpoint_r.py	29d441a578f10fe7f4beb38476d3699f3648a3b1
checker	checker/global_axial_c1b_endpoint_r.py	1a953b22c12a89afc06790b28d6b0dea9680dc43
producer	producer/endpoint_interval_producer.py	51060fea01cb9ff661518b7c52146f71187846ff
producer	producer/monotone_tube_interval_producer.py	b6d96df223c0e423e804d96f4892a8e818c05827
producer	producer/global_axial_c0_producer.py	c4c8d6b59d3829e1843d149b7857eda5800287aa
checker	checker/global_axial_c0_checker.py	85978625e029b01c8ae40fa8234566f10eea251c
checker	checker/endpoint_local_controls.py	c913c47d228e51a15f56957f5df9196efa1b22c3
checker	checker/oblate_axis_prototype.py	df402583c320c459ff4f72dc5294558f14f44d31
checker	checker/endpoint_interval_checker.py	4cb16f8a975e5a3be601a7926af695ad5be57790
checker	checker/endpoint_local_checker.py	2bddddf6e9a08ca7acae94c89bd4d5ab1de861bc
producer	producer/global_axial_c0_producer_v2.py	cdbdf51f8656c1fcae97666cc1846461b250a591
checker	checker/global_axial_c0_checker_v2.py	fbec890588d2d390ea67bc90116b80bb37ebf9cc


実装差分監査では、7つの新実装ファイルだけでなく、この15本が pin した blob と byte-identical であることも確認する。新実装から別 blob の同名 module を読むことは禁止。
5. region split と共有 λ 辺
①の λ domain を exact rational により
- L = [2/5, 699/1600]
- X = [699/1600, 281/640]
- R = [281/640, 9/20]
に分ける。
coarse slab は region boundary を跨がない。共有 λ 辺は両側で評価してよいが、ledger の canonical ownership は
- 699/1600：X owner、L は overlap check
- 281/640：R owner、X は overlap check
- 9/20：①は boundary consistency、②/C1b side が上側接続 owner
とする。
6. DIFF-A：R は queue 順序だけで左向きにする
baseline choose_predictor(slab, previous_root) は変更しない。
- previous_root is None → t_cont=9/16
- それ以外 → previous certified root interval の midpoint
R の initial queue を高 λ → 低 λ に並べる。
初回は 9/20 に接する slab。以後 ACCEPT のときだけ previous_root を更新する。
REFINE の場合は right child を先、left child を後に queue へ戻す。この順序だけで「右隣の certified root enclosure → 左 slab」の continuation を作る。
P1/P2 body は byte-identical。失敗時に別 predictor rule へ切り替えない。
7. DIFF-B：X は固定 path
X では predictor と root localization を一切呼ばない。
X の canonical t ownership：
- lower monotonicity block：[1/2,5/8]
- negative block：[5/8,31/32]
- endpoint block：[31/32,1]
共有辺：
- t=5/8 の canonical sign owner は negative block。lower tube でも同じ閉辺を overlap check してよい。
- t=31/32 の canonical owner は endpoint block の seed。negative block でも同じ閉辺を overlap check してよい。
X path：
1. [1/2,5/8]×Λ：direct gt_box により sup G_t<0。
2. [5/8,31/32]×Λ：direct g_box により sup g<0。
3. endpoint block：§9 の mean-value endpoint rule。
4. C1a endpoint signs は root count classification にのみ使用。
X が失敗しても predictor/root path へフォールバックしない。
8. DIFF-C：L は root-free negative path
L では predictor/root localization を一切呼ばない。
- interior block [1/2,31/32]×Λ：direct g_box<0
- endpoint block [31/32,1]×Λ：§9
t=31/32 の canonical owner は endpoint seed。interior block は overlap check として同じ辺を含めてよい。
失敗時に root search へ移らない。predeclared refinement が尽きれば CERTIFICATE_INCONCLUSIVE。
9. DIFF-D：cumulative mean-value endpoint gate
Judge ruling S1 により、旧設計の「endpoint 内部を direct g_box、最後の1箱だけ mean-value」は廃止する。
空白①では endpoint start を
\[
\boxed{t_0=31/32}
\]
に固定する。
9.1 seed は \(t=31/32\) の1点だけ
各 current λ slab \(\Lambda_c\) について、
\[
G_0(\Lambda_c)
=
\sup_{\lambda\in\Lambda_c}g(31/32,\lambda)
\]
を direct g_box で1回だけ評価する。
(31/32,1) 内では direct g_box を呼ばない。
9.2 endpoint strip は16等分した Gt boxes
\[
[31/32,1]
\]
を
\[
\Delta t=\frac1{512}
\]
で16等分し、
\[
t_j=\frac{31}{32}+\frac{j}{512},
\qquad j=0,\ldots,16,
\]
\[
Q_j=[t_j,t_{j+1}]\times\Lambda_c,
\qquad j=0,\ldots,15
\]
とする。
各 \(Q_j\) で direct gt_box により
\[
U_j=\sup_{Q_j}G_t
\]
を包む。
- \(j=0,\ldots,14\)：ordinary chart。
- \(j=15\)：tr == T_HI == 1 なので既存 endpoint corner/ordinary dispatch。
- t partition は run 中に変更しない。
- λ refinement が起きても同じ16 t-boxesを使う。
9.3 cumulative success gate
endpoint upper bound を
\[
\boxed{
U_{\rm cum}
=
G_0(\Lambda_c)
+
\sum_{j=0}^{15}
\frac1{512}\max(0,U_j)
}
\]
と定義する。
endpoint strip の唯一の成功条件は
\[
\boxed{U_{\rm cum}<0}.
\]
各加算項は非負なので、full cumulative sum が負なら任意の途中時刻に対応する partial sum もそれ以下であり、
\[
g(t,\lambda)<0
\qquad
(31/32\le t\le1)
\]
が従う。
これは G0/E1 の \(C^1\) interior と \(t=1\) の左微分に基づく。
9.4 禁止事項
- (31/32,1) 内で direct g_box を使わない。
- C_\Lambda(1-t) を runtime gate に使わない。
- 各 Gt box に Gt<0 を必須条件としない。正の upper bound も max(0,U_j) として累積する。
- endpoint route が不確定なとき B_ob receipt で救済しない。
- run 中に16分割を変更・追加 refinement しない。
- max(0,U_j) を midpoint、point estimate、sample 値で置換しない。
10. B_ob の役割
① v6 の独立 G1「B_ob<0 on [2/5,9/20]」は実装 gate から削除する。
endpoint certificate が通れば、G0/E1 の continuity により
\[
g(1,\lambda)=B_{\rm ob}(\lambda)<0
\]
は certificate の帰結である。
既存 B_ob receipt は、coverage overlap 上で符号が一致することを確認する NON-GATING CONSISTENCY CHECK としてのみ残す。
B_ob receipt 不一致は provenance/consistency failure として停止するが、B_ob receipt 単独で slab を ACCEPT しない。
11. DIFF-E：dispatcher / ledger / replay
各 slab は exact rational endpoint から region ∈ {L,X,R} を一意に割り当てる。
ledger は最低限：
- region
- diff_categories_used
- lambda_lo, lambda_hi
- coarse_index, depth
- endpoint_partition_id
- endpoint_seed_t=31/32
- endpoint_seed_g_upper
- 16 endpoint Gt box labels / upper bounds
- 16個の max(0, gt_upper) contribution
- endpoint_cumulative_mvt_upper
- L/X/R 固有 guard summary
- R のみ predictor/root fields
を記録する。
L/X record で predictor/root field が non-null なら CONTRACT_MISMATCH。
R record で old P2 rule が観測されたら CONTRACT_MISMATCH。
12. producer/checker 独立性
checker は producer の新実装 module を import しない。
producer/checker は同じ predeclared contract、partition、region ownership、P2 rule を使うが、interval 値は別々に再計算する。
checker が producer から信用してよいのは replay plan の exact rational box labels / decision labels だけであり、producer interval bounds を再利用しない。
13. 差分監査の提出物
FREEZE 前に：
1. baseline 7 blob → new 7 file の full diff。
2. 全 hunk の DIFF-A/B/C/D/E/K 分類。
3. 未分類 hunk = 0。
4. P1/P2 body の byte-identical check。
5. g_box, gt_box, ordinary/corner T1–T3 の formula identity check。
6. baseline import closure 15本の blob/byte identity check。
7. X/L から predictor/root code が到達不能である control。
8. R の descending queue / right-child-first control。
9. endpoint は seed g(31/32) 1回 + 16個の Gt boxes + cumulative mean-value expression 以外に成功経路がなく、(31/32,1) 内で g_box が到達不能である control。
10. B_ob receipt が gate ではなく consistency check だけである control。
14. FREEZE blocker
- 数値契約 v0 の CHAT AUDIT / Judge ruling
- 本実装と full diff audit
- D6：5afa815f... と 7cb9b809... の外部監査
- producer/checker control audit
これらが閉じるまで FREEZE しない。