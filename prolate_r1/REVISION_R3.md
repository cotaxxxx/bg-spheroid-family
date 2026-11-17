# D-PRO R1 R3 変更記録
DIAGNOSTIC_ONLY / NOT_EVIDENCE

2026-11-17。R2 `bc70e1badbd9a89449cae6707ef37f5e69757a11`からの変更。

| 要求 | 実装 |
|---|---|
| R3-1 | quadrature.make_meshがlambda箱を受け、sigma/lambdaと1/lambdaの小さい方で分割。全APIがlambda箱を渡す。既定は6次・32×64・比1/4 |
| R3-2 | center_bounds.py。Wは128、Phi_sは8小箱。中心で2次Taylor求積、箱上の微分積分で平均値補正、絶対値上界の最大 |
| R3-3 | tests/width_r3.py。指定点と3箱、半幅上限35件＋E_beta参照1件。FAILにも測定値と時間を保存 |
| R3-4 | y座標を保持し、軸セルの径を2(asin(y_hi)-asin(y_lo))の上端へ変更 |

原本の密度・jet/級数・球冠公式、端点/中心差商の定数は変更しない。
R2のtests/run_tests.pyとtests/test_revision_r2.pyも変更しない。
再開runnerはR3計画のハッシュと失敗観測値の保存だけを拡張した。
新しいrun_r3_validation.pyが旧テストと幅検査を一つの再開可能な列に並べる。

中心剰余の分割数と幅基準はPLAN_R3_BEFORE_RUN.mdで事前固定。
幅不足を理由に設定を変更せず、結果はVALIDATION.mdとoutputsに記録する。
新しい数学的包囲の説明はANALYSIS.md §13。R3の独立数学監査はOPEN。

試走前に、参照値の文字列をpython-flint 0.8.0のfmpqへ直接渡せないことを確認した。
テスト用参照値は標準ライブラリFractionで10進文字列を正確な分数へ変換し、
分子・分母からfmpqを作る。浮動小数点を経由しない。
この準備段階の読込修正は、核・設定・基準値の変更ではない。
