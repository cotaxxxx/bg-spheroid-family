# chat 検収記録：C 空白② preflight（実装 `0d32ac2`、NOT_EVIDENCE）

2026-11-15 / chat

## 対象

`bg-spheroid-family` branch `evidence/c-gap2-preflight-0d32ac2-20261115` commit `e20ade6`、zip `C_GAP2_PREFLIGHT_0D32AC2_20261115.zip`。GitHub から取り出し、SHA-256 `9653bdde540ea3db3d10941fa1be95c1a878a7002df9a210c513271be945b637` の一致と、中の SHA256SUMS（51行）の照合を確かめた。

## 判定：PASS（NOT_EVIDENCE）

| 確かめたこと | 結果 |
|---|---|
| 13 手順すべての HEAD と作業木 | HEAD `0d32ac2…`、clean（各手順の前の記録） |
| 環境 | Python 3.11.16、python-flint 0.9.0、ほかの重い計算なし |
| run4 原本2本の SHA | GitHub の run4 `SHA256SUMS.txt` と一致（`4b58a61f…`、`5636da10…`） |
| 静的検査（両系統） | PASS。精度 160／192、次数 50、panel 8192、深さ 3、一般の分割の式が run4 と一致 |
| run4 回帰（両系統） | 3/3 PASS。**chat の環境（Python 3.13、python-flint 0.9.0）で両系統とも流し直し、門の行が Dig の出力と分数まで同一** |
| 合成区画の対照 | 両系統 PASS。chat が比較を流し直して PASS_NOT_EVIDENCE |
| 端から端までの対照 | 正常終了・強制 ABORT とも両系統 PASS。chat が比較を流し直して SYNTHETIC_COMPARE_PASS_NOT_EVIDENCE |
| 台帳の独立な検算（chat の独自のコード） | 4つの run の連鎖のつながり、前後の同一性、変更ファイル17・run4 の blob 25 の記録、分割（t_e ＝ 993/1024 で N ＝ 16、63/64 で N ＝ 8）、厳密な分数の累積（seed ＋ Δt・Σ max(0, U_j)）が記録の累積上界に等しく負 |

## 参考（設計の変更には使わない）

合成区画では Gt の上界の最大が正（約 8.8〜10.2）で、g は t ＝ 1 に向かって増えている。累積の上界は seed より約 0.017〜0.020 大きいが、負のまま（−0.114、−0.124）である。B_ob が 0 に近い λ（clamp の境に近い区画）では余裕が小さくなる可能性がある。その場合は、深さ3の λ 二分でも門が通らず ABORT になり、方式を変えるには v5 と再 FREEZE が要る。これは事前宣言どおりの扱いである。
