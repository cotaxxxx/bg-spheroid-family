# 較正 C1A 初回実行前の型の修正

2026-11-20 / DIAGNOSTIC_ONLY / NOT_EVIDENCE

C1の最初の計算は、測度の4/piをPython整数からBoxで割る箇所でTypeErrorとなった。
区間評価の数値行は一つも出ていない。code/calibration_c1_initial.pyとout/calibration_error_c1.jsonに当初のコードと原因を残す。

修正は weight=Box(4)/pi_box()/den とする一箇所のみ。
対象箱、精度、式、角度格子、終了条件はPLAN_CALIBRATION.mdから変更しない。
修正コードのハッシュを本ファイルとともに実行前に固定する。
初回の出力先はcalibration_pilot_c1a.csvとする。
