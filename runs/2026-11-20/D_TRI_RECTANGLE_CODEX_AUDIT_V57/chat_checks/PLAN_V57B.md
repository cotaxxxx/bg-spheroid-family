# V57-B 計画（追加。実行前に固定）

層 IV の「零曲線はグラフ」の根拠である central.csv の down_t（∂_t h_i < 0）の箱を抜き取る。
- 抜き取り：surface R、軸 2 の down_t のうち dthi が 0 に最も近い 2 箱と、乱数 2 箱（seed 57）。軸 1 の down_t から乱数 2 箱。計 6 箱。
- 核：`tri2.param_grad("centre", i, ...)`（箱の上での ∂_t の自然な包み。一次）。
- 手順：N ＝ 128、256、512 の順に試す。符号が出なければ形の箱を 4 分割し（深さ 4 まで）、N ＝ 512 で試す。
- 結果：CONFIRMED / NOT_REPRODUCED（反例ではない）/ CONTRADICTED。1 箱あたり 1200 秒。
