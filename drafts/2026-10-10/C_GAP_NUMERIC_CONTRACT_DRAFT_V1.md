C 空白①② — 数値契約 DRAFT v1
状態：NUMERIC CONTRACT DRAFT v1 / NOT FROZEN / NO RUN AUTHORIZED。
基準：
- bg-spheroid-family main 1c9a6e036884d58de782bc47cb220700187fe511 / STATE v1.13
- C1b implementation head 85eca2288732a3cac65f4d5f87ecfd2ba5ce2e9b
- 空白① implementation design v1：CHAT AUDIT PASS
- endpoint addendum v1：CHAT AUDIT PASS as text
- numeric contract v0：CONDITIONAL PASS
- 監査記録：CHAT_AUDIT_C_GAP_NUMERIC_CONTRACT_V0_DESIGN_V1_ADDENDUM_V1_2026-10-10.md
  SHA-256 prefix 9b026f66…f526
- Judge ruling S1：endpoint は 累積 mean-value form に変更する。
- G0/E1 v3：CHAT AUDIT PASS。ただし D6 の外部監査は FREEZE blocker。
この v1 は、v0 の数値契約のうち監査で PASS した値を維持し、endpoint partition だけを S1 裁定に従って置換する。実行結果を見て方式・partition・precision・degree を変更してはならない。
Part I — 空白①
1. λ coarse grid
①全体の coarse grid は
\[
\boxed{\Delta\lambda=1/3200}.
\]
region	interval	width	coarse slabs
L	[2/5,699/1600]	59/1600=118/3200	118
X	[699/1600,281/640]	7/3200	7
R	[281/640,9/20]	7/640=35/3200	35
total	[2/5,9/20]	1/20=160/3200	160


