# chat 監査記録：C 空白② 事前宣言 DRAFT v4（A案）

2026-11-15 / chat / 文書の監査（計算なし）

## 対象

| 文書 | SHA-256 |
|---|---|
| `C_GAP2_PREDECLARE_DRAFT_V4_A_20261115.md`（Dig 起草、106行） | `8aff8493cba66d21eb47bffe27b3e5f95f8610d2fde2466ab7433643b99b01a5` |
| 旧 v3 `drafts/2026-10-10/C_GAP2_PREDECLARE_DRAFT_V3.md` | `b9647d1f889eafbeb2a954b69ace520ee04be7881d828390002cacbcf93d55be` |
| 共通 endpoint 追補 v2 `drafts/2026-10-10/C_GAP_ENDPOINT_ADDENDUM_DRAFT_V2.md` | `7471800d81caabdbbe3bfb5c8dc2e020434adbd0a67ed4e6bbd38afbea33d3a4` |
| G0/E1 v3 `drafts/2026-10-10/G0_E1_UNIFORM_GT_PAPER_PROOF_DRAFT_V3.md` | `8bf8f5d87cfc2e6f424499804b0fd85d982cf480deb99a26c284367960578671` |
| 空白① run4 の 25 blob 表 `runs/2026-10-12/C_GAP1_V0_5_RUN4/RUN_COMMIT_25_BLOBS.tsv` | `ec5b70b6cc8ebd0ab29fc31021ead613526cc3187efe09f1d6a6d795b810dd00` |

封印入力の第三の控え（`evidence/c-gap2-sealed-inputs-20261115`、commit `ff09197`）は、chat が GitHub から4ファイルを読み出して SHA-256 を計算し、固定値と64桁一致した（`1e46da3a…`、`09caf7b9…`、`c31af672…`、`8a332e56…`）。

## 判定

**方向は PASS、FREEZE には修正が要る（v4-r1）。** §3 の累積の平均値形の門（U_cum ＝ G_seed ＋ Σ Δt·max(0, U_j) < 0）は正しい。G0/E1 v3 が t ∈ [1/2, 1)、λ ∈ [2/5, 5/8] で g が C¹、G_t ＝ ∂_t g と同定し、t ＝ 1 へ連続に延びるので、任意の t ∈ [t_e, 1] で g(t) ≤ g(t_e) ＋ ∫ max(0, ∂_t g) ≤ U_cum < 0 となる。空白②の範囲（λ ∈ [9/20, 931/1600]、t ≥ t_e > 1/2）は G0/E1 v3 の範囲の内側にある。

## 要修正（数学：FREEZE の前に必須）

**M1. t ∈ (t₊(Λ), 31/32] の持ち主が書かれていない。** t₊ < 31/32 の区画では、t_* ＝ 31/32 から上を②が受け持つが、その下の (t₊, 31/32] を g < 0 で押さえている証明が、どの Judge の主張にも入っていない。

- C1b の Judge request の主張は (A)〜(E) で、管の内側 [t₋, t₊] の Gt、二つの壁、被覆の正確さだけである。
- C1b の machine receipt は、左の外側 [1/2, t₋] の被覆（経路 B、159 区画）を数えているが、右の外側は数えていない。
- 実際には、C1b 改訂 v2.4（`GLOBAL_AXIAL_C1B_MONOTONE_CLOSURE_WALL_ADJACENT_EXTERIOR_PRE_RUN_AMENDMENT_V2_4.md`）が右の外側 [t₊, T_MID_HI ＝ 31/32] を規則「Gt < 0 on [t₊, b] かつ G(t₊) < 0 ⇒ G < 0」で証明しており、封印台帳に記録があるはずである。ただし、それは receipt にも Judge の主張にも上がっていない。

直し方（chat の推奨は (i)）：

- (i) L0(c) の照合項目に「unclamped の全区画で、右の外側 [t₊, 31/32] の被覆が両系統の台帳にあり、unresolved ＝ 0」を加え、②の Judge request でこれを C1b からの取り込みとして主張に含める。新しい計算は要らない。
- (ii) (i) の照合が通らない区画では、②が [t₊, 31/32] × Λ を、空白① の X 群と同じ「負の g の箱」で計算し直す（追補 v2 §6 の ① X と同じ持ち主の規則）。

**M2. 端点の道具を新しく決め直さず、空白① run4 の凍結済みのコードに pin する。** §4 の blocker（`ENDPOINT_GT_CONTRACT_OPEN`、`APPROX_DEGREE_OPEN`、`CORNER_CHART_PIN_OPEN`）は、run4 の RUN_COMMIT `26d81e1049340d44ef7f08ae8e17d0692983395b`（25 blob 表 `ec5b70b6…`）の端点の関数（`producer/endpoint_interval_producer.py` `51060fea`、`checker/endpoint_interval_checker.py` `4cb16f8a`、`checker/endpoint_local_checker.py` `2bddddf6`、`checker/endpoint_local_controls.py` `c913c47d` など、chat 監査済み）を、同じ引数（panel 数、次数、精度、corner/ordinary の判定）で使うと書けば閉じる。②で変わるのは入力の範囲（区画と t_e）だけ、と明記する。

## 指摘（手順：v4-r1 で一緒に直す）

1. **pin の書き方。** §0 の追補 v2 と G0/E1 v3 に、commit（`4c04d57`）と SHA-256 を付ける（上の表の値）。
2. **期待数。** unclamped ＝ 159 − 35 ＝ 124 区画（λ ∈ [9/20, 931/1600]）を期待値として書く。L0(c) で実データと照合する。
3. **規模の見積もり。** t_e ≥ 31/32 なら N(Λ) ≤ 16 なので、Gt の箱は 124 × 16 ＝ 1,984 以下、seed は 124 である。48 core-hours の上限には十分な余裕がある。実測は run4 の端点の門の 1 箱あたりの時間から出す。
4. **λ の細分。** 失敗した区画の λ 二分は、空白① の規則（二分子の端点の持ち主を含む）をそのまま使うと書く。
5. **条件。** ②の結論も、空白① と同じく C 側の補題束（D6：`5afa815f`、`7cb9b809`）が条件として付く。この束は chat が次に監査する（P1 ノートと同じやり方）。

## 次の工程

v4-r1（M1・M2 と指摘1〜5）→ chat 監査 → Judge FREEZE → 本走（L0(c)(d) → producer → checker）。v4 の起草と第三の控えの登録は、FREEZE や実行の許可ではない（v4 §0 のとおり）。
