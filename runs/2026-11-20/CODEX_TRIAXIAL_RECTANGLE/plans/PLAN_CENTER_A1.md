# 中心の長軸固有値の較正 計画 A1

2026-11-20 / DIAGNOSTIC_ONLY / NOT_EVIDENCE

計画Aは最初の箱を評価する前に、整数4を区間型で割る演算の未実装により停止した。
元のコードをcode/center_interval_A_original.py、空の台帳とエラーをout/へ保存した。
修正はwt=I(4)/pi_interval()/denの1行のみ。計画Aの形状箱、格子、式、精度、判定条件は変えない。
修正後のコードをSHA-256で固定して、全計画を最初から実行する。
