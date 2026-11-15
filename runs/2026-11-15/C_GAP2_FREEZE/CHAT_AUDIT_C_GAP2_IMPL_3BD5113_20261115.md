# chat 監査記録：C 空白② 実装の修正 `3bd5113`（直親 `ff07e09`）

2026-11-15 / chat / 差分と静的な監査（実行なし、封印入力は読んでいない）

## 対象

`cotaxxxx/bg-oblate-spheroid`、branch `implement/c-gap2-v4-r2-20261115`、commit `3bd5113e7d26e2860ddb8228904d977842aef541`。直親が `ff07e09` の単一 commit であることを確かめた。変更は5ファイル（+294/−29 行）：`endpoint_driver.py`、`lineage_compare.py`、`runtime_identity.py`、`README`（改修）、`end_to_end_preflight.py`（新規）。kernel と gating は変わっていない。

## 判定

**PASS（G1〜G5 はすべて対応済み）。残りは小さな直し2点（H1、F7）である。数値の preflight は、その直しを入れた最終の commit で流すのがよい。**

## 1. 前回の指摘への対応

| 指摘 | 対応 | 判定 |
|---|---|---|
| G1（t_e の型） | `Fraction(ev["endpoint_seed_t"])` と `Fraction(item["t_e"])` の両方を親の t_e と比べる | PASS |
| G2（端から端までの対照） | `full_run` を、L0(c) と、共通の実行部分 `run_parent_set` に分けた。`end_to_end_preflight.py` は、合成の親2つ（λ ∈ [1/2, 1/2 ＋ 1/1600]、t_e ＝ 993/1024 と、隣の区画で 63/64）を、本物の kernel・gating・Ledger・manifest・runtime_identity で流し、`lineage_compare --synthetic-two-parent` で比べる。強制 ABORT の経路（本物の門を1回呼んだ後に ABORT、segment_end、manifest の ABORT_NOT_EVIDENCE、前後の同一性）も通す | PASS |
| G2 の安全柵 | SEALED のときは親124が必須で、テスト用の強制 ABORT は禁止。合成のときは親2が必須で、封印入力と Judge の裁定を読まない。状態は `SYNTHETIC_COMPLETE_NOT_EVIDENCE` | PASS |
| G3（import の違い） | pin した集合（変更分と run4 の25）の辞書と、系統ごとの import の閉包を分けた。系統間で比べるのは前者だけ | PASS |
| G4（門の算術の独立な検算） | `check_gate_arithmetic`：一般の式で分割を作り直して t 区間と一致すること、最終箱だけ corner/ordinary の振り分け、各箱の寄与 ＝ max(0, upper)、厳密な分数の seed ＋ Δt・Σ寄与 ≤ 記録の累積上界 < 0、N と Δt の記録との一致 | PASS |
| G5（lscpu の記録） | header と segment_end の直後だけ許し、ほかの位置では止める。連鎖の検査には含める | PASS |
| `runtime_identity` の直親 | `BASE_NEW ＝ ff07e09`、`PREVIOUS_NEW ＝ 45617d0`、祖父 `26d81e1` の鎖を検査する | PASS |

## 2. 残りの直し（最終 commit に入れる）

**H1. 本番の比較で、入力の pin と Judge の裁定の SHA を固定値と照合する。** 比較器は SEALED のとき、両系統の `input_sha256` が互いに等しいことしか見ていない。`run_parent_set` は公開の関数なので、L0(c) を通らない親の一覧でも `mode="SEALED"` の manifest を作れてしまう。次を加えること。

- SEALED の比較で `input_sha256` が `sealed_contract.PINNED`（4ファイルの SHA）と完全に一致すること。
- `judge_ruling_sha256` が、比較器に引数で渡す Judge の FREEZE 裁定の SHA と一致すること。

本走の後に chat が封印入力と突き合わせて検収するので、致命的ではない。しかし比較器だけで本物の実行かどうかが決まるようにしておくべきである。

**F7（前々回から）。** `c1b_receipt_extract.json` の件数（accepted 159、clamped 35）を、台帳から数えた値と照合する。

## 3. 次の工程（効率の観点から）

`runtime_identity` は直親の commit を固定するので、H1・F7 を入れた commit を作ると、それより前の commit で流した preflight の同一性はそのまま使えない。したがって次の順がむだがない。

1. H1・F7 を入れた最終の単一 commit（直親 `3bd5113`、`BASE_NEW` などの定数も更新）。
2. chat の差分監査（小さい差分なので短時間）。
3. その commit で preflight 一式を流す（すべて NOT_EVIDENCE、封印入力は読まない）。
   - `run4_regression.py`（両系統）
   - `synthetic_preflight.py`（両系統と比較）
   - `end_to_end_preflight.py`（両系統の正常終了、両系統の強制 ABORT、`--compare`）
4. chat の検収 → Judge FREEZE・実行許可 → L0(c)(d) → 本走 → 比較 → chat の検収 → Judge の採否。
