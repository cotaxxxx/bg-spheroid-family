# D-PRO R1 修正版 R2
**DIAGNOSTIC_ONLY / NOT_EVIDENCE — 新版のPython/Arb実行は未検証**

R1原本とDigのRUN1証拠を保存したまま、次の2点を修正した版です。

1. axis_g の D^(-3) を、正の下界で包んだ逆数 invD の積として評価する。
2. 固定full 23ケースの結果を逐次保存し、未完了ケースから再開する。

詳細は REVISION_R2.md、包囲の導出は ANALYSIS.md §12、
実行状況は VALIDATION.md を参照してください。
R1のquick 2/2とpilot成功は旧版の結果です。R2の実行結果はまだありません。

## 原本・版
R1: `4b7f1f73421f2765d347e4d2ffc9ab004393695c`。
Dig RUN1: `1917e1ab3c22191852385cf8cd3df5f6d9958fb8`。
新版branch: `codex/d-pro-r1-corotation-r2-20261117`。

新版ZIP: `artifacts/D_PRO_R1_COROTATION_R2_20261117.zip`。
対応する `.zip.sha256` を展開前に照合し、**新しいフォルダに展開**してください。
ZIPはソース・文書・未実行記録と SHA256SUMS を含み、
artifacts/ とZIP自身は含みません。
リポジトリ内の旧ZIPは不変です。

## Dig用：小さな回帰検査
展開先またはリポジトリのルートで実行：
```sh
python -m pip install -r prolate_r1/requirements.txt && python -m prolate_r1.verify_manifest && python -m unittest prolate_r1.tests.test_revision_r2 -v
```

11個のR2回帰検査は旧fullとは別です。
報告されたセル、axis_g(1/2,3)、逆数係数、逐次保存、
再開・例外・SIGTERM・識別情報違いを検査します。
SIGTERMの回帰はPOSIXで行い、その他のOSではその1件を明示的にskipします。

## quick と pilot
```sh
python -m prolate_r1.tests.run_tests --resume --out prolate_r1/outputs/dig_r2_quick.json && python -m prolate_r1.run_diagnostics --pilot --output-dir prolate_r1/outputs/r2_pilot
```

quickの2ケースとpilot box13の設定はR1と同じです。

## full：1ケースずつ保存・再開する1行
```sh
python -m prolate_r1.tests.run_tests --full --resume --max-cases 1 --out prolate_r1/outputs/dig_r2_full.json
```

同じ行を繰り返すと、完了済みケースを保存したまま次へ進みます。
全件が揃うまでは終了コード2、全件完了後は0または1です。
この行に `&& 次の処理` を付けると、未完了コード2のため次の処理は走りません。

時間制限なしで全件を続ける場合：
```sh
python -m prolate_r1.tests.run_tests --full --resume --out prolate_r1/outputs/dig_r2_full.json
```

ケース一覧と指定（IDは0から22）：
```sh
python -m prolate_r1.tests.run_tests --full --list-cases
python -m prolate_r1.tests.run_tests --full --resume --case 6 --out prolate_r1/outputs/dig_r2_full.json
```

`dig_r2_full.json` と `dig_r2_full.json.cases/` をまとめて保存してください。
後者には実行前計画、試行ごとの結果JSON、stdout・stderr、
失敗・捕捉できた中断のスタックが入ります。
未完了ケースはケース先頭から再実行します。途中の積分セルからは再開しません。
ソース・Python/python-flint・精度・記録対象の環境変数が変わると、
同じ出力へのresumeを拒否します。その場合は新しい --out を指定します。
元の失敗を再試行する場合は --retry-failed を明示します。
ケースの標本・判定を変更して時間制限に合わせる処理はありません。

## API
```python
from flint import fmpq as Q
from prolate_r1 import angular_raw, angular_quotient, axis_g, equatorial_phi_s, Config
g = axis_g(Q(1,2), Q(3), config=Config())
raw = angular_raw(Q(1,2), Q(1,2), Q(3), angle_kind="tau")
w = angular_quotient((Q(15,16), Q(1)), Q(1), Q(3), angle_kind="tau")
phi = equatorial_phi_s(Q(1,4), Q(3))
```

入力はfmpqの点またはfmpq端点対。lambda=1は球の対照、通常は[2,5]。
R,s∈[0,1]、axis_gはt∈[0,1)。beta=pi/2はtau=1で指定します。
rawの微分はtau入力でもbeta微分です。
Resultの意味と数学的包囲の条件はR1と同じです。

`outputs/CODEX_TEST_STATUS.json`、`CODEX_PILOT_STATUS.json`、
`JS_SOURCE_CHECKS.json` は旧版に含まれた履歴として保持しています。
新版の未実行記録は `outputs/R2_VALIDATION_STATUS.json` です。
このソースの存在や動作成功は、条件 A・Z・C の符号を示しません。
