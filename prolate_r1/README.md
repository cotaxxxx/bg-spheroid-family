# D-PRO R1 修正版 R3
**DIAGNOSTIC_ONLY / NOT_EVIDENCE**

2026-11-17。R2の包囲方式を保ち、lambdaに応じたセル分割、中心剰余の
小箱ごとの平均値評価、半幅上限テスト、軸の弧長によるセル条件を追加した版です。
実行済みの範囲・幅・時間・未実行項目は **[VALIDATION.md](VALIDATION.md)** に記録します。
独立した数学監査と研究用PCでのfull実行はDig/chatの工程です。

**試走結果：点Wの半幅は約0.0007023で上限0.05以内ですが、指定箱2は約802万で
上限0.3に未達です。箱の幅の問題が解消した版とは扱いません。**
点・箱各1件の結果であり、未実行の中心経路や他の箱へ一般化しません。

## 版と固定設定

- 修正元R2：`bc70e1badbd9a89449cae6707ef37f5e69757a11`。
- V31監査：`47a4558a9adecea65ddcab038186cc3130bcb849`。
- 新版branch：`codex/d-pro-r1-corotation-r3-20261117`。
- 新版ZIP：`artifacts/D_PRO_R1_COROTATION_R3_20261117.zip`。
- 既定Config：python-flint **0.8.0**、128 bits、6次、初期32×64、径の比1/4。
- 中心剰余：WはR8×tau16、Phi_sはR8。各小箱の中心の求積は2次。

設定は [PLAN_R3_BEFORE_RUN.md](PLAN_R3_BEFORE_RUN.md) で試走前に固定しました。
上限を満たさない測定はFAILとして残し、設定や判定値を緩めません。
軸のy座標、級数・符号付き剰余、球冠上界、端点・中心の差商定数はR2と同じです。
解析上の根拠、複素距離の主張への留保、OPEN項目は [ANALYSIS.md](ANALYSIS.md) §13。

## Dig用の1行

ZIPの対応する`.zip.sha256`を照合し、**新しいフォルダ**へ展開したルートで実行：

```sh
python -m pip install -r prolate_r1/requirements.txt && python -m prolate_r1.verify_manifest && python -m prolate_r1.run_r3_validation --full --resume --out prolate_r1/outputs/dig_r3_full.json
```

R2回帰11件、R3軽量回帰6件、変更していない旧full23ケース、新しい幅36ケースを実行します。
先頭の回帰群は各1ケースとしてrunnerに格納されるため、runner上の計数は61です。
回帰の各テスト名・結果はstdoutログに残ります。quickは旧来の2件のまま別途実行できます。
幅36件には、半幅上限を持つ35件とE_betaの参照照合1件が含まれます。

各ケースの開始・終了・幅・時間・例外スタックを原子的に保存します。
失敗しても後続ケースに進みます。同じ行で再開でき、完了済みケースを再実行しません。
強制終了されたケースは先頭からやり直し、途中の積分セルからの再開ではありません。
ソース・実行環境が変わった場合は別の`--out`が必要です。
runner自身には480秒の打切りを設けていません。外部実行器に時間制限がある場合は、
Dig側で終了まで存続するプロセスとして起動し、保存されたJSONとログを監視してください。
全件が終わるまで終了コード2、完了時は全件成功なら0、失敗があれば1です。
これは動作・幅診断の判定であり、正値認証ではありません。

1ケースずつ進める場合は同じコマンドの末尾に`--max-cases 1`を加えます。
ケース一覧は`python -m prolate_r1.run_r3_validation --full --list-cases`。
`--case N`で実行対象を指定できます。既存のFAILを再試行する場合だけ`--retry-failed`を付けます。
`dig_r3_full.json`と`dig_r3_full.json.cases/`の両方を保存してください。
Codexの出力ファイルをDigの再開先に使わないでください（環境識別が異なります）。

12コアPCでも、この1行のrunner自体は逐次です。複数プロセスで実行する場合は、
異なる`--out`と互いに重ならない`--case`集合を使います。
同じ出力への同時実行はOSロックで拒否します。

## 個別実行

```sh
python -m prolate_r1.tests.run_tests --resume --out prolate_r1/outputs/dig_r3_quick.json
python -m prolate_r1.tests.width_r3 --resume --out prolate_r1/outputs/dig_r3_width.json
python -m prolate_r1.run_diagnostics --fixed27 --output-dir prolate_r1/outputs/dig_r3_fixed27
```

最後の行は全27箱と各中心点の時間・幅を記録する研究用PC向けの別測定です。
旧`run_diagnostics --pilot`はR1/R2の小規模設定を保持しているため、
R3の既定Configでの幅検査とは扱いません。

CodexのR3試走は`tests.width_r3`のID8（lambda=5の点W）とID33（指定箱2）だけです。
他の新しい幅ケースは実行したことにしません。時間外挿は`r3_time_report.py`で
幾何セル数から計算し、[VALIDATION.md](VALIDATION.md)に限界とともに載せます。

## API（名前・引数を維持）

```python
from flint import fmpq as Q
from prolate_r1 import angular_raw, angular_quotient, axis_g, equatorial_phi_s, Config
w = angular_quotient(Q(1,2), Q(1,2), Q(5), angle_kind="tau", config=Config())
raw = angular_raw(Q(1,2), Q(1,2), Q(5), angle_kind="tau")
g = axis_g(Q(1,2), Q(3), config=Config())
phi = equatorial_phi_s(Q(1,4), Q(5), config=Config())
```

幾何入力はfmpqまたはfmpq端点対。beta=pi/2はtau=1で指定します。
rawの微分はtau入力でもbeta微分です。Arbによる包囲を返します。
入力lambdaは球の対照1または[2,5]、R/sは[0,1]、axis_gのtは[0,1)です。
Result.detailsに中心剰余の上界と小箱数を追加しています。

## 原本と封印

R1/R2原本ZIP・既存branchは保持します。新版ZIPはprolate_r1のソース、文書、
実行記録、SHA256SUMSを含み、artifacts、bytecode、実行時lockは含みません。
SHA256SUMSは自分自身とZIPを除く内容を封印し、ZIPは外側の`.zip.sha256`で封印します。
旧outputsとREVISION_R2.mdは履歴であり、R3の最新結果はVALIDATION.mdを参照してください。
この実装は既存コードの再利用であり、clean-roomや独立checkerとは呼びません。
