# B7 独立 verifier（chat 監査ツール）— 2026-11-04

Judge 決定 #1（全リーフを独立カーネルで再計算）のための chat 製監査ツール。Dig の producer モジュールは import していない。

## 何を独立に確かめるか

検証の主張は次のとおり。各外箱 O = λ×τ×δ について、Dig のリーフ分割の上で chat 自身の下界を合計し、次の量が正であることを示す。

  λ(2/π)·Σ_leaf L_leaf − 2λ⁺·(275/4)·σ(P0)

これが正なら、O のすべての点で H > 0 である。

| 項目 | chat の実装 | Dig との関係 |
|---|---|---|
| 表示 H = λ(2/π)∫[0,1]⁴ Σ_ε K | P1 の F_xx 直接積分と浮動小数で照合する（selftest 4） | 公式は同じ。正しさは P1 から独立に確認した |
| 区間演算 | float64 の端点。誤差なし変換（TwoSum / Dekker TwoProduct）で厳密な方向付き丸めを行う | Dig は 2^-128 固定小数点。実装は別 |
| 2-jet 自動微分 | 自作（区間成分） | 実装は別 |
| リーフの被覆 | ギロチン再帰で [0,1]×[P0,1]×[0,1]² の厳密な tiling を検査する | 自前の検査 |
| MIDPOINT | 反復 1 次元中点則の厳密剰余と、外変数の中心形式 ∩ 直接形式 | 数学は同じ、実装は別 |
| ZEROTH | vol × inf K | 同上 |
| K_FLOOR | F ≥ −275/4（Astra 補題1）。Δβ ≤ 2(t_b−t_a)/(1+t_a t_b) | Dig の Δβ ≤ 2Δt/(1+t_a²) より緻密で、これも有効 |
| ASTRA3 | F ≥ −b₃[1−3ρ/2]₊（Astra 補題2）。ρ の下界は3経路（直接、λ²cp²、|r×v|²）。b₃ ≤ min(b₃, 2W/λ³, 275/4)。δ は幾何分割したスラブの min | 数学は同じ。Δβ を上と同じく緻密化 |
| 2/π | Machin 公式による厳密な有理区間 | Dig は 7/11 ≤ 2/π ≤ 2/3 |

producer のリーフ情報のうち使うのは、どの外分割を使うかの指定（outer_parts、delta_boxes、rem_parts）だけである。delta_boxes が外箱の δ を tiling しているかどうかは verifier が検査する。

## L0_T3_D1 での照合（このコンテナで実行）

- リーフファイルの SHA 3f80a336… は宣言値と一致。TILING PASS（127,185 ノード）。
- chat の最終下界は 9.54e-3 で PASS。Dig の最終下界は 3.79e-4。
- MIDPOINT と ZEROTH は、Dig との差が丸めの粒度程度しかない（合計 1e-20 以下）。
- 差の大部分は ASTRA3 の Δβ 緻密化から来ている。

## 実行（daybreak-works）

```
mkdir -p ~/B7_work/b7iv && cd ~/B7_work/b7iv && unzip -o ~/B7IV_CHAT_VERIFIER_20261104.zip
python3 -I b7iv_selftest.py
python3 -I b7iv_all.py ~/B7_work --workers 10
```

- 依存は numpy だけ。
- 各 key について、producer status が PASS の最新リーフファイルを自動で選ぶ。
- 結果は B7IV_SUMMARY.txt と out/<KEY>.log に出る。
- 1箱あたり約 6 万リーフで、10 workers なら数分。
- PASS ではない箱が出た場合、それは「chat の下界ではこの分割で足りない」という意味で、反例ではない。差の大きさを記録して chat に返す。
