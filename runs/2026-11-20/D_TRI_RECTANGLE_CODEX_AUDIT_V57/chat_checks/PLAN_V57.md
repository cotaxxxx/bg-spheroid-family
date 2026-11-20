# V57 計画（実行前に固定）— chat による Codex 主矩形報告の独立な抜き取り包み直し

2026-11-20 ／ chat ／ DIAGNOSTIC_ONLY

## 道具
GeoEncloseReader 0.3.0（chat 実装）。新しい三軸の核 `tri2.py`（平均値形式の二次の包み）、`dual.py`、`fiv.py`（binary64 の外向き丸め）。
Codex のコード・核・係数は使わない。比較に使うのは Codex の台帳の数（箱の端点と区間）だけ。

## 抜き取り（決定的。乱数は seed 57）
- S1 層 IV の中心（central.csv、surface R）：(軸1, negative)、(軸2, positive)、(軸2, negative) のそれぞれで、余裕の最も弱い 2 箱と、乱数 2 箱。計 12 箱。
- S2 層 IV の軸端（axis_cover.csv の mode 1 と bfinish.csv、surface R、値の行）：(軸2, negative)、(軸2, positive)、(軸1, negative)、(軸1, positive) のそれぞれで、最弱 1 箱と乱数 2 箱。計 12 箱。軸1 の行は bfinish.csv から取る。
- S3 明示帯の円板（disk.csv）：tau の最弱 2 箱、tau2 の最弱 2 箱。計 4 箱。
- S4 移送（transfer.csv の 194 行すべて）：有理数で再計算。V50 の台帳との一致、誤差の式、残りの余裕 > 0、[2,5]×[0,1] の被覆。V50 の台帳のバイトは、chat が持つ V50 の ZIP と照合する。
- S5 交点：Codex の数（cross.csv）から Krawczyk の包含を chat の有理数コードで再計算する。非区間の Newton は実施済み（chat_v57_numeric.log）。

## 判定の手順（各箱）
1. 箱の中心の点で chat の包みを作り、Codex の [lower, upper] と交わることを確かめる（同じ量であることの確認。交わらなければ CONTRADICTED）。
2. 符号の確認：角度の分割 N ＝ 128 から始める。符号が出なければ、形の項の幅が角度の項の幅より大きく、深さが 8 未満なら 4 分割する。そうでなければ N を倍にする（上限 512）。
3. 結果：CONFIRMED（全部の部分箱で符号が出た）、NOT_REPRODUCED（予算内で出ない。反例ではない）、CONTRADICTED（ある部分箱で、chat の包みが主張と逆の符号に完全に入る）。
4. 予算：1 箱あたり 1800 秒。全体で 2 プロセス。
