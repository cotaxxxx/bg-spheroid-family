C 空白①② — t=1 近傍 endpoint 契約追補 DRAFT v2
状態：DRAFT ADDENDUM v2 / NOT FROZEN / EXECUTION PROHIBITED。
基準：
- bg-spheroid-family main 1c9a6e036884d58de782bc47cb220700187fe511 / STATE v1.13
- 空白① contract v6
- 空白② contract v3
- implementation design v1：CHAT AUDIT PASS
- endpoint addendum v1：CHAT AUDIT PASS as text
- numeric contract v0：CONDITIONAL PASS
- 監査記録：
  CHAT_AUDIT_C_GAP_NUMERIC_CONTRACT_V0_DESIGN_V1_ADDENDUM_V1_2026-10-10.md
  SHA-256 prefix 9b026f66…f526
- Judge ruling S1：endpoint の実装詳細を 累積 mean-value form に置換する。
- G0/E1 v3：CHAT AUDIT PASS。D6 は未完了。
この v2 は、v1 の「interior direct-g + final mean-value box」を廃止し、seed の g と endpoint strip 全体の Gt 累積上界だけで閉じる。
1. 共通原理
endpoint start を \(t_e\) とする。
\[
t_e=t_0<t_1<\cdots<t_N=1
\]
を FREEZE 前の規則で固定し、
\[
Q_j=[t_j,t_{j+1}]\times\Lambda.
\]
seed で
\[
G_{\rm seed}
=
\sup_{\lambda\in\Lambda}g(t_e,\lambda)
\]
を1回だけ direct g_box で評価する。
各 endpoint box では
\[
U_j=\sup_{Q_j}G_t
\]
を direct gt_box で評価する。
累積上界
\[
\boxed{
U_{\rm cum}
=
G_{\rm seed}
+
\sum_{j=0}^{N-1}
(t_{j+1}-t_j)\max(0,U_j)
}
\]
に対して
\[
\boxed{U_{\rm cum}<0}
\]
を endpoint certificate の唯一の成功条件とする。
なぜ strip 全体が閉じるか
各 box 内で、右向き増加に寄与し得る derivative の上限は \(\max(0,U_j)\) である。
したがって任意の partial path の増加量は対応する partial sum 以下。
全項が非負なので partial sum は full sum 以下であり、full cumulative upper bound が負なら
\[
g(t,\lambda)<0
\]
は endpoint strip 全体で成立する。
G0/E1 の \(C^1\) interior と \(t=1\) の左微分により、この mean-value 使用が正当化される。
2. 禁止事項
endpoint strip の内部では：
- direct g_box を使わない。
- C_\Lambda(1-t) を runtime gate に使わない。
- B_ob receipt を代替 gate に使わない。
- partition を run 中に変更しない。
- Gt cell が不確定なとき別方式へ切り替えない。
許される direct g_box は seed \(t=t_e\) のみ。
3. 空白①
①では
\[
\boxed{t_e=31/32}.
\]
fixed partition
\[
[31/32,1]
\]
を16等分：
\[
\boxed{\Delta t=1/512}.
\]
\[
t_j=31/32+j/512,\qquad j=0,\ldots,16.
\]
16個すべてで Gt enclosure を計算する。
最終 box [t_15,1] は t=1 に接するため既存 corner/ordinary endpoint handling を使う。
それ以前の15 box は ordinary chart。
seed
\[
\sup_{\lambda\in\Lambda}g(31/32,\lambda)
\]
のみ direct g_box。
gate
\[
\boxed{
\sup g(31/32,\Lambda)
+
\sum_{j=0}^{15}
\frac1{512}
\max(0,\sup_{Q_j}G_t)
<0
}.
\]
L/X/R のすべてで同じ endpoint rule を使う。
4. 空白②
各 sealed unclamped slab Λ について
\[
\boxed{
t_e=t_*(\Lambda)=\max(31/32,t_+(\Lambda))
}.
\]
deterministic equal partition
\(t_*<1\) なら
\[
\boxed{
N(\Lambda)
=
\lceil512(1-t_*)\rceil
}
\]
とする。
\[
\Delta t_\Lambda=\frac{1-t_*}{N(\Lambda)}\le1/512.
\]
これは各 box 幅を ≤1/512 にする最小の equal-box count であり、\(t_*\) だけから exact に決まる。
\[
t_j=t_*+j\Delta t_\Lambda.
\]
seed
direct g_box は
\[
t=t_*
\]
のみ。
既存 C1b evidence は overlap consistency として残すが、seed の代わりにしない。
Gt boxes / gate
全 endpoint box で gt_box。
最終 box は corner/ordinary endpoint handling。
\[
\boxed{
\sup g(t_*,\Lambda)
+
\sum_{j=0}^{N-1}
\Delta t_\Lambda
\max(0,\sup_{Q_j}G_t)
<0
}
\]
を唯一の成功条件とする。
5. B_ob の扱い
①の旧 G1「B_ob<0 on [2/5,9/20]」は独立 gate ではない。
endpoint cumulative certificate と G0/E1 continuity から
\[
g(1,\lambda)=B_{\rm ob}(\lambda)<0
\]
が自動的に従う。
②でも B_ob receipts は
BOB_SIGN_CONSISTENCY_CHECK
のみ。
receipt と endpoint certificate の帰結が矛盾した場合は consistency/provenance failure として停止する。
receipt 単独で ACCEPT しない。
6. t-edge ownership
① X
- t=5/8：negative g block owner。lower tube は overlap check。
- t=31/32：endpoint seed owner。lower negative block は overlap check。
① L/R
- t=31/32：endpoint seed owner。
②
- t=t_*：② endpoint seed owner。既存 C1b evidence は overlap consistency。
- t=1：endpoint certificate の consequence。B_ob receipt は consistency only。
7. FAIL-CLOSED
- ENDPOINT_SEED_G_INCONCLUSIVE
- ENDPOINT_GT_CELL_INCONCLUSIVE
- ENDPOINT_CUMULATIVE_MVT_INCONCLUSIVE
- ENDPOINT_PARTITION_MISMATCH
- ENDPOINT_NONFINITE
- ENDPOINT_RESOURCE_CAP
- BOB_SIGN_CONSISTENCY_FAILED
これらは数学的反例を意味しない。
8. 依存条件
この endpoint rule は G0/E1 v3 の：
- paper derivation PASS
- G_t=T1+T2+T3 symbolic identity PASS
- machine Gt source-formula identification PASS
を使用する。
ただし元の2補題：
- 5afa815ff24760ab5ebbb63bcbae912c9c7a84c6
- 7cb9b8091596510203d74e09387bc1e8188b8b47
は D6 外部監査待ち。
さらに：
- ① implementation / diff audit
- ② seal path confirmation
- numeric contract v1 audit
が閉じるまで FREEZE しない。