region boundary を跨ぐ slab は作らない。
λ refinement
\[
\boxed{\text{MAX\_DEPTH}=3}.
\]
したがって
\[
\boxed{\text{MAX\_ACCEPTED}=1280},
\qquad
\boxed{\text{MAX\_ATTEMPTED}=2400}.
\]
R は高 λ → 低 λ の順で処理し、REFINE 時は right child first。
2. ① precision / approximation degree
①は baseline C1b との差分を最小化し、同一 kernel を同一数値環境で比較できるようにするため、C1b と同じ固定精度を採用する。
- producer：\(\boxed{160\text{ bits}}\)
- checker：\(\boxed{192\text{ bits}}\)
- series / approximation degree：\(\boxed{50}\)
- U_STAR=3/5
- W0=1/16
- PRED_ACCEPT=1/64
- ROOT_TARGET=1/128
これは②の precision ladder と異なるが、①では baseline identity / diff-auditability を優先した事前宣言である。
runtime precision escalation は禁止する。160/192 bits で不確定なら PRECISION_INCONCLUSIVE。
3. R の C1b-derived stages
predictor
- PRED_GRID_DEN=1024
- PRED_SCAN_PANELS=256
tube
- T0：8 t cells × 4 λ cells × 4096 s-panels
- T1：16 × 8 × 4096
- T2：32 × 16 × 8192
root
- ROOT_MV_STEPS=8
- ROOT_G_PANELS=32768
- ROOT_GT_PANELS=8192
- ROOT_GL_PANELS=8192
- ROOT_GT_T_CELLS=16
- ROOT_GL_T_CELLS=16
- ROOT_GL_CORNER_K=16
- ROOT_GL_CORNER_TAU=65535/65536
- ROOT_GT_CLAMP_TAU=255/256
- ROOT_GL_CORNER_WALL_PANELS=8192
- ROOT_GT_REFINE_DEPTH=2
- T2_ENDPOINT_REFINE_DEPTH=4
P1/P2 と上記 stage は run 中に変更しない。
4. L の lower/interior negative grid
L の [1/2,31/32] は direct g_box<0。
initial allocation：
- E0_TBOXES=24
- E0_LBOXES=8
panel ladder：
- E0 = 1024
- E1 = 2048
- E2 = 4096
caps：
- E_BOX_CAP=4096
- MONO_WORK_CAP=1,048,576
L で predictor/root path へ移らない。
5. X の fixed tube / negative block
[1/2,5/8]
- X-T0：8 × 4 × 4096
- X-T1：16 × 8 × 4096
- X-T2：32 × 16 × 8192
全 cell で Gt.upper()<0。
[5/8,31/32]
- initial t boxes = 24
- λ split = 8
- panels = 1024 → 2048 → 4096
- E_BOX_CAP=4096
edge ownership：
- t=5/8：negative g block owner。lower Gt tube は overlap check。
- t=31/32：endpoint block owner。negative block は overlap check。
6. ① endpoint：累積 mean-value partition
seed
seed は
\[
\boxed{t_0=31/32}
\]
のみ。
各 current λ slab Λ_c について
\[
G_0(\Lambda_c)
:=
\sup_{\lambda\in\Lambda_c}g(31/32,\lambda)
\]
を direct g_box で計算する。
- seed g_box s-panels：\(\boxed{8192}\)
- 成功の必要条件：G0_upper < 0
- (31/32,1) 内では direct g_box を一切使わない。
t partition
\[
[31/32,1]
\]
を 16 等分する。
\[
\boxed{\Delta t=1/512}.
\]
exact breakpoints：
\[
t_j=\frac{31}{32}+\frac{j}{512},
\qquad
j=0,1,\ldots,16.
\]
各 box：
\[
Q_j=[t_j,t_{j+1}]\times\Lambda_c,
\qquad
j=0,\ldots,15.
\]
各 \(Q_j\) で gt_box を評価する。
- s-panels：\(\boxed{8192}\)
- \(j=15\) の box は \(t=1\) に接するので既存 corner/ordinary endpoint dispatch を使う。
- \(j=0,\ldots,14\) は ordinary chart。
- t partition の追加 refinement は禁止。
- λ slab refinement は MAX_DEPTH=3 の範囲でのみ許す。子 slab でも同じ16 t-boxesを使う。
cumulative gate
各 box の interval upper bound を
\[
U_j
=
\sup_{Q_j}G_t
\]
とする。
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
を計算し、
\[
\boxed{U_{\rm cum}<0}
\]
を endpoint strip の唯一の成功条件とする。
全加算項は非負なので、最終 cumulative bound が負なら各 partial cumulative bound も負であり、各 box 内の全 \(t\) に対して \(g(t,\lambda)<0\) が従う。
禁止：
- (31/32,1) の direct g_box
- C_\Lambda(1-t) の runtime 使用
- endpoint t partition の runtime 変更
- box ごとの別方式への切替
7. ① work ceilings
v0 の PASS 済み ceiling を維持する。
- ATTEMPT_WORK_CEILING = 25,600,000
- GLOBAL_ATTEMPT_WORK_CEILING = 61,440,000,000
- ACCEPTED_WORK_CEILING = 32,768,000,000
- CPU budget：96 core-hours
- RAM：32 GiB
- output：10 GiB
cap 到達は RESOURCE_CAP。数学的反例ではない。
Part II — 空白②
8. λ source / refinement
primary λ slabs は sealed C1b accepted ledger の unclamped slabs。再 coarse-gridding しない。
- λ binary refinement depth ≤ \(\boxed{10}\)
- ledger slab ID / exact endpoints を保持
- run 後に slab endpoint を変更しない
seal path / ledger pin の確認は FREEZE blocker。
9. ② endpoint start と equal-box rule
各 slab Λ について
\[
\boxed{
t_*(\Lambda)=\max(31/32,t_+(\Lambda))
}.
\]
seed はこの一点だけ。
\[
G_*(\Lambda)
=
\sup_{\lambda\in\Lambda}g(t_*(\Lambda),\lambda).
\]
seed g evaluation
②では predeclared escalation を許す。
s-panel ladder：
\[
\boxed{4096\to8192\to16384}.
\]
同じ \(t_*,\Lambda\) を再評価するだけで、method / partition は変えない。
number of endpoint boxes
\(t_*<1\) のとき
\[
\boxed{
N(\Lambda)
=
\left\lceil 512(1-t_*(\Lambda))\right\rceil
}.
\]
これは [t_*,1] を equal-width boxes に分けたとき、各幅を ≤1/512 にする最小の正整数である。
\(t_*\ge31/32\) なので
\[
1\le N(\Lambda)\le16.
\]
幅を
\[
\boxed{
\Delta t_\Lambda
=
\frac{1-t_*(\Lambda)}{N(\Lambda)}
\le\frac1{512}
}
\]
とし、
\[
t_j=t_*+j\Delta t_\Lambda,
\qquad
j=0,\ldots,N.
\]
この rule は \(t_*\) だけから exact rational に決まり、run 中に変更しない。
Gt boxes
\[
Q_j=[t_j,t_{j+1}]\times\Lambda_c.
\]
各 \(Q_j\) で gt_box。
- s-panels：\(\boxed{8192}\)
- 最終 box \(Q_{N-1}\) は \(t=1\) に接するため corner/ordinary endpoint dispatch。
- それ以前は ordinary chart。
- endpoint t refinement は禁止。
- λ refinement depth≤10 のみ許す。
cumulative gate
\[
U_j=\sup_{Q_j}G_t.
\]
\[
\boxed{
U_{\rm cum}^{(2)}
=
G_*(\Lambda_c)
+
\sum_{j=0}^{N-1}
\Delta t_\Lambda\max(0,U_j)
}
\]
とし、
\[
\boxed{U_{\rm cum}^{(2)}<0}
\]
を endpoint strip の唯一の成功条件とする。
(t_*,1) 内では direct g_box を使わない。
10. ② precision / approximation degree
②は既存 v3 の precision ladder を維持する。
producer：
\[
\boxed{256\to512\to1024\text{ bits}}
\]
checker：
\[
\boxed{320\to640\to1280\text{ bits}}
\]
approximation / series degree：
\[
\boxed{50}.
\]
precision level を上げても box / method / partition は同一。
degree 50 で不確定でも runtime で degree を増やさない。
11. ② caps
- λ refinement depth≤10
- endpoint t refinement：0（equal-box ruleのみ）
- total endpoint cells≤\(\boxed{1,048,576}\)
- CPU：48 core-hours
- RAM：32 GiB
- output：10 GiB
D5 と同時占有しない。Judge scheduling ruling がなければ SCHEDULING_HOLD。
Part III — 共通状態
12. B_ob
B_ob<0 は独立 gate ではない。
endpoint cumulative certificate が通れば G0/E1 continuity により
\[
g(1,\lambda)=B_{\rm ob}(\lambda)<0
\]
が帰結する。
既存 B_ob receipt は
BOB_SIGN_CONSISTENCY_CHECK
のみ。
receipt 単独で slab / box を ACCEPT しない。
13. FAIL-CLOSED vocabulary
共通：
- DOMAIN_MISMATCH
- CONTRACT_MISMATCH
- PRECISION_INCONCLUSIVE
- APPROX_DEGREE_INCONCLUSIVE
- NONFINITE
- RESOURCE_CAP
- COVERAGE_FAILED
- BOB_SIGN_CONSISTENCY_FAILED
endpoint：
- ENDPOINT_SEED_G_INCONCLUSIVE
- ENDPOINT_GT_CELL_INCONCLUSIVE
- ENDPOINT_CUMULATIVE_MVT_INCONCLUSIVE
- ENDPOINT_PARTITION_MISMATCH
①：
- DIFF_OUTSIDE_ALLOWLIST
- IMPORT_BLOB_MISMATCH
- PREDICTOR_RULE_MISMATCH
②：
- SEAL_PATH_OPEN
- LEDGER_MISMATCH
- SCHEDULING_HOLD
これらは数学的反例を意味しない。
14. FREEZE 条件
1. この numeric contract v1 の CHAT AUDIT / Judge ruling。
2. D6：5afa815f... と 7cb9b809... の外部監査。
3. ① implementation と full diff audit。
4. ① import closure 15本の blob identity audit。
5. ② seal path / ledger pin audit。
6. producer/checker の partition・precision・degree・ownership の一致確認。
FREEZE までは一切実行しない。