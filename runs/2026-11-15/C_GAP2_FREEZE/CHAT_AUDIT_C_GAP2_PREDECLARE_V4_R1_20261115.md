# chat 監査記録：C 空白② 事前宣言 DRAFT v4-r1（A案）

2026-11-15 / chat / 文書の監査と、凍結コード（空白① run4）の読み取り照合（計算なし）

## 対象

| 文書・コード | 識別 |
|---|---|
| `C_GAP2_PREDECLARE_DRAFT_V4_R1_20261115.md`（Dig 起草、147行） | SHA-256 `89aee2da5f378168562ff78f42b9fbbe0c210e8f8633a43023f1c0c64db5b1b8` |
| 前回の chat 監査記録（Dig が受領した写し） | SHA-256 `5fc59b3913e0266a1964b4f631540774cd4d6e472c83f046791a2e4c6c1de7b7`（chat の原本と一致） |
| 空白① run4 の凍結コード | `cotaxxxx/bg-oblate-spheroid` `run/c-gap1-v0-5` ＝ `26d81e1049340d44ef7f08ae8e17d0692983395b`（GitHub から読み取り） |

## 判定

**M1 は PASS。M2 は数値の値は PASS だが、FREEZE の前に直しが要る（v4-r2）。**

### M1（右の外側）：PASS

§1 の3区間の持ち主（C1b の管、C1b v2.4 の右の外側の取り込み、②の上側の累積の門）、L0(c) の照合項目、照合が通らない区画の扱い（保留して別紙で再 FREEZE）、§6 の Judge request の文案は、前回の指摘どおりで足りる。

### M2（run4 の道具）：値は一致、ただし2点の直しが要る

凍結コードの定数を読み、v4-r1 §4 の表と照合した。

| 項目 | v4-r1 | 凍結コード（`gap1_producer`／`gap1_checker` の `global_axial_c1b_kernel.py`） | 判定 |
|---|---|---|---|
| 精度 | 160／192 bit | `BITS, DEG = 160, 50`／`192, 50` | 一致 |
| 次数 | 50 | 同上 | 一致 |
| seed の panel | 8192 | `ENDPOINT_SEED_PANELS = 8192` | 一致 |
| Gt の panel | 8192 | `ENDPOINT_GT_PANELS = 8192` | 一致 |
| λ の深さ | ≤3 | `MAX_DEPTH = 3` | 一致 |
| 箱の幅 | ≤1/512 | `ENDPOINT_DT = 1/512` | 一致 |
| 門の式 | U_cum < 0 のみ | `endpoint_gate(slab)`：seed の `g_box` 1回、全 `gt_box`、U_cum < 0 だけが成功条件、t の細分なし、最終箱だけ corner/ordinary | 一致 |

**M2-a. pin するファイルが違う（chat の前回の書き方の誤り）。** 前回の監査記録で例に挙げた4本（`producer/endpoint_interval_producer.py` `51060fea` ほか）は、端点の門そのものではない。門と `g_box`・`gt_box` は次のファイルにある。v4-r1 §4 の「最低限の endpoint 関数 pin」を次に差し替え、25 blob 全体の照合はそのまま残す。

| ファイル | 凍結 blob（25 blob 表より） |
|---|---|
| `gap1_producer/global_axial_c1b_kernel.py` | `5503bb7da981ef90266a9cdd67de2bef07998fd8` |
| `gap1_checker/global_axial_c1b_kernel.py` | `b4bb44bdf57dc2ec6e5a1b3b262acdfec7e07a39` |
| `gap1_producer/global_axial_c1b_gating.py` | `baffaf4952364cce94411b8982ce57c3a5d7bea1` |
| `gap1_checker/global_axial_c1b_gating.py` | `36bb7983f2a806ba3d87b7f486aafd22ea1a5184` |

**M2-b. 凍結の門は t_e ＝ 31/32、16 箱に固定されている。** `endpoint_partition()` は `ENDPOINT_T_SEED == T_MID_HI`（＝31/32）と16箱を検査し、違えば `ENDPOINT_PARTITION_MISMATCH` になる。したがって t₊(Λ) > 31/32 の区画（t_e ＝ t₊）は、凍結コードのままでは扱えない。v4-r1 の規則では `RUN4_INTERFACE_MISMATCH → STOP` になる。そうした区画があるかどうかは L0(c) まで分からない（台帳は FREEZE 前に読まない）。そのため、設計の段階で両方の場合に備える必要がある。

また、空白① の駆動部は [2/5, 9/20] の L・X・R の区画を回すもので、C1b の封印台帳から区画を読む入口がない。②には、端点の門だけを回す小さな駆動部が新しく要る。

直し方（v4-r2）：

1. **門の一般化を、宣言した最小の差分として行う。** `endpoint_gate(slab)` を `endpoint_gate(slab, t_e)` にし、分割を t_j ＝ t_e ＋ j·Δt、N ＝ ⌈512(1 − t_e)⌉、Δt ＝ (1 − t_e)/N にする。`g_box`、`gt_box`、精度、次数、panel、chart の判定は変えない。両系統（producer と checker の kernel）に同じ差分を入れ、chat が差分を監査する。
2. **回帰の対照。** t_e ＝ 31/32 では N ＝ 16、Δt ＝ 1/512 になり、run4 と同じ分割に戻る。run4 の端点の門を通った区画のうち数個で、一般化した門の記録が run4 の記録と（作業量・上界の分数まで）一致することを、本走の前の preflight で確かめる。
3. **端点だけの駆動部を新しく書く。** 封印台帳から unclamped の区画と t₊ を読み（L0(c) と同じ読み方）、両系統で一般化した門を呼ぶ。失敗した区画は空白① の規則で λ を二分し（深さ ≤3、子の端点の持ち主も同じ）、記録を台帳に書き、系統間で比べる。これは新しいコードなので、chat の差分・静的監査の対象にする。
4. v4-r1 §4 の「勝手に改造して本走に使わない」はそのまま正しい。上の 1〜3 を v4-r2 で**宣言して監査する改造**に置き換える、という位置づけにする。

## そのほか（v4-r2 で一緒に直す、手順）

- §5 の見積もり（seed 124、Gt 1,984、λ 細分の最大 15,872）は妥当。t_e > 31/32 の区画では N < 16 なので、Gt の箱はこれより少なくなる。
- §7 の FREEZE の条件 (c)（D6 の補題束の監査）は chat が次に行う。

## 次の工程

v4-r2（M2-a・M2-b）→ chat 監査 → 一般化した門と駆動部の実装 → chat の差分監査と回帰の対照 → D6 の監査 → Judge FREEZE → 本走。